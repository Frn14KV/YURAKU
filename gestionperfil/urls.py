"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    Este archvio esta creado para que en trabajos futuro se pueda utilizar web service de Comentario.
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from gestionperfil import views

urlpatterns = [
    url(r'^perfiles/$', views.PerfilList.as_view()),
    url(r'^perfiles/(?P<pk>[0-9]+)/$', views.PerfilDetalle.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)
