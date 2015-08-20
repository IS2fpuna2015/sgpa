from django.db import models

# Create your models here.
class BurndownChartSprint(models.Model):
    id_sprint = models.IntegerField(default=0)
    dia = models.IntegerField(default=0)
    horas_trabajadas = models.IntegerField(default=0)

    class Meta:
        default_permissions = ()
        permissions = (
            ('modificar_burndown_chart_sprint', 'Actualizar Burndown Chart Sprint'),
            ('consulta_burndown_chart_sprint', 'Visualizar Burndown Chart Sprint'),
        )

class BurndownChartProyecto(models.Model):
    id_proyecto = models.IntegerField(default=0)
    dia = models.IntegerField(default=0)
    horas_trabajadas = models.IntegerField(default=0)

    class Meta:
        default_permissions = ()
        permissions = (
            ('modificar_burndown_chart_proyecto', 'Actualizar Burndown Chart Proyecto'),
            ('consulta_burndown_chart_proyecto', 'Visualizar Burndown Chart Proyecto'),
        )