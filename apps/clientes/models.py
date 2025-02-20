from django.db import models

from apps.usuarios.models import Usuario

import uuid

# Create your models here.
class Cliente(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=100)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cliente')
    nombre_completo = models.CharField(max_length=100, blank=True, null=True)
    identificacion = models.CharField(max_length=10, verbose_name='Doc. Identificación', blank=True, null=True)
    telefono = models.CharField(max_length=10, verbose_name='Teléfono', blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=100, verbose_name='Dirección', blank=True, null=True)
    f_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento', blank=True, null=True)
    f_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    f_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    def __str__(self):
        return self.nombre_completo
    
    class Meta:
        ordering = ['nombre_completo']
