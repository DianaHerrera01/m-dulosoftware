from django.contrib import admin

from .models import Cliente # Importa los modelos

# Registra los modelos en el administrador
admin.site.register(Cliente)
