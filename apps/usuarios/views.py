from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Usuario

# Create your views here.
class DetallePerfilView(LoginRequiredMixin, generic.DetailView):
    model = Usuario
    template_name = 'perfil.html'
    context_object_name = 'perfil'

    def get_object(self, queryset = ...):
        perfil_usuario = self.request.user
        return perfil_usuario

