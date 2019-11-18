"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    subprocess: libreria propia de django para permite generar nuevos procesos, conectarse a sus tuberías de entrada / salida / error y obtener sus códigos de retorno
    threading: libreria propia de django para crear hilos.
    time: libreria propia de django para asiganr un tiempo de retardo en la ejecucion de algun proceso. 
    login_required: libreria propia de django para controlar que este iniciado sesion para acceder a una funcion.
    permission_required: libreria propia de django para verificar si tiene permisos para realizar ciertas funciones.
    User: importa el modelo llamado User que representa los usuarios del Sistema.
    Q: encapsula una expresión SQL en un objeto Python que se puede usar en operaciones relacionadas con la base de datos.
    HttpResponse: libreria propia de django para generar respuestas web mas simples.
    get_object_or_404: libreria propia de django para realizar una busqueda de un objeto de un modelo.
    render: libreria propia de django para retornar una pagina web con sus resultados.
    redirect: libreria propia de django para acceder a una pagina de manera mas rapida sin paso de datos.
    reverse_lazy: libreria propia de django para retornar a una pagina espeficica si no tiene permisos.
    generics: libreria propia de django para crear clases para manejar los web services.
    Response: libreria propia de django es un tipo de TemplateResponse que toma contenido sin procesar y utiliza la negociación 
    de contenido para determinar el tipo de contenido correcto para regresar al cliente.
    json: libreria propia de django para canvertir que se estaran en el web service.
    APIView: libreria propia de django para crear web service.
    Busqueda: importa el modelo llamado Busqueda.
    GuardarComentarioForm: importa el formulario llamado GuardarComentarioForm.
    Comentario: importa el modelo llamado Comentario.
    Juego: importa el modelo llamado Juego.
    Perfil: importa el modelo llamado Perfil.
    GuardarPlantaForm: importa el formulario llamado GuardarPlantaForm.
    Planta: importa el modelo llamado Planta.
    ReconocimientoForm: importa el formulario llamado ReconocimientoForm.
    Reconocimiento: importa el modelo llamado Reconocimiento.
    Resultado: importa el modelo llamado Resultado.
    PlantaSerializer: importa el serializablle llamado PlantaSerializer.
    ratelimit: libreria propia de django para retardar cierto tiempo las peticiones Http de una IP.
"""
import subprocess
import threading
import time
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from gestionbusqueda.models import Busqueda
from gestioncomentario.form import GuardarComentarioForm
from gestioncomentario.models import Comentario
from gestionjuego.models import Juego
from gestionperfil.models import Perfil
from gestionplantas.form import GuardarPlantaForm
from gestionplantas.models import Planta
from gestionreconocimiento.form import ReconocimientoForm
from gestionreconocimiento.models import Reconocimiento
from gestionresultado.models import Resultado
from .serializers import PlantaSerializer
from ratelimit.decorators import ratelimit

"""
    Clase postList
    Clase creada para generar el web service de plantas.
    Funcion get(selft)
        Funcion creada para retornar el listado de plantas.
            Parametro
                self:objeto instanciado de la clase Planta.
                request: para manejar las peticiones HTTP, FTP.
    
    Funcion post(selft)
        Funcion creada para tener acceso a la infomacion de las plantas.
        Parametro
                self:objeto instanciado de la clase Planta.
"""
##Web Service
class postList(APIView):

    def get(self, request):
        allpost = Planta.objects.all()
        serializer = PlantaSerializer(allpost, many=True)
        return Response(serializer.data)

    def post(self):
        pass

"""
    Clase PlantaList
    Clase creada para generar la lista de plantas.
        Parametro
            generics.ListCreateAPIView:objeto instanciado para la lista de plantas.
"""
class PlantaList(generics.ListCreateAPIView):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer

"""
    Clase PlantaDetalle
    Clase creada para comprimir todos los datos de cada planta.
        Parametro
            generics.RetrieveUpdateDestroyAPIView:objeto instanciado de los detalles de cada planta.
"""
class PlantaDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer

"""
    Funcion buscar_planta
    Funcion creada para servir de web service de busqueda de plantas desde la apliacion movil.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
# Web service de Busqueda
def buscar_plantas_web(request):
    query = request.GET.get('q', '')
    data = []
    if len(query) > 0:
        if query:
            qset = (
                    Q(id__icontains=query) |
                    Q(nombre_planta__icontains=query) |
                    Q(uso__icontains=query) |
                    Q(nombre_comun__icontains=query)
            )
            plantas_encontradas = Planta.objects.filter(qset).values()
            for i in range(0, len(plantas_encontradas)):
                data.append(plantas_encontradas[i])

            return HttpResponse(json.dumps(data, indent=4, sort_keys=True), content_type="application/json")
        else:
            return HttpResponse(json.dumps(data, indent=3, sort_keys=True), content_type="application/json")
    else:
        plantas_encontradas = Planta.objects.all().values()[0:8]
        for i in range(0, len(plantas_encontradas)):
            data.append(plantas_encontradas[i])
        return HttpResponse(json.dumps(data, indent=3, sort_keys=True), content_type="application/json")

"""
    Funcion index
    Funcion creada para listar los datos de todas las plantas.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
# listado de plantas.
def index(request):
    plantas = Planta.objects.all().order_by('id')
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
    return render(request, 'planta/lista_planta.html', {'plantas': plantas, 'perfiles': perfiles})

"""
    Funcion planta_planta 
    Funcion creada para ver los datos de una planta del sistema, eso lo realiza los usuarios que esten iniciado sesion y que tengan lo permisos.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        planta_id: representa el id de la plantas del que se quiere ver la informacion.
"""
# perfil Planta
def planta_detalle(request, planta_id):
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
    perfilesc = Perfil.objects.all()
    planta = get_object_or_404(Planta, pk=planta_id)
    comentarios = Comentario.objects.filter(Planta_id=planta_id)
    form = GuardarComentarioForm()
    return render(request, 'planta/perfil_planta.html',
                  {'form': form, 'planta': planta, 'perfilesc': perfilesc, 'perfiles': perfiles,
                   'comentarios': comentarios})

"""
    Funcion guardar_planta
    Funcion creada para registrar los datos de una planta del sistema, eso lo realiza los usuarios que esten iniciado sesion y que tengan lo permisos.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
# guardar Planta
@login_required
@permission_required('gestionplantas.agregar_planta', reverse_lazy('Planta'))
def guardar_planta(request):
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
    if request.method == 'POST':
        form = GuardarPlantaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Planta')
    else:
        form = GuardarPlantaForm()
    return render(request, 'planta/agregar_planta.html',
                  {'form': form, 'perfiles': perfiles})

"""
    Funcion editar_planta
    Funcion creada para editar la planta del sistema, eso lo realiza los usuarios que esten iniciado sesion y que tengan lo permisos.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        planta_id: representa el id de la plantas del que se quiere editar.
"""
# editar Planta
@login_required
@permission_required('gestionplantas.editar_planta', reverse_lazy('Planta'))
def editar_planta(request, planta_id):
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
    if request.method == 'POST':
        form = GuardarPlantaForm(request.POST, request.FILES, instance=planta)
        if form.is_valid():
            form.save()
            return redirect('Planta')
    else:
        form = GuardarPlantaForm(instance=planta)
    return render(request, 'planta/editar_planta.html', {'form': form, 'planta': planta, 'perfiles': perfiles})

"""
    Funcion eliminar_planta
    Funcion creada para eliminar la planta del sistema, eso lo realiza los usuarios que esten iniciado sesion y que tengan lo permisos.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        planta_id: representa el id de la plantas del que se quiere eliminar.
"""
# eliminar Planta
@login_required
@permission_required('gestionplantas.eliminar_planta', reverse_lazy('Planta'))
def eliminar_planta(request, planta_id):
    planta = get_object_or_404(Planta, id=planta_id)
    planta.delete()
    return redirect('Planta')

"""
    Funcion buscar_plantas
    Funcion creada para buscar plantas y retorna el resultado en una pagina, simpre y cuando este iniciado sesion.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
# busqueda de Plantas
@login_required
def buscar_plantas(request):
    form = Busqueda()
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
    query = request.GET.get('q', '')
    if len(query) > 0:
        if query:
            qset = (
                    Q(id__icontains=query) |
                    Q(nombre_planta__icontains=query) |
                    Q(uso__icontains=query) |
                    Q(nombre_comun__icontains=query)
            )
            plantas_encontradas = Planta.objects.filter(qset).all()
            userid = request.user.id
            if userid != None:
                usuario = get_object_or_404(User, id=userid)
                form.nombre_busqueda = query
                form.Usuario_id = usuario
                form.save()
                for i in (plantas_encontradas):
                    planta = get_object_or_404(Planta, pk=i.id)
                    form.Planta.add(planta)
            if (len(plantas_encontradas) > 0):
                message = "La búsqueda tuvo los siguientes resultados:"
                return render(request, 'planta/busqueda_planta.html',
                              {'planta_encontradas': plantas_encontradas, 'perfiles': perfiles, 'message': message})
            else:
                plantas_encontradas = []
                message = "No hay resultados"
                return render(request, 'planta/busqueda_planta.html',
                              {'planta_encontradas': plantas_encontradas, 'perfiles': perfiles, 'message': message})
        else:
            plantas_encontradas = []
            message = "No hay resultados"
            return render(request, 'planta/busqueda_planta.html',
                          {'planta_encontradas': plantas_encontradas, 'perfiles': perfiles, 'message': message})
    else:
        plantas_encontradas = Planta.objects.all()[0:8]
        message = None
    return render(request, 'planta/busqueda_planta.html',
                  {'planta_encontradas': plantas_encontradas, 'perfiles': perfiles, 'message': message})

"""
    Funcion juegos
    Funcion creada para acceder a la lista de juegos
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
# Juegos
def juegos(request):
    plantas = Planta.objects.all().order_by('id')
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
    return render(request, 'juego/lista_juego.html', {'plantas': plantas, 'perfiles': perfiles})

"""
    Funcion juego_memorama
    Funcion creada para acceder al juego adivina la planta.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
# juego Memorama
@login_required
def juego_memorama(request):
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
    plantas = Planta.objects.all().order_by('id')
    ranking = Juego.objects.all().order_by('aciertos', '-tiempo').reverse().filter(nombre_juego="Memorama")
    palabras = []
    palabrasc = []
    for p in range(len(plantas)):
        if ' ' in plantas[p].nombre_planta:
            palabrasc.append(plantas[p].nombre_planta)
        else:
            palabras.append(plantas[p].nombre_planta)
    return render(request, 'juego/memorama.html', {'ranking': ranking, 'palabras': palabras, 'perfiles': perfiles})

"""
    Funcion juego_sopa_de_letras
    Funcion creada para acceder al juego adivina la planta.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
# juego sopa_de_letras
@login_required
def juego_sopa_de_letras(request):
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
    plantas = Planta.objects.all().order_by('id')
    palabras = []
    palabrasc = []
    ranking = Juego.objects.all().order_by('aciertos', '-tiempo').reverse().filter(nombre_juego="Sopa de Letras")
    for p in range(len(plantas)):
        if ' ' in plantas[p].nombre_planta:
            palabrasc.append(plantas[p].nombre_planta)
        else:
            palabras.append(plantas[p].nombre_planta)
    return render(request, 'juego/sopa_de_letras.html',
                  {'ranking': ranking, 'palabras': palabras, 'perfiles': perfiles})

"""
    Funcion juego_adivina
    Funcion creada para acceder al juego adivina la planta.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
# juego Adivina
@login_required
def juego_adivina(request):
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
    plantas = Planta.objects.all().order_by('id')
    palabras = []
    palabrasimagen = []
    palabrasnc = []
    palabrasc = []
    ranking = Juego.objects.all().order_by('aciertos', '-tiempo').reverse().filter(nombre_juego="Adivina la Planta")
    for p in range(len(plantas)):
        if ' ' in plantas[p].nombre_planta:
            palabrasc.append(plantas[p].nombre_planta)
        else:
            a, b = 'áéíóúüñ', 'aeiouun'
            trans = str.maketrans(a, b)
            palabras.append(plantas[p].nombre_planta.translate(trans))
            palabrasimagen.append(plantas[p].imagen_planta.name)
            palabrasnc.append(plantas[p].nombre_cientifico)
    tamanio = (len(palabras))
    print(palabrasimagen)
    return render(request, 'juego/adivina.html',
                  {'ranking': ranking, 'perfiles': perfiles, 'palabras': palabras, 'palabrasimagen': palabrasimagen,
                   'palabrasnc': palabrasnc, 'tamanio': tamanio})

"""
    Funcion reconocimiento
    Funcion creada para realizar el reconocimiento, recupera la imagen que se sube para reconocer, se llama la la funcion de servicion y se recupera el resultado 
    rerornado en la pagina para mostar al usuario, siempre y cuando este iniciado sesion.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
# Reconocimiento
@login_required
@ratelimit(key="ip", rate="15/s")
def reconocimiento(request):
    global nombre, planta_id
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        nombre = usuario.username
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    if request.method == 'POST':
        form = ReconocimientoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            pb = Reconocimiento.objects.last()
            t = threading.Thread(target=servicio, name=nombre)
            t.start()
            if t.is_alive():
                time.sleep(20)
                # f = open('/home/franklin/YURAKU/media/datos/' + t.getName() + '.txt', 'r')
                f = open('media/datos/' + t.getName() + '.txt', 'r')
                mensaje = f.read()
                np = mensaje.split(';')
                f.close()
                nom = np[0]
                val = nom.split('+')
                query = val[0]
                if len(query) > 0:
                    if query:
                        qset = (
                            Q(nombre_planta__icontains=query)
                        )
                        plantas_encontradas = Planta.objects.filter(qset).all()
                    else:
                        plantas_encontradas = []
                else:
                    plantas_encontradas = []
                perfilesc = Perfil.objects.all()
                if len(plantas_encontradas) > 1:
                    for p in plantas_encontradas[0:1]:
                        planta_id = p.id
                elif len(plantas_encontradas) == 1:
                    planta_id = plantas_encontradas.get().id
                else:
                    planta_id = []
                # planta_id = plantas_encontradas.get().id
                if planta_id:
                    planta = get_object_or_404(Planta, pk=planta_id)
                    usuario = User.objects.get(id=request.user.id)
                    result = Resultado()
                    result.Usuario_id = usuario
                    result.Reconociento_id = pb
                    result.Planta_id = planta
                    result.puntuacion = val[1]
                    result.mas_resultados = np[1]+""+np[2]+""+np[3]+""+np[4]
                    result.save()
                    comentarios = Comentario.objects.filter(Planta_id=planta_id)
                    form = GuardarComentarioForm()
                    datos =[]
                    for i in [1, 2, 3, 4]:
                        nom2 = np[i]
                        val2 = nom2.split('+')
                        resp1 = val2[0]
                        por1 = val2[1]
                        datos.append(resp1)
                        datos.append(por1)
                    data = {'Nombre1': datos[0],
                            'Porcentaje1': datos[1],
                            'Nombre2': datos[2],
                            'Porcentaje2': datos[3],
                            'Nombre3': datos[4],
                            'Porcentaje3': datos[5],
                            'Nombre4': datos[6],
                            'Porcentaje4': datos[7],
                            }
                    return render(request, 'planta/reconocimiento.html', {'form': form, 'planta': planta, 'perfilesc': perfilesc, 'datos':data,
                                                                          'perfiles': perfiles, 'comentarios': comentarios, 'pb': pb, 'result':result})
                else:
                    return redirect('Reconocimiento')
            else:
                return redirect('Reconocimiento')
        else:
            return redirect('Reconocimiento')
    else:
        form = ReconocimientoForm()
        perfilesc = Perfil.objects.all()
        planta = []
        comentarios = []
        pb = []
        return render(request, 'planta/reconocimiento.html',
                      {'form': form, 'planta': planta, 'perfilesc': perfilesc, 'perfiles': perfiles,
                       'comentarios': comentarios, 'pb': pb})

"""
    Funcion servicio
    Funcion creada para saber que hijo a sido generado, obtener su nombre y mandar a ejecutar la red neuronal.
"""
# Hilo para le Reconocimiento
def servicio():
    pb = Reconocimiento.objects.last()
    # f = open('/home/franklin/YURAKU/media/datos/pb.txt', 'w')
    f = open('media/datos/pb.txt', 'w')
    f.write(str(pb.imagen_reconocimiento) + ";")
    f.write(str(threading.currentThread().getName()))
    f.close()
    # subprocess.run(["python", '/home/franklin/YURAKU/gestionplantas/scripts/label_image.py'])
    subprocess.run(["python", 'D:/Tesis/YURAKU/gestionplantas/scripts/label_image.py'])