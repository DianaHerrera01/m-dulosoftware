from django.db import models
from apps.proveedor.models import Proveedor
from apps.producto.models import Producto

class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Recibido', 'Recibido'),
    ]
    id_orden_pedido = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='Pendiente')

    def __str__(self):
        return f"Pedido {self.id_orden_pedido} - {self.producto.nombre_producto} ({self.cantidad})"
