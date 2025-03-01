from django import forms

from .models import Cliente

from apps.usuarios.models import Usuario

class FormCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        # exclude = ['usuario']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.visible_fields():
            campo.field.widget.attrs['class'] = 'form-control'
            campo.field.widget.attrs['placeholder'] = f"Ingrese el {campo.label.lower()} del cliente"
        
        self.fields['identificacion'].widget.attrs['placeholder'] = 'Ingrese el documento de identificación del cliente'
        self.fields['direccion'].widget.attrs['placeholder'] = 'Ingrese la dirección del cliente'
        self.fields['f_nacimiento'].widget.attrs['placeholder'] = 'Ingrese la fecha de nacimiento del cliente (dd/mm/yy)'

        if not self.instance._state.adding: # Solo ejecuta si el objeto YA EXISTE en la BD
            self.fields['usuario'].initial = self.instance.usuario
            self.fields['usuario'].disabled = True
        else:
            self.fields['usuario'].queryset = Usuario.objects.exclude(pk__in=Cliente.objects.values_list('usuario'))
        
        
