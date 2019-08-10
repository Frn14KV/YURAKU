from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from gestionperfil import views

urlpatterns =[
    url(r'^perfiles/$',views.PerfilList.as_view()),
    url(r'^perfiles/(?P<pk>[0-9]+)/$',views.PerfilDetalle.as_view())
]
urlpatterns=format_suffix_patterns(urlpatterns)