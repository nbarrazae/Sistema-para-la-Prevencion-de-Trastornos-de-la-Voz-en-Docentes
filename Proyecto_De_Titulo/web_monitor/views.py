from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializer import InstitucionSerializer, ProfesorSerializer, AulaSerializer, HorarioSerializer
from .models import Institucion, Profesor, Aula, Horario
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect



def index(request):
    return render(request, 'index.html')
def instituciones(request):
    #obterner todas las instituciones y pasarlas al template
    instituciones = Institucion.objects.all()
    paginator = Paginator(instituciones, 10)  # 10 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'instituciones.html', {
        'page_obj': page_obj,
        'page_range': paginator.get_elided_page_range(number=page_obj.number, on_each_side=2, on_ends=1),
    })
def eliminar_institucion(request, pk):
    institucion = get_object_or_404(Institucion, pk=pk)
    if request.method == 'POST':
        institucion.delete()
        return redirect('instituciones')  # Nombre de tu vista principal

    return render(request, 'confirmar_eliminacion.html', {'institucion': institucion})
def editar_institucion(request, pk):
    institucion = get_object_or_404(Institucion, pk=pk)
    if request.method == "POST":
        institucion.nombre_institucion = request.POST.get("nombre_institucion")
        institucion.rut_institucion = request.POST.get("rut_institucion")
        institucion.direccion = request.POST.get("direccion")
        institucion.telefono_institucion = request.POST.get("telefono_institucion")
        institucion.correo_institucion = request.POST.get("correo_institucion")
        institucion.save()
        return redirect('instituciones')  # o tu vista actual





def profesores(request):
    return render(request, 'profesores.html')
def dispositivos_iot(request):
    return render(request, 'dispositivos_iot.html')
def usuarios(request):
    return render(request, 'usuarios.html')
def estadisticas(request):
    return render(request, 'estadisticas.html')
def variables_ambientales(request):
    return render(request, 'variables_ambientales.html')
def variables_voz(request):
    return render(request, 'variables_voz.html')









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
@csrf_exempt
def registrarvar(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))  # Cargar JSON manualmente
            print("Datos recibidos:", data)
            return JsonResponse({"message": "Datos recibidos correctamente"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato JSON"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)