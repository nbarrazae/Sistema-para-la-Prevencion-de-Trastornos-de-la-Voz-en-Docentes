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
from django.template.loader import render_to_string


def index(request):
    return render(request, 'index.html')
def instituciones(request):
    orden = request.GET.get('orden', 'nombre_institucion')  # Orden por defecto
    if orden not in ['nombre_institucion', 'rut_institucion']:
        orden = 'nombre_institucion'

    instituciones = Institucion.objects.all().order_by(orden)

    paginator = Paginator(instituciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'instituciones.html', {
        'page_obj': page_obj,
        'page_range': paginator.get_elided_page_range(number=page_obj.number, on_each_side=2, on_ends=1),
        'orden_actual': orden,
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

def crear_institucion(request):
    if request.method == "POST":
        institucion = Institucion(
            nombre_institucion=request.POST.get("nombre_institucion"),
            rut_institucion=request.POST.get("rut_institucion"),
            direccion=request.POST.get("direccion"),
            sitio_web=request.POST.get("sitio_web"),
            representante_legal=request.POST.get("representante_legal"),
            telefono_institucion=request.POST.get("telefono_institucion"),
            correo_institucion=request.POST.get("correo_institucion")
        )
        institucion.save()
        return redirect('instituciones')  # o tu vista actual

def obtener_aulas(request, pk):
    institucion = get_object_or_404(Institucion, pk=pk)
    #busca todas las aulas de la institucion
    aulas = Aula.objects.filter(id_institucion=institucion)
    # Si no hay aulas, devuelve un mensaje
    # if not aulas:
    #     return JsonResponse({'html': '<p>No hay aulas disponibles</p>'})
    try:
        html = render_to_string("partials/modal_aulas.html", {'aulas': aulas, 'institucion': institucion}, request=request)
        return JsonResponse({'html': html})
    except Exception as e:
        print("❌ Error al renderizar:", e)
        return JsonResponse({'html': '<p>Error al cargar aulas</p>'})

import json

def crear_aula(request, pk):
    if request.method == "POST":
        print("📥 Recibido POST JSON")

        data = json.loads(request.body)
        print("Contenido del JSON:", data)  # 👈 Aquí ves qué se está enviando

        aula = Aula(
            nro_aula=data.get("nro_aula"),
            tamaño=data.get("tamanio"),
            cantidad_alumnos=data.get("cantidad_alumnos"),
            descripcion=data.get("descripcion"),
            id_institucion_id=pk  # 👈 Ya viene en la URL
        )
        aula.save()

        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

def eliminar_aula(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    if request.method == 'POST':
        aula.delete()
        return redirect('instituciones')  # Nombre de tu vista principal

    return render(request, 'confirmar_eliminacion.html', {'aula': aula})
    

def modificar_aula(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            aula = Aula.objects.get(pk=pk)
            aula.nro_aula = data.get("nro_aula", aula.nro_aula)
            aula.tamaño = data.get("tamanio", aula.tamaño)
            aula.cantidad_alumnos = data.get("cantidad_alumnos", aula.cantidad_alumnos)
            aula.descripcion = data.get("descripcion", aula.descripcion)
            aula.save()
            return JsonResponse({"success": True})
        except Aula.DoesNotExist:
            return JsonResponse({"success": False, "error": "Aula no encontrada"})


@csrf_exempt  # solo si no estás manejando CSRF correctamente en el fetch
def eliminar_aula(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    if request.method == 'POST':
        aula.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=400)



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