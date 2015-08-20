from django.db import models
from GestiondeProyectos.models import Proyecto


class Sprint(models.Model):
    ESTADOS_SPRINT = (
        ('Pendiente', 'PENDIENTE'),
        ('Activo', 'ACTIVO'),
        ('Cancelado', 'CANCELADO'),
        ('Finalizado', 'FINALIZADO'),
    )
    nombre_sprint = models.CharField(max_length=50, null=False)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(choices=ESTADOS_SPRINT, default='PENDIENTE', max_length=10)
    id_proyecto = models.ForeignKey(Proyecto)
    numero_sprint = models.IntegerField(default=1)


    def __unicode__(self):
        return self.nombre_sprint

    class Meta:
        default_permissions = ()
        permissions = (
            ('listar_sprint', 'listar sprint'),
            ('consulta_sprint', 'cosultar sprint'),
            ('modificar_sprint', 'modificar sprints'),
            ('eliminar_sprint', 'eliminar sprints'),
            ('crear_sprint', 'crear sprints'),
            ('gestion_sprint', 'Gestion de sprints'),
            ('asignar_us_a_sprint', 'Asignar US a Sprint'),
        )

class Sprint_Detalle(models.Model):

    id_sprint = models.ForeignKey(Sprint)
    descripcion = models.TextField(max_length=300)

    class Meta:
        default_permissions = ()
        permissions = (
            ('listar_detalle_sprint', 'listar detalle_sprint'),
            ('consulta_detalle_sprint', 'cosultar detalle_sprint'),
            ('modificar_detalle_sprint', 'modificar detalle_sprints'),
            ('eliminar_detalle_sprint', 'eliminar detalle_sprints'),
            ('crear_detalle_sprint', 'crear detalle_sprints'),
            ('gestion_detalle_sprint', 'Gestion de detalle_sprints'),
        )