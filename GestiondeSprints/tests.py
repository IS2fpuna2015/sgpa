from django.test import TestCase
import traceback
from datetime import datetime
from GestiondeUsuarios.models import Usuario
from GestiondeSprints.models import Sprint
from GestiondeProyectos.models import Proyecto

class SprintTestCase(TestCase):
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
        Equipo_desarrollo = [usuario1, usuario2]

        proyecto = Proyecto.objects.create(nombre_proyecto=nombre_proyecto, codigo_proyecto=Codigo, estado_proyecto='PENDIENTE',
                                fecha_inicio=Fecha_inicio, fecha_finalizacion=Fecha_finalizacion, scrum_master=usuario1,
                                descripcion_proyecto=Descripcion, cliente=usuario3,
        )
        proyecto.save()
        sprint = Sprint(nombre_sprint="Mi Test Sprint", id_proyecto=proyecto, fecha_inicio=Fecha_inicio, fecha_fin=Fecha_finalizacion, estado='finalizado')
        sprint.save()

    def test_listar_sprint(self):
        print('Prueba listar Sprints')
        sprints = Sprint.objects.all()
        for sprint in sprints:
            print(sprint.nombre_sprint)
            print(sprint.estado)
            print(sprint.fecha_inicio)
            print(sprint.fecha_fin)
        print('Fin listar Sprints')

    def test_consulta_sprint(self):
        print('Prueba consulta sprint')
        print(Sprint.objects.filter(nombre_sprint='Mi Test Sprint').values('nombre_sprint', 'estado'))
        print('Sprint consultado')

    def test_eliminar_sprint(self):
        print('Prueba eliminar sprint')
        Sprint.objects.filter(nombre_sprint='Mi Test Sprint').delete()
        print('Sprint eliminado')