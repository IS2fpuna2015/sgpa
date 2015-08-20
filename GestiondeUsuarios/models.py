from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Usuario(User):

    observacion = models.CharField(max_length=20, default="no especificado",null=False)
    telefono = models.IntegerField(max_length=15,default=00,null=False)
    domicilio = models.CharField(max_length=20,default="no especificado",null=False)
    notificaciones = models.IntegerField(default=0)
    class Meta:
        default_permissions = ()
        permissions = (
            ('gestion_usuario','gestion de usuario'),
            ('consulta_usuario', 'consultar usuarios'),
            ('modificar_usuario', 'modificar usuarios'),
            ('eliminar_usuario', 'eliminar usuarios'),
            ('crear_usuario', 'crear usuarios'),
            ('listar_usuario', 'listar usuarios'),
        )

