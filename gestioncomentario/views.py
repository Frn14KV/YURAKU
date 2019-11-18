"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    User: importa el modelo llamado User que representa los usuarios del Sistema.
    Busqueda: importa el modelo llamado Busqueda.
    Comentario: importa el modelo llamado Comentario.
    Resultado: importa el modelo llamado Resultado.
    GuardarComentarioForm: importa el formulario llamado GuardarComentarioForm.
    get_object_or_404: libreria propia de django para realizar una busqueda de un objeto de un modelo.
    render: libreria propia de django para retornar una pagina web con sus resultados.
    login_required: libreria propia de django para controlar que este iniciado sesion para acceder a una funcion.
    APIView: libreria propia de django para crear web service.
    Response: libreria propia de django para crear la respuesta de los web services.
    generics: libreria propia de django para crear clases para manejar los web services.
    GuardarPerfilForm: importa el formulario llamado GuardarComentarioForm.
    Perfil: importa el modelo llamado Perfil.
    Planta: importa el modelo llamado Planta.
    ComentarioSerializer: importa el serializablle llamado ComentarioSerializer.
"""
from django.contrib.auth.models import User
from gestionbusqueda.models import Busqueda
from gestioncomentario.models import Comentario
from gestionresultado.models import Resultado
from gestioncomentario.form import GuardarComentarioForm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from gestionperfil.form import GuardarPerfilForm
from gestionperfil.models import Perfil
from gestionplantas.models import Planta
from .serializers import ComentarioSerializer

"""
    Esta seccion esta creado para que en trabajos futuro se pueda utilizar web service de Comentario.
"""


######
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


######

"""
    Funcion agregar_comentario
    Funcion creada para guardar los comentario que se hagan a una Planta y retorna una pagina web con los resultados (si se realizo o no el comentario).
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        planta_id: representa el id de la planta a la cual se va a Comentar.
"""


# Guardar Comentario
@login_required
def agregar_comentario(request, planta_id):
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
    planta = get_object_or_404(Planta, pk=planta_id)
    perfilesc = Perfil.objects.all()
    comentarios = Comentario.objects.filter(Planta_id=planta_id)
    if request.method == 'POST':
        form = GuardarComentarioForm(request.POST)
        usuario = User.objects.get(id=request.user.id)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.Usuario_id = usuario
            comentario.Planta_id = planta
            comentario.save()
            form = GuardarComentarioForm()
            return render(request, 'planta/perfil_planta.html',
                          {'form': form, 'planta': planta, 'perfiles': perfiles, 'comentarios': comentarios,
                           'perfilesc': perfilesc})
        else:
            form = GuardarComentarioForm(request.POST)
            message = "Datos Erroneos para pubicar el Comentario."
            return render(request, 'planta/perfil_planta.html',
                          {'form': form, 'planta': planta, 'perfiles': perfiles, 'comentarios': comentarios,
                           'message': message, 'perfilesc': perfilesc})
    else:
        form = GuardarComentarioForm()
    return render(request, 'planta/perfil_planta.html',
                  {'form': form, 'planta': planta, 'perfiles': perfiles, 'comentarios': comentarios, 'message': message,
                   'perfilesc': perfilesc})


"""
    Funcion eliminar_comentario
    Funcion creada para eliminar los comentario que se hagan a una Planta y retorna una pagina web con los resultados (si se elimino o no el Comentario).
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        comentario_id: representa el id del comentario a la cual se va eliminar.
"""


# Eliminar Comentario
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
    usuario = get_object_or_404(User, id=request.user.id)
    id = usuario.id
    comentario = get_object_or_404(Comentario, id=comentario_id)
    comentario.delete()
    message = "Eliminado con éxito"
    if perfiles != None and len(perfiles) != 0:
        fecha = perfiles.get().fecha_nacimiento_perfil
        if fecha is not None:
            factiva = "Si"
        else:
            factiva = None
        perfil = Perfil.objects.get(Usuario_id=id)
        form = GuardarPerfilForm(instance=perfil)
        planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
        comentarios = Comentario.objects.filter(Usuario_id=id).all()
        reconocimientos = Resultado.objects.filter(Usuario_id=id).all()
        if planta_buscada == None:
            planta_buscada = []
        else:
            planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
        if comentarios == None:
            comentarios = []
        else:
            comentarios = Comentario.objects.filter(Usuario_id=id).all()
        if reconocimientos == None:
            reconocimientos = []
        else:
            reconocimientos = Resultado.objects.filter(Usuario_id=id).all()
        return render(request, 'usuario/perfil_1.html',
                      {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada,
                       'perfiles': perfiles, 'factiva': factiva, 'reconocimientos': reconocimientos,
                       'message': message, 'comentarios': comentarios, 'perfil': perfil})
    else:
        form = GuardarPerfilForm()
        planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
        comentarios = Comentario.objects.filter(Usuario_id=id).all()
        reconocimientos = Resultado.objects.filter(Usuario_id=id).all()
        if planta_buscada == None:
            planta_buscada = []
        else:
            planta_buscada = Busqueda.objects.filter(Usuario_id=id).all()
        if comentarios == None:
            comentarios = []
        else:
            comentarios = Comentario.objects.filter(Usuario_id=id).all()
        if reconocimientos == None:
            reconocimientos = []
        else:
            reconocimientos = Resultado.objects.filter(Usuario_id=id).all()
        return render(request, 'usuario/perfil.html',
                      {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada, 'perfiles': perfiles,
                       'message': message, 'comentarios': comentarios, 'reconocimientos': reconocimientos})
