from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from gestionplantas.models import Planta

# Create your models here.
class Comentario(models.Model):
    comentario = models.CharField(max_length=500)
    fecha_comentario= models.DateTimeField(auto_now_add=True, null=True)
    Usuario_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    Planta_id = models.ForeignKey(Planta, null=False, blank=False, on_delete=models.CASCADE)
    #like = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="likes")

    def __str__(self):
        return self.comentario

    def get_absolute_url(self):
        pass
