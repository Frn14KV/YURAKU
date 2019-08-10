from rest_framework import serializers
from gestionperfil.models import Perfil

class PerfilSerializer(serializers.ModelSerializer):
   class Meta:
      model = Perfil
      fields= '__all__'
