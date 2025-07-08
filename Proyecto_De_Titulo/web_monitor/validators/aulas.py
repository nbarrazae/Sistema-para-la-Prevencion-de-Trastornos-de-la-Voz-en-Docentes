import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

def validate_nro_aula(value):
    """
    Valida el número de aula.
    Debe tener al menos 1 carácter, máximo 10 y solo contener letras, números y espacios.
    """
    if len(value) < 1:
        raise ValidationError(
            _('El número de aula debe tener al menos 1 carácter.'),
            params={'value': value},
        )
    if len(value) > 10:
        raise ValidationError(
            _('El número de aula debe tener como máximo 10 caracteres.'),
            params={'value': value},
        )
    if not re.match(r'^[a-zA-Z0-9\s]+$', value):
        raise ValidationError(
            _('El número de aula solo puede contener letras, números y espacios.'),
            params={'value': value},
        )
    
def validate_tamano(value):
    """
    Valida el tamaño del aula.
    Debe ser un número entero positivo.
    """
    if value is not None and (not isinstance(value, int) or value <= 0):
        raise ValidationError(
            _('El tamaño del aula debe ser un número entero positivo.'),
            params={'value': value},
        )

def validate_cantidad_alumnos(value):
    """
    Valida la cantidad de alumnos en el aula.
    Debe ser un número entero positivo.
    """
    if value is not None and (not isinstance(value, int) or value <= 0):
        raise ValidationError(
            _('La cantidad de alumnos debe ser un número entero positivo.'),
            params={'value': value},
        )

def validate_descripcion(value):
    """
    Valida la descripción del aula.
    Debe tener un máximo de 100 caracteres y solo contener letras, números, espacios y caracteres especiales.
    """
    if value is not None and len(value) > 100:
        raise ValidationError(
            _('La descripción del aula no puede exceder los 100 caracteres.'),
            params={'value': value},
        )
    if value is not None and not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-\(\)\.,:]+$', value):
        raise ValidationError(
            _('La descripción del aula solo puede contener letras, números, espacios y caracteres especiales.'),
            params={'value': value},
        )
    
def validate_aulas_data(nro_aula, tamano, cantidad_alumnos, descripcion):
    """
    Valida los datos de un aula.
    Lanza ValidationError si algún dato es inválido.
    """
    validate_nro_aula(nro_aula)
    validate_tamano(tamano)
    validate_cantidad_alumnos(cantidad_alumnos)
    validate_descripcion(descripcion)


def normalizar_nro_aula(nro_aula):
    """
    Normaliza el número de aula eliminando espacios extra y convirtiéndolo a mayúsculas.
    """
    return ' '.join(nro_aula.split()).upper()

def normalizar_descripcion(descripcion):
    """
    Normaliza la descripción del aula eliminando espacios extra y convirtiéndola a título.
    """
    return ' '.join(descripcion.split()).title() if descripcion else None



