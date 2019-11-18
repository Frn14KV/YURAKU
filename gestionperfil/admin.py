"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    admin: administrador de Django
    Perfil: importa el modelo llamado Perfil.
"""
from django.contrib import admin
from gestionperfil.models import Perfil

""" Registra el modelo Perfil en el administrador."""
admin.site.register(Perfil)
