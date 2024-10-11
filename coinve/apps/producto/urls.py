from django.urls import path
from . import views

urlpatterns = [
    path('', views.productos, name='producto'),  # Ruta raíz que apunta a la vista de productos
    path('productos/', views.productos, name='producto'),  # Lista y registra productos
    path('editar_producto/<int:id_producto>/', views.edicion_producto, name='editar_producto'),  # Página para editar producto
    path('actualizar_producto/', views.editar_producto, name='editar_producto'),  # Procesa la edición de un producto
    path('eliminar_producto/<int:id_producto>/', views.eliminar_producto, name='eliminar_producto'),  # Ruta para eliminar producto
]
