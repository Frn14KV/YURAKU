from rest_framework import serializers
from gestionescuela.models import Escuela

class EscuelaSerializer(serializers.ModelSerializer):
   class Meta:
      model = Escuela
      fields= '__all__'
