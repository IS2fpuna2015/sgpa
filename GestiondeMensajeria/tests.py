from django.utils import timezone
from django.test import TestCase
from GestiondeMensajeria.models import Mensaje
from GestiondeUsuarios.models import Usuario

class MensajeriaTestCase(TestCase):

    def setUp(self):
        Usuario.objects.create(username="usuario1",first_name="nombre1", last_name="apellido1")
        Usuario.objects.create(username="usuario2",first_name="nombre2", last_name="apellido2")
        Usuario.objects.create(username="usuario3",first_name="nombre3", last_name="apellido3")
        usuario1 = Usuario.objects.get(username='usuario1')
        usuario2 = Usuario.objects.get(username='usuario2')
        usuario3 = Usuario.objects.get(username='usuario3')
        mensaje = Mensaje(asunto='test',remitente=usuario1,destinatario=usuario2,mensaje='testmensaje',fecha_envio=timezone.now())
        mensaje2 = Mensaje(asunto='test2',remitente=usuario1,destinatario=usuario3,mensaje='testmensaje2',fecha_envio=timezone.now())
        mensaje.save()
        mensaje2.save()

    def test_enviar_mensaje(self):

        usuario1 = Usuario.objects.get(username='usuario1')
        usuario2 = Usuario.objects.get(username='usuario2')
        mensaje = Mensaje(asunto='test3',remitente=usuario1,destinatario=usuario2,mensaje='testmensaje3',fecha_envio=timezone.now())
        mensaje.save()
        if Mensaje.objects.filter(destinatario=usuario2).count()==2:
            print("Se envio exitosamente mensajes")
        else:
            print("Error al enviar mensaje")

    def test_leer_mensaje(self):
        mensaje= Mensaje.objects.get(asunto='test2')
        mensaje.leido = True
        mensaje.save()
        estado_leido = mensaje.leido

        if(estado_leido is True):
            print("El mensaje se leyo exitosamente")
        else:
            print("El mensaje no se pudo leer")


    def test_eliminar_mensaje(self):

        usuario3 = Usuario.objects.get(username='usuario3')
        mensaje = Mensaje.objects.get(asunto='test2')
        mensaje.delete()

        if not Mensaje.objects.filter(destinatario=usuario3):
            print("Se elimino el mensaje correctamente")
        else:
            print("Error al eliminar mensaje")

    def test_listar_mensajes(self):

        usuario3 = Usuario.objects.get(username='usuario3')
        if (Mensaje.objects.filter(destinatario=usuario3).count()==1):
            print("Se listaron correctamente los mensajes")
        else:
            print("Error al listar los mensajes")

