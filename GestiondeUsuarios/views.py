from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from  django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

from .models import Usuario
from .forms import Tipos_Usuario_form
from GestiondeSistema.models import Sistema


@login_required(login_url="/login/")
def crear_usuario_view(request):
    """
    Redirecciona a la interfaz para la creacion de un usuario nuevo
    :param request:
    :return:
    """
    grupo_de_permisos = Group.objects.all()
    if request.method == 'POST' and 'Cancelar' in request.POST:
        if request.POST.get('username') != '':
            username = request.POST.get('username')
            try:
                temp_user = Usuario.objects.get(username=username)
                temp_user.delete()
            except:
                None
        return HttpResponseRedirect('/home/')

    #Primero creara un usuario de forma temporal para poder asignar los permisos que sean elegidos
    if request.method == 'POST' and 'Guardar' in request.POST:
        username = request.POST.get('username')
        password = make_password(request.POST.get('password'), salt=None, hasher='default')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        activo = request.POST.get('activo')
        roles_asignados = request.POST.getlist('agregar')

        #Controla que el usuario a crear sea unico
        if User.objects.filter(username=username).exists():
            return render_to_response("Gestion_de_usuarios/crear_usuario.html",
                                      {'error': 'existente', 'disponibles': grupo_de_permisos},
                                      context_instance=RequestContext(request))

        #Controlara que se haya seleccionado al menos un rol
        if len(roles_asignados) == 0:
            return render_to_response("Gestion_de_usuarios/crear_usuario.html",
                                      {'error': 'roles', 'disponibles': grupo_de_permisos},
                                      context_instance=RequestContext(request))
        #Controla que no se hayan dejado en blanco ningun campo
        if username != '' and password != '' and lastname != '' and email != '':
            # Se creara el usuario
            user = Usuario(username=username, password=password, email=email)
            user.first_name = request.POST.get('firstname')
            user.last_name = lastname

            #Si no se elige una de las opciones se tomara usuario desactivado por defecto
            if activo == 'true':
                user.is_active = True
            else:
                user.is_active = False

            user.is_staff = True
            user.is_superuser = False
            user.save()
            Sistema().registrar("creado usuario "+username+" ",request.user.username,"none")


            #Se agrega el rol que poseera el usuario
            for item in roles_asignados:
                group = Group.objects.get(pk=item)
                user.groups.add(group)

            return HttpResponseRedirect('/listar_usuarios/')
            #return render_to_response("Gestion_de_usuarios/crear_usuario.html", {'error': 'ninguno',  'disponibles': grupo_de_permisos},context_instance=RequestContext(request))
        else:
            return render_to_response("Gestion_de_usuarios/crear_usuario.html", {'error': 'vacio',  'disponibles': grupo_de_permisos},
                                      context_instance=RequestContext(request))


    return render_to_response("Gestion_de_usuarios/crear_usuario.html", { 'disponibles': grupo_de_permisos},
                              context_instance=RequestContext(request))



@login_required(login_url="/login/")
def listar_usuarios_filtro_view(request):
    """
    Permite al usuario realizar el listado de usuarios que se encuentran en el sistema
    habilitando con la opcion de filtrados de usuarios, tambien habilitara el boton para
    modificar, crear o eliminar si es que posee los permisos el usuario en sesion.
    :param request:
    :return:
    """
    tipos = {}
    if request.method == 'POST':


        form = Tipos_Usuario_form(request.POST)
        if form.is_valid():
            tipos = form.cleaned_data.get('Tipos_Usuario')
            busqueda = form.cleaned_data.get('Busqueda')
            if busqueda == 'todos' or busqueda == 'Todos': #Si el usuario ingresa "Todos"
                usuarios = User.objects.filter(is_active='True')
                context = {'form': form, 'usuarios': usuarios}
            elif busqueda != '' and tipos: #Si el usuario ingresa un tipo y un nombre especificos
                usuarios = User.objects.filter(groups__id=tipos.id).filter(username=busqueda,is_active='True')
                context = {'form': form, 'usuarios': usuarios}
            elif tipos: #Si el usuario solo ingresa el tipo
                usuarios = User.objects.filter(groups__id=tipos.id,is_active='True')
                context = {'form': form, 'usuarios': usuarios}
            elif busqueda != '' and not tipos: #Si el usuario ingresa solo el nombre
                usuarios = User.objects.filter(username=busqueda,is_active='True')
                context = {'form': form, 'usuarios': usuarios}
            else:
                form = Tipos_Usuario_form()
                #tipos = "Ninguno" Es cuando el usuario oprime el boton buscar sin ningun parametro de busqueda
                context = {'form': form}
        else:
            form = Tipos_Usuario_form()
            #tipos = "No valido" Es cuando el parametro de busqueda es invalido
            context = {'form': form}

    else:
        form = Tipos_Usuario_form()
        usuarios = User.objects.filter(is_active='True')

        context = {'form': form, 'usuarios': usuarios}
    return render(request, 'Gestion_de_usuarios/Listar_Usuario_Filtro.html', context)




@login_required(login_url="/login/")
def modificar_usuario_view(request, id_usuario):
    """
    Redirecciona al usuario la modificacion de un usuario especifico
    :param id_usuario: el id del usuario que sera modificado
    :return:
    """
    grupos_permisos = Group.objects.all()

    #Se obtienen los datos del usuario
    usuario_seleccionado = Usuario.objects.get(pk=id_usuario)
    roles_asignados =  usuario_seleccionado.groups.all()
    usuario_pass_hash = usuario_seleccionado.password

    if request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_usuarios/')

    if request.method == 'POST' and 'Guardar' in request.POST:
        usuario_seleccionado.username = request.POST.get('username')
        usuario_seleccionado.first_name = request.POST.get('firstname')
        usuario_seleccionado.telefono = request.POST.get('telefono')
        usuario_seleccionado.observacion = request.POST.get('observacion')
        usuario_seleccionado.domicilio = request.POST.get('domicilio')
        usuario_seleccionado.password =   request.POST.get('password')
        usuario_seleccionado.last_name = request.POST.get('lastname')
        usuario_seleccionado.email = request.POST.get('email')
        roles_asignados = request.POST.getlist('agregar')

        if request.POST.get('activo'):
            usuario_seleccionado.is_active = True
        else:
            usuario_seleccionado.is_active = False

        #Controlara que se haya asignado un rol como minimo al modificar
        if len(roles_asignados) == 0:
            return render_to_response("Gestion_de_usuarios/modificar_usuario.html",
                                      {'error':"roles", 'usuario': usuario_seleccionado, 'grupos': grupos_permisos,'roles':roles_asignados},
                                      context_instance=RequestContext(request))

            #Controla que no se hayan dejado en blanco ningun campo
        if usuario_seleccionado.username != '' and usuario_seleccionado.password != '' and usuario_seleccionado.last_name != '' and usuario_seleccionado.email != '':
            usuario_seleccionado.groups.clear()
            #Se agrega el rol que poseera el usuario
            for item in roles_asignados:
                group = Group.objects.get(pk=item)
                usuario_seleccionado.groups.add(group)

            if usuario_seleccionado.password != usuario_pass_hash:
                usuario_seleccionado.password = make_password(usuario_seleccionado.password, salt=None, hasher='default')

            usuario_seleccionado.save()
            Sistema().registrar("modificado usuario "+ usuario_seleccionado.username+" ",request.user.username,"none")
            return HttpResponseRedirect('/listar_usuarios/')
        else:
            return render_to_response("Gestion_de_usuarios/modificar_usuario.html",
                                      {'error':"vacio", 'usuario': usuario_seleccionado, 'grupos': grupos_permisos,'roles':roles_asignados},
                                      context_instance=RequestContext(request))

    return render_to_response("Gestion_de_usuarios/modificar_usuario.html",
                              {"usuario": usuario_seleccionado, 'grupos': grupos_permisos,'roles':roles_asignados},
                                      context_instance=RequestContext(request))



@login_required(login_url="/login/")
def consultar_usuario_view(request, id_usuario):
    """
    La funcion consultar, es basicamente la misma que modificar, sin embargo no permite
    la modificacion de ninguno de los campos.
    :param id_usuario: el id del usuario que sera modificado
    :return:
    """
    usuario_seleccionado = Usuario.objects.get(pk=id_usuario)
    if request.method == 'POST' and 'Retroceder' in request.POST:
        return HttpResponseRedirect('/listar_usuarios/')
    return render_to_response("Gestion_de_usuarios/consultar_usuario.html",{"usuario":usuario_seleccionado},context_instance=RequestContext(request))


@login_required(login_url="/login/")
def eliminar_usuario_view(request, id_usuario, template_name='Gestion_de_usuarios/eliminar_usuario.html'):
    """
    La funcion Eliminar en realidad solo cambia el estado del usuario en la base de datos
    dejandolo inactivo, a fin de tener un registro sobre el historial de los usuarios creados.
    :param id_usuario: el id del usuario que sera modificado
    :return:
    """
    usuario_seleccionado = Usuario.objects.get(pk=id_usuario)
    nombre = usuario_seleccionado.username
    if request.method == 'POST' and 'Aceptar' in request.POST:
        usuario_seleccionado.is_active = False
        usuario_seleccionado.save()
        Sistema().registrar("desactivado usuario "+ nombre+" ",request.user.username,"none")
        return HttpResponseRedirect('/listar_usuarios/')
    else:
        return render(request, template_name, {'nombre': nombre})
