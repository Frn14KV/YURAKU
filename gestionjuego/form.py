from django import forms
from gestionjuego.models import Juego


class GuardarJuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ['nombre_juego', 'aciertos', 'intentos' , 'tiempo', ]
        labels = {'nombre_juego': 'nombre del juego:',
                  'aciertos': 'aciertos del juego:',
                  'intentos': 'intentos del juego:',
                  'tiempo': 'tiempo del juego:',}
        widgets = { }
