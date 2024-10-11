from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Factura, DetalleFactura
from apps.producto.models import Producto
from apps.cliente.models import Cliente, TipoDocumento

# Vista para listar y crear las facturas
def facturas(request):
    facturas = Factura.objects.all()
    productos = Producto.objects.all()
    clientes = Cliente.objects.all()
    tipos_documento = TipoDocumento.objects.all()
    
    if request.method == 'POST':
        cliente_id = request.POST.get('id_cliente')
        fecha_emision = request.POST.get('fecha_emision')

        # Busca el cliente
        try:
            cliente = Cliente.objects.get(id_cliente=cliente_id)
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente no encontrado.')
            return redirect('crear_factura')

        factura = Factura(cliente=cliente, tipo_documento=cliente.id_tipo_docum, 
                          numero_documento=cliente.documento_cli, fecha_emision=fecha_emision)
        factura.save()

        total = 0  # Inicializa el total
        productos_ids = request.POST.getlist('producto_id')
        cantidades = request.POST.getlist('cantidad')

        for producto_id, cantidad in zip(productos_ids, cantidades):
            try:
                producto = Producto.objects.get(id_producto=producto_id)
                cantidad = int(cantidad)

                # Valida la cantidad
                if cantidad <= 0 or cantidad > producto.cantidad:
                    messages.error(request, f'La cantidad para {producto.nombre_producto} no es válida.')
                    continue

                subtotal = producto.preciounidadventa * cantidad  # Cálculo de subtotal

                # Crea el detalle de la factura
                detalle = DetalleFactura(
                    factura=factura,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unidad_venta=producto.preciounidadventa,
                    precio_total_venta=subtotal  # Aquí colocamos el subtotal
                )
                detalle.save()

                # Actualiza la cantidad del producto
                producto.cantidad -= cantidad
                producto.save()

                total += subtotal  # Sumar al total general

            except Producto.DoesNotExist:
                messages.error(request, f'Producto {producto_id} no encontrado.')

        # Actualiza el total en la factura
        factura.precio_total_venta = total
        factura.save()


        messages.success(request, '¡Factura creada exitosamente!')
        return redirect('facturas')

    return render(request, 'factura.html', {
        'facturas': facturas,
        'productos': productos,
        'clientes': clientes,
        'tipos_documento': tipos_documento
    })


# Vista para eliminar una factura
def eliminar_factura(request, id_factura):
    try:
        factura = Factura.objects.get(id_factura=id_factura)
    except Factura.DoesNotExist:
        messages.error(request, 'La factura no existe.')
        return redirect('facturas')

    factura.delete()
    messages.success(request, 'Factura eliminada exitosamente.')
    return redirect('facturas')

# Función para convertir el HTML en PDF
def generar_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')
    return response

# Vista para imprimir la factura en PDF
def imprimir_factura_pdf(request, id_factura):
    try:
        factura = Factura.objects.get(id_factura=id_factura)
        detalles = DetalleFactura.objects.filter(factura=factura)
        context = {
            'factura': factura,
            'detalles': detalles,
        }
        return generar_pdf('factura_pdf.html', context)
    except Factura.DoesNotExist:
        messages.error(request, 'La factura no existe.')
        return redirect('facturas')