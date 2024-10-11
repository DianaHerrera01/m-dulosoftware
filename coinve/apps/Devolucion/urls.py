from django.urls import path
from . import views

urlpatterns = [
    path('', views.devolucion, name='devolucion'),  # URL para la vista principal de devoluciones
    path('devolucion/', views.devolucion, name='devolucion'),  # URL adicional para devoluciones
    path('editar_devolucion/<int:id_devolucion>/', views.editar_devolucion, name='editar_devolucion'),  # URL para editar una devolución
    path('actualizar_devolucion/<int:id_devolucion>/', views.editar_devolucion, name='actualizar_devolucion'),  # URL para la actualización
    path('eliminar_devolucion/<int:id_devolucion>/', views.eliminar_devolucion, name='eliminar_devolucion'),  # URL para eliminar una devolución
]
