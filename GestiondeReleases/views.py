from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from GestiondeProyectos.forms import Proyecto_Buscar_form
from GestiondeProyectos.models import Proyecto
from GestiondeReleases.forms import Release_Buscar_form
from GestiondeReleases.models import Release
from GestiondeSistema.models import Sistema
from GestiondeUserStories.models import UserStory


@login_required(login_url="/login/")
def crear_release_view(request, id_proyecto):

    """
    Permite crear un release en un proyecto seleccinado
    :param request:
    :param id_proyecto:
    :return:
    """
    releases  = Release.objects.all().order_by('-fecha')
    if len(releases):
        version_anterior = "La version del release anterior es el " + releases[0].version
    else:
        version_anterior = "Este es el primer Release del proyecto"

    userstories = UserStory.objects.filter(proyecto=id_proyecto).filter(estado='APROBADO').filter(release__isnull=True)
    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)

    if request.method=='POST' and 'Guardar' in request.POST:
        nombre = request.POST.get('nombre_release')
        version  = request.POST.get('version_release')
        descripcion = request.POST.get('descripcion_release')
        us_seleccionados_id = request.POST.getlist('us_seleccionados')

        if nombre == '' or version == '' or descripcion == '':
            context = {'version_anterior':version_anterior,'userstories':userstories,'error':'campos','nombre_proyecto':proyecto_seleccionado.nombre_proyecto}
            return render(request,'Gestion_de_Releases/crear_release.html',context)

        if len(us_seleccionados_id) == 0:
            context = {'version_anterior':version_anterior,'userstories':userstories,'error':'seleccion_us','nombre_proyecto':proyecto_seleccionado.nombre_proyecto}
            return render(request,'Gestion_de_Releases/crear_release.html',context)

        release = Release(nombre=nombre,version=version,descripcion=descripcion,proyecto=proyecto_seleccionado)
        release.save()

        for us_seleccionado_id in us_seleccionados_id:
            us_tmp  = UserStory.objects.get(pk=us_seleccionado_id)
            us_tmp.release = release
            us_tmp.save()

            Sistema().registrar("Creacion de Release en el proyecto " + proyecto_seleccionado.nombre_proyecto, request.user.username,"Ninguno")

        redireccion = reverse('listar_releases_proyecto', args=[id_proyecto])
        return HttpResponseRedirect(redireccion)

    context = {'version_anterior':version_anterior,'userstories': userstories, 'error': 'ninguno', 'nombre_proyecto': proyecto_seleccionado.nombre_proyecto}
    return render(request, 'Gestion_de_Releases/crear_release.html', context)


@login_required(login_url="/login/")
def listar_releases_view(request, id_proyecto):
    """
    Permite listar releases de un proyecto seleccinado
    :param request:
    :param id_proyecto:
    :return:
    """

    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)

    if request.method == 'POST':
        form = Release_Buscar_form(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data.get('Busqueda')
            if busqueda == '':
                releases = Release.objects.filter(proyecto=proyecto_seleccionado)
            else:
                releases = Release.objects.filter(proyecto=proyecto_seleccionado).filter(nombre=busqueda)
        else:
            form = Release_Buscar_form()
    else:
        form = Release_Buscar_form()
        releases = Release.objects.filter(proyecto=proyecto_seleccionado)

    Sistema().registrar("Listado de Releases del proyecto " + proyecto_seleccionado.nombre_proyecto, request.user.username,"Ninguno")

    context = {'form':form,'releases':releases,'nombre_proyecto':proyecto_seleccionado.nombre_proyecto}
    return render(request,'Gestion_de_Releases/lista_releases_de_proyecto.html',context)


@login_required(login_url="/login/")
def listar_proyectos_release_view(request):
    """
    Permite listar proyectos para determinar la accion a tomar, crear o listar releases
    :param request:
    :return:
    """
    usuario = request.user
    misproyectos = []
    for proyectotmp in Proyecto.objects.all():
        if proyectotmp.scrum_master.id == usuario.id:
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

    ## para no hacer un duplicado de views y de template, el parametro a es una abreviatura de accion
    context['tipo_accion']=request.GET['a']

    return render(request, 'Gestion_de_Releases/seleccionar_proyecto_accion_release.html', context)

@login_required(login_url="/login")
def consultar_release_view(request, id_release):
    """
    Permite la consulta de un release a partir del proyecto que es seleccionado
    :param request:
    :param id_proyecto:
    :return:
    """

    release_seleccionado = Release.objects.get(pk=id_release)
    userstories_de_release = release_seleccionado.userstory_set.all()
    context = {'release':release_seleccionado,'userstories':userstories_de_release}

    Sistema().registrar("Consuldta de " + release_seleccionado.nombre, request.user.username,"Ninguno")

    return render(request,'Gestion_de_Releases/consultar_release.html',context)