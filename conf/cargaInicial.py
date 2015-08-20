from datetime import datetime, timedelta

from GestiondeRolesyPermisos.models import Rol
from GestiondeUsuarios.models import Usuario
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import   Group, Permission
from GestiondeProyectos.models import Proyecto
from GestiondeSprints.models import Sprint
from GestiondeUserStories.models import UserStory
from GestiondeFlujos.models import Flujo
from GestiondeFlujos.models import Actividad
from GestiondeBurndownChart.models import BurndownChartSprint
from GestiondeBurndownChart.models import BurndownChartProyecto




######################### Carga de Usuarios   ##########################################################################

Usuario.objects.create(username="admin",first_name="admin",email="admin@sgpa.com", last_name="admin",is_superuser=True,is_active=True,is_staff=True,password= make_password("admin", salt=None, hasher='default')).save()
Usuario.objects.create(username="froman",first_name="fede",email="froman@sgpa.com", last_name="roman",is_active=True,is_staff=True,password= make_password("fede", salt=None, hasher='default')).save()
Usuario.objects.create(username="lbenitez",first_name="leo",email="lbenitez@sgpa.com", last_name="benitez",is_active=True,is_staff=True,password= make_password("leo", salt=None, hasher='default')).save()
Usuario.objects.create(username="bmaluff",first_name="bader",email="bmaluff@sgpa.com", last_name="maluff",is_active=True,is_staff=True,password= make_password("bader", salt=None, hasher='default')).save()

Usuario.objects.create(username="desarrollador1",first_name="desarrollador1",email="desarrollador1@sgpa.com", last_name="admin",is_active=True,is_staff=True,password= make_password("desarrollador1", salt=None, hasher='default')).save()
Usuario.objects.create(username="desarrollador2",first_name="desarrollador2",email="desarrollador2@sgpa.com", last_name="admin",is_active=True,is_staff=True,password= make_password("desarrollador2", salt=None, hasher='default')).save()
Usuario.objects.create(username="desarrollador3",first_name="desarrollador3",email="desarrollador3@sgpa.com", last_name="admin",is_active=True,is_staff=True,password= make_password("desarrollador3", salt=None, hasher='default')).save()

Usuario.objects.create(username="scrummaster1",first_name="scrummaster1",email="scrummaster1@sgpa.com", last_name="admin", is_active=True,is_staff=True,password= make_password("scrummaster1", salt=None, hasher='default')).save()
Usuario.objects.create(username="scrummaster2",first_name="scrummaster2",email="scrummaster2@sgpa.com", last_name="admin", is_active=True,is_staff=True,password= make_password("scrummaster2", salt=None, hasher='default')).save()

Usuario.objects.create(username="cliente1",first_name="cliente1",email="cliente1@sgpa.com", last_name="admin",is_superuser=True,is_active=True,is_staff=True,password= make_password("cliente1", salt=None, hasher='default')).save()
Usuario.objects.create(username="cliente2",first_name="cliente2",email="cliente2@sgpa.com", last_name="admin",is_superuser=True,is_active=True,is_staff=True,password= make_password("cliente2", salt=None, hasher='default')).save()

########################################################################################################################

######################### Carga de Roles y asignacion de permisos ######################################################
Rol(name="Cliente").save()
Rol(name="Scrum Master").save()
Rol(name="Desarrollador").save()
Rol(name="Administrador").save()

group1 = Group.objects.get(name='Cliente')
group2 = Group.objects.get(name='Scrum Master')
group3 = Group.objects.get(name='Desarrollador')
group4 = Group.objects.get(name='Administrador')


for item in Permission.objects.all():
    if "CREAR" in item.name.upper() or "MODIFICAR" in item.name.upper() or  "ELIMINAR" in item.name.upper() or  "CAN" in item.name.upper() or "GENERAR" in item.name.upper():
        group2.permissions.add(item)
        group4.permissions.add(item)
        group3.permissions.add(item)
    if "LISTAR" in item.name.upper() or "CONSULTAR" in item.name.upper() or "GESTION" in item.name.upper():
        group1.permissions.add(item)
        group2.permissions.add(item)
        group4.permissions.add(item)
        group3.permissions.add(item)
    else:
        group4.permissions.add(item)




user = Usuario.objects.get(username="admin")
user.groups.add(group1)
user.groups.add(group2)
user.groups.add(group3)
user.groups.add(group4)

user1 = Usuario.objects.get(username="froman")
user1.groups.add(group1)
user1.groups.add(group2)
user1.groups.add(group3)
user1.groups.add(group4)


user2 = Usuario.objects.get(username="lbenitez")
user2.groups.add(group1)
user2.groups.add(group2)
user2.groups.add(group3)
user2.groups.add(group4)


user3 = Usuario.objects.get(username="bmaluff")
user3.groups.add(group1)
user3.groups.add(group2)
user3.groups.add(group3)
user3.groups.add(group4)

user4 = Usuario.objects.get(username="desarrollador1")
user4.groups.add(group3)
user4 = Usuario.objects.get(username="desarrollador2")
user4.groups.add(group3)
user4 = Usuario.objects.get(username="desarrollador3")
user4.groups.add(group3)


user4 = Usuario.objects.get(username="scrummaster1")
user4.groups.add(group2)
user4 = Usuario.objects.get(username="scrummaster2")
user4.groups.add(group2)

user4 = Usuario.objects.get(username="cliente1")
user4.groups.add(group1)
user4 = Usuario.objects.get(username="cliente2")
user4.groups.add(group1)

########################################################################################################################

######################### Carga de Proyectos ###########################################################################

nombre_proyecto = 'Proyecto 1'
Codigo = 'pro1'
Descripcion = "proyecto 1"
Fecha_inicio = datetime.now()- timedelta(days=+15)
Fecha_finalizacion = datetime.now() + timedelta(days=+60)
Scrum_master = Usuario.objects.get(username="froman")
proyecto1 = Proyecto(nombre_proyecto=nombre_proyecto,descripcion_proyecto=Descripcion, codigo_proyecto=Codigo, estado_proyecto='PENDIENTE',
                     fecha_inicio=Fecha_inicio, fecha_finalizacion=Fecha_finalizacion, scrum_master=Scrum_master,cliente=Usuario.objects.get(username="cliente1")
                     )
proyecto1.save()
proyecto1.save()
proyecto1.equipo_desarrollo.add(proyecto1.id, Usuario.objects.get(username="lbenitez") )
proyecto1.equipo_desarrollo.add(proyecto1.id, Usuario.objects.get(username="bmaluff") )
proyecto1.equipo_desarrollo.add(proyecto1.id, Usuario.objects.get(username="desarrollador1") )
proyecto1.equipo_desarrollo.add(proyecto1.id, Usuario.objects.get(username="desarrollador2") )
proyecto1.save()

nombre_proyecto = 'Proyecto 2'
Codigo = 'pro2'
Descripcion = "proyecto 2"
Fecha_inicio = datetime.now()
Fecha_finalizacion = datetime.now() + timedelta(days=+90)
Scrum_master = Usuario.objects.get(username="lbenitez")
proyecto2 = Proyecto(nombre_proyecto=nombre_proyecto,descripcion_proyecto=Descripcion, codigo_proyecto=Codigo, estado_proyecto='PENDIENTE',
                     fecha_inicio=Fecha_inicio, fecha_finalizacion=Fecha_finalizacion, scrum_master=Scrum_master,cliente=user1
                     )
proyecto2.save()
proyecto2.equipo_desarrollo.add(proyecto2.id, Usuario.objects.get(username="froman") )
proyecto2.equipo_desarrollo.add(proyecto2.id, Usuario.objects.get(username="bmaluff") )
proyecto2.equipo_desarrollo.add(proyecto2.id, Usuario.objects.get(username="desarrollador1") )
proyecto2.equipo_desarrollo.add(proyecto2.id, Usuario.objects.get(username="desarrollador2") )
proyecto2.save()

nombre_proyecto = 'Proyecto 3'
Codigo = 'pro3'
Descripcion = "proyecto 3"
Fecha_inicio = datetime.now()
Fecha_finalizacion = datetime.now() + timedelta(days=+120)
Scrum_master = Usuario.objects.get(username="bmaluff")
proyecto3 = Proyecto(nombre_proyecto=nombre_proyecto,descripcion_proyecto=Descripcion, codigo_proyecto=Codigo, estado_proyecto='PENDIENTE',
                     fecha_inicio=Fecha_inicio, fecha_finalizacion=Fecha_finalizacion, scrum_master=Scrum_master,cliente=user2
                     )
proyecto3.save()
proyecto3.equipo_desarrollo.add(proyecto3.id, Usuario.objects.get(username="froman") )
proyecto3.equipo_desarrollo.add(proyecto3.id, Usuario.objects.get(username="lbenitez") )
proyecto3.equipo_desarrollo.add(proyecto3.id, Usuario.objects.get(username="desarrollador1") )
proyecto3.equipo_desarrollo.add(proyecto3.id, Usuario.objects.get(username="desarrollador2") )
proyecto3.save()


########################################################################################################################

######################### Carga de Sprints #############################################################################


sprint1 = Sprint(nombre_sprint="Sprint1", id_proyecto=proyecto1,numero_sprint=1 ,fecha_inicio=datetime.now() - timedelta(days=+15) , fecha_fin=datetime.now() + timedelta(days=+15), estado='Pendiente')
sprint1.save()
sprint2 = Sprint(nombre_sprint="Sprint2", id_proyecto=proyecto1,numero_sprint=2 , fecha_inicio=Fecha_inicio, fecha_fin=datetime.now() + timedelta(days=+15) + timedelta(days=+30), estado='Pendiente')
sprint2.save()
sprint3 = Sprint(nombre_sprint="Sprint3", id_proyecto=proyecto2,numero_sprint=1 , fecha_inicio=Fecha_inicio, fecha_fin=Fecha_finalizacion, estado='Pendiente')
sprint3.save()
########################################################################################################################

######################### Carga de US - 3 Por Proyecto ####################################################################
userstory = UserStory(nombre='US1 - Proyecto1', descripcion= 'US', prioridad='ALTA', codigo='us-1',valor_de_negocio=4, valor_tecnico=8,usuario_asignado=user1, proyecto=proyecto1, size=8,horas_dedicadas=36, porcentaje_realizado=100,estado="APROBADO")
userstory.save()
userstory = UserStory(nombre='US2 - Proyecto1', descripcion= 'US', prioridad='ALTA', codigo='us-2',valor_de_negocio=4, valor_tecnico=8,usuario_asignado=user1, proyecto=proyecto1, size=3,horas_dedicadas=40 ,  porcentaje_realizado=100,estado="APROBADO")
userstory.save()
userstory = UserStory(nombre='US3 - Proyecto1', descripcion= 'US', prioridad='ALTA', codigo='us-3',valor_de_negocio=4, valor_tecnico=8,usuario_asignado=user1, proyecto=proyecto1, size=5)
userstory.save()

userstory = UserStory(nombre='US1 - Proyecto2', descripcion= 'US', prioridad='ALTA', codigo='us-1',valor_de_negocio=4, valor_tecnico=8,usuario_asignado=user2, proyecto=proyecto2, size=10)
userstory.save()
userstory = UserStory(nombre='US2 - Proyecto2', descripcion= 'US', prioridad='ALTA', codigo='us-2',valor_de_negocio=4, valor_tecnico=8,usuario_asignado=user2, proyecto=proyecto2, size=10)
userstory.save()
userstory = UserStory(nombre='US3 - Proyecto2', descripcion= 'US', prioridad='ALTA', codigo='us-3',valor_de_negocio=4, valor_tecnico=8,usuario_asignado=user2, proyecto=proyecto2, size=10)
userstory.save()

userstory = UserStory(nombre='US1 - Proyecto3', descripcion= 'US', prioridad='ALTA', codigo='us-1',valor_de_negocio=4, valor_tecnico=8,usuario_asignado=user2, proyecto=proyecto3, size=10)
userstory.save()
userstory = UserStory(nombre='US2 - Proyecto3', descripcion= 'US', prioridad='ALTA', codigo='us-2',valor_de_negocio=4, valor_tecnico=8,usuario_asignado=user2, proyecto=proyecto3, size=10)
userstory.save()
userstory = UserStory(nombre='US3 - Proyecto3', descripcion= 'US', prioridad='ALTA', codigo='us-3',valor_de_negocio=4, valor_tecnico=8,usuario_asignado=user2, proyecto=proyecto3, size=10)
userstory.save()
###########################################################################################################################


######################### Asignacion de US a sprint   ####################################################################

sprint = Sprint.objects.get(nombre_sprint="Sprint1")
userstory = UserStory.objects.get(nombre="US1 - Proyecto1")
userstory.nombre_sprint = sprint.nombre_sprint
userstory.save()

userstory = UserStory.objects.get(nombre="US2 - Proyecto1")
userstory.nombre_sprint = sprint.nombre_sprint
userstory.save()

userstory = UserStory.objects.get(nombre='US3 - Proyecto1')
userstory.nombre_sprint = sprint.nombre_sprint
userstory.save()

###########################################################################################################################


######################### Carga de flujos  #############################################################################

flujo1 = Flujo(nombre_flujo="Flujo 1 - Proyecto 1",id_Proyecto=proyecto1)
flujo1.save()

flujo2 = Flujo(nombre_flujo="Flujo 2 - Proyecto 1",id_Proyecto=proyecto1)
flujo2.save()

flujo3 = Flujo(nombre_flujo="Flujo 1 - Proyecto 2",id_Proyecto=proyecto2)
flujo3.save()

########################################################################################################################


######################### Carga de Burndown chart sprint ###############################################################
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
########################################################################################################################



######################### Carga de Burndown chart proyecto ###############################################################
proyecto = Proyecto.objects.get(nombre_proyecto="Proyecto 1")
fecha_proyecto_inicio = datetime.combine(proyecto.fecha_inicio , datetime.min.time())
fecha_proyecto_fin = datetime.combine(proyecto.fecha_finalizacion , datetime.min.time())
fecha_actual = datetime.now()- timedelta(days=+14)
dias_restantes = fecha_proyecto_fin - fecha_actual
BurndownChartProyecto(id_proyecto=proyecto.id,dia = dias_restantes.days+1,horas_trabajadas=2).save()


fecha_actual = datetime.now()  - timedelta(days=+13)
dias_restantes = fecha_proyecto_fin - fecha_actual
BurndownChartProyecto(id_proyecto=proyecto.id,dia = dias_restantes.days+1,horas_trabajadas=1).save()

fecha_actual = datetime.now()  - timedelta(days=+12)
dias_restantes = fecha_proyecto_fin - fecha_actual
BurndownChartProyecto(id_proyecto=proyecto.id,dia = dias_restantes.days+1,horas_trabajadas=0).save()

fecha_actual = datetime.now()  - timedelta(days=+11)
dias_restantes = fecha_proyecto_fin - fecha_actual
BurndownChartProyecto(id_proyecto=proyecto.id,dia = dias_restantes.days+1,horas_trabajadas=1).save()

fecha_actual = datetime.now()  - timedelta(days=+10)
dias_restantes = fecha_proyecto_fin - fecha_actual
BurndownChartProyecto(id_proyecto=proyecto.id,dia = dias_restantes.days+1,horas_trabajadas=0).save()


######################### Carga de Actividades##########################################################################

actividad1 = Actividad(id_Flujo_id=flujo1.id,nombre_actividad="Actividad_1",orden_actividad=1,estado_actividad="ToDo")
actividad1.save()
actividad2 = Actividad(id_Flujo_id=flujo1.id,nombre_actividad="Actividad_2",orden_actividad=2,estado_actividad="ToDo")
actividad2.save()
actividad3 = Actividad(id_Flujo_id=flujo2.id,nombre_actividad="Actividad_1",orden_actividad=3,estado_actividad="ToDo")
actividad3.save()

########################################################################################################################
