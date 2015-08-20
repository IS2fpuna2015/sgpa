from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.core.urlresolvers import reverse

from .models import Flujo, Actividad
import GestiondeFlujos.forms
from GestiondeProyectos.models import Proyecto
from GestiondeSistema.models import Sistema
from GestiondeProyectos.forms import Proyecto_Buscar_form


@login_required(login_url="/login/")
def crear_flujo_view(request, id_proyecto):
    """
    La funcion Crear Flujo recibe 2 parametros los cuales son, la peticion natural del protocolo HTTP que contiene
    todos los formularios y campos definidos en la pagina visitada por el cliente, ademas
    recibe el identificador del proyecto al cual se desea agregar un flujo de trabajo.

    El flujo en si no posee mas que un campo para designar un nombre que lo describa
    y un identificador asignado automaticamente por el sistema.
    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)

    if request.method == 'POST' and 'Guardar' in request.POST:
        formulario = GestiondeFlujos.forms.crear_flujo_form(request.POST)

        try:
            flujo_prueba = Flujo.objects.get(nombre_flujo=request.POST.get('nombre_flujo'),id_Proyecto=id_proyecto)
            formulario = GestiondeFlujos.forms.crear_flujo_form()
            context = {'formulario':formulario, 'id_proyecto':id_proyecto,'nombre_proyecto':proyecto_seleccionado.nombre_proyecto,"error":"nombre"}
            return render_to_response("Gestion_de_flujos/crear_flujo.html", context, context_instance=RequestContext(request))
        except:
            pass

        if formulario.is_valid():
            nombre_flujo = request.POST.get('nombre_flujo')
            flujo = Flujo(nombre_flujo=nombre_flujo,id_Proyecto=proyecto_seleccionado)
            flujo.save()
            Sistema().registrar("Creado flujo ",request.user.username,"Ninguno")
            redireccion = reverse('listar_flujo', args=[id_proyecto])
            return HttpResponseRedirect(redireccion)


    formulario = GestiondeFlujos.forms.crear_flujo_form()
    context = {'formulario':formulario, 'id_proyecto':id_proyecto,'nombre_proyecto':proyecto_seleccionado.nombre_proyecto}
    return render_to_response("Gestion_de_flujos/crear_flujo.html", context, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def modificar_flujo_view(request, id_proyecto, id_flujo):
    flujo_seleccionado = Flujo.objects.get(pk=id_flujo)
    if request.method == 'POST' and 'Cancelar' in request.POST:
        redireccion = reverse('listar_flujo', args=[id_proyecto])
        return HttpResponseRedirect(redireccion)
    if request.method == 'POST' and 'Guardar' in request.POST:
        flujo_seleccionado.nombre_flujo = request.POST.get('nombre_flujo')
        formulario = GestiondeFlujos.forms.crear_flujo_form(request.POST)
        if formulario.is_valid():
            flujo_seleccionado.save()
            Sistema().registrar("Modificado flujo " +request.POST.get('nombre_flujo'),request.user.username,"Ninguno")
            redireccion = reverse('listar_flujo', args=[id_proyecto])
            return HttpResponseRedirect(redireccion)
        redireccion = reverse('listar_flujo', args=[id_proyecto])
        return HttpResponseRedirect(redireccion)
    context = {'proyecto':id_proyecto,'flujo':flujo_seleccionado}
    return render_to_response("Gestion_de_flujos/modificar_flujo.html", context, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def listar_flujo_view(request, id_proyecto):
    """
    La funcion listar flujo, permite al usuario ver los flujos asociados al proyecto
    que esta siendo consultado en ese momento. Un proyecto puede tener mas de un flujo
    de acuerdo a la estructura organizacional del Equipo encargado del Proyecto, asicomo
    de los requerimientos del producto.

    Recibe 2 parametros las cuales son, la peticion natural del protocolo HTTP que contiene
    todos los formularios y campos definidos en la pagina visitada por el cliente, ademas
    recibe el identificador del proyecto que contiene a esos flujos.
    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)

    if request.method == 'POST':
        formulario = GestiondeFlujos.forms.Busqueda_flujo_form(request.POST)
        if formulario.is_valid():
            busqueda = formulario.cleaned_data.get('Busqueda')
            if busqueda != '':
                flujos = Flujo.objects.filter(id_Proyecto=id_proyecto).filter(nombre_flujo=busqueda)
            elif busqueda == '':
                flujos = Flujo.objects.filter(id_Proyecto=id_proyecto)
        else:
            formulario = GestiondeFlujos.forms.Busqueda_flujo_form()
            flujos = Flujo.objects.filter(id_Proyecto=id_proyecto)
    else:
        formulario = GestiondeFlujos.forms.Busqueda_flujo_form()
        flujos = Flujo.objects.filter(id_Proyecto=id_proyecto)

    context = {'formulario': formulario, 'flujos': flujos,'id_proyecto':id_proyecto,'nombre_proyecto':proyecto_seleccionado.nombre_proyecto,"id_proyecto":id_proyecto}

    return render(request, 'Gestion_de_flujos/listar_flujo.html', context)


@login_required(login_url="/login/")
def eliminar_flujo_view(request,id_proyecto, id_flujo):
    flujo_seleccionado = Flujo.objects.get(pk=id_flujo)
    nombre = flujo_seleccionado.nombre_flujo

    if request.method == 'POST' and 'Aceptar' in request.POST:
        flujo_seleccionado.delete()
        Sistema().registrar("Eliminado flujo " +nombre,request.user.username,"Ninguno")
        redireccion = reverse('listar_flujo', args=[id_proyecto])
        return HttpResponseRedirect(redireccion)
    if request.method == 'POST' and 'Cancelar' in request.POST:
        redireccion = reverse('listar_flujo', args=[id_proyecto])
        return HttpResponseRedirect(redireccion)

    return render(request,"Gestion_de_flujos/eliminar_flujo.html" ,{'nombre':nombre})


@login_required(login_url="/login/")
def consultar_flujo_view(request, id_flujo,id_proyecto):
    """
    Permite realizar la consulta de un flujo que es especificado por su id
    :param request:
    :param id_flujo:contiene el id del flujo que sera consultado
    :return:retornara los datos del flujo que se consulto
    """
    flujo_seleccionado = Flujo.objects.get(pk=id_flujo)
    proyecto = Proyecto.objects.get(id=id_proyecto)
    actividades = Actividad.objects.filter(id_Flujo_id=id_flujo)
    context = {"flujo_seleccionado":flujo_seleccionado,"proyecto":proyecto,"actividades":actividades}
    return render(request, "Gestion_de_flujos/consultar_flujo.html", context)


@login_required(login_url="/login/")
def agregar_actividad_view(request,id_flujo,id_proyecto):
    """
    La funcion agregar actividad es referenciada en el template como crear actividad,
    la misma recibe tres parametros, la peticion natural del protocolo HTTP que contiene
    todos los formularios y campos definidos en la pagina visitada por el cliente, ademas
    recibe los identificadores del flujo y del proyecto a los cuales se desea agregar una
    actividad, la cual puede estar en uno de los siguientes estados predeterminados por
    los requerimientos funcionales, Pendiente, En proceso y Completo.

    Cada campo mostrado en la plantilla debe ser completado, ya sea por el usuario o de
    manera automatica por el sistema.

    Los campos completados automaticamente por el sistema son, identificador del flujo,
    identificador del proyecto e identificador de la actividad; el resto de los campos
    deben ser rellenados por el usuario.

    Una actividad  dentro del mismo estado no puede tener el mismo nombre.
    :param request:
    :param id_flujo:
    :param id_proyecto:
    :return:
    """
    flujo_seleccionado = Flujo.objects.get(pk=id_flujo)


    #Si el usuario guarda la actividad se asocia el formulario a una variable y se confirma la validez de los datos
    if request.method == 'POST' and 'Guardar' in request.POST:
        formulario_actividad = GestiondeFlujos.forms.crear_actividad_form(request.POST)
        ultima_actividad = Actividad.objects.filter(id_Flujo=flujo_seleccionado.id).filter(estado_actividad=request.POST.get('estado_actividad')).aggregate(Max('orden_actividad'))
        nombre_actividad_nueva = request.POST.get('nombre_actividad')
        estado_actividad_nueva = request.POST.get('estado_actividad')


        if not ultima_actividad.get('orden_actividad__max'):
            orden_actividad_nueva = 1
        else:
            orden_actividad_nueva = ultima_actividad.get('orden_actividad__max')+1

        if formulario_actividad.is_valid():
            if Actividad.objects.filter(nombre_actividad=nombre_actividad_nueva,id_Flujo_id=id_flujo).exists() and Actividad.objects.filter(estado_actividad=estado_actividad_nueva).exists():
                context = {'formulario':formulario_actividad, 'flujo':flujo_seleccionado,'error': 'existente',"id_proyecto":id_proyecto,'id_flujo':id_flujo}
                return render_to_response("Gestion_de_flujos/crear_actividad.html",
                                          context,
                                          context_instance=RequestContext(request))
            else:
                actividad = Actividad()
                actividad.id_Flujo = flujo_seleccionado
                actividad.nombre_actividad = nombre_actividad_nueva
                actividad.estado_actividad = estado_actividad_nueva
                actividad.orden_actividad = orden_actividad_nueva
                actividad.save()
                Sistema().registrar("Creada actividad " +actividad.nombre_actividad,request.user.username,"Ninguno")


            flujo_seleccionado = Flujo.objects.get(pk=id_flujo)
            actividades_todo = Actividad.objects.filter(id_Flujo=flujo_seleccionado.id).filter(estado_actividad='todo').order_by('orden_actividad')
            actividades_doing = Actividad.objects.filter(id_Flujo=flujo_seleccionado.id).filter(estado_actividad='doing').order_by('orden_actividad')
            actividades_done = Actividad.objects.filter(id_Flujo=flujo_seleccionado.id).filter(estado_actividad='done').order_by('orden_actividad')
            context = {'actividades_todo': actividades_todo, 'actividades_doing':actividades_doing, 'actividades_done':actividades_done, 'flujo':flujo_seleccionado,"id_proyecto":id_proyecto, 'error': 'ninguno','id_flujo':id_flujo}
            return render_to_response("Gestion_de_flujos/listar_actividad.html", context, context_instance=RequestContext(request))

    elif request.method == 'POST' and 'GuardarContinuar' in request.POST:
        # Si el usuario guarda y desea continuar agregando actividades, simplemente
        # agrega el boton Guardar y Continuar, el cual tendra un efecto parecido al
        # guardado normal , pero le redirecciona al usuario a la pantalla de creacion de
        # una actividad en blanco

        formulario_actividad = GestiondeFlujos.forms.crear_actividad_form(request.POST)
        ultima_actividad = Actividad.objects.filter(id_Flujo=flujo_seleccionado.id).filter(estado_actividad=request.POST.get('estado_actividad')).aggregate(Max('orden_actividad'))
        nombre_actividad_nueva = request.POST.get('nombre_actividad')
        estado_actividad_nueva = request.POST.get('estado_actividad')

        if not ultima_actividad.get('orden_actividad__max'):
            orden_actividad_nueva = 1
        else:
            orden_actividad_nueva = ultima_actividad.get('orden_actividad__max')+1

        if formulario_actividad.is_valid():
            if Actividad.objects.filter(nombre_actividad=nombre_actividad_nueva).exists() and Actividad.objects.filter(estado_actividad=estado_actividad_nueva).exists():
                context = {'formulario':formulario_actividad, 'flujo':flujo_seleccionado,'error': 'existente',"id_proyecto":id_proyecto,'id_flujo':id_flujo}
                return render_to_response("Gestion_de_flujos/crear_actividad.html",
                                          context,
                                          context_instance=RequestContext(request))
            else:
                actividad = Actividad()
                actividad.id_Flujo = flujo_seleccionado
                actividad.nombre_actividad = nombre_actividad_nueva
                actividad.estado_actividad = estado_actividad_nueva
                actividad.orden_actividad = orden_actividad_nueva
                actividad.save()
                Sistema().registrar("Creada actividad " +actividad.nombre_actividad,request.user.username,"Ninguno")

            formulario = GestiondeFlujos.forms.crear_actividad_form()
            context = {'formulario':formulario, 'error':'ninguno','id_flujo':id_flujo,"id_proyecto":id_proyecto}
            return render_to_response("Gestion_de_flujos/crear_actividad.html", context,context_instance=RequestContext(request))
        else:
            if nombre_actividad_nueva == '' or estado_actividad_nueva == '':
                return render_to_response("Gestion_de_flujos/crear_actividad.html", {'error': 'vacio','id_flujo':id_flujo,'id_proyecto':id_proyecto},context_instance=RequestContext(request))

    formulario_actividad = GestiondeFlujos.forms.crear_actividad_form()
    context = {'formulario':formulario_actividad, 'flujo':flujo_seleccionado,'id_flujo':id_flujo,"id_proyecto":id_proyecto}

    return render_to_response("Gestion_de_flujos/crear_actividad.html/", context, context_instance=RequestContext(request),)

@login_required(login_url="/login/")
def listar_actividad_view(request, id_flujo,id_proyecto):
    """
    La funcion listar actividad, tambien recibe tres parametros al igual que la funcion
    agregar actividad, los cuales son: la peticion natural del protocolo HTTP que contiene
    todos los formularios y campos definidos en la pagina visitada por el cliente, ademas
    recibe los identificadores del flujo y del proyecto a los cuales poseen las actividades\
    a ser listadas.
    :param request:
    :param id_proyecto:
    :param id_flujo:
    :return:
    """
    flujo_seleccionado = Flujo.objects.get(pk=id_flujo)
    actividades_todo = Actividad.objects.filter(id_Flujo=flujo_seleccionado.id).filter(estado_actividad='todo').order_by('orden_actividad')
    if actividades_todo:
        primera_actividad_orden = actividades_todo[0].orden_actividad
        if primera_actividad_orden != 1:
            reordenar_actividad(actividades_todo)
    actividades_doing = Actividad.objects.filter(id_Flujo=flujo_seleccionado.id).filter(estado_actividad='doing').order_by('orden_actividad')
    if actividades_doing:
        primera_actividad_orden = actividades_doing[0].orden_actividad
        if primera_actividad_orden != 1:
            reordenar_actividad(actividades_doing)
    actividades_done = Actividad.objects.filter(id_Flujo=flujo_seleccionado.id).filter(estado_actividad='done').order_by('orden_actividad')
    if actividades_done:
        primera_actividad_orden = actividades_done[0].orden_actividad
        if primera_actividad_orden != 1:
            reordenar_actividad(actividades_done)
    context = {'actividades_todo': actividades_todo, 'actividades_doing':actividades_doing, 'actividades_done':actividades_done, 'id_flujo':id_flujo,"id_proyecto":id_proyecto,"flujo":flujo_seleccionado}

    return render_to_response("Gestion_de_flujos/listar_actividad.html", context, context_instance=RequestContext(request))

def reordenar_actividad(actividades):
    indice = 1
    for actividad_cambiar in actividades:
        actividad_cambiar.orden_actividad = indice
        actividad_cambiar.save()
        indice+=1
@login_required(login_url="/login/")
def modificar_actividad_view(request, id_proyecto, id_flujo, id_actividad):
    """
    La funcion modificar recibe 4 parametros, los cuales son: la peticion natural del protocolo HTTP que contiene
    todos los formularios y campos definidos en la pagina visitada por el cliente, los identificadores del flujo,
    del proyecto y de la actividad a ser modificada.

    Si el usuario coloca una orden de secuencia fuera de los valores limites el sistema
    alertara al usuario de esta situacion y si utiliza un secuencia ya utilizada intercambia
    los valores entre las actividades afectadas.
    :param request:
    :param id_proyecto:
    :param id_flujo:
    :param id_actividad:
    :return:
    """
    actividad_seleccionada = Actividad.objects.get(pk=id_actividad)
    proyecto_actual = Proyecto.objects.get(pk=id_proyecto)
    flujo_actual = Flujo.objects.get(pk=id_flujo)
    actividad_cambiar = {}
    flag = 0

    if request.method == 'POST' and 'Cancelar' in request.POST:
        redireccion = reverse('listar_actividad', args=[id_proyecto,id_flujo])
        return HttpResponseRedirect(redireccion)


    if request.method == 'POST' and 'Guardar' in request.POST:
        try:
            orden_temporal = int(request.POST.get('orden_actividad'))

            ultima_actividad_orden = Actividad.objects.filter(id_Flujo=id_flujo).filter(estado_actividad=actividad_seleccionada.estado_actividad).aggregate(Max('orden_actividad'))
            if not ultima_actividad_orden.get('orden_actividad__max'):
                flag = 1
                actividad_seleccionada.orden_actividad = 1
            elif orden_temporal == 0 or orden_temporal>int(ultima_actividad_orden.get('orden_actividad__max')):
                print("Error!! El orden esta fuera del rango")
                formulario = GestiondeFlujos.forms.modificar_actividad_form(request.POST)
                error = 'fuera_de_orden'
                context = {'formulario':formulario,'proyecto':proyecto_actual, 'flujo':flujo_actual, 'actividad':actividad_seleccionada, 'error':error}
                return render_to_response("Gestion_de_flujos/modificar_actividad.html", context,
                                  context_instance=RequestContext(request))
            else:
                if orden_temporal != actividad_seleccionada.orden_actividad:
                    orden_vieja = actividad_seleccionada.orden_actividad
                    actividad_cambiar = Actividad.objects.filter(estado_actividad=actividad_seleccionada.estado_actividad).get(orden_actividad=orden_temporal)
                    actividad_cambiar.orden_actividad = orden_vieja
                    actividad_seleccionada.orden_actividad = orden_temporal
                else:
                    flag = 1
            formulario = GestiondeFlujos.forms.modificar_actividad_form(request.POST)
            if formulario.is_valid():
                actividad_seleccionada.nombre_actividad = request.POST.get('nombre_actividad')
                actividad_seleccionada.estado_actividad = request.POST.get('estado_actividad')
                actividad_seleccionada.save()
                if flag == 0:
                    actividad_cambiar.save()
                    Sistema().registrar("Modificada actividad " +actividad_seleccionada.nombre_actividad,request.user.username,"Ninguno")
                    redireccion = reverse('listar_actividad', args=[id_proyecto,id_flujo])
                    return HttpResponseRedirect(redireccion)
            actividades_a_verificar_orden = Actividad.objects.filter(id_Flujo=id_flujo).filter(estado_actividad=actividad_seleccionada.estado_actividad).order_by('orden_actividad')
            primera_actividad_orden = actividades_a_verificar_orden[0]
            if unica_actividad_orden(id_flujo,actividad_seleccionada.estado_actividad,orden_temporal) == False or primera_actividad_orden != 1:
                actividades_a_modificar_orden = Actividad.objects.filter(id_Flujo=id_flujo).filter(estado_actividad=actividad_seleccionada.estado_actividad).order_by('orden_actividad')
                indice = 1
                for actividad_cambiar in actividades_a_modificar_orden:
                    actividad_cambiar.orden_actividad = indice
                    actividad_cambiar.save()
                    indice+=1
            redireccion = reverse('listar_actividad', args=[id_proyecto,id_flujo])
            return HttpResponseRedirect(redireccion)
        except ValueError:
            orden_temporal = request.POST.get('orden_actividad')
            if orden_temporal == '':
                print("Error!! El orden no puede estar vacio")
                formulario = GestiondeFlujos.forms.modificar_actividad_form(request.POST)
                error = 'vacio'
                context = {'formulario':formulario,'proyecto':proyecto_actual, 'flujo':flujo_actual, 'actividad':actividad_seleccionada, 'error':error}
                return render_to_response("Gestion_de_flujos/modificar_actividad.html", context,
                                  context_instance=RequestContext(request))
            print("Error!! El tipo de campo debe ser numerico")
            formulario = GestiondeFlujos.forms.modificar_actividad_form(request.POST)
            error = 'tipo_de_dato'
            context = {'formulario':formulario,'proyecto':proyecto_actual, 'flujo':flujo_actual, 'actividad':actividad_seleccionada, 'error':error}
            return render_to_response("Gestion_de_flujos/modificar_actividad.html", context,
                              context_instance=RequestContext(request))




    formulario = GestiondeFlujos.forms.modificar_actividad_form()
    context = {'formulario':formulario,'proyecto':proyecto_actual, 'flujo':flujo_actual, 'actividad':actividad_seleccionada}
    return render_to_response("Gestion_de_flujos/modificar_actividad.html", context,
                              context_instance=RequestContext(request))

def unica_actividad_orden(id_flujo, estado, orden_temporal ):
    try:
        actividad_unica = Actividad.objects.filter(id_Flujo=id_flujo).filter(estado_actividad=estado).order_by(orden_temporal)
        return True
    except:
        return False

@login_required(login_url="/login/")
def eliminar_actividad_view(request, id_proyecto, id_flujo, id_actividad):
    actividad_seleccionada = Actividad.objects.get(pk=id_actividad)
    nombre = actividad_seleccionada.nombre_actividad
    if request.method == 'POST' and 'Aceptar' in request.POST:
        actividad_seleccionada.delete()
        Sistema().registrar("Eliminada actividad " +actividad_seleccionada.nombre_actividad,request.user.username,"Ninguno")
        redireccion = reverse('listar_actividad', args=[id_proyecto,id_flujo])
        return HttpResponseRedirect(redireccion)
    if request.method == 'POST' and 'Cancelar' in request.POST:
        redireccion = reverse('listar_actividad', args=[id_proyecto,id_flujo])
        return HttpResponseRedirect(redireccion)

    return render(request,"Gestion_de_flujos/eliminar_flujo.html" ,{'nombre':nombre,'id_proyecto':id_proyecto,'id_flujo':id_flujo})


@login_required(login_url="/login/")
def listar_proyecto_flujo_view(request):
    """
    Permite listar proyectos para seleccionar el proyecto para crear un flujo
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
    return render(request, 'Gestion_de_flujos/listar_proyecto_para_crear_flujo.html', context)


@login_required(login_url="/login/")
def listar_proyecto_flujos_listado_view(request):
    """
    Permite listar proyectos para seleccionar el proyecto del cual se  listaran los flujos
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
    return render(request, 'Gestion_de_flujos/listar_proyecto_para_listar_flujo.html', context)


