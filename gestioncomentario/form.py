from django import forms
from gestioncomentario.models import Comentario


class GuardarComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario',]
        labels = {'comentario':'Comentario:',}
        widgets = {'comentario':forms.TextInput(attrs={'class':'form-control input-sm','placeholder': 'Comentario'}),}
