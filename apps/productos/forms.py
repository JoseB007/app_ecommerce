from django.forms import *

from .models import Producto

class FormProducto(ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"
        labels = {
            'descripcion': 'Descripción',
        }
        widgets = {
            'descripcion': Textarea(
                attrs={
                    'rows': 3,
                    'cols': 3,
                }
            )
        }
        exclude = ["slug", "disponible", "favoritos"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.visible_fields():
            campo.field.widget.attrs['autocomplete'] = 'off'
            campo.field.widget.attrs['placeholder'] = f"{campo.label} del producto"
            campo.field.widget.attrs['class'] = 'form-control'


class BuscarProducto(Form):
    ref = CharField(max_length=150)

    ref.widget.attrs.update({
        'class': 'form-control',
        'placeholder': "Ingresar producto...",
    })