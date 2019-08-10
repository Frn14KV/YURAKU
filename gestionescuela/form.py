from django import forms
from gestionescuela.models import Escuela


class GuardarEscuelaForm(forms.ModelForm):
    class Meta:
        model = Escuela
        fields = ['nombre_escuela',
                  'direccion_escuela',]
        labels = {'nombre_escuela':'Nombre:',
                  'direccion_escuela':'Direccion:',}
        widgets = {'nombre_escuela':forms.TextInput(attrs={'class':'form-control','placeholder': 'Ejemplo: Escuela Remigio Crespo.'}),
                   'direccion_escuela': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Ejemplo: Av. de las Americas.'}),}
