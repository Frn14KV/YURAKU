"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    models: libreria propia de django para crear modulos
    Planta: importa el modelo llamado Planta.
    User: importa el modelo llamado User que representa los usuarios del Sistema.
"""
from django.db import models
from gestionplantas.models import Planta
from django.contrib.auth.models import User

"""
    Clase Busqueda
    Clase creada para generar el modelo de Busqueda, es decir la tabla
    que se generara en la base de datos
        Campos
        nombre_busqueda: campo de texto para registrar el nombre de la Busqueda.
        fecha_busqueda: campo de fecha para registrar la fecha de Busqueda.
        Usuario_id: campo foreignKey para registrar el Usuario que realiza la Busqueda.
        Planta: campo ManyToMany para registrar que plantas son encontradas en la Busqueda.

    Funcion __str__(selft)
        Funcion creada para retornar el nombre de la busqueda realizada.
            Parametro
                :param self:objeto instanciado de la clase Busqueda

"""
class Busqueda(models.Model):
    nombre_busqueda =models.CharField(max_length=1000)
    fecha_busqueda= models.DateTimeField(auto_now_add=True, null=True)
    Usuario_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    Planta = models.ManyToManyField(Planta)

    def __str__(self):
        return self.nombre_busqueda
