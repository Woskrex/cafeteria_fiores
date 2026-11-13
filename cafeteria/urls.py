
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from pedidos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(
        template_name='pedidos/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.inicio, name='inicio'),
    path('encargado/', views.panel_encargado, name='panel_encargado'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
]
