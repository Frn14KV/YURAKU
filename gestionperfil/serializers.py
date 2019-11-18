"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    Este archvio esta creado para que en trabajos futuro se pueda utilizar web service de Comentario.
"""
from rest_framework import serializers
from gestionperfil.models import Perfil

class PerfilSerializer(serializers.ModelSerializer):
   class Meta:
      model = Perfil
      fields= '__all__'
