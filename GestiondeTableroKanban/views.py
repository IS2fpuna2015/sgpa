from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
# Create your views here.
from GestiondeProyectos.models import Proyecto
from GestiondeFlujos.models import Flujo
from GestiondeProyectos.forms import Proyecto_Buscar_form
from GestiondeTableroKanban.models import TableroKanban
from GestiondeSprints.models import Sprint
from GestiondeSistema.models import Sistema
from GestiondeFlujos.models import Actividad
from GestiondeUserStories.models import UserStory
from GestiondeUserStories.models import FileAttached_model

from sgpa import settings
from django.utils import datetime_safe
from GestiondeUsuarios.models import Usuario
from sgpa.Util import enviar_notificacion
from GestiondeUserStories.models import Comentario


@login_required(login_url="/login/")
def crear_tablero_kanban_view(request, id_proyecto):
    """
    Permite la generacion de un tablero kanban al proyecto que posee el id de id_proyecto
    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)
    flujos = Flujo.objects.filter(id_Proyecto=id_proyecto)
    sprints = Sprint.objects.filter(id_proyecto=id_proyecto,estado="Activo")
    sprints_copy = []
    tablero = TableroKanban()
    error = "Ninguno"

    #Controla que no exista otro sprint que se encuentre activo
    lista_sprint = list(Sprint.objects.filter(id_proyecto=id_proyecto))
    sprints_activos = []
    for item in lista_sprint:
        if item.estado == "ACTIVO":
            sprints_activos.append(item)

    if len(sprints_activos) >= 1:
        error = "sprint activo"
        context = {'tablero':tablero,"proyecto":proyecto_seleccionado,"flujos":flujos,"sprints":sprints,"error":error}
        return render_to_response("Gestion_de_tablero_kanban/crear_tablero.html",context,context_instance=RequestContext(request))


    #Controla que existan sprint antes de realizar la creacion del tablero
    if len(sprints) == 0:
        error = "cree sprint"
        context = {'tablero':tablero,"proyecto":proyecto_seleccionado,"flujos":flujos,"sprints":sprints,"error":error}
        return render_to_response("Gestion_de_tablero_kanban/crear_tablero.html",context,context_instance=RequestContext(request))

    uss = []
    #Obtiene los us que fueron asignados a ese sprint
    for item in sprints:
        uss = UserStory.objects.filter(proyecto_id=id_proyecto,nombre_sprint=item.nombre_sprint)
        if len(uss) > 0:
            sprints_copy.append(item)

    for item in uss:
        if item.usuario_asignado_id:
            error == "ningun_usuario"

    if error == "ningun_usuario":
        context = {'tablero':tablero,"proyecto":proyecto_seleccionado,"flujos":flujos,"sprints":sprints,"error":error}
        return render_to_response("Gestion_de_tablero_kanban/crear_tablero.html",context,context_instance=RequestContext(request))

    sprints = sprints_copy

    #Controla que existan mas de un US dentro del sprint
    if len(sprints) == 0:
        error = "asigne us"
        context = {'tablero':tablero,"proyecto":proyecto_seleccionado,"flujos":flujos,"sprints":sprints,"error":error}
        return render_to_response("Gestion_de_tablero_kanban/crear_tablero.html",context,context_instance=RequestContext(request))

    #Controla que existan flujos para la creacion del tablero kanban
    if len(flujos) == 0:
        error = "asigne flujo"
        context = {'tablero':tablero,"proyecto":proyecto_seleccionado,"flujos":flujos,"sprints":sprints,"error":error}
        return render_to_response("Gestion_de_tablero_kanban/crear_tablero.html",context,context_instance=RequestContext(request))



    if request.method == 'POST' and 'Guardar' in request.POST:
        if request.POST.get('nombre_tablero') is not None and request.POST.get('sprint') is not None and request.POST.get("flujo") is not None:

            try:
                error = "Contenido"
                tablero1 = TableroKanban.objects.get(id_proyecto_id=id_proyecto,id_sprint_id=request.POST.get('sprint'),id_flujo_id=request.POST.get('flujo'))
                #Si pasa esta linea quiere decir que existe un tablero con las mismas caracteristicas en el proyecto, debe mostrar el error
                context = {'tablero':tablero,"proyecto":proyecto_seleccionado,"flujos":flujos,"sprints":sprints,"error":error,'tablero_copy':tablero1}
                return render_to_response("Gestion_de_tablero_kanban/crear_tablero.html",context,context_instance=RequestContext(request))
            except:
                #Si salta la excepcion quiere decir que no existe un tablero con el mismo contenido, por tanto puede continuar
                pass



            try:
                #va a buscar en la bd si existe el tablero con el nombre indicado, de esa manera se
                #controla que los nombre de los tableros no coincidan
                error = "Nombre"
                tablero2 = TableroKanban.objects.get(nombre_tablero=request.POST.get('nombre_tablero'))
                #si pasa a esta linea quiere decir que el tablero existe, debe mostrar un cuadro indicando el error
                context = {'tablero':tablero,"proyecto":proyecto_seleccionado,"flujos":flujos,"sprints":sprints,"error":error,'tablero_copy':tablero1}
                return render_to_response("Gestion_de_tablero_kanban/crear_tablero.html",context,context_instance=RequestContext(request))
            except:
                pass

                tablero.nombre_tablero = request.POST.get('nombre_tablero')
                tablero.estado_tablero = request.POST.get('estado')
                sprint = Sprint.objects.get(pk=request.POST.get("sprint"))
                flujo = Flujo.objects.get(pk=request.POST.get("flujo"))
                flujo.id_sprint = sprint.id
                flujo.save()

                uss = UserStory.objects.filter(proyecto_id=id_proyecto,nombre_sprint=sprint.nombre_sprint)
                actividades = list(Actividad.objects.filter(id_Flujo_id = flujo))

                for us in uss:
                    if us.estado != "En Curso":
                        us.estado = "En Curso"
                        us.id_flujo = flujo.id
                        us.id_actividad = actividades[0].id
                        us.save()



                tablero.id_sprint = sprint
                tablero.id_flujo  = flujo
                tablero.id_proyecto = Proyecto.objects.get(pk=id_proyecto)
                tablero.nombre_proyecto = Proyecto.objects.get(pk=id_proyecto).nombre_proyecto
                tablero.save()



                Sistema().registrar("Creado tablero kanban "+ request.POST.get('nombre_tablero') +" para proyecto "+Proyecto.objects.get(pk=id_proyecto).nombre_proyecto,request.user.username,"Ninguno")
                redireccion = reverse('listar_tablero_kanban_proyecto', args=[id_proyecto])
                return HttpResponseRedirect(redireccion)
        else:
            error = "Incompleto"

    context = {'tablero':tablero,"proyecto":proyecto_seleccionado,"flujos":flujos,"sprints":sprints,"error":error}
    return render_to_response("Gestion_de_tablero_kanban/crear_tablero.html",context,context_instance=RequestContext(request))

@login_required(login_url="/login/")
def listar_proyecto_kanban_view(request):
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
    return render(request, 'Gestion_de_tablero_kanban/Listar_Proyecto_para_crear_tablero.html', context)



@login_required(login_url="/login/")
def listar_tablero_kanban_proyecto_view(request,id_proyecto):
    """
    Permite listar los tableros que posee un proyecto
    :param request:
    :param id_proyecto:
    :return:
    """
    tableros = TableroKanban.objects.filter(id_proyecto=id_proyecto)
    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)
    context = {'tableros':tableros,"proyecto":proyecto_seleccionado}
    return render(request, 'Gestion_de_tablero_kanban/listar_tableros_proyecto.html', context)


@login_required(login_url="/login/")
def listar_tablero_kanban_view(request):
    """
    Lista todos los tableros que se encuentran en en la BD
    :param request:
    :return:
    """
    tableros = TableroKanban.objects.all()
    context = {'tableros':tableros}
    return render(request, 'Gestion_de_tablero_kanban/listar_tablero.html', context)

@login_required(login_url="/login/")
def visualizar_tablero_kanban_view(request,id_tablero):
    """
    Permite visualizar el tablero kanban
    :param request:
    :param id_tablero:
    :return:
    """

    tablero = TableroKanban.objects.get(pk=id_tablero)
    flujo = Flujo.objects.get(pk=tablero.id_flujo.id)
    actividades = Actividad.objects.filter(id_Flujo_id=flujo.id)
    sprint = Sprint.objects.get(pk=tablero.id_sprint.id)
    uss = UserStory.objects.filter(nombre_sprint=sprint.nombre_sprint,id_flujo=flujo.id)

    primera_actividad = list(actividades)
    primera_actividad.pop()
    print(len(uss))
    for us in uss:
        if us.id_actividad == 0:
            us.id_actividad = actividades[0].id

    context = {'tablero':tablero , 'flujo':flujo ,'sprint':sprint,'actividades':actividades,'uss':uss}
    return render(request, 'Gestion_de_tablero_kanban/visualizar_tablero_kanban.html', context)

@login_required(login_url="/login/")
def cambio_us_actividad_estado_tablero_kanban_view(request,id_tablero,id_us):
    """
    Permite cambiar de actividad el US al usuario que posea los permisos adecuados
    :param request:
    :param id_tablero:
    :param id_us:
    :return:
    """
    us = UserStory.objects.get(pk=id_us)
    tablero = TableroKanban.objects.get(pk=id_tablero)
    flujo = Flujo.objects.get(pk=tablero.id_flujo.id)
    actividades = Actividad.objects.filter(id_Flujo_id=flujo.id)
    copy_actividades = list(actividades)
    rol = ""
    ultima_actividad = Actividad.objects.get(id=us.id_actividad)
    siguiente_actividad = ultima_actividad
    us_completado = False;

    #Se obtiene el rol del usuario para limitar las vistas
    for permiso in request.user.groups.all():
        if permiso.name == "Scrum Master":
            rol = "Scrum Master"
            break
        if permiso.name == "Desarrollador":
            rol = "Desarrollador"


    #Se obtendra la siguiente actividad a realizar cuando el US posea estado Done
    if us.estado_en_actividad == 'Done':
        for index in range(len(copy_actividades)):
            if ultima_actividad == copy_actividades[index]:
                if len(copy_actividades) > index+1:
                    siguiente_actividad = copy_actividades[index+1]
                    break


    if us.id_actividad == copy_actividades.pop().id and us.estado_en_actividad == "Done":
        us_completado = True

    ######################
    #rol = "Desarrollador"
    ######################

    if request.method == 'POST':
        if us_completado and rol == "Desarrollador":
            estado_en_actividad = "Done"
        else:
            estado_en_actividad =  request.POST.get('estado') or "ToDo"


        if request.POST.get('comentario') == "":
            error = "comentario"
            context = {'tablero':tablero,'actividades':actividades,"siguiente_actividad":siguiente_actividad,'error':error,'us':us,"rol":rol,"us_completado":us_completado}
            return render(request, 'Gestion_de_tablero_kanban/cambio_actividad_estado.html', context)

        contenido_comentario = request.POST.get('comentario')
        comentario = Comentario(comentario=contenido_comentario,autor=request.user.username,us_id=id_us)
        comentario.save()


        id_actividad = request.POST.get('actividad') or us.id_actividad
        us.id_actividad = id_actividad
        us.porcentaje_realizado = request.POST.get('porcentaje_realizado')
        us.horas_dedicadas = request.POST.get('horas_dedicadas')
        us.estado_en_actividad = estado_en_actividad
        us.save()

        if int(us.porcentaje_realizado) == 100:
            proyecto = Proyecto.objects.get(id=us.proyecto_id)
            scrum_master = Usuario.objects.get(id=proyecto.scrum_master.id)
            enviar_notificacion("Finalizacion de US ",us.nombre,scrum_master.email,'sgpa@sgpa.com')


        #Se debe agregar un comentario o un archivo para que se guarde el cambio de estado
        #Seccion para agregar un archivo a un US para realizar el cambio de actividad o estado
        if request.POST.get('image') is not None:
            fecha_path = str(datetime_safe.date.today()).split("-")
            archivo_request = request.FILES['image']
            archivo_a_adjuntar = FileAttached_model()
            archivo_a_adjuntar.file = archivo_request
            archivo_a_adjuntar.file_name = archivo_request.name
            archivo_a_adjuntar.file_path = settings.MEDIA_URL + 'subidos/'+fecha_path[0]+'/'+fecha_path[1]+'/'+fecha_path[2]+'/'
            #archivo_a_adjuntar.save()

        #if request.POST.get('image') is None and request.POST.get('comentario'):
            #print error, debe ingresar uno de los dos para guardar el cambio de estado o actividad del US


        Sistema().registrar("Cambio US "+us.nombre+" a actividad "+ultima_actividad.nombre_actividad+" con estado "+us.estado_en_actividad,request.user.username,"Ninguno")
        redireccion = reverse('visualizar_tablero_kanban', args=[id_tablero])
        return HttpResponseRedirect(redireccion)

    context = {'tablero':tablero,'actividades':actividades,"siguiente_actividad":siguiente_actividad,'us':us,"rol":rol,"us_completado":us_completado}
    return render(request, 'Gestion_de_tablero_kanban/cambio_actividad_estado.html', context)


@login_required(login_url="/login/")
def modificar_tablero_kanban_view(request, id_tablero):
    """
    Permite la modificacion de un tablero kanban especificado a la hora de seleccionar
    :param request:
    :param id_tablero:
    :return:
    """
    tablero = TableroKanban.objects.get(pk=id_tablero)
    flujo = Flujo.objects.get(pk=tablero.id_flujo.id)
    actividades = Actividad.objects.filter(id_Flujo_id=flujo.id)
    sprint = Sprint.objects.get(pk=tablero.id_sprint.id)
    proyecto_seleccionado = Proyecto.objects.get(pk=tablero.id_proyecto.id)
    error = "Ninguno"

    if request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_proyecto_kanban/')

    if request.method == 'POST' and 'Guardar' in request.POST:

        if request.POST.get('nombre_tablero') is not None and request.POST.get('sprint') is not None and request.POST.get("flujo") is not None:
            tablero.nombre_tablero = request.POST.get('nombre_tablero')
            tablero.estado_tablero = request.POST.get('estado')
            tablero.id_sprint = Sprint.objects.get(pk=request.POST.get("sprint"))
            tablero.id_flujo  = Flujo.objects.get(pk=request.POST.get("flujo"))
            tablero.id_proyecto = Proyecto.objects.get(pk=tablero.id_proyecto.id)
            tablero.nombre_proyecto = Proyecto.objects.get(pk=tablero.id_proyecto.id).nombre_proyecto
            tablero.save()
            Sistema().registrar("Modificado tablero "+tablero.nombre_tablero,request.user.username,"Ninguno")
            redireccion = reverse('listar_tablero_kanban_proyecto', args=[tablero.id_proyecto.id])
            return HttpResponseRedirect(redireccion)
        else:
            error = "Incompleto"

    context = {'tablero':tablero,"proyecto":proyecto_seleccionado,"flujos":flujo,"sprints":sprint,"error":error}
    return render_to_response("Gestion_de_tablero_kanban/modificar_tablero.html", context,
                              context_instance=RequestContext(request))

@login_required(login_url="/login/")
def consultar_tablero_kanban_view(request, id_tablero):
    """
    Permite consultar la informacion asociada al tablero
    :param request:
    :param id_tablero:
    :return:
    """
    tablero = TableroKanban.objects.get(pk=id_tablero)
    flujo = Flujo.objects.get(pk=tablero.id_flujo.id)
    actividades = Actividad.objects.filter(id_Flujo_id=flujo.id)
    sprint = Sprint.objects.get(pk=tablero.id_sprint.id)
    proyecto_seleccionado = Proyecto.objects.get(pk=tablero.id_proyecto.id)

    if request.method == 'POST' and 'Volver' in request.POST:
        redireccion = reverse('listar_tablero_kanban_proyecto', args=[tablero.id_proyecto.id])
        return HttpResponseRedirect(redireccion)

    context = {'tablero':tablero,"proyecto":proyecto_seleccionado,"flujos":flujo,"sprints":sprint}
    return render_to_response("Gestion_de_tablero_kanban/consultar_tablero_kanban.html", context,
                              context_instance=RequestContext(request))


