"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    models: libreria propia de django para crear modulos
    User: importa el modelo llamado User que representa los usuarios del Sistema.
"""
from django.db import models
from django.contrib.auth.models import User

"""
    Clase Juego
    Clase creada para generar el modelo de Juego, es decir la tabla
    que se generara en la base de datos
        Parametro
        models.Model: modelo propio de dijango para generar los campos de la clase Juego.

        Campos
        Usuario_id: campo foreignKey para registrar el Usuario que ha jugado.
        nombre_juego: campo de texto para registrar el nombre del Juego.
        aciertos: campo entero para registrar los aciertos de cada juego.
        intentos: campo entero para registrar los intentos de cada juego.
        tiempo: campo de texto para registrar el tiempo que cada jugador uso para cada juego.
        fecha_comentario : campo de fecha para registrar la fecha de cuando el jugador jugo.

    Funcion __str__(selft)
        Funcion creada para retornar el mombre del juego registrado.
            Parametro
                self:objeto instanciado de la clase Juego

    Funcion get_absolute_url
        Funcion creada para permitir el acceso a los datos del modelo Juego.
            Parametro
                self:objeto instanciado de la clase Juego
"""
# Create your models here.
class Juego(models.Model):
    Usuario_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    nombre_juego = models.CharField(max_length=50)
    aciertos = models.IntegerField(default=0)
    intentos = models.IntegerField(default=0)
    tiempo = models.CharField(max_length=50)
    fecha_juego= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nombre_juego

    def get_absolute_url(self):
        pass

