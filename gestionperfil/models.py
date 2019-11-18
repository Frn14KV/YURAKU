"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    models: libreria propia de django para crear modulos
    User: importa el modelo llamado User que representa los usuarios del Sistema.
"""
from django.db import models
from django.contrib.auth.models import User

"""
    Clase Perfil
    Clase creada para generar el modelo de Perfil, es decir la tabla
    que se generara en la base de datos
        Campos
        nombres_perfil: campo de texto para registrar los nombres del usuario del Perfil.
        apellidos_perfil: campo de texto para registrar los apellidos del usuario del Perfil.
        edad_perfil: campo de texto para registrar la edad del del usuario Perfil.
        grado_perfil: campo de texto para registrar el grado de estudio del usuario del Perfil.
        imagen_perfil: campo de imagen para agregar la imagen que tendra el Perfil del usuario..
        escuela_perfil: campo de texto para registrar el nombre de la escuela del Perfil
        fecha_nacimiento_perfil= campo de fecha para registrar la fecha de nacimiento del usuario del Perfil.
        Usuario_id = campo foreignKey para registrar el Usuario que tendra el Perfil.

    Funcion __str__(selft)
        Funcion creada para retornar los nombres del perfil creado.
            Parametro
                self:objeto instanciado de la clase Perfil
"""
class Perfil(models.Model):
    nombres_perfil = models.CharField(max_length=50)
    apellidos_perfil = models.CharField(max_length=50)
    edad_perfil = models.CharField(max_length=10)
    grado_perfil = models.CharField(max_length=20)
    fecha_nacimiento_perfil = models.DateTimeField(auto_now_add=False, null=True)
    imagen_perfil = models.ImageField(upload_to="perfiles/", null=True, blank=True)
    escuela_perfil = models.CharField(max_length=50)
    Usuario_id =models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombres_perfil