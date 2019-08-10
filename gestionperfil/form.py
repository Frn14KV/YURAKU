from django import forms
from gestionperfil.models import Perfil


class GuardarPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nombres_perfil',
                  'apellidos_perfil',
                  'edad_perfil',
                  'fecha_nacimiento_perfil',
                  'grado_perfil',
                  'imagen_perfil',
                  'Escuela_perfil',
                  'Usuario_id',]
        labels = {'nombres_perfil':'Nombres Completos:',
                  'apellidos_perfil':'Apellidos Completos:',
                  'edad_perfil': 'Edad:',
                  'fecha_nacimiento_perfil':'Fecha de Nacimiento:',
                  'grado_perfil':'Grado:'}
        widgets = {'nombres_perfil':forms.TextInput(attrs={'class':'form-control','placeholder': 'Ejemplo: Ricardo Xavie'}),
                   'apellidos_perfil': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ejemplo: Carrion Parra'}),
                   'edad_perfil': forms.NumberInput(attrs={'class': 'form-control', 'name': 'edad_perfil', 'placeholder': 'Ejemplo: 7','type': 'number'}),
                   'grado_perfil': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ejemplo: tercero'}),
                   'fecha_nacimiento_perfil': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 03/03/2018','type':'date'}),}


