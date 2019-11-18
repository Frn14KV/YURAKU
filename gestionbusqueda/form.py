"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    forms: libreria propia de django para crear formularios
    Busqueda: importa el modelo llamado Busqueda.
"""
from django import forms
from gestionbusqueda.models import Busqueda

"""
    Clase GuardarBusquedaForm
    Clase creada para generar el formulario de Busqueda basado en los
    campos que tiene el modelo Busqueda
        Parametros
        :param forms.ModelForm: Modelo basico propio de Django.

    Subclase Meta
        Clase creada para pasarle el modelo y los  los campos del moledo Busqueda al
        nuevo Formulario.

"""
class GuardarBusquedaForm(forms.ModelForm):
    class Meta:
        model = Busqueda
        fields = "__all__"
