from django.urls import path
from . import views

urlpatterns = [
    path('notas/', views.notas, name='notas'),  # URL para la vista de listar y crear notas
    path('editar_nota/<int:id_nota>/', views.editar_nota, name='editar_nota'),  # URL para editar una nota
    path('eliminar_nota/<int:id_nota>/', views.eliminar_nota, name='eliminar_nota'),  # URL para eliminar una nota
    path('imprimir_nota/<int:id_nota>/', views.imprimir_nota_pdf, name='imprimir_nota'), 
]
