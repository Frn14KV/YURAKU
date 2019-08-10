from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Count
from django.urls import reverse_lazy

from django.http import HttpResponse
from gestionayuda.form import GuardarForm
from gestionbusqueda.models import Busqueda
from gestioncomentario.models import Comentario
from gestionescuela.models import Escuela
from gestionperfil.form import GuardarPerfilForm
from django.shortcuts import redirect, render, get_object_or_404

from YURAKU.forms import LoginForm, SignUpForm, EditProfileForm, Edit
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission, Group

from datetime import *

from gestionperfil.models import Perfil
from gestionplantas.models import Planta


# web service
# login
def weblogin(request):
    username = request.GET['username']
    password = request.GET['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            response = 'usuario correcto'
            return HttpResponse(response)
        else:
            response = 'datos incorrectos '
            return HttpResponse(response)
    else:
        response = 'el usuario no existe '
        return HttpResponse(response)


# Ingresar al Login
def login_view(request):
    return redirect('login')


# Salir del Sistema
def logout_view(request):
    logout(request)
    return redirect('homepage')


# Listado de Usuarios
@login_required
@permission_required('gestionescuela.agregar_escuela',reverse_lazy('homepage'))
def usuarios(request):
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    usuarios = User.objects.all().order_by('id')
    return render(request, 'usuario/usuarios.html', {'usuarios': usuarios, 'perfiles': perfiles})


# Pefil de Usuario
@login_required
def perfil(request, usuario_id):
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    escuelas = Escuela.objects.all()
    usuario = User.objects.get(id=usuario_id)
    #id = usuario.id
    form = GuardarPerfilForm()
    planta_buscada = Busqueda.objects.filter(Usuario_id=usuario.id).all()
    comentarios = Comentario.objects.filter(Usuario_id=usuario_id).all()
    print(comentarios)
    #perfil = Perfil.objects.filter(pk=id)
    return render(request, 'usuario/perfil.html',
                  {'formulario': form, 'comentarios': comentarios, 'usuario': usuario, 'planta_buscada': planta_buscada,
                   'perfiles': perfiles, 'escuelas': escuelas})


# Login de cualquier Usuario
def login_page(request):
    message = None
    plantas = Planta.objects.all()
    year = datetime.now().year
    dataset1 = Busqueda.objects \
        .values('Planta__nombre_planta') \
        .annotate(count=Count('Planta__nombre_planta', filter=Q(fecha_busqueda__year=year))) \
        .order_by('Planta')
    dataset = Busqueda.objects \
        .values('fecha_busqueda__month') \
        .annotate(fecha_busqueda_count=Count('fecha_busqueda__month')) \
        .order_by('fecha_busqueda__month')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    id = user.id
                    perfil = Perfil.objects.filter(pk=id)
                    if id:
                        usuario = User.objects.get(id=request.user.id)
                        id = usuario.id
                        perfiles = Perfil.objects.filter(Usuario_id=id)
                        if len(perfiles) > 0:
                            perfiles = Perfil.objects.filter(Usuario_id=id)
                        else:
                            perfiles = []
                    else:
                        perfiles = Perfil.objects.all()
                    if perfil.exists() == False:
                        return redirect('homepage')
                    else:
                        return render(request, 'homepage.html',
                                      {'perfiles': perfiles, 'plantas': plantas, 'dataset': dataset,
                                       'dataset1': dataset1})
                else:
                    message = "Tu usuario esta inactivo"
                    return render(request, 'inicio.html', {'message': message, 'form': form})
            else:
                message = "Nombre de usuario y/o password  incorrecto"
                return render(request, 'inicio.html', {'message': message, 'form': form})
    else:
        form = LoginForm()
    return render(request, 'inicio.html', {'message': message, 'form': form})


# Home
def homepage(request):
    plantas = Planta.objects.all().order_by("id")
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    year = datetime.now().year
    dataset1 = Busqueda.objects \
        .values('Planta__nombre_planta') \
        .annotate(count=Count('Planta__nombre_planta', filter=Q(fecha_busqueda__year=year))) \
        .order_by('Planta')
    dataset = Busqueda.objects \
        .values('fecha_busqueda__month') \
        .annotate(fecha_busqueda_count=Count('fecha_busqueda__month')) \
        .order_by('fecha_busqueda__month')
    return render(request, 'homepage.html',
                  {'perfiles': perfiles, 'plantas': plantas, 'dataset': dataset, 'dataset1': dataset1})


# Informacion Aplicacion
def aplicacion(request):
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    return render(request, 'apliacion.html', {'perfiles':perfiles})


# Agregar Usuario
@login_required
@permission_required('gestionescuela.agregar_escuela',reverse_lazy('homepage'))
def agregar_usuario(request):
    message = None
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    global correoer
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            correoe = form.cleaned_data.get('email')
            if correoe == correoer:
                form.save()
                typeuser = form.cleaned_data.get('typeuser')

                # grupo de usuarios
                g_estudiantes, gel = Group.objects.get_or_create(name='Estudiantes')
                g_profesores, gpl = Group.objects.get_or_create(name='Profesores')
                g_administradores, gad1 = Group.objects.get_or_create(name='Administradores')
                g_superusuarios, gsp1 = Group.objects.get_or_create(name='SuperUsuarios')

                # contenttype
                ce = ContentType.objects.get_for_model(Escuela)

                cp = ContentType.objects.get_for_model(Perfil)

                cpl = ContentType.objects.get_for_model(Planta)

                # Permisos de Escuela
                permiso1e, pe1 = Permission.objects.get_or_create(codename='listar_escuela',
                                                                  name='Puede listar Escuelas',
                                                                  content_type=ce)
                permiso2e, pe2 = Permission.objects.get_or_create(codename='agregar_escuela',
                                                                  name='Puede agregar Escuelas',
                                                                  content_type=ce)
                permiso3e, pe3 = Permission.objects.get_or_create(codename='editar_escuela',
                                                                  name='Puede editar Escuelas',
                                                                  content_type=ce)
                permiso4e, pe4 = Permission.objects.get_or_create(codename='eliminar_escuela',
                                                                  name='Puede eliminar Escuela',
                                                                  content_type=ce)

                # Permisos de Perfil
                permiso1p, pp1 = Permission.objects.get_or_create(codename='listar_perfil',
                                                                  name='Puede listar Perfiles',
                                                                  content_type=cp)
                permiso2p, pp2 = Permission.objects.get_or_create(codename='agregar_perfil',
                                                                  name='Puede agregar Perfiles',
                                                                  content_type=cp)
                permiso3p, pp3 = Permission.objects.get_or_create(codename='editar_perfil',
                                                                  name='Puede editar Perfiles',
                                                                  content_type=cp)
                permiso4p, pp4 = Permission.objects.get_or_create(codename='eliminar_perfil',
                                                                  name='Puede eliminar Perfiles',
                                                                  content_type=cp)

                # Permisos de Planta
                permiso1pp, ppl1 = Permission.objects.get_or_create(codename='listar_planta',
                                                                    name='Puede listar Plantas',
                                                                    content_type=cpl)
                permiso2pp, ppl2 = Permission.objects.get_or_create(codename='agregar_planta',
                                                                    name='Puede agregar Plantas',
                                                                    content_type=cpl)
                permiso3pp, ppl3 = Permission.objects.get_or_create(codename='editar_planta',
                                                                    name='Puede editar Plantas',
                                                                    content_type=cpl)
                permiso4pp, ppl4 = Permission.objects.get_or_create(codename='eliminar_planta',
                                                                    name='Puede eliminar Plantas',
                                                                    content_type=cpl)
                # Permisos para el Estudiante
                # Estudiante con permisos de Escuela
                g_estudiantes.permissions.add(permiso1e)
                # Estudiante con permisos de Perfil
                g_estudiantes.permissions.add(permiso1p)
                g_estudiantes.permissions.add(permiso2p)
                g_estudiantes.permissions.add(permiso3p)
                g_estudiantes.permissions.add(permiso4p)
                # Estudiante con permisos de Planta
                g_estudiantes.permissions.add(permiso1pp)

                # Permisos para el Profesor
                # Estudiante con permisos de Escuela
                g_profesores.permissions.add(permiso1e)
                # Estudiante con permisos de Perfil
                g_profesores.permissions.add(permiso1p)
                g_profesores.permissions.add(permiso2p)
                g_profesores.permissions.add(permiso3p)
                g_profesores.permissions.add(permiso4p)
                # Estudiante con permisos de Planta
                g_profesores.permissions.add(permiso1pp)

                # Permisos para el Administrador
                # Estudiante con permisos de Escuela
                g_administradores.permissions.add(permiso1e)
                g_administradores.permissions.add(permiso2e)
                g_administradores.permissions.add(permiso3e)
                # Estudiante con permisos de Perfil
                g_administradores.permissions.add(permiso1p)
                # Estudiante con permisos de Planta
                g_administradores.permissions.add(permiso1pp)
                g_administradores.permissions.add(permiso2pp)
                g_administradores.permissions.add(permiso3pp)

                # Permisos para el SuperUsuario
                # Estudiante con permisos de Escuela
                g_superusuarios.permissions.add(permiso1e)
                g_superusuarios.permissions.add(permiso2e)
                g_superusuarios.permissions.add(permiso3e)
                g_superusuarios.permissions.add(permiso4e)
                # Estudiante con permisos de Perfil
                g_superusuarios.permissions.add(permiso1p)
                # Estudiante con permisos de Planta
                g_superusuarios.permissions.add(permiso1pp)
                g_superusuarios.permissions.add(permiso2pp)
                g_superusuarios.permissions.add(permiso3pp)
                g_superusuarios.permissions.add(permiso4pp)

                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                # user =User.objects.get(username=request.POST.get('username'))

                if typeuser == 'Estudiantes':
                    user.groups.add(g_estudiantes)
                elif typeuser == 'Profesores':
                    user.groups.add(g_profesores)
                elif typeuser == 'Administradores':
                    user.groups.add(g_administradores)
                elif typeuser == 'Superusuarios':
                    user.groups.add(g_superusuarios)
                else:
                    a = "No hay"
                f = open('media/datos/' + username + '.txt', 'w')
                f.close()
                return redirect('usuarios')
            else:
                message = "Al parecer los correos no son iguales. "
                return render(request, 'usuario/agregar_usuario.html',
                              {'message': message, 'form': form, 'perfiles': perfiles})
        else:
            form = SignUpForm(request.POST)
            m = form.errors.as_json()
            partes = m.split('message')
            a = None
            if (len(partes)) == 2:
                mt = partes[1].split(',')
                a = mt[0].split('"')
                message = a[2]
            elif (len(partes)) == 3:
                mt = partes[1].split(',')
                mt1 = partes[2].split(',')
                a = mt[0].split('"')
                a1 = mt1[0].split('"')
                message = (a[2] + a1[2])
            elif (len(partes)) == 4:
                mt = partes[1].split(',')
                mt1 = partes[2].split(',')
                mt2 = partes[3].split(',')
                a = mt[0].split('"')
                a1 = mt1[0].split('"')
                a2 = mt2[0].split('"')
                message = (a[2] + a1[2] + a2[2])

            return render(request, 'usuario/agregar_usuario.html',
                          {'message': message, 'form': form, 'perfiles': perfiles})
    else:
        form = SignUpForm()
    return render(request, 'usuario/agregar_usuario.html', {'message': message, 'form': form, 'perfiles': perfiles})


# Registro Normal
def registro(request):
    message = None
    plantas = Planta.objects.all().order_by("id")
    dataset1 = Busqueda.objects \
        .values('Planta__nombre_planta') \
        .annotate(count=Count('Planta__nombre_planta', filter=Q(fecha_busqueda__year='2019'))) \
        .order_by('Planta')
    dataset = Busqueda.objects \
        .values('fecha_busqueda__month') \
        .annotate(fecha_busqueda_count=Count('fecha_busqueda__month')) \
        .order_by('fecha_busqueda__month')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        form1 = GuardarForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            if form1.is_valid():
                correoer = form1.cleaned_data.get('email1')
            else:
                correoer = None

            correoe = form.cleaned_data.get('email')
            if correoe == correoer:
                form.save()
                typeuser = form.cleaned_data.get('typeuser')

                # grupo de usuarios
                g_estudiantes, gel = Group.objects.get_or_create(name='Estudiantes')
                g_profesores, gpl = Group.objects.get_or_create(name='Profesores')
                g_administradores, gad1 = Group.objects.get_or_create(name='Administradores')
                g_superusuarios, gsp1 = Group.objects.get_or_create(name='SuperUsuarios')

                # contenttype
                ce = ContentType.objects.get_for_model(Escuela)
                cp = ContentType.objects.get_for_model(Perfil)
                cpl = ContentType.objects.get_for_model(Planta)

                # Permisos de Escuela
                permiso1e, pe1 = Permission.objects.get_or_create(codename='listar_escuela',
                                                                  name='Puede listar Escuelas',
                                                                  content_type=ce)
                permiso2e, pe2 = Permission.objects.get_or_create(codename='agregar_escuela',
                                                                  name='Puede agregar Escuelas',
                                                                  content_type=ce)
                permiso3e, pe3 = Permission.objects.get_or_create(codename='editar_escuela',
                                                                  name='Puede editar Escuelas',
                                                                  content_type=ce)
                permiso4e, pe4 = Permission.objects.get_or_create(codename='eliminar_escuela',
                                                                  name='Puede eliminar Escuela',
                                                                  content_type=ce)
                # Permisos de Perfil
                permiso1p, pp1 = Permission.objects.get_or_create(codename='listar_perfil',
                                                                  name='Puede listar Perfiles',
                                                                  content_type=cp)
                permiso2p, pp2 = Permission.objects.get_or_create(codename='agregar_perfil',
                                                                  name='Puede agregar Perfiles',
                                                                  content_type=cp)
                permiso3p, pp3 = Permission.objects.get_or_create(codename='editar_perfil',
                                                                  name='Puede editar Perfiles',
                                                                  content_type=cp)
                permiso4p, pp4 = Permission.objects.get_or_create(codename='eliminar_perfil',
                                                                  name='Puede eliminar Perfiles',
                                                                  content_type=cp)
                # Permisos de Planta
                permiso1pp, ppl1 = Permission.objects.get_or_create(codename='listar_planta',
                                                                    name='Puede listar Plantas',
                                                                    content_type=cpl)
                permiso2pp, ppl2 = Permission.objects.get_or_create(codename='agregar_planta',
                                                                    name='Puede agregar Plantas',
                                                                    content_type=cpl)
                permiso3pp, ppl3 = Permission.objects.get_or_create(codename='editar_planta',
                                                                    name='Puede editar Plantas',
                                                                    content_type=cpl)
                permiso4pp, ppl4 = Permission.objects.get_or_create(codename='eliminar_planta',
                                                                    name='Puede eliminar Plantas',
                                                                    content_type=cpl)
                # Permisos para el Estudiante
                # Estudiante con permisos de Escuela
                g_estudiantes.permissions.add(permiso1e)
                # Estudiante con permisos de Perfil
                g_estudiantes.permissions.add(permiso1p)
                g_estudiantes.permissions.add(permiso2p)
                g_estudiantes.permissions.add(permiso3p)
                g_estudiantes.permissions.add(permiso4p)
                # Estudiante con permisos de Planta
                g_estudiantes.permissions.add(permiso1pp)

                # Permisos para el Profesor
                # Estudiante con permisos de Escuela
                g_profesores.permissions.add(permiso1e)
                # Estudiante con permisos de Perfil
                g_profesores.permissions.add(permiso1p)
                g_profesores.permissions.add(permiso2p)
                g_profesores.permissions.add(permiso3p)
                g_profesores.permissions.add(permiso4p)
                # Estudiante con permisos de Planta
                g_profesores.permissions.add(permiso1pp)

                # Permisos para el Administrador
                # Estudiante con permisos de Escuela
                g_administradores.permissions.add(permiso1e)
                g_administradores.permissions.add(permiso2e)
                g_administradores.permissions.add(permiso3e)
                # Estudiante con permisos de Perfil
                g_administradores.permissions.add(permiso1p)
                # Estudiante con permisos de Planta
                g_administradores.permissions.add(permiso1pp)
                g_administradores.permissions.add(permiso2pp)
                g_administradores.permissions.add(permiso3pp)

                # Permisos para el SuperUsuario
                # Estudiante con permisos de Escuela
                g_superusuarios.permissions.add(permiso1e)
                g_superusuarios.permissions.add(permiso2e)
                g_superusuarios.permissions.add(permiso3e)
                g_superusuarios.permissions.add(permiso4e)
                # Estudiante con permisos de Perfil
                g_superusuarios.permissions.add(permiso1p)
                # Estudiante con permisos de Planta
                g_superusuarios.permissions.add(permiso1pp)
                g_superusuarios.permissions.add(permiso2pp)
                g_superusuarios.permissions.add(permiso3pp)
                g_superusuarios.permissions.add(permiso4pp)

                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                # user =User.objects.get(username=request.POST.get('username'))

                if typeuser == 'Estudiantes' or typeuser == "on":
                    user.groups.add(g_estudiantes)
                elif typeuser == 'Profesores':
                    user.groups.add(g_profesores)
                elif typeuser == 'Administradores':
                    user.groups.add(g_administradores)
                elif typeuser == 'Superusuarios':
                    user.groups.add(g_superusuarios)
                else:
                    a = "No hay"

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        f = open('media/datos/' + username + '.txt', 'w')
                        f.close()
                        return redirect('homepage')
                    else:
                        message = "Tu usuario esta inactivo"
                        return render(request, 'registro.html', {'message': message, 'form': form})
            else:
                message = "Al parecer los correos no son iguales."
                return render(request, 'registro.html',
                              {'message': message, 'form': form})
        else:
            form = SignUpForm(request.POST)
            m = form.errors.as_json()
            partes = m.split('message')
            a = None
            if (len(partes)) == 2:
                mt = partes[1].split(',')
                a = mt[0].split('"')
                message = a[2]
            elif (len(partes)) == 3:
                mt = partes[1].split(',')
                mt1 = partes[2].split(',')
                a = mt[0].split('"')
                a1 = mt1[0].split('"')
                message = (a[2] + a1[2])
            elif (len(partes)) == 4:
                mt = partes[1].split(',')
                mt1 = partes[2].split(',')
                mt2 = partes[3].split(',')
                a = mt[0].split('"')
                a1 = mt1[0].split('"')
                a2 = mt2[0].split('"')
                message = (a[2] + a1[2] + a2[2])

            return render(request, 'registro.html',
                          {'message': message, 'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'message': message, 'form': form})


# Registro Administradores
def registroad(request):
    message = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        form1 = GuardarForm(request.POST)
        if form.is_valid():
            if form1.is_valid():
                correoer = form1.cleaned_data.get('email1')
            else:
                correoer = None

            correoe = form.cleaned_data.get('email')
            if correoe == correoer:
                form.save()
                typeuser = form.cleaned_data.get('typeuser')

                # grupo de usuarios
                g_estudiantes, gel = Group.objects.get_or_create(name='Estudiantes')
                g_profesores, gpl = Group.objects.get_or_create(name='Profesores')
                g_administradores, gad1 = Group.objects.get_or_create(name='Administradores')
                g_superusuarios, gsp1 = Group.objects.get_or_create(name='SuperUsuarios')

                # contenttype
                ce = ContentType.objects.get_for_model(Escuela)

                cp = ContentType.objects.get_for_model(Perfil)

                cpl = ContentType.objects.get_for_model(Planta)

                # Permisos de Escuela
                permiso1e, pe1 = Permission.objects.get_or_create(codename='listar_escuela',
                                                                  name='Puede listar Escuelas',
                                                                  content_type=ce)
                permiso2e, pe2 = Permission.objects.get_or_create(codename='agregar_escuela',
                                                                  name='Puede agregar Escuelas',
                                                                  content_type=ce)
                permiso3e, pe3 = Permission.objects.get_or_create(codename='editar_escuela',
                                                                  name='Puede editar Escuelas',
                                                                  content_type=ce)
                permiso4e, pe4 = Permission.objects.get_or_create(codename='eliminar_escuela',
                                                                  name='Puede eliminar Escuela',
                                                                  content_type=ce)
                # Permisos de Perfil
                permiso1p, pp1 = Permission.objects.get_or_create(codename='listar_perfil',
                                                                  name='Puede listar Perfiles',
                                                                  content_type=cp)
                permiso2p, pp2 = Permission.objects.get_or_create(codename='agregar_perfil',
                                                                  name='Puede agregar Perfiles',
                                                                  content_type=cp)
                permiso3p, pp3 = Permission.objects.get_or_create(codename='editar_perfil',
                                                                  name='Puede editar Perfiles',
                                                                  content_type=cp)
                permiso4p, pp4 = Permission.objects.get_or_create(codename='eliminar_perfil',
                                                                  name='Puede eliminar Perfiles',
                                                                  content_type=cp)
                # Permisos de Planta
                permiso1pp, ppl1 = Permission.objects.get_or_create(codename='listar_planta',
                                                                    name='Puede listar Plantas',
                                                                    content_type=cpl)
                permiso2pp, ppl2 = Permission.objects.get_or_create(codename='agregar_planta',
                                                                    name='Puede agregar Plantas',
                                                                    content_type=cpl)
                permiso3pp, ppl3 = Permission.objects.get_or_create(codename='editar_planta',
                                                                    name='Puede editar Plantas',
                                                                    content_type=cpl)
                permiso4pp, ppl4 = Permission.objects.get_or_create(codename='eliminar_planta',
                                                                    name='Puede eliminar Plantas',
                                                                    content_type=cpl)
                # Permisos para el Estudiante
                # Estudiante con permisos de Escuela
                g_estudiantes.permissions.add(permiso1e)
                # Estudiante con permisos de Perfil
                g_estudiantes.permissions.add(permiso1p)
                g_estudiantes.permissions.add(permiso2p)
                g_estudiantes.permissions.add(permiso3p)
                g_estudiantes.permissions.add(permiso4p)
                # Estudiante con permisos de Planta
                g_estudiantes.permissions.add(permiso1pp)

                # Permisos para el Profesor
                # Estudiante con permisos de Escuela
                g_profesores.permissions.add(permiso1e)
                # Estudiante con permisos de Perfil
                g_profesores.permissions.add(permiso1p)
                g_profesores.permissions.add(permiso2p)
                g_profesores.permissions.add(permiso3p)
                g_profesores.permissions.add(permiso4p)
                # Estudiante con permisos de Planta
                g_profesores.permissions.add(permiso1pp)

                # Permisos para el Administrador
                # Estudiante con permisos de Escuela
                g_administradores.permissions.add(permiso1e)
                g_administradores.permissions.add(permiso2e)
                g_administradores.permissions.add(permiso3e)
                # Estudiante con permisos de Perfil
                g_administradores.permissions.add(permiso1p)
                # Estudiante con permisos de Planta
                g_administradores.permissions.add(permiso1pp)
                g_administradores.permissions.add(permiso2pp)
                g_administradores.permissions.add(permiso3pp)

                # Permisos para el SuperUsuario
                # Estudiante con permisos de Escuela
                g_superusuarios.permissions.add(permiso1e)
                g_superusuarios.permissions.add(permiso2e)
                g_superusuarios.permissions.add(permiso3e)
                g_superusuarios.permissions.add(permiso4e)
                # Estudiante con permisos de Perfil
                g_superusuarios.permissions.add(permiso1p)
                # Estudiante con permisos de Planta
                g_superusuarios.permissions.add(permiso1pp)
                g_superusuarios.permissions.add(permiso2pp)
                g_superusuarios.permissions.add(permiso3pp)
                g_superusuarios.permissions.add(permiso4pp)

                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                # user =User.objects.get(username=request.POST.get('username'))

                if typeuser == 'Estudiantes':
                    user.groups.add(g_estudiantes)
                elif typeuser == 'Profesores':
                    user.groups.add(g_profesores)
                elif typeuser == 'Administradores':
                    user.groups.add(g_administradores)
                elif typeuser == 'Superusuarios':
                    user.groups.add(g_superusuarios)
                else:
                    a = "No hay"

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('homepage')
                    else:
                        message = "Tu usuario esta inactivo"
                        return render(request, 'usuario/registroad.html', {'message': message, 'form': form})
            else:
                message = "Al parecer los correos no son iguales."
                return render(request, 'usuario/registroad.html',
                              {'message': message, 'form': form})
        else:
            form = SignUpForm(request.POST)
            m = form.errors.as_json()
            partes = m.split('message')
            a = None
            if (len(partes)) == 2:
                mt = partes[1].split(',')
                a = mt[0].split('"')
                message = a[2]
            elif (len(partes)) == 3:
                mt = partes[1].split(',')
                mt1 = partes[2].split(',')
                a = mt[0].split('"')
                a1 = mt1[0].split('"')
                message = (a[2] + a1[2])
            elif (len(partes)) == 4:
                mt = partes[1].split(',')
                mt1 = partes[2].split(',')
                mt2 = partes[3].split(',')
                a = mt[0].split('"')
                a1 = mt1[0].split('"')
                a2 = mt2[0].split('"')
                message = (a[2] + a1[2] + a2[2])

            return render(request, 'usuario/registroad.html', {'message': message, 'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'usuario/registroad.html', {'message': message, 'form': form})


# Registro Super Usuarios
def registrosp(request):
    message = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        form1 = GuardarForm(request.POST)
        if form.is_valid():
            if form1.is_valid():
                correoer = form1.cleaned_data.get('email1')
            else:
                correoer = None

            correoe = form.cleaned_data.get('email')
            if correoe == correoer:
                form.save()
                typeuser = form.cleaned_data.get('typeuser')

                # grupo de usuarios
                g_estudiantes, gel = Group.objects.get_or_create(name='Estudiantes')
                g_profesores, gpl = Group.objects.get_or_create(name='Profesores')
                g_administradores, gad1 = Group.objects.get_or_create(name='Administradores')
                g_superusuarios, gsp1 = Group.objects.get_or_create(name='SuperUsuarios')

                # contenttype
                ce = ContentType.objects.get_for_model(Escuela)

                cp = ContentType.objects.get_for_model(Perfil)

                cpl = ContentType.objects.get_for_model(Planta)

                # Permisos de Escuela
                permiso1e, pe1 = Permission.objects.get_or_create(codename='listar_escuela',
                                                                  name='Puede listar Escuelas',
                                                                  content_type=ce)
                permiso2e, pe2 = Permission.objects.get_or_create(codename='agregar_escuela',
                                                                  name='Puede agregar Escuelas',
                                                                  content_type=ce)
                permiso3e, pe3 = Permission.objects.get_or_create(codename='editar_escuela',
                                                                  name='Puede editar Escuelas',
                                                                  content_type=ce)
                permiso4e, pe4 = Permission.objects.get_or_create(codename='eliminar_escuela',
                                                                  name='Puede eliminar Escuela',
                                                                  content_type=ce)
                # Permisos de Perfil
                permiso1p, pp1 = Permission.objects.get_or_create(codename='listar_perfil',
                                                                  name='Puede listar Perfiles',
                                                                  content_type=cp)
                permiso2p, pp2 = Permission.objects.get_or_create(codename='agregar_perfil',
                                                                  name='Puede agregar Perfiles',
                                                                  content_type=cp)
                permiso3p, pp3 = Permission.objects.get_or_create(codename='editar_perfil',
                                                                  name='Puede editar Perfiles',
                                                                  content_type=cp)
                permiso4p, pp4 = Permission.objects.get_or_create(codename='eliminar_perfil',
                                                                  name='Puede eliminar Perfiles',
                                                                  content_type=cp)
                # Permisos de Planta
                permiso1pp, ppl1 = Permission.objects.get_or_create(codename='listar_planta',
                                                                    name='Puede listar Plantas',
                                                                    content_type=cpl)
                permiso2pp, ppl2 = Permission.objects.get_or_create(codename='agregar_planta',
                                                                    name='Puede agregar Plantas',
                                                                    content_type=cpl)
                permiso3pp, ppl3 = Permission.objects.get_or_create(codename='editar_planta',
                                                                    name='Puede editar Plantas',
                                                                    content_type=cpl)
                permiso4pp, ppl4 = Permission.objects.get_or_create(codename='eliminar_planta',
                                                                    name='Puede eliminar Plantas',
                                                                    content_type=cpl)
                # Permisos para el Estudiante
                # Estudiante con permisos de Escuela
                g_estudiantes.permissions.add(permiso1e)
                # Estudiante con permisos de Perfil
                g_estudiantes.permissions.add(permiso1p)
                g_estudiantes.permissions.add(permiso2p)
                g_estudiantes.permissions.add(permiso3p)
                g_estudiantes.permissions.add(permiso4p)
                # Estudiante con permisos de Planta
                g_estudiantes.permissions.add(permiso1pp)

                # Permisos para el Profesor
                # Estudiante con permisos de Escuela
                g_profesores.permissions.add(permiso1e)
                # Estudiante con permisos de Perfil
                g_profesores.permissions.add(permiso1p)
                g_profesores.permissions.add(permiso2p)
                g_profesores.permissions.add(permiso3p)
                g_profesores.permissions.add(permiso4p)
                # Estudiante con permisos de Planta
                g_profesores.permissions.add(permiso1pp)

                # Permisos para el Administrador
                # Estudiante con permisos de Escuela
                g_administradores.permissions.add(permiso1e)
                g_administradores.permissions.add(permiso2e)
                g_administradores.permissions.add(permiso3e)
                # Estudiante con permisos de Perfil
                g_administradores.permissions.add(permiso1p)
                # Estudiante con permisos de Planta
                g_administradores.permissions.add(permiso1pp)
                g_administradores.permissions.add(permiso2pp)
                g_administradores.permissions.add(permiso3pp)

                # Permisos para el SuperUsuario
                # Estudiante con permisos de Escuela
                g_superusuarios.permissions.add(permiso1e)
                g_superusuarios.permissions.add(permiso2e)
                g_superusuarios.permissions.add(permiso3e)
                g_superusuarios.permissions.add(permiso4e)
                # Estudiante con permisos de Perfil
                g_superusuarios.permissions.add(permiso1p)
                # Estudiante con permisos de Planta
                g_superusuarios.permissions.add(permiso1pp)
                g_superusuarios.permissions.add(permiso2pp)
                g_superusuarios.permissions.add(permiso3pp)
                g_superusuarios.permissions.add(permiso4pp)

                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                # user =User.objects.get(username=request.POST.get('username'))

                if typeuser == 'Estudiantes':
                    user.groups.add(g_estudiantes)
                elif typeuser == 'Profesores':
                    user.groups.add(g_profesores)
                elif typeuser == 'Administradores':
                    user.groups.add(g_administradores)
                elif typeuser == 'Superusuarios':
                    user.groups.add(g_superusuarios)
                else:
                    a = "no hay"

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('homepage')
                    else:
                        message = "Tu usuario esta inactivo"
                        return render(request, 'usuario/registrosp.html', {'message': message, 'form': form})
            else:
                message = "Al parecer los correos no son iguales."
                return render(request, 'usuario/registrosp.html',
                              {'message': message, 'form': form})
        else:
            form = SignUpForm(request.POST)
            m = form.errors.as_json()
            partes = m.split('message')
            a = None
            if (len(partes)) == 2:
                mt = partes[1].split(',')
                a = mt[0].split('"')
                message = a[2]
            elif (len(partes)) == 3:
                mt = partes[1].split(',')
                mt1 = partes[2].split(',')
                a = mt[0].split('"')
                a1 = mt1[0].split('"')
                message = (a[2] + a1[2])
            elif (len(partes)) == 4:
                mt = partes[1].split(',')
                mt1 = partes[2].split(',')
                mt2 = partes[3].split(',')
                a = mt[0].split('"')
                a1 = mt1[0].split('"')
                a2 = mt2[0].split('"')
                message = (a[2] + a1[2] + a2[2])

            return render(request, 'usuario/registrosp.html', {'message': message, 'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'usuario/registrosp.html', {'message': message, 'form': form})


# Cambio de clave
@login_required
def cambiar_clave(request, usuario_id):
    escuelas = Escuela.objects.all()
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    usuario = User.objects.get(id=request.user.id)
    id = usuario.id
    perfil = Perfil.objects.filter(pk=id)
    form = Edit(request.POST)
    if form.is_valid():
        a = "no hay"
    password1 = form.cleaned_data.get('password1')
    password2 = form.cleaned_data.get('password2')
    us = User.objects.get(id=usuario_id)
    username = us.username
    if us is None:
        a = "No hay"
    else:
        if (password1 == password2) and password2 is not None:
            us.set_password(password1)
            us.save()
            us = authenticate(username=username, password=password1)
            if us is not None:
                if us.is_active:
                    login(request, us)
                    message = "Editado con éxito"
                    if perfil.exists() == False:
                        form = GuardarPerfilForm()
                        planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
                        return render(request, 'usuario/perfil.html',
                                      {'message': message, 'formulario': form, 'usuario': usuario,
                                       'planta_buscada': planta_buscada,
                                       'perfil': perfil, 'perfiles': perfiles, 'escuelas': escuelas})
                    else:
                        fecha = perfil.get().fecha_nacimiento_perfil
                        if fecha is not None:
                            factiva = "Si"
                        else:
                            factiva = None
                        perfil = get_object_or_404(Perfil, id=usuario_id)
                        form = GuardarPerfilForm(instance=perfil)
                        escuela = get_object_or_404(Escuela, pk=perfil.Escuela_perfil.id)
                        planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
                        return render(request, 'usuario/perfil_1.html',
                                      {'message': message, 'formulario': form, 'usuario': usuario,
                                       'planta_buscada': planta_buscada,
                                       'perfil': perfil, 'perfiles': perfiles, 'escuela': escuela, 'escuelas': escuelas,
                                       'factiva': factiva})
                else:
                    message = "Tu usuario esta inactivo"
                    if perfil.exists() == False:
                        form = GuardarPerfilForm()
                        planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
                        return render(request, 'usuario/perfil.html',
                                      {'message': message, 'formulario': form, 'usuario': usuario,
                                       'planta_buscada': planta_buscada,
                                       'perfil': perfil, 'perfiles': perfiles, 'escuelas': escuelas})
                    else:
                        fecha = perfil.get().fecha_nacimiento_perfil
                        if fecha is not None:
                            factiva = "Si"
                        else:
                            factiva = None
                        perfil = get_object_or_404(Perfil, id=usuario_id)
                        form = GuardarPerfilForm(instance=perfil)
                        escuela = get_object_or_404(Escuela, pk=perfil.Escuela_perfil.id)
                        planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
                        return render(request, 'usuario/perfil_1.html',
                                      {'message': message, 'formulario': form, 'usuario': usuario,
                                       'planta_buscada': planta_buscada,
                                       'perfil': perfil, 'perfiles': perfiles, 'escuela': escuela, 'escuelas': escuelas,
                                       'factiva': factiva})
            else:
                message = "Nombre de usuario y/o password  incorrecto"
                if perfil.exists() == False:
                    form = GuardarPerfilForm()
                    planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
                    return render(request, 'usuario/perfil.html',
                                  {'message': message, 'formulario': form, 'usuario': usuario,
                                   'planta_buscada': planta_buscada,
                                   'perfil': perfil, 'perfiles': perfiles, 'escuelas': escuelas})
                else:
                    fecha = perfil.get().fecha_nacimiento_perfil
                    if fecha is not None:
                        factiva = "Si"
                    else:
                        factiva = None
                    perfil = get_object_or_404(Perfil, id=usuario_id)
                    form = GuardarPerfilForm(instance=perfil)
                    escuela = get_object_or_404(Escuela, pk=perfil.Escuela_perfil.id)
                    planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
                    return render(request, 'usuario/perfil_1.html',
                                  {'message': message, 'formulario': form, 'usuario': usuario,
                                   'planta_buscada': planta_buscada,
                                   'perfil': perfil, 'perfiles': perfiles, 'escuela': escuela, 'escuelas': escuelas,
                                   'factiva': factiva})
        elif password1 is None and password2 is None:
            if perfil.exists() == False:
                form = GuardarPerfilForm()
                planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
                return render(request, 'usuario/perfil.html',
                              {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada,
                               'perfil': perfil, 'perfiles': perfiles, 'escuelas': escuelas})
            else:
                fecha = perfil.get().fecha_nacimiento_perfil
                if fecha is not None:
                    factiva = "Si"
                else:
                    factiva = None
                perfil = get_object_or_404(Perfil, id=usuario_id)
                form = GuardarPerfilForm(instance=perfil)
                escuela = get_object_or_404(Escuela, pk=perfil.Escuela_perfil.id)
                planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
                return render(request, 'usuario/perfil_1.html',
                              {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada,
                               'perfil': perfil, 'perfiles': perfiles, 'escuela': escuela, 'escuelas': escuelas,
                               'factiva': factiva})
        else:
            message = "No son iguales las claves"
            if perfil.exists() == False:
                form = GuardarPerfilForm()
                planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
                return render(request, 'usuario/perfil.html',
                              {'message': message, 'formulario': form, 'usuario': usuario,
                               'planta_buscada': planta_buscada,
                               'perfil': perfil, 'perfiles': perfiles, 'escuelas': escuelas})
            else:
                fecha = perfil.get().fecha_nacimiento_perfil
                if fecha is not None:
                    factiva = "Si"
                else:
                    factiva = None
                perfil = get_object_or_404(Perfil, id=usuario_id)
                form = GuardarPerfilForm(instance=perfil)
                escuela = get_object_or_404(Escuela, pk=perfil.Escuela_perfil.id)
                planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
                return render(request, 'usuario/perfil_1.html',
                              {'message': message, 'formulario': form, 'usuario': usuario,
                               'planta_buscada': planta_buscada,
                               'perfil': perfil, 'perfiles': perfiles, 'escuela': escuela, 'escuelas': escuelas,
                               'factiva': factiva})
    if perfil.exists() == False:
        form = GuardarPerfilForm()
        planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
        return render(request, 'usuario/perfil.html',
                      {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada,
                       'perfil': perfil, 'perfiles': perfiles, 'escuelas': escuelas})
    else:
        fecha = perfil.get().fecha_nacimiento_perfil
        if fecha is not None:
            factiva = "Si"
        else:
            factiva = None
        perfil = get_object_or_404(Perfil, id=usuario_id)
        form = GuardarPerfilForm(instance=perfil)
        escuela = get_object_or_404(Escuela, pk=perfil.Escuela_perfil.id)
        planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
        return render(request, 'usuario/perfil_1.html',
                      {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada,
                       'perfil': perfil, 'perfiles': perfiles, 'escuela': escuela, 'escuelas': escuelas,
                       'factiva': factiva})


# Editar el tipo(rol) del Usuario
@login_required
@permission_required('gestionescuela.editar_escuela',reverse_lazy('homepage'))
def editar_rol_usuario(request, usuario_id):
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    form = Edit(request.POST)
    if form.is_valid():
        a = "no es valido"
    typeuser = form.cleaned_data.get('typeuser')
    usuario = User.objects.get(id=usuario_id)
    if typeuser is None:
        a = "no es valido"
    else:
        if usuario.groups.all().exists():
            # Action if existing
            grupo = Group.objects.get(user=usuario)
            usuario.groups.clear()
            typeuser = form.cleaned_data.get('typeuser')

            # grupo de usuarios
            g_estudiantes, gel = Group.objects.get_or_create(name='Estudiantes')
            g_profesores, gpl = Group.objects.get_or_create(name='Profesores')
            g_administradores, gad1 = Group.objects.get_or_create(name='Administradores')
            g_superusuarios, gsp1 = Group.objects.get_or_create(name='SuperUsuarios')

            # contenttype
            ce = ContentType.objects.get_for_model(Escuela)
            cp = ContentType.objects.get_for_model(Perfil)
            cpl = ContentType.objects.get_for_model(Planta)

            # Permisos de Escuela
            permiso1e, pe1 = Permission.objects.get_or_create(codename='listar_escuela',
                                                              name='Puede listar Escuelas',
                                                              content_type=ce)
            permiso2e, pe2 = Permission.objects.get_or_create(codename='agregar_escuela',
                                                              name='Puede agregar Escuelas',
                                                              content_type=ce)
            permiso3e, pe3 = Permission.objects.get_or_create(codename='editar_escuela',
                                                              name='Puede editar Escuelas',
                                                              content_type=ce)
            permiso4e, pe4 = Permission.objects.get_or_create(codename='eliminar_escuela',
                                                              name='Puede eliminar Escuela',
                                                              content_type=ce)
            # Permisos de Perfil
            permiso1p, pp1 = Permission.objects.get_or_create(codename='listar_perfil',
                                                              name='Puede listar Perfiles',
                                                              content_type=cp)
            permiso2p, pp2 = Permission.objects.get_or_create(codename='agregar_perfil',
                                                              name='Puede agregar Perfiles',
                                                              content_type=cp)
            permiso3p, pp3 = Permission.objects.get_or_create(codename='editar_perfil',
                                                              name='Puede editar Perfiles',
                                                              content_type=cp)
            permiso4p, pp4 = Permission.objects.get_or_create(codename='eliminar_perfil',
                                                              name='Puede eliminar Perfiles',
                                                              content_type=cp)
            # Permisos de Planta
            permiso1pp, ppl1 = Permission.objects.get_or_create(codename='listar_planta',
                                                                name='Puede listar Plantas',
                                                                content_type=cpl)
            permiso2pp, ppl2 = Permission.objects.get_or_create(codename='agregar_planta',
                                                                name='Puede agregar Plantas',
                                                                content_type=cpl)
            permiso3pp, ppl3 = Permission.objects.get_or_create(codename='editar_planta',
                                                                name='Puede editar Plantas',
                                                                content_type=cpl)
            permiso4pp, ppl4 = Permission.objects.get_or_create(codename='eliminar_planta',
                                                                name='Puede eliminar Plantas',
                                                                content_type=cpl)
            # Permisos para el Estudiante
            # Estudiante con permisos de Escuela
            g_estudiantes.permissions.add(permiso1e)
            # Estudiante con permisos de Perfil
            g_estudiantes.permissions.add(permiso1p)
            g_estudiantes.permissions.add(permiso2p)
            g_estudiantes.permissions.add(permiso3p)
            g_estudiantes.permissions.add(permiso4p)
            # Estudiante con permisos de Planta
            g_estudiantes.permissions.add(permiso1pp)

            # Permisos para el Profesor
            # Estudiante con permisos de Escuela
            g_profesores.permissions.add(permiso1e)
            # Estudiante con permisos de Perfil
            g_profesores.permissions.add(permiso1p)
            g_profesores.permissions.add(permiso2p)
            g_profesores.permissions.add(permiso3p)
            g_profesores.permissions.add(permiso4p)
            # Estudiante con permisos de Planta
            g_profesores.permissions.add(permiso1pp)

            # Permisos para el Administrador
            # Estudiante con permisos de Escuela
            g_administradores.permissions.add(permiso1e)
            g_administradores.permissions.add(permiso2e)
            g_administradores.permissions.add(permiso3e)
            # Estudiante con permisos de Perfil
            g_administradores.permissions.add(permiso1p)
            # Estudiante con permisos de Planta
            g_administradores.permissions.add(permiso1pp)
            g_administradores.permissions.add(permiso2pp)
            g_administradores.permissions.add(permiso3pp)

            # Permisos para el SuperUsuario
            # Estudiante con permisos de Escuela
            g_superusuarios.permissions.add(permiso1e)
            g_superusuarios.permissions.add(permiso2e)
            g_superusuarios.permissions.add(permiso3e)
            g_superusuarios.permissions.add(permiso4e)
            # Estudiante con permisos de Perfil
            g_superusuarios.permissions.add(permiso1p)
            # Estudiante con permisos de Planta
            g_superusuarios.permissions.add(permiso1pp)
            g_superusuarios.permissions.add(permiso2pp)
            g_superusuarios.permissions.add(permiso3pp)
            g_superusuarios.permissions.add(permiso4pp)

            if typeuser == 'Estudiantes':
                usuario.groups.add(g_estudiantes)
            elif typeuser == 'Profesores':
                usuario.groups.add(g_profesores)
            elif typeuser == 'Administradores':
                usuario.groups.add(g_administradores)
            elif typeuser == 'Superusuarios':
                usuario.groups.add(g_superusuarios)
            else:
                a = "No hay"

            return redirect('usuarios')

        else:
            # Action if not existing
            # grupo de usuarios
            g_estudiantes, gel = Group.objects.get_or_create(name='Estudiantes')
            g_profesores, gpl = Group.objects.get_or_create(name='Profesores')
            g_administradores, gad1 = Group.objects.get_or_create(name='Administradores')
            g_superusuarios, gsp1 = Group.objects.get_or_create(name='SuperUsuarios')

            # contenttype
            ce = ContentType.objects.get_for_model(Escuela)
            cp = ContentType.objects.get_for_model(Perfil)
            cpl = ContentType.objects.get_for_model(Planta)

            # Permisos de Escuela
            permiso1e, pe1 = Permission.objects.get_or_create(codename='listar_escuela',
                                                              name='Puede listar Escuelas',
                                                              content_type=ce)
            permiso2e, pe2 = Permission.objects.get_or_create(codename='agregar_escuela',
                                                              name='Puede agregar Escuelas',
                                                              content_type=ce)
            permiso3e, pe3 = Permission.objects.get_or_create(codename='editar_escuela',
                                                              name='Puede editar Escuelas',
                                                              content_type=ce)
            permiso4e, pe4 = Permission.objects.get_or_create(codename='eliminar_escuela',
                                                              name='Puede eliminar Escuela',
                                                              content_type=ce)
            # Permisos de Perfil
            permiso1p, pp1 = Permission.objects.get_or_create(codename='listar_perfil',
                                                              name='Puede listar Perfiles',
                                                              content_type=cp)
            permiso2p, pp2 = Permission.objects.get_or_create(codename='agregar_perfil',
                                                              name='Puede agregar Perfiles',
                                                              content_type=cp)
            permiso3p, pp3 = Permission.objects.get_or_create(codename='editar_perfil',
                                                              name='Puede editar Perfiles',
                                                              content_type=cp)
            permiso4p, pp4 = Permission.objects.get_or_create(codename='eliminar_perfil',
                                                              name='Puede eliminar Perfiles',
                                                              content_type=cp)
            # Permisos de Planta
            permiso1pp, ppl1 = Permission.objects.get_or_create(codename='listar_planta',
                                                                name='Puede listar Plantas',
                                                                content_type=cpl)
            permiso2pp, ppl2 = Permission.objects.get_or_create(codename='agregar_planta',
                                                                name='Puede agregar Plantas',
                                                                content_type=cpl)
            permiso3pp, ppl3 = Permission.objects.get_or_create(codename='editar_planta',
                                                                name='Puede editar Plantas',
                                                                content_type=cpl)
            permiso4pp, ppl4 = Permission.objects.get_or_create(codename='eliminar_planta',
                                                                name='Puede eliminar Plantas',
                                                                content_type=cpl)
            # Permisos para el Estudiante
            # Estudiante con permisos de Escuela
            g_estudiantes.permissions.add(permiso1e)
            # Estudiante con permisos de Perfil
            g_estudiantes.permissions.add(permiso1p)
            g_estudiantes.permissions.add(permiso2p)
            g_estudiantes.permissions.add(permiso3p)
            g_estudiantes.permissions.add(permiso4p)
            # Estudiante con permisos de Planta
            g_estudiantes.permissions.add(permiso1pp)

            # Permisos para el Profesor
            # Estudiante con permisos de Escuela
            g_profesores.permissions.add(permiso1e)
            # Estudiante con permisos de Perfil
            g_profesores.permissions.add(permiso1p)
            g_profesores.permissions.add(permiso2p)
            g_profesores.permissions.add(permiso3p)
            g_profesores.permissions.add(permiso4p)
            # Estudiante con permisos de Planta
            g_profesores.permissions.add(permiso1pp)

            # Permisos para el Administrador
            # Estudiante con permisos de Escuela
            g_administradores.permissions.add(permiso1e)
            g_administradores.permissions.add(permiso2e)
            g_administradores.permissions.add(permiso3e)
            # Estudiante con permisos de Perfil
            g_administradores.permissions.add(permiso1p)
            # Estudiante con permisos de Planta
            g_administradores.permissions.add(permiso1pp)
            g_administradores.permissions.add(permiso2pp)
            g_administradores.permissions.add(permiso3pp)

            # Permisos para el SuperUsuario
            # Estudiante con permisos de Escuela
            g_superusuarios.permissions.add(permiso1e)
            g_superusuarios.permissions.add(permiso2e)
            g_superusuarios.permissions.add(permiso3e)
            g_superusuarios.permissions.add(permiso4e)
            # Estudiante con permisos de Perfil
            g_superusuarios.permissions.add(permiso1p)
            # Estudiante con permisos de Planta
            g_superusuarios.permissions.add(permiso1pp)
            g_superusuarios.permissions.add(permiso2pp)
            g_superusuarios.permissions.add(permiso3pp)
            g_superusuarios.permissions.add(permiso4pp)

            if typeuser == 'Estudiantes':
                usuario.groups.add(g_estudiantes)
            elif typeuser == 'Profesores':
                usuario.groups.add(g_profesores)
            elif typeuser == 'Administradores':
                usuario.groups.add(g_administradores)
            elif typeuser == 'Superusuarios':
                usuario.groups.add(g_superusuarios)
            else:
                a = "No hay"

            return redirect('usuarios')

    return render(request, 'usuario/editar_tipo.html', {'usuario': usuario, 'perfiles': perfiles})


# Editar perfil del Usuario
@login_required
def editar_cuenta(request):
    escuelas = Escuela.objects.all()
    usuario = User.objects.get(id=request.user.id)
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    id = usuario.id
    perfil = Perfil.objects.filter(pk=id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        remove('media/datos/' + usuario.username + '.txt')
        if form.is_valid():
            form.save()
            formp = GuardarPerfilForm()
            usuario = User.objects.get(id=id)
            f = open('media/datos/' + usuario.username + '.txt', 'w')
            f.close()
            print(usuario)
            message = "Editado con éxito"
            if perfil.exists() == False:
                form = GuardarPerfilForm()
                planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
                return render(request, 'usuario/perfil.html',
                              {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada,
                               'perfil': perfil, 'perfiles': perfiles, 'escuelas': escuelas, 'message':message})
            else:
                fecha = perfil.get().fecha_nacimiento_perfil
                if fecha is not None:
                    factiva = "Si"
                else:
                    factiva = None
                perfil = get_object_or_404(Perfil, id=id)
                form = GuardarPerfilForm(instance=perfil)
                escuela = get_object_or_404(Escuela, pk=perfil.Escuela_perfil.id)
                planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
                return render(request, 'usuario/perfil_1.html',
                              {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada,
                               'perfil': perfil, 'perfiles': perfiles, 'escuela': escuela, 'escuelas': escuelas,
                               'factiva': factiva, 'message':message})
    else:
        form = EditProfileForm(instance=request.user)
        formp = GuardarPerfilForm()
        return render(request, 'usuario/perfil.html',
                      {'formulario': formp, 'formular': form, 'usuario': usuario, 'perfil': perfil,
                       'perfiles': perfiles,
                       'escuelas': escuelas})


from os import remove
# Eliminar Usuario
@login_required
@permission_required('gestionescuela.eliminar_escuela',reverse_lazy('Escuela'))
def eliminar(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    remove('media/datos/' + usuario.username+'.txt')
    usuario.delete()
    return redirect('usuarios')