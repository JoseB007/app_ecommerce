from django.http import JsonResponse
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import resolve_url

class LoginRequiredJSONMixin(AccessMixin):
    """ 
    Mixin que verifica si el usuario está autenticado en peticiones AJAX.
    Permite definir una URL personalizada de redirección con `redirect_url`.
    """

    next_url = None  # Cada vista puede personalizar esta variable

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Si la vista tiene un `next_url` definido, se usa; de lo contrario, se toma la URL actual
            redirect_to = resolve_url("/accounts/login/")  # Página de login por defecto
            next_param = self.next_url if self.next_url else request.path  # Se usa la `next_url` de la vista si está definida

            # Construir la URL de redirección con `next`
            redirect_to = f"{redirect_to}?next={next_param}"

            return JsonResponse({
                "error": "not_authenticated",
                "redirect_url": redirect_to
            }, status=401)

        return super().dispatch(request, *args, **kwargs)
