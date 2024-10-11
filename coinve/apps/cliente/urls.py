from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes, name='clientes'),  # Ruta raíz que apunta a la vista de clientes
    path('clientes/', views.clientes, name='clientes'),  # Lista y registra clientes
    path('editar_cliente/<int:id_cliente>/', views.edicion_cliente, name='editar_cliente'),  # Página para editar un cliente
    path('actualizar_cliente/', views.editar_cliente, name='editar_cliente'),  # Procesa la actualización de un cliente
    path('eliminar_cliente/<int:id_cliente>/', views.eliminar_cliente, name='eliminar_cliente'),  # Ruta para eliminar un cliente
]
