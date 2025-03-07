from django.db import models
from django.utils.text import slugify  # Importa slugify para generar slugs automáticamente
from django.urls import reverse
from django.forms import model_to_dict

import uuid

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Genera el slug automáticamente si no se proporciona uno
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
 

class Producto(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)
    categorias = models.ManyToManyField(Categoria, related_name="productos", verbose_name="Categoría")
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True, verbose_name="Imágen")
    favoritos = models.ManyToManyField('clientes.Cliente', related_name='favoritos', through='ProductosFavoritos')
    f_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    f_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    class Meta:
        ordering = ['-f_actualizacion']

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Genera el slug automáticamente si no se proporciona uno
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("shop:detalle-producto", args=[self.slug])

    def get_imagen(self):
        if self.imagen:
            imagen = self.imagen.url
        else:
            imagen = '/static/img/default.png'
        return imagen
    
    def json_producto(self):
        producto = model_to_dict(self, exclude=["f_creacion", "f_actualizacion", "favoritos"])
        producto["imagen"] = self.get_imagen()
        producto["disponible"] = "Disponible" if self.disponible else "No disponible"
        producto["categorias"] = [cat.nombre for cat in self.categorias.all()]
        return producto
    
    def lista_categorias(self):
        return ", ".join(categoria.nombre for categoria in self.categorias.all())
    lista_categorias.short_description = 'Categorías'

    def total_favoritos(self):
        return self.favoritos.all().count()
    total_favoritos.short_description = 'Favoritos'
    

class ProductosFavoritos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE, related_name="favoritos_asociados")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="relaciones_favoritas")
    f_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-f_creacion']
        constraints = [
            models.UniqueConstraint(fields=['cliente', 'producto'], name='unique_cliente_producto_favorito')
        ]

    def __str__(self):
        return f"{self.cliente}: {self.producto}"
    

