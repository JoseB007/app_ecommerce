from django.views.generic import ListView, DetailView, CreateView, DetailView, UpdateView, TemplateView
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db.models import Count

from apps.productos.models import Producto, Categoria


# Create your views here.
class IndexView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.all()[:4]
        context['categorias'] = Categoria.objects.all()[:4]
        return context


class ListaTiendaProductosView(ListView):
    model = Producto
    template_name = "tienda_productos.html"
    context_object_name = "productos"
    paginate_by = 8

    def get_queryset(self):
        # Si ya se definió un queryset en el método get, usarlo
        if hasattr(self, 'queryset'):
            queryset = self.queryset
        
        queryset = super().get_queryset()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['cat_actual'] = Categoria.objects.get(slug=self.tag) if self.tag else None
        context['lista_paginas'] = self.__generar_lista_paginas(self.get_queryset())
        return context
    
    def _agregar_textos_contexto(self, contexto):
        contexto.update({
        })
        return contexto
    
    def __generar_lista_paginas(self, queryset):
        paginador = Paginator(queryset, self.paginate_by)
        num_pag = int(self.request.GET.get("page", 1))

        lista_paginas = list(paginador.page_range)
        lista_menor = [x for x in lista_paginas if x <= num_pag]
        lista_mayor = [x for x in lista_paginas if x > num_pag]
        
        return sorted(lista_menor[-3:] + lista_mayor[:2])
    
    def get(self, request, *args, **kwargs):
        # Obtener el queryset actual
        self.queryset = self.get_queryset()
        
        # Obtener el parámetro 'ref' de la URL para ordenar queryset
        act = request.GET.get('ref')
        if act:
            self.queryset = self.ordenar_queryset(act, self.queryset)

        # Obtener la categoría actual, y si existe filtrar productos por esa categoría
        self.tag = self.kwargs.get("tag")
        if self.tag:
            self.queryset = self.queryset.filter(categorias__slug=self.tag)

        # Llamar al método get de la clase padre para continuar con el flujo normal
        return super().get(request, *args, **kwargs)

    def ordenar_queryset(self, act, queryset):
        # Si el parámetro es 'most-popular', ordenar por favoritos
        if act == "mas-popular":
            queryset = Producto.objects.annotate(total_fav=Count("favoritos")).order_by("-total_fav")
        # Si el parámetro es 'most-purchased', ordenar por cant. de detalles de venta
        elif act == "mas-comprado":
            queryset = Producto.objects.annotate(total_compras=Count("detalles")).filter(total_compras__gt=0).order_by("-total_compras")
        else:
            queryset = Producto.objects.all()
        return queryset


class DetalleProductoView(DetailView):
    model = Producto
    template_name = "detalle_producto.html"
    context_object_name = "producto"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self._agregar_textos_contexto(context)
        return context
    
    def _agregar_textos_contexto(self, context):
        context.update({
            'categorias': Categoria.objects.all(),
            'mensaje_whatsapp': f"¡Hola! Estoy interesado en el producto \"{self.get_object().nombre}\" que cuesta ${self.get_object().precio}. Aquí está el enlace: {self.request.build_absolute_uri()}"
        })
        return context