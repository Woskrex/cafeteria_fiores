
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafeteria.settings')
django.setup()

from pathlib import Path
from django.contrib.auth.models import User, Permission
from django.core.management import call_command
from pedidos.models import Categoria, Producto

categorias = {}

for nombre in ['Cafés', 'Tés', 'Sándwiches', 'Pastelería']:
    categoria, _ = Categoria.objects.get_or_create(
        nombre=nombre,
        defaults={'descripcion': f'Productos de {nombre}', 'activa': True}
    )
    categorias[nombre] = categoria

productos = [
    ('Espresso', 'Cafés', 1800),
    ('Americano', 'Cafés', 1600),
    ('Cappuccino', 'Cafés', 2500),
    ('Latte', 'Cafés', 2600),
    ('Mocaccino', 'Cafés', 2900),
    ('Té negro', 'Tés', 1300),
    ('Té verde', 'Tés', 1400),
    ('Té chai', 'Tés', 1800),
    ('Infusión de frutas', 'Tés', 1700),
    ('Té con limón', 'Tés', 1500),
    ('Sándwich jamón queso', 'Sándwiches', 3500),
    ('Sándwich de pollo', 'Sándwiches', 4200),
    ('Sándwich vegetariano', 'Sándwiches', 3900),
    ('Barros Luco', 'Sándwiches', 4800),
    ('Aliado', 'Sándwiches', 3300),
    ('Brownie', 'Pastelería', 2100),
    ('Muffin', 'Pastelería', 1900),
    ('Croissant', 'Pastelería', 2300),
    ('Galleta de avena', 'Pastelería', 900),
    ('Cheesecake', 'Pastelería', 3500),
]

for i, (nombre, categoria, precio) in enumerate(productos, start=1):
    Producto.objects.update_or_create(
        codigo=f'CAF-{i:03d}',
        defaults={
            'nombre': nombre,
            'categoria': categorias[categoria],
            'precio': precio,
            'stock': 0 if i == 1 else 10,
            'disponible': i != 2,
        }
    )

for nombre, encargado in [
    ('encargado', True),
    ('cliente1', False),
    ('cliente2', False),
]:
    usuario, _ = User.objects.get_or_create(username=nombre)
    usuario.is_staff = encargado
    usuario.set_password('Prueba2026!')
    usuario.save()

    if encargado:
        permisos = Permission.objects.filter(
            content_type__app_label='pedidos'
        )
        usuario.user_permissions.add(*permisos)

Path('pedidos/fixtures').mkdir(exist_ok=True)

with open('pedidos/fixtures/datos_prueba.json', 'w', encoding='utf-8') as archivo:
    call_command(
        'dumpdata',
        'pedidos.Categoria',
        'pedidos.Producto',
        indent=2,
        stdout=archivo
    )

print('Datos creados: 4 categorías, 20 productos y 3 usuarios.')
