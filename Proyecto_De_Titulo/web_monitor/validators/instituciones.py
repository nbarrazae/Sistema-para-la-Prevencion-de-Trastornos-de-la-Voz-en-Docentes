import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

def validate_nombre(value):
    """
    Valida el campo de nombre.
    Debe tener al menos 2 caracteres, maximo 100 y solo contener letras, numeros, espacios y caracteres especiales.
    Permite nombres con espacios y acentos.
    Ejemplo: 'Juan Pérez', 'María del Carmen'.
    """
    if len(value) < 2 or len(value) > 100 or not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-\(\)\.,:\'"]+$', value):
        raise ValidationError(
            _('El nombre debe tener al menos 2 caracteres, máximo 100 y solo contener letras, números, espacios y caracteres especiales.'),
            params={'value': value},
        )

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
    
def validate_direccion(value):
    """
    Valida el campo de dirección.
    Debe tener al menos 5 caracteres, maximo 100 y solo contener letras, números, espacios y caracteres especiales.
    Permite direcciones con espacios y acentos.
    Ejemplo: 'Avenida Libertador Bernardo O'Higgins 1234'.
    """
    if len(value) < 5 or len(value) > 100 or not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-\(\)\.,:]+$', value):
        raise ValidationError(
            _('La dirección debe tener al menos 5 caracteres, máximo 100 y solo contener letras, números, espacios y caracteres especiales.'),
            params={'value': value},
        )

def validate_sitio_web(value):
    """
    Valida el campo de sitio web.
    Debe tener un formato válido de URL.
    Ejemplo: 'http://www.ejemplo.cl' , 'https://ejemplo.com' , www.STomas.cl , STomas.cl
    """
    url_pattern = r'^(https?://)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/.*)?$'
    if not re.match(url_pattern, value):
        raise ValidationError(
            _('El sitio web debe tener un formato válido.'),
            params={'value': value},
        )
    
def validate_representante_legal(value):
    """
    Valida el campo de representante legal.
    Debe tener al menos 2 caracteres maximo 100 y solo contener letras, espacios y caracteres especiales.
    Permite nombres con espacios y acentos.
    Ejemplo: 'Juan Pérez', 'María del Carmen'.
    """
    if len(value) < 2 or len(value) > 100 or not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-\(\)\.,:\'"]+$', value):
        raise ValidationError(
            _('El representante legal debe tener al menos 2 caracteres, máximo 100 y solo contener letras, números, espacios y caracteres especiales.'),
            params={'value': value},
        )


def validate_telefono(value):
    """
    Valida el campo de teléfono.
    Debe tener un formato válido de número de teléfono chileno.
    Ejemplo: '123456789' o '+56 9 1234 5678'.
    """
    phone_pattern = r'^\+?56\s?9\s?\d{4}\s?\d{4}$|^\d{8,12}$'
    if not re.match(phone_pattern, value):
        raise ValidationError(
            _('El teléfono debe tener un formato válido.'),
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

def validate_institucion_data(nombre_institucion, rut_institucion, direccion, sitio_web, representante_legal, telefono_institucion, correo_institucion):
    """
    Valida los datos de una institución.
    Lanza ValidationError si algún dato es inválido.
    """
    validate_nombre(nombre_institucion)
    validate_rut(rut_institucion)
    validate_direccion(direccion)
    if sitio_web:
        validate_sitio_web(sitio_web)
    validate_representante_legal(representante_legal)
    validate_telefono(telefono_institucion)
    validate_email(correo_institucion)


# Funciones para normalizar los datos de la institución
def normalizar_rut(rut):
    """
    Elimina los puntos y convierte el dígito verificador a mayúscula.
    Deja el RUT en formato XXXXXXXX-X.
    """
    rut = rut.replace(".", "").upper()
    return rut

def normalizar_nombre(nombre):
    """
    Normaliza el nombre eliminando espacios extra y convirtiendo a título.
    """
    return ' '.join(nombre.split()).title()

def normalizar_direccion(direccion):
    """
    Normaliza la dirección eliminando espacios extra y convirtiendo a título.
    """
    return ' '.join(direccion.split()).title()

def normalizar_sitio_web(sitio_web):
    """
    Normaliza el sitio web asegurando que comience con 'http://' o 'https://'.
    """
    if not sitio_web.startswith(('http://', 'https://')):
        sitio_web = 'http://' + sitio_web
    return sitio_web.lower()

def normalizar_representante_legal(representante_legal):
    """
    Normaliza el nombre del representante legal eliminando espacios extra y convirtiendo a título.
    """
    return ' '.join(representante_legal.split()).title()

def normalizar_telefono(telefono):
    """
    Normaliza el número de teléfono eliminando espacios y guiones.
    """
    return re.sub(r'\D', '', telefono)  # Elimina todo lo que no sea dígito

def normalizar_email(email):
    """
    Normaliza el correo electrónico convirtiéndolo a minúsculas.
    """
    return email.lower().strip()

