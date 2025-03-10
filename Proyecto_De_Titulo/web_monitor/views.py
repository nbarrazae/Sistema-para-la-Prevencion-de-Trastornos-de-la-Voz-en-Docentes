from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializer import InstitucionSerializer, ProfesorSerializer, AulaSerializer, HorarioSerializer
from .models import Institucion, Profesor, Aula, Horario

class InstitucionViewSet(viewsets.ModelViewSet):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer
    lookup_field = 'rut_institucion'  # Permite buscar por nombre


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
        rut_institucion = self.request.query_params.get('rut_institucion')  # Cambio a RUT
        
        if nro_aula and rut_institucion:
            queryset = queryset.filter(nro_aula=nro_aula, id_institucion__rut_institucion=rut_institucion)
        elif rut_institucion:
            queryset = queryset.filter(id_institucion__rut_institucion=rut_institucion)  # Filtra todas las aulas de la institución
        
        return queryset

    def get_object(self):
        nro_aula = self.kwargs.get('nro_aula')
        rut_institucion = self.kwargs.get('rut_institucion')  # Cambio a RUT

        try:
            return Aula.objects.get(nro_aula=nro_aula, id_institucion__rut_institucion=rut_institucion)
        except Aula.DoesNotExist:
            raise NotFound({"error": "Aula no encontrada"})

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        rut_profesor = self.request.query_params.get('rut_profesor')
        nro_aula = self.request.query_params.get('nro_aula')
        rut_institucion = self.request.query_params.get('rut_institucion')  # Cambio a RUT
        dia = self.request.query_params.get('dia')

        if rut_profesor:
            queryset = queryset.filter(id_profesor__rut_profesor=rut_profesor)
        if nro_aula and rut_institucion:
            queryset = queryset.filter(id_aula__nro_aula=nro_aula, id_aula__id_institucion__rut_institucion=rut_institucion)
        if dia:
            queryset = queryset.filter(dia=dia)
        
        return queryset
    def get_object(self):
        """ Busca un horario basado en los datos enviados (sin usar ID). """
        kwargs = self.kwargs  # Parámetros de la URL
        try:
            return Horario.objects.get(
                id_profesor__rut_profesor=kwargs['rut_profesor'],
                id_aula__nro_aula=kwargs['nro_aula'],
                id_aula__id_institucion__nombre_institucion=kwargs['nombre_institucion'],
                dia=kwargs['dia'],
                hora_inicio=kwargs['hora_inicio'],
                hora_termino=kwargs['hora_termino']
            )
        except Horario.DoesNotExist:
            raise NotFound("Horario no encontrado")