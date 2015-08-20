# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GestiondeUsuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuario',
            options={'default_permissions': (), 'permissions': (('gestion_usuario', 'gestion de usuario'), ('consulta_usuario', 'consultar usuarios'), ('modificar_usuario', 'modificar usuarios'), ('eliminar_usuario', 'eliminar usuarios'), ('crear_usuario', 'crear usuarios'), ('listar_usuario', 'listar usuarios'))},
        ),
    ]
