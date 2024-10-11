from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Nota, TipoNota, ProductoNota
from apps.factura.models import Factura
from apps.producto.models import Producto
from decimal import Decimal
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def notas(request):
    facturas = Factura.objects.all()
    tipos_nota = TipoNota.objects.all()
    productos = Producto.objects.all()
    notas = Nota.objects.all()

    if request.method == 'POST':
        factura_id = request.POST.get('factura_id')
        motivo = request.POST.get('motivo')
        valor = request.POST.get('valor')
        tipo_nota_id = request.POST.get('tipo_nota_id')
        producto_ids = request.POST.getlist('producto_id')
        cantidades = request.POST.getlist('cantidad')

        try:
            factura = Factura.objects.get(id_factura=factura_id)
        except Factura.DoesNotExist:
            messages.error(request, 'Factura no encontrada.')
            return redirect('notas')

        try:
            tipo_nota = TipoNota.objects.get(id_tipo_nota=tipo_nota_id)
        except TipoNota.DoesNotExist:
            messages.error(request, 'Tipo de nota no encontrado.')
            return redirect('notas')
        
        try:
            valor = Decimal(request.POST.get('valor', '0'))
        except:
            messages.error(request, 'Valor inválido.')
            return redirect('notas')

        # Crear la nueva nota sin el valor
        nota = Nota(factura=factura, motivo=motivo, tipo_nota=tipo_nota, valor=valor)
        nota.save()

        total_nota = Decimal('0.00')

        for producto_id, cantidad_str in zip(producto_ids, cantidades):
            if producto_id and cantidad_str:  # Verificar si se seleccionó un producto y una cantidad
                try:
                    producto = Producto.objects.get(id_producto=producto_id)
                    cantidad = int(cantidad_str)

                    if cantidad <= 0:
                        messages.error(request, f'La cantidad para {producto.nombre_producto} debe ser mayor a cero.')
                        continue

                    # Crear ProductoNota, el ajuste de stock y total se maneja en su método save
                    
                    producto_nota = ProductoNota(nota=nota, producto=producto, cantidad=cantidad)
                    producto_nota.save()

                    # Calcular el subtotal y agregarlo al total de la nota
                    subtotal = producto.preciounidadventa * cantidad
                    total_nota += subtotal

                except Producto.DoesNotExist:
                    messages.error(request, f'Producto con ID {producto_id} no encontrado.')
                except ValueError:
                    messages.error(request, f'Cantidad inválida para el producto {producto.nombre_producto}.')

        messages.success(request, 'Nota creada y productos procesados exitosamente.')
        return redirect('notas')

    return render(request, 'notas.html', {
        'facturas': facturas,
        'tipos_nota': tipos_nota,
        'productos': productos,
        'notas': notas
    })

def editar_nota(request, id_nota):
    nota = Nota.objects.get(id_nota=id_nota)
    facturas = Factura.objects.all()
    tipos_nota = TipoNota.objects.all()
    productos = Producto.objects.all()  # Todos los productos
    
    # Obtener productos asociados a la nota
    productos_asociados = nota.productonota_set.select_related('producto')

    if request.method == 'POST':
        # Obtener datos del formulario
        factura_id = request.POST.get('factura_id')
        motivo = request.POST.get('motivo')
        tipo_nota_id = request.POST.get('tipo_nota_id')
        valor = request.POST.get('valor')
        producto_ids = request.POST.getlist('producto_id')
        cantidades = request.POST.getlist('cantidad')

        # Validar y obtener factura y tipo de nota
        try:
            factura = Factura.objects.get(id_factura=factura_id)
            tipo_nota = TipoNota.objects.get(id_tipo_nota=tipo_nota_id)
            nota.factura = factura
            nota.tipo_nota = tipo_nota
            nota.motivo = motivo
            nota.valor = Decimal(valor)

            # Eliminar productos existentes
            nota.productos.clear()

            total_nota = Decimal('0.00')

            for producto_id, cantidad_str in zip(producto_ids, cantidades):
                if producto_id and cantidad_str:
                    try:
                        producto = Producto.objects.get(id_producto=producto_id)
                        cantidad = int(cantidad_str)

                        if cantidad <= 0:
                            messages.error(request, f'La cantidad para {producto.nombre_producto} debe ser mayor a cero.')
                            continue

                        ProductoNota.objects.create(nota=nota, producto=producto, cantidad=cantidad)

                        subtotal = producto.preciounidadventa * cantidad
                        total_nota += subtotal

                    except Producto.DoesNotExist:
                        messages.error(request, f'Producto con ID {producto_id} no encontrado.')
                    except ValueError:
                        messages.error(request, f'Cantidad inválida para el producto {producto.nombre_producto}.')

            nota.save()
            messages.success(request, 'Nota actualizada exitosamente.')
            return redirect('notas')

        except (Factura.DoesNotExist, TipoNota.DoesNotExist, ValueError):
            messages.error(request, 'Error en los datos del formulario.')
            return redirect('notas')

    return render(request, 'editar_nota.html', {
        'nota': nota,
        'facturas': facturas,
        'tipos_nota': tipos_nota,
        'productos': productos,  # Agregar todos los productos
        'productos_asociados': productos_asociados  # Productos asociados
    })

def eliminar_nota(request, id_nota):
    nota = Nota.objects.get(id_nota=id_nota)  # Obtener la nota a eliminar
    nota.delete()
    messages.success(request, 'Nota eliminada exitosamente.')
    return redirect('notas')  # Redirigir a la vista de notas

def generar_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="nota.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')
    return response

# Vista para imprimir la nota en PDF
def imprimir_nota_pdf(request, id_nota):
    try:
        nota = Nota.objects.get(id_nota=id_nota)
        factura = nota.factura
        productos_asociados = ProductoNota.objects.filter(nota=nota)

        # Obtener los productos de la factura original
        productos_factura = factura.detallefactura_set.select_related('producto')

        for producto_nota in productos_asociados:
            producto_nota.subtotal = producto_nota.producto.preciounidadventa * producto_nota.cantidad

        contribuyente = {
            'nombre_negocio': factura.nombre_negocio,
            'nit': factura.nit,
            'actividad_comercial': factura.actividad_comercial
        }

        context = {
            'nota': nota,
            'factura': factura,
            'productos_asociados': productos_asociados,
            'productos_factura': productos_factura,
            'contribuyente': contribuyente
        }

        return generar_pdf('imprimir_nota.html', context)
    except Nota.DoesNotExist:
        messages.error(request, "Nota no encontrada.")
        return redirect('notas')
