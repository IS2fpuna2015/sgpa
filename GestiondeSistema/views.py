from io import BytesIO
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, Spacer
from GestiondeProyectos.models import Proyecto
from GestiondeSistema.models import Sistema
from GestiondeSprints.models import Sprint
from GestiondeUserStories.models import UserStory
from .forms import Busqueda_Auditoria_form
from GestiondeUsuarios.models import Usuario
from sgpa.Util import cabecera_alpie, NumberedCanvas
import time

@login_required(login_url="/login/")
def home(request):
    """
    Redirecciona a la pagina principal al usuario, es necesario estar logueado
    :param request:
    :return:
    """
    usuario = Usuario.objects.get(id=request.user.id)
    return render_to_response("Sistema/principal.html",{'usuario':usuario} ,context_instance=RequestContext(request))


def login_view(request):
    """
    Redirecciona a la interfaz de logueo y obtiene los parametros del usuario para verificar
    :param request:
    :return:
    """
    username = password = ''
    status = "valido"
    if request.POST and 'Entrar' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                Sistema().registrar("Ingreso al sistema el usuario "+ username+" ",request.user.username,"none")
                return HttpResponseRedirect('/home/')
            else:
                status = "no activo"
                return render_to_response('Sistema/login.html', {'username': username, 'status': status},
                                          context_instance=RequestContext(request))
        else:
            status = "invalido"
            return render_to_response('Sistema/login.html', {'username': username, 'status': status},
                                      context_instance=RequestContext(request))
    if request.POST and 'olvide' in request.POST:
        status = "olvide"
        return render_to_response('Sistema/login.html', {'status': status},
                                      context_instance=RequestContext(request))

    return render_to_response('Sistema/login.html', {'username': username, 'status': status},
                              context_instance=RequestContext(request))


def logout_view(request):
    """
    Redirecciona al usuario a la interfaz de logueo cerrando la sesion
    :param request:
    :return:
    """
    Sistema().registrar("Salio del sistema el usuario "+ request.user.username+" ",request.user.username,"none")
    logout(request)
    return render_to_response("Sistema/login.html", locals(), context_instance=RequestContext(request))

@login_required(login_url="/login/")
def visualizar_auditoria_view(request):
    """
    Redirecciona a la pagina para visualizar los registros almacenados en auditoria
    :param request:
    :return:
    """

    if request.method == 'POST':
        form = Busqueda_Auditoria_form(request.POST)
        if form.is_valid():
            try:
                busqueda = form.cleaned_data.get('Busqueda')
                elementos = Sistema.objects.filter(nombre_usuario=busqueda)
                return render_to_response("Sistema/ver_auditoria.html",{'elementos':elementos,'form':form} ,context_instance=RequestContext(request))
            except:
                pass

    form = Busqueda_Auditoria_form()
    elementos = Sistema.objects.all().order_by('hora_dia')
    return render_to_response("Sistema/ver_auditoria.html",{'elementos':elementos,'form':form} ,context_instance=RequestContext(request))


@login_required(login_url="login")
def reporte_product_backlog_pdf_view(request,id_proyecto):
    """
    Genera un reporte en pdf sobre el product backlog del proyecto seleccionado
    :param request:
    :return:
    """
    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)
    userstories = UserStory.objects.filter(proyecto=proyecto_seleccionado)

    response = HttpResponse(content_type='application/pdf')
    buff = BytesIO()

    doc = SimpleDocTemplate(buff, pagesize=A4)
    story=[]

    tituloStyle = ParagraphStyle(name='Titulo', fontName='Helvetica-Bold', fontSize=16, alignment=TA_CENTER,leading=32)
    paraStyle = ParagraphStyle(name='Contenido',fontName='Helvetica', fontSize=13 ,alignment=TA_CENTER,leading=32)
    titulo = Paragraph("Informe de Product Backlog del Producto: " + proyecto_seleccionado.nombre_proyecto,tituloStyle)
    fecha_generado = Paragraph("Fecha: "+time.strftime("%d/%m/%Y"),paraStyle)
    story.append(Spacer(2, 15))
    story.append(fecha_generado)
    story.append(titulo)

    if len(userstories):
        datos = []
        datos.append(['Nombre','Responsable','Prioridad','Estado','H. Trabajadas','% Realizado'])
        for us in userstories:
            temp = []
            temp.append(us.nombre)
            temp.append(us.usuario_asignado)
            temp.append(us.prioridad)
            temp.append(us.estado)
            temp.append(us.horas_dedicadas)
            temp.append(us.porcentaje_realizado)
            datos.append(temp)

        tabla = Table(data=datos,
                      style=[
                          ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                          ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                      ]
        )
        story.append(tabla)
        story.append(Spacer(2, 15))
    else:
        texto = Paragraph("No se encontraron User Stories pertenecientes al Proyecto.",paraStyle)
        story.append(texto)

    doc.build(story, onFirstPage=cabecera_alpie, canvasmaker=NumberedCanvas)
    response.write(buff.getvalue())
    buff.close()

    return response

@login_required(login_url="login")
def reporte_sprint_backlog_pdf_view(request,id_sprint):
    """
    Genera un reporte en pdf sobre el product backlog del proyecto seleccionado
    :param request:
    :return:
    """
    sprint_seleccionado = Sprint.objects.get(pk=id_sprint)
    id_proyecto = sprint_seleccionado.id_proyecto
    userstories = UserStory.objects.filter(proyecto=id_proyecto).filter(nombre_sprint=sprint_seleccionado.nombre_sprint)


    response = HttpResponse(content_type='application/pdf')
    buff = BytesIO()

    doc = SimpleDocTemplate(buff, pagesize=A4)
    story=[]

    tituloStyle = ParagraphStyle(name='Titulo', fontName='Helvetica-Bold', fontSize=16, alignment=TA_CENTER,leading=32)
    paraStyle = ParagraphStyle(name='Contenido',fontName='Helvetica', fontSize=13 ,alignment=TA_CENTER,leading=32)
    titulo = Paragraph("Informe de Sprint Backlog del Sprint: " + sprint_seleccionado.nombre_sprint,tituloStyle)
    fecha_generado = Paragraph("Fecha: "+time.strftime("%d/%m/%Y"),paraStyle)
    story.append(Spacer(2, 15))
    story.append(fecha_generado)
    story.append(titulo)

    if len(userstories):
        datos = []
        datos.append(['Nombre','Responsable','Prioridad','Estado','H. Trabajadas','% Realizado'])
        for us in userstories:
            temp = []
            temp.append(us.nombre)
            temp.append(us.usuario_asignado)
            temp.append(us.prioridad)
            temp.append(us.estado)
            temp.append(us.horas_dedicadas)
            temp.append(us.porcentaje_realizado)
            datos.append(temp)

        tabla = Table(data=datos,
                      style=[
                          ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                          ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                      ]
        )
        story.append(tabla)
        story.append(Spacer(2, 15))
    else:
        texto = Paragraph("No se encontraron User Stories Asignados al Sprint",paraStyle)
        story.append(texto)

    doc.build(story, onFirstPage=cabecera_alpie,canvasmaker=NumberedCanvas)
    response.write(buff.getvalue())
    buff.close()

    return response