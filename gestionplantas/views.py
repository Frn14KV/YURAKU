import os

from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from rest_framework.utils import json

from django.contrib.auth.models import User

from gestionayudar.models import Ayudar
from gestionbusqueda.models import Busqueda
from gestioncomentario.form import GuardarComentarioForm
from gestioncomentario.models import Comentario
from gestionperfil.models import Perfil
from gestionplantas.form import GuardarPlantaForm
from gestionayudar.form import AyudarForm
from gestionplantas.models import Planta

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import PlantaSerializer
from rest_framework import generics

import subprocess
import time


##Web Service
class postList(APIView):

    def get(self, request):
        allpost = Planta.objects.all()
        serializer = PlantaSerializer(allpost, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class PlantaList(generics.ListCreateAPIView):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer


class PlantaDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer


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


# perfil Planta
# @permission_required('gestionproyecto.listar_proyecto',reverse_lazy('Proyecto'))
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


# eliminar Planta
@login_required
@permission_required('gestionplantas.eliminar_planta', reverse_lazy('Planta'))
def eliminar_planta(request, planta_id):
    planta = get_object_or_404(Planta, id=planta_id)
    planta.delete()
    return redirect('Planta')


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
    palabras = []
    palabrasc = []
    for p in range(len(plantas)):
        if ' ' in plantas[p].nombre_planta:
            palabrasc.append(plantas[p].nombre_planta)
        else:
            palabras.append(plantas[p].nombre_planta)
    return render(request, 'juego/memorama.html', {'palabras': palabras, 'perfiles': perfiles})


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
    for p in range(len(plantas)):
        if ' ' in plantas[p].nombre_planta:
            palabrasc.append(plantas[p].nombre_planta)
        else:
            palabras.append(plantas[p].nombre_planta)
    return render(request, 'juego/sopa_de_letras.html', {'palabras': palabras, 'perfiles': perfiles})


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
    for p in range(len(plantas)):
        if ' ' in plantas[p].nombre_planta:
            palabrasc.append(plantas[p].nombre_planta)
        else:
            a, b = 'áéíóúüñ', 'aeiouun'
            trans = str.maketrans(a, b)
            palabras.append(plantas[p].nombre_planta.translate(trans))
            palabrasimagen.append(plantas[p].imagen_planta)
            palabrasnc.append(plantas[p].nombre_cientifico)
    tamanio = (len(palabras))
    return render(request, 'juego/adivina.html',
                  {'perfiles': perfiles, 'palabras': palabras, 'palabrasimagen': palabrasimagen,
                   'palabrasnc': palabrasnc, 'tamanio': tamanio})


# reconocimiento
@login_required
def reconocimeinto(request):
    global nombre
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
        form = AyudarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            pb = Ayudar.objects.last()
            f = open('pb.txt', 'w')
            f.write(str(pb.imagen_reconocimiento)+";")
            f.write(str(nombre))
            f.close()
            process1 = subprocess.run(['python', 'D:/Tesis/YURAKU/gestionplantas/scripts/label_image.py '])
            # process1 = subprocess.Popen(['python', 'D:/Tesis/TesisVF/gestionplantas/scripts/label_image.py --graph=D:/Tesis/TesisVF/gestionplantas/tf_files/retrained_graph.pb --image = D:/Tesis/TesisVF/gestionplantas/rosas.jpg'])
            print(process1.returncode)
            while process1 == 0:
                print("SI")

            time.sleep(5)
            print(nombre)
            f = open(nombre+'.txt', 'r')
            mensaje = f.read()
            np = mensaje.split(';')
            f.close()
            nom = np[0]
            val = nom.split(' ')
            query = val[0]
            if len(query) > 0:
                if query:
                    qset = (
                        Q(nombre_planta__icontains=query)
                    )
                    plantas_encontradas = Planta.objects.filter(qset).all().first()
                    # userid = request.user.id
                    # if userid != None:
                    #   usuario = get_object_or_404(User, id=userid)
                    #  form.nombre_busqueda = query
                    # form.Usuario_id = usuario
                    # form.save()
                    # for i in (plantas_encontradas):
                    #   planta = get_object_or_404(Planta, pk=i.id)
                    #  form.Planta.add(planta)
                    message = "La búsqueda tuvo los siguientes resultados:"
                else:
                    plantas_encontradas = []
                    message = "No hay resultados."
            else:
                plantas_encontradas = []
                message = None
            perfilesc = Perfil.objects.all()
            planta_id = plantas_encontradas.get().id
            planta = get_object_or_404(Planta, pk=planta_id)
            comentarios = Comentario.objects.filter(Planta_id=planta_id)
            form = GuardarComentarioForm()
            return render(request, 'planta/reconocimiento.html',
                          {'form': form, 'planta': planta, 'perfilesc': perfilesc, 'perfiles': perfiles,
                           'comentarios': comentarios, 'pb': pb})
    else:
        form = AyudarForm()
        perfilesc = Perfil.objects.all()
        planta = []
        comentarios = []
        pb = []
        return render(request, 'planta/reconocimiento.html',
                      {'form': form, 'planta': planta, 'perfilesc': perfilesc, 'perfiles': perfiles,
                       'comentarios': comentarios, 'pb': pb})


from ratelimit.decorators import ratelimit
#hilo de reconocimiento
@login_required
@ratelimit(key="ip", rate="15/s")
def reconocimiento(request):
    global nombre, planta_id
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        nombre =usuario.username
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    if request.method == 'POST':
        form = AyudarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            pb = Ayudar.objects.last()
            t = threading.Thread(target=servicio, name=nombre)
            t.start()
            if t.is_alive():
                time.sleep(5)
                f = open('media/datos/' + t.getName()+'.txt', 'r')
                mensaje = f.read()
                np = mensaje.split(';')
                f.close()
                nom = np[0]
                val = nom.split(' ')
                query = val[0]
                if len(query) > 0:
                    if query:
                        qset = (
                            Q(nombre_planta__icontains=query)
                        )
                        plantas_encontradas = Planta.objects.filter(qset).all()
                        # userid = request.user.id
                        # if userid != None:
                        #   usuario = get_object_or_404(User, id=userid)
                        #  form.nombre_busqueda = query
                        # form.Usuario_id = usuario
                        # form.save()
                        # for i in (plantas_encontradas):
                        #   planta = get_object_or_404(Planta, pk=i.id)
                        #  form.Planta.add(planta)
                        message = "La búsqueda tuvo los siguientes resultados:"
                    else:
                        plantas_encontradas = []
                        message = "No hay resultados."
                else:
                    plantas_encontradas = []
                    message = None
                perfilesc = Perfil.objects.all()
                #if len(plantas_encontradas)>1:
                 #   for p in plantas_encontradas[0:1]:
                  #      planta_id = p.id
                #else:
                 #   planta_id = plantas_encontradas.get().id
                planta_id = plantas_encontradas.get().id
                planta = get_object_or_404(Planta, pk=planta_id)
                comentarios = Comentario.objects.filter(Planta_id=planta_id)
                form = GuardarComentarioForm()
                return render(request, 'planta/reconocimiento.html',
                              {'form': form, 'planta': planta, 'perfilesc': perfilesc, 'perfiles': perfiles,
                               'comentarios': comentarios, 'pb': pb})
            else:
                print("se fue")
                return redirect('Reconocimiento')
    else:
        form = AyudarForm()
        perfilesc = Perfil.objects.all()
        planta = []
        comentarios = []
        pb = []
        return render(request, 'planta/reconocimiento.html',
                      {'form': form, 'planta': planta, 'perfilesc': perfilesc, 'perfiles': perfiles,
                       'comentarios': comentarios, 'pb': pb})


import threading
import time
def servicio():
    pb = Ayudar.objects.last()
    f = open('media/datos/pb.txt', 'w')
    #print(str(threading.currentThread().getName()))
    f.write(str(pb.imagen_reconocimiento)+";")
    f.write(str(threading.currentThread().getName()))
    f.close()
    #process1 = subprocess.Popen(['python', 'D:/Tesis/TesisVF/gestionplantas/scripts/label_image.py '])
    p = subprocess.run(["python", 'D:/Tesis/YURAKU/gestionplantas/scripts/label_image.py'])


def send_simple_message():
    return requests.post(
		"https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages",
		auth=("api", "YOUR_API_KEY"),
		data={"from": "Excited User <mailgun@YOUR_DOMAIN_NAME>",
			"to": ["bar@example.com", "YOU@YOUR_DOMAIN_NAME"],
			"subject": "Hello",
			"text": "Testing some Mailgun awesomness!"})