from django.contrib import admin


from .models import EntradaProducto # Importa los modelos

# Registra los modelos en el administrador
admin.site.register(EntradaProducto)