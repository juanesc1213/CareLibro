from django.contrib import admin
from .models import Editorial, Producto,Contacto, PerfilUsuario, forum, Discussion
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

class PerfilUsuarioInLine(admin.StackedInline):
    model = PerfilUsuario
    can_delete: False
    verbose_name_plural = "Perfiles"

class CustomPerfilAdmin (UserAdmin):
    inlines= (PerfilUsuarioInLine, )

admin.site.unregister(User)

admin.site.register(User,CustomPerfilAdmin)
admin.site.register(Editorial)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Contacto, ContactoAdmin)
admin.site.register(forum)
admin.site.register(Discussion)