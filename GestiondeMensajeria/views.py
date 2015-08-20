from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from GestiondeMensajeria.forms import CrearMensajeForm, BuscarMensajeForm
from GestiondeMensajeria.models import Mensaje
from GestiondeUsuarios.models import Usuario


@login_required(login_url="/login/")
def enviar_mensaje_view(request):

    """
    Permite enviar un mensaje a un usuario del sistema
    :param request:
    :return:
    """

    if (request.method == 'POST' and 'Enviar' in request.POST):

        formulario = CrearMensajeForm(request.user,request.POST)
        id_destinatario = request.POST.get('destinatario')
        asunto = request.POST.get('asunto')
        mensaje= request.POST.get('mensaje')

        if id_destinatario == '':
            context = {'formulario':formulario,'error':'destinatario'}
            return render(request,'Gestion_de_Mensajeria/enviar_mensaje.html',context)
        if asunto == '':
            context = {'formulario':formulario,'error':'asunto'}
            return render(request,'Gestion_de_Mensajeria/enviar_mensaje.html',context)

        if mensaje == '':
            context = {'formulario':formulario,'error':'mensaje'}
            return render(request,'Gestion_de_Mensajeria/enviar_mensaje.html',context)

        remitente= Usuario.objects.get(username=request.user)
        destinatario = Usuario.objects.get(pk=id_destinatario)
        mensaje_obj = Mensaje(destinatario=destinatario,asunto=asunto,mensaje=mensaje,remitente=remitente)
        mensaje_obj.save()

        destinatario.notificaciones = destinatario.notificaciones + 1
        destinatario.save()

        return HttpResponseRedirect('/listar_mensajes/')

    formulario = CrearMensajeForm(request.user)
    context = {'formulario':formulario}
    return render(request, 'Gestion_de_Mensajeria/enviar_mensaje.html', context)

@login_required(login_url="/login/")
def visualizar_mensaje_view(request,id_mensaje):

    """
    Permite visualizar el contenido de un mensaje seleccionado
    :param
    request:
    :param id_mensaje:
    :return:
    """

    mensaje_obj = Mensaje.objects.get(pk=id_mensaje)
    mensaje_obj.leido = True;
    mensaje_obj.save()

    #Se encarga de las notificaciones del usuario
    usuario = Usuario.objects.get(id=request.user.id)
    usuario.notificaciones = usuario.notificaciones - 1
    if usuario.notificaciones < 0:
        usuario.notificaciones = 0
    usuario.save()

    if request.method == 'POST' and "Eliminar" in request.POST:
        mensaje_obj.delete()
        return HttpResponseRedirect('/listar_mensajes/')
    context = {'mensaje_obj':mensaje_obj}
    return render(request,'Gestion_de_Mensajeria/visualizar_mensaje.html',context)

@login_required(login_url="/login/")
def listar_mensajes_view(request):

    """
    Permite listar los mensaje de un usuario
    :param request:
    :return:
    """


    if request.method == 'POST':
        busqueda = request.POST.get('busqueda')
        if busqueda !='':
            mensajes = Mensaje.objects.filter(destinatario=request.user.id).filter(asunto=busqueda).order_by('-fecha_envio')
            formulario = BuscarMensajeForm(request.POST)
            context ={'mensajes':mensajes,'formulario':formulario}
            return render(request,'Gestion_de_Mensajeria/listar_mensajes.html',context)
        else:
            mensajes = mensajes = Mensaje.objects.filter(destinatario=request.user.id).order_by('-fecha_envio')
            formulario = BuscarMensajeForm()
            context ={'mensajes':mensajes,'formulario':formulario}
            return render(request,'Gestion_de_Mensajeria/listar_mensajes.html',context)

    formulario = BuscarMensajeForm()
    mensajes = Mensaje.objects.filter(destinatario=request.user.id).order_by('-fecha_envio')
    context ={'mensajes':mensajes,'formulario':formulario}
    return render(request,'Gestion_de_Mensajeria/listar_mensajes.html',context)

