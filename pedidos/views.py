from functools import wraps
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Categoria, Producto
from .models import Pedido

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



@login_required
def catalogo(request):
    if request.user.is_staff:
        raise PermissionDenied

    productos = Producto.objects.filter(
        disponible=True,
        categoria__activa=True
    ).select_related('categoria')

    busqueda = request.GET.get('buscar', '')
    categoria_id = request.GET.get('categoria', '')

    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)

    if categoria_id.isdigit():
        productos = productos.filter(categoria_id=int(categoria_id))

    categorias = Categoria.objects.filter(activa=True)

    return render(request, 'pedidos/catalogo.html', {
        'productos': productos,
        'categorias': categorias,
        'busqueda': busqueda,
        'categoria_id': categoria_id,
    })

@login_required
def mis_pedidos(request):
    if request.user.is_staff:
        raise PermissionDenied

    pedidos = Pedido.objects.filter(
        cliente=request.user
    ).prefetch_related(
        'detalles__producto'
    ).order_by('-fecha')

    return render(request, 'pedidos/mis_pedidos.html', {
        'pedidos': pedidos
    })