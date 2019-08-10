from django.contrib.auth.models import User
from django.urls import reverse_lazy

from gestionescuela.models import Escuela
from gestionescuela.form import GuardarEscuelaForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import generics
from gestionperfil.models import Perfil
from . serializers import EscuelaSerializer

class postList(APIView):

   def get(self, request):
      allpost = Escuela.objects.all()
      serializer = EscuelaSerializer(allpost, many=True)
      return Response(serializer.data)

   def post(self):
      pass

class EscuelaList(generics.ListCreateAPIView):
    queryset = Escuela.objects.all()
    serializer_class = EscuelaSerializer

class EscuelaDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Escuela.objects.all()
    serializer_class = EscuelaSerializer


#Lista de Escuelas
# Create your views here.
@permission_required('gestionescuela.listar_escuela',reverse_lazy('homepage'))
def index(request):
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
    escuelas = Escuela.objects.all().order_by('id')
    return render(request, 'escuela/lista_escuela.html', {'escuelas': escuelas, 'perfiles':perfiles})


#Guardar Escuela
@login_required
@permission_required('gestionescuela.agregar_escuela',reverse_lazy('Escuela'))
def guardar_escuela(request):
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
    if request.method == 'POST':
        form = GuardarEscuelaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Escuela')
        else:
            form = GuardarEscuelaForm(request.POST)
            message = "datos faltantes para registrar la Escuela"
            return render(request, 'escuela/agregar_escuela.html',
                          {'form': form,'message':message, 'perfiles':perfiles})
    else:
        form = GuardarEscuelaForm()
    return render(request, 'escuela/agregar_escuela.html',
                {'message':message, 'form': form, 'perfiles':perfiles})


#Editarr Escuela
@login_required
@permission_required('gestionescuela.editar_escuela',reverse_lazy('Escuela'))
def editar_escuela(request, escuela_id):
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
    escuela = get_object_or_404(Escuela, pk=escuela_id)
    if request.method == 'POST':
        form = GuardarEscuelaForm(request.POST, instance=escuela )
        if form.is_valid():
            form.save()
            return redirect('Escuela')
        else:
            form = GuardarEscuelaForm(instance=escuela)
            message = "datos faltantes para registrar la Escuela"
            return render(request, 'escuela/editar_escuela.html',
                          {'form': form, 'message': message,'escuela ':escuela, 'perfiles':perfiles })
    else:
        form = GuardarEscuelaForm(instance=escuela)
    return render(request, 'escuela/editar_escuela.html',
                              {'form': form,'message': message, 'escuela ':escuela, 'perfiles':perfiles })


#Eliminar Escuela
@login_required
@permission_required('gestionescuela.eliminar_escuela',reverse_lazy('Escuela'))
def eliminar_escuela(request, carrera_id):
    escuela = get_object_or_404(Escuela, id=carrera_id)
    escuela.delete()
    return redirect('Escuela')