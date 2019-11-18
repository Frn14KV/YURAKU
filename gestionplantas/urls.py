"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    url: libreria propia de django para crear ulr(direciones) para acceder a funciones que estan en los views.
    format_suffix_patterns:  libreria propia de django que es un booleano que indica si los sufijos en las URL 
    deben ser opcionales u obligatorios. El valor predeterminado es False, lo que significa que los sufijos son 
    opcionales de forma predeterminada, y se le agrega format para definir el formato.
    views: importamos el archivo views de la carpeta gestionplantas, donde esta las funciones sobre le modelo de Planta.
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from gestionplantas import views

"""
    En esta parte esta las url que permiten tener un enlaces a las funciones que estan en la views de Plantas.
"""
urlpatterns =[
    url(r'^plantas/$',views.PlantaList.as_view()),
    url(r'^plantas/(?P<pk>[0-9]+)/$',views.PlantaDetalle.as_view())
]
urlpatterns=format_suffix_patterns(urlpatterns)

