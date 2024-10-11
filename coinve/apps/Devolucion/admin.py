from django.contrib import admin

# Register your models here.

from .models import Devolucion # Importa los modelos

# Registra los modelos en el administrador
admin.site.register(Devolucion)