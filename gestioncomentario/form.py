"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    forms: libreria propia de django para crear formularios
    Comentario: importa el modelo llamado Comentario.
"""
from django import forms
from gestioncomentario.models import Comentario

"""
    Clase GuardarComentarioForm
    Clase creada para generar el formulario de Comentario basado en los
    campos que tiene el modelo Comentario
        Parametros
        :param forms.ModelForm: Modelo basico propio de Django.

    Subclase Meta
        Clase creada para pasarle los atributos del moledo Comentario al
        nuevo Formulario.
            Atributos:
                model : moldelo que tengra el fomulario (en esta caso sera del modelo Comentario)
                fields : campos que tendra el formulario (en este caso sera del modelo Comentario)
                labels : mensajes que tendra en cada campo del formulario
                widgets : estilos que tendran cada campo.

"""
class GuardarComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario',]
        labels = {'comentario':'Comentario:',}
        widgets = {'comentario':forms.TextInput(attrs={'class':'form-control input-sm','placeholder': 'Comentario'}),}
