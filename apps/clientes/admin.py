from django.contrib import admin

from .models import Cliente, Carrito, ItemCarrito

# Register your models here.
@admin.register(Cliente)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'identificacion', 'telefono', 'email', 'direccion', 'f_creacion')

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'f_creacion', 'f_actualizacion')


@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad', 'f_creacion')