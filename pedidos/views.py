from functools import wraps
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.
@login_required
def inicio(request):
    return render(request, 'pedidos/inicio.html')


def solo_encargado(vista):
    @login_required
    @wraps(vista)
    def protegida(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return vista(request, *args, **kwargs)
    return protegida


@solo_encargado
def panel_encargado(request):
    return render(request, 'pedidos/panel_encargado.html')
