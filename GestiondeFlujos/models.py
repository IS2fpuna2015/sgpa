from django.db import models

from GestiondeProyectos.models import Proyecto


class Flujo(models.Model):
    nombre_flujo = models.CharField(max_length=50, default="no especificado",null=False)
    id_Proyecto = models.ForeignKey(Proyecto)
    id_sprint = models.IntegerField(default=0)

    def __unicode__(self):
        return self.nombre_flujo
    class Meta:
        default_permissions = ()
        permissions = (
            ('listar_flujo', 'listar flujo'),
            ('consulta_flujo', 'cosultar flujos'),
            ('modificar_flujo', 'modificar flujos'),
            ('eliminar_flujo', 'eliminar flujos'),
            ('crear_flujo', 'crear flujos'),
            ('gestion_flujo', 'Gestion de flujos'),
        )

class Actividad(models.Model):
    id_Flujo = models.ForeignKey(Flujo)
    nombre_actividad = models.CharField(max_length=50, default="no especificado",null=False)
    orden_actividad = models.IntegerField()
    estado_actividad = models.CharField(max_length=20, default="no especificado",null=False)

    class Meta:
        default_permissions = ()
        permissions = (
            ('listar_actividad', 'listar actividad'),
            ('consulta_actividad', 'cosultar actividad'),
            ('modificar_actividad', 'modificar actividad'),
            ('eliminar_actividad', 'eliminar actividad'),
            ('crear_actividad', 'crear actividad')
        )
