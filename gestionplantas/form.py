"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    forms: libreria propia de django para crear formularios
    Planta: importa el modelo llamado Planta.
"""
from django import forms
from gestionplantas.models import Planta

"""
    Clase GuardarPlantaForm
    Clase creada para generar el formulario de Planta basado en los
    campos que tiene el modelo Planta
        Parametros
        :param forms.ModelForm: Modelo basico propio de Django.

    Subclase Meta
        Clase creada para pasarle los atributos del moledo Comentario al
        nuevo Formulario.
            Atributos:
                model : moldelo que tengra el fomulario (en esta caso sera del modelo Planta)
                fields : campos que tendra el formulario (en este caso sera del modelo Planta)
                labels : mensajes que tendra en cada campo del formulario
                widgets : estilos que tendran cada campo.
"""
class GuardarPlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = ['nombre_planta',
                  'nombre_comun',
                  'nombre_cientifico',
                  'reino',
                  'lugar_adaptacion',
                  'lugar_proviene',
                  'como_ingerir',
                  'uso',
                  'dosis',
                  'tipo',
                  'clase',
                  'orden',
                  'familia',
                  'genero',
                  'especie',
                  'imagen_planta',]
        labels = {'nombre_planta':'Nombre de la Planta:',
                  'nombre_comun':'Nombre Común:',
                  'nombre_cientifico': 'Nombre Cientifico:',
                  'reino': 'Reino:',
                  'lugar_adaptacion': 'Lugar de Adaptacion:',
                  'lugar_proviene': 'Lugar de donde proviene:',
                  'como_ingerir':'Como ingerir',
                  'uso':'Uso',
                  'dosis': 'Dosis:',
                  'tipo': 'Tipo:',
                  'clase': 'Clase:',
                  'orden': 'Orden:',
                  'familia': 'Familia:',
                  'genero': 'Genero:',
                  'especie': 'Especie:',}
        widgets = {'nombre_planta':forms.TextInput(attrs={'class':'form-control','placeholder': 'Ejemplo: Floripondio'}),
                   'nombre_comun':forms.TextInput(attrs={'class':'form-control','placeholder': 'Ejemplo: Guanto'}),
                   'nombre_cientifico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Es para fines educativos'}),
                   'reino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Plantae'}),
                   'lugar_adaptacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Todo el mundo'}),
                   'lugar_proviene': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Todo el mundo'}),
                   'uso': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Sedante para dormir'}),
                   'como_ingerir': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Se debe hacer infusión'}),
                   'dosis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: cada noche durante 1 semana'}),
                   'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Magnoliophyta.'}),
                   'clase': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Dicotyledons'}),
                   'orden': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Dicotyledons'}),
                   'familia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Solanaceae'}),
                   'genero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Brugmansia'}),
                   'especie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Arbustiva'}),}