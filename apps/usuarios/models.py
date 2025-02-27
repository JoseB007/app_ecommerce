from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid

# Create your models here.
# Asegurar que Django use el modelo personalizado Usuario en lugar del modelo User por defecto.
# AUTH_USER_MODEL = 'usuarios.Usuario'
class Usuario(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")

    def __str__(self):
        return self.username
    
    def get_avatar(self):
        avatar = '/static/img/avatars/default.png'
        if self.avatar:
            avatar = self.avatar.url
        return avatar
    
    def get_nombre_completo(self):
        if self.first_name:
            nombre_completo = self.get_full_name()
        nombre_completo = self.username
        return nombre_completo
    
    def save(self, *args, **kwargs):
        if not self._state.adding:  # Solo ejecuta esto si el objeto usuario YA EXISTE en la BD
            user = Usuario.objects.filter(pk=self.pk).first()
            if user and user.password != self.password:
                self.set_password(self.password)
        else:
            # Si es un objeto usuario nuevo, ciframos la contraseña antes de guardar
            self.set_password(self.password)

        super().save(*args, **kwargs)
    
