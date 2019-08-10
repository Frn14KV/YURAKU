from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Juego(models.Model):
    Usuario_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    nombre_juego = models.CharField(max_length=50)
    aciertos = models.IntegerField(default=0)
    intentos = models.IntegerField(default=0)
    tiempo = models.CharField(max_length=50)
    fecha_juego= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nombre_juego

    def get_absolute_url(self):
        pass
