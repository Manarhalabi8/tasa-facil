from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render
from .forms import RegistroForm


class RegistroView(CreateView):
    """Vista para registrar un nuevo usuario.

    Utiliza RegistroForm, renderiza el template
    cuentas/registro.html y redirige al login tras el éxito.
    """
    form_class = RegistroForm
    template_name = 'cuentas/registro.html'
    success_url = reverse_lazy('login')


class LoginPersonalizadoView(LoginView):
    """Vista de inicio de sesión personalizada.

    Renderiza el template cuentas/login.html.
    """
    template_name = 'cuentas/login.html'


@login_required
def panel_usuario(request):
    """Vista del panel de usuario.

    Requiere autenticación previa. Renderiza cuentas/panel.html.
    """
    return render(request, 'cuentas/panel.html')
