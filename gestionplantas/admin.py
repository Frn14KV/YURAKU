"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    admin: administrador de Django
    Planta: importa el modelo llamado Planta.
"""

from django.contrib import admin
from gestionplantas.models import Planta

""" Registra el modelo Planta en el administrador."""
admin.site.register(Planta)