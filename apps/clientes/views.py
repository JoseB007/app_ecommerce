from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib import messages
from django.db.models import Sum, Count
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import get_messages


from .models import Cliente, Carrito, ItemCarrito

from apps.productos.models import Producto

# Create your views here.
class AgregarItemCarritoView(LoginRequiredMixin, View):
    msj_exito = 'Producto agregado al carrito.'

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
            return JsonResponse(data, status=400)

        # Obtener el carrito del cliente
        cliente = request.user.cliente
        carrito, carrito_creado = Carrito.objects.get_or_create(cliente=cliente)

        # Agregar o actualizar el ítem en el carrito
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
            messages.success(request, self.msj_exito)
            storage = get_messages(request)
            lista_mensajes = [(message.tags, message.message) for message in storage]
            
            # Datos para la respuesta JSON
            data['item'] = item.producto.json_producto()
            data['carrito_items'] = carrito.productos.count()
            data['message'] = lista_mensajes
        except Exception as e:
            data['error'] = str(e)
            return JsonResponse(data, status=500)

        return JsonResponse(data)


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


