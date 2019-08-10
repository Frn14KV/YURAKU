from django.db import models
# Create your models here.
class Ayudar(models.Model):
    imagen_reconocimiento = models.ImageField(upload_to="reconocimiento/", null=False, blank=False)

    def __str__(self):
        return self.imagen_reconocimiento
