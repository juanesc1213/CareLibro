from django.contrib import admin
from .models import Editorial, Producto,Contacto, PerfilUsuario

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

admin.site.register(PerfilUsuario)
admin.site.register(Editorial)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Contacto, ContactoAdmin)