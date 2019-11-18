"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    models: libreria propia de django para crear modulos.
"""
from django.db import models

"""
    Clase Planta
    Clase creada para generar el modelo de Planta, es decir la tabla
    que se generara en la base de datos.
        Campos
        #Datos Generales
        nombre_planta: campo de texto para ingresar el nombre de la Planta.
        nombre_comun: campo de texto para ingresar los nombres comunes que tiene la Planta.
        nombre_cientifico: campo de texto para ingresar el nombre cientifico que tiene la Planta.
        #Datos Adisionales
        reino: campo de texto para ingresar el reino de la Planta
        lugar_adaptacion: campo de texto para ingresar el lugar de adaptacion que tiene la Planta.
        lugar_proviene: campo de texto para ingresar el lugar de donde proviene de la Planta.
        uso: campo de texto para ingresar el uso que se tiene de la Planta.
        como_ingerir: campo de texto para ingresar como se debe ingerir la Planta.
        dosis: campo de texto para ingresar la dosis que se debe subministrar de la Planta.
        tipo: campo de texto para ingresar el tipo que es la Planta.
        clase: campo de texto para ingresar la clase que es la Planta.
        orden: campo de texto para ingresar el orden que es la Planta.
        familia: campo de texto para ingresar la familia que es la Planta.
        genero: campo de texto para ingresar el genero que es la Planta.
        especie: campo de texto para ingresar la especie que es la Planta.
        imagen_planta = campo de imagen para asignarle una imagen a la Planta.

    Funcion __str__(selft)
        Funcion creada para retornar: nombre_planta, nombre_comun, nombre_cientifico y reino de la planta registrada.
            Parametro
                self:objeto instanciado de la clase Planta.
"""
# Create your models here.
class Planta(models.Model):
    #Datos Generales
    nombre_planta = models.CharField(max_length=70)
    nombre_comun = models.CharField(max_length=70)
    nombre_cientifico = models.CharField(max_length=70, null=True, blank=True)
    #Datos Adisionales
    reino = models.CharField(max_length=50, null=True, blank=True)
    lugar_adaptacion = models.CharField(max_length=500, null=True, blank=True)
    lugar_proviene = models.CharField(max_length=500, null=True, blank=True)
    uso = models.CharField(max_length=5000, null=True, blank=True)
    como_ingerir = models.CharField(max_length=1000, null=True, blank=True)
    dosis = models.CharField(max_length=300, null=True, blank=True)
    tipo = models.CharField(max_length=50, null=True, blank=True)
    clase = models.CharField(max_length=50, null=True, blank=True)
    orden = models.CharField(max_length=50, null=True, blank=True)
    familia = models.CharField(max_length=50, null=True, blank=True)
    genero = models.CharField(max_length=50, null=True, blank=True)
    especie = models.CharField(max_length=50, null=True, blank=True)
    imagen_planta = models.ImageField(upload_to="plantas/", null=True, blank=True)


    def __str__(self):
        mensaje = (str(self.nombre_planta) + str(self.nombre_comun) + str(self.nombre_cientifico) + str(self.reino))
        return mensaje
