"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    serializers: libreria propia de django para convertir datos para mandalor en los web service.
    Planta: importa el modelo llamado Planta.
"""
from rest_framework import serializers
from gestionplantas.models import Planta

""" 
   Clase PlantaSerializer
    Clase creada para generar los datos convertidos para ser enviados por los web services.
        Parametros
        :param serializers.ModelSerializer: Modelo basico propio de Django para convertirlos datos.

    Subclase Meta
        Clase creada para pasarle el modelo Planta y los campos del moledo Planta al
        formulario para ser enviados en los web service..
"""
class PlantaSerializer(serializers.ModelSerializer):
   class Meta:
      model = Planta
      fields= '__all__'
