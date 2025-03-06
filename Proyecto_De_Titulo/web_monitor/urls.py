from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstitucionViewSet, ProfesorViewSet, AulaViewSet, HorarioViewSet

router = DefaultRouter()
router.register(r'instituciones', InstitucionViewSet)
router.register(r'profesores', ProfesorViewSet)
router.register(r'aulas', AulaViewSet)
router.register(r'horarios', HorarioViewSet, basename='horario')



urlpatterns = [
    path('api/', include(router.urls)),
    path('api/aulas/<str:nro_aula>/<str:nombre_institucion>/', AulaViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='aula-detail'),

]
