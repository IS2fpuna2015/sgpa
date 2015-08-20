# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('user_ptr', models.OneToOneField(primary_key=True, parent_link=True, auto_created=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('observacion', models.CharField(default='no especificado', max_length=20)),
                ('telefono', models.IntegerField(default=0, max_length=15)),
                ('domicilio', models.CharField(default='no especificado', max_length=20)),
            ],
            options={
                'permissions': (('consulta_usuario', 'permiste cosultar usuarios'), ('modificar_usuarios', 'permite modificar usuarios'), ('eliminar_usuarios', 'permite eliminar usuarios'), ('crear_usuarios', 'permite crear usuarios')),
                'default_permissions': (),
            },
            bases=('auth.user',),
        ),
    ]
