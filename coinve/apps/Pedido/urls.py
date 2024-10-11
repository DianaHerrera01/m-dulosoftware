from django.urls import path
from . import views

urlpatterns = [
    path('', views.pedidos, name='pedido'),
    path('pedidos/', views.pedidos, name='pedido'),
    path('editar_pedido/<int:id_pedido>/', views.editar_pedido, name='editar_pedido'),  # Corregido
    path('actualizar_pedido/<int:id_pedido>/', views.editar_pedido, name='actualizar_pedido'),  # URL para la actualización
    path('eliminar_pedido/<int:id_pedido>/', views.eliminar_pedido, name='eliminar_pedido'),
    path('recibir_pedido/<int:id_pedido>/', views.recibir_pedido, name='recibir_pedido'),
]

