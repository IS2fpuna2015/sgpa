from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from GestiondeSprints.models import Sprint
from GestiondeUserStories.models import UserStory
from datetime import datetime
from GestiondeBurndownChart.models import BurndownChartSprint
from GestiondeProyectos.models import Proyecto
from GestiondeBurndownChart.models import BurndownChartProyecto
from GestiondeSistema.models import Sistema


@login_required(login_url="/login/")
def actualizar_burdownchart_sprint(request,id_sprint):
    """
    Permite la creacion o actualizacion del burndown chart
    :param request:
    :param id_sprint:
    :return:
    """
    sprint_seleccionado = Sprint.objects.get(id=id_sprint)
    fecha_sprint_inicio = datetime.combine(sprint_seleccionado.fecha_inicio , datetime.min.time())
    fecha_sprint_fin = datetime.combine(sprint_seleccionado.fecha_fin , datetime.min.time())
    fecha_actual = datetime.now()
    dias_utilizados = fecha_actual - fecha_sprint_inicio
    dias_utilizados = dias_utilizados.days
    dias_restantes = fecha_sprint_fin - fecha_actual
    error = 'ninguno'

    burn_existente_fecha = BurndownChartSprint()

    try:
        burn_existente_fecha = BurndownChartSprint.objects.get(id_sprint=sprint_seleccionado.id,dia = dias_restantes.days+1)
    except:
        pass


    if request.method == 'POST':
        if request.POST.get('horas_trabajadas') is not None:
            #se guarda el burndown chart
            try:
                burn_existente_fecha = BurndownChartSprint.objects.get(id_sprint=sprint_seleccionado.id,dia = dias_restantes.days+1)
                #Si trae quiere decir que existe y solo se actualizara ese burndown chart
                burn_existente_fecha.horas_trabajadas=request.POST.get('horas_trabajadas')
                burn_existente_fecha.save()
                Sistema().registrar("Modificado burn down chart de sprint " + sprint_seleccionado.nombre_sprint, request.user.username,
                            "Ninguno")
            except:
                #Caso contrario se creara el burndown chart
                BurndownChartSprint(id_sprint=sprint_seleccionado.id,dia = dias_restantes.days+1,horas_trabajadas=request.POST.get('horas_trabajadas')).save()
                Sistema().registrar("Modificado burn down chart de sprint " + sprint_seleccionado.nombre_sprint, request.user.username,
                            "Ninguno")

            redireccion = reverse('listar_sprint', args=[sprint_seleccionado.id_proyecto_id])
            return HttpResponseRedirect(redireccion)
        elif request.POST.get('horas_trabajadas') is None:
            error = "horas"
            context = {"burn":burn_existente_fecha,"sprint":sprint_seleccionado,'fecha':dias_utilizados,'dia_actual':dias_utilizados+1,'dias_restantes':dias_restantes.days,'error':error}
            return render(request, "Gestion_de_BurndownChart/actualizar_burndown_chart_sprint.html",context)

    context = {"burn":burn_existente_fecha,"sprint":sprint_seleccionado,'fecha':dias_utilizados,'dia_actual':dias_utilizados+1,'dias_restantes':dias_restantes.days,'error':error}
    return render(request, "Gestion_de_BurndownChart/actualizar_burndown_chart_sprint.html",context)


@login_required(login_url="/login/")
def visualizar_burdownchart_sprint(request,id_sprint):
    """
    Permite visualizar el burndown chart que es identificado por el id del sprint
    :param request:
    :param id_sprint:
    :return:
    """
    sprint_seleccionado = Sprint.objects.get(id=id_sprint)
    uss = UserStory.objects.filter(nombre_sprint=sprint_seleccionado.nombre_sprint)

    fecha_inicio = sprint_seleccionado.fecha_inicio
    fecha_fin = sprint_seleccionado.fecha_fin
    dias = fecha_fin - fecha_inicio

    #Se obtiene la duracion total de los US asignados al sprint para saber el limite del eje y
    duracion_total_de_us = 0
    for us in uss:
        duracion_total_de_us = duracion_total_de_us + us.size



    #Crea una lista con los dias que durara el sprint para el eje x
    duracion_optima = []
    lista_dias = []
    horas_anteriores = duracion_total_de_us
    contador = 1
    duracion_optima.append(duracion_total_de_us)
    while(contador <=dias.days):
        lista_dias.append(contador)
        duracion_optima.append(horas_anteriores-1)
        contador = contador +1
        horas_anteriores = horas_anteriores -1

    #Se tiene una lista con n elementos, donde n es la cantidad de dias trabajados
    #Se trae de la BD la lista de burndown chart que corresponde a este sprint
    linea_trabajada = []
    burn = BurndownChartSprint.objects.filter(id_sprint=sprint_seleccionado.id)
    horas = duracion_total_de_us
    for item in burn:
        horas = horas -item.horas_trabajadas
        linea_trabajada.append(horas)


    context = {"sprint":sprint_seleccionado, "dias":dias.days,'lista_dias':lista_dias ,'duracion_total_us':duracion_total_de_us,"duracion_optima":duracion_optima,"linea_trabajada":linea_trabajada}
    return render(request, "Gestion_de_BurndownChart/burndown_chart_sprint.html",context)


@login_required(login_url="/login/")
def visualizar_burdownchart_proyecto(request,id_proyecto):
    """
    Permite visualizar el burndown chart que es identificado por el id del proyecto
    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    uss = UserStory.objects.filter(proyecto_id=proyecto.id)

    fecha_inicio = proyecto.fecha_inicio
    fecha_fin = proyecto.fecha_finalizacion
    dias = fecha_fin - fecha_inicio

    #Se obtiene la duracion total de los US asignados al sprint para saber el limite del eje y
    duracion_total_de_us = 0
    for us in uss:
        duracion_total_de_us = duracion_total_de_us + us.size



    #Crea una lista con los dias que durara el sprint para el eje x
    duracion_optima = []
    lista_dias = []
    horas_anteriores = duracion_total_de_us
    contador = 1
    duracion_optima.append(duracion_total_de_us)
    while(contador <=dias.days):
        lista_dias.append(contador)
        duracion_optima.append(horas_anteriores-1)
        contador = contador +1
        horas_anteriores = horas_anteriores -1

    #Se tiene una lista con n elementos, donde n es la cantidad de dias trabajados
    #Se trae de la BD la lista de burndown chart que corresponde a este sprint
    linea_trabajada = []
    burn = BurndownChartProyecto.objects.filter(id_proyecto=proyecto.id)
    horas = duracion_total_de_us
    for item in burn:
        horas = horas -item.horas_trabajadas
        linea_trabajada.append(horas)


    context = {"proyecto":proyecto, "dias":dias.days,'lista_dias':lista_dias ,'duracion_total_us':duracion_total_de_us,"duracion_optima":duracion_optima,"linea_trabajada":linea_trabajada}
    return render(request, "Gestion_de_BurndownChart/burndown_chart_proyecto.html",context)


@login_required(login_url="/login/")
def actualizar_burdownchart_proyecto(request,id_proyecto):
    """
    Permite la creacion o actualizacion del burndown chart por proyecto
    :param request:
    :param id_sprint:
    :return:
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    fecha_proyecto_inicio = datetime.combine(proyecto.fecha_inicio , datetime.min.time())
    fecha_proyecto_fin = datetime.combine(proyecto.fecha_finalizacion , datetime.min.time())
    fecha_actual = datetime.now()
    dias_utilizados = fecha_actual - fecha_proyecto_inicio
    dias_utilizados = dias_utilizados.days
    dias_restantes = fecha_proyecto_fin - fecha_actual
    error = 'ninguno'

    burn_existente_fecha = BurndownChartProyecto()

    try:
        burn_existente_fecha = BurndownChartProyecto.objects.get(id_proyecto=proyecto.id,dia = dias_restantes.days+1)
    except:
        pass


    if request.method == 'POST':
        if request.POST.get('horas_trabajadas') is not None:
            #se guarda el burndown chart
            try:
                burn_existente_fecha = BurndownChartProyecto.objects.get(id_proyecto=proyecto.id,dia = dias_restantes.days+1)
                #Si trae quiere decir que existe y solo se actualizara ese burndown chart
                burn_existente_fecha.horas_trabajadas=request.POST.get('horas_trabajadas')
                burn_existente_fecha.save()
                Sistema().registrar("Modificado burn down chart de proyecto " + proyecto.nombre_proyecto, request.user.username,
                            "Ninguno")
            except:
                #Caso contrario se creara el burndown chart
                BurndownChartProyecto(id_proyecto=proyecto.id,dia = dias_restantes.days+1,horas_trabajadas=request.POST.get('horas_trabajadas')).save()
                Sistema().registrar("Modificado burn down chart de proyecto " + proyecto.nombre_proyecto, request.user.username,
                            "Ninguno")

            redireccion = reverse('listar_proyecto' )
            return HttpResponseRedirect(redireccion)
        elif request.POST.get('horas_trabajadas') is None:
            error = "horas"
            context = {"burn":burn_existente_fecha,"proyecto":proyecto,'fecha':dias_utilizados,'dia_actual':dias_utilizados+1,'dias_restantes':dias_restantes.days,'error':error}
            return render(request, "Gestion_de_BurndownChart/actualizar_burndown_chart_sprint.html",context)

    context = {"burn":burn_existente_fecha,"proyecto":proyecto,'fecha':dias_utilizados,'dia_actual':dias_utilizados+1,'dias_restantes':dias_restantes.days,'error':error}
    return render(request, "Gestion_de_BurndownChart/actualizar_burndown_chart_proyecto.html",context)
