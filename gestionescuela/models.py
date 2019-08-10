from django.db import models


# Create your models here.
class Escuela(models.Model):
    nombre_escuela = models.CharField(max_length=50)
    direccion_escuela = models.TextField(max_length=200)

    def __str__(self):
        return self.nombre_escuela
