# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GestiondeBurndownChart', '0002_auto_20150519_2046'),
    ]

    operations = [
        migrations.CreateModel(
            name='BurndownChartProyecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_proyecto', models.IntegerField(default=0)),
                ('dia', models.IntegerField(default=0)),
                ('horas_trabajadas', models.IntegerField(default=0)),
            ],
            options={
                'default_permissions': (),
                'permissions': (),
            },
            bases=(models.Model,),
        ),
    ]
