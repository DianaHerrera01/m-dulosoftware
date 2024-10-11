from django.urls import path
from . import views

urlpatterns = [
    path('', views.proveedores, name='proveedor'),  # Ruta raíz que apunta a la vista de proveedores 
    path('proveedor/', views.proveedores, name='proveedor'),  # Para la lista y registro de proveedores
    path('proveedor/editar/<int:id_proveedor>/', views.edicion_proveedor, name='editar_proveedor'),  # Para cargar el formulario de edición
    path('proveedor/editar/', views.editar_proveedor, name='editar_proveedor'),  # Para procesar la edición del proveedor
    path('proveedor/eliminar/<int:id_proveedor>/', views.eliminar_proveedor, name='eliminar_proveedor'),  # Para eliminar un proveedor
]
