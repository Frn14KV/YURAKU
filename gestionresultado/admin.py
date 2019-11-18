"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    admin: administrador de Django
    Resultado: importa el modelo llamado Resultado.
"""
from django.contrib import admin
from gestionresultado.models import Resultado

""" Registra el modelo Busqueda en el administrador."""
admin.site.register(Resultado)
