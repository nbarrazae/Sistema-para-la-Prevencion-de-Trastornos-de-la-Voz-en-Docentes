from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstitucionViewSet, ProfesorViewSet, AulaViewSet, HorarioViewSet, registrarvar, index, instituciones, profesores, usuarios, estadisticas, variables_ambientales, variables_voz, dispositivos_iot, eliminar_institucion, editar_institucion, crear_institucion, obtener_aulas, crear_aula, eliminar_aula, modificar_aula, eliminar_aula

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
    path('', index, name='index'),


    
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
    path('institucion/<int:pk>/aulas/', obtener_aulas, name='obtener_aulas'),
    path('institucion/<int:pk>/aulas/agregar/', crear_aula, name='agregar_aula'),
    path('institucion/aula/<int:pk>/modificar/', modificar_aula, name='modificar_aula'),
    path('institucion/aula/<int:pk>/eliminar/', eliminar_aula, name='eliminar_aula')



]
