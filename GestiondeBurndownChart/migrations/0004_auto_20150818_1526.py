# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GestiondeBurndownChart', '0003_burndownchartproyecto'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='burndownchartproyecto',
            options={'default_permissions': (), 'permissions': (('modificar_burndown_chart_proyecto', 'Actualizar Burndown Chart Proyecto'), ('consulta_burndown_chart_proyecto', 'Visualizar Burndown Chart Proyecto'))},
        ),
        migrations.AlterModelOptions(
            name='burndownchartsprint',
            options={'default_permissions': (), 'permissions': (('modificar_burndown_chart_sprint', 'Actualizar Burndown Chart Sprint'), ('consulta_burndown_chart_sprint', 'Visualizar Burndown Chart Sprint'))},
        ),
    ]
