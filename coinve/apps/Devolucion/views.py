from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Devolucion
from apps.producto.models import Producto
from apps.proveedor.models import Proveedor
from django.db import transaction

def devolucion(request):
    devoluciones = Devolucion.objects.all()
    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        if 'editar' in request.POST:
            devolucion_id = request.POST.get('devolucion_id')
            devolucion_instance = Devolucion.objects.filter(id_devolucion=devolucion_id).first()

            if devolucion_instance is None:
                messages.error(request, 'Devolución no encontrada.')
                return redirect('devolucion')

            cantidad_anterior = devolucion_instance.cantidad

            try:
                devolucion_instance.producto = Producto.objects.get(id_producto=request.POST.get('producto'))
            except Producto.DoesNotExist:
                messages.error(request, 'Producto no encontrado.')
                return redirect('devolucion')

            devolucion_instance.cantidad = int(request.POST.get('cantidad'))
            devolucion_instance.motivo = request.POST.get('motivo')

            # Ajustar la cantidad en el producto
            producto = devolucion_instance.producto
            producto.cantidad += cantidad_anterior
            producto.cantidad -= devolucion_instance.cantidad
            producto.save()

            devolucion_instance.save()
            messages.success(request, 'Devolución editada exitosamente.')
            return redirect('devolucion')

        # Lógica para crear una nueva devolución
        producto_id = request.POST.get('producto')
        cantidad = int(request.POST.get('cantidad'))
        motivo = request.POST.get('motivo')

        try:
            producto = Producto.objects.get(id_producto=producto_id)
        except Producto.DoesNotExist:
            messages.error(request, 'Producto no encontrado.')
            return redirect('devolucion')

        if cantidad > producto.cantidad:
            messages.error(request, 'La cantidad a devolver supera el inventario disponible.')
            return redirect('devolucion')

        with transaction.atomic():
            devolucion = Devolucion.objects.create(
                producto=producto,
                cantidad=cantidad,
                motivo=motivo
            )

            producto.cantidad -= cantidad
            producto.save()
            messages.success(request, 'Devolución registrada exitosamente.')
            return redirect('devolucion')

    return render(request, 'devolucion.html', {
        'devoluciones': devoluciones,
        'productos': productos,
        'proveedores': proveedores
    })

def editar_devolucion(request, id_devolucion):
    devolucion_instance = Devolucion.objects.filter(id_devolucion=id_devolucion).first()
    if devolucion_instance is None:
        messages.error(request, 'Devolución no encontrada.')
        return redirect('devolucion')

    if request.method == 'POST':
        # Obtener la cantidad anterior para restaurar en el producto
        cantidad_anterior = devolucion_instance.cantidad

        # Actualizar la devolución
        devolucion_instance.producto = Producto.objects.get(id_producto=request.POST.get('producto'))
        devolucion_instance.cantidad = int(request.POST.get('cantidad'))
        devolucion_instance.motivo = request.POST.get('motivo')

        # Ajustar la cantidad en el producto
        producto = devolucion_instance.producto
        producto.cantidad += cantidad_anterior  # Restaurar la cantidad anterior
        producto.cantidad -= devolucion_instance.cantidad  # Restar la nueva cantidad
        producto.save()

        devolucion_instance.save()

        messages.success(request, 'Devolución editada exitosamente.')
        return redirect('devolucion')
 
    # Renderizar el formulario de edición
    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()

    return render(request, 'editar_devolucion.html', {
        'devolucion': devolucion_instance,
        'productos': productos,
        'proveedores': proveedores
    })

def eliminar_devolucion(request, id_devolucion):
    devolucion = Devolucion.objects.filter(id_devolucion=id_devolucion).first()  # Buscar la devolución

    if devolucion is None:
        messages.error(request, 'Devolución no encontrada.')
    else:
        # Restaurar la cantidad al producto antes de eliminar la devolución
        producto = devolucion.producto
        producto.cantidad += devolucion.cantidad  # Aumentar la cantidad del producto
        producto.save()

        devolucion.delete()
        messages.success(request, 'Devolución eliminada exitosamente.')

    return redirect('devolucion')
