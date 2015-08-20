from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),

    # URL's Para el sistema
    url(r'^$', 'GestiondeSistema.views.login_view', name='login'),
    url(r'^home', 'GestiondeSistema.views.home', name='home'),
    url(r'^login', 'GestiondeSistema.views.login_view', name='login'),
    url(r'^logout', 'GestiondeSistema.views.logout_view', name='logout'),
    url(r'^auditoria', 'GestiondeSistema.views.visualizar_auditoria_view', name='auditoria'),
    url(r'^reporte_product_backlog/(?P<id_proyecto>\d+)$', 'GestiondeSistema.views.reporte_product_backlog_pdf_view',name='reporteproductbacklog'),
    url(r'^reporte_sprint_backlog/(?P<id_sprint>\d+)$', 'GestiondeSistema.views.reporte_sprint_backlog_pdf_view',name='reportesprintbacklog'),

    # URL's Para la gestion usuario
    url(r'^usuario', 'GestiondeUsuarios.views.crear_usuario_view', name='crearusuario'),
    url(r'^listar_usuario', 'GestiondeUsuarios.views.listar_usuarios_filtro_view', name='listar_usuarios'),
    url(r'^modificar_usuario/(?P<id_usuario>\d+)$', 'GestiondeUsuarios.views.modificar_usuario_view', name='modificarusuario'),
    url(r'^consultar_usuario/(?P<id_usuario>\d+)$', 'GestiondeUsuarios.views.consultar_usuario_view', name='consultar_usuario'),
    url(r'^eliminar_usuario/(?P<id_usuario>\d+)$', 'GestiondeUsuarios.views.eliminar_usuario_view', name='eliminar_usuario'),
    url(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),

    # URL's Para la gestion de roles
    url(r'^crear_rol','GestiondeRolesyPermisos.views.crear_rol_view',name='crearrol'),
    url(r'^listar_roles', 'GestiondeRolesyPermisos.views.listar_roles_filtro_view', name='listar_roles'),
    url(r'^modificar_rol/(?P<id_rol>\d+)$', 'GestiondeRolesyPermisos.views.modificar_rol_view', name='modificarrol'),
    url(r'^eliminar_rol/(?P<id_rol>\d+)$', 'GestiondeRolesyPermisos.views.eliminar_rol_view', name='eliminarrol'),
    url(r'^consultar_rol/(?P<id_rol>\d+)$', 'GestiondeRolesyPermisos.views.consultar_rol_view', name='consultarrol'),

    # URL's Para listar permisos
    url(r'^listar_permisos', 'GestiondeRolesyPermisos.views.listar_permisos_view', name='listar_permisos'),

    # URL's Para la gestion de flujo
    url(r'^SeleccionProyectoFlujo','GestiondeFlujos.views.listar_proyecto_flujo_view', name='listar_proyecto_flujo'),
    url(r'^crear_flujo/(?P<id_proyecto>\d+)$', 'GestiondeFlujos.views.crear_flujo_view', name='crear_flujo'),
    url(r'^listar_flujo/(?P<id_proyecto>\d+)$',  'GestiondeFlujos.views.listar_flujo_view', name='listar_flujo'),
    url(r'^consultar_flujo/(?P<id_proyecto>\d+)/(?P<id_flujo>\d+)$', 'GestiondeFlujos.views.consultar_flujo_view', name='consultar_flujo'),
    url(r'^eliminar_flujo/(?P<id_proyecto>\d+)/(?P<id_flujo>\d+)$', 'GestiondeFlujos.views.eliminar_flujo_view', name='eliminarflujo'),
    url(r'^modificar_flujo/(?P<id_proyecto>\d+)/(?P<id_flujo>\d+)$', 'GestiondeFlujos.views.modificar_flujo_view', name='modificar_flujo'),
    url(r'^ListarTodosLosFlujos', 'GestiondeFlujos.views.listar_proyecto_flujos_listado_view', name='listar_todos_flujos'),

    # URL's Para la gestion de actividades
    url(r'^crear_actividad/(?P<id_proyecto>\d+)/(?P<id_flujo>\d+)$', 'GestiondeFlujos.views.agregar_actividad_view', name='crear_actividad'),
    url(r'^listar_actividad/(?P<id_proyecto>\d+)/(?P<id_flujo>\d+)$', 'GestiondeFlujos.views.listar_actividad_view', name='listar_actividad'),
    url(r'^eliminar_actividad/(?P<id_proyecto>\d+)/(?P<id_flujo>\d+)/(?P<id_actividad>\d+)$', 'GestiondeFlujos.views.eliminar_actividad_view', name='eliminaractividad'),
    url(r'^modificar_actividad/(?P<id_proyecto>\d+)/(?P<id_flujo>\d+)/(?P<id_actividad>\d+)$', 'GestiondeFlujos.views.modificar_actividad_view', name='modificar_actividad'),


    #URL's Para la gestion de proyectos
    url(r'^crear_proyecto','GestiondeProyectos.views.crear_proyecto_view', name='crear_proyecto'),
    url(r'^listar_proyecto','GestiondeProyectos.views.listar_proyecto_view', name='listar_proyecto'),
    url(r'^modificar_proyecto/(?P<id_proyecto>\d+)$', 'GestiondeProyectos.views.modificar_proyecto_view', name='modificarproyecto'),
    url(r'^consultar_proyecto/(?P<id_proyecto>\d+)$', 'GestiondeProyectos.views.consultar_proyecto_view', name='consultar_proyecto'),
    url(r'^generar_reporte/(?P<id_proyecto>\d+)$',  'GestiondeProyectos.views.reporte_proyecto_view', name='generar_reporte'),
    url(r'^product_backlog/(?P<id_proyecto>\d+)$', 'GestiondeProyectos.views.product_backlog_view', name='product_backlog'),
    url(r'^grafico_estado_us/(?P<id_userStory>\d+)$', 'GestiondeProyectos.views.grafico_estado_us_view', name='grafico_us_estado'),


    #URL's Para la gestion de user stories
    url(r'^SeleccionProyectoUS','GestiondeUserStories.views.listar_proyecto_us_view', name='listar_proyecto_us'),
    url(r'^crear_userstory/(?P<id_proyecto>\d+)$','GestiondeUserStories.views.crear_userstory_view', name='crear_userstory'),
    url(r'^consultar_userstory/(?P<id_userStory>\d+)$', 'GestiondeUserStories.views.consultar_userstory_view', name='consultar_userstory'),
    url(r'^modificar_userstory/(?P<id_userStory>\d+)$', 'GestiondeUserStories.views.modificar_userstory_view', name='modificar_userstory'),
    url(r'^ListarTodosLosUS', 'GestiondeUserStories.views.listar_todos_us_view', name='listar_todos_us'),
    url(r'^listar_userstories_proyecto/(?P<id_proyecto>\d+)$','GestiondeUserStories.views.listar_userstories_proyecto_view', name='listar_userstories_proyecto'),
    url(r'^comentario_userstory/(?P<id_userStory>\d+)$', 'GestiondeUserStories.views.listar_comentarios_us_view', name='comentario_userstory'),
    url(r'^ListarLosUSs', 'GestiondeUserStories.views.listar_proyecto_US_listado_view', name='listar_uss'),

    
    #URL's Para la gestion de sprints
    url(r'^SeleccionProyectoSprint','GestiondeSprints.views.listar_proyecto_sprint_view', name='listar_proyecto_sprint'),
    url(r'^crear_sprint/(?P<id_proyecto>\d+)$', 'GestiondeSprints.views.crear_sprint_view', name='crear_sprint'),
    url(r'^listar_sprint/(?P<id_proyecto>\d+)$',  'GestiondeSprints.views.listar_sprint_view', name='listar_sprint'),
    url(r'^consultar_sprint/(?P<id_proyecto>\d+)/(?P<id_sprint>\d+)$',  'GestiondeSprints.views.consultar_sprint_view', name='consultar_sprint'),
    url(r'^modificar_sprint/(?P<id_proyecto>\d+)/(?P<id_sprint>\d+)$',  'GestiondeSprints.views.modificar_sprint_view', name='modificar_sprint'),
    url(r'^eliminar_sprint/(?P<id_proyecto>\d+)/(?P<id_sprint>\d+)$',  'GestiondeSprints.views.eliminar_sprint_view', name='eliminar_sprint'),
    url(r'^AsignarUSaSprint/(?P<id_sprint>\d+)',  'GestiondeSprints.views.asignar_user_story_a_sprint', name='asingarUsASprint'),
    url(r'^ListarTodosLosSprint', 'GestiondeSprints.views.listar_todos_sprints_view', name='listar_todos_sprint'),
    url(r'^sprint_backlog/(?P<id_sprint>\d+)$', 'GestiondeSprints.views.sprint_backlog_view', name='sprint_backlog'),
    url(r'^reportewip', 'GestiondeSprints.views.ReporpteWIP_view', name='reporte_wip'),


    #URL's Para la gestion de BurndownChart
    url(r'^BurndownChartSprint/(?P<id_sprint>\d+)',  'GestiondeBurndownChart.views.visualizar_burdownchart_sprint', name='burndownchartSprint'),
    url(r'^ActualizarBurndownChartSprint/(?P<id_sprint>\d+)',  'GestiondeBurndownChart.views.actualizar_burdownchart_sprint', name='actualizarburndownsprint'),
    url(r'^BurndownChartProyecto/(?P<id_proyecto>\d+)',  'GestiondeBurndownChart.views.visualizar_burdownchart_proyecto', name='burndownchartproyecto'),
    url(r'^ActualizarBurndownChartProyecto/(?P<id_proyecto>\d+)',  'GestiondeBurndownChart.views.actualizar_burdownchart_proyecto', name='actualizarburndownproyecto'),

    #URL's Para la gestion de tablero kanban
    url(r'^SeleccionProyectoTableroKanban','GestiondeTableroKanban.views.listar_proyecto_kanban_view', name='listar_proyecto_kanban'),
    url(r'^CrearTableroKanban/(?P<id_proyecto>\d+)$', 'GestiondeTableroKanban.views.crear_tablero_kanban_view', name='crear_tablero_kanban'),
    url(r'^ListaTableroKanbanProyecto/(?P<id_proyecto>\d+)$', 'GestiondeTableroKanban.views.listar_tablero_kanban_proyecto_view', name='listar_tablero_kanban_proyecto'),
    url(r'^ListaTableroKanban', 'GestiondeTableroKanban.views.listar_tablero_kanban_view', name='listar_tablero_kanban'),
    url(r'^ConsultarTableroKanban/(?P<id_tablero>\d+)$', 'GestiondeTableroKanban.views.consultar_tablero_kanban_view', name='consultar_tablero_kanban'),
    url(r'^CambioEstadoActividad/(?P<id_tablero>\d+)/(?P<id_us>\d+)$', 'GestiondeTableroKanban.views.cambio_us_actividad_estado_tablero_kanban_view', name='cambio_estado_actividad'),
    url(r'^ModificarTableroKanban/(?P<id_tablero>\d+)$', 'GestiondeTableroKanban.views.modificar_tablero_kanban_view', name='modificar_tablero_kanban'),
    url(r'^VisualizarTableroKanban/(?P<id_tablero>\d+)$', 'GestiondeTableroKanban.views.visualizar_tablero_kanban_view', name='visualizar_tablero_kanban'),

    #URL's Para la gestion de Mensajeria
    url(r'^enviar_mensaje','GestiondeMensajeria.views.enviar_mensaje_view',name='enviar_mensaje'),
    url(r'^visualizar_mensaje/(?P<id_mensaje>\d+)$','GestiondeMensajeria.views.visualizar_mensaje_view',name='visualizar_mensaje'),
    url(r'^listar_mensajes','GestiondeMensajeria.views.listar_mensajes_view',name='listar_mensajes'),

    #URL's Para la gestion de Releases
    url(r'^SeleccionProyectoRelease$','GestiondeReleases.views.listar_proyectos_release_view',name='listar_proyecto_release'),
    url(r'^crear_release/(?P<id_proyecto>\d+)$', 'GestiondeReleases.views.crear_release_view', name='crear_release'),
    url(r'^consultar_release/(?P<id_release>\d+)$', 'GestiondeReleases.views.consultar_release_view', name='consultar_release'),
    url(r'^listar_releases_proyecto/(?P<id_proyecto>\d+)$','GestiondeReleases.views.listar_releases_view', name='listar_releases_proyecto'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

