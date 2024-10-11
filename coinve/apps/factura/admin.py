from django.contrib import admin

from .models import Factura,  DetalleFactura  # Importa los modelos

# Registra los modelos en el administrador
admin.site.register(Factura)
admin.site.register(DetalleFactura)