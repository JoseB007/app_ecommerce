from django.db.models.signals import post_delete
from django.dispatch import receiver


from .models import Carrito, ItemCarrito

@receiver(post_delete, sender=ItemCarrito)
def actualizar_total_despues_de_eliminar(sender, instance, **kwargs):
    carrito = instance.carrito
    carrito.calcular_total()