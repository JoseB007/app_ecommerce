from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, View
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator

from .models import Producto
from .forms import FormProducto
# Create your views here.
class AgregarProductoView(LoginRequiredMixin, CreateView):
    model = Producto
    template_name = 'crear_producto.html'
    form_class = FormProducto
    success_url = reverse_lazy('productos:lista-productos')
    msj_exito = "Producto agregado correctamente."

    def _agregar_textos_contexto(self, context):
        # Agrega los textos estáticos al contexto.
        context.update({
            'action': "agregar",
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self._agregar_textos_contexto(context)
        context['url_redireccion'] = self.success_url
        return context
    
    def post(self, request, *args, **kwargs):
        # Maneja las solicitudes POST y ejecuta la acción correspondiente
        try:
            action = request.POST.get('action')
            if action == "agregar":
                return self._agregar_registro(request)
                
            return self._respuesta_error("No se ha ingresado ninguna opción.")
        
        except Exception as e:
            return self._respuesta_error(str(e))

    def _agregar_registro(self, request):
        # Maneja la acción de agregar un nuevo registro
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, self.msj_exito)
            return JsonResponse({})
    
        return self._respuesta_error(form.errors)

    def _respuesta_error(self, mensaje):
        # Retorna una respuesta JSON con un mensaje de error
        return JsonResponse({'error': mensaje})
    

class ActualizarProductoView(LoginRequiredMixin, UpdateView):
    model = Producto
    template_name = "crear_producto.html"
    form_class = FormProducto
    success_url = reverse_lazy('productos:lista-productos')
    msj_exito = "Producto actualizado correctamente."

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def _agregar_textos_contexto(self, context):
        # Agrega los textos estáticos al contexto.
        context.update({
            'action': "actualizar",
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self._agregar_textos_contexto(context)
        context['url_redireccion'] = self.success_url
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            action = request.POST.get('action')
            if action == "actualizar":
                return self._agregar_registro(request)
            
            return self._respuesta_error("No se ha ingresado ninguna opción.")

        except Exception as e:
            return self._respuesta_error(str(e))

    def _agregar_registro(self, request):
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, self.msj_exito)
            return JsonResponse({})
        
        return self._respuesta_error(form.errors)

    def _respuesta_error(self, mensaje):
        # Retorna una respuesta JSON con un mensaje de error
        return JsonResponse({'error': mensaje}) 


class ListarProductosView(ListView):
    model = Producto
    template_name = "lista_producto.html"
    context_object_name = "productos"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        prod_a_buscar = self.request.GET.get('ref')
        if prod_a_buscar:
            queryset = queryset.filter(nombre__icontains=prod_a_buscar)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self._agregar_textos_contexto(context)
        context['lista_paginas'] = self._generar_lista_paginas(self.get_queryset())
        return context
        
    def _agregar_textos_contexto(self, context):
        # Agrega los textos estáticos al contexto.
        context.update({
            'titulo_tabla': "Lista de productos",
            'action': "mostrar",
            'accion_btn': "Agregar producto",
        })
    
    def _generar_lista_paginas(self, queryset):
        # Genera la lista de páginas a mostrar en la paginación
        paginador = Paginator(queryset, self.paginate_by)
        num_pag = int(self.request.GET.get('page', 1))
    
        lista_paginas = list(paginador.page_range)
        lista_menor = [x for x in lista_paginas if x <= num_pag]
        lista_mayor = [x for x in lista_paginas if x > num_pag]
        
        return sorted(lista_menor[-3:] + lista_mayor[:2])
        
    def _respuesta_error(self, mensaje):
        return JsonResponse({'error': mensaje}) 
        



