from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import FormularioCreacionUsuarioPersonalizado, FormularioAutenticacionPersonalizado
from django.db.models import Q, Avg, Count
from .models import Manga, Genero, ItemCarrito, Pedido, ItemPedido, ImagenManga
from .forms import FormularioManga, FormularioReview
from googletrans import Translator
import requests

def registro(request):
    if request.method == 'POST':
        formulario = FormularioCreacionUsuarioPersonalizado(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            login(request, usuario)
            return redirect('lista_mangas')
    else:
        formulario = FormularioCreacionUsuarioPersonalizado()
    return render(request, 'sesion/registro.html', {'form': formulario})

def iniciar_sesion(request):
    if request.method == 'POST':
        formulario = FormularioAutenticacionPersonalizado(data=request.POST)
        if formulario.is_valid():
            usuario = formulario.get_user()
            login(request, usuario)
            return redirect('lista_mangas')
    else:
        formulario = FormularioAutenticacionPersonalizado()
    return render(request, 'sesion/login.html', {'form': formulario})

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('lista_mangas')

@login_required
def inicio(request):
    return render(request, 'manga/inicio.html')

@login_required
def perfil(request):
    return render(request, 'manga/perfil.html')

def lista_mangas(request):
    mangas = Manga.objects.annotate(
        promedio_calificacion=Avg('resenas__calificacion'),
        cantidad_resenas=Count('resenas')
    )
    generos = Genero.objects.all()

    titulo = request.GET.get('titulo')
    genero = request.GET.get('genero')
    orden_precio = request.GET.get('orden_precio')
    autor = request.GET.get('autor')

    if titulo:
        mangas = mangas.filter(titulo__icontains=titulo)
    if genero:
        mangas = mangas.filter(generos__nombre=genero)
    if autor:
        mangas = mangas.filter(autor__icontains=autor)
    if orden_precio:
        if orden_precio == 'asc':
            mangas = mangas.order_by('precio')
        elif orden_precio == 'desc':
            mangas = mangas.order_by('-precio')

    contexto = {
        'mangas': mangas,
        'generos': generos,
    }
    return render(request, 'manga/lista_mangas.html', contexto)

def detalle_manga(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id)
    if request.method == 'POST':
        formulario = FormularioReview(request.POST)
        if formulario.is_valid():
            resena = formulario.save(commit=False)
            resena.manga = manga
            resena.usuario = request.user
            resena.save()
            return redirect('detalle_manga', manga_id=manga.id)
    else:
        formulario = FormularioReview()
    return render(request, 'manga/detalle_manga.html', {'manga': manga, 'formulario': formulario})

@login_required
def agregar_al_carrito(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id)
    item_carrito, creado = ItemCarrito.objects.get_or_create(usuario=request.user, manga=manga)
    if not creado:
        item_carrito.cantidad += 1
        item_carrito.save()
    return redirect('carrito')

@login_required
def carrito(request):
    items_carrito = ItemCarrito.objects.filter(usuario=request.user)
    items_with_subtotals = []
    total = 0

    for item in items_carrito:
        subtotal = item.manga.precio * item.cantidad
        items_with_subtotals.append({
            'item': item,
            'subtotal': subtotal
        })
        total += subtotal

    return render(request, 'manga/carrito.html', {'cart_items': items_with_subtotals, 'total': total})

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, usuario=request.user)
    item.delete()
    return redirect('carrito')

@login_required
def actualizar_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, usuario=request.user)
    cantidad = int(request.POST.get('cantidad', 1))
    if cantidad > 0:
        item.cantidad = cantidad
        item.save()
    else:
        item.delete()
    return redirect('carrito')

@login_required
def finalizar_compra(request):
    items_carrito = ItemCarrito.objects.filter(usuario=request.user)


    items_with_subtotals = []
    total = 0

    for item in items_carrito:
        subtotal = item.manga.precio * item.cantidad
        items_with_subtotals.append({
            'item': item,
            'subtotal': subtotal
        })
        total += subtotal
    if request.method == 'POST':
        pedido = Pedido.objects.create(usuario=request.user, precio_total=total)
        for item in items_carrito:
            ItemPedido.objects.create(
                pedido=pedido,
                manga=item.manga,
                cantidad=item.cantidad,
                precio=item.manga.precio
            )
            item.manga.stock -= item.cantidad
            item.manga.save()
        items_carrito.delete()
        return render(request, 'manga/confirmacion.html', {'pedido': pedido})

    return render(request, 'manga/checkout.html', {'cart_items': items_with_subtotals, 'total': total})




@login_required
def vender_manga(request):
    respuesta = requests.get('https://api.jikan.moe/v4/genres/manga')
    datos_generos = respuesta.json()['data']
    generos = [(genero['mal_id'], genero['name']) for genero in datos_generos]
    generos = Genero.objects.all()

    translator = Translator()

    if request.method == 'POST':
        formulario = FormularioManga(request.POST, request.FILES)
        generos_seleccionados = request.POST.getlist('generos')
        
        if formulario.is_valid():
            manga = formulario.save(commit=False)
            manga.vendedor = request.user
            manga.save()
            formulario.save_m2m()
            
            for id_genero in generos_seleccionados:
                genero = Genero.objects.get(id=id_genero)
                manga.generos.add(genero)

            imagenes = request.FILES.getlist('imagenes')
            for imagen in imagenes:
                ImagenManga.objects.create(manga=manga, imagen=imagen)

            return redirect('detalle_manga', manga_id=manga.id)
    else:
        titulo = request.GET.get('titulo', '')
        sinopsis_ingles = request.GET.get('descripcion', '')
        autor = request.GET.get('autor', '')
        generos_seleccionados = request.GET.getlist('generos', '')

        if sinopsis_ingles:
            traduccion = translator.translate(sinopsis_ingles, src='en', dest='es')
            sinopsis_espanol = traduccion.text
        else:
            sinopsis_espanol = ''

        datos_iniciales = {
            'titulo': titulo,
            'sinopsis': sinopsis_espanol,
            'autor': autor,
            'generos': generos_seleccionados
        }
        formulario = FormularioManga(initial=datos_iniciales)

    return render(request, 'manga/vender_manga.html', {'form': formulario, 'genres': generos})


@login_required
def buscar_jikan(request):
    consulta = request.GET.get('q')
    if consulta:
        respuesta = requests.get(f'https://api.jikan.moe/v4/manga?q={consulta}')
        resultados = respuesta.json()['data']
        return render(request, 'manga/resultados_jikan.html', {'results': resultados})
    return render(request, 'manga/buscar_jikan.html')

@login_required
def perfil_usuario(request):
    usuario = request.user
    compras = Pedido.objects.filter(usuario=usuario)
    ventas = Manga.objects.filter(vendedor=usuario)
    return render(request, 'manga/perfil_usuario.html', {
        'usuario': usuario,
        'compras': compras,
        'ventas': ventas
    })

@login_required
def editar_manga(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id, vendedor=request.user)
    generos = Genero.objects.all()
    generos_seleccionados = manga.generos.values_list('id', flat=True)
    
    if request.method == 'POST':
        formulario = FormularioManga(request.POST, request.FILES, instance=manga)
        if formulario.is_valid():
            manga_actualizado = formulario.save()
            manga_actualizado.generos.set(request.POST.getlist('generos'))
            return redirect('detalle_manga', manga_id=manga.id)
    else:
        formulario = FormularioManga(instance=manga)
    
    return render(request, 'manga/editar_manga.html', {
        'form': formulario,
        'manga': manga,
        'generos': generos,
        'generos_seleccionados': generos_seleccionados
    })

@login_required
def eliminar_manga(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id)
    if request.method == 'POST':
        manga.delete()
        return redirect('perfil_usuario')
    return render(request, 'manga/eliminar_manga.html', {'manga': manga})

def pagina_no_encontrada(request, exception=None):
    return redirect('iniciar_sesion')
