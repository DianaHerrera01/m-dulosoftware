from django.db import models
from apps.factura.models import Factura
from apps.producto.models import Producto

class TipoNota(models.Model):
    id_tipo_nota = models.AutoField(primary_key=True)
    nom_nota = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_nota

class Nota(models.Model):
    id_nota = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    motivo = models.TextField()
    tipo_nota = models.ForeignKey(TipoNota, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    productos = models.ManyToManyField(Producto, through='ProductoNota')

    def __str__(self):
        return f"Nota {self.id_nota} - Factura {self.factura.id_factura}"

class ProductoNota(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)  # Producto opcional
    nota = models.ForeignKey(Nota, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(null=True, blank=True)  # Cantidad opcional

    def __str__(self):
        if self.producto:
            return f"Producto: {self.producto.nombre_producto} - Nota: {self.nota.id_nota}"
        return f"Nota sin producto asociado - Nota: {self.nota.id_nota}"

    def save(self, *args, **kwargs):
        # Llamar al método save original primero para asegurarnos de que la nota existe
        super(ProductoNota, self).save(*args, **kwargs)

        # Asegúrate de que el producto y la cantidad están definidos
        if self.producto and self.cantidad:
            subtotal = self.producto.preciounidadventa * self.cantidad  # Calcular subtotal

            # Ajustar el stock del producto y el total de la factura
            if self.nota.tipo_nota.nom_nota.lower() == "nota de crédito":
                # Devolución del producto - aumentar stock y disminuir total de factura
                self.producto.cantidad += self.cantidad
                self.nota.factura.precio_total_venta -= subtotal
                
            elif self.nota.tipo_nota.nom_nota.lower() == "nota de débito":
                # Venta adicional - disminuir stock y aumentar total de factura
                if self.producto.cantidad < self.cantidad:
                    raise ValueError("No hay suficiente stock para vender este producto.")
                self.producto.cantidad -= self.cantidad
                self.nota.factura.precio_total_venta += subtotal

            # Guardar los cambios en el producto y la factura
            self.producto.save()
            self.nota.factura.save()

            # Actualizar la cantidad en la factura
            detalle_factura = self.nota.factura.detallefactura_set.filter(producto=self.producto).first()
            if detalle_factura:
                if self.nota.tipo_nota.nom_nota.lower() == "nota de crédito":
                    # Disminuir cantidad en la factura
                    detalle_factura.cantidad -= self.cantidad
                elif self.nota.tipo_nota.nom_nota.lower() == "nota de débito":
                    # Aumentar cantidad en la factura
                    detalle_factura.cantidad += self.cantidad
                detalle_factura.save()