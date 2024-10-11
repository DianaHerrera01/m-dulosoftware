from django.db import models
from apps.producto.models import Producto, Categoria
from apps.proveedor.models import Proveedor
from apps.Pedido.models import Pedido
from decimal import Decimal

class EntradaProducto(models.Model):
    id_entrada = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True, blank=True)  
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField()
    precio_total_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_unidad_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return f"Entrada de {self.producto.nombre_producto} - {self.cantidad}"

    def save(self, *args, **kwargs):
        # Si no se proporciona precio unidad compra, se toma del producto
        if self.precio_unidad_compra is None:
            self.precio_unidad_compra = self.producto.preciounidadcompra

        self.cantidad = int(self.cantidad)
        self.precio_total_compra = Decimal(self.precio_unidad_compra) * self.cantidad

        # Actualizar la cantidad del producto
        self.producto.cantidad += self.cantidad  # Aumentar la cantidad existente
        self.producto.preciounidadcompra = self.precio_unidad_compra
        self.producto.save()  # Guarda los cambios en el producto

        super().save(*args, **kwargs)