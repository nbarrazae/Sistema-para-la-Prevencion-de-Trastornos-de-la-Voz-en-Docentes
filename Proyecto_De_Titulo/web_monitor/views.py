from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .serializer import InstitucionSerializer, ProfesorSerializer, AulaSerializer, HorarioSerializer
from .models import Institucion, Profesor, Aula, Horario, Dispositivo_IoT, Dispositivo_IoT_Aula, Dispositivo_IoT_Profesor

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.db.models import Q
from django.db import IntegrityError
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from web_monitor.validators.profesor import validate_rut, validate_email, validate_nombre, validate_apellido, validate_sexo, validate_area_docencia, validate_antecedentes_medicos
from django.core.exceptions import ValidationError

def index(request):
    return render(request, 'index.html')

def instituciones(request):
    busqueda = request.GET.get('busqueda', '')

    instituciones = Institucion.objects.all()
    
    if busqueda:
        instituciones = instituciones.filter(
            Q(nombre_institucion__icontains=busqueda) |
            Q(rut_institucion__icontains=busqueda)
        )

    # ordenamiento
    orden = request.GET.get('orden', 'nombre_institucion')
    direccion = request.GET.get('direccion', 'asc')
    if direccion == 'desc':
        orden = '-' + orden
    instituciones = instituciones.order_by(orden)

    paginator = Paginator(instituciones, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'instituciones/base-instituciones.html', context)

def listar_instituciones(request):
    orden = request.GET.get('orden', 'nombre_institucion')
    direccion = request.GET.get('direccion', 'asc')
    
    if direccion == 'desc':
        orden = f'-{orden}'

    instituciones = Institucion.objects.all().order_by(orden)

    paginator = Paginator(instituciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    contexto = {'page_obj': page_obj}
    return render(request, 'instituciones.html', contexto)

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
        try:
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
            messages.success(request, "Institución creada correctamente.")
        except IntegrityError as e:
            print(e)
            messages.error(request, "Error: ya existe una institución con ese RUT.")
        except Exception as e:
            print(e)
            messages.error(request, f"Ocurrió un error inesperado: {str(e)}")
        return redirect('instituciones')


def obtener_aulas(request, pk):
    institucion = get_object_or_404(Institucion, pk=pk)
    #busca todas las aulas de la institucion
    aulas = Aula.objects.filter(id_institucion=institucion)
    # Si no hay aulas, devuelve un mensaje
    # if not aulas:
    #     return JsonResponse({'html': '<p>No hay aulas disponibles</p>'})
    try:
        html = render_to_string("instituciones/modals/aula_contenido.html", {'aulas': aulas, 'institucion': institucion}, request=request)
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

# def buscar_instituciones_ajax(request):
#     query = request.GET.get('q', '')
#     instituciones = Institucion.objects.filter(
#         Q(nombre_institucion__icontains=query) |
#         Q(rut_institucion__icontains=query)
#     ).values('nombre_institucion', 'rut_institucion', 'direccion')[:10]  # Devuelve máximo 10 resultados
#     return JsonResponse(list(instituciones), safe=False)



# def profesores(request):
#     return render(request, 'profesores/base-profesores.html')

def profesores(request):
    # Búsqueda
    busqueda = request.GET.get('busqueda', '')
    orden = request.GET.get('orden', 'apellido_profesor')  # orden por defecto
    direccion = request.GET.get('direccion', 'asc')
    orden_final = orden if direccion == 'asc' else f'-{orden}'
    instituciones = Institucion.objects.all()
    profesores = Profesor.objects.select_related('id_institucion')

    if busqueda:
        profesores = profesores.filter(
            Q(nombre_profesor__icontains=busqueda) |
            Q(apellido_profesor__icontains=busqueda) |
            Q(rut_profesor__icontains=busqueda) |
            Q(correo_profesor__icontains=busqueda)
        )

    profesores = profesores.order_by(orden_final)
    DIAS_SEMANA = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    # paginación
    paginator = Paginator(profesores, 10)  # 10 profesores por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # cálculo de rango de páginas para mostrar (como en el ejemplo HTML)
    page_range = []
    if paginator.num_pages <= 10:
        page_range = range(1, paginator.num_pages + 1)
    else:
        if page_obj.number <= 6:
            page_range = list(range(1, 8)) + ['…', paginator.num_pages]
        elif page_obj.number > paginator.num_pages - 6:
            page_range = [1, '…'] + list(range(paginator.num_pages - 6, paginator.num_pages + 1))
        else:
            page_range = [1, '…'] + list(range(page_obj.number - 2, page_obj.number + 3)) + ['…', paginator.num_pages]

    return render(request, 'profesores/base-profesores.html', {
        'page_obj': page_obj,
        'page_range': page_range,
        'orden': orden,
        'direccion': direccion,
        'instituciones': instituciones,
        'dias_semana': DIAS_SEMANA,
        'busqueda': busqueda,
    })

def crear_profesor(request):
    if request.method == 'POST':

        try:
            validate_rut(request.POST['rut_profesor'])
            validate_email(request.POST['correo_profesor'])
            validate_nombre(request.POST['nombre_profesor'])
            validate_apellido(request.POST['apellido_profesor'])
            validate_sexo(request.POST['sexo'])
            validate_area_docencia(request.POST['area_docencia'])
            validate_antecedentes_medicos(request.POST.get('antecedentes_medicos', ''))
            # Verifica si la institución existe antes de crear el profesor
            institucion = Institucion.objects.get(id_institucion=request.POST['id_institucion'])

            profesor = Profesor.objects.create(
                rut_profesor=request.POST['rut_profesor'],
                nombre_profesor=request.POST['nombre_profesor'],
                apellido_profesor=request.POST['apellido_profesor'],
                correo_profesor=request.POST['correo_profesor'],
                sexo=request.POST['sexo'],
                altura=request.POST.get('altura') or None,
                peso=request.POST.get('peso') or None,
                antecedentes_medicos=request.POST.get('antecedentes_medicos') or '',
                area_docencia=request.POST['area_docencia'],
                id_institucion=institucion
            )
            messages.success(request, "Profesor creado correctamente.")
        except Institucion.DoesNotExist:
            messages.error(request, "La institución seleccionada no existe.")
        except Exception as e:
            messages.error(request, f"Error al crear el profesor: {e}")
        
    return redirect('profesores')  # Redirige a la lista de profesores después de crear uno

@require_http_methods(["POST"])
def editar_profesor(request, pk):
    profesor = get_object_or_404(Profesor, pk=pk)

    # Rellenar los datos desde request.POST
    profesor.nombre_profesor = request.POST.get('nombre_profesor')
    profesor.apellido_profesor = request.POST.get('apellido_profesor')
    profesor.rut_profesor = request.POST.get('rut_profesor')
    profesor.correo_profesor = request.POST.get('correo_profesor')
    profesor.sexo = request.POST.get('sexo')
    profesor.altura = request.POST.get('altura')
    profesor.peso = request.POST.get('peso')
    profesor.antecedentes_medicos = request.POST.get('antecedentes_medicos')
    profesor.area_docencia = request.POST.get('area_docencia')
    profesor.id_institucion_id = request.POST.get('id_institucion')  # usar _id si es clave foránea

    profesor.save()

    return redirect('profesores')  # o la vista donde se lista todo


def eliminar_profesor(request, id_profesor):
    profesor = get_object_or_404(Profesor, id_profesor=id_profesor)
    if request.method == 'POST':
        profesor.delete()
        messages.success(request, 'Profesor eliminado exitosamente.')
    return redirect('profesores')

def aulas_por_institucion(request, id_institucion):
    print(id_institucion)
    aulas = Aula.objects.filter(id_institucion=id_institucion).values('id_aula', 'nro_aula')
    print(aulas)
    return JsonResponse(list(aulas), safe=False)

def horarios_por_profesor(request, id_profesor):
    horarios = Horario.objects.filter(id_profesor=id_profesor).select_related('id_aula')
    data = [
        {
            'id_horario': h.id_horario,
            'dia': h.dia,
            'hora_inicio': str(h.hora_inicio),
            'hora_termino': str(h.hora_termino),
            'nombre_aula': h.id_aula.nro_aula,
        }
        for h in horarios
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt
def eliminar_horario(request, id_horario):
    if request.method == 'POST':
        try:
            horario = Horario.objects.get(id_horario=id_horario)
            horario.delete()
            return JsonResponse({'success': True})
        except Horario.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Horario no encontrado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

from datetime import time

@csrf_exempt  # Solo si no manejas CSRF en el fetch, de lo contrario omite esto
def agregar_horario(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        id_profesor = data.get('id_profesor')
        dia = data.get('dia')
        hora_inicio = data.get('hora_inicio')
        hora_termino = data.get('hora_termino')
        id_aula = data.get('id_aula')

        horario = Horario.objects.create(
            id_profesor_id=id_profesor,
            dia=dia,
            hora_inicio=hora_inicio,
            hora_termino=hora_termino,
            id_aula_id=id_aula
        )
        return JsonResponse({'success': True, 'message': 'Horario agregado correctamente'})
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)





# relacion entre Dispositivo_IoT y su usuario (aula o profesor), buscar cada id y aquello activos == flase, devolver mac, tipo, "libre", aquellos con activo == True buscar profesor o aula, devolver mac, tipo, usuario (profesor o aula), institucion correspondiente
def dispositivos_iot(request):
    busqueda = request.GET.get('busqueda', '')
    dispositivos = Dispositivo_IoT.objects.all()

    if busqueda:
        dispositivos = dispositivos.filter(
            Q(mac_dispositivo__icontains=busqueda) |
            Q(tipo_dispositivo__icontains=busqueda)
        )

    resultado = []

    for dispositivo in dispositivos:
        entrada = {
            'mac': dispositivo.mac_dispositivo,
            'tipo': dispositivo.get_tipo_dispositivo_display(),
        }

        if not dispositivo.activo:
            entrada['estado'] = 'Libre'
            entrada['usuario'] = None
            entrada['institucion'] = None
        else:
            # Verificar si está asociado a un profesor
            try:
                rel_prof = Dispositivo_IoT_Profesor.objects.get(id_dispositivo=dispositivo)
                profesor = rel_prof.id_profesor
                entrada['estado'] = 'Asignado'
                entrada['usuario'] = f"{profesor.nombre_profesor} {profesor.apellido_profesor}"
                entrada['institucion'] = profesor.id_institucion.nombre_institucion
            except Dispositivo_IoT_Profesor.DoesNotExist:
                try:
                    # Si no está asociado a profesor, buscar si está a un aula
                    rel_aula = Dispositivo_IoT_Aula.objects.get(id_dispositivo=dispositivo)
                    aula = rel_aula.id_aula
                    entrada['estado'] = 'Asignado'
                    entrada['usuario'] = f"Aula {aula.nro_aula}"
                    entrada['institucion'] = aula.id_institucion.nombre_institucion
                except Dispositivo_IoT_Aula.DoesNotExist:
                    # Caso inesperado: activo pero sin usuario
                    entrada['estado'] = 'Asignado'
                    entrada['usuario'] = 'Desconocido'
                    entrada['institucion'] = 'Desconocida'

        resultado.append(entrada)

    context = {
        'dispositivos': resultado,
        'busqueda': busqueda,
    }

    return render(request, 'Dispositivos-IoT/base-IoT.html', context)





def crear_dispositivo(request):
    if request.method == 'POST':
        mac_dispositivo = request.POST.get('mac_dispositivo')
        tipo_dispositivo = request.POST.get('tipo_dispositivo')

        print(tipo_dispositivo)
        if tipo_dispositivo == 'Dosímetro de Voz':
            tipo_dispositivo = '1'
        elif tipo_dispositivo == 'Registrador de Variables Ambientales':
            tipo_dispositivo = '2'
        else:
            messages.error(request, "Tipo de dispositivo no válido.")
            return redirect('iot')

        if not mac_dispositivo or not tipo_dispositivo:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('iot')

        try:
            dispositivo = Dispositivo_IoT.objects.create(
                mac_dispositivo=mac_dispositivo,
                tipo_dispositivo=tipo_dispositivo
            )
            messages.success(request, "Dispositivo IoT agregado correctamente.")
        except IntegrityError:
            messages.error(request, "Ya existe un dispositivo con esa MAC.")
        except Exception as e:
            messages.error(request, f"Error al agregar el dispositivo: {e}")

    return redirect('iot')  # Redirige a la lista de dispositivos después de agregar uno

def eliminar_dispositivo(request, mac):
    dispositivo = get_object_or_404(Dispositivo_IoT, mac_dispositivo=mac)
    if request.method == 'POST':
        dispositivo.delete()
        messages.success(request, 'Dispositivo eliminado exitosamente.')
        return redirect('iot')

    return render(request, 'confirmar_eliminacion.html', {'dispositivo': dispositivo})


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