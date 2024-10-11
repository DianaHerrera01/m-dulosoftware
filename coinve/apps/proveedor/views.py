from django.shortcuts import render, redirect
from .models import Proveedor, ProductoServicio
from django.contrib import messages

# Vista para registrar y listar proveedores 
def proveedores(request):
    proveedores = Proveedor.objects.all()  # Listar todos los proveedores
    productos_servicio = ProductoServicio.objects.all()  # Listar todos los productos o servicios

    if request.method == 'POST':
        # Procesar el formulario de registro
        nombre_proveedor = request.POST['nombre_proveedor']
        apellidos_proveedor = request.POST['apellidos_proveedor']
        correo = request.POST['correo']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        productos_servicio_ids = request.POST.getlist('producto_servicio')  # Selección de múltiples productos o servicios

        # Crear y guardar el nuevo proveedor
        proveedor = Proveedor(
            nombre_proveedor=nombre_proveedor,
            apellidos_proveedor=apellidos_proveedor,
            correo=correo,
            direccion=direccion,
            telefono=telefono,
        )
        proveedor.save()

        # Relacionar el proveedor con los productos o servicios seleccionados
        for producto_servicio_id in productos_servicio_ids:
            producto_servicio = ProductoServicio.objects.get(id_producto_servicio=producto_servicio_id)
            proveedor.productos.add(producto_servicio)

        messages.success(request, '¡Proveedor registrado con éxito!')
        return redirect('proveedor')  # Redirigir después de guardar el proveedor

    return render(request, 'proveedor.html', {
        'proveedores': proveedores,  # Lista de proveedores
        'productos_servicio': productos_servicio  # Lista de productos o servicios
    })


# Vista para editar 

def edicion_proveedor(request, id_proveedor):
    proveedor = Proveedor.objects.get(id_proveedor=id_proveedor)
    productos_servicio = ProductoServicio.objects.all()  # Opciones de productos o servicios
    return render(request, 'editar_proveedor.html', {'proveedor': proveedor, 'productos_servicio': productos_servicio})

# Vista para actualizar 

def editar_proveedor(request):
    if request.method == 'POST':
        id_proveedor = request.POST['id_proveedor']
        nombre_proveedor = request.POST['nombre_proveedor']
        apellidos_proveedor = request.POST['apellidos_proveedor']
        correo = request.POST['correo']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        producto_servicio_id = request.POST.get('producto_servicio')  # Selección del producto o servicio

        proveedor = Proveedor.objects.get(id_proveedor=id_proveedor)
        producto_servicio = ProductoServicio.objects.get(id_producto_servicio=producto_servicio_id)

        # Actualizar el proveedor con los nuevos datos
        proveedor.nombre_proveedor = nombre_proveedor
        proveedor.apellidos_proveedor = apellidos_proveedor
        proveedor.correo = correo
        proveedor.direccion = direccion
        proveedor.telefono = telefono
        proveedor.save()

        # Actualizar la relación con el producto o servicio
        producto_servicio.proveedor = proveedor
        producto_servicio.save()

        messages.success(request, '¡Proveedor actualizado exitosamente!')
        return redirect('proveedor')  # Redirigir después de la actualización
    
# Vista para eliminar
    
def eliminar_proveedor(request, id_proveedor):
    proveedor = Proveedor.objects.get(id_proveedor=id_proveedor)
    proveedor.delete()
    messages.success(request, '¡Proveedor eliminado!')
    return redirect('proveedor')
