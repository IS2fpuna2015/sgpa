from django.db.models import Model, CharField, ForeignKey,DateTimeField, TextField, BooleanField
from GestiondeUsuarios.models import Usuario


class Mensaje(Model):

    remitente = CharField(max_length=100)
    destinatario = ForeignKey(Usuario)
    asunto = CharField(max_length=100)
    fecha_envio = DateTimeField(auto_now_add=True)
    mensaje = TextField(null=False)
    leido = BooleanField(default=False)

    class Meta:
        default_permissions = ()
        permissions = (('crear_mensaje', 'crear mensajes'),
                       ('listar_mensajes', 'listar mensajes'),
                       ('visualizar_mensaje', 'visualizar mensajes'),
                       ('eliminar_mensaje', 'eliminar mensajes'),
                       ('gestion_de_mensajeria', 'gestion de mensajeria'),
        )
