from django.db import models

# Create your models here.
from GestiondeProyectos.models import Proyecto
from GestiondeSprints.models import Sprint
from GestiondeFlujos.models import Flujo


class TableroKanban(models.Model):
    nombre_tablero = models.CharField(max_length=100, null=False)
    estado_tablero = models.CharField(max_length=100, null=False,default="abierto")
    id_proyecto = models.ForeignKey(Proyecto)
    nombre_proyecto = models.CharField(max_length=100, null=False,default="0")
    id_sprint = models.ForeignKey(Sprint)
    id_flujo = models.ForeignKey(Flujo)

    class Meta:
        default_permissions = ()
        permissions = (
            ('listar_proyectos_con_tableros_kanban', 'Listar Proyectos con tablero kanban'),
            ('listar_tablero_kanban', 'Listar tablero kanban'),
            ('consulta_tablero_kanban', 'Cosultar tablero kanban'),
            ('modificar_tablero_kanban', 'Modificar tablero kanban'),
            ('eliminar_tablero_kanban', 'Eliminar tablero kanban'),
            ('crear_tablero_kanban', 'Crear tablero kanban'),
            ('gestion_tablero_kanban', 'Gestion de tablero kanban'),
            ('cambiar_us_de_actividad', 'Cambiar US de actividad dentro del tablero kanban'),
            ('cambiar_us_de_estado', 'Cambiar US de estado dentro del tablero kanban'),
        )
