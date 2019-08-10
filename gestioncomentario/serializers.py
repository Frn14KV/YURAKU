from rest_framework import serializers
from gestioncomentario.models import Comentario

class ComentarioSerializer(serializers.ModelSerializer):
   class Meta:
      model = Comentario
      fields= '__all__'
