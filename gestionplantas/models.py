from django.db import models

# Create your models here.
class Planta(models.Model):
    #Datos Generales
    nombre_planta = models.CharField(max_length=70)
    nombre_comun = models.CharField(max_length=70)
    nombre_cientifico = models.CharField(max_length=70, null=True, blank=True)
    #Datos Adisionales
    reino = models.CharField(max_length=50, null=True, blank=True)
    lugar_adaptacion = models.CharField(max_length=500, null=True, blank=True)
    lugar_proviene = models.CharField(max_length=500, null=True, blank=True)
    uso = models.CharField(max_length=5000, null=True, blank=True)
    como_ingerir = models.CharField(max_length=1000, null=True, blank=True)
    dosis = models.CharField(max_length=300, null=True, blank=True)
    tipo = models.CharField(max_length=50, null=True, blank=True)
    clase = models.CharField(max_length=50, null=True, blank=True)
    orden = models.CharField(max_length=50, null=True, blank=True)
    familia = models.CharField(max_length=50, null=True, blank=True)
    genero = models.CharField(max_length=50, null=True, blank=True)
    especie = models.CharField(max_length=50, null=True, blank=True)
    imagen_planta = models.ImageField(upload_to="plantas/", null=True, blank=True)


    def __str__(self):
        mensaje = (str(self.nombre_planta) + str(self.nombre_comun)  + str(self.nombre_cientifico) + str(self.reino))
        return mensaje
