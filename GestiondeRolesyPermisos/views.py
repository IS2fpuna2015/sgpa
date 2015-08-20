from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from .forms import RolForm, Busqueda_Rol_form
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.db.models import Q

from GestiondeSistema.models import Sistema


@login_required(login_url="/login/")
def crear_rol_view(request):
    """
    Permite la creacion de un rol
    :param request:
    :return:
    """

    if request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/home/')

    if request.method == 'POST' and 'Guardar' in request.POST:
        formulario = RolForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            Sistema().registrar("Creado rol ",request.user.username,"Ninguno")
            return HttpResponseRedirect('/listar_roles/')

    formulario = RolForm()
    return render_to_response("Gestion_de_roles/crear_rol.html", {'formulario': formulario},
                              context_instance=RequestContext(request), )


@login_required(login_url="/login/")
def listar_roles_filtro_view(request):
    """
    Permite al usuario realizar el listado de roles que se encuentran en el sistema
    habilitando con la opcion de filtrados de roles, tambien habilitara el boton para
    modificar, crear o eliminar si es que posee los permisos el usuario en sesion.
    :param request:
    :return:
    """

    if request.method == 'POST':
        form = Busqueda_Rol_form(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data.get('Busqueda')

            if busqueda != '':
                roles = Group.objects.filter(name=busqueda)
                context = {'form': form, 'roles': roles}
            elif busqueda == '':
                roles = Group.objects.all()
                context = {'form': form, 'roles': roles}
        else:
            form = Busqueda_Rol_form()
            roles = Group.objects.all()
            context = {'form': form, 'foles': roles}
    else:
        form = Busqueda_Rol_form()
        roles = Group.objects.all()
        context = {'form': form, 'roles': roles}
    return render(request, 'Gestion_de_roles/Listar_Roles_Filtro.html', context)


@login_required(login_url="/login/")
def modificar_rol_view(request, id_rol):
    """
    permite la modificacion de un rol a los usuarios con permisos adecuados
    :param request:
    :param id_proyecto:
    :return:
    """

    rol_seleccionado = Group.objects.get(pk=id_rol)

    if request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_roles/')
    if request.method == 'POST' and 'Guardar' in request.POST:
        formulario = RolForm(request.POST, instance=rol_seleccionado)
        if formulario.is_valid():
            Sistema().registrar("Modificado rol "+rol_seleccionado.name,request.user.username,"Ninguno")
            formulario.save(rol_seleccionado)
            return HttpResponseRedirect('/listar_roles/')

        return HttpResponseRedirect('/listar_roles/')
    formulario = RolForm(instance=rol_seleccionado)
    return render_to_response("Gestion_de_roles/modificar_rol.html", {"formulario": formulario},
                              context_instance=RequestContext(request))

@login_required(login_url="/login/")
def consultar_rol_view(request,id_rol):
    """
    Permite la consulta de un proyecto a partir del proyecto que es seleccionado
    :param request:
    :param id_rol:
    :return:
    """

    rol_seleccionado = Group.objects.get(pk=id_rol)
    permissions = Permission.objects.filter(group=rol_seleccionado.id)
    if request.method=='POST' and 'Retroceder' in request.POST:
        return HttpResponseRedirect('/listar_roles/')
    return render_to_response("Gestion_de_roles/consultar_rol.html",{"rol":rol_seleccionado,'permisos':permissions},context_instance=RequestContext(request))



@login_required(login_url="/login/")
def eliminar_rol_view(request, id_rol, template_name='Gestion_de_roles/eliminar_rol.html'):

    """
    La funcion Eliminar elimina un rol seleccionado
    :param id_rol: el id del rol que sera eliminado
    :return:
    """

    rol_seleccionado = Group.objects.get(pk=id_rol)
    nombre = rol_seleccionado.name
    if request.method == 'POST' and 'Aceptar' in request.POST:
        Group.delete(rol_seleccionado)
        Sistema().registrar("Eliminado rol "+rol_seleccionado.name,request.user.username,"Ninguno")
        return HttpResponseRedirect('/listar_roles/')
    else:
        return render(request, template_name ,{'nombre':nombre})

@login_required(login_url="/login/")
def listar_permisos_view(request):

    """
    Permite al usuario realizar el listado de permisos que se encuentran en el sistema.
    :param request:
    :return:
    """

    permisos = Permission.objects.filter(~Q(content_type=1),~Q(content_type=2),~Q(content_type=3),~Q(content_type=4),~Q(content_type=5), ~Q(content_type=6))
    context = {'permisos':permisos}
    return render(request, 'Gestion_de_roles/listar_permisos.html', context)