from django.contrib import admin

from .models import Nota, TipoNota, ProductoNota   # Importa los modelos

# Registra los modelos en el administrador
admin.site.register(Nota)
admin.site.register(TipoNota)
admin.site.register(ProductoNota)

