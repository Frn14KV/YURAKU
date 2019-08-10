from django.db import models
from gestionescuela.models import Escuela
from django.contrib.auth.models import User


# Create your models here.
class Perfil(models.Model):
    nombres_perfil = models.CharField(max_length=50)
    apellidos_perfil = models.CharField(max_length=50)
    edad_perfil = models.CharField(max_length=10)
    grado_perfil = models.CharField(max_length=20)
    fecha_nacimiento_perfil = models.DateTimeField(auto_now_add=False, null=True)
    imagen_perfil = models.ImageField(upload_to="perfiles/", null=True, blank=True)
    Escuela_perfil = models.ForeignKey(Escuela, null=True, blank=True, on_delete=models.CASCADE)
    Usuario_id =models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombres_perfil




