# Cafetería Fiores

Proyecto Django para una cafetería de INACAP. Permite que los clientes consulten productos y, una vez completadas todas las funcionalidades, realicen pedidos para retiro.

## Tecnologías

- Python y Django
- SQLite para desarrollo
- HTML y plantillas de Django
- Git y GitHub
- python-dotenv para variables de entorno

## Instalación y ejecución en Windows (PowerShell)

1. Clona el repositorio y abre la carpeta que contiene `manage.py`.
2. Crea y activa un entorno virtual:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Instala las dependencias:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Crea .env a partir de .env.example y asigna una SECRET_KEY propia. Para desarrollo local, configura `DEBUG=True`. No publiques .env
5. Crea las tablas:

   powershell
   python manage.py migrate
   

6. Carga los datos de prueba y crea los usuarios:

   powershell
   python seed_rf01.py


   El script crea o actualiza cuatro categorías, veinte productos y tres usuarios, y genera `pedidos/fixtures/datos_prueba.json`. Alternativamente, el fixture JSON puede cargar las categorías y productos con `python manage.py loaddata datos_prueba`, pero no crea los usuarios

7. Ejecuta:

   powershell
   python manage.py check
   python manage.py runserver
   

8. Visita http://127.0.0.1:8000/login/.

## Usuarios de prueba

Los siguientes usuarios se crean mediante `seed_rf01.py`:

| Usuario | Rol | Contraseña de prueba |
| --- | --- | --- |
| encargado | Encargado (is_staff=True) | Prueba2026! |
| cliente1| Cliente | `Prueba2026!` |
| cliente2 | Cliente | `Prueba2026!` |

Estas credenciales son únicamente para demostración local y deben cambiarse en cualquier despliegue real. Ejecutar nuevamente el script restablece las contraseñas de estos usuarios.

## Rutas principales implementadas

- /login/: iniciar sesión
- /página de inicio
- /catalogo/: catálogo de productos para clientes
- /mis-pedidos/: historial de pedidos del cliente
- /encargado/: panel del encargado
- /encargado/pedidos/`: listado y filtro de pedidos del día
- /admin/: Django Admin

## Funcionalidades y estado

- RF-01 — Modelos y administración: modelos, relaciones, administrador y datos de prueba implementados.
- RF-02 — Autenticación y roles: login, logout, acceso por roles y duración de sesión configurados.
- RF-03 — Catálogo: búsqueda, filtro por categoría, precios en CLP e indicación de agotados implementados.
- RF-04 — Gestión del catálogo sin IA: pendiente de desarrollo manual.
- RF-05 — Carrito y confirmación sin IA: pendiente de desarrollo manual.
- RF-06 — Seguimiento de pedidos: vistas de historial, cancelación y avance de estado implementadas; falta comprobar el flujo completo con pedidos reales una vez disponible RF-05.

Los RF-04 y RF-05 deben realizarse sin asistencia de IA según las reglas de la evaluación.

## Uso de IA y commits

Consulta [BITACORA_IA.md](BITACORA_IA.md) para ver las consultas representativas, el código utilizado, las revisiones y los problemas reales encontrados. Los commits se registran por funcionalidad con etiquetas [IA] o [SIN-IA] conforme a las instrucciones de la evaluación.

## Consideraciones

- No se incluye db.sqlite3 ni .env en Git; se generan o configuran localmente.
- La creación de pedidos depende de completar RF-05.
- Antes de utilizar la aplicación en un entorno real, se deben revisar contraseñas, permisos, configuración de producción y pruebas de reglas de negocio.
