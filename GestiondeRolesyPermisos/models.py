
from django.contrib.auth.models import Group

class Rol(Group):

    class Meta:
        default_permissions = ()
        permissions = (
            ('gestion_rol', 'gestion roles'),
            ('consulta_rol', 'consultar roles'),
            ('modificar_rol', 'modificar roles'),
            ('eliminar_rol', 'eliminar roles'),
            ('crear_rol', 'crear roles'),
            ('listar_rol', 'listar roles'),
            ('listar_permiso', 'listar permisos'),
        )

