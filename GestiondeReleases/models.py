from django.db import models
from GestiondeProyectos.models import Proyecto


class Release(models.Model):
    nombre = models.CharField(max_length=100, null=False, default='Release-XYZ')
    version = models.CharField(max_length=30, null=False, default='Y.X.Z')
    fecha = models.DateField(auto_now=True)
    descripcion = models.TextField(null=False, default='Descripcion ....')
    proyecto = models.ForeignKey(Proyecto,null=False)

    class Meta:
        default_permissions = ()
        permissions = (('crear_release',' crear releases'),
                       ('listar_release',' listar releases'),
                       ('consultar_release',' consultar releases'),
                       ('gestion_de_release',' gestion de releases'),)


