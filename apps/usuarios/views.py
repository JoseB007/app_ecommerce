from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.messages import get_messages
from django.urls import reverse_lazy, reverse

from .models import Usuario

from apps.productos.models import Producto, ProductosFavoritos
from core.mixins import LoginRequiredJSONMixin

# Create your views here.
class DetallePerfilView(LoginRequiredMixin, generic.DetailView):
    model = Usuario
    template_name = 'perfil.html'
    context_object_name = 'usuario'

    def get_object(self, queryset = ...):
        perfil_usuario = self.request.user
        return perfil_usuario
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prod_favoritos'] = self.get_object().cliente.favoritos.all().order_by('f_creacion')[:3]
        return context


class AgregarProdFavoritoView(LoginRequiredJSONMixin, generic.View):
    msj_exito = "Producto agregado a favoritos."
    msj_info = "Se ha eliminado un producto de favoritos."
    next_url = None

    def _get_url(self, prod):
        # Devuelve la URL del producto basado en su slug
        return reverse("shop:detalle-producto", kwargs={"slug": prod.slug})

    def dispatch(self, request, *args, **kwargs):
        # Captura el producto desde POST y almacena su URL
        id_producto = request.POST.get('id_producto')
        if not id_producto:
            return JsonResponse({'error': 'ID de producto no proporcionado'}, status=400)  # Manejo de error

        prod = get_object_or_404(Producto, id=id_producto)
        self.next_url = self._get_url(prod)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}

        # Obtener el producto
        producto = get_object_or_404(Producto, id=self.request.POST.get('id_producto'))

        # Obtener el cliente
        try:
            cliente = request.user.cliente
        except AttributeError:
            return JsonResponse({'error': 'El usuario no tiene un cliente asociado.'})
        
        try:
            datos = self.add_prod_fav(cliente, producto)
                
            storage = get_messages(request)
            lista_mensajes = [(message.tags, message.message) for message in storage]

            data['message'] = lista_mensajes
            data['txt_button'] = datos['txt_button']
        except Exception as e:
            data['error'] = str(e)
            return JsonResponse(data)
        
        return JsonResponse(data)
    
    def add_prod_fav(self, cliente, producto):
        datos = {}
        # Obtener el producto favorito o crear uno
        prod_favorito, prod_creado = ProductosFavoritos.objects.get_or_create(cliente=cliente, producto=producto)

        # Si el prod ya existe, eliminar de favoritos
        if not prod_creado:
            prod_favorito.delete()
            messages.info(self.request, self.msj_info)
            datos['txt_button'] = "Añadir a favoritos"
        else:
            messages.success(self.request, self.msj_exito)
            datos['txt_button'] = "Eliminar de favoritos"
        
        return datos
    

class EliminarProdFavorito(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.headers.get("HX-Request") == 'true':
            # Obtener el producto
            producto = get_object_or_404(Producto, id=self.kwargs.get('pk'))

            # Obtener el cliente
            try:
                cliente = request.user.cliente
            except AttributeError:
                return JsonResponse({'error': 'El usuario no tiene un cliente asociado'})
            
            try:
                prod_favorito = ProductosFavoritos.objects.get(cliente=cliente, producto=producto)
                prod_favorito.delete()
            except Exception as e:
                return JsonResponse({'error': str(e)}) 

            context = {
                'prod_favoritos': cliente.favoritos.all()[:3],
                'usuario': request.user,
            }
            
            # Renderizar la plantilla
            return render(request, 'snippets/snippet_favorito.html', context)
        
        return super().get(request, *args, **kwargs)



