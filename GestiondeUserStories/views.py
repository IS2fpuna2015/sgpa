from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from GestiondeProyectos.models import Proyecto
from GestiondeSistema.models import Sistema
from GestiondeUsuarios.models import Usuario
from sgpa.Util import generarcodigo, usuario_es_scrum_de_proyecto
from GestiondeUserStories.forms import CrearUserStoryForm, Busqueda_UserStory_form, ModificarUserStoryForm, \
    ModificarUserStoryFormDesarrollador
from GestiondeUserStories.models import UserStory
from GestiondeProyectos.forms import Proyecto_Buscar_form
import os
from os.path import abspath, dirname
import shutil

from .forms import FileAttached_form
from .models import FileAttached_model, Comentario
from .models import FileAttached_model, File
from .storage import DatabaseStorage
from sgpa import settings
from django.utils import datetime_safe
from GestiondeFlujos.models import Flujo
from GestiondeSprints.models import Sprint


import os
import mimetypes
import base64
from django.core import files
from reportlab.platypus import SimpleDocTemplate, Table
@login_required(login_url="/login/")
def crear_userstory_view(request, id_proyecto):
    """
    La funcion Crear User Story recibe 2 parametros los cuales son, la peticion natural del protocolo HTTP que contiene
    todos los formularios y campos definidos en la pagina visitada por el cliente, ademas
    recibe el identificador del proyecto al cual se desea agregar un User Story.
    :param request:
    :param id_proyecto:
    :return:
    """
    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)

    formulario = CrearUserStoryForm(proyecto_seleccionado)
    upload_form = FileAttached_form()
    archivo = ''
    error = 'sinerrores'

    if request.method == 'POST' and 'Guardar' in request.POST:
        formulario = CrearUserStoryForm(proyecto_seleccionado, request.POST)

        if formulario.is_valid():
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            prioridad = request.POST.get('prioridad')
            valor_tecnico = request.POST.get('valor_tecnico')
            valor_de_negocio = request.POST.get('valor_de_negocio')
            usuario_asignado = None

            proyecto = proyecto_seleccionado
            size = request.POST.get('size')

            newuserstory = UserStory(nombre=nombre,descripcion=descripcion,prioridad=prioridad,
                                     valor_de_negocio=valor_de_negocio,valor_tecnico=valor_tecnico,
                                     usuario_asignado=usuario_asignado,proyecto=proyecto,size=size)

            try:
                #Si me trae el siguiente us_prueba, quiere decir que ya existe en la BD, se debe cambiar el nombre
                us_prueba = UserStory.objects.get(nombre=nombre,proyecto=proyecto)
                error = 'nombre'

                formulario = CrearUserStoryForm(proyecto_seleccionado)
                context = {'formulario': formulario, 'error': error,'id_proyecto':id_proyecto,'nombre_proyecto':proyecto_seleccionado.nombre_proyecto}
                return render(request, 'Gestion_de_UserStories/crear_userstory.html', context)
            except:
                pass

            newuserstory.save()
            try:
                if FileAttached_model.objects.filter(userstory_id=0) != None:
                    archivo_unico = FileAttached_model.objects.get(userstory_id=0)
                    archivo_unico.userstory_id = newuserstory.id
                    archivo_unico.save()
                else:
                    print('no archivo')
            except:
                pass
            codigo = generarcodigo(newuserstory.id, proyecto_seleccionado.codigo_proyecto)
            newuserstory.codigo = codigo
            newuserstory.save()
            Sistema().registrar("Creado User Story "+nombre,request.user.username,"Ninguno")
            redireccion = reverse('listar_userstories_proyecto', args=[id_proyecto])

            return HttpResponseRedirect(redireccion)
        else:
            error = 'campos'
            print(formulario.errors)

    formulario = CrearUserStoryForm(proyecto_seleccionado)
    context = {'formulario': formulario, 'error': error, 'id_proyecto': id_proyecto,
               'nombre_proyecto': proyecto_seleccionado.nombre_proyecto}
    if request.method == 'POST' and 'Upload' in request.POST:
        if request.FILES:
            fecha_path = str(datetime_safe.date.today()).split("-")
            archivo_request = request.FILES['image']
            archivo = FileAttached_model()
            archivo.file = archivo_request
            archivo.file_name = archivo_request.name
            archivo.file_path = settings.MEDIA_URL + 'subidos/'+fecha_path[0]+'/'+fecha_path[1]+'/'+fecha_path[2]+'/'
            archivo.file_type = archivo_request.content_type
            archivo.save()
            formulario_lleno = CrearUserStoryForm(proyecto_seleccionado,request.POST)


            #print(formulario_lleno.nombre)

            return render_to_response("Gestion_de_UserStories/crear_userstory.html", {'formulario':formulario_lleno,'error': error,'id_proyecto':id_proyecto,'nombre_proyecto':proyecto_seleccionado.nombre_proyecto},
                              context_instance=RequestContext(request))

        else:
            print('No files')

    context = {'formulario': formulario, 'error': error,'id_proyecto':id_proyecto,'nombre_proyecto':proyecto_seleccionado.nombre_proyecto, 'form_popup':upload_form}

    return render(request, 'Gestion_de_UserStories/crear_userstory.html', context)


@login_required(login_url="/login/")
def modificar_userstory_view(request, id_userStory):
    """
    Permite realizar la modificacion de un user story
    :param request:
    :return:
    """
    usuario = request.user
    us_seleccionado = UserStory.objects.get(pk=id_userStory)
    proyecto = us_seleccionado.proyecto
    upload_form = FileAttached_form()
    usuario_es_scrum = proyecto.scrum_master.id == usuario.id
    usuario_es_desarrollador = proyecto.equipo_desarrollo.filter(pk=usuario.id).exists()
    archivo = ''

    if not usuario_es_scrum and not usuario_es_desarrollador:
        print("chau!")



    if request.method == 'POST' and 'Guardar' in request.POST:

        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        prioridad =request.POST.get('prioridad')
        estado = request.POST.get('estado')
        valor_de_negocio = request.POST.get('valor_de_negocio')
        valor_tecnico = request.POST.get('valor_tecnico')
        porcentaje_realizado = request.POST.get('porcentaje_realizado')
        usuario_asignado = request.POST.get('usuario_asignado')
        size = request.POST.get('size')
        comentario_us = request.POST.get('comentario')
        horas_trabajadas = request.POST.get('horas_trabajadas')


        try:
            sprint_seleccionado = Sprint.objects.get(id=request.POST.get('sprint'))
            nombre_sprint = sprint_seleccionado.nombre_sprint
        except:
            nombre_sprint = "No Asignado"


        try:
            if FileAttached_model.objects.get(userstory_id=0) != None:
                archivo = FileAttached_model.objects.get(userstory_id=0)
                archivo.userstory_id = id_userStory
                archivo.save()
        except:
            pass

        if usuario_es_scrum:
            formulario = ModificarUserStoryForm(us_seleccionado.proyecto,us_seleccionado.estado,us_seleccionado.porcentaje_realizado,sprint_inicial=us_seleccionado.nombre_sprint,instance=us_seleccionado)

            if nombre=='' or descripcion==''  or size=='' or horas_trabajadas =='':
                context = {'formulario': formulario, 'error': 'campos','userstory': us_seleccionado, 'usuario_es_scrum': usuario_es_scrum,
               'usuario_es_desarrollador': usuario_es_desarrollador}
                return render(request, 'Gestion_de_UserStories/modificar_userstory.html', context)

            us_seleccionado.nombre = nombre
            us_seleccionado.descripcion = descripcion
            us_seleccionado.prioridad = prioridad
            us_seleccionado.estado = estado
            us_seleccionado.valor_de_negocio = valor_de_negocio
            us_seleccionado.valor_tecnico = valor_tecnico
            us_seleccionado.porcentaje_realizado = porcentaje_realizado
            us_seleccionado.nombre_sprint = nombre_sprint

            if comentario_us != "":
                comentario = Comentario(comentario=comentario_us,autor=request.user.username,us_id=id_userStory)
                comentario.save()

            if not usuario_asignado is None :
                if usuario_asignado=='':
                    us_seleccionado.usuario_asignado = None
                else:
                    us_seleccionado.usuario_asignado = Usuario.objects.get(pk=usuario_asignado)

            us_seleccionado.size = size
            us_seleccionado.horas_dedicadas+= int(horas_trabajadas)
            us_seleccionado.save()
            Sistema().registrar("Se modifico User Story", request.user.username, "Ninguno")

        else:
            formulario = ModificarUserStoryFormDesarrollador(us_seleccionado.estado,us_seleccionado.porcentaje_realizado)
            if horas_trabajadas =='':
                context = {'formulario': formulario, 'error': 'campos','userstory': us_seleccionado, 'usuario_es_scrum': usuario_es_scrum,
               'usuario_es_desarrollador': usuario_es_desarrollador}
                return render(request, 'Gestion_de_UserStories/modificar_userstory.html', context)


            us_seleccionado.porcentaje_realizado = request.POST.get('porcentaje_realizado')
            us_seleccionado.horas_dedicadas+= int(horas_trabajadas)
            us_seleccionado.estado = estado
            us_seleccionado.save()

            Sistema().registrar("Se modifico User Story ", request.user.username, "Ninguno")

        redireccion = reverse('listar_userstories_proyecto', args=[us_seleccionado.proyecto.id])
        return HttpResponseRedirect(redireccion)

    if request.method == 'POST' and 'Upload' in request.POST:
        if request.FILES:
            fecha_path = str(datetime_safe.date.today()).split("-")
            archivo_request = request.FILES['image']
            archivo = FileAttached_model()
            archivo.file = archivo_request
            archivo.file_name = archivo_request.name
            archivo.file_path = settings.MEDIA_URL + 'subidos/'+fecha_path[0]+'/'+fecha_path[1]+'/'+fecha_path[2]+'/'
            archivo.file_type = archivo_request.content_type
            archivo.save()
            formulario_lleno = ModificarUserStoryForm(us_seleccionado.proyecto,us_seleccionado.estado,us_seleccionado.porcentaje_realizado,sprint_inicial=us_seleccionado.nombre_sprint,instance=us_seleccionado)
            return render_to_response("Gestion_de_UserStories/modificar_userstory.html", {'formulario':formulario_lleno, 'userstory': us_seleccionado, 'usuario_es_scrum': usuario_es_scrum,'usuario_es_desarrollador': usuario_es_desarrollador},
                              context_instance=RequestContext(request))

        else:
            print('No files')

    if usuario_es_scrum:

        formulario = ModificarUserStoryForm(us_seleccionado.proyecto,us_seleccionado.estado,us_seleccionado.porcentaje_realizado,sprint_inicial=us_seleccionado.nombre_sprint,instance=us_seleccionado)
    else:
        formulario = ModificarUserStoryForm(us_seleccionado.proyecto,us_seleccionado.estado,us_seleccionado.porcentaje_realizado,sprint_inicial=us_seleccionado.nombre_sprint,instance=us_seleccionado)


    context = {'formulario': formulario, 'userstory': us_seleccionado, 'usuario_es_scrum': usuario_es_scrum,
               'usuario_es_desarrollador': usuario_es_desarrollador,'upload_form':upload_form}
    return render_to_response("Gestion_de_UserStories/modificar_userstory.html", context,
                              context_instance=RequestContext(request))


@login_required(login_url="/login/")
def listar_userstories_proyecto_view(request, id_proyecto):
    """
     Permite al usuario realizar el listado de userstories que pertenecen a un proyecto determinado
     habilitado con la opcion de filtrados de userstories por nombre, tambien habilitara el boton para
     modificar o consultar si es que posee los permisos el usuario en sesion.
     :param request:
     :return:
     """
    proyecto_seleccionado = Proyecto.objects.get(pk=id_proyecto)
    nombre_proyecto = proyecto_seleccionado.nombre_proyecto

    usuario_es_scrum = usuario_es_scrum_de_proyecto(request.user,proyecto_seleccionado)

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

    context = {'formulario': form, 'userstories': userstories, "nombre_proyecto": nombre_proyecto,
               "id_proyecto": id_proyecto,'usuario_es_scrum':usuario_es_scrum}

    return render(request, 'Gestion_de_UserStories/listar_userstories_proyecto.html', context)


@login_required(login_url="/login/")
def consultar_userstory_view(request, id_userStory):
    """
    Permite realizar la consulta de un user story en especifico
    :param request:
    :return:
    """
    template_filename = ''
    us_seleccionado = UserStory.objects.get(pk=id_userStory)
    metadata_file_userstory = ''
    boton_imagen = False
    fileName = ''
    try:
        metadata_file_userstory = FileAttached_model.objects.get(userstory_id=id_userStory)
        id_file = str(metadata_file_userstory.file).split(".")
        archivo_codificado = File.objects.get(pk=int(id_file[0]))
        archivo_decodificado = base64.b64decode(archivo_codificado.content)

        if 'image' in metadata_file_userstory.file_type:
            fileName = os.path.join(settings.BASE_DIR, "static") + '/' + metadata_file_userstory.file_name
            writeFile(archivo_decodificado, fileName, {'error':''})
            template_filename = settings.STATIC_URL+'/'+metadata_file_userstory.file_name
            boton_imagen = True

        if request.method == 'POST' and 'Ver_Archivo' in request.POST:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
            elementos = []
            cm = 2.54
            doc = SimpleDocTemplate(response, rightMargin=0, leftMargin=0.1 * cm, topMargin=0.3 * cm, bottomMargin=0)
            data = [[archivo_decodificado]]
            table = Table(data,colWidths=460, hAlign='LEFT')
            elementos.append(table)
            doc.build(elementos)
            return response

        if request.method == 'POST' and 'descargar_imagen' in request.POST:
            homedir = os.environ['HOME']
            if not homedir+'/'+'Descargas':
                os.mkdir(homedir+'/'+'Descargas', 0o777)
            descargasdir = homedir+'/'+'Descargas'
            try:
                shutil.copy(fileName, descargasdir)
            except:
                pass
    except:
        pass


    if request.method == 'POST' and 'Volver' in request.POST:
        print(request.POST)
        redireccion = reverse('listar_userstories', args=[us_seleccionado.proyecto.id])
        return HttpResponseRedirect(redireccion)

    return render_to_response("Gestion_de_UserStories/consultar_userstory.html", {"userstory": us_seleccionado, "files":metadata_file_userstory, "Temp_fileName":template_filename,"Boton_imagen":boton_imagen},
                              context_instance=RequestContext(request))


@login_required(login_url="/login/")
def listar_todos_us_view(request):
    """
    Lista todos los sprints que se encuentran en en la BD
    :param request:
    :return:
    """
    usuario = request.user
    userStories = UserStory.objects.filter(usuario_asignado=usuario)

    proyectos = []
    for us in userStories:
        proyectos.append(Proyecto.objects.get(id=us.proyecto_id))

    list = zip(userStories,proyectos)

    context = {'list':list}
    return render(request, 'Gestion_de_UserStories/listar_todos_us.html', context)


@login_required(login_url="/login/")
def listar_proyecto_us_view(request):
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
    return render(request, 'Gestion_de_UserStories/listar_proyecto_para_crear_us.html', context)

@login_required(login_url="/login/")
def listar_comentarios_us_view(request,id_userStory):
    us = UserStory.objects.get(id= id_userStory)
    comentarios = Comentario.objects.filter(us_id= id_userStory)
    context = {'elementos':comentarios,'us':us}
    return render(request, 'Gestion_de_UserStories/listar_comentarios_de_us.html', context)

@cache_control(max_age=86400)
def servir_view(request,name):
    pk, file_ext = os.path.splitext(name)
    try:
        pk = int(pk)
    except ValueError:
        raise Http404('La clave del archivo no es un Entero')
    archivo = get_object_or_404(File, pk=pk)
    mimetype = mimetypes.guess_type(name)[0] or 'application/octet-stream'
    response = HttpResponse(base64.b64decode(archivo.content), mimetype=mimetype)
    response['Content-Length'] = archivo.size
    return response

def openFile(fileName, mode, context):
# open file using python's open method
# by default file gets opened in read mode
    try:
        fileHandler = open(fileName, mode)
        return {'opened':True, 'handler':fileHandler}
    except IOError:
        context['error'] += 'Unable to open file ' + fileName + '\n'
    except:
        context['error'] += 'Unexpected exception in openFile method.\n'
    return {'opened':False, 'handler':None}

def leerArchivo(fileName, context):
    archivo = ""
    fileHandler = openFile(fileName, 'rb', context)
    if fileHandler['opened']:
        archivo = files.File(fileHandler['handler'])

        #context['fileContent'] = ''

        for chunk in archivo.chunks():
            context['fileContent'] += chunk

        archivo.close()
    return archivo

def readFile(fileName, context):
	# open file in read-only mode
    archivo = ""
    fileHandler = openFile(fileName, 'rb', context)
    if fileHandler['opened']:
		# create Django File object using python's file object
        archivo = files.File(fileHandler['handler'])

        # we have atleast empty file now
        context['fileContent'] = ''
		# use chunks to iterate over the file in chunks.
		# this is helpful when file is large enough.
		# '10' represents the size of each chunk
        for chunk in archivo.chunks(10):
            context['fileContent'] += chunk

		# make sure to close the file before exit
        archivo.close()

def writeFile(content, fileName, context):
	# open file write mode
	fileHandler = openFile(fileName, 'wb', context)

	if fileHandler['opened']:
		# create Django File object using python's file object
		file = files.File(fileHandler['handler'])
		# write content into the file
		file.write(content)
		# flush content so that file will be modified.
		file.flush()
		# close file
		file.close()

@login_required(login_url="/login/")
def listar_proyecto_US_listado_view(request):
    """
    Permite listar proyectos para seleccionar el proyecto del cual se  listaran los User Stories
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
        print("Estoy en la funcion correcta")
        form = Proyecto_Buscar_form()
        proyecto = Proyecto.objects.all()
        context = {'form': form, 'proyectos': proyecto}
    return render(request, 'Gestion_de_UserStories/listar_proyecto_para_listar_US.html', context)