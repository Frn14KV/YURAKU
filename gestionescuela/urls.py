from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from gestionescuela import views

urlpatterns =[
    url(r'^escuelas/$',views.EscuelaList.as_view()),
    url(r'^escuelas/(?P<pk>[0-9]+)/$',views.EscuelaDetalle.as_view())
]
urlpatterns=format_suffix_patterns(urlpatterns)