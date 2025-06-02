
# funcion crear en view como guia
# def crear_profesor(request):
#     if request.method == 'POST':
#         try:
#             institucion = Institucion.objects.get(id_institucion=request.POST['id_institucion'])

#             profesor = Profesor.objects.create(
#                 rut_profesor=request.POST['rut_profesor'],
#                 nombre_profesor=request.POST['nombre_profesor'],
#                 apellido_profesor=request.POST['apellido_profesor'],
#                 correo_profesor=request.POST['correo_profesor'],
#                 sexo=request.POST['sexo'],
#                 altura=request.POST.get('altura') or None,
#                 peso=request.POST.get('peso') or None,
#                 antecedentes_medicos=request.POST.get('antecedentes_medicos') or '',
#                 area_docencia=request.POST['area_docencia'],
#                 id_institucion=institucion
#             )
#             messages.success(request, "Profesor creado correctamente.")
#         except Institucion.DoesNotExist:
#             messages.error(request, "La institución seleccionada no existe.")
#         except Exception as e:
#             messages.error(request, f"Error al crear el profesor: {e}")
        
#     return redirect('profesores')  # Redirige a la lista de profesores después de crear uno

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
def validate_rut(value):
    """
    Valida el RUT chileno.
    El RUT debe tener el formato 'XX.XXX.XXX-X' o 'XXXXXXXX-X'.
    """
    rut_pattern = r'^\d{1,2}\.\d{3}\.\d{3}-[0-9Kk]$|^\d{7,8}-[0-9Kk]$'
    if not re.match(rut_pattern, value):
        raise ValidationError(
            _('El RUT debe tener el formato XX.XXX.XXX-X o XXXXXXXX-X.'),
            params={'value': value},
        )
def validate_email(value):
    """
    Valida el formato del correo electrónico.
    El correo debe tener un formato válido.
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, value):
        raise ValidationError(
            _('El correo electrónico debe tener un formato válido.'),
            params={'value': value},
        )
    
def validate_nombre(value):
    """
    Valida el campo de nombre.
    Debe tener al menos 2 caracteres y solo contener letras y espacios.
    Permite nombres con espacios y acentos.
    Ejemplo: 'Juan Pérez', 'María del Carmen'.
    """
    if len(value) < 2 or not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
        raise ValidationError(
            _('El nombre debe tener al menos 2 caracteres y solo contener letras y espacios.'),
            params={'value': value},
        )
def validate_apellido(value):
    """
    Valida el campo de apellido.
    Debe tener al menos 2 caracteres y solo contener letras y espacios.
    Permite apellidos con espacios y acentos.
    Ejemplo: 'Pérez González', 'Del Río'.
    """
    if len(value) < 2 or not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
        raise ValidationError(
            _('El apellido debe tener al menos 2 caracteres y solo contener letras y espacios.'),
            params={'value': value},
        )
    
def validate_sexo(value):
    """
    Valida el campo de sexo.
    Debe ser 'M' o 'F'.
    """
    if value not in ['M', 'F']:
        raise ValidationError(
            _('El sexo debe ser "M" para Masculino o "F" para Femenino.'),
            params={'value': value},
        )
    
# Validar altura, que sea numero entre 50 y 250 cm y numeros de 1 a 3 digitos
def validate_altura(value):
    """
    Valida el campo de altura.
    Debe ser un número entre 50 y 250 cm.
    """
    try:
        altura = float(value)
        if not (50 <= altura <= 250):
            raise ValidationError(
                _('La altura debe estar entre 50 y 250 cm.'),
                params={'value': value},
            )
    except ValueError:
        raise ValidationError(
            _('La altura debe ser un número válido.'),
            params={'value': value},
        )
    
# numero de 1 a 3 digitos y debe ser un numero entre 20 y 300 kg
def validate_peso(value):
    """
    Valida el campo de peso.
    Debe ser un número entre 20 y 300 kg.
    """
    try:
        peso = float(value)
        if not (20 <= peso <= 300):
            raise ValidationError(
                _('El peso debe estar entre 20 y 300 kg.'),
                params={'value': value},
            )
    except ValueError:
        raise ValidationError(
            _('El peso debe ser un número válido.'),
            params={'value': value},
        )
    
# Validar área de docencia, que sea un string con al menos 3 caracteres
def validate_area_docencia(value):
    """
    Valida el campo de área de docencia.
    Debe tener al menos 3 caracteres.
    """
    if len(value) < 3:
        raise ValidationError(
            _('El área de docencia debe tener al menos 3 caracteres.'),
            params={'value': value},
        )
    
def validate_antecedentes_medicos(value):
    """
    Valida el campo de antecedentes médicos.
    Debe tener un máximo de 100 caracteres.
    """
    if len(value) > 100:
        raise ValidationError(
            _('Los antecedentes médicos no pueden exceder los 100 caracteres.'),
            params={'value': value},
        )
def validate_profesor_data(rut, email, sexo, area_docencia, antecedentes_medicos):
    """
    Valida los datos del profesor.
    Llama a las funciones de validación individuales.
    """
    validate_rut(rut)
    validate_email(email)
    validate_sexo(sexo)
    validate_area_docencia(area_docencia)
    validate_antecedentes_medicos(antecedentes_medicos)
    
    # Si todas las validaciones pasan, no se lanza ninguna excepción
    return True


# Funciones para nomralizar
def normalizar_rut(rut):
    """
    Elimina los puntos y convierte el dígito verificador a mayúscula.
    Deja el RUT en formato XXXXXXXX-X.
    """
    rut = rut.replace(".", "").upper()
    return rut

def normalizar_nombre(nombre):
    """
    Convierte el nombre en formato capitalizado:
    'juan PÉREZ gonzalez' -> 'Juan Pérez Gonzalez'
    """
    nombre = ' '.join(nombre.strip().split())  # Elimina espacios extra
    return nombre.title()

def normalizar_correo(correo):
    """
    Convierte el correo a minúsculas.
    """
    return correo.lower()


