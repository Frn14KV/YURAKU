"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    admin: administrador de Django
    Busqueda: importa el modelo llamado Busqueda.
"""
from django.contrib import admin
from gestionbusqueda.models import Busqueda

""" 
    Registra el modelo Busqueda en el administrador.
"""
admin.site.register(Busqueda)
