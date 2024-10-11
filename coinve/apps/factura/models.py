from django.db import models
from apps.producto.models import Producto
from apps.cliente.models import Cliente, TipoDocumento

class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    numero_documento = models.CharField(max_length=11, default='' )
    fecha_emision = models.DateField()
    precio_total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # campos con valores por defecto
    actividad_comercial = models.CharField(max_length=255, default="Comercio al por menor de computadores, equipos periféricos y equipo de telecomunicaciones.")
    nit = models.CharField(max_length=15, default="700668550-5")
    nombre_negocio = models.CharField(max_length=100, default="TEGNOFACIL")

    def __str__(self):
        return f"Factura {self.id_factura} - {self.cliente.nombre_cliente} {self.cliente.apellidos_cliente}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unidad_venta = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.producto.nombre_producto} ({self.cantidad})"
