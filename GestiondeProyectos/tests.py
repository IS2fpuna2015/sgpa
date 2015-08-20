from datetime import datetime
import traceback
from django.test import TestCase
from GestiondeUsuarios.models import Usuario
from GestiondeProyectos.models import Proyecto



class ProyectoTestCase(TestCase):

    def test_crear_proyecto(self):
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

        try:
            proyecto = Proyecto(nombre_proyecto=nombre_proyecto, codigo_proyecto=Codigo, estado_proyecto='PENDIENTE', cliente_id=0,
                                fecha_inicio=Fecha_inicio, fecha_finalizacion=Fecha_finalizacion, scrum_master=usuario1,
            )
            proyecto.save()

        except:
            print("Prueba fallida, no ssde pudo crear el proyecto")
            traceback.print_exc()
            return
        if len(Proyecto.objects.all()) == 1:
            print("Prueba exitosa, el proyecto fue creado correctamente")
        else:
            print("Prueba fallida, no se pudo crear el proyecto")


    def test_cancelar_proyecto(self):
        print("\nTEST: Cancelar proyecto")
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

        proyecto = Proyecto(nombre_proyecto=nombre_proyecto, codigo_proyecto=Codigo, estado_proyecto='PENDIENTE',
                            fecha_inicio=Fecha_inicio, fecha_finalizacion=Fecha_finalizacion, scrum_master=usuario1,
                            descripcion_proyecto=Descripcion, cliente=usuario3,
                            )
        proyecto.save()

        proyecto_cancel = Proyecto.objects.get(nombre_proyecto='prueba')
        proyecto.estado_proyecto = 'CANCELADO'
        proyecto.save()

        if (len(Proyecto.objects.filter(estado_proyecto='CANCELADO')) == 1):
            print("Prueba exitosa, el proyecto fue cancelado correctamente")
        else:
            print("Prueba fallida, el proyecto no fue cancelado")

