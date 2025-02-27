from django.urls import path

from . import views

app_name = 'perfil'
urlpatterns = [
    path("", views.DetallePerfilView.as_view(), name="perfil"),
    path("agregar-a-favoritos/", views.AgregarProdFavoritoView.as_view(), name="agregar-a-favoritos"),
    path("eliminar-favorito/<pk>/", views.EliminarProdFavorito.as_view(), name="eliminar-favorito"),
]