from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class AdminView(LoginRequiredMixin ,generic.TemplateView):
    template_name = 'admin.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)