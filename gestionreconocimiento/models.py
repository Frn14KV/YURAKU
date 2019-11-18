"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    models: libreria propia de django para crear modulos.
"""
from django.db import models

"""
    Clase  Reconocimiento
    Clase creada para generar el modelo de Reconocimiento, es decir la tabla
    que se generara en la base de datos
        Campos
        imagen_reconocimiento: campo de imagen para agregar la imagen del reconocimiento de plantas.

    Funcion __str__(selft)
        Funcion creada para retornar el nombre de la imagne del reconocimiento.
            Parametro
                self:objeto instanciado de la clase Reconocimiento
"""
class Reconocimiento(models.Model):
    imagen_reconocimiento = models.ImageField(upload_to="reconocimiento/", null=False, blank=False)

    def __str__(self):
        return self.imagen_reconocimiento
