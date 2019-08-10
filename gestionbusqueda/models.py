from django.db import models
from gestionplantas.models import Planta
from django.contrib.auth.models import User

# Create your models here.
class Busqueda(models.Model):
    nombre_busqueda =models.CharField(max_length=1000)
    fecha_busqueda= models.DateTimeField(auto_now_add=True, null=True)
    Usuario_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    Planta = models.ManyToManyField(Planta)

    def __str__(self):
        return self.nombre_busqueda
