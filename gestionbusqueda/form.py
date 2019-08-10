#franklin
from django import forms
from gestionbusqueda.models import Busqueda


class GuardarBusquedaForm(forms.ModelForm):
    class Meta:
        model = Busqueda
        fields = "__all__"
