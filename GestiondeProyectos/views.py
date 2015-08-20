from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext

# Create your views here.
from GestiondeProyectos.forms import Proyecto_Buscar_form, CrearProyectoForm, ModificarProyectoForm
from GestiondeProyectos.models import Proyecto
from GestiondeFlujos.models import Flujo
from GestiondeSistema.models import Sistema
from GestiondeUserStories.forms import Busqueda_UserStory_form
from GestiondeUserStories.models import UserStory
from GestiondeUsuarios.models import Usuario
from GestiondeSprints.models import Sprint


@login_required(login_url="/login/")
def crear_proyecto_view(request):
    """
    Permite la creacion de un proyecto
    :param request:
    :return:
    """
    usuario = request.user
    if not usuario.has_perm('GestiondeProyectos.crear_proyecto'):
        msg = 'El usuario no tiene permiso para crear proyectos'
        return render(request, 'Sistema/403.html', {'msg': msg})

    if request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/home')

    if request.method == 'POST' and 'Guardar' in request.POST:

        formulario = CrearProyectoForm(request.POST)
        if request.POST.get('cliente') is None:
            context = {'formulario': formulario, 'error': 'cliente'}
            return render(request, 'Gestion_de_Proyectos/crear_proyecto.html', context)

        if request.POST.get('equipo_desarrollo') is None:
            context = {'formulario': formulario, 'error': 'equipo_desarrollo'}
            return render(request, 'Gestion_de_Proyectos/crear_proyecto.html', context)

        if request.POST.get('scrum_master') is None:
            context = {'formulario': formulario, 'error': 'scrum_master'}
            return render(request, 'Gestion_de_Proyectos/crear_proyecto.html', context)

        if request.POST.get('fecha_inicio') >= request.POST.get('fecha_finalizacion'):
            context = {'formulario': formulario, 'error': 'fechas'}
            return render(request, 'Gestion_de_Proyectos/crear_proyecto.html', context)

        nombre_proyecto = request.POST.get('nombre_proyecto')
        codigo_proyecto = request.POST.get('codigo_proyecto')


        if Proyecto.objects.filter(nombre_proyecto=nombre_proyecto):
            context = {'formulario': formulario, 'error': 'nombre'}
            return render(request, 'Gestion_de_Proyectos/crear_proyecto.html', context)

        if Proyecto.objects.filter(codigo_proyecto=codigo_proyecto):
            context = {'formulario': formulario, 'error': 'codigo'}
            return render(request, 'Gestion_de_Proyectos/crear_proyecto.html', context)

        if formulario.is_valid():
            formulario.save()
            Sistema().registrar("Creado proyecto " + request.POST.get('nombre_proyecto'), request.user.username,
                                "Ninguno")
            return HttpResponseRedirect('listar_proyecto')
        else:
            context = {'formulario': formulario, 'error': 'otro'}
            return render(request, 'Gestion_de_Proyectos/crear_proyecto.html', context)

    formulario = CrearProyectoForm()
    context = {'formulario': formulario}

    return render(request, 'Gestion_de_Proyectos/crear_proyecto.html', context)


@login_required(login_url="/login/")
def listar_proyecto_view(request):
    """
    Permite al usuario realizar el listado de proyectos que se encuentran en el sistema
    habilitando con la opcion de filtrados de usuarios, tambien habilitara el boton para
    modificar si es que posee los permisos el usuario en sesion.
    :param request:
    :return:
    """

    usuario = request.user
    if not usuario.has_perm('GestiondeProyectos.listar_proyecto'):
        msg = 'El usuario no tiene permiso para listar proyectos'
        return render(request, 'Sistema/403.html', {'msg': msg})

    misproyectos = []
    for proyectotmp in Proyecto.objects.all():
        if proyectotmp.scrum_master.id == usuario.id or proyectotmp.equipo_desarrollo.filter(
                username=usuario.username).exists():
            misproyectos.append(proyectotmp)

    if request.method == 'POST':
        form = Proyecto_Buscar_form(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data.get('Busqueda')
            if busqueda == '':
                proyecto = misproyectos
                context = {'form': form, 'proyectos': proyecto}
            else:
                misproyectosconfiltro = []
                for item in misproyectos:
                    if busqueda in item.nombre_proyecto:
                        misproyectosconfiltro.append(item)

                proyecto = misproyectosconfiltro
                context = {'form': form, 'proyectos': proyecto}
        else:
            form = Proyecto_Buscar_form()
            context = {'form': form}

    else:
        form = Proyecto_Buscar_form()
        proyecto = misproyectos
        context = {'form': form, 'proyectos': proyecto}
    return render(request, 'Gestion_de_Proyectos/Listar_Proyecto.html', context)


@login_required(login_url="/login/")
def reporte_proyecto_view(request, id_proyecto):
    """
     Permite al usuario realizar un reporte del proyecto en cuanto a user stories.
     :param request:
     :return:
     """
    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)
    nombre_proyecto = proyecto_seleccionado.nombre_proyecto

    if request.method == 'POST':
        form = Busqueda_UserStory_form(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data.get('Busqueda')

            if busqueda != '':
                userstories = UserStory.objects.filter(proyecto_id=id_proyecto).filter(nombre=busqueda)

            elif busqueda == '':
                userstories = UserStory.objects.filter(proyecto_id=id_proyecto)
        else:
            form = Busqueda_UserStory_form()
            userstories = UserStory.objects.filter(proyecto_id=id_proyecto)

    else:
        form = Busqueda_UserStory_form()
        userstories = UserStory.objects.filter(proyecto_id=id_proyecto)

    userstories_reporte = []

    for userstory in userstories:
        usuario = ''
        if userstory.usuario_asignado is None:
            usuario = "No ha sido Asignado"
        else:
            usuario = userstory.usuario_asignado.username

        userstories_reporte.append(
            ReporteInfo(nombre=userstory.nombre, estado=userstory.estado, horasdedicadas=userstory.horas_dedicadas,
                        responsable=usuario))

    context = {'formulario': form, 'userstories_reporte': userstories_reporte, "nombre_proyecto": nombre_proyecto,
               "id_proyecto": id_proyecto}

    return render(request, 'Gestion_de_Proyectos/reporte_proyecto.html', context)


@login_required(login_url="/login/")
def modificar_proyecto_view(request, id_proyecto):
    """
    permite la modificacion de un proyecto que no posea un estado de finalizado o cancelado a los usuarios con permisos adecuados
    :param
    request:
    :param id_proyecto:
    :return:
    """
    usuario = request.user
    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)
    formulario_original = proyecto_seleccionado
    cliente_proyecto = proyecto_seleccionado.cliente

    if (not usuario.has_perm(
            'GestiondeProyectos.modificar_proyecto') or proyecto_seleccionado.scrum_master.id != usuario.id) and not usuario.groups.filter(
            name='Administrador').exists():
        msg = 'El usuario no tiene permiso para modificar el proyecto'
        return render(request, 'Sistema/403.html', {'msg': msg})

    if request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_proyecto')

    if request.method == 'POST' and 'Guardar' in request.POST:
        formulario = ModificarProyectoForm(request.POST, instance=proyecto_seleccionado)

        #Control para que no pase de estado activo a pendiente
        if (formulario_original.estado_proyecto.upper == "ACTIVO" and request.POST.get('estado_proyecto').upper == "PENDIENTE"):
            mensaje = "estado_activo_pendiente"
            formulario = ModificarProyectoForm(instance=proyecto_seleccionado)
            context = {'formulario': formulario, 'id_proyecto': id_proyecto, "error": mensaje,
                       'cliente': cliente_proyecto}
            return render_to_response('Gestion_de_Proyectos/modificar_proyecto.html', context,
                                      context_instance=RequestContext(request))

        #Control para que la fecha de inicio sea mayor a la fecha de finalizacion
        if request.POST.get('fecha_inicio') >= request.POST.get('fecha_finalizacion'):
            context = {'formulario': formulario, 'error': 'fechas', 'id_proyecto': id_proyecto}
            return render(request, 'Gestion_de_Proyectos/modificar_proyecto.html', context)

        #Control para que en caso de modificarse el equipo de desarrollo no se deje sin seleccionar al equipo
        if request.POST.getlist('equipo_desarrollo') is None:
            context = {'formulario': formulario, 'error': 'equipo', 'id_proyecto': id_proyecto}
            return render(request, 'Gestion_de_Proyectos/modificar_proyecto.html', context)

        #Control para que se coloque una descripcion del proyecto
        if request.POST.get('descripcion_proyecto') is None:
            context = {'formulario': formulario, 'error': 'descripcion', 'id_proyecto': id_proyecto}
            return render(request, 'Gestion_de_Proyectos/modificar_proyecto.html', context)

        print(request.POST.get('estado_proyecto'))
        #Control de que si el proyecto pasa a estado finalizado todos los sprints y us deben ser finalizados
        if request.POST.get('estado_proyecto').upper() == 'FINALIZADO':
            existen_sprints_activos_o_pendientes = False
            try:
                sprints_proyecto = Sprint.objects.filter(id_proyecto=id_proyecto)

                for item in sprints_proyecto:

                    if item.estado.upper() == 'PENDIENTE' or item.estado.upper() == 'ACTIVO':
                        existen_sprints_activos_o_pendientes = True

                if existen_sprints_activos_o_pendientes:
                    mensaje = "sprints_activos_o_pendientes"
                    context = {'formulario': formulario, 'error': mensaje, 'id_proyecto': id_proyecto}
                    return render(request, 'Gestion_de_Proyectos/modificar_proyecto.html', context)
            except:
                pass

            try:
                us_proyecto = UserStory.objects.filter(proyecto_id=id_proyecto)
                existen_us_activos_o_pendientes = False

                for item in us_proyecto:
                    if item.estado.upper() == 'PENDIENTE' or item.estado.upper() == 'ACTIVO':
                        existen_us_activos_o_pendientes = True


                if existen_us_activos_o_pendientes:
                    mensaje = "us_activos_o_pendientes"
                    context = {'formulario': formulario, 'error': mensaje, 'id_proyecto': id_proyecto}
                    return render(request, 'Gestion_de_Proyectos/modificar_proyecto.html', context)
            except:
                pass

        if not request.POST.get('scrum_master') is None:
            proyecto_seleccionado.scrum_master = Usuario.objects.get(pk=request.POST.get('scrum_master'))

        proyecto_seleccionado.fecha_finalizacion = request.POST.get('fecha_finalizacion')
        proyecto_seleccionado.descripcion_proyecto = request.POST.get('descripcion_proyecto')
        proyecto_seleccionado.cliente = Usuario.objects.get(pk=(request.POST.get('cliente')))
        equipo_seleccionado = request.POST.getlist('equipo_desarrollo')
        proyecto_seleccionado.equipo_desarrollo.clear()
        proyecto_seleccionado.estado_proyecto = request.POST.get('estado_proyecto')

        for item in equipo_seleccionado:
            participante = Usuario.objects.get(pk=item)
            proyecto_seleccionado.equipo_desarrollo.add(participante)


        proyecto_seleccionado.save()

        Sistema().registrar("Modificado proyecto " + request.POST.get('nombre_proyecto'), request.user.username,
                            "Ninguno")
        return HttpResponseRedirect('/listar_proyecto')

    formulario = ModificarProyectoForm(instance=proyecto_seleccionado)
    context = {'formulario': formulario, 'id_proyecto': id_proyecto, 'cliente': cliente_proyecto}
    return render_to_response('Gestion_de_Proyectos/modificar_proyecto.html', context,
                              context_instance=RequestContext(request))


@login_required(login_url="/login")
def consultar_proyecto_view(request, id_proyecto):
    """
    Permite la consulta de un proyecto a partir del proyecto que es seleccionado
    :param request:
    :param id_proyecto:
    :return:
    """

    usuario = request.user
    if not usuario.has_perm('GestiondeProyectos.consulta_proyecto'):
        msg = 'El usuario no tiene permiso para consultar proyectos'
        return render(request, 'Sistema/403.html', {'msg': msg})

    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)
    flujos = Flujo.objects.filter(id_Proyecto=id_proyecto)

    if request.method == 'POST' and 'Retroceder' in request.POST:
        return HttpResponseRedirect('/listar_proyecto')
    return render_to_response("Gestion_de_Proyectos/consultar_proyecto.html",
                              {"proyecto": proyecto_seleccionado, "flujos": flujos},
                              context_instance=RequestContext(request))


@login_required(login_url="/login/")
def product_backlog_view(request, id_proyecto):
    """
    Permite listar el backlog del proyecto seleccionado
    :param request:
    :param id_proyecto:
    :return:
    """


    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)
    userstories = UserStory.objects.filter(proyecto=proyecto_seleccionado)

    product_backlog_items = []
    for us in userstories:
        product_backlog_item_tmp = ProductBacklogInfo()
        product_backlog_item_tmp.id = us.id
        product_backlog_item_tmp.nombre= us.nombre
        product_backlog_item_tmp.codigo= us.codigo
        product_backlog_item_tmp.prioridad = us.prioridad
        product_backlog_item_tmp.responsable = us.usuario_asignado
        product_backlog_item_tmp.sprint = us.nombre_sprint
        product_backlog_item_tmp.porcentaje_realizado= us.porcentaje_realizado
        product_backlog_item_tmp.estado = us.estado
        product_backlog_item_tmp.horas_trabajadas = us.horas_dedicadas
        product_backlog_item_tmp.horas_estimadas = us.size*8 # se considera un dia como 8 horas de trabajo
        product_backlog_items.append(product_backlog_item_tmp)

    context = {"id_proyecto":id_proyecto,"nombre_proyecto":proyecto_seleccionado.nombre_proyecto,'product_backlog_items':product_backlog_items}
    return render(request,'Gestion_de_Proyectos/product_backlog.html',context)


class ProductBacklogInfo():
    def __init__(self, id=0,nombre="", estado="", horas_trabajadas=0, responsable="",horas_estimadas=0,porcentaje_realizado=0, codigo="",prioridad="",sprint=""):
        self.id = id
        self.nombre = nombre
        self.codigo = codigo
        self.prioridad = prioridad
        self.responsable = responsable
        self.sprint = sprint
        self.horas_estimadas = horas_estimadas
        self.horas_trabajadas = horas_trabajadas
        self.porcentaje_realizado = porcentaje_realizado
        self.estado = estado


class ReporteInfo():
    def __init__(self, nombre="", estado="", horasdedicadas=0, responsable=""):
        self.nombre = nombre
        self.horasdedicadas = horasdedicadas
        self.responsable = responsable
        self.estado = estado


@login_required(login_url="/login/")
def grafico_estado_us_view(request, id_userStory):
    us = UserStory.objects.get(id=id_userStory)
    horas_dedicadas_a_dias = us.horas_dedicadas
    try:
        horas_dedicadas_a_dias = horas_dedicadas_a_dias/8
    except:
        pass

    print(horas_dedicadas_a_dias)

    context = {'us':us,'tiempo_real':horas_dedicadas_a_dias}
    return render(request,'Gestion_de_Proyectos/grafico_estado_us.html',context)
