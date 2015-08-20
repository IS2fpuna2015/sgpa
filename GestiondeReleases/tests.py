from django.utils import timezone
from django.test import TestCase
from GestiondeProyectos.models import Proyecto
from GestiondeReleases.models import Release
from GestiondeUserStories.models import UserStory
from GestiondeUsuarios.models import Usuario


class ReleaseTestCase(TestCase):

    def setUp(self):
        nombre_proyecto = 'prueba'
        usuario1 = Usuario(username='lbenitez', password='test')
        usuario1.save()
        usuario2 = Usuario(username='bmaluff', password='test')
        usuario2.save()
        usuario3 = Usuario(username='froman', password='test')
        usuario3.save()

        codigo_proyecto = 'test'
        descripcion_proyecto = "proyecto prueba"
        fecha_inicio = timezone.now()
        fecha_finalizacion = timezone.now()
        cliente = usuario3

        proyecto = Proyecto(nombre_proyecto=nombre_proyecto, descripcion_proyecto= descripcion_proyecto, codigo_proyecto=codigo_proyecto, estado_proyecto='PENDIENTE',
                            fecha_inicio=fecha_inicio, fecha_finalizacion=fecha_finalizacion, scrum_master=usuario1,
                            cliente_id=cliente.id,
        )

        proyecto.save()

        nombre_userstory= 'userstorytest'
        codigo_userstory = 'test-123'
        descripcion_userstory = 'test'
        usuario_asignado = Usuario.objects.get(username='lbenitez')
        proyecto_pertenece = Proyecto.objects.get(nombre_proyecto='prueba')
        size = 10
        prioridad = 'ALTA'
        valor_tecnico = 8
        valor_de_negocio = 4

        userstory = UserStory(nombre=nombre_userstory, descripcion=descripcion_userstory, prioridad=prioridad, codigo=codigo_userstory,
                              valor_de_negocio=valor_de_negocio, valor_tecnico=valor_tecnico,
                              usuario_asignado=usuario_asignado, proyecto=proyecto_pertenece, size=size)

        userstory.save()


        nombre_userstory= 'userstorytest2'
        codigo_userstory = 'test2-123'
        descripcion_userstory = 'test2'
        usuario_asignado = Usuario.objects.get(username='bmaluff')
        proyecto_pertenece = Proyecto.objects.get(nombre_proyecto='prueba')
        size = 10
        prioridad = 'ALTA'
        valor_tecnico = 8
        valor_de_negocio = 4
        estado = "APROBADO"
        porcentaje_realizado=100

        userstory2 = UserStory(nombre=nombre_userstory, descripcion=descripcion_userstory, prioridad=prioridad, codigo=codigo_userstory,
                              valor_de_negocio=valor_de_negocio, valor_tecnico=valor_tecnico,
                              usuario_asignado=usuario_asignado, proyecto=proyecto_pertenece, size=size,estado=estado,porcentaje_realizado=porcentaje_realizado)

        userstory2.save()


    def test_crear_release(self):

        print("\nTEST DE CREACION DE RELEASE\n")
        proyecto = Proyecto.objects.get(nombre_proyecto='prueba')
        if UserStory.objects.filter(estado="APROBADO").count() == 0:
            print("Error al crear release, no existen us aprobados\n")
        else:
            try:
                release = Release(nombre="releasetest",version="1.0.0",descripcion="release en proyecto",proyecto=proyecto)
                release.save()
                userstory = UserStory.objects.get(nombre='userstorytest2')
                userstory.release=release
                userstory.save()
                print("Se creo Release exitosamente\n")
            except:
                print("Error al crear Release\n")



    def test_listar_release(self):
        print("\nTEST DE LISTADO DE RELEASES\n")
        proyecto = Proyecto.objects.get(nombre_proyecto='prueba')
        if UserStory.objects.filter(estado="APROBADO").count() == 0:
            print("Error al crear release, no existen us aprobados")
        else:
            try:
                release = Release(nombre="releasetest",version="1.0.0",descripcion="release en proyecto",proyecto=proyecto)
                release.save()
                userstory = UserStory.objects.get(nombre='userstorytest2')
                userstory.release=release
                userstory.save()

                if Release.objects.all().count()>0:
                    print("Listado de Releases Exitoso\n")
                else:
                    print("Error al Listar Releases\n")

            except:
                print("Error al crear Release\n")







