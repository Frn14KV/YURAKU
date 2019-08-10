from django.urls import reverse_lazy

from gestionbusqueda.models import Busqueda
from gestioncomentario.models import Comentario
from gestionperfil.form import GuardarPerfilForm
from gestionperfil.models import Perfil
from django.contrib.auth.models import User
from gestionescuela.models import Escuela

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, permission_required


from rest_framework.views import APIView
from rest_framework.response import Response

from . serializers import PerfilSerializer
from rest_framework import generics

##Web Service
class postList(APIView):

   def get(self, request):
      allpost = Perfil.objects.all()
      serializer = PerfilSerializer(allpost, many=True)
      return Response(serializer.data)

   def post(self):
      pass

class PerfilList(generics.ListCreateAPIView):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer

class PerfilDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer


#Datos Del Perfil
def perfil_detallado(request, user_id):
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
    usuario = get_object_or_404(User, id=user_id)
    id = usuario.id
    perfil = Perfil.objects.filter(Usuario_id=id)
    if perfil.exists()==False:
        form = GuardarPerfilForm()
        planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
        comentarios = Comentario.objects.filter(Usuario_id=id).all()
        return render(request, 'usuario/perfil.html', {'formulario':form, 'comentarios':comentarios, 'usuario': usuario, 'planta_buscada': planta_buscada, 'perfil': perfil,'perfiles': perfiles, 'escuelas':escuelas})
    else:
        fecha = perfil.get().fecha_nacimiento_perfil
        if fecha is not None:
            factiva = "Si"
        else:
            factiva = None
        perfil =get_object_or_404(Perfil,Usuario_id=user_id)
        form = GuardarPerfilForm(instance=perfil)
        escuela = get_object_or_404(Escuela, pk=perfil.Escuela_perfil.id)
        planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
        comentarios = Comentario.objects.filter(Usuario_id=id).all()
        return render(request, 'usuario/perfil_1.html', {'formulario':form, 'comentarios':comentarios, 'usuario': usuario, 'planta_buscada': planta_buscada, 'perfil': perfil, 'perfiles': perfiles, 'escuela':escuela, 'escuelas':escuelas, 'factiva':factiva})


#Guardar Perfil
@login_required
def guardar_perfil(request):
    global partes
    message = None
    escuelas = Escuela.objects.all()
    if request.method == 'POST':
        form = GuardarPerfilForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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

            usuario = get_object_or_404(User, id=request.user.id)
            id = usuario.id
            perfil = get_object_or_404(Perfil, Usuario_id=id)
            fecha = perfil.fecha_nacimiento_perfil
            if fecha is not None:
                factiva = "Si"
            else:
                factiva = None
            perfil = get_object_or_404(Perfil, Usuario_id=request.user.id)
            form = GuardarPerfilForm(instance=perfil)
            escuela = get_object_or_404(Escuela, pk=perfil.Escuela_perfil.id)
            planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
            comentarios = Comentario.objects.filter(Usuario_id=id).all()
            return render(request, 'usuario/perfil_1.html',
                          {'formulario': form, 'comentarios': comentarios, 'usuario': usuario,
                           'planta_buscada': planta_buscada, 'perfil': perfil, 'perfiles': perfiles, 'escuela': escuela,
                           'escuelas': escuelas, 'factiva': factiva})

        else:
            message = "uno de los campos no fue ingresado al registrar el Perfil."
            return render(request, 'usuario/perfil.html',
                          {'message': message, 'formulario': form, 'escuelas':escuelas,})
    else:
        form = GuardarPerfilForm()
    return render(request, 'usuario/perfil.html',{'formulario': form, 'message':message, 'escuelas':escuelas,})


#Editar Perfil
@login_required
def editar_perfil(request, user_id):
    global partes
    message = None
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
    usuario = get_object_or_404(User, id=user_id)
    id = usuario.id
    perfil = get_object_or_404(Perfil, Usuario_id=id)
    if request.method == 'POST':
        form = GuardarPerfilForm(request.POST, request.FILES, instance=perfil)
        planta_buscada = Busqueda.objects.filter(Usuario_id=perfil.id).all()
        escuela = get_object_or_404(Escuela, pk=perfil.Escuela_perfil.id)
        if form.is_valid():
            form.save()
            fecha = perfil.fecha_nacimiento_perfil
            if fecha is not None:
                factiva = "Si"
            else:
                factiva = None
            planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
            comentarios = Comentario.objects.filter(Usuario_id=id).all()
            message = "Editado con éxito"
            return render(request, 'usuario/perfil_1.html',
                      {'message': message, 'formulario': form, 'usuario': usuario, 'perfil': perfil,
                       'escuelas': escuelas, 'factiva': factiva, 'planta_buscada':planta_buscada, 'escuela':escuela, 'perfiles': perfiles, 'comentarios':comentarios})
        else:
            message = "uno de los campos no fue ingresado al editar el Perfil"
            fecha = perfil.fecha_nacimiento_perfil
            if fecha is not None:
                factiva = "Si"
            else:
                factiva = None
            return render(request, 'usuario/perfil_1.html',
                          {'message': message, 'formulario':form, 'usuario': usuario, 'perfil': perfil,
                           'escuelas':escuelas, 'factiva':factiva, 'planta_buscada':planta_buscada, 'escuela':escuela, 'perfiles': perfiles,})
    else:
        planta_buscada = Busqueda.objects.filter(Usuario_id=perfil.id).all()
        escuela = get_object_or_404(Escuela, pk=perfil.Escuela_perfil.id)
        form =GuardarPerfilForm(instance=perfil)
        fecha = perfil.fecha_nacimiento_perfil
        if fecha is not None:
            factiva = "Si"
        else:
            factiva = None
        message = None
    return render(request, 'usuario/perfil_1.html',
                              {'message':message, 'formulario':form, 'usuario': usuario, 'perfil': perfil,
                               'escuelas':escuelas, 'factiva':factiva, 'planta_buscada':planta_buscada, 'escuela':escuela, 'perfiles': perfiles,})


#Eliminar Perfil
@login_required
@permission_required('gestionperfil.eliminar_perfil',reverse_lazy('Perfil'))
def eliminar_perfil(request, perfil_id):
    perfil = get_object_or_404(Perfil, id=perfil_id)
    perfil.delete()
    return redirect('Perfil')


#Eliminar Busqueda
@login_required
def eliminar_busqueda(request, busqueda_id):
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
    usuario = get_object_or_404(User, id=request.user.id)
    id = usuario.id
    busqueda = get_object_or_404(Busqueda, id=busqueda_id)
    busqueda.delete()
    message = "Eliminado con éxito"
    if perfiles != None:
        fecha = perfiles.get().fecha_nacimiento_perfil
        if fecha is not None:
            factiva = "Si"
        else:
            factiva = None
        perfil = Perfil.objects.get(Usuario_id=id)
        form = GuardarPerfilForm(instance=perfil)
        escuela = get_object_or_404(Escuela, pk=perfil.Escuela_perfil.id)
        planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
        comentarios = Comentario.objects.filter(Usuario_id=id).all()
        return render(request, 'usuario/perfil_1.html',
                      {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada, 'perfil': perfil,
                       'perfiles': perfiles, 'escuela': escuela, 'escuelas': escuelas, 'factiva': factiva,
                       'message':message, 'comentarios':comentarios})
    else:
        form = GuardarPerfilForm()
        planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
        comentarios = Comentario.objects.filter(Usuario_id=id).all()
        if planta_buscada == None:
            planta_buscada = []
        else:
            planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
        return render(request, 'usuario/perfil.html',
                      {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada,'perfiles': perfiles,
                       'escuelas': escuelas, 'mesaage':message, 'comentarios':comentarios})

