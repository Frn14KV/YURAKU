#franklin
from django import forms
from gestionayuda.models import Ayuda


class GuardarForm(forms.ModelForm):
    class Meta:
        model = Ayuda
        fields = "__all__"
