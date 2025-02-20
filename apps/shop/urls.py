from django.urls import path

from . import views

app_name = "shop"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("productos/", views.ListaTiendaProductosView.as_view(), name="tienda-productos"),
    path("productos/<tag>/", views.ListaTiendaProductosView.as_view(), name="tiendaProductos-tag"),
    path("producto/<slug>/", views.DetalleProductoView.as_view(), name="detalle-producto"),
]