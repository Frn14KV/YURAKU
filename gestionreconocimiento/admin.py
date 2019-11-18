"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    admin: administrador de Django
    Reconocimiento: importa el modelo llamado Reconocimiento.
"""
from django.contrib import admin
from gestionreconocimiento.models import Reconocimiento

""" Registra el modelo Busqueda en el administrador."""
admin.site.register(Reconocimiento)
