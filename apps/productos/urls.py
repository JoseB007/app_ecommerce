from django.urls import path

from . import views

app_name = "productos"
urlpatterns = [
    # Rutas a las fuciones del Admin
    path("agregar-producto/", views.AgregarProductoView.as_view(), name="agregar-producto"),
    path("actualizar-producto/<slug>/", views.ActualizarProductoView.as_view(), name="actualizar-producto"),      
    path("lista-productos/", views.ListarProductosView.as_view(), name="lista-productos"),
]