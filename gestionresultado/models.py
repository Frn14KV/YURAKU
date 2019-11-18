"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    models: libreria propia de django para crear modulos.
    User: importa el modelo llamado User que representa los usuarios del Sistema.
    Planta: importa el modelo llamado Planta.
    Reconocimiento: importa el modelo llamado Reconocimiento.
"""
from django.db import models
from django.contrib.auth.models import User
from gestionplantas.models import Planta
from gestionreconocimiento.models import Reconocimiento

"""
    Clase Resultado
    Clase creada para generar el modelo de Resultado, es decir la tabla
    que se generara en la base de datos
        Campos
        fecha_busqueda: campo de fecha para registrar la fecha de Resultado.
        Usuario_id: campo foreignKey para registrar el Usuario que realizo el reconocimiento y se creo el Resultado.
        Planta_id: campo foreignKey para registrar que plantas son encontradas en el Resultado del reconocimiento.
        puntuacion: campo de texto para registrar la puncaion del primero Resultado del reconocimineto.
        mas_resultados: campo de texto para registrar los demas posibles Resultados del reconocimiento.

    Funcion __str__(selft)
        Funcion creada para retornar el nombre de la fecha del resultado.
            Parametro
                self:objeto instanciado de la clase Resultado
"""
class Resultado(models.Model):
    fecha_busqueda= models.DateTimeField(auto_now_add=True, null=True)
    Usuario_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    Reconociento_id = models.ForeignKey(Reconocimiento, null=False, blank=False, on_delete=models.CASCADE)
    Planta_id = models.ForeignKey(Planta, null=True, blank=True, on_delete=models.CASCADE)
    puntuacion = models.CharField(max_length=50, null=False, blank=False)
    mas_resultados = models.CharField(max_length=500, null=False, blank=False)

    def __str__(self):
        return self.fecha_busqueda
