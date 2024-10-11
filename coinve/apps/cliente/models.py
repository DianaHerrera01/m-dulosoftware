from django.db import models

class TipoDocumento(models.Model):
    id_tipo_docum = models.AutoField(primary_key=True)
    nom_tipo_doc = models.CharField(max_length=50)

    def __str__(self):
        return self.nom_tipo_doc

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=100)
    apellidos_cliente = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    id_tipo_docum = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    documento_cli = models.CharField(max_length=11)  
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombre_cliente} {self.apellidos_cliente}"
