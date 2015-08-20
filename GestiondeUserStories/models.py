from datetime import datetime

from django.db import models
from GestiondeProyectos.models import Proyecto
from GestiondeReleases.models import Release
from GestiondeUsuarios.models import Usuario
import os

class UserStory(models.Model):
    codigo = models.CharField(max_length=10, null=False, default='AAAA')
    nombre = models.CharField(max_length=200, null=False)
    descripcion = models.TextField(null=False)
    prioridad = models.CharField(max_length=6, null=False, default='BAJA')
    valor_tecnico = models.PositiveIntegerField(null=False, default=1)
    valor_de_negocio = models.PositiveIntegerField(null=False, default=1)
    size = models.FloatField(null=False, default=1)
    porcentaje_realizado = models.IntegerField(null=False, default=0)
    usuario_asignado = models.ForeignKey(Usuario, related_name='usuario_asignado', null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto , related_name='proyecto',null=False)
    estado = models.CharField(max_length=15, null=False, default='PENDIENTE')
    horas_dedicadas = models.IntegerField(null=False, default=0)

    nombre_sprint = models.CharField(max_length=200, default="No Asignado")
    estado_en_actividad = models.CharField(max_length=200, default="ToDo")
    id_actividad = models.IntegerField(null=False, default=0)
    id_flujo = models.IntegerField(null=False, default=0)
    release = models.ForeignKey(Release, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        default_permissions = ()
        permissions = (
            ('listar_userstories', 'listar user stories'),
            ('consulta_userstories', 'cosultar user stories'),
            ('modificar_userstories', 'modificar user stories'),
            ('crear_userstories', 'crear user stories'),
            ('gestion_userstories', 'gestion de user stories'),
        )

class Comentario(models.Model):
    comentario = models.TextField(default="")
    autor = models.TextField(default="")
    fecha =  models.DateTimeField(default=datetime.now, blank=True)
    us_id = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.comentario

    class Meta:
        default_permissions = ()
        permissions = (
            ('listar_comentarios', 'Listar Comentarios'),
            ('agregar_comentarios', 'Agregar Comentarios'),
            ('visualizar_comentarios', 'Visualizar Comentarios'),
        )

class FileAttached_model(models.Model):
    file = models.FileField(upload_to='not required', default="", blank=True, null=True)
    file_name = models.CharField(max_length=200, default="", null=True)
    file_path = models.CharField(max_length=2000,default="", null=True)
    userstory_id = models.IntegerField(default=0, null=True)
    file_type = models.CharField(max_length=200, default="")

class FileManager(models.Manager):
    def get_from_name(self, name):
        return self.get(pk=os.path.splitext(os.path.split(name)[1])[0])

class File(models.Model):
    content = models.TextField()
    size = models.IntegerField()
    objects = FileManager()
