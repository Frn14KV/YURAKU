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
from django.urls import reverse_lazy
from gestionbusqueda.models import Busqueda
from gestioncomentario.models import Comentario
from gestionperfil.form import GuardarPerfilForm
from gestionperfil.models import Perfil
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.views import APIView
from rest_framework.response import Response
from gestionresultado.models import Resultado
from . serializers import PerfilSerializer
from rest_framework import generics

"""
    Esta seccion esta creado para que en trabajos futuro se pueda utilizar web service de Comentario.
"""


######
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


######

"""
    Funcion perfil_detallado
    Funcion creada para devolver el perfil (si tiene creado) de un usuario y retorna una pagina web con los resultados (si tiene la fecha de nacimiento se concatena si no se lo manda sin ese campo).
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        user_id: representa el id del usuario para encontrar el Perfil.
"""
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
    usuario = get_object_or_404(User, id=user_id)
    id = usuario.id
    perfil = Perfil.objects.filter(Usuario_id=id)
    if perfil.exists()==False:
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
        return render(request, 'usuario/perfil.html', {'formulario':form, 'comentarios':comentarios, 'reconocimientos':reconocimientos,
                                                       'usuario': usuario, 'planta_buscada': planta_buscada, 'perfil': perfil,
                                                       'perfiles': perfiles})
    else:
        fecha = perfil.get().fecha_nacimiento_perfil
        if fecha is not None:
            factiva = "Si"
        else:
            factiva = None
        perfil =get_object_or_404(Perfil,Usuario_id=user_id)
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
        return render(request, 'usuario/perfil_1.html', {'formulario':form, 'comentarios':comentarios, 'reconocimientos':reconocimientos,
                                                         'usuario': usuario, 'planta_buscada': planta_buscada, 'perfil': perfil,
                                                         'perfiles': perfiles, 'factiva':factiva})

"""
    Funcion guardar_peril
    Funcion creada para guardar los datos del perfil del usuario y retorna una pagina web con los resultados (si se creo con exito o no el perfil).
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
#Guardar Perfil
@login_required
def guardar_perfil(request):
    global partes
    message = None
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
                          {'formulario': form, 'comentarios': comentarios, 'usuario': usuario, 'reconocimientos':reconocimientos,
                           'planta_buscada': planta_buscada, 'perfil': perfil, 'perfiles': perfiles,
                            'factiva': factiva})

        else:
            message = "uno de los campos no fue ingresado al registrar el Perfil."
            return render(request, 'usuario/perfil.html',
                          {'message': message, 'formulario': form})
    else:
        form = GuardarPerfilForm()
    return render(request, 'usuario/perfil.html',{'formulario': form, 'message':message})

"""
    Funcion edtiar_peril
    Funcion creada para editar los datos del perfil del usuario y retorna una pagina web con los resultados (si se edito con exito o no el perfil).
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        user_id: representa el id del usuario para encontrar el Perfil.
"""
#Editar Perfil
@login_required
def editar_perfil(request, user_id):
    global partes
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
    usuario = get_object_or_404(User, id=user_id)
    id = usuario.id
    perfil = get_object_or_404(Perfil, Usuario_id=id)
    if request.method == 'POST':
        form = GuardarPerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            fecha = perfil.fecha_nacimiento_perfil
            if fecha is not None:
                factiva = "Si"
            else:
                factiva = None
            message = "Editado con éxito"
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
                      {'message': message, 'formulario': form, 'usuario': usuario, 'perfil': perfil, 'comentarios':comentarios, 'reconocimientos':reconocimientos,
                       'factiva': factiva, 'planta_buscada':planta_buscada, 'perfiles': perfiles})
        else:
            message = "uno de los campos no fue ingresado al editar el Perfil"
            fecha = perfil.fecha_nacimiento_perfil
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
                          {'message': message, 'formulario':form, 'usuario': usuario, 'perfil': perfil, 'comentarios':comentarios, 'reconocimientos':reconocimientos,
                           'factiva':factiva, 'planta_buscada':planta_buscada, 'perfiles': perfiles,})
    else:
        planta_buscada = Busqueda.objects.filter(Usuario_id=perfil.id).all()
        comentarios = Comentario.objects.filter(Usuario_id=perfil.id).all()
        reconocimientos = Resultado.objects.filter(Usuario_id=perfil.id).all()
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
        form =GuardarPerfilForm(instance=perfil)
        fecha = perfil.fecha_nacimiento_perfil
        if fecha is not None:
            factiva = "Si"
        else:
            factiva = None
        message = None
    return render(request, 'usuario/perfil_1.html',
                              {'message':message, 'formulario':form, 'usuario': usuario, 'perfil': perfil,'comentarios':comentarios, 'reconocimientos':reconocimientos,
                               'factiva':factiva, 'planta_buscada':planta_buscada, 'perfiles': perfiles,})


"""
    Funcion eliminar_peril
    Funcion creada para eliminar los datos del perfil del usuario y retorna a la pagina del Perfil.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        perfil_id: representa el id del perfil para eliminar el Perfil del usuario.
"""
#Eliminar Perfil
@login_required
@permission_required('gestionperfil.eliminar_perfil',reverse_lazy('Perfil'))
def eliminar_perfil(request, perfil_id):
    perfil = get_object_or_404(Perfil, id=perfil_id)
    perfil.delete()
    return redirect('Perfil')


"""
    Funcion eliminar_busqueda
    Funcion creada para eliminar la busqueda del usuario y retorna una pagina web con los resultados (si se elimino con exito o no la busqueda del usuario).
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        busqueda_id: representa el id de la busqueda para eliminar.
"""
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
    usuario = get_object_or_404(User, id=request.user.id)
    id = usuario.id
    busqueda = get_object_or_404(Busqueda, id=busqueda_id)
    busqueda.delete()
    message = "Eliminado con éxito"
    if perfiles != None and len(perfiles) !=0:
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
                      {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada, 'perfil': perfil,
                       'perfiles': perfiles, 'factiva': factiva, 'reconocimientos':reconocimientos,
                       'message':message, 'comentarios':comentarios})
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
                      {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada,'perfiles': perfiles, 'reconocimientos':reconocimientos,
                        'message':message, 'comentarios':comentarios})

"""
    Funcion eliminar_reconocimiento
    Funcion creada para eliminar el reconocimiento del usuario y retorna una pagina web con los resultados (si se elimino con exito o no el reconocimiento del usuario).
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        reconocimiento_id: representa el id del reconocimiento para eliminar.
"""
#Eliminar Reconocimiento
@login_required
def eliminar_reconocimiento(request, reconocimiento_id):
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
    reconos = get_object_or_404(Resultado, id=reconocimiento_id)
    reconos.delete()
    message = "Eliminado con éxito"
    if perfiles != None and len(perfiles) !=0:
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
                      {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada, 'reconocimientos':reconocimientos,
                       'perfil': perfil, 'perfiles': perfiles, 'factiva': factiva,
                       'message':message, 'comentarios':comentarios})
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
                      {'formulario': form, 'usuario': usuario, 'planta_buscada': planta_buscada, 'reconocimientos':reconocimientos,
                       'perfiles': perfiles, 'message':message, 'comentarios':comentarios})