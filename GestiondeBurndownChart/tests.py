# Create your tests here.
from datetime import datetime, timedelta
from unittest import TestCase

from GestiondeSprints.models import Sprint
from GestiondeBurndownChart.models import BurndownChartSprint
from GestiondeProyectos.models import Proyecto
from GestiondeUsuarios.models import Usuario


class BurndownChartTestCase(TestCase):
    def setUp(self):# Create your tests here.
        Usuario(username="leo").save()


        nombre_proyecto = 'Proyecto 1'
        Codigo = 'pro1'
        Descripcion = "proyecto 1"
        Fecha_inicio = datetime.now()
        Fecha_finalizacion = datetime.now() + timedelta(days=+60)
        Scrum_master = Usuario.objects.get(username="leo")
        proyecto1 = Proyecto(nombre_proyecto=nombre_proyecto,descripcion_proyecto=Descripcion, codigo_proyecto=Codigo, estado_proyecto='PENDIENTE',
                             fecha_inicio=Fecha_inicio, fecha_finalizacion=Fecha_finalizacion, scrum_master=Scrum_master,cliente=Usuario.objects.get(username="leo")
                             )
        proyecto1.save()
        proyecto1.save()
        proyecto1.equipo_desarrollo.add(proyecto1.id, Usuario.objects.get(username="leo") )
        proyecto1.save()

        sprint1 = Sprint(nombre_sprint="Sprint1", id_proyecto=proyecto1,numero_sprint=1 ,fecha_inicio=datetime.now() - timedelta(days=+15) , fecha_fin=datetime.now() + timedelta(days=+15), estado='Pendiente')
        sprint1.save()

        sprint = Sprint.objects.get(nombre_sprint="Sprint1")
        fecha_sprint_inicio = datetime.combine(sprint.fecha_inicio , datetime.min.time())
        fecha_sprint_fin = datetime.combine(sprint.fecha_fin , datetime.min.time())
        fecha_actual = datetime.now()  - timedelta(days=+14)
        dias_restantes = fecha_sprint_fin - fecha_actual
        BurndownChartSprint(id_sprint=sprint.id,dia = dias_restantes.days+1,horas_trabajadas=2).save()

        fecha_actual = datetime.now()  - timedelta(days=+13)
        dias_restantes = fecha_sprint_fin - fecha_actual
        BurndownChartSprint(id_sprint=sprint.id,dia = dias_restantes.days+1,horas_trabajadas=1).save()

        fecha_actual = datetime.now()  - timedelta(days=+12)
        dias_restantes = fecha_sprint_fin - fecha_actual
        BurndownChartSprint(id_sprint=sprint.id,dia = dias_restantes.days+1,horas_trabajadas=0).save()

        fecha_actual = datetime.now()  - timedelta(days=+11)
        dias_restantes = fecha_sprint_fin - fecha_actual
        BurndownChartSprint(id_sprint=sprint.id,dia = dias_restantes.days+1,horas_trabajadas=1).save()

        fecha_actual = datetime.now()  - timedelta(days=+10)
        dias_restantes = fecha_sprint_fin - fecha_actual
        BurndownChartSprint(id_sprint=sprint.id,dia = dias_restantes.days+1,horas_trabajadas=0).save()

    def test_consultar(self):
        sprint1 = Sprint.objects.get(nombre_sprint="Sprint1")
        BurndownChartSprint.objects.filter(id_sprint=sprint1.id)
        print("Consulta y creacion de BurnDown Chart sin problemas")

