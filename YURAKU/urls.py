from django.contrib import admin

admin.autodiscover()
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

import YURAKU.views
import gestionplantas.views
import gestionescuela.views
import gestionperfil.views
import gestioncomentario.views
import gestionjuego.views
import gestioncomentario
import gestionplantas.scripts



from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),

    #path('carreraw/', gestioncarrera.views.postList.as_view()),
    path('admin/doc', include('django.contrib.admindocs.urls')),
    #//////////////////webservice
    #login
    re_path(r'^weblogin/$', YURAKU.views.weblogin),
    #escuelas
    re_path(r'^',include('gestionescuela.urls')),
    #perfil
    re_path(r'^',include('gestionperfil.urls')),
    #plantas
    re_path(r'^',include('gestionplantas.urls')),
    #busqueda de plantas
    re_path(r'^busquedaweb/$', gestionplantas.views.buscar_plantas_web),

    # inicion y registro
    path('login', YURAKU.views.login_page, name="login"),
    path('loginv', YURAKU.views.login_view, name="loginv"),
    path('logout', YURAKU.views.logout_view, name="logout"),
    path('registro', YURAKU.views.registro, name='registro'),
    path('registroad', YURAKU.views.registroad, name='registroad'),
    path('registrosp', YURAKU.views.registrosp, name='registrosp'),
    re_path(r'^oauth/', include('social_django.urls', namespace="social")),

    # carga de imagenes
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    # Juegos
    path('juegos', gestionplantas.views.juegos, name='Juego'),
    path('juegos/adivina', gestionplantas.views.juego_adivina, name="juego_adivina"),
    path('juegos/memorama', gestionplantas.views.juego_memorama, name='juego_memorama'),
    path('juegos/sopa_de_letras', gestionplantas.views.juego_sopa_de_letras, name='juego_sopa_de_letras'),

    #Ranking de juegos
    path('juegos/ranking_sopa', gestionjuego.views.ranking_sopa, name='Ranking_Sopa'),
    path('juegos/ranking_adivina', gestionjuego.views.ranking_adivina, name='Ranking_Adivina'),
    path('juegos/ranking_memorama', gestionjuego.views.ranking_memorama, name='Ranking_Memorama'),
    re_path(r'^juegos/ranking/eliminar/(?P<juego_id>\d+)/$', gestionjuego.views.eliminar_ranking_adivina, name='eliminar_ranking'),

    #reporte
    path('reporteusuario', gestionjuego.views.reporte_usuario, name="report_usuario"),
    path('reportejuegos/sopa', gestionjuego.views.agregar_redord_sopa, name='guardar_sopa'),
    path('reportejuegos/memorama', gestionjuego.views.agregar_redord_memorama, name='record_memorama'),
    path('reportejuegos/adivina', gestionjuego.views.agregar_record_adivina, name='guardar_reporte'),
    re_path(r'^reporte/sopa/(?P<usuario_id>\d+)/$', gestionjuego.views.reporte_sopa_pdf, name="reporte_sopa"),
    re_path(r'^reporte/adivina/(?P<usuario_id>\d+)/$', gestionjuego.views.reporte_adivina_pdf, name="reporte_adivina"),
    re_path(r'^reporte/memorama/(?P<usuario_id>\d+)/$', gestionjuego.views.reporte_memorama_pdf, name="reporte_memorama"),
    re_path(r'^reporte_personas_pdf/$', gestionjuego.views.ReportePersonasPDF.as_view(), name="reporte_personas_pdf"),

    #inicio y opciones usuario
    path('', YURAKU.views.homepage, name="homepage"),
    path('usuarios', YURAKU.views.usuarios, name="usuarios"),
    path('apliacion', YURAKU.views.aplicacion, name="apliacion"),
    path('usuarios/editar/', YURAKU.views.editar_cuenta, name='editar_usuario'),
    path('usuarios/agregar', YURAKU.views.agregar_usuario, name='agregar_usuario'),
    re_path(r'^usuarios/perfil/(?P<usuario_id>\d+)/$', YURAKU.views.perfil, name='perfil'),
    re_path(r'^usuarios/eliminar/(?P<usuario_id>\d+)/$', YURAKU.views.eliminar, name='eliminar_usuario'),
    re_path(r'^usuarios/editar/(?P<usuario_id>\d+)/$', YURAKU.views.editar_rol_usuario, name='editar_rol'),
    re_path(r'^usuarios/editar/clave/(?P<usuario_id>\d+)/$', YURAKU.views.cambiar_clave, name="editar_clave"),

    #recuperar password
    re_path(r'^password-reset/$',auth_views.PasswordResetView.as_view(template_name='registro/password_reset_form.html'), name="password_reset"),
    re_path(r'^password-reset/done/$',auth_views.PasswordResetDoneView.as_view(template_name='registro/password_reset_done.html'), name="password_reset_done"),
    re_path(r'^password-reset/complete/$',auth_views.PasswordResetCompleteView.as_view(template_name='registro/password_reset_complete.html'), name="password_reset_complete"),
    re_path(r'^password-reset/confirm/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/$',auth_views.PasswordResetConfirmView.as_view(template_name='registro/password_reset_confirm.html'), name="password_reset_confirm"),

    #escuela
    path('escuela', gestionescuela.views.index, name='Escuela'),
    path('escuela/guardar', gestionescuela.views.guardar_escuela, name='guardar_escuela'),
    re_path(r'^escuela/editar/(?P<escuela_id>\d+)/$', gestionescuela.views.editar_escuela, name='editar_escuela'),
    re_path(r'^escuela/eliminar/(?P<escuela_id>\d+)/$', gestionescuela.views.eliminar_escuela, name='eliminar_escuela'),

    #perfil
    path('perfil/guardar', gestionperfil.views.guardar_perfil, name='guardar_perfil'),
    re_path(r'^perfil/editar/(?P<user_id>\d+)/$', gestionperfil.views.editar_perfil, name='editar_perfil'),
    re_path(r'^perfil/infor/(?P<user_id>\d+)/$', gestionperfil.views.perfil_detallado, name='perfil_detallado'),
    re_path(r'^perfil/eliminar/(?P<perfil_id>\d+)/$', gestionperfil.views.eliminar_perfil, name='eliminar_perfil'),
    re_path(r'^perfil/eliminar/busqueda/(?P<busqueda_id>\d+)/$', gestionperfil.views.eliminar_busqueda, name='eliminar_busqueda'),

    #comentario
    #path('comentario', gestionescuela.views.index, name='Escuela'),
    re_path(r'^comentario/agregar/(?P<planta_id>\d+)/$', gestioncomentario.views.agregar_comentario, name='agregar_comentario'),
    #re_path(r'^comentario/agregar/(?P<escuela_id>\d+)/$', gestionescuela.views.editar_escuela, name='editar_escuela'),
    re_path(r'^comentario/eliminar/(?P<comentario_id>\d+)/$', gestioncomentario.views.eliminar_comentario, name='eliminar_comentario'),

    #planta
    path('planta', gestionplantas.views.index, name='Planta'),
    path('planta/buscar', gestionplantas.views.buscar_plantas, name = 'buscar_planta'),
    path('planta/guardar', gestionplantas.views.guardar_planta, name='guardar_planta'),
    path('planta/reconocimiento',gestionplantas.views.reconocimeinto, name= 'Reconocimiento'),
    path('planta/prueba',gestionplantas.views.contar, name= 'prueba'),
    re_path(r'^planta/editar/(?P<planta_id>\d+)/$', gestionplantas.views.editar_planta, name='editar_planta'),
    re_path(r'^planta/infor/(?P<planta_id>\d+)/$', gestionplantas.views.planta_detalle, name='planta_detalle'),
    re_path(r'^planta/eliminar/(?P<planta_id>\d+)/$', gestionplantas.views.eliminar_planta, name='eliminar_planta')


]
#Archivos
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
