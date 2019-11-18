"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    forms: libreria propia de django para crear formularios
    Reconocimiento: importa el modelo llamado Reconocimiento.
"""
from django import forms
from gestionreconocimiento.models import Reconocimiento

"""
    Clase ReconocimientoForm
    Clase creada para generar el formulario de Reconocimiento basado en los
    campos que tiene el modelo Reconocimiento
        Parametros
        :param forms.ModelForm: Modelo basico propio de Django.

    Subclase Meta
        Clase creada para pasarle el modelo y los  los campos del moledo Reconocimiento al
        nuevo Formulario.
"""
class ReconocimientoForm(forms.ModelForm):
    class Meta:
        model = Reconocimiento
        fields = "__all__"