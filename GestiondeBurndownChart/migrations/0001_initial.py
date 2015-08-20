# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BurndownChartSprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_sprint', models.IntegerField(default=0)),
                ('dia', models.IntegerField(default=0)),
                ('horas_a_completar', models.IntegerField(default=0)),
                ('horas_desarrolladas', models.IntegerField(default=0)),
                ('total_de_dias', models.IntegerField(default=0)),
            ],
            options={
                'default_permissions': (),
                'permissions': (('listar_flujo', 'listar flujo'),),
            },
            bases=(models.Model,),
        ),
    ]
