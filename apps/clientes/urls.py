from django.urls import path

from . import views

app_name = 'clientes'
urlpatterns = [
    path('agregar-al-carrito/<pk>/', views.AgregarItemCarritoView.as_view(), name='agregar-al-carrito'),
    path('mi-carrito/', views.CarritoView.as_view(), name='mi-carrito'),
    path('mi-carrito/<pk>/actualizar/', views.ActualizarItemCarrito.as_view(), name='actualizar-item-carrito'),
    path('mi-carrito/item/<pk>/eliminar/', views.EliminarItemCarrito.as_view(), name='eliminar-item-carrito'),
    # Clientes
    path('', views.ListaClientesView.as_view(), name="lista-clientes"),
    path('editar-cliente/<pk>/', views.EditarClienteView.as_view(), name="editar-cliente"),
    path('mi-cuenta/', views.EditarClienteView.as_view(), name='mi-cuenta'),
    path('agregar-cliente/', views.AgregarClienteView.as_view(), name='agregar-cliente'),
]