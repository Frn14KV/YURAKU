"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    admin: administrador de Django
    Busqueda: importa el modelo llamado Comentario.
"""
from django.contrib import admin
from gestioncomentario.models import Comentario

""" 
    Registra el modelo Comentario en el administrador.
"""
admin.site.register(Comentario)
