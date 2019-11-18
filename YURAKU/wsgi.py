"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
La comunidad web Python ha creado un estándar llamado Web Server Gateway Interface,
o por sus siglas, WSGI. Este standar nos permite escribir programas los cuales puedan
comunicarse a través del protocolo HTTP, es decir, Internet.

WSGI de configuracion para proyecto YURAKU .

El WSGI invocado como una variable de nivel de módulo se lo denomina "application".

Para obtener más información sobre este archivo, vea
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YURAKU.settings')

application = get_wsgi_application()
