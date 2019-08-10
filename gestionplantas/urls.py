from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns

from gestionplantas import views

urlpatterns =[
    url(r'^plantas/$',views.PlantaList.as_view()),
    url(r'^plantas/(?P<pk>[0-9]+)/$',views.PlantaDetalle.as_view())
]
urlpatterns=format_suffix_patterns(urlpatterns)

