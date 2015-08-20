from datetime import datetime

from django.db import models

# Create your models here.
class Sistema(models.Model):
    nombre_usuario = models.CharField(max_length=100, null=False,default="No especificado")
    hora_dia = models.DateTimeField(default=datetime.now, auto_now_add=True)
    accion = models.CharField(max_length=100, null=False,default="No especificado")
    observacion = models.CharField(max_length=100, null=False,default="No especificado")


    def registrar(self,accion, usuario, observacion):
        self.nombre_usuario = usuario
        self.accion = accion
        self.observacion = observacion
        self.save()

    class Meta:
        get_latest_by = 'hora_dia'
        default_permissions = ()
        permissions = (
            ('consultar_auditoria', 'consultar auditoria'),
        )
