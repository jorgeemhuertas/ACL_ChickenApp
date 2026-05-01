import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Archivo, Producto
from django.forms import modelform_factory
from .forms import LoginForm, RegistroForm
from .views_utils import calcular_acl

ARCHIVOS_PREDEFINIDOS = {
    '1': 'Top_Secret.txt',
    '2': 'Confidencial.txt',
    '3': 'Public.txt'
}

def login_view(request):
    mensaje_error = None
    if request.method == 'POST':
        modelo = request.POST.get('modelo', 'bell')
        form = LoginForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            password = form.cleaned_data['password']
            try:
                usuario = Usuario.objects.get(nombre=nombre)
                if usuario.check_password(password):
                    request.session['modelo_seguridad'] = modelo
                    return redirect('ver_archivos', usuario_id=usuario.id)
                else:
                    mensaje_error = "Contraseña incorrecta"
            except Usuario.DoesNotExist:
                mensaje_error = "Usuario no encontrado"
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'mensaje_error': mensaje_error})

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def ver_archivos(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    modelo = request.session.get('modelo_seguridad', 'bell') 
    guardado = False
    print(modelo)

    if request.method == 'POST':
        archivo_nombre = request.POST.get('archivo_nombre')
        contenido = request.POST.get('contenido')
        archivo_db = Archivo.objects.get(nombre=archivo_nombre)
        puede_leer, puede_escribir = calcular_acl(usuario, archivo_db, modelo)

        path = os.path.join(settings.ARCHIVOS_DIR, ARCHIVOS_PREDEFINIDOS[str(archivo_db.id)])

        if puede_escribir:
            guardado = True
            if puede_leer:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(contenido)
            else:
                with open(path, 'a', encoding='utf-8') as f:
                    f.write('\n' + contenido)

    permisos = []
    for archivo in Archivo.objects.all():
        puede_leer, puede_escribir = calcular_acl(usuario, archivo, modelo)
        path = os.path.join(settings.ARCHIVOS_DIR, ARCHIVOS_PREDEFINIDOS[str(archivo.id)])
        contenido = ""
        contenido_visible = False

        if os.path.exists(path) and puede_leer:
            with open(path, 'r', encoding='utf-8') as f:
                contenido = f.read()
                contenido_visible = True

        permisos.append({
            'archivo': archivo,
            'puede_leer': puede_leer,
            'puede_escribir': puede_escribir,
            'contenido': contenido,
            'contenido_visible': contenido_visible,
        })

    return render(request, 'ver_archivos.html', {
        'usuario': usuario,
        'permisos': permisos,
        'guardado': guardado,
        'modelo': modelo,
    })

ProductoForm = modelform_factory(Producto, fields=('nombre', 'precio'))

Paso1Form = modelform_factory(Producto, fields=('nombre', 'precio'))
Paso2Form = modelform_factory(Producto, fields=('descripcion',))

def editar_producto_paso1(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = Paso1Form(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('editar_producto_paso2', producto_id=producto.id)
    else:
        form = Paso1Form(instance=producto)

    return render(request, 'editar_producto_paso1.html', {'form': form, 'producto_id': producto.id})

def editar_producto_paso2(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = Paso2Form(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('producto_exito')
    else:
        form = Paso2Form(instance=producto)

    return render(request, 'editar_producto_paso2.html', {'form': form, 'producto_id': producto.id})