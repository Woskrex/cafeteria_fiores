from django.contrib import admin
from django.contrib import admin
from .models import Categoria, Producto, Pedido, DetallePedido

# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'codigo', 'nombre', 'categoria',
        'precio', 'stock', 'disponible'
    )
    list_filter = ('categoria', 'disponible')
    search_fields = ('codigo', 'nombre')


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cliente', 'fecha',
        'hora_retiro', 'estado', 'total'
    )
    list_filter = ('estado', 'fecha')
    search_fields = ('cliente__username',)
    inlines = [DetallePedidoInline]


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = (
        'pedido', 'producto', 'cantidad',
        'precio_unitario', 'subtotal'
    )
    search_fields = ('producto__nombre',)
