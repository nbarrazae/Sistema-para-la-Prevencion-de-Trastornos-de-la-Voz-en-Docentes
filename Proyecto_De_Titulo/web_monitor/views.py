from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializer import InstitucionSerializer, ProfesorSerializer, AulaSerializer, HorarioSerializer
from .models import Institucion, Profesor, Aula, Horario

class InstitucionViewSet(viewsets.ModelViewSet):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer
    lookup_field = 'nombre_institucion'  # Permite buscar por nombre


class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    lookup_field = 'rut_profesor'  # Permite buscar por RUT

class AulaViewSet(viewsets.ModelViewSet):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        nro_aula = self.request.query_params.get('nro_aula')
        nombre_institucion = self.request.query_params.get('nombre_institucion')
        if nro_aula and nombre_institucion:
            queryset = queryset.filter(nro_aula=nro_aula, id_institucion__nombre_institucion=nombre_institucion)
        return queryset

    def get_object(self):
        nro_aula = self.kwargs.get('nro_aula')
        nombre_institucion = self.kwargs.get('nombre_institucion')
        try:
            return Aula.objects.get(nro_aula=nro_aula, id_institucion__nombre_institucion=nombre_institucion)
        except Aula.DoesNotExist:
            return Response({"error": "Aula no encontrada"}, status=status.HTTP_404_NOT_FOUND)

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        rut_profesor = self.request.query_params.get('rut_profesor')
        nro_aula = self.request.query_params.get('nro_aula')
        nombre_institucion = self.request.query_params.get('nombre_institucion')
        if rut_profesor:
            queryset = queryset.filter(id_profesor__rut_profesor=rut_profesor)
        if nro_aula and nombre_institucion:
            queryset = queryset.filter(id_aula__nro_aula=nro_aula, id_aula__id_institucion__nombre_institucion=nombre_institucion)
        return queryset