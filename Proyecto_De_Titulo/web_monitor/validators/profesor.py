
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
    Debe tener al menos 2 caracteres y solo contener letras.
    """
    if len(value) < 2 or not value.isalpha():
        raise ValidationError(
            _('El nombre debe tener al menos 2 caracteres y solo contener letras.'),
            params={'value': value},
        )
def validate_apellido(value):
    """
    Valida el campo de apellido.
    Debe tener al menos 2 caracteres y solo contener letras.
    """
    if len(value) < 2 or not value.isalpha():
        raise ValidationError(
            _('El apellido debe tener al menos 2 caracteres y solo contener letras.'),
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
