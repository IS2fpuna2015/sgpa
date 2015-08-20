
from django.test import TestCase
from datetime import datetime
# Create your tests here.
from GestiondeProyectos.models import Proyecto
from GestiondeUserStories.models import UserStory
from GestiondeUsuarios.models import Usuario


class UserStoryTestCase(TestCase):

    def setUp(self):
        nombre_proyecto = 'prueba'
        usuario1 = Usuario(username='lbenitez', password='test')
        usuario1.save()
        usuario2 = Usuario(username='bmaluff', password='test')
        usuario2.save()
        usuario3 = Usuario(username='froman', password='test')
        usuario3.save()

        Codigo = 'test'
        Descripcion = "proyecto prueba"
        Fecha_inicio = datetime.now()
        Fecha_finalizacion = datetime.now()
        Scrum_master = usuario1;
        Equipo_desarrollo = [usuario1, usuario2]
        cliente = usuario3

        proyecto = Proyecto(nombre_proyecto=nombre_proyecto, codigo_proyecto=Codigo, estado_proyecto='PENDIENTE',
                            fecha_inicio=Fecha_inicio, fecha_finalizacion=Fecha_finalizacion, scrum_master=usuario1,
                            cliente_id=cliente.id
        )
        proyecto.save()

    def test_crear_userstory(self):

        nombre = 'userstorytest'
        codigo = 'test-123'
        descripcion = 'test'
        usuario_asignado = Usuario.objects.get(username='lbenitez')
        proyecto_pertenece = Proyecto.objects.get(nombre_proyecto='prueba')
        size = 10
        prioridad = 'ALTA'
        valor_tecnico = 8
        valor_de_negocio = 4

        userstory = UserStory(nombre=nombre, descripcion=descripcion, prioridad=prioridad, codigo=codigo,
                              valor_de_negocio=valor_de_negocio, valor_tecnico=valor_tecnico,
                              usuario_asignado=usuario_asignado, proyecto=proyecto_pertenece, size=size)

        userstory.save()

    def test_listar_userstory(self):
        print('Prueba listar User Stories')
        print(UserStory.objects.all())
        print('listar sin problemas')

    def test_consulta_userstory(self):
        print('Prueba consultar User Story')
        print(UserStory.objects.filter(codigo='test-123'))
        print('User Story consultado')

    def test_modificacion_userstory(self):
        nombre = 'userstorytest'
        codigo = 'test-123'
        descripcion = 'test'
        usuario_asignado = Usuario.objects.get(username='lbenitez')
        proyecto_pertenece = Proyecto.objects.get(nombre_proyecto='prueba')
        size = 10
        prioridad = 'ALTA'
        valor_tecnico = 8
        valor_de_negocio = 4

        userstory = UserStory(nombre=nombre, descripcion=descripcion, prioridad=prioridad, codigo=codigo,
                              valor_de_negocio=valor_de_negocio, valor_tecnico=valor_tecnico,
                              usuario_asignado=usuario_asignado, proyecto=proyecto_pertenece, size=size)

        userstory.save()


        print("Modificacion de user Story")
        userstory = UserStory.objects.get(codigo="test-123")
        prioridad = userstory.prioridad
        valor_tecnico = userstory.valor_tecnico
        userstory.prioridad="BAJA"
        userstory.valor_tecnico=10
        userstory.save()

        if prioridad!=userstory.prioridad and userstory.valor_tecnico!=valor_tecnico:
            print("Modificacino Correcta!!")
        else:
            print("No se realizo correctamete la modificacion")


