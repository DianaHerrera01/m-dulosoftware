from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EntradaProducto  
from apps.producto.models import Producto, Categoria
from apps.proveedor.models import Proveedor  
from apps.Pedido.models import Pedido
from django.db import transaction

# Vista para listar y agregar entradas de producto
def entradas_producto(request):
    entradas = EntradaProducto.objects.all()  # Listar todas las entradas
    productos = Producto.objects.all()  # Obtener todos los productos
    proveedores = Proveedor.objects.all()  # Obtener todos los proveedores
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    pedidos = Pedido.objects.all()  # Obtener todos los pedidos

    if request.method == 'POST':
        # Procesar el formulario de registro de entrada
        producto_id = request.POST['producto_id']
        proveedor_id = request.POST['proveedor_id']
        categoria_id = request.POST.get('categoria')
        cantidad = int(request.POST['cantidad'])  # Convertir a entero
        fecha = request.POST['fecha']
        precio_unidad_compra = request.POST.get('precio_unidad_compra')
        pedido_id = request.POST.get('pedido_id')  # Obtener el ID del pedido

        try:
            categoria = Categoria.objects.get(categoriaID=categoria_id)
            producto = Producto.objects.get(id_producto=producto_id)
            proveedor = Proveedor.objects.get(id_proveedor=proveedor_id)
            pedido = Pedido.objects.get(id_orden_pedido=pedido_id)  # Obtener el pedido correspondiente
        except (Categoria.DoesNotExist, Producto.DoesNotExist, Proveedor.DoesNotExist, Pedido.DoesNotExist) as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('entradas_producto')

        # Iniciar una transacción para asegurar la consistencia de los datos
        with transaction.atomic():
            # Crear y guardar la nueva entrada
            entrada = EntradaProducto(
                producto=producto,
                proveedor=proveedor,
                cantidad=cantidad,
                fecha=fecha,
                categoria=categoria,
                precio_unidad_compra=precio_unidad_compra,
                pedido=pedido  # Asocia la entrada al pedido
            )
            entrada.save()

            # Actualizar el precio de unidad compra en el producto
            producto.preciounidadcompra = precio_unidad_compra
            producto.save()

            messages.success(request, '¡Entrada de producto registrada y precio actualizado!')
            return redirect('entradas_producto')

    return render(request, 'entradas_producto.html', {
        'entradas': entradas,
        'productos': productos,
        'proveedores': proveedores,
        'categorias': categorias,
        'pedidos': pedidos  # Añadir pedidos a la plantilla
    })


# Vista para editar entrada de producto
def editar_entrada(request, id_entrada):
    try:
        entrada = EntradaProducto.objects.get(id_entrada=id_entrada)  # Obtener entrada por ID
    except EntradaProducto.DoesNotExist:
        messages.error(request, 'Entrada de producto no encontrada.')
        return redirect('entradas_producto')

    productos = Producto.objects.all()  # Obtener todos los productos
    proveedores = Proveedor.objects.all()  # Obtener todos los proveedores
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    pedidos = Pedido.objects.all()  # Obtener todos los pedidos

    if request.method == 'POST':
        # Procesar el formulario de actualización
        try:
            entrada.producto = Producto.objects.get(id_producto=request.POST['producto_id'])
            entrada.proveedor = Proveedor.objects.get(id_proveedor=request.POST['proveedor_id'])
            entrada.categoria = Categoria.objects.get(categoriaID=request.POST['categoria'])
            entrada.cantidad = int(request.POST['cantidad'])
            entrada.fecha = request.POST['fecha']
            entrada.precio_unidad_compra = request.POST['precio_unidad_compra']  # Tomar el nuevo precio

            # Actualizar el precio en el producto
            entrada.producto.preciounidadcompra = entrada.precio_unidad_compra  
            entrada.producto.save()  # Guarda los cambios en el producto

            entrada.save()  
            messages.success(request, '¡Entrada de producto actualizada exitosamente!')
            return redirect('entradas_producto')
        except (Producto.DoesNotExist, Proveedor.DoesNotExist, Categoria.DoesNotExist) as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'editar_entrada.html', {
        'entrada': entrada,
        'productos': productos,
        'proveedores': proveedores,
        'categorias': categorias,
        'pedidos': pedidos  # Añadir pedidos a la plantilla
    })

# Vista para eliminar entrada de producto
def eliminar_entrada_producto(request, id_entrada):
    try:
        entrada = EntradaProducto.objects.get(id_entrada=id_entrada)  # Obtener entrada por ID
        entrada.delete()
        messages.success(request, '¡Entrada de producto eliminada!')
    except EntradaProducto.DoesNotExist:
        messages.error(request, 'Entrada de producto no encontrada.')
    return redirect('entradas_producto')