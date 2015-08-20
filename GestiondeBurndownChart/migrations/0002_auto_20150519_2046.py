# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GestiondeBurndownChart', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='burndownchartsprint',
            options={'default_permissions': (), 'permissions': ()},
        ),
        migrations.RemoveField(
            model_name='burndownchartsprint',
            name='horas_a_completar',
        ),
        migrations.RemoveField(
            model_name='burndownchartsprint',
            name='horas_desarrolladas',
        ),
        migrations.RemoveField(
            model_name='burndownchartsprint',
            name='total_de_dias',
        ),
        migrations.AddField(
            model_name='burndownchartsprint',
            name='horas_trabajadas',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
