from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstitucionViewSet, ProfesorViewSet, AulaViewSet, HorarioViewSet, registrarvar, index, instituciones, profesores, usuarios, estadisticas, variables_ambientales, variables_voz, dispositivos_iot, eliminar_institucion, editar_institucion, crear_institucion, obtener_aulas, crear_aula, eliminar_aula, modificar_aula, eliminar_aula,crear_profesor, editar_profesor, eliminar_profesor, aulas_por_institucion, horarios_por_profesor, eliminar_horario, agregar_horario, crear_dispositivo, eliminar_dispositivo, obtener_opciones, asignar_dispositivo, obtener_instituciones, profesores_por_institucion, aulas_por_institucion, exportar_instituciones_y_aulas_csv,exportar_profesores_y_horarios_csv, exportar_dispositivos_iot_csv, login_view, logout_view,error_404_view

router = DefaultRouter()
router.register(r'instituciones', InstitucionViewSet)
router.register(r'profesores', ProfesorViewSet)
router.register(r'aulas', AulaViewSet)
router.register(r'horarios', HorarioViewSet, basename='horario')




urlpatterns = [
    path('api/', include(router.urls)),
    path('api/aulas/<str:nro_aula>/<str:rut_institucion>/',    AulaViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='aula-detail'),
    path(
        'api/horarios/<str:rut_profesor>/<str:nro_aula>/<str:nombre_institucion>/<str:dia>/<str:hora_inicio>/<str:hora_termino>/',
        HorarioViewSet.as_view({'put': 'update', 'delete': 'destroy'}),
        name='horario-detail'
    ),
    path('api/registrovar', registrarvar, name='registrarvar'),
    path('home', index, name='index'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),


    
    path('instituciones/', instituciones, name='instituciones'),
    path('profesores/', profesores, name='profesores'),
    path('dispositivos_iot/', dispositivos_iot, name='iot'),
    path('usuarios/', usuarios, name='usuarios'),
    path('estadisticas/', estadisticas, name='estadisticas'),
    path('variables_ambientales/', variables_ambientales, name='variables_ambientales'),
    path('variables_voz/', variables_voz, name='variables_voz'),

    path('instituciones/eliminar/<int:pk>/', eliminar_institucion, name='eliminar_institucion'),
    path('instituciones/editar/<int:pk>/', editar_institucion, name='editar_institucion'),
    path('instituciones/crear/', crear_institucion, name='crear_institucion'),
    path('instituciones/exportar_csv/', exportar_instituciones_y_aulas_csv, name='exportar_instituciones_csv'),

    path('institucion/<int:pk>/aulas/', obtener_aulas, name='obtener_aulas'),
    path('institucion/<int:pk>/aulas/agregar/', crear_aula, name='agregar_aula'),
    path('institucion/aula/<int:pk>/modificar/', modificar_aula, name='modificar_aula'),
    path('institucion/aula/<int:pk>/eliminar/', eliminar_aula, name='eliminar_aula'),

    # path('instituciones/buscar_ajax/', buscar_instituciones_ajax, name='buscar_instituciones_ajax'),

    path('profesores/crear/', crear_profesor, name='crear_profesor'),
    path('profesores/editar/<int:pk>/', editar_profesor, name='editar_profesor'),
    path('profesores/eliminar/<int:id_profesor>/', eliminar_profesor, name='eliminar_profesor'),
    path('profesores/exportar_csv/', exportar_profesores_y_horarios_csv, name='exportar_profesores_y_horarios_csv'),

    path('aulas_por_institucion/<int:id_institucion>/', aulas_por_institucion),
    path('horarios_por_profesor/<int:id_profesor>/', horarios_por_profesor),
    path('eliminar_horario/<int:id_horario>/', eliminar_horario, name='eliminar_horario'),
    path('agregar_horario/', agregar_horario, name='agregar_horario'),

    # path('profesores/buscar_ajax/', buscar_profesores_ajax, name='buscar_profesores_ajax'),

    path('dispositivos_iot/crear/', crear_dispositivo, name='crear_dispositivo_iot'),
    path('dispositivos/eliminar/<str:mac>/', eliminar_dispositivo, name='eliminar_dispositivo'),
    path('obtener_opciones/<int:institucion_id>/<str:tipo>/', obtener_opciones, name='obtener_opciones'),
    path('asignar-dispositivo/', asignar_dispositivo, name='asignar_dispositivo'),
    path('obtener-instituciones/', obtener_instituciones, name='obtener_instituciones'),
    path('api/profesores_por_institucion/<int:id_institucion>/', profesores_por_institucion, name='profesores_por_institucion'),
    path('api/aulas_por_institucion/<int:id_institucion>/', aulas_por_institucion, name='aulas_por_institucion'),
    path('exportar_dispositivos_iot_csv/', exportar_dispositivos_iot_csv, name='exportar_dispositivos_iot_csv'),

    path('error_404/', error_404_view, name='error_404_view'),



]