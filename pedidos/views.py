from functools import wraps
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Categoria, Producto
from .models import Pedido
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.views.decorators.http import require_POST
from django.utils import timezone

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


@login_required
@require_POST
def cancelar_pedido(request, pedido_id):
    if request.user.is_staff:
        raise PermissionDenied

    with transaction.atomic():
        pedido = get_object_or_404(
            Pedido.objects.select_for_update(),
            id=pedido_id,
            cliente=request.user,
            estado='Pendiente'
        )

        for detalle in pedido.detalles.all():
            Producto.objects.filter(
                id=detalle.producto_id
            ).update(
                stock=F('stock') + detalle.cantidad
            )

        pedido.estado = 'Cancelado'
        pedido.save(update_fields=['estado'])

    messages.success(request, 'Pedido cancelado correctamente')
    return redirect('mis_pedidos')

@solo_encargado
def pedidos_del_dia(request):
    pedidos = Pedido.objects.filter(
        fecha__date=timezone.localdate()
    ).select_related('cliente').order_by('-fecha')

    estado = request.GET.get('estado', '')

    if estado in dict(Pedido.ESTADOS):
        pedidos = pedidos.filter(estado=estado)

    return render(request, 'pedidos/pedidos_del_dia.html', {
        'pedidos': pedidos,
        'estados': Pedido.ESTADOS,
        'estado_actual': estado,
    })


@solo_encargado
@require_POST
def avanzar_pedido(request, pedido_id):
    flujo = {
        'Pendiente': 'En preparación',
        'En preparación': 'Listo',
        'Listo': 'Entregado',
    }

    with transaction.atomic():
        pedido = get_object_or_404(
            Pedido.objects.select_for_update(),
            id=pedido_id
        )

        siguiente = flujo.get(pedido.estado)

        if siguiente is None:
            messages.error(request, 'Este pedido no puede avanzar')
        else:
            pedido.estado = siguiente
            pedido.save(update_fields=['estado'])
            messages.success(request, 'Estado actualizado correctamente')

    return redirect('pedidos_del_dia')
