from django.test import TestCase
import traceback
from datetime import datetime
from GestiondeUsuarios.models import Usuario
from GestiondeFlujos.models import Flujo, Actividad
from GestiondeProyectos.models import Proyecto


class FlujoTestCase(TestCase):
    def setUp(self):

        print("\nTEST: Crear proyecto")
        nombre_proyecto = 'prueba'
        usuario1 = Usuario(username='test1', password='test')
        usuario1.save()
        usuario2 = Usuario(username='test2', password='test')
        usuario2.save()
        usuario3 = Usuario(username='test3', password='test')
        usuario3.save()

        Codigo = 'test'
        Descripcion = "proyecto prueba"
        Fecha_inicio = datetime.now()
        Fecha_finalizacion = datetime.now()
        Scrum_master = usuario1;
        Equipo_desarrollo = [usuario3, usuario2]

        proyecto = Proyecto.objects.create(nombre_proyecto=nombre_proyecto, codigo_proyecto=Codigo, estado_proyecto='PENDIENTE',
                                fecha_inicio=Fecha_inicio, fecha_finalizacion=Fecha_finalizacion, scrum_master=usuario1,
                                descripcion_proyecto=Descripcion, cliente=usuario3,
        )
        proyecto.save()
        flujo = Flujo(nombre_flujo="flujo prueba",id_Proyecto=proyecto)
        flujo.save()
        actividad = Actividad(nombre_actividad="actividad prueba", estado_actividad="todo",orden_actividad=1,id_Flujo=flujo)

    def test_listar_flujo(self):
        print('Prueba listar flujo')
        print(Flujo.objects.all())
        print('listar flujo')

    def test_consulta_flujo(self):
        print('Prueba consulta flujo')
        print(Flujo.objects.filter(nombre_flujo='flujo prueba'))
        print('Flujo consultado')

    def test_eliminar_flujo(self):
        print('Prueba eliminar Flujo')
        Flujo.objects.filter(nombre_flujo='flujo prueba').delete()
        print('Flujo eliminado')

    def test_listar_actividad(self):
        print('Prueba listar actividad')
        print(Actividad.objects.all())
        print('listar actividad')

    def test_eliminar_actividad(self):
        print('Prueba de eliminar actividad')
        Actividad.objects.filter(nombre_actividad="actividad prueba").delete()
        print('Actividad eliminada')