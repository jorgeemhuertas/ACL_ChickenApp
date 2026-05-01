from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('archivos/<int:usuario_id>/', views.ver_archivos, name='ver_archivos'),
    path('producto/', views.crear_producto, name='producto'),
]
