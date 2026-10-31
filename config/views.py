from django.shortcuts import render


def home(request):
    """Vista de la página principal pública.

    Renderiza el template home.html. Visible para visitantes y usuarios.
    """
    return render(request, 'home.html')
