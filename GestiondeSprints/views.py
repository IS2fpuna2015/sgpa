from io import BytesIO

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Sprint
from .forms import sprint_form, Busqueda_sprint_form, modificar_sprint_form
from GestiondeProyectos.models import Proyecto
from GestiondeSistema.models import Sistema
from GestiondeUserStories.models import UserStory
from GestiondeUsuarios.models import Usuario
from GestiondeProyectos.forms import Proyecto_Buscar_form
from GestiondeFlujos.models import Flujo
from GestiondeFlujos.models import Actividad
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle,TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, cm
from sgpa.settings import MEDIA_URL
from reportlab.graphics.shapes import Drawing
from reportlab.platypus import *
from GestiondeBurndownChart.models import BurndownChartProyecto


@login_required(login_url="/login/")
def crear_sprint_view(request, id_proyecto):
    """
    Permite la creacion de un sprint de limitando a un proyecto en especifico
    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST' and 'Guardar' in request.POST:
        formulario = sprint_form(request.POST)
        if formulario.is_valid():
            nombre_sprint_temp = request.POST.get('nombre_sprint')
            fecha_inicio_temp = request.POST.get('fecha_inicio')
            fecha_fin_temp = request.POST.get('fecha_fin')


            #Se controla que la fecha de inicio del sprint sea menor  a la fecha de fin del sprint
            if control_fecha(fecha_inicio_temp,fecha_fin_temp) == False:
                context = {'formulario': formulario, 'nro_sprint': proyecto_seleccionado.cantidad_sprints+1,'nombre_proyecto': proyecto_seleccionado.nombre_proyecto, 'error': 'fechas'}
                return render(request, 'Gestion_de_sprints/crear_sprint.html', context)

            #Se controla que la fecha de inicio del sprint sea menor a la fecha de fin del proyecto
            if control_fecha(fecha_inicio_temp, str(proyecto_seleccionado.fecha_finalizacion)) == False:
                context = {'formulario': formulario, 'nro_sprint': proyecto_seleccionado.cantidad_sprints+1,'nombre_proyecto': proyecto_seleccionado.nombre_proyecto, 'error': 'finalizacion_proyecto'}
                return render(request, 'Gestion_de_sprints/crear_sprint.html', context)

            #Se controla que la fecha de inicio del sprint sea superior a la fecha de inicio del proyecto
            if control_fecha(str(proyecto_seleccionado.fecha_inicio),fecha_inicio_temp) == False:
                context = {'formulario': formulario, 'nro_sprint': proyecto_seleccionado.cantidad_sprints+1,'nombre_proyecto': proyecto_seleccionado.nombre_proyecto, 'error': 'inicio_proyecto'}
                return render(request, 'Gestion_de_sprints/crear_sprint.html', context)

            #Se controla que la fecha de fin del sprint sea menor a la fecha de fin del proyecto
            if control_fecha(fecha_fin_temp, str(proyecto_seleccionado.fecha_finalizacion)) == False:
                context = {'formulario': formulario, 'nro_sprint': proyecto_seleccionado.cantidad_sprints+1,'nombre_proyecto': proyecto_seleccionado.nombre_proyecto, 'error': 'fin_proyecto'}
                return render(request, 'Gestion_de_sprints/crear_sprint.html', context)


            try:
                #Si ya existe un sprint con este nombre y en el mismo proyecto no va a explotar, quiere decir que esta mal, si no existe se puede guardar
                sprint_prueba = Sprint.objects.get(nombre_sprint=nombre_sprint_temp,id_proyecto_id=id_proyecto)
                context = {'formulario': formulario, 'nro_sprint': proyecto_seleccionado.cantidad_sprints+1,
                       'nombre_proyecto': proyecto_seleccionado.nombre_proyecto, 'error': 'nombre'}
                return render(request, 'Gestion_de_sprints/crear_sprint.html', context)
            except:
                pass


            numero_sprint = proyecto_seleccionado.cantidad_sprints + 1
            sprint = Sprint(nombre_sprint=nombre_sprint_temp, fecha_inicio=fecha_inicio_temp, fecha_fin=fecha_fin_temp,
                            id_proyecto=proyecto_seleccionado,numero_sprint=numero_sprint)
            sprint.estado = "Pendiente"
            sprint.save()
            proyecto_seleccionado.cantidad_sprints+=1
            proyecto_seleccionado.save()

            Sistema().registrar("Creado Sprint " + sprint.nombre_sprint , request.user.username,  "Ninguno")
            redireccion = reverse('listar_sprint', args=[id_proyecto])
            return HttpResponseRedirect(redireccion)
        else:
            context = {'formulario': formulario, 'nro_sprint': proyecto_seleccionado.cantidad_sprints+1,
                       'nombre_proyecto': proyecto_seleccionado.nombre_proyecto, 'error': 'camposobligatorios'}
            return render(request, 'Gestion_de_sprints/crear_sprint.html', context)

    formulario = sprint_form()
    context = {'formulario': formulario, 'nro_sprint': proyecto_seleccionado.cantidad_sprints+1,
               'nombre_proyecto': proyecto_seleccionado.nombre_proyecto}
    return render_to_response("Gestion_de_sprints/crear_sprint.html", context, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def listar_sprint_view(request, id_proyecto):
    """
    Redirige al usuario a la pantalla de listar los sprints que se encuentran en un determinado proyecto
    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)
    formulario = Busqueda_sprint_form()
    if request.method == 'POST':
        formulario = Busqueda_sprint_form(request.POST)

        if formulario.is_valid():
            busqueda = formulario.cleaned_data.get('Busqueda')
            if busqueda == '':
                sprints = Sprint.objects.filter(id_proyecto=id_proyecto)
                context = {'formulario': formulario, 'sprints': sprints, 'id_proyecto': id_proyecto,
                           'nombre_proyecto': proyecto_seleccionado.nombre_proyecto}
                return render(request, 'Gestion_de_sprints/listar_sprint.html', context)
            else:
                sprints = Sprint.objects.filter(id_proyecto=id_proyecto).filter(nombre_sprint=busqueda)
                context = {'formulario': formulario, 'sprints': sprints, 'id_proyecto': id_proyecto,
                           'nombre_proyecto': proyecto_seleccionado.nombre_proyecto}
                return render(request, 'Gestion_de_sprints/listar_sprint.html', context)

    sprints = Sprint.objects.filter(id_proyecto=id_proyecto)
    context = {'formulario': formulario, 'sprints': sprints, 'id_proyecto': id_proyecto,
               'nombre_proyecto': proyecto_seleccionado.nombre_proyecto}
    return render(request, 'Gestion_de_sprints/listar_sprint.html', context)


@login_required(login_url="/login/")
def consultar_sprint_view(request, id_proyecto, id_sprint):
    """
    Permite realizar la consulta de un sprint en especifico
    :param request:
    :return:
    """

    sprint_seleccionado = Sprint.objects.get(pk=id_sprint)
    user_stories = UserStory.objects.filter(nombre_sprint=sprint_seleccionado.nombre_sprint)
    return render_to_response("Gestion_de_sprints/consultar_sprint.html",
                              {"sprint": sprint_seleccionado, "id_proyecto": id_proyecto, "id_sprint": id_sprint,"userStories":user_stories},
                              context_instance=RequestContext(request))

@login_required(login_url="/login/")
def modificar_sprint_view(request, id_proyecto, id_sprint):
    """
    Permite la modificacion de ciertos atributos que posee un sprint que es especificado por el id id_sprint
    y pertenece al proyecto con id id_proyecto
    :param request:
    :param id_proyecto:
    :param id_sprint:
    :return:
    """
    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)
    sprint_seleccionado = Sprint.objects.get(pk=id_sprint)
    estado_inicial = sprint_seleccionado.estado
    numero_de_sprint = sprint_seleccionado.numero_sprint

    if request.method == 'POST' and 'Guardar' in request.POST:
        formulario = modificar_sprint_form(request.POST, instance=sprint_seleccionado)
        if formulario.is_valid():
            fecha_inicio_temp = request.POST.get('fecha_inicio')
            fecha_fin_temp = request.POST.get('fecha_fin')

            #Se controlara que no existan 2 sprint con estados activos
            if request.POST.get('estado').upper() == "ACTIVO":
                otros_activos = Sprint.objects.filter(id_proyecto_id=id_proyecto ,estado="Activo")

                if(len(otros_activos) > 0):
                    error = "activo"
                    context = {'formulario': formulario, 'proyecto': proyecto_seleccionado,'nombre_proyecto': proyecto_seleccionado.nombre_proyecto, 'error': error,'sprint': sprint_seleccionado}
                    return render(request, 'Gestion_de_sprints/modificar_sprint.html', context)


            #Se controla que la fecha de inicio del sprint sea menor  a la fecha de fin del sprint
            if control_fecha(fecha_inicio_temp,fecha_fin_temp) == False:
                context = {'formulario': formulario, 'proyecto': proyecto_seleccionado,'nombre_proyecto': proyecto_seleccionado.nombre_proyecto, 'error': 'fechas','sprint': sprint_seleccionado}
                return render(request, 'Gestion_de_sprints/modificar_sprint.html', context)

            #Se controla que la fecha de inicio del sprint sea menor a la fecha de fin del proyecto
            if control_fecha(fecha_inicio_temp, str(proyecto_seleccionado.fecha_finalizacion)) == False:
                context = {'formulario': formulario, 'proyecto': proyecto_seleccionado,'nombre_proyecto': proyecto_seleccionado.nombre_proyecto,'error': 'finalizacion_proyecto', 'sprint': sprint_seleccionado}
                return render(request, 'Gestion_de_sprints/modificar_sprint.html', context)

            #Se controla que la fecha de inicio del sprint sea superior a la fecha de inicio del proyecto
            if control_fecha(str(proyecto_seleccionado.fecha_inicio),fecha_inicio_temp) == False:
                context = {'formulario': formulario, 'proyecto': proyecto_seleccionado,'nombre_proyecto': proyecto_seleccionado.nombre_proyecto,'error': 'inicio_proyecto', 'sprint': sprint_seleccionado}
                return render(request, 'Gestion_de_sprints/modificar_sprint.html', context)

            #Se controla que la fecha de fin del sprint sea menor a la fecha de fin del proyecto
            if control_fecha(fecha_fin_temp, str(proyecto_seleccionado.fecha_finalizacion)) == False:
                context = {'formulario': formulario, 'proyecto': proyecto_seleccionado,'nombre_proyecto': proyecto_seleccionado.nombre_proyecto,'error': 'fin_proyecto', 'sprint': sprint_seleccionado}
                return render(request, 'Gestion_de_sprints/modificar_sprint.html', context)

            #Se controla que no vuelva a un estado pendiente si posee un estado activo
            if estado_inicial.upper() == "ACTIVO" and request.POST.get('estado').upper() == "PENDIENTE":
                context = {'formulario': formulario, 'proyecto': proyecto_seleccionado,'nombre_proyecto': proyecto_seleccionado.nombre_proyecto,'error': 'estado', 'sprint': sprint_seleccionado}
                return render(request, 'Gestion_de_sprints/modificar_sprint.html', context)

            #Se controla que no vuelva a un estado pendiente si posee un estado activo
            if estado_inicial.upper() != "ACTIVO" and request.POST.get('estado').upper() == "FINALIZADO":
                context = {'formulario': formulario, 'proyecto': proyecto_seleccionado,'nombre_proyecto': proyecto_seleccionado.nombre_proyecto,'error': 'estado_salteado', 'sprint': sprint_seleccionado}
                return render(request, 'Gestion_de_sprints/modificar_sprint.html', context)


            #Se reasignara los US si se cambia a estado finalizado
            if request.POST.get('estado').upper() == "FINALIZADO":
                equipo =  Usuario.objects.filter(equipo_desarrollo=sprint_seleccionado.id_proyecto_id)
                uss = list(UserStory.objects.filter(nombre_sprint=sprint_seleccionado.nombre_sprint))
                ultima_actividad = []
                completados_todos = True
                mayor_size = 0
                error = "Ninguno"
                us_no_finalizados = []
                porcentaje_total = 100
                horas_en_un_dia = 12
                for us in uss:
                    if us.porcentaje_realizado < porcentaje_total:
                        completados_todos = False
                        us_no_finalizados.append(us)
                        ultima_actividad.append(Actividad.objects.get(id=us.id_actividad or 0))

                        try:
                            #Se realiza en un try porque us.horas_dedicadas puede ser 0
                            dias_trabajados = horas_en_un_dia/us.horas_dedicadas
                        except:
                            dias_trabajados = 0

                        dias_restantes = us.size - dias_trabajados
                        if dias_restantes > mayor_size:
                            mayor_size = dias_restantes

                uss = us_no_finalizados
                lista = zip(uss,ultima_actividad)

                if completados_todos == False:
                    #existen US que no finalizaron
                    try:
                        prox_sprint = Sprint.objects.get(numero_sprint=numero_de_sprint+1)
                        for us in uss:
                            if us.porcentaje_realizado < porcentaje_total:
                                us.nombre_sprint = prox_sprint.nombre_sprint
                                us.save()

                        formulario.save()
                        Sistema().registrar("Modificado Sprint " + sprint_seleccionado.nombre_sprint , request.user.username,  "Ninguno")

                        context = {'equipo':equipo,'lista':lista,'prox_sprint':prox_sprint,'error':error,'mayor_size':mayor_size}
                    except:
                        error = "falta_sprint"
                        context = {'equipo':equipo,'lista':lista,'error':error,'mayor_size':mayor_size}

                    return render(request,'Gestion_de_sprints/reasignacion_de_us.html',context)
                if completados_todos == True:
                    formulario.save()
                    Sistema().registrar("Modificado Sprint " + sprint_seleccionado.nombre_sprint , request.user.username,  "Ninguno")
                    redireccion = reverse('listar_sprint', args=[id_proyecto])
                    return HttpResponseRedirect(redireccion)

            formulario.save()
            Sistema().registrar("Modificado Sprint " + sprint_seleccionado.nombre_sprint , request.user.username,  "Ninguno")
            redireccion = reverse('listar_sprint', args=[id_proyecto])
            return HttpResponseRedirect(redireccion)
        else:
            context = {'formulario': formulario, 'proyecto': proyecto_seleccionado,
                        'nombre_proyecto': proyecto_seleccionado.nombre_proyecto, 'error': 'camposobligatorios',
                        'sprint': sprint_seleccionado}
            return render(request, 'Gestion_de_sprints/modificar_sprint.html', context)

    formulario = modificar_sprint_form(instance=sprint_seleccionado)
    context = {'formulario': formulario, 'proyecto': proyecto_seleccionado, 'error': 'ninguno',
                   'sprint': sprint_seleccionado}
    return render_to_response("Gestion_de_sprints/modificar_sprint.html", context,
                                  context_instance=RequestContext(request))


def control_fecha(fecha_menor,fecha_mayor):
    """
    Funcion para determinar si verdaderamente el atributo que viene en el parametro fecha_menor
    es menor al de fecha_mayor
    :param fecha_menor:
    :param fecha_mayor:
    :return:
    """
    if fecha_mayor >=  fecha_menor:
        return True
    else:
        return False




@login_required(login_url="/login/")
def eliminar_sprint_view(request, id_proyecto, id_sprint):
    """
    Permite la eliminacion de un sprint especificado en el id_sprint perteneciente al
    proyecto con id id_proyecto
    :param request:
    :param id_proyecto:
    :param id_sprint:
    :return:
    """
    sprint_seleccionado = Sprint.objects.get(pk=id_sprint)
    nombre = sprint_seleccionado.nombre_sprint

    if request.method == 'POST' and 'Aceptar' in request.POST:
        sprint_seleccionado.delete()
        Sistema().registrar("Eliminado sprint " + nombre, request.user.username, "Ninguno")
        redireccion = reverse('listar_sprint', args=[id_proyecto])
        return HttpResponseRedirect(redireccion)
    if request.method == 'POST' and 'Cancelar' in request.POST:
        redireccion = reverse('listar_sprint', args=[id_proyecto])
        return HttpResponseRedirect(redireccion)

    return render(request, "Gestion_de_sprints/eliminar_sprint.html", {'nombre': nombre})

@login_required(login_url="/login/")
def asignar_user_story_a_sprint(request, id_sprint):
    """
    Permite realizar al usuario con los permisos adecuados la asignacion de un US a un Sprint
    :param request:
    :param id_userStory:
    :param id_proyecto:
    :return:
    """
    error="ninguno"
    sprint = Sprint.objects.get(id=id_sprint)
    fecha  = sprint.fecha_fin - sprint.fecha_inicio
    userStories = UserStory.objects.filter(proyecto_id=sprint.id_proyecto,nombre_sprint='No Asignado').order_by('prioridad')
    userStories_copy = list(userStories)


    #Se agregara a la lista los US que fueron reasignados en sprints anteriores
    userReasignados = UserStory.objects.filter(proyecto_id=sprint.id_proyecto,nombre_sprint=sprint.nombre_sprint)
    for us in userReasignados:
        userStories_copy.append(us)

    userStories = userStories_copy

    proyecto = Proyecto.objects.get(id=sprint.id_proyecto.id)
    usuario_equipo =  Usuario.objects.filter(equipo_desarrollo=proyecto.id)
    flujos = Flujo.objects.filter(id_Proyecto_id=proyecto.id)


    if request.method == 'POST' and "Volver" in request.POST:
        redireccion = reverse('listar_todos_sprint' )
        return HttpResponseRedirect(redireccion)


    if request.method == 'POST' and "Guardar" in request.POST:
        usuarios = request.POST.getlist('usuario')
        flujos_seleccionados = request.POST.getlist('flujo')
        uss = request.POST.getlist('agregar')

        flujos_copy = []
        for flujo in flujos_seleccionados:
            if flujo != "---":
                flujos_copy.append(flujo)
        flujos_seleccionados = flujos_copy


        usuarios_copy = []
        for usuario in usuarios:
            if usuario != "---":
                usuarios_copy.append(usuario)
        usuarios = usuarios_copy

        if len(usuarios) != len(uss):
            #Debe seleccionar tantos usuarios como checkbox marco
            error = "cantidad_diferente_"


        for (us,usuario,flujo_seleccionado) in zip(uss,usuarios,flujos_seleccionados):
                userStory = UserStory.objects.get(id=us)
                userStory.nombre_sprint = sprint.nombre_sprint
                userStory.usuario_asignado = Usuario.objects.get(id=usuario)
                userStory.id_flujo = flujo_seleccionado
                userStory.save()
                Sistema().registrar("Asginado US " + userStory.nombre+" a usuario "+Usuario.objects.get(id=usuario).username , request.user.username,  "Ninguno")


        redireccion = reverse('listar_todos_sprint' )
        return HttpResponseRedirect(redireccion)

    return render_to_response("Gestion_de_sprints/asignar_us_sprint.html", {"userstories": userStories,"flujos":flujos,"sprint":sprint,"equipo":usuario_equipo,"duracion_sprint":fecha.days,'error':error},
                          context_instance=RequestContext(request))



@login_required(login_url="/login/")
def listar_todos_sprints_view(request):
    """
    Permite listar todos los tableros kanban que se encuentran en la BD y filtrar por nombre de proyecto
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = Proyecto_Buscar_form(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data.get('Busqueda')
            if busqueda == '':
                proyecto = Proyecto.objects.all()
                context = {'form': form, 'proyectos': proyecto}
            else:
                proyecto = Proyecto.objects.filter(nombre_proyecto=busqueda)
                context = {'form': form, 'proyectos': proyecto}
        else:
            form = Proyecto_Buscar_form()
            context = {'form': form}

    else:
        form = Proyecto_Buscar_form()
        proyecto = Proyecto.objects.all()
        context = {'form': form, 'proyectos': proyecto}
    return render(request, 'Gestion_de_sprints/listar_proyecto_para_listar_sprint.html', context)




@login_required(login_url="/login/")
def listar_proyecto_sprint_view(request):
    """
    Permite listar todos los tableros kanban que se encuentran en la BD y filtrar por nombre de proyecto
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = Proyecto_Buscar_form(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data.get('Busqueda')
            if busqueda == '':
                proyecto = Proyecto.objects.all()
                context = {'form': form, 'proyectos': proyecto}
            else:
                proyecto = Proyecto.objects.filter(nombre_proyecto=busqueda)
                context = {'form': form, 'proyectos': proyecto}
        else:
            form = Proyecto_Buscar_form()
            context = {'form': form}

    else:
        form = Proyecto_Buscar_form()
        proyecto = Proyecto.objects.all()
        context = {'form': form, 'proyectos': proyecto}
    return render(request, 'Gestion_de_sprints/listar_proyecto_para_crear_sprint.html', context)


@login_required(login_url="/login/")
def sprint_backlog_view(request, id_sprint):
    """
    Permite listar el backlog del sprint seleccionado
    :param request:
    :param id_sprint:
    :return:
    """

    sprint_seleccionado = Sprint.objects.get(pk=id_sprint)
    id_proyecto = sprint_seleccionado.id_proyecto
    userstories = UserStory.objects.filter(proyecto=id_proyecto).filter(nombre_sprint=sprint_seleccionado.nombre_sprint)

    sprint_backlog_items = []
    for us in userstories:
        sprint_backlog_item_tmp = SprintBacklogInfo()
        sprint_backlog_item_tmp.nombre= us.nombre
        sprint_backlog_item_tmp.codigo= us.codigo
        sprint_backlog_item_tmp.prioridad = us.prioridad
        sprint_backlog_item_tmp.responsable = us.usuario_asignado
        sprint_backlog_item_tmp.porcentaje_realizado= us.porcentaje_realizado
        sprint_backlog_item_tmp.estado = us.estado
        sprint_backlog_item_tmp.horas_trabajadas = us.horas_dedicadas
        sprint_backlog_item_tmp.horas_estimadas = us.size*8 # se considera un dia como 8 horas de trabajo
        sprint_backlog_items.append(sprint_backlog_item_tmp)

    context = {'id_sprint':id_sprint,"nombre_sprint":sprint_seleccionado.nombre_sprint,'sprint_backlog_items':sprint_backlog_items}
    context = {'id_sprint':id_sprint,"nombre_sprint":sprint_seleccionado.nombre_sprint,'sprint_backlog_items':sprint_backlog_items}
    return render(request,'Gestion_de_sprints/sprint_backlog.html',context)


class SprintBacklogInfo():
    def __init__(self, nombre="", estado="", horas_trabajadas=0, responsable="",horas_estimadas=0,porcentaje_realizado=0, codigo="",prioridad=""):
        self.nombre = nombre
        self.codigo = codigo
        self.prioridad = prioridad
        self.responsable = responsable
        self.horas_estimadas = horas_estimadas
        self.horas_trabajadas = horas_trabajadas
        self.porcentaje_realizado = porcentaje_realizado
        self.estado = estado

@login_required(login_url="/login/")
def ReporpteWIP_view(request):
    """
    Genera un reporte en pdf sobre los trabajos activos y pendientes por cada
    equipo.
    :param request:
    :return:
    """

    if request.method == 'POST' and "r1" in request.POST:
        return reporte_trabajo_equipo_b()

    if request.method == 'POST' and "r2" in request.POST:
        return reporte_trabajo_usuario()

    if request.method == 'POST' and "r3" in request.POST:
        return reporte_actividades_proyecto()


    if request.method == 'POST' and "r6" in request.POST:
        return reporte_tiempo_proyecto()

    context = {}
    return render(request, 'Gestion_de_Reporte/reporte.html', context)

def reporte_trabajo_equipo_b():
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte_trabajo_usuario.pdf"
    #response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=72,
                            )
    elements = []


    tituloStyle = ParagraphStyle(name='Titulo', fontName='Helvetica-Bold', fontSize=16, alignment=TA_CENTER,leading=32)
    titulo = Paragraph("Informe de Trabajos por Equipos",tituloStyle)
    elements.append(titulo)
    lista = []
    paraStyle = ParagraphStyle(name='Contenido',fontName='Helvetica', fontSize=11, alignment=0)
    lista_proyectos = Proyecto.objects.all()

    for proyecto in lista_proyectos:
        try:
            lista_us = UserStory.objects.filter(proyecto_id = proyecto.id)
        except:
            lista_us = []

        headings = ('\nTrabajos del equipo del Proyecto: ' + proyecto.nombre_proyecto)

        no_existen_en_curso = True

        if len(lista_us) > 0:
            for us in lista_us:
                if us.estado.upper() == 'ENCURSO':
                    texto ="Codigo: "+us.codigo +"  Nombre: "+us.nombre+"  Duracion: "+str(int(us.size)) + " Dias" + "  Estado: en curso"
                    formato = Paragraph(texto,paraStyle)
                    lista.append(formato)
                    no_existen_en_curso = False

        if no_existen_en_curso:
            texto ="Sin trabajos asignados."
            formato = Paragraph(texto,paraStyle)
            lista.append(formato)

        WIP = []
        WIP.append(lista)
        t = Table([[headings]] + [WIP])
        t.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (3, -1),1, colors.dodgerblue),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
            ]
        ))
        elements.append(t)
        lista = []




    doc.build(elements, onFirstPage=titulo_logo)
    response.write(buff.getvalue())
    buff.close()
    return response


def reporte_trabajo_equipo():
    lista_proyecto = Proyecto.objects.filter(estado_proyecto='PENDIENTE') | Proyecto.objects.filter(estado_proyecto='ACTIVO')
    lista_sprint_cancelado = Sprint.objects.filter(estado='Cancelado')
    lista_us = list(UserStory.objects.filter(estado='PENDIENTE').order_by('nombre_sprint') | UserStory.objects.filter(estado='ENCURSO').order_by('nombre_sprint'))
    for cancelado in lista_sprint_cancelado:
        for us in lista_us:
            if us.nombre_sprint == cancelado.nombre_sprint:
                lista_us.remove(us)

    response = HttpResponse(content_type='application/pdf')
    pdf_name = "ReporteWIP.pdf"
    #response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=72,
                            )
    elements = []


    tituloStyle = ParagraphStyle(name='Titulo', fontName='Helvetica-Bold', fontSize=16, alignment=TA_CENTER,leading=32)
    titulo = Paragraph("Informe de Trabajos por Equipos",tituloStyle)
    elements.append(titulo)
    lista = []
    paraStyle = ParagraphStyle(name='Contenido',fontName='Helvetica', fontSize=11, alignment=0)

    for proyecto in lista_proyecto:
        headings = ('\nTrabajos del equipo del Proyecto: ' + proyecto.nombre_proyecto)
        if len(lista_us):
            for us in lista_us:
                if us.proyecto_id == proyecto.id and us.estado.upper() == 'ENCURSO':
                    texto ="Codigo: "+us.codigo +"  Nombre: "+us.nombre+"  Duracion: "+str(int(us.size)) + " Dias" + "  Estado: En curso"
                    formato = Paragraph(texto,paraStyle)
                    lista.append(formato)


        else:
            texto ="Tareas no asignadas."
            formato = Paragraph(texto,paraStyle)
            lista.append(formato)
        WIP = []
        WIP.append(lista)
        t = Table([[headings]] + [WIP])
        t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1),1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
        ]
        ))
        elements.append(t)
        lista = []

    doc.build(elements, onFirstPage=titulo_logo)
    response.write(buff.getvalue())
    buff.close()
    return response




def reporte_trabajo_usuario():
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte_trabajo_usuario.pdf"
    #response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=72,
                            )
    elements = []

    tituloStyle = ParagraphStyle(name='Titulo', fontName='Helvetica-Bold', fontSize=16, alignment=TA_CENTER,leading=32)
    titulo = Paragraph("Informe de Trabajos por Usuarios",tituloStyle)
    elements.append(titulo)
    lista = []
    paraStyle = ParagraphStyle(name='Contenido',fontName='Helvetica', fontSize=11, alignment=0)
    lista_usuario = Usuario.objects.all()

    for usuario in lista_usuario:
        if usuario.username != 'admin':
            headings = ('\nTrabajo del usuario: ' + usuario.first_name)
            lista_us = UserStory.objects.filter(usuario_asignado_id=usuario.id)
            if len(lista_us) > 0:
                for us in lista_us:
                        texto ="Codigo: "+us.codigo +"  Nombre: "+us.nombre+"  Duracion: "+str(int(us.size)) + " Dias" + "  Estado: " + us.estado.lower()
                        formato = Paragraph(texto,paraStyle)
                        lista.append(formato)
            else:
                texto ="Sin trabajos asignados."
                formato = Paragraph(texto,paraStyle)
                lista.append(formato)
            WIP = []
            WIP.append(lista)
            t = Table([[headings]] + [WIP])
            t.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (3, -1),1, colors.dodgerblue),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
            ]
            ))
            elements.append(t)
            lista = []

    doc.build(elements, onFirstPage=titulo_logo)
    response.write(buff.getvalue())
    buff.close()
    return response


def reporte_actividades_proyecto():
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte_actividades_proyecto.pdf"
    #response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=72,
                            )
    elements = []

    tituloStyle = ParagraphStyle(name='Titulo', fontName='Helvetica-Bold', fontSize=16, alignment=TA_CENTER,leading=32)

    titulo = Paragraph("Informe de Actividades de Proyectos por prioridad",tituloStyle)
    elements.append(titulo)
    lista = []
    paraStyle = ParagraphStyle(name='Contenido',fontName='Helvetica', fontSize=11, alignment=0)
    lista_proyecto = Proyecto.objects.all()
    for proyecto in lista_proyecto:
        lista_flujos = Flujo.objects.filter(id_Proyecto_id=proyecto.id)
        headings = ('\nActividades del proyecto: ' + proyecto.nombre_proyecto)

        if len(lista_flujos) > 0:
            for flujo in lista_flujos:
                lista_actividades = Actividad.objects.filter(id_Flujo_id=flujo.id )
                if len(lista_actividades) > 0:
                    for actividad in lista_actividades:
                        texto ="Nombre: "+str(actividad.nombre_actividad) + " Prioridad"+str(actividad.orden_actividad)
                        formato = Paragraph(texto,paraStyle)
                        lista.append(formato)
                else:
                    texto ="Sin actividades asignadas."
                    formato = Paragraph(texto,paraStyle)
                    lista.append(formato)
        else:
            texto ="Sin actividades asignadas."
            formato = Paragraph(texto,paraStyle)
            lista.append(formato)


        WIP = []
        WIP.append(lista)
        t = Table([[headings]] + [WIP])
        t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1),1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
        ]
        ))
        elements.append(t)
        lista = []

    doc.build(elements, onFirstPage=titulo_logo)
    response.write(buff.getvalue())
    buff.close()
    return response

def reporte_tiempo_proyecto():
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte_tiempo_proyecto.pdf"
    #response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=72,
                            )
    elements = []


    ################ INFORME DE TRABAJO POR EQUIPO ###########################################

    tituloStyle = ParagraphStyle(name='Titulo', fontName='Helvetica-Bold', fontSize=16, alignment=TA_CENTER,leading=32)
    titulo = Paragraph("Informe de tiempo estimado por proyecto y ejecucion del mismo",tituloStyle)
    elements.append(titulo)

    lista_proyecto = Proyecto.objects.all()
    for proyecto in lista_proyecto:
        headings = ('\nNombre de proyecto: ' + proyecto.nombre_proyecto)
        drawing = linechart(proyecto.id)

        WIP = []
        WIP.append(drawing)
        t = Table([[headings]] + [WIP])
        t.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (3, -1),1, colors.dodgerblue),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
            ]
            ))
        elements.append(t)

    doc.build(elements, onFirstPage=titulo_logo)
    response.write(buff.getvalue())
    buff.close()
    return response



def linechart(id_proyecto):
    d = MyLineChartDrawing()
    d.title._text = 'Some custom title'
    d.YLabel._text = 'Horas Restantes'
    labels =  ["Optimo","Real"]

    #Datos
    proyecto = Proyecto.objects.get(id=id_proyecto)
    uss = UserStory.objects.filter(proyecto_id=proyecto.id)
    duracion_total_de_us = 0 #en horas


    fecha_inicio = proyecto.fecha_inicio
    fecha_fin = proyecto.fecha_finalizacion
    dias = fecha_fin - fecha_inicio

    d.XLabel._text = 'Duracion del proyecto ' + str(dias.days) + ' dias.'


    for item in uss:
        duracion_total_de_us = duracion_total_de_us + item.size

    #Se calcula el optimo
    duracion_optima = []
    lista_dias = []
    horas_anteriores = duracion_total_de_us
    contador = 1
    duracion_optima.append(duracion_total_de_us)
    while(contador <=dias.days and horas_anteriores > 0):
        lista_dias.append(contador)
        duracion_optima.append(horas_anteriores-1)
        contador = contador +1
        horas_anteriores = horas_anteriores -1

    lista_optima = zip(lista_dias,duracion_optima)

    #Se obtiene el real
    linea_trabajada = []
    dias_transcurridos = []
    burn = BurndownChartProyecto.objects.filter(id_proyecto=proyecto.id)
    horas = duracion_total_de_us
    dia_auxiliar = 1
    for item in burn:
        dias_transcurridos.append(dia_auxiliar)
        horas = horas -item.horas_trabajadas
        linea_trabajada.append(horas)
        dia_auxiliar = dia_auxiliar +1

    duracion_real = zip(dias_transcurridos,linea_trabajada)

    if len(duracion_real)>0:
        d.chart.data = [lista_optima,
                    duracion_real]
    else:
        d.chart.data = [lista_optima]



    if labels:
        # set colors in the legend
        d.Legend.colorNamePairs = []
        for cnt,label in enumerate(labels):
                d.Legend.colorNamePairs.append((d.chart.lines[cnt].strokeColor,label))
    return d



def titulo_logo(canvas,doc):
    canvas.saveState()
    canvas.drawString(1 * cm, 27 * cm,'Grupo R07')
    canvas.drawString(1 * cm, 26.5 * cm,'Ingenieria de Software II')
    canvas.restoreState()

from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.lib import colors
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.textlabels import Label


class MyLineChartDrawing(Drawing):
    def __init__(self,width=400,height=200,*args,**kw):
        apply(Drawing.__init__,(self,width,height)+args,kw)
        self.add(LinePlot(), name='chart')

        self.add(String(200,150,''), name='title')

        #set any shapes, fonts, colors you want here.  We'll just
        #set a title font and place the chart within the drawing.
        #pick colors for all the lines, do as many as you need
        self.chart.x = 30
        self.chart.y = 40
        self.chart.width = self.width-2*self.chart.x
        self.chart.height = self.height-2*self.chart.y
        self.chart.lines[0].strokeColor = colors.blue
        self.chart.lines[1].strokeColor = colors.green
        self.chart.lines[2].strokeColor = colors.yellow
        self.chart.lines[3].strokeColor = colors.red
        self.chart.lines[4].strokeColor = colors.black
        self.chart.lines[5].strokeColor = colors.orange
        self.chart.lines[6].strokeColor = colors.cyan
        self.chart.lines[7].strokeColor = colors.magenta
        self.chart.lines[8].strokeColor = colors.brown

        self.chart.fillColor = colors.white
        self.title.fontSize = 15
        self.chart.data = [((0, 50), (100,100), (200,200), (250,210), (300,300), (400,500))]
        self.chart.xValueAxis.labels.fontSize = 12
        self.chart.xValueAxis.forceZero = 0
        self.chart.xValueAxis.gridEnd = 115
        self.chart.xValueAxis.tickDown = 3
        self.chart.xValueAxis.visibleGrid = 1
        self.chart.yValueAxis.tickLeft = 3
        self.chart.yValueAxis.labels.fontSize = 12
        self.title.x = self.width/2
        self.title.y = self.height - 50
        self.title.textAnchor ='middle'
        self.add(Legend(),name='Legend')
        self.Legend.fontSize = 12
        self.Legend.x = self.width
        self.Legend.y = 85
        self.Legend.dxTextSpace = 5
        self.Legend.dy = 5
        self.Legend.dx = 5
        self.Legend.deltay = 5
        self.Legend.alignment ='right'
        self.add(Label(),name='XLabel')
        self.XLabel.fontSize = 12
        self.XLabel.x = 200
        self.XLabel.y = 5
        self.XLabel.textAnchor ='middle'
        #self.XLabel.height = 20
        self.XLabel._text = ""
        self.add(Label(),name='YLabel')
        self.YLabel.fontSize = 12
        self.YLabel.x = 2
        self.YLabel.y = 80
        self.YLabel.angle = 90
        self.YLabel.textAnchor ='middle'
        self.YLabel._text = ""
        self.chart.yValueAxis.forceZero = 1
        self.chart.xValueAxis.forceZero = 1
