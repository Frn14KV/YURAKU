#franklin
from django import forms
from gestionayudar.models import Ayudar


class AyudarForm(forms.ModelForm):
    class Meta:
        model = Ayudar
        fields = "__all__"
