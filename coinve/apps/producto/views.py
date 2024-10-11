from django.shortcuts import render, redirect
from .models import Producto, Categoria
from apps.proveedor.models import Proveedor  
from django.contrib import messages


# Vista para registrar y listar productos 
def productos(request):
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()  # Obtener todos los proveedores
    productos = Producto.objects.all()  # Listar todos los productos

    if request.method == 'POST':
        # Procesar el formulario de registro
        nombre_producto = request.POST['nombre_producto']
        cantidad = request.POST['cantidad']
        categoria_id = request.POST['categoria']
        descripcion = request.POST['descripcion']
        proveedor_id = request.POST['proveedor_id']  
        preciounidadcompra = request.POST['precio_unidad_compra']
        preciounidadventa = request.POST['precio_unidad_venta']

        try:
            categoria = Categoria.objects.get(categoriaID=categoria_id)
            proveedor = Proveedor.objects.get(id_proveedor=proveedor_id)  
        except (Categoria.DoesNotExist, Proveedor.DoesNotExist):
            messages.error(request, 'Categoría o proveedor no encontrados.')
            return redirect('producto')

        # Crear y guardar el nuevo producto
        producto = Producto(
            nombre_producto=nombre_producto,
            cantidad=cantidad,
            categoria=categoria,
            descripcion=descripcion,
            proveedor=proveedor,  
            preciounidadcompra=preciounidadcompra,
            preciounidadventa=preciounidadventa
        )
        producto.save()
        messages.success(request, '¡Producto registrado!')
        return redirect('producto')

    return render(request, 'producto.html', {
        'categorias': categorias,
        'proveedores': proveedores,  
        'productos': productos
    })

# Vista para editar producto
def edicion_producto(request, id_producto):
    producto = Producto.objects.get(id_producto=id_producto)
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()  
    return render(request, 'editar_producto.html', {
        'producto': producto,
        'categorias': categorias,
        'proveedores': proveedores  
    })

def editar_producto(request):
    if request.method == 'POST':
        id_producto = request.POST['id_producto']
        nombre_producto = request.POST['nombre_producto']
        cantidad = request.POST['cantidad']
        categoria_id = request.POST['categoria']
        descripcion = request.POST['descripcion']
        proveedor_id = request.POST['proveedor_id']  
        precio_unidad_compra = request.POST['precio_unidad_compra']
        precio_unidad_venta = request.POST['precio_unidad_venta']

        producto = Producto.objects.get(id_producto=id_producto)
        categoria = Categoria.objects.get(categoriaID=categoria_id)
        proveedor = Proveedor.objects.get(id_proveedor=proveedor_id)  

        # Actualizar el producto con los nuevos datos
        producto.nombre_producto = nombre_producto
        producto.cantidad = cantidad
        producto.categoria = categoria
        producto.descripcion = descripcion
        producto.proveedor = proveedor  
        producto.preciounidadcompra = precio_unidad_compra
        producto.preciounidadventa = precio_unidad_venta
        producto.save()

        messages.success(request, '¡Producto actualizado exitosamente!')
        return redirect('producto')

# Vista para eliminar producto
def eliminar_producto(request, id_producto):
    producto = Producto.objects.get(id_producto=id_producto)
    producto.delete()
    messages.success(request, '¡Producto eliminado!')
    return redirect('listar_productos')

