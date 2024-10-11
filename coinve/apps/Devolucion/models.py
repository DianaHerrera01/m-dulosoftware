from django.db import models
from apps.proveedor.models import Proveedor
from apps.producto.models import Producto

class Devolucion(models.Model):
    id_devolucion = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    motivo = models.TextField(blank=True, null=True)
    fecha_devolucion = models.DateTimeField(auto_now_add=True)

    @property
    def precio_unidad_compra(self):
        # Obtener el precio unidad compra del producto
        return self.producto.preciounidadcompra if self.producto else 0

    @property
    def precio_total_compra(self):
        # Calcular el precio total de compra basado en la cantidad y el precio unidad compra
        return self.precio_unidad_compra * self.cantidad

    @property
    def nombre_proveedor(self):
        # Obtener el nombre del proveedor relacionado con el producto
        return self.producto.proveedor.nombre_proveedor if self.producto.proveedor else "Sin proveedor"

    @property
    def apellidos_proveedor(self):
        # Obtener los apellidos del proveedor relacionado con el producto
        return self.producto.proveedor.apellidos_proveedor if self.producto.proveedor else "Sin apellidos"

    def __str__(self):
        return f"Devolución de {self.cantidad} {self.producto.nombre_producto} a {self.nombre_proveedor} {self.apellidos_proveedor}"
