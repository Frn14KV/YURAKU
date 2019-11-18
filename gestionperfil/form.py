"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    forms: libreria propia de django para crear formularios
    Perfil: importa el modelo llamado Perfil.
"""
from django import forms
from gestionperfil.models import Perfil

"""
    Clase GuardarPerfilForm
    Clase creada para generar el formulario de Perfil basado en los
    campos que tiene el modelo Perfil
        Parametros
        :param forms.ModelForm: Modelo basico propio de Django.

    Subclase Meta
        Clase creada para pasarle los atributos del moledo Perfil al
        nuevo Formulario.
            Atributos:
                model : moldelo que tengra el fomulario (en esta caso sera del modelo Perfil)
                fields : campos que tendra el formulario (en este caso sera del modelo Perfil)
                labels : mensajes que tendra en cada campo del formulario
                widgets : estilos que tendran cada campo.

"""
class GuardarPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nombres_perfil',
                  'apellidos_perfil',
                  'edad_perfil',
                  'fecha_nacimiento_perfil',
                  'grado_perfil',
                  'imagen_perfil',
                  'escuela_perfil',
                  'Usuario_id',]
        labels = {'nombres_perfil':'Nombres Completos:',
                  'apellidos_perfil':'Apellidos Completos:',
                  'edad_perfil': 'Edad:',
                  'fecha_nacimiento_perfil':'Fecha de Nacimiento:',
                  'grado_perfil':'Grado:',
                  'escuela_perfil':'Escuela:'}
        widgets = {'nombres_perfil':forms.TextInput(attrs={'class':'form-control','placeholder': 'Ejemplo: Ricardo Xavie'}),
                   'apellidos_perfil': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ejemplo: Carrion Parra'}),
                   'edad_perfil': forms.NumberInput(attrs={'class': 'form-control', 'name': 'edad_perfil', 'placeholder': 'Ejemplo: 7','type': 'number'}),
                   'grado_perfil': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ejemplo: tercero'}),
                   'escuela_perfil': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Escuela 1'}),
                   'fecha_nacimiento_perfil': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 03/03/2018','type':'date'}),}


