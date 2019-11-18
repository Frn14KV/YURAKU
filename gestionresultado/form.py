"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    forms: libreria propia de django para crear formularios
    Resultado: importa el modelo llamado Resultado.
"""
from django import forms
from gestionresultado.models import Resultado

"""
    Clase GuardarResultadoForm
    Clase creada para generar el formulario de Resultado basado en los
    campos que tiene el modelo Resultado
        Parametros
        :param forms.ModelForm: Modelo basico propio de Django.

    Subclase Meta
        Clase creada para pasarle el modelo y los  los campos del moledo Resultado al
        nuevo Formulario.
"""

class GuardarResultadoForm(forms.ModelForm):
    class Meta:
        model = Resultado
        fields = "__all__"
