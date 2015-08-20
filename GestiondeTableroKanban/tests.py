# Create your tests here.
from datetime import datetime
from unittest import TestCase

from GestiondeTableroKanban.models import TableroKanban
from GestiondeProyectos.models import Proyecto
from GestiondeFlujos.models import Flujo
from GestiondeSprints.models import Sprint
from GestiondeUsuarios.models import Usuario
from GestiondeUserStories.models import UserStory
from GestiondeFlujos.models import Actividad


class TableroKanbanTestCase(TestCase):
    def setUp(self):
        print("\nTEST 1: Creacion de usuario")
        usuario1 = Usuario(username='test1', password='test')
        usuario1.save()
        usuario2 = Usuario(username='test2', password='test')
        usuario2.save()
        usuario3 = Usuario(username='test3', password='test')
        usuario3.save()
        print("Creacion de usuarios sin problemas")

        print("\nTEST 2: Creacion de  proyecto")
        nombre_proyecto = 'prueba'
        Codigo = 'test'
        Descripcion = "proyecto prueba"
        Fecha_inicio = datetime.now()
        Fecha_finalizacion = datetime.now()
        Scrum_master = usuario1;
        Equipo_desarrollo = [usuario1, usuario2]
        proyecto = Proyecto(nombre_proyecto=nombre_proyecto,descripcion_proyecto=Descripcion, codigo_proyecto=Codigo, estado_proyecto='PENDIENTE',
                            fecha_inicio=Fecha_inicio, fecha_finalizacion=Fecha_finalizacion, scrum_master=Scrum_master,cliente=usuario3
                            )
        proyecto.save()
        print("TEST: Creacion de  proyecto sin problemas")


        print("\nTEST 3: Asignacion de equipo de desarrollo al proyecto")
        proyecto.equipo_desarrollo = [usuario1, usuario2, usuario3]
        proyecto.save()
        print("TEST: Asignacion de equipo de desarrollo a proyecto sin problemas")



        print("\nTEST 4: Creacion de sprint")
        sprint = Sprint(nombre_sprint="Mi Test Sprint", id_proyecto=proyecto, fecha_inicio=Fecha_inicio, fecha_fin=Fecha_finalizacion, estado='finalizado')
        sprint.save()
        print("TEST: Creacion de sprint sin problemas")



        print("\nTEST 5: Creacion de US")
        nombre = 'userstorytest'
        codigo = 'test-123'
        descripcion = 'test'
        usuario_asignado = Usuario.objects.get(username='test1')
        proyecto_pertenece = Proyecto.objects.get(nombre_proyecto=nombre_proyecto)
        size = 10
        prioridad = 'ALTA'
        valor_tecnico = 8
        valor_de_negocio = 4
        userstory = UserStory(nombre=nombre, descripcion=descripcion, prioridad=prioridad, codigo=codigo,
                              valor_de_negocio=valor_de_negocio, valor_tecnico=valor_tecnico,
                              usuario_asignado=usuario_asignado, proyecto=proyecto_pertenece, size=size)
        userstory.save()
        print("Creacion de US sin problemas")



        print("\nTEST 6: Asignacion de usuario a US")
        userstory.usuario_asignado = usuario3
        userstory.save()
        print("TEST:  Asignacion de usuario a US sin problemas")


        print("\nTEST 7: Creacion de flujo")
        flujo = Flujo(nombre_flujo="flujo prueba",id_Proyecto=proyecto)
        flujo.save()
        print("TEST: Creacion de flujo sin problemas")

        print("\nTEST 8: Creacion de actividades")
        actividad1 = Actividad(id_Flujo_id=flujo.id,nombre_actividad="actividad_prueba 1",orden_actividad=1,estado_actividad="ToDo")
        actividad1.save()
        actividad2 = Actividad(id_Flujo_id=flujo.id,nombre_actividad="actividad_prueba 2",orden_actividad=2,estado_actividad="ToDo")
        actividad2.save()
        actividad3 = Actividad(id_Flujo_id=flujo.id,nombre_actividad="actividad_prueba 3",orden_actividad=3,estado_actividad="ToDo")
        actividad3.save()
        print("TEST: Creacion de actividades sin problemas")



        print("\nTEST 9: Asignacion de US a Sprint")
        userstory.nombre_sprint = sprint.nombre_sprint
        userstory.save()
        print("TEST:  Asignacion de US a Sprint sin problemas")

        print("\nTEST 10: Asignacion de US a Flujo")
        userstory.id_flujo = flujo.id
        userstory.save()
        print("TEST:  Asignacion de US a Flujo sin problemas")

        print("\nTEST 11: Asignacion de US a Actividad")
        userstory.id_actividad = actividad1.id
        userstory.estado_en_actividad = "ToDo"
        userstory.save()
        print("TEST:  Asignacion de US a Actividad sin problemas")


        print("\nTEST 12: Creacion de Tablero Kanban")
        tablero = TableroKanban(nombre_tablero='Tablero de prueba unitaria',estado_tablero='Abierto',id_sprint_id=sprint.id,id_flujo_id=flujo.id,id_proyecto=proyecto,nombre_proyecto=proyecto.nombre_proyecto)
        tablero.save()
        print("TEST: Creacion de Tablero Kanban sin problemas")




    def test_consulta_tablero(self):
        print('\nTEST 13:Consulta de tablero')
        tablero = TableroKanban.objects.get(nombre_tablero='Tablero de prueba unitaria')
        sprint_tablero = Sprint.objects.get(id=tablero.id_sprint_id)
        flujo_tablero = Flujo.objects.get(id=tablero.id_flujo_id)
        proyecto_tablero = Proyecto.objects.get(id=tablero.id_proyecto.id)
        us_tablero = UserStory.objects.filter(nombre_sprint=sprint_tablero.nombre_sprint)

        print("Nombre del tablero: "+tablero.nombre_tablero)
        print("Sprint del tablero: "+sprint_tablero.nombre_sprint)
        print("Flujo del tablero: "+flujo_tablero.nombre_flujo)
        print("Estado del tablero: "+tablero.estado_tablero)
        print("Proyecto del tablero: "+proyecto_tablero.nombre_proyecto)
        print("\nLista de US que se encuentran en el tablero")
        for us in us_tablero:
            print("\tNombre de US en tablero: "+us.nombre)
        print('Tablero consultado sin problemas')

        print('\nTEST 14:Modificacion de tablero')
        tablero.estado_tablero = "Cerrado"
        tablero.save()
        print("Estado del tablero: "+tablero.estado_tablero)
        print('Tablero modificado sin problemas')


