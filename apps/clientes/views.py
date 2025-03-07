from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib import messages
from django.db.models import Sum, Count
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView, View, ListView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import get_messages
from django.core.paginator import Paginator


from .models import Cliente, Carrito, ItemCarrito
from .forms import FormCliente

from apps.productos.models import Producto
from core.mixins import LoginRequiredJSONMixin

# Create your views here.
class AgregarItemCarritoView(LoginRequiredJSONMixin, View):
    msj_exito = 'Producto agregado al carrito.'
    next_url = None

    def _get_url(self, producto):
        return reverse("shop:detalle-producto", kwargs={'slug': producto.slug})

    def dispatch(self, request, *args, **kwargs):
        id_producto = self.kwargs['pk']
        if not id_producto:
            return JsonResponse({'error': 'ID de producto no proporcionado'}, status=400)
        
        producto = get_object_or_404(Producto, id=id_producto)
        self.next_url = self._get_url(producto)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}

        # Obtener el producto o devolver un 404 si no existe
        producto = get_object_or_404(Producto, id=kwargs['pk'])

        # Obtener la cantidad del formulario (valor predeterminado: 1)
        try:
            cantidad = int(request.POST.get('cantidad', 1))
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser un número positivo.")
        except ValueError as e:
            data['error'] = str(e)
            return JsonResponse(data)

        # Obtener el carrito del cliente
        cliente = request.user.cliente
        carrito, carrito_creado = Carrito.objects.get_or_create(cliente=cliente)

        # Agregar o actualizar el ítem en el carrito
        data = self._agregar_item_carrito(producto, cantidad, carrito)

        return JsonResponse(data)
    
    def _agregar_item_carrito(self, producto, cantidad, carrito):
        data = {}
        try:
            item, item_creado = ItemCarrito.objects.get_or_create(
                carrito=carrito,
                producto=producto,
                defaults={'cantidad': cantidad}  # Valor predeterminado si se crea
            )

            # Si el ítem ya existe, incrementar la cantidad
            if not item_creado:
                item.cantidad += cantidad
                item.save()

            carrito.calcular_total()

            # Mensaje de éxito
            messages.success(self.request, self.msj_exito)
            storage = get_messages(self.request)
            lista_mensajes = [(message.tags, message.message) for message in storage]            
            
            # Datos para la respuesta JSON
            data['item'] = item.producto.json_producto()
            data['carrito_items'] = carrito.productos.count()
            data['message'] = lista_mensajes
        except Exception as e:
            data['error'] = str(e)
            return JsonResponse(data)
        
        return data


class ActualizarItemCarrito(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Verificar si es una solicitud HTMX
        if self.request.headers.get('HX-Request') != 'true':
            return super().get(request, *args, **kwargs)

        try:
            # Obtener el carrito del cliente
            carrito = request.user.cliente.carrito
        except AttributeError:
            return JsonResponse({'error': 'El usuario no tiene un cliente o carrito asociado'}, status=400)

        try:
            # Obtener el producto
            producto = Producto.objects.get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'El producto no existe'}, status=404)

        # Obtener la acción
        action = self.request.GET.get('action')
        if not action:
            return JsonResponse({'error': 'Acción no especificada'}, status=400)

        # Realizar la acción correspondiente
        item = None
        if action == 'incrementar':
            item = self.incrementar_item(carrito, producto)
        elif action == 'decrementar':
            item = self.decrementar_item(carrito, producto)
        else:
            return JsonResponse({'error': 'Acción no válida'}, status=400)

        # Recalcular el total del carrito
        carrito.calcular_total()

        # Calcular el total de productos en el carrito actual
        total_prod = carrito.items.aggregate(total_prod=Sum('cantidad'))['total_prod'] or 0

        # Preparar el contexto para la plantilla
        context = {
            'item': item,
            'carrito': carrito,
            'total_prod': total_prod,
        }

        # Renderizar la plantilla
        return render(request, 'snippets/snippet_carrito.html', context)
    
    def incrementar_item(self, carrito, producto):
        item, item_creado = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': 1}
        )
        if not item_creado:
            item.cantidad += 1
            item.save()

        return item
    
    def decrementar_item(self, carrito, producto):
        item = ItemCarrito.objects.get(carrito=carrito, producto=producto)
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()

        return item


class EliminarItemCarrito(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Verificar si es una solicitud HTMX
        if self.request.headers.get('HX-Request') != 'true':
            return super().get(request, *args, **kwargs)
        
        try:
            # Obtener el carrito del cliente
            carrito = request.user.cliente.carrito
        except AttributeError:
            return JsonResponse({'error': 'El usuario no tiene un cliente o carrito asociado'}, status=400)
        
        # Obtener la acción
        action = self.request.GET.get('action')
        if not action:
            return JsonResponse({'error': 'Acción no especificada'}, status=400)
        
        if action == 'eliminar':
            item = get_object_or_404(ItemCarrito, id=self.kwargs.get('pk'))
            item.delete()
        
        # Recalcular el total del carrito
        carrito.calcular_total()

        # Calcular el total de productos en el carrito actual
        total_prod = carrito.items.aggregate(total_prod=Sum('cantidad'))['total_prod'] or 0

        # Preparar el contexto para la plantilla
        context = {
            'carrito': carrito,
            'total_prod': total_prod,
        }

        # Renderizar la plantilla
        return render(request, 'snippets/snippet_actualizar-carrito.html', context)


class CarritoView(LoginRequiredMixin, DetailView):
    model = Carrito
    template_name = "carrito.html"
    context_object_name = "carrito"

    def get_object(self, queryset = ...):
        cliente = self.request.user.cliente
        return cliente.carrito

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_prod'] = self.get_object().items.aggregate(total_prod=Sum('cantidad'))['total_prod'] or 0
        return context


class ListaClientesView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "lista_clientes.html"
    context_object_name = "clientes"
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self._agregar_textos_contexto(context)
        return context
    
    def _agregar_textos_contexto(self, context):
        # Agrega los textos estáticos al contexto.
        context.update({
            'titulo_tabla': "Lista de clientes",
            'url_btn': reverse_lazy('clientes:agregar-cliente'),
            'accion_btn': "Agregar cliente",
            'placehoder': 'Ingresar cliente...',
            'lista_paginas': self.__generar_lista_paginas(self.get_queryset())
        })

    def __generar_lista_paginas(self, queryset):
        paginador = Paginator(queryset, self.paginate_by)
        num_pag = int(self.request.GET.get("page", 1))

        lista_paginas = list(paginador.page_range)
        lista_menor = [x for x in lista_paginas if x <= num_pag]
        lista_mayor = [x for x in lista_paginas if x > num_pag]
        
        return sorted(lista_menor[-3:] + lista_mayor[:2])


class EditarClienteView(LoginRequiredMixin, UpdateView):
    model = Cliente
    template_name = "editar_cliente.html"
    form_class = FormCliente
    success_url = reverse_lazy('clientes:lista-clientes')
    msj_exito = "Se ha editado el perfil del cliente exitosamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self._agregar_textos_contexto(context)
        return context
    
    def _agregar_textos_contexto(self, context):
        context.update({
            'nombre_form': 'Editar Cliente',
            'url_redireccion': self.success_url
        })
        return context
    
    def get_object(self, queryset=None):
        # Obtiene el cliente basado en la URL o el usuario autenticado
        id_cliente = self.kwargs.get('pk')

        if id_cliente:
            return get_object_or_404(Cliente, pk=id_cliente)

        # Si no hay `id_cliente`, intenta obtener el cliente del usuario en sesión
        try:
            return self.request.user.cliente
        except AttributeError:  # Se lanza si el usuario no tiene relación con Cliente
            return JsonResponse({'error': 'El usuario no tiene un cliente asociado'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, self.msj_exito)
            return JsonResponse({})

        return self._respuesta_error(form.errors)
    
    def _respuesta_error(self, mensaje):
        # Retorna una respuesta JSON con un mensaje de error
        return JsonResponse({'error': mensaje}) 


class AgregarClienteView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = FormCliente
    template_name = "agregar_cliente.html"
    success_url = reverse_lazy('clientes:lista-clientes')
    msj_exito = "Se ha agregado un nuevo cliente"


