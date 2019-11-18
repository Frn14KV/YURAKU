"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    admin: administrador de Django
    Juego: importa el modelo llamado Juego.
"""
from django.contrib import admin
from gestionjuego.models import Juego

""" Registra el modelo Busqueda en el administrador."""
admin.site.register(Juego)