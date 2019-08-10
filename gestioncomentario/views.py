from django.contrib.auth.models import User
from gestionbusqueda.models import Busqueda
from gestioncomentario.models import Comentario
from gestioncomentario.form import GuardarComentarioForm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from gestionescuela.models import Escuela
from gestionperfil.form import GuardarPerfilForm
from gestionperfil.models import Perfil
from gestionplantas.models import Planta
from . serializers import ComentarioSerializer

class postList(APIView):

   def get(self, request):
      allpost = Comentario.objects.all()
      serializer = ComentarioSerializer(allpost, many=True)
      return Response(serializer.data)

   def post(self):
      pass

class ComentarioList(generics.ListCreateAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

class ComentarioDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer


#Guardar Comentario
@login_required
def agregar_comentario(request, planta_id):
    message=None
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
    planta = get_object_or_404(Planta, pk=planta_id)
    perfilesc = Perfil.objects.all()
    comentarios = Comentario.objects.filter(Planta_id=planta_id)
    if request.method == 'POST':
        form = GuardarComentarioForm(request.POST)
        usuario = User.objects.get(id=request.user.id)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.Usuario_id=usuario
            comentario.Planta_id=planta
            comentario.save()
            form = GuardarComentarioForm()
            return render(request, 'planta/perfil_planta.html', {'form':form, 'planta': planta, 'perfiles':perfiles, 'comentarios':comentarios, 'perfilesc': perfilesc})
        else:
            form = GuardarComentarioForm(request.POST)
            message = "Datos Erroneos para pubicar el Comentario."
            return render(request, 'planta/perfil_planta.html', {'form':form, 'planta': planta, 'perfiles':perfiles, 'comentarios':comentarios, 'message':message, 'perfilesc': perfilesc})
    else:
        form = GuardarComentarioForm()
    return render(request, 'planta/perfil_planta.html', {'form':form, 'planta': planta, 'perfiles':perfiles, 'comentarios':comentarios, 'message':message, 'perfilesc': perfilesc})


#Eliminar Comentario
@login_required
def eliminar_comentario(request, comentario_id):
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
    comentario = get_object_or_404(Comentario, id=comentario_id)
    comentario.delete()
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
                      {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada,
                       'perfiles': perfiles, 'escuela': escuela, 'escuelas': escuelas, 'factiva': factiva,
                       'message': message, 'comentarios':comentarios, 'perfil': perfil})
    else:
        form = GuardarPerfilForm()
        planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
        comentarios = Comentario.objects.filter(Usuario_id=id).all()
        if planta_buscada == None:
            planta_buscada = []
        else:
            planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
        if comentarios == None:
            comentarios = []
        else:
            comentarios = Comentario.objects.filter(Usuario_id=id).all()
        return render(request, 'usuario/perfil.html',
                      {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada, 'perfiles': perfiles,
                       'escuelas': escuelas, 'mesaage': message, 'comentarios':comentarios})





