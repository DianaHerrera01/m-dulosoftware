from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Pedido
from apps.producto.models import Producto
from apps.proveedor.models import Proveedor
from django.db import transaction
from apps.EntradaProducto.models import EntradaProducto

# Vista para listar y agregar pedidos

def pedidos(request):
    pedidos = Pedido.objects.all()  # Listar todos los pedidos
    productos = Producto.objects.all()  # Obtener todos los productos
    proveedores = Proveedor.objects.all()  # Obtener todos los proveedores

    if request.method == 'POST':
        # Procesar el formulario de registro de pedido
        producto_id = request.POST['producto_id']
        proveedor_id = request.POST['proveedor_id']
        cantidad = int(request.POST['cantidad'])

        try:
            producto = Producto.objects.get(id_producto=producto_id)
            proveedor = Proveedor.objects.get(id_proveedor=proveedor_id)
        except (Producto.DoesNotExist, Proveedor.DoesNotExist):
            messages.error(request, 'Producto o proveedor no encontrado.')
            return redirect('pedido')

        # Iniciar una transacción para asegurar la consistencia de los datos
        with transaction.atomic():
            # Crear y guardar el nuevo pedido
            pedido = Pedido(
                producto=producto,
                proveedor=proveedor,
                cantidad=cantidad,
            )
            pedido.save()

            messages.success(request, '¡Pedido registrado exitosamente!')
            return redirect('pedido')

    return render(request, 'pedido.html', {
        'pedidos': pedidos,
        'productos': productos,
        'proveedores': proveedores
    })

def recibir_pedido(request, id_pedido):
    try:
        pedido = Pedido.objects.get(id_orden_pedido=id_pedido)

        # Control de errores: Solo permitir recibir si el pedido no ha sido recibido ya
        if pedido.estado == 'Recibido':
            messages.error(request, 'Este pedido ya ha sido recibido.')
            return redirect('pedido')

        # Actualizar el inventario
        producto = pedido.producto
        producto.cantidad += pedido.cantidad  
        producto.save()

        # Actualizar la entrada de producto
        try:
            entrada_producto = EntradaProducto.objects.get(producto=producto)
            entrada_producto.cantidad += pedido.cantidad
            entrada_producto.save()
        except EntradaProducto.DoesNotExist:
            messages.warning(request, 'No se encontró la entrada de producto para actualizar.')

        # Marcar el pedido como recibido
        pedido.estado = 'Recibido'
        pedido.save()

        messages.success(request, '¡Pedido recibido y cantidades actualizadas en inventario!')
    except Pedido.DoesNotExist:
        messages.error(request, 'Pedido no encontrado.')
    return redirect('pedido')


# Vista para editar un pedido
def editar_pedido(request, id_pedido):
    pedido = Pedido.objects.get(id_orden_pedido=id_pedido)
    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        pedido.producto = Producto.objects.get(id_producto=request.POST['producto_id'])
        pedido.proveedor = Proveedor.objects.get(id_proveedor=request.POST['proveedor_id'])
        pedido.cantidad = int(request.POST['cantidad'])
        pedido.save()

        messages.success(request, '¡Pedido actualizado exitosamente!')
        return redirect('pedido')

    return render(request, 'editar_pedido.html', {
        'pedido': pedido,
        'productos': productos,
        'proveedores': proveedores
    })

# Vista para eliminar un pedido
def eliminar_pedido(request, id_pedido):
    pedido = Pedido.objects.get(id_orden_pedido=id_pedido)
    pedido.delete()
    messages.success(request, '¡Pedido eliminado!')
    return redirect('pedido')

