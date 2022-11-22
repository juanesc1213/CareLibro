from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display    = ["nombre", "precio", "nuevo", "editorial","autor","genero","issn"]
    list_editable   = ["precio"]
    search_fields   = ["nombre"]
    list_filter     = ["editorial", "nuevo"]
    list_per_page   = 10

class ContactoAdmin(admin.ModelAdmin):
    list_display    = ["nombre", "tipo_consulta"]
    list_filter     = ["tipo_consulta"]
    list_per_page   = 10

class PerfilInline(admin.StackedInline):
    model= PerfilUsuario
    can_delete = False
    exclude = ['generos_preferencia','direccion_correspondencia']

class AdminCustom(UserAdmin):
    inlines = (PerfilInline,)

admin.site.unregister(User)
admin.site.register(User, AdminCustom)
admin.site.register(forum)
admin.site.register(Discussion)
admin.site.register(Tarjeta)
admin.site.register(Existencias)
admin.site.register(Tienda)
admin.site.register(Carrito)
admin.site.register(PerfilUsuario)
admin.site.register(Editorial)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Contacto, ContactoAdmin)
admin.site.register(Orden)
admin.site.register(OrdenItem)
admin.site.register(noticia)
admin.site.register(Reserva)