from django.urls import path
from .views import *
from app.controller import cart, checkout

urlpatterns = [
    path('',            home,       name="home"),
    path('contacto/',   contacto,   name="contacto"),
    path('galeria/',    galeria,    name="galeria"),
    path('agregar-producto/',    agregar_producto,    name="agregar_producto"),
    path('listar-productos/',    listar_productos,    name="listar_productos"),
    path('modificar-producto/<id>/',    modificar_producto,    name="modificar_producto"),
    path('eliminar-producto/<id>/',    eliminar_producto,    name="eliminar_producto"),
    path('detalle-producto/<int:pk>/',    DetalleLibro.as_view(),    name="detalle_libro"),
    path('agregar-tienda/',    agregar_tienda,    name="agregar_tienda"),
    path('listar-tiendas/',    listar_tiendas,    name="listar_tiendas"),
    path('modificar-tienda/<id>/',    modificar_tienda,    name="modificar_tienda"),
    path('eliminar-tienda/<id>/',    eliminar_tienda,    name="eliminar_tienda"),
    path('agregar-existencias/<id>/<id2>/',    agregar_existencias,    name="agregar_existencias"),
    path('aumentar-existencias/<id>/<id2>/<id3>',    aumentar_existencias_t,    name="aumentar_existencias"),
    path('eliminar-existencias/<id>/<id2>/<id3>',    eliminar_existencias_t,    name="eliminar_existencias"),
    path('listar-existencias/<id>/',    listar_existencias,    name="listar_existencias"),
    path('escoger-existencia/<id>/',    escoger_existencias,    name="escoger_existencia"),
    path('registro/',    registro,    name="registro"),
    path('ver-perfil/',    ver_perfil,    name="ver_perfil"),
    path('modificar-perfil/',    modificar_perfil,    name="modificar_perfil"),
    path('eliminar-perfil/<int:pk>/',    eliminar_perfil.as_view(),    name="eliminar_perfil"),
    path('cambiar-contraseña',    cambiar_contrasenia.as_view(),    name="cambiar_contraseña"),
    path('add-to-cart', cart.addtocart, name="addtocart"),
    path('cart', cart.viewcart, name="cart"),
    path('update-cart', cart.updatecart, name="updatecart"),
    path('delete-cart-item', cart.deletecartitem, name="deletecartitem"),
    path('checkout', checkout.index, name="checkout"),
    path('listar-tarjetas/',    listar_tarjetas,    name="listar_tarjetas"),
    path('agregar-saldo/<id>',    agregar_saldo,    name="agregar_saldo"),
    path('eliminar-tarjeta/<id>',    eliminar_tarjeta,    name="eliminar_tarjeta"),
    path('tarjeta/',    tarjeta,    name="tarjeta"),
    path('forum/', forums, name="forum"),
    path('addInForum/',addInForum,name='addInForum'),
    path('addInDiscussion/',addInDiscussion,name='addInDiscussion'),
    path('noticias/', noticia, name="noticia"),
    path('noticia-producto/<int:pk>/', NoticiaProducto.as_view(), name="noticia_producto")
    
]