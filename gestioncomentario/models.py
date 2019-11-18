"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    models: libreria propia de django para crear modulos
    Planta: importa el modelo llamado Planta.
    User: importa el modelo llamado User que representa los usuarios del Sistema.
"""
from django.db import models
from django.contrib.auth.models import User
from gestionplantas.models import Planta

"""
    Clase Comentario
    Clase creada para generar el modelo de Comentario, es decir la tabla
    que se generara en la base de datos
        Parametro
        models.Model: modelo propio de dijango para generar los campos de la clase Comentario.

        Campos
        comentario: campo de texto para registrar el nombre de la Comentario.
        fecha_comentario: campo de fecha para registrar la fecha de Comentario.
        Usuario_id: campo foreignKey para registrar el Usuario que realiza el Comentario.
        Planta: campo foreignKey para registrar la Planta en la cual se realiza el Comentario.

    Funcion __str__(selft)
        Funcion creada para retornar el comentario realizado.
            Parametro
                self:objeto instanciado de la clase Comentario

    Funcion get_absolute_url
        Funcion creada para permitir el acceso a los datos de las Plantas comentadas.
            Parametro
                self:objeto instanciado de la clase Comentario
"""
class Comentario(models.Model):
    comentario = models.CharField(max_length=500)
    fecha_comentario = models.DateTimeField(auto_now_add=True, null=True)
    Usuario_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    Planta_id = models.ForeignKey(Planta, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.comentario

    def get_absolute_url(self):
        pass
