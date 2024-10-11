from django.contrib import admin


from .models import Pedido  # Importa los modelos

# Registra los modelos en el administrador
admin.site.register(Pedido)
