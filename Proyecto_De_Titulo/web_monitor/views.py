from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .serializer import InstitucionSerializer, ProfesorSerializer, AulaSerializer, HorarioSerializer
from .models import Institucion, Profesor, Aula, Horario, Dispositivo_IoT, Relacion_Aula, Relacion_Profesor, Aula_CO2, Aula_Temperatura, Aula_Humedad, Aula_Ruido, Profesor_Voz

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
from web_monitor.validators.profesor import normalizar_correo, normalizar_nombre, capitalizar_texto, normalizar_rut, validate_rut, validate_email, validate_nombre, validate_apellido, validate_sexo, validate_area_docencia, validate_antecedentes_medicos, validate_altura, validate_peso
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from web_monitor.validators.instituciones import (
    validate_nombre,
    validate_rut,
    validate_direccion,
    validate_sitio_web,
    validate_representante_legal,
    validate_telefono,
    validate_email,
    normalizar_rut,
    normalizar_nombre,
    normalizar_direccion,
    normalizar_sitio_web,
    normalizar_representante_legal,
    normalizar_telefono,
    normalizar_email
)
from web_monitor.validators.aulas import (
    validate_nro_aula,
    validate_tamano,
    validate_cantidad_alumnos,
    validate_descripcion,
    normalizar_nro_aula,
    normalizar_descripcion
)



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
        try:
            # Normalizar entradas
            nombre_institucion_limpio = normalizar_nombre(request.POST.get("nombre_institucion"))
            rut_institucion_limpio = normalizar_rut(request.POST.get("rut_institucion"))
            direccion_limpio = normalizar_direccion(request.POST.get("direccion"))
            sitio_web_limpio = normalizar_sitio_web(request.POST.get("sitio_web"))
            representante_legal_limpio = normalizar_representante_legal(request.POST.get("representante_legal"))
            telefono_institucion_limpio = normalizar_telefono(request.POST.get("telefono_institucion"))
            correo_institucion_limpio = normalizar_email(request.POST.get("correo_institucion"))

            # Validaciones
            validate_nombre(nombre_institucion_limpio)
            validate_rut(rut_institucion_limpio)
            validate_direccion(direccion_limpio)
            validate_sitio_web(sitio_web_limpio)
            validate_representante_legal(representante_legal_limpio)
            validate_telefono(telefono_institucion_limpio)
            validate_email(correo_institucion_limpio)

            # Verificar unicidad
            errores = []
            if Institucion.objects.filter(nombre_institucion=nombre_institucion_limpio).exclude(pk=pk).exists():
                errores.append('Ya existe una institución con ese nombre.')
            if Institucion.objects.filter(rut_institucion=rut_institucion_limpio).exclude(pk=pk).exists():
                errores.append('Ya existe una institución con ese RUT.')
            if Institucion.objects.filter(correo_institucion=correo_institucion_limpio).exclude(pk=pk).exists():
                errores.append('Ya existe una institución con ese correo.')
            # Si hay errores, devolverlos todos juntos
            if errores:
                return JsonResponse({'error': errores}, status=400)
            
            # Actualizar la institución
            institucion.nombre_institucion = nombre_institucion_limpio
            institucion.rut_institucion = rut_institucion_limpio
            institucion.direccion = direccion_limpio
            institucion.sitio_web = sitio_web_limpio
            institucion.representante_legal = representante_legal_limpio
            institucion.telefono_institucion = telefono_institucion_limpio
            institucion.correo_institucion = correo_institucion_limpio

            institucion.save()
            return JsonResponse({'success': True}, status=200)
        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)
        except IntegrityError as e:
            return JsonResponse({'error': 'Error de integridad: Verifica los datos ingresados.'}, status=400)
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=400)

def crear_institucion(request):
    if request.method == "POST":
        try:
            print("Datos recibidos:", request.POST)  # Registro para depuración

            # Normalizar entradas
            nombre_institucion_limpio = normalizar_nombre(request.POST.get("nombre_institucion"))
            rut_institucion_limpio = normalizar_rut(request.POST.get("rut_institucion"))
            direccion_limpio = normalizar_direccion(request.POST.get("direccion"))
            sitio_web_limpio = normalizar_sitio_web(request.POST.get("sitio_web"))
            representante_legal_limpio = normalizar_representante_legal(request.POST.get("representante_legal"))
            telefono_institucion_limpio = normalizar_telefono(request.POST.get("telefono_institucion"))
            correo_institucion_limpio = normalizar_email(request.POST.get("correo_institucion"))

            # Validaciones
            validate_nombre(nombre_institucion_limpio)
            validate_rut(rut_institucion_limpio)
            validate_direccion(direccion_limpio)
            validate_sitio_web(sitio_web_limpio)
            validate_representante_legal(representante_legal_limpio)
            validate_telefono(telefono_institucion_limpio)
            validate_email(correo_institucion_limpio)

            # Verificar unicidad
            errores = []
            if Institucion.objects.filter(nombre_institucion=nombre_institucion_limpio).exists():
                errores.append('Ya existe una institución con ese nombre.')
            if Institucion.objects.filter(rut_institucion=rut_institucion_limpio).exists():
                errores.append('Ya existe una institución con ese RUT.')
            if Institucion.objects.filter(correo_institucion=correo_institucion_limpio).exists():
                errores.append('Ya existe una institución con ese correo.')

            # Si hay errores, devolverlos todos juntos
            if errores:
                return JsonResponse({'error': errores}, status=400)

            # Crear la institución
            institucion = Institucion(
                nombre_institucion=nombre_institucion_limpio,
                rut_institucion=rut_institucion_limpio,
                direccion=direccion_limpio,
                sitio_web=sitio_web_limpio,
                representante_legal=representante_legal_limpio,
                telefono_institucion=telefono_institucion_limpio,
                correo_institucion=correo_institucion_limpio
            )
            institucion.save()
            # messages.success(request, "Institución creada correctamente.")
            return JsonResponse({'success': True}, status=200)
        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)
        except IntegrityError as e:
            return JsonResponse({'error': 'Error de integridad: Verifica los datos ingresados.'}, status=400)
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=400)
            

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
        try:
            print("📥 Recibido POST JSON")

            data = json.loads(request.body)
            print("Contenido del JSON:", data)  # 👈 Aquí ves qué se está enviando

            # Normalizar entradas
            nro_aula_limpio = normalizar_nro_aula(data.get("nro_aula"))
            descripcion_limpio = normalizar_descripcion(data.get("descripcion"))

            # Validaciones
            validate_nro_aula(nro_aula_limpio)
            validate_tamano(data.get("tamanio"))
            validate_cantidad_alumnos(data.get("cantidad_alumnos"))
            validate_descripcion(descripcion_limpio)

            # Verificar unicidad
            errores = []
            if Aula.objects.filter(nro_aula=nro_aula_limpio, id_institucion_id=pk).exists():
                errores.append('Ya existe un aula con ese número en esta institución.')

            # Si hay errores, devolverlos todos juntos
            if errores:
                return JsonResponse({'error': errores}, status=400)

            # Crear el aula
            aula = Aula(
                nro_aula=nro_aula_limpio,
                tamaño=data.get("tamanio"),
                cantidad_alumnos=data.get("cantidad_alumnos"),
                descripcion=descripcion_limpio,
                id_institucion_id=pk  # 👈 Ya viene en la URL
            )
            aula.save()

            return JsonResponse({"success": True}, status=200)
        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)
        except IntegrityError as e:
            return JsonResponse({'error': 'Error de integridad: Verifica los datos ingresados.'}, status=400)
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=400)
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

def eliminar_aula(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    if request.method == 'POST':
        aula.delete()
        return redirect('instituciones')  # Nombre de tu vista principal

    return render(request, 'confirmar_eliminacion.html', {'aula': aula})
    

def modificar_aula(request, pk):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Normalizar entradas
            nro_aula_limpio = normalizar_nro_aula(data.get("nro_aula"))
            descripcion_limpio = normalizar_descripcion(data.get("descripcion"))

            # Validaciones
            validate_nro_aula(nro_aula_limpio)
            validate_tamano(data.get("tamanio"))
            validate_cantidad_alumnos(data.get("cantidad_alumnos"))
            validate_descripcion(descripcion_limpio)

            # Verificar unicidad
            errores = []
            if Aula.objects.filter(nro_aula=nro_aula_limpio).exclude(pk=pk).exists():
                errores.append('Ya existe un aula con ese número en esta institución.')

            # Si hay errores, devolverlos todos juntos
            if errores:
                return JsonResponse({'error': errores}, status=400)

            # Actualizar el aula
            aula = Aula.objects.get(pk=pk)
            aula.nro_aula = nro_aula_limpio
            aula.tamaño = data.get("tamanio", aula.tamaño)
            aula.cantidad_alumnos = data.get("cantidad_alumnos", aula.cantidad_alumnos)
            aula.descripcion = descripcion_limpio
            aula.save()

            return JsonResponse({"success": True}, status=200)
        except Aula.DoesNotExist:
            return JsonResponse({"success": False, "error": "Aula no encontrada"}, status=404)
        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)
        except IntegrityError as e:
            return JsonResponse({'error': 'Error de integridad: Verifica los datos ingresados.'}, status=400)
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=400)
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)


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
            print("Datos recibidos:", request.POST)  # Agrega este registro para depurar
            # Normalizar entradas
            rut_profe_limpio = normalizar_rut(request.POST['rut_profesor'])
            nombre_profe_limpio = normalizar_nombre(request.POST['nombre_profesor'])
            apellido_profe_limpio = normalizar_nombre(request.POST['apellido_profesor'])
            correo_profe_limpio = normalizar_correo(request.POST['correo_profesor'])
            antecedentes_medicos_limpio = capitalizar_texto(request.POST.get('antecedentes_medicos', ''))
            area_docencia_limpio = capitalizar_texto(request.POST['area_docencia'])
            
            # Validaciones
            validate_rut(rut_profe_limpio)
            validate_email(correo_profe_limpio)
            validate_nombre(nombre_profe_limpio)
            validate_apellido(apellido_profe_limpio)
            validate_sexo(request.POST['sexo'])
            validate_altura(request.POST.get('altura', ''))
            validate_peso(request.POST.get('peso', ''))
            validate_area_docencia(area_docencia_limpio)
            validate_antecedentes_medicos(antecedentes_medicos_limpio)

            # Obtener la institución
            institucion = Institucion.objects.get(id_institucion=request.POST['id_institucion'])

            # Verificar unicidad
            errores = []
            if Profesor.objects.filter(rut_profesor=rut_profe_limpio).exists():
                errores.append('Ya existe un profesor con ese RUT.')
            if Profesor.objects.filter(correo_profesor=correo_profe_limpio).exists():
                errores.append('Ya existe un profesor con ese correo.')
            
            # Si hay errores, devolverlos todos juntos
            if errores:
                return JsonResponse({'error': errores}, status=400)
            
            # Crear el profesor
            Profesor.objects.create(
                rut_profesor=rut_profe_limpio,
                nombre_profesor=nombre_profe_limpio,
                apellido_profesor=apellido_profe_limpio,
                correo_profesor=correo_profe_limpio,
                sexo=request.POST['sexo'],
                altura=request.POST.get('altura') or None,
                peso=request.POST.get('peso') or None,
                antecedentes_medicos=antecedentes_medicos_limpio,
                area_docencia=area_docencia_limpio,
                id_institucion=institucion
            )
            return JsonResponse({'success': True}, status=200)
        except Institucion.DoesNotExist:
            return JsonResponse({'error': 'La institución seleccionada no existe.'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': ', '.join(e.messages)}, status=400)
        except IntegrityError as e:
            return JsonResponse({'error': 'Error de integridad: Verifica los datos ingresados.'}, status=400)
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=400)

def editar_profesor(request, pk):
    if request.method == 'POST':
        try:
            print("Datos recibidos:", request.POST)  # Agrega este registro para depurar
            profesor = get_object_or_404(Profesor, pk=pk)

            # Normalizar entradas
            rut_profe_limpio = normalizar_rut(request.POST['rut_profesor'])
            nombre_profe_limpio = normalizar_nombre(request.POST['nombre_profesor'])
            apellido_profe_limpio = normalizar_nombre(request.POST['apellido_profesor'])
            correo_profe_limpio = normalizar_correo(request.POST['correo_profesor'])
            antecedentes_medicos_limpio = capitalizar_texto(request.POST.get('antecedentes_medicos', ''))
            area_docencia_limpio = capitalizar_texto(request.POST['area_docencia'])
            # Validaciones
            validate_rut(rut_profe_limpio)
            validate_email(correo_profe_limpio)
            validate_nombre(nombre_profe_limpio)
            validate_apellido(apellido_profe_limpio)
            validate_sexo(request.POST['sexo'])
            validate_altura(request.POST.get('altura', ''))
            validate_peso(request.POST.get('peso', ''))
            validate_area_docencia(area_docencia_limpio)
            validate_antecedentes_medicos(antecedentes_medicos_limpio)

            # Obtener la institución
            institucion = Institucion.objects.get(id_institucion=request.POST['id_institucion'])

            # Verificar unicidad
            errores = []
            if Profesor.objects.filter(rut_profesor=rut_profe_limpio).exclude(pk=pk).exists():
                errores.append('Ya existe un profesor con ese RUT.')
            if Profesor.objects.filter(correo_profesor=correo_profe_limpio).exclude(pk=pk).exists():
                errores.append('Ya existe un profesor con ese correo.')
            # Si hay errores, devolverlos todos juntos
            if errores:
                return JsonResponse({'error': errores}, status=400)
            
            # Actualizar el profesor
            profesor.rut_profesor = rut_profe_limpio
            profesor.nombre_profesor = nombre_profe_limpio
            profesor.apellido_profesor = apellido_profe_limpio
            profesor.correo_profesor = correo_profe_limpio
            profesor.sexo = request.POST['sexo']
            profesor.altura = request.POST.get('altura') or None
            profesor.peso = request.POST.get('peso') or None
            profesor.antecedentes_medicos = antecedentes_medicos_limpio
            profesor.area_docencia = area_docencia_limpio
            profesor.id_institucion = institucion

            profesor.save()
            return JsonResponse({'success': True}, status=200)
        except Institucion.DoesNotExist:
            return JsonResponse({'error': 'La institución seleccionada no existe.'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': ', '.join(e.messages)}, status=400)
        except IntegrityError as e:
            return JsonResponse({'error': 'Error de integridad: Verifica los datos ingresados.'}, status=400)
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=400)


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
            'hora_inicio': str(hora_inicio),
            'hora_termino': str(hora_termino),
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

        # Verificar si está asociado a un aula
        try:
            rel_aula = Relacion_Aula.objects.get(id_dispositivo=dispositivo)
            aula = rel_aula.id_aula
            entrada['estado'] = 'Asignado'
            entrada['usuario'] = f"Aula {aula.nro_aula}"
            entrada['institucion'] = aula.id_institucion.nombre_institucion
        except Relacion_Aula.DoesNotExist:
            try:
                # Si no está asociado a aula, buscar si está a un profesor
                rel_profesor = Relacion_Profesor.objects.get(id_dispositivo=dispositivo)
                profesor = rel_profesor.id_profesor
                entrada['estado'] = 'Asignado'
                entrada['usuario'] = f"{profesor.nombre_profesor} {profesor.apellido_profesor}"
                entrada['institucion'] = profesor.id_institucion.nombre_institucion
            except Relacion_Profesor.DoesNotExist:
                # Caso no asignado
                entrada['estado'] = 'Libre'
                entrada['usuario'] = None
                entrada['institucion'] = None

        resultado.append(entrada)

    instituciones = Institucion.objects.all()
    context = {
        'dispositivos': resultado,
        'busqueda': busqueda,
        'instituciones': instituciones,
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

def obtener_opciones(request, institucion_id, tipo):
    if tipo == 'aula':
        aulas = Aula.objects.filter(id_institucion=institucion_id)
        data = [{'id': a.id_aula, 'nombre': a.nro_aula} for a in aulas]
    elif tipo == 'profesor':
        profesores = Profesor.objects.filter(id_institucion=institucion_id)
        data = [{'id': p.id_profesor, 'nombre': f"{p.nombre_profesor} {p.apellido_profesor}"} for p in profesores]
    else:
        data = []
    return JsonResponse(data, safe=False)


def vista_dispositivos(request):
    instituciones = Institucion.objects.all()
    return render(request, 'tabla-iot.html', {'instituciones': instituciones})

def asignar_dispositivo(request):
    if request.method == 'POST':
        mac = request.POST.get('mac')
        institucion_id = request.POST.get('institucion')
        destino_id = request.POST.get('destino')
        tipo_destino = request.POST.get('tipo_destino')

        try:
            dispositivo = Dispositivo_IoT.objects.get(mac_dispositivo=mac)

            # Verificar si el dispositivo ya está asignado
            relacion_aula = Relacion_Aula.objects.filter(id_dispositivo=dispositivo)
            relacion_profesor = Relacion_Profesor.objects.filter(id_dispositivo=dispositivo)

            mensaje_cambio = None

            if relacion_aula.exists():
                relacion_aula_obj = relacion_aula.first()
                if relacion_aula_obj and relacion_aula_obj.id_aula:
                    aula = relacion_aula_obj.id_aula.nro_aula
                    relacion_aula.delete()
                    aula_obj = Aula.objects.get(nro_aula=aula, id_institucion=relacion_aula_obj.id_aula.id_institucion)
                    nueva_aula = Aula.objects.get(id_aula=destino_id)
                    mensaje_cambio = f"Se ha cambiado la relación de Aula {aula_obj.nro_aula} de la institución {aula_obj.id_institucion.nombre_institucion} a Aula {nueva_aula.nro_aula} de la institución {nueva_aula.id_institucion.nombre_institucion}."
            elif relacion_profesor.exists():
                profesor = relacion_profesor.first().id_profesor
                relacion_profesor.delete()
                mensaje_cambio = f"Se ha cambiado la relación de Profesor {profesor.nombre_profesor} {profesor.apellido_profesor} a Profesor {Profesor.objects.get(id_profesor=destino_id).nombre_profesor} {Profesor.objects.get(id_profesor=destino_id).apellido_profesor}."

            if mensaje_cambio:
                messages.info(request, mensaje_cambio)

            if tipo_destino == 'aula':
                aula = Aula.objects.get(id_aula=destino_id, id_institucion_id=institucion_id)
                Relacion_Aula.objects.create(id_aula=aula, id_dispositivo=dispositivo, mac=mac)
            elif tipo_destino == 'profesor':
                profesor = Profesor.objects.get(id_profesor=destino_id, id_institucion_id=institucion_id)
                Relacion_Profesor.objects.create(id_profesor=profesor, id_dispositivo=dispositivo, mac=mac)
            else:
                messages.error(request, "Tipo de destino no válido.")
                return redirect('iot')

            messages.success(request, "Dispositivo asignado correctamente.")
        except Dispositivo_IoT.DoesNotExist:
            messages.error(request, "Dispositivo no encontrado.")
        except Aula.DoesNotExist:
            messages.error(request, "Aula no encontrada.")
        except Profesor.DoesNotExist:
            messages.error(request, "Profesor no encontrado.")
        except IntegrityError:
            messages.error(request, "El dispositivo ya está asignado.")
        except Exception as e:
            messages.error(request, f"Error inesperado: {e}")

    return redirect('iot')  # Redirige a la lista de dispositivos después de intentar asignar uno

def obtener_instituciones(request):
    instituciones = Institucion.objects.all().values('id', 'nombre_institucion')
    return JsonResponse(list(instituciones), safe=False)

def profesores_por_institucion(request, id_institucion):
    profesores = Profesor.objects.filter(id_institucion_id=id_institucion).values(
        'id_profesor', 'nombre_profesor', 'apellido_profesor'
    )
    return JsonResponse(list(profesores), safe=False)

def aulas_por_institucion(request, id_institucion):
    aulas = Aula.objects.filter(id_institucion_id=id_institucion).values(
        'id_aula', 'nro_aula'
    )
    return JsonResponse(list(aulas), safe=False)


def usuarios(request):
    return render(request, 'usuarios.html')


from django.shortcuts import render
from .models import Institucion

def estadisticas(request):
    instituciones = Institucion.objects.all()

    if request.method == 'POST':
        id_institucion = int(request.POST.get('institucion'))
        id_profesor_raw = request.POST.get('profesor')
        id_profesor = int(id_profesor_raw) if id_profesor_raw else None

        fecha_inicio_raw = request.POST.get('fecha_inicio')
        fecha_fin_raw = request.POST.get('fecha_fin')
        print(f"Fecha Inicio: {fecha_inicio_raw}, Fecha Fin: {fecha_fin_raw}, Institución: {id_institucion}, Profesor: {id_profesor}")

        if fecha_inicio_raw and fecha_fin_raw:
            fecha_inicio_str, hora_inicio_str = fecha_inicio_raw.split('T')
            fecha_fin_str, hora_fin_str = fecha_fin_raw.split('T')

            fechas, detalles, dt_inicio, dt_fin = generar_rango_fechas_con_dia(fecha_inicio_str, hora_inicio_str, fecha_fin_str, hora_fin_str)
            horarios = buscar_horarios(detalles, id_institucion, dt_inicio, dt_fin, id_profesor)

            resultados = []

            contador = 0  # Inicializar contador
            for horario in horarios:
                print(f"\nAula: {horario['id_aula']}, Fecha: {horario['fecha']}, Hora Inicio: {horario['hora_inicio']}")
                
                for medicion in horario['registros_ruido']:
                    contador += 1
                    print(f"  Ruido {contador}. {medicion['fecha_hora']}: {medicion['ruido']} dB")
                
                for medicion in horario['registros_humedad']:
                    print(f"  Humedad: {medicion['fecha_hora']}: {medicion['humedad']}%")
                
                for medicion in horario['registros_temperatura']:
                    print(f"  Temperatura: {medicion['fecha_hora']}: {medicion['temperatura']}°C")
                
                for medicion in horario['registros_co2']:
                    print(f"  CO2: {medicion['fecha_hora']}: {medicion['co2']} ppm")
                
                for medicion in horario['registros_voz']:
                    print(f"  Voz: {medicion['fecha_hora']}: Frecuencia {medicion['freq']} Hz, Intensidad {medicion['intensidad']} dB")

    return render(request, 'Estadisticas/base-estadisticas.html', {'instituciones': instituciones})



from collections import defaultdict

def asignar_fechas_a_horarios(horarios, detalles_por_dia):
    # Agrupar fechas por día de semana
    fechas_por_dia = defaultdict(list)
    for detalle in detalles_por_dia:
        fechas_por_dia[detalle['dia_semana']].append(detalle['fecha'])

    horarios_con_fecha = []

    for horario in horarios:
        dia = horario['dia']
        fechas = fechas_por_dia.get(dia, [])

        for fecha in fechas:
            horario_con_fecha = horario.copy()
            horario_con_fecha['fecha'] = fecha
            horarios_con_fecha.append(horario_con_fecha)

    return horarios_con_fecha





from datetime import datetime, timedelta

dias_semana = {
    0: 'Lunes',
    1: 'Martes',
    2: 'Miércoles',
    3: 'Jueves',
    4: 'Viernes',
    5: 'Sábado',
    6: 'Domingo'
}

def generar_rango_fechas_con_dia(fecha_inicio_str, hora_inicio_str, fecha_fin_str, hora_fin_str):
    inicio = datetime.strptime(f"{fecha_inicio_str} {hora_inicio_str}", "%Y-%m-%d %H:%M")
    fin = datetime.strptime(f"{fecha_fin_str} {hora_fin_str}", "%Y-%m-%d %H:%M")

    detalles = []
    fecha_actual = inicio.date()

    while fecha_actual <= fin.date():
        if fecha_actual == inicio.date() and fecha_actual == fin.date():
            hora_ini, hora_fin = inicio.time(), fin.time()
        elif fecha_actual == inicio.date():
            hora_ini, hora_fin = inicio.time(), datetime.strptime("23:59", "%H:%M").time()
        elif fecha_actual == fin.date():
            hora_ini, hora_fin = datetime.strptime("00:00", "%H:%M").time(), fin.time()
        else:
            hora_ini = datetime.strptime("00:00", "%H:%M").time()
            hora_fin = datetime.strptime("23:59", "%H:%M").time()

        detalles.append({
            "fecha": fecha_actual.strftime("%Y-%m-%d"),
            "hora_inicio": hora_ini.strftime("%H:%M"),
            "hora_fin": hora_fin.strftime("%H:%M"),
            "dia_semana": dias_semana[fecha_actual.weekday()]
        })

        fecha_actual += timedelta(days=1)

    return [d["fecha"] for d in detalles], detalles, inicio, fin




def buscar_horarios(detalles_por_dia, id_institucion, dt_inicio, dt_fin, id_profesor=None):
    resultados = []

    for detalle in detalles_por_dia:
        dia = detalle['dia_semana']
        fecha = detalle['fecha']
        hora_inicio = datetime.strptime(detalle['hora_inicio'], "%H:%M").time()
        hora_fin = datetime.strptime(detalle['hora_fin'], "%H:%M").time()

        filtros = {
            'dia': dia,
            'hora_inicio__gte': hora_inicio,
            'hora_termino__lte': hora_fin,
            'id_aula__id_institucion': id_institucion
        }

        if id_profesor:
            filtros['id_profesor_id'] = id_profesor

        horarios = Horario.objects.filter(**filtros).select_related('id_profesor', 'id_aula')
        for horario in horarios:
            dt_hora_inicio = datetime.strptime(f"{fecha} {horario.hora_inicio.strftime('%H:%M')}", "%Y-%m-%d %H:%M")
            dt_hora_termino = datetime.strptime(f"{fecha} {horario.hora_termino.strftime('%H:%M')}", "%Y-%m-%d %H:%M")



            if dt_hora_inicio >= dt_inicio and dt_hora_termino <= dt_fin:
                # 🔹 Obtener registros de ruido
                registros_ruido = Aula_Ruido.objects.filter(
                    id_aula=horario.id_aula,
                    fecha_hora__range=(dt_hora_inicio, dt_hora_termino)
                ).order_by('fecha_hora')

                lista_ruido = [
                    {
                        'fecha_hora': registro.fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
                        'ruido': registro.ruido
                    }
                    for registro in registros_ruido
                ]

                # 🔹 Obtener registros de humedad
                registros_humedad = Aula_Humedad.objects.filter(
                    id_aula=horario.id_aula,
                    fecha_hora__range=(dt_hora_inicio, dt_hora_termino)
                ).order_by('fecha_hora')

                lista_humedad = [
                    {
                        'fecha_hora': registro.fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
                        'humedad': registro.humedad
                    }
                    for registro in registros_humedad
                ]

                # 🔹 Obtener registros de temperatura
                registros_temperatura = Aula_Temperatura.objects.filter(
                    id_aula=horario.id_aula,
                    fecha_hora__range=(dt_hora_inicio, dt_hora_termino)
                ).order_by('fecha_hora')

                lista_temperatura = [
                    {
                        'fecha_hora': registro.fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
                        'temperatura': registro.temperatura
                    }
                    for registro in registros_temperatura
                ]

                # 🔹 Obtener registros de CO2
                registros_co2 = Aula_CO2.objects.filter(
                    id_aula=horario.id_aula,
                    fecha_hora__range=(dt_hora_inicio, dt_hora_termino)
                ).order_by('fecha_hora')

                lista_co2 = [
                    {
                        'fecha_hora': registro.fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
                        'co2': registro.co2
                    }
                    for registro in registros_co2
                ]

                # 🔹 Obtener registros de intensidad de voz
                registros_voz = Profesor_Voz.objects.filter(
                    id_profesor=horario.id_profesor,
                    fecha_hora__range=(dt_hora_inicio, dt_hora_termino)
                ).order_by('fecha_hora')

                lista_voz = [
                    {
                        'fecha_hora': registro.fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
                        'freq': registro.Freq,
                        'intensidad': registro.Intensidad
                    }
                    for registro in registros_voz
                ]

                resultados.append({
                    "id_aula": horario.id_aula.id_aula,
                    "hora_inicio": horario.hora_inicio.strftime("%H:%M"),
                    "hora_termino": horario.hora_termino.strftime("%H:%M"),
                    "profesor": horario.id_profesor.nombre_profesor,
                    "dia": horario.dia,
                    "fecha": fecha,
                    "registros_ruido": lista_ruido,
                    "registros_humedad": lista_humedad,
                    "registros_temperatura": lista_temperatura,
                    "registros_co2": lista_co2,
                    "registros_voz": lista_voz
                })

    return resultados


























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