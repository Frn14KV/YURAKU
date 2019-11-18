"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    date: libreria propia de django para manejar fechas y todo lo que conlleve estas.
    login_required: libreria propia de django para controlar que este iniciado sesion para acceder a una funcion.
    permission_required: libreria propia de django para verificar si tiene permisos para realizar ciertas funciones.
    reverse_lazy: libreria propia de django para retornar a una pagina espeficica si no tiene permisos.
    colors: libreria propia de django para manejar colores de letra en la hoja de reportes.
    TA_CENTER: libreria propia de django para centrar cualquier tipo de texto en la hoja de reportes.
    getSampleStyleSheet: libreria propia de django para manejar las cabeceras de las tablas.
    cm: libreria propia de jango para manejar la posicion que tendra la tabla en la hoja para los reportes.
    A4: libreria propia de django para manejar el estilo de la hoja para los reportes.
    TableStyle: libreria propia de django para manejar los estilos de tablas en los reportes.
    Table: libreria propia de django para manejar las tablas para los reportes.
    Paragraph: libreria propia para crear cada uno de los encabesados de la cabecera de la tabla de los reportes.
    HttpResponse: libreria propia de django para generar respuestas web mas simples.
    redirect: libreria propia de django para acceder a una pagina de manera mas rapida sin paso de datos.
    get_object_or_404: libreria propia de django para realizar una busqueda de un objeto de un modelo.
    render: libreria propia de django para retornar una pagina web con sus resultados.
    User: importa el modelo llamado User que representa los usuarios del Sistema.
    GuardarJuegoForm: importa el formulario llamado GuardarJuegoForm.
    Juego: importa el modelo llamado Juego.
    Perfil: importa el modelo llamado Perfil.
    Planta: importa el modelo llamado Planta.
    BytesIO: libreria propia de django que permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    canvas: libreria propia de django que permite hacer el reporte con coordenadas X y Y
    View: libreria propia de dajngo para usar una vista basica.
"""
from datetime import date
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import TableStyle, Table, Paragraph
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from gestionjuego.form import GuardarJuegoForm
from gestionjuego.models import Juego
from gestionperfil.models import Perfil
from gestionplantas.models import Planta
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View

"""
    Funcion reporte_usuario
    Funcion creada para guardar acceder a la pagina de reportes siempre y cuando este iniciado sesion y tenga el permiso para usar esta funcion, si lo tiene retorna una pagina web de reportes;
    Si no tiene regresara a la pagina principal.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
# Reportes
@permission_required('gestionescuela.agregar_escuela',reverse_lazy('homepage'))
@login_required
def reporte_usuario(request):
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    usuarios = User.objects.all().order_by('id')
    return render(request, 'reporte/reporte_usuario.html', {'usuarios': usuarios, 'perfiles': perfiles})

"""
    Funcion reporte_adivina_pdf
    Funcion creada para generar reportes de un usuario especifico del juego Adivina la Palabra y retorna un archivo pdf con los resultados.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        usuario_id: representa el id del usuario del que se quiere realizar el reporte.
"""
# reporte del juego Adivina
def reporte_adivina_pdf(request, usuario_id):
    # Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    # La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = BytesIO()
    # Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer, pagesize=A4)
    # cabecera
    pdf.setLineWidth(.3)
    # Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
    #archivo_imagen = '/home/franklin/YURAKU/static/AdminLTE-2.4.2/img/reporte/logo.png'
    archivo_imagen = 'D:/Tesis/YURAKU/static/AdminLTE-2.4.2/img/reporte/logo.png'
    # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
    pdf.drawImage(archivo_imagen, 430, 700, 150, 150, preserveAspectRatio=True)
    #log_imagen = '/home/franklin/YURAKU/static/AdminLTE-2.4.2/img/reporte/hoja.png'
    log_imagen = 'D:/Tesis/YURAKU/static/AdminLTE-2.4.2/img/reporte/hoja.png'
    # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
    pdf.drawImage(log_imagen, 30, 740, 50, 50, preserveAspectRatio=True)
    #
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(480, 745, str(date.today()))
    pdf.line(460, 757, 560, 757)
    # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Helvetica", 16)
    # Dibujamos una cadena en la ubicación X,Y especificada
    pdf.drawString(250, 790, u"REPORTE")
    # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Helvetica", 12)
    pdf.drawString(230, 775, u"ADIVINA LA PLANTA")
    #aqui
    # Creamos una tupla de encabezados para neustra tabla
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    usuario = Paragraph('''Usuario''', styleBH)
    nombre_j = Paragraph('''Nombre del Juego''', styleBH)
    aciertos = Paragraph('''Aciertos''', styleBH)
    intentos = Paragraph('''Intentos''', styleBH)
    tiempo = Paragraph('''Tiempo de Juego''', styleBH)

    data = [[usuario, nombre_j, aciertos, intentos, tiempo]]

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    width, height = A4
    high = 700
    for jueg in Juego.objects.all().filter(Usuario_id=usuario_id, nombre_juego="Adivina la Planta"):
        this_jueg = [str(jueg.Usuario_id.first_name) + " " + str(jueg.Usuario_id.last_name), jueg.nombre_juego,
                     jueg.aciertos, jueg.intentos, jueg.tiempo]
        data.append(this_jueg)
        high = high - 18

    width, height = A4
    table = Table(data, colWidths=[4.9 * cm, 6.5 * cm, 1.9 * cm, 2 * cm, 4 * cm, 5 * cm])
    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    # Establecemos el tamaño de la hoja que ocupará la tabla
    table.wrapOn(pdf, width, height)
    # Definimos la coordenada donde se dibujará la tabla
    table.drawOn(pdf, 30, high)
    # Con show page hacemos un corte de página para pasar a la siguiente
    pdf.showPage()
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

"""
    Funcion reporte_sopa_pdf
    Funcion creada para generar reportes de un usuario especifico del juego Sopa de Letras y retorna un archivo pdf con los resultados.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        usuario_id: representa el id del usuario del que se quiere realizar el reporte.
"""
# reporte del juego Sopa de Letras
def reporte_sopa_pdf(request, usuario_id):
    # Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    # La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = BytesIO()
    # Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer, pagesize=A4)
    # cabecera
    pdf.setLineWidth(.3)
    # Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
    #archivo_imagen = '/home/franklin/YURAKU/static/AdminLTE-2.4.2/img/reporte/logo.png'
    archivo_imagen = 'D:/Tesis/YURAKU/static/AdminLTE-2.4.2/img/reporte/logo.png'
    # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
    pdf.drawImage(archivo_imagen, 430, 700, 150, 150, preserveAspectRatio=True)
    #log_imagen = '/home/franklin/YURAKU/static/AdminLTE-2.4.2/img/reporte/hoja.png'
    log_imagen = 'D:/Tesis/YURAKU/static/AdminLTE-2.4.2/img/reporte/hoja.png'
    # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
    pdf.drawImage(log_imagen, 30, 740, 50, 50, preserveAspectRatio=True)
    #
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(480, 745, str(date.today()))
    pdf.line(460, 757, 560, 757)
    # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Helvetica", 16)
    # Dibujamos una cadena en la ubicación X,Y especificada
    pdf.drawString(250, 790, u"REPORTE")
    # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Helvetica", 12)
    pdf.drawString(237, 775, u"SOPA DE LETRAS")
    #aqui
    # Creamos una tupla de encabezados para neustra tabla
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    usuario = Paragraph('''Usuario''', styleBH)
    nombre_j = Paragraph('''Nombre del Juego''', styleBH)
    aciertos = Paragraph('''Aciertos''', styleBH)
    intentos = Paragraph('''Intentos''', styleBH)
    tiempo = Paragraph('''Tiempo de Juego''', styleBH)

    data = [[usuario, nombre_j, aciertos, intentos, tiempo]]

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    width, height = A4
    high = 700
    for jueg in Juego.objects.all().filter(Usuario_id=usuario_id, nombre_juego="Sopa de Letras"):
        this_jueg = [str(jueg.Usuario_id.first_name) + " " + str(jueg.Usuario_id.last_name), jueg.nombre_juego,
                     jueg.aciertos, jueg.intentos, jueg.tiempo]
        data.append(this_jueg)
        high = high - 18

    width, height = A4
    table = Table(data, colWidths=[4.9 * cm, 6.5 * cm, 1.9 * cm, 2 * cm, 4 * cm, 5 * cm])
    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    # Establecemos el tamaño de la hoja que ocupará la tabla
    table.wrapOn(pdf, width, height)
    # Definimos la coordenada donde se dibujará la tabla
    table.drawOn(pdf, 30, high)
    # Con show page hacemos un corte de página para pasar a la siguiente
    pdf.showPage()
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

"""
    Funcion reporte_memorama_pdf
    Funcion creada para generar reportes de un usuario especifico del juego Memorama y retorna un archivo pdf con los resultados.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        usuario_id: representa el id del usuario del que se quiere realizar el reporte.
"""
# reporte del juego Memorama
def reporte_memorama_pdf(request, usuario_id):
    # Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    # La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = BytesIO()
    # Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer, pagesize=A4)
    # cabecera
    pdf.setLineWidth(.3)
    # Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
    #archivo_imagen = '/home/franklin/YURAKU/static/AdminLTE-2.4.2/img/reporte/logo.png'
    archivo_imagen = 'D:/Tesis/YURAKU/static/AdminLTE-2.4.2/img/reporte/logo.png'
    # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
    pdf.drawImage(archivo_imagen, 430, 700, 150, 150, preserveAspectRatio=True)
    #log_imagen = '/home/franklin/YURAKU/static/AdminLTE-2.4.2/img/reporte/hoja.png'
    log_imagen = 'D:/Tesis/YURAKU/static/AdminLTE-2.4.2/img/reporte/hoja.png'
    # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
    pdf.drawImage(log_imagen, 30, 740, 50, 50, preserveAspectRatio=True)
    #
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(480, 745, str(date.today()))
    pdf.line(460, 757, 560, 757)
    # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Helvetica", 16)
    # Dibujamos una cadena en la ubicación X,Y especificada
    pdf.drawString(250, 790, u"REPORTE")
    # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Helvetica", 12)
    pdf.drawString(241, 775, u"MEMORAMA")
    #aqui
    # Creamos una tupla de encabezados para neustra tabla
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10

    usuario = Paragraph('''Usuario''', styleBH)
    nombre_j = Paragraph('''Nombre del Juego''', styleBH)
    aciertos = Paragraph('''Aciertos''', styleBH)
    intentos = Paragraph('''Intentos''', styleBH)
    tiempo = Paragraph('''Tiempo de Juego''', styleBH)

    data = [[usuario, nombre_j, aciertos, intentos, tiempo]]

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleN.fontSize = 7

    width, height = A4
    high = 700
    for jueg in Juego.objects.all().filter(Usuario_id=usuario_id, nombre_juego="Memorama"):
        this_jueg = [str(jueg.Usuario_id.first_name) + " " + str(jueg.Usuario_id.last_name), jueg.nombre_juego,
                     jueg.aciertos, jueg.intentos, jueg.tiempo]
        data.append(this_jueg)
        high = high - 18

    width, height = A4
    table = Table(data, colWidths=[4.9 * cm, 6.5 * cm, 1.9 * cm, 2 * cm, 4 * cm, 5 * cm])
    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    # Establecemos el tamaño de la hoja que ocupará la tabla
    table.wrapOn(pdf, width, height)
    # Definimos la coordenada donde se dibujará la tabla
    table.drawOn(pdf, 30, high)
    # Con show page hacemos un corte de página para pasar a la siguiente
    pdf.showPage()
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

"""
    Clase ReportePersonasPDF
    Clase creada para generar reportes de todos los juegos con todos los uruarios que hayan jugado.
        Parametro
        View: para generar una vista basica para los reportes.

        Funcion cabecera
        Funcion creada para generar la cabecera que tendra el reporte. 
        En esta parte se le agrega una imagen, posicion, tamaño de la imagne, estilo de letra para el titulo y para todo el texto del reporte..
            Parametro
            self:  es un objeto instanciado de esa clase ReportePersonasPDF invocando por esta funcion.
            pdf: objeto que representa el reporte en conrdenadas X y Y.

        Funcion tabla
        Funcion creada para generar el cuerpo de la tabla que tendra el reporte. 
        En esta parte se le agrega el encabezado, se le asigna estilos y datos al encabezado, se le coloca los datos en la tabla y se define las cordenadas que ocupara dicha tabla.
            Parametro
            self:  es un objeto instanciado de esa clase ReportePersonasPDF invocando por esta funcion.
            pdf: objeto que representa el reporte en conrdenadas X y Y.

        Funcion get
        Funcion creada para generar el pdf y llamar a las funciones anteriores (cabecera y tabla) para compeltar el proceso.
        En esta funcion se le indica que tipo de archivo va a generar, se le asigna el estilo de la hoja, se le configura para que en caso de compeltar
        una hoja pase a la siguente los datos, retornado un archivo pdf con el response.
            Parametros
        	self: es un objeto instanciado de esa clase ReportePersonasPDF invocando por esta funcion.
        	request: para manejar las peticiones HTTP, FTP.
        	*args: se usa para enviar una lista de argumentos de longitud variable sin palabras clave a la función. 
        	**kwargs: permite pasar una longitud variable de argumentos con palabras clave a una función. Debe usar ** kwargs si desea manejar argumentos con nombre en una función. 
"""
# Reportes de todos los juego
class ReportePersonasPDF(View):

    def cabecera(self, pdf):
        # cabecera
        pdf.setLineWidth(.3)
        # Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        #archivo_imagen = '/home/franklin/YURAKU/static/AdminLTE-2.4.2/img/reporte/logo.png'
        archivo_imagen = 'D:/Tesis/YURAKU/static/AdminLTE-2.4.2/img/reporte/logo.png'
        # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 430, 700, 150, 150, preserveAspectRatio=True)
        #log_imagen = '/home/franklin/YURAKU/static/AdminLTE-2.4.2/img/reporte/hoja.png'
        log_imagen = 'D:/Tesis/YURAKU/static/AdminLTE-2.4.2/img/reporte/hoja.png'
        # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(log_imagen, 30, 740, 50, 50, preserveAspectRatio=True)
        #
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(480, 745, str(date.today()))
        pdf.line(460, 757, 560, 757)
        # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 16)
        # Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(210, 790, u"REPORTE DE JUEGOS")
        # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 16)

    def tabla(self, pdf):
        # Creamos una tupla de encabezados para neustra tabla
        styles = getSampleStyleSheet()
        styleBH = styles["Normal"]
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10

        usuario = Paragraph('''Usuario''', styleBH)
        nombre_j = Paragraph('''Nombre del Juego''', styleBH)
        aciertos = Paragraph('''Aciertos''', styleBH)
        intentos = Paragraph('''Intentos''', styleBH)
        tiempo = Paragraph('''Tiempo de Juego''', styleBH)

        data = [[usuario, nombre_j, aciertos, intentos, tiempo]]

        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7

        width, height = A4
        high = 700
        for jueg in Juego.objects.all():
            this_jueg = [str(jueg.Usuario_id.first_name) +" "+ str(jueg.Usuario_id.last_name), jueg.nombre_juego, jueg.aciertos, jueg.intentos, jueg.tiempo]
            data.append(this_jueg)
            high = high - 18

        width, height = A4
        table = Table(data, colWidths=[4.9 * cm, 6.5 * cm, 1.9 * cm, 2 * cm, 4 * cm, 5 * cm])
        table.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        # Establecemos el tamaño de la hoja que ocupará la tabla
        table.wrapOn(pdf, width, height)
        # Definimos la coordenada donde se dibujará la tabla
        table.drawOn(pdf, 30, high)

    def get(self, request, *args, **kwargs):
        # Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        # La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        # Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer, pagesize=A4)
        # Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        self.tabla(pdf)
        # Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

"""
    Funcion agregar_record_adivina
    Funcion creada para guardar los record de los usuarios que juege el Adivina la Palabra siempre y cuando este iniciado sesion y retorna a la misma pagina.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
#Guardar Record Adivina
@login_required
def agregar_record_adivina(request):
    message=None
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    plantas = Planta.objects.all().order_by('id')
    palabras = []
    palabrasimagen = []
    palabrasnc = []
    palabrasc = []
    for p in range(len(plantas)):
        if ' ' in plantas[p].nombre_planta:
            palabrasc.append(plantas[p].nombre_planta)
        else:
            a, b = 'áéíóúüñ', 'aeiouun'
            trans = str.maketrans(a, b)
            palabras.append(plantas[p].nombre_planta.translate(trans))
            palabrasimagen.append(plantas[p].imagen_planta.name)
            palabrasnc.append(plantas[p].nombre_cientifico)
    tamanio = (len(palabras))
    if request.method == 'POST':
        form = GuardarJuegoForm(request.POST)
        usuario = User.objects.get(id=request.user.id)
        if form.is_valid():
            juego = form.save(commit=False)
            juego.Usuario_id=usuario
            juego.save()
            print(palabrasimagen)
            return render(request, 'juego/adivina.html',
                          {'perfiles': perfiles, 'palabras': palabras, 'palabrasimagen': palabrasimagen,
                           'palabrasnc': palabrasnc, 'tamanio': tamanio})
        else:
            form = GuardarJuegoForm(request.POST)
            return render(request, 'juego/adivina.html',
                          {'perfiles': perfiles, 'palabras': palabras, 'palabrasimagen': palabrasimagen,
                           'palabrasnc': palabrasnc, 'tamanio': tamanio})
    else:
        form = GuardarJuegoForm()
        print(palabrasimagen)
    return render(request, 'juego/adivina.html',
                  {'perfiles': perfiles, 'palabras': palabras, 'palabrasimagen': palabrasimagen,
                   'palabrasnc': palabrasnc, 'tamanio': tamanio})

"""
    Funcion agregar_record_sopa
    Funcion creada para guardar los record de los usuarios que juege la Sopa de Letras siempre y cuando este iniciado sesion y retorna a la misma pagina.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
#Guardar Sopa de Letras
@login_required
def agregar_redord_sopa(request):
    message = None
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    plantas = Planta.objects.all().order_by('id')
    palabras = []
    palabrasc = []
    for p in range(len(plantas)):
        if ' ' in plantas[p].nombre_planta:
            palabrasc.append(plantas[p].nombre_planta)
        else:
            palabras.append(plantas[p].nombre_planta)
    if request.method == 'POST':
        form = GuardarJuegoForm(request.POST)
        usuario = User.objects.get(id=request.user.id)
        if form.is_valid():
            juego = form.save(commit=False)
            juego.Usuario_id = usuario
            juego.save()
            # form = GuardarJuegoForm()
            return render(request, 'juego/sopa_de_letras.html',
                          {'palabras': palabras, 'perfiles': perfiles})
        else:
            form = GuardarJuegoForm(request.POST)
            return render(request, 'juego/sopa_de_letras.html',
                          {'palabras': palabras, 'perfiles': perfiles})
    else:
        form = GuardarJuegoForm()
    return render(request, 'juego/sopa_de_letras.html',
                  {'palabras': palabras, 'perfiles': perfiles})

"""
    Funcion agregar_record_memorama
    Funcion creada para guardar los record de los usuarios que juege el Memorama siempre y cuando este iniciado sesion y retorna a la misma pagina.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
#Guardar Record Memorama
@login_required
def agregar_redord_memorama(request):
    message = None
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    if request.method == 'POST':
        form = GuardarJuegoForm(request.POST)
        usuario = User.objects.get(id=request.user.id)
        if form.is_valid():
            juego = form.save(commit=False)
            juego.Usuario_id = usuario
            juego.save()
            # form = GuardarJuegoForm()
            return render(request, 'juego/memorama.html',
                          {'perfiles': perfiles})
        else:
            form = GuardarJuegoForm(request.POST)
            return render(request, 'juego/memorama.html',
                          {'perfiles': perfiles})
    else:
        form = GuardarJuegoForm()
    return render(request, 'juego/memorama.html',
                  {'perfiles': perfiles})

"""
    Funcion ranking_adivina
    Funcion creada para obtener las posiciones que tienen los usuarios que jugaron el Adivina la Palabra y retorna a la misma pagina con dichos datos.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
#ranklin de Juego Adivina
def ranking_adivina(request):
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    ranking = Juego.objects.all().order_by('aciertos','-tiempo').reverse().filter(nombre_juego="Adivina la Planta")
    return render(request, 'reporte/ranking.html', {'ranking': ranking, 'perfiles': perfiles})

"""
    Funcion ranking_sopa
    Funcion creada para obtener las posiciones que tienen los usuarios que jugaron la Sopa de Letras y retorna a la misma pagina con dichos datos.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
#ranklin de Juego Sopa de Letras
def ranking_sopa(request):
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    ranking = Juego.objects.all().order_by('aciertos','-tiempo').reverse().filter(nombre_juego="Sopa de Letras")
    return render(request, 'reporte/ranking.html', {'ranking': ranking, 'perfiles': perfiles})

"""
    Funcion ranking_memorama
    Funcion creada para obtener las posiciones que tienen los usuarios que jugaron el Memorama y retorna a la misma pagina con dichos datos.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
"""
#ranklin de Juego Memorama
def ranking_memorama(request):
    if request.user.id:
        usuario = User.objects.get(id=request.user.id)
        id = usuario.id
        perfiles = Perfil.objects.filter(Usuario_id=id)
        if len(perfiles) > 0:
            perfiles = Perfil.objects.filter(Usuario_id=id)
        else:
            perfiles = []
    else:
        perfiles = Perfil.objects.all()
    ranking = Juego.objects.all().order_by('aciertos','-tiempo').reverse().filter(nombre_juego="Memorama")
    return render(request, 'reporte/ranking.html', {'ranking': ranking, 'perfiles': perfiles})

"""
    Funcion eliminar_ranking_adivina
    Funcion creada para eliminar un registro de un cualquier juego que le usuario quiera eliminar simpre y cuando este iniciado sesion y retorna a la misma pagina con las posiciones actualizadas.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        juego_id: para encontrar los datos del juego que se quiere eliminar
"""
#Eliminar Ranking
@login_required
def eliminar_ranking(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    if juego.nombre_juego == "Adivina la Planta":
        juego.delete()
        return redirect('Ranking_Adivina')
    elif juego.nombre_juego == "Memorama":
        juego.delete()
        return redirect('Ranking_Memorama')
    else:
        juego.delete()
        return redirect('Ranking_Sopa')

"""
    Funcion eliminar_memorama_ranking
    Funcion creada para eliminar un registro del juego Memorama que le usuario quiera eliminar simpre y cuando este iniciado sesion y retorna a la misma pagina con las posiciones actualizadas.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        juego_id: para encontrar los datos del juego que se quiere eliminar
"""
#Eliminar Ranking Memorama
@login_required
def eliminar_memorama_ranking(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    juego.delete()
    print("Memorma")
    return redirect('juego_memorama')

"""
    Funcion eliminar_adivina_ranking
    Funcion creada para eliminar un registro del juego Adivina la Planta que le usuario quiera eliminar simpre y cuando este iniciado sesion y retorna a la misma pagina con las posiciones actualizadas.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        juego_id: para encontrar los datos del juego que se quiere eliminar
"""
#Eliminar Ranking Advina
@login_required
def eliminar_adivina_ranking(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    juego.delete()
    print("ADIVINA")
    return redirect('juego_adivina')

"""
    Funcion eliminar_sopa_sopa
    Funcion creada para eliminar un registro del juego Sopa de Letras que le usuario quiera eliminar simpre y cuando este iniciado sesion y retorna a la misma pagina con las posiciones actualizadas.
        Parametro
        request: para manejar las peticiones HTTP, FTP.
        juego_id: para encontrar los datos del juego que se quiere eliminar
"""
#Eliminar Ranking Sopa de Letras
@login_required
def eliminar_sopa_sopa_ranking(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    juego.delete()
    return redirect('juego_sopa_de_letras')