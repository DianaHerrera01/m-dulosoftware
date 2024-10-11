from django.urls import path
from . import views

urlpatterns = [
    path('', views.entradas_producto, name='entradas_producto'),
    path('entradas_producto/', views.entradas_producto, name='entradas_producto'),
   path('editar_entrada/<int:id_entrada>/', views.editar_entrada, name='editar_entrada'),  # URL específica para editar
    path('actualizar_entrada/<int:id_entrada>/', views.editar_entrada, name='actualizar_entrada'),  # URL para la actualización
    path('eliminar_entrada/<int:id_entrada>/', views.eliminar_entrada_producto, name='eliminar_entrada_producto'),
]
