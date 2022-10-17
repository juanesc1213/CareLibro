from django.urls import path
from .views import *


urlpatterns = [
    path('',            home,       name="home"),
    path('contacto/',   contacto,   name="contacto"),
    path('galeria/',    galeria,    name="galeria"),
    path('agregar-producto/',    agregar_producto,    name="agregar_producto"),
    path('listar-productos/',    listar_productos,    name="listar_productos"),
    path('modificar-producto/<id>/',    modificar_producto,    name="modificar_producto"),
    path('eliminar-producto/<id>/',    eliminar_producto,    name="eliminar_producto"),
    path('registro/',    registro,    name="registro"),
    path('ver-perfil/',    ver_perfil,    name="ver_perfil"),
    path('modificar-perfil/',    modificar_perfil,    name="modificar_perfil"),
    path('eliminar-perfil/<int:pk>/',    eliminar_perfil.as_view(),    name="eliminar_perfil"),
    path('cambiar-contraseña',    cambiar_contrasenia.as_view(),    name="cambiar_contraseña"),
]