from django.db import models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT
    )
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.IntegerField()
    disponible = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En preparación', 'En preparación'),
        ('Listo', 'Listo'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    fecha = models.DateTimeField(auto_now_add=True)
    hora_retiro = models.TimeField()
    estado = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='Pendiente'
    )
    total = models.IntegerField(default=0)
    observacion = models.TextField(blank=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.username}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT
    )
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()
    subtotal = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['pedido', 'producto'],
                name='unique_pedido_producto'
            )
        ]

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad}"
