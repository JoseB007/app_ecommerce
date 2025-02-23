from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .models import Usuario
from apps.clientes.models import Cliente, Carrito


@receiver(post_save, sender=Usuario)
def crear_cliente(sender, instance, created, **kwargs):
    usuario = instance
    if created:
        cliente = Cliente.objects.create(usuario=usuario)
        cliente.nombre_completo = usuario.username
        cliente.save()


@receiver(post_save, sender=Cliente)
def crear_carrito(sender, instance, created, **kwargs):
    cliente = instance
    if created:
        Carrito.objects.create(cliente=cliente)


