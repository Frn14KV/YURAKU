"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    forms: libreria propia de django para crear formularios
    Juego: importa el modelo llamado Juego.
"""
from django import forms
from gestionjuego.models import Juego

"""
    Clase GuardarJuegoForm
    Clase creada para generar el formulario de Juego basado en los
    campos que tiene el modelo Juego
        Parametros
        :param forms.ModelForm: Modelo basico propio de Django.

    Subclase Meta
        Clase creada para pasarle los atributos del moledo Juego al
        nuevo Formulario.
            Atributos:
                model: moldelo que tengra el fomulario (en esta caso sera del modelo Juego)
                fields: campos que tendra el formulario (en este caso sera del modelo Juego)
                labels: mensajes que tendra en cada campo del formulario
                widgets: estilos que tendran cada campo.

"""
class GuardarJuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ['nombre_juego', 'aciertos', 'intentos' , 'tiempo', ]
        labels = {'nombre_juego': 'nombre del juego:',
                  'aciertos': 'aciertos del juego:',
                  'intentos': 'intentos del juego:',
                  'tiempo': 'tiempo del juego:',}
        widgets = { }
