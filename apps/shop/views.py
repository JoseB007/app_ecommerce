from django.views.generic import ListView, DetailView, CreateView, DetailView, UpdateView, TemplateView
from django.core.paginator import Paginator

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
        queryset = super().get_queryset()
        self.tag = self.kwargs.get("tag")
        if self.tag:
            queryset = Producto.objects.filter(categorias__slug=self.tag)
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


class DetalleProductoView(DetailView):
    model = Producto
    template_name = "detalle_producto.html"
    context_object_name = "producto"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context