from django.shortcuts import render, redirect
from .models import Cliente, TipoDocumento
from django.contrib import messages

# Vista para listar y registrar clientes
def clientes(request):
    clientes = Cliente.objects.all()  # Listar todos los clientes
    tipos_documento = TipoDocumento.objects.all()  # Obtener todos los tipos de documento

    if request.method == 'POST':
        # Procesar el formulario de registro
        nombre_cliente = request.POST['nombre_cliente']
        apellidos_cliente = request.POST['apellidos_cliente']
        correo = request.POST['correo']
        id_tipo_docum = request.POST['tipo_documento']
        documento_cli = request.POST['documento_cli']
        telefono = request.POST['telefono']

        tipo_documento = TipoDocumento.objects.get(id_tipo_docum=id_tipo_docum)

        # Crear y guardar el nuevo cliente
        cliente = Cliente(
            nombre_cliente=nombre_cliente,
            apellidos_cliente=apellidos_cliente,
            correo=correo,
            id_tipo_docum=tipo_documento,
            documento_cli=documento_cli,
            telefono=telefono
        )
        cliente.save()
        messages.success(request, '¡Cliente registrado exitosamente!')
        return redirect('clientes')

    return render(request, 'clientes.html', {
        'clientes': clientes,
        'tipos_documento': tipos_documento,
    })

# Vista para editar un cliente
def edicion_cliente(request, id_cliente):
    cliente = Cliente.objects.get(id_cliente=id_cliente)
    tipos_documento = TipoDocumento.objects.all()  # Obtener todos los tipos de documento
    return render(request, 'editar_cliente.html', {
        'cliente': cliente,
        'tipos_documento': tipos_documento,
    })

# Vista para actualizar los datos de un cliente
def editar_cliente(request):
    if request.method == 'POST':
        id_cliente = request.POST['id_cliente']
        nombre_cliente = request.POST['nombre_cliente']
        apellidos_cliente = request.POST['apellidos_cliente']
        correo = request.POST['correo']
        id_tipo_docum = request.POST['tipo_documento']
        documento_cli = request.POST['documento_cli']
        telefono = request.POST['telefono']

        # Obtener el cliente y los objetos relacionados
        try:
            cliente = Cliente.objects.get(id_cliente=id_cliente)
            tipo_documento = TipoDocumento.objects.get(id_tipo_docum=id_tipo_docum)

            # Actualizar el cliente con los nuevos datos
            cliente.nombre_cliente = nombre_cliente
            cliente.apellidos_cliente = apellidos_cliente
            cliente.correo = correo
            cliente.id_tipo_docum = tipo_documento
            cliente.documento_cli = documento_cli
            cliente.telefono = telefono
            cliente.save()

            messages.success(request, '¡Cliente actualizado exitosamente!')
            return redirect('clientes')
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente no encontrado.')
            return redirect('clientes')
        except TipoDocumento.DoesNotExist:
            messages.error(request, 'Tipo de documento no válido.')
            return redirect('clientes')
        
    return redirect('clientes')

# Vista para eliminar un cliente
def eliminar_cliente(request, id_cliente):
    cliente = Cliente.objects.get(id_cliente=id_cliente)
    cliente.delete()
    messages.success(request, '¡Cliente eliminado!')
    return redirect('clientes')
