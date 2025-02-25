from django.contrib import admin

from .models import Producto, Categoria, ProductosFavoritos

# Register your models here.
@admin.register(Producto)
class Producto(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'disponible', 'lista_categorias', 'total_favoritos', 'f_creacion')

    # @admin.display(description="Favoritos")
    # def favoritos(self, obj):
    #     return obj.favoritos.all().count()

admin.site.register(Categoria)

@admin.register(ProductosFavoritos)
class ProductosFavoritosAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'producto', 'f_creacion')
