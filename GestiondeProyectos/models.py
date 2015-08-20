from django.db import models

from GestiondeUsuarios.models import Usuario


class Proyecto(models.Model):
    nombre_proyecto = models.CharField(max_length=100, null=False)
    codigo_proyecto = models.CharField(max_length=4, unique=True, null=False)
    descripcion_proyecto = models.TextField(null=False)
    fecha_inicio = models.DateField(blank=False)
    fecha_finalizacion = models.DateField(blank=False)
    estado_proyecto = models.CharField(max_length=20,null=False)
    scrum_master = models.ForeignKey(Usuario, related_name='scrum_master',null=False)
    equipo_desarrollo = models.ManyToManyField(Usuario, related_name='equipo_desarrollo',null=False)
    cliente = models.ForeignKey(Usuario, related_name='cliente',null=False)
    cantidad_sprints = models.IntegerField(default=0)



    def __str__(self):
        return self.nombre_proyecto

    class Meta:
        default_permissions = ()
        permissions = (
            ('listar_proyecto', 'listar proyectos'),
            ('consulta_proyecto', 'cosultar proyectos'),
            ('modificar_proyecto', 'modificar proyectos'),
            ('crear_proyecto', 'crear proyectos'),
            ('gestion_proyecto', 'gestion de proyectos'),
            ('modificar_scrummaster','modificar scrum master de proyectos'),
            ('generar_reporte',"generar reporte de proyectos"),
            ('consultar_estado_us',"cosultar estado de us")
        )

