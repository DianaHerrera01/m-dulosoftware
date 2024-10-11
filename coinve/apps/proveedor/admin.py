from django.contrib import admin
from .models import Proveedor, ProductoServicio # Importa los modelos

# Registra los modelos en el administrador
admin.site.register(Proveedor)
admin.site.register(ProductoServicio)