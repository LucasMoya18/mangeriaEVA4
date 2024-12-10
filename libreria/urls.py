from django.urls import path
from django.conf.urls import handler404
from . import views
from libreria.views import pagina_no_encontrada

handler404 = 'libreria.views.pagina_no_encontrada'

urlpatterns = [
    path('', views.lista_mangas, name='lista_mangas'),
    path('manga/<int:manga_id>/', views.detalle_manga, name='detalle_manga'),
    path('agregar-al-carrito/<int:manga_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.carrito, name='carrito'),
    path('eliminar-del-carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('actualizar-carrito/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    path('vender/', views.vender_manga, name='vender_manga'),
    path('buscar-jikan/', views.buscar_jikan, name='buscar_jikan'),
    path('perfil-usuario/', views.perfil_usuario, name='perfil_usuario'),
    path('editar-manga/<int:manga_id>/', views.editar_manga, name='editar_manga'),
    path('eliminar-manga/<int:manga_id>/', views.eliminar_manga, name='eliminar_manga'),
    path('registro/', views.registro, name='registro'),
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('perfil/', views.perfil, name='perfil'),
]
