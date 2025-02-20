from django.contrib import admin
from .models import Orden, DetalleOrden

# Register your models here.
@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'valor_total', 'f_creacion', 'estado')


@admin.register(DetalleOrden)
class DetalleOrdenAdmin(admin.ModelAdmin):
    list_display = ('orden', 'producto', 'cantidad', 'precio')

