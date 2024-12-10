from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('staff', 'Empleado'),
        ('user', 'Usuario'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='user', verbose_name='Rol')

    def __str__(self):
        return self.username
    

class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    mal_id = models.IntegerField(unique=True, null=True, blank=True, verbose_name='ID MAL') 

    def __str__(self):
        return self.nombre


class Manga(models.Model):
    titulo = models.CharField(max_length=200,default='', verbose_name='Título')
    sinopsis = models.TextField(default='', verbose_name='Sinopsis')
    descripcion = models.TextField(default='',verbose_name='Descripción del artículo')
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock')
    autor = models.CharField(max_length=200, verbose_name='Autor')
    generos = models.ManyToManyField(Genero, related_name='mangas', verbose_name='Géneros')
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='mangas_en_venta', 
        verbose_name='Vendedor',
        default=1
    )
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name='Actualizado en')

    def __str__(self):
        return self.titulo


class ImagenManga(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='imagenes', verbose_name='Manga')
    imagen = models.ImageField(upload_to='imagenes/', verbose_name='Imagen')


class Review(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='resenas', verbose_name='Manga')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario')
    calificacion = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        verbose_name='Calificación',
        default=1
    )
    comentario = models.TextField(default='',verbose_name='Comentario')
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')

    class Meta:
        unique_together = ('manga', 'usuario')


class ItemCarrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario')
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, verbose_name='Manga')
    cantidad = models.PositiveIntegerField(default=1, verbose_name='Cantidad')

    class Meta:
        unique_together = ('usuario', 'manga')


class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario')
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio Total')


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items', verbose_name='Pedido')
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, verbose_name='Manga')
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
