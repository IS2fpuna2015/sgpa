# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='auth.Group', primary_key=True, serialize=False)),
            ],
            options={
                'permissions': (('gestion_rol', 'gestion roles'), ('consulta_rol', 'consultar roles'), ('modificar_rol', 'modificar roles'), ('eliminar_rol', 'eliminar roles'), ('crear_rol', 'crear roles'), ('listar_rol', 'listar roles'), ('listar_permiso', 'listar permisos')),
                'default_permissions': (),
            },
            bases=('auth.group',),
        ),
    ]
