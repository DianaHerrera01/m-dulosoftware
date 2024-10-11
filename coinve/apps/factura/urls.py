from django.urls import path
from . import views

urlpatterns = [
    path('facturas/', views.facturas, name='facturas'),
    path('factura/crear/', views.facturas, name='crear_factura'),
    path('factura/eliminar/<int:id_factura>/', views.eliminar_factura, name='eliminar_factura'),
    path('factura/imprimir/<int:id_factura>/', views.imprimir_factura_pdf, name='imprimir_factura_pdf'),
]
