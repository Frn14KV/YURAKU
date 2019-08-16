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
from gestioncomentario.models import Comentario
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User

from gestionjuego.form import GuardarJuegoForm
from gestionjuego.models import Juego
from gestionperfil.models import Perfil
from gestionplantas.models import Planta

from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View


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
    archivo_imagen = 'D:/Tesis/TesisVF/static/AdminLTE-2.4.2/img/reporte/logo.png'
    # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
    pdf.drawImage(archivo_imagen, 430, 700, 150, 150, preserveAspectRatio=True)
    log_imagen = 'D:/Tesis/TesisVF/static/AdminLTE-2.4.2/img/reporte/hoja.png'
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
    archivo_imagen = 'D:/Tesis/TesisVF/static/AdminLTE-2.4.2/img/reporte/logo.png'
    # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
    pdf.drawImage(archivo_imagen, 430, 700, 150, 150, preserveAspectRatio=True)
    log_imagen = 'D:/Tesis/TesisVF/static/AdminLTE-2.4.2/img/reporte/hoja.png'
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
    archivo_imagen = 'D:/Tesis/TesisVF/static/AdminLTE-2.4.2/img/reporte/logo.png'
    # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
    pdf.drawImage(archivo_imagen, 430, 700, 150, 150, preserveAspectRatio=True)
    log_imagen = 'D:/Tesis/TesisVF/static/AdminLTE-2.4.2/img/reporte/hoja.png'
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


# Reportes
class ReportePersonasPDF(View):

    def cabecera(self, pdf):
        # cabecera
        pdf.setLineWidth(.3)
        # Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = 'D:/Tesis/TesisVF/static/AdminLTE-2.4.2/img/reporte/logo.png'
        # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 430, 700, 150, 150, preserveAspectRatio=True)
        log_imagen = 'D:/Tesis/TesisVF/static/AdminLTE-2.4.2/img/reporte/hoja.png'
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
        y = 580
        self.tabla(pdf)
        # Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


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
            palabrasimagen.append(plantas[p].imagen_planta)
            palabrasnc.append(plantas[p].nombre_cientifico)
    tamanio = (len(palabras))
    if request.method == 'POST':
        form = GuardarJuegoForm(request.POST)
        usuario = User.objects.get(id=request.user.id)
        if form.is_valid():
            juego = form.save(commit=False)
            juego.Usuario_id=usuario
            juego.save()
            #form = GuardarJuegoForm()
            return render(request, 'juego/adivina.html',
                          {'perfiles': perfiles, 'palabras': palabras, 'palabrasimagen': palabrasimagen,
                           'palabrasnc': palabrasnc, 'tamanio': tamanio})
        else:
            form = GuardarJuegoForm(request.POST)
            message = "datos faltantes para registrar la Escuela"
            return render(request, 'juego/adivina.html',
                          {'perfiles': perfiles, 'palabras': palabras, 'palabrasimagen': palabrasimagen,
                           'palabrasnc': palabrasnc, 'tamanio': tamanio})
    else:
        form = GuardarJuegoForm()
    return render(request, 'juego/adivina.html',
                  {'perfiles': perfiles, 'palabras': palabras, 'palabrasimagen': palabrasimagen,
                   'palabrasnc': palabrasnc, 'tamanio': tamanio})


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
            message = "datos faltantes para registrar la Escuela"
            return render(request, 'juego/sopa_de_letras.html',
                          {'palabras': palabras, 'perfiles': perfiles})
    else:
        form = GuardarJuegoForm()
    return render(request, 'juego/sopa_de_letras.html',
                  {'palabras': palabras, 'perfiles': perfiles})


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
            message = "datos faltantes para registrar la Escuela"
            return render(request, 'juego/memorama.html',
                          {'perfiles': perfiles})
    else:
        form = GuardarJuegoForm()
    return render(request, 'juego/memorama.html',
                  {'perfiles': perfiles})


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


#Eliminar Comentario
@login_required
def eliminar_ranking_adivina(request, juego_id):
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

