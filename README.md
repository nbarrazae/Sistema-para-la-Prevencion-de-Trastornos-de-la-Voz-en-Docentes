# Proyecto de Título

## Cómo Usar

### Instituciones

- **GET**: `http://127.0.0.1:8000/api/instituciones/`
- **GET**: `http://127.0.0.1:8000/api/instituciones/609110066`  <----rut
- **POST**: `http://127.0.0.1:8000/api/instituciones/`
    ```json
    {
        "rut_institucion": "715515008",
        "nombre_institucion": "Universidad Santo Tomás",
        "direccion": "Av. Collao 1202, Concepción",
        "sitio_web": "https://santotomas.cl",
        "representante_legal": "EDUARDO JAVIER ITURRATE UGALDE",
        "telefono_institucion": "+56912345678",
        "correo_institucion": "contacto@STomas.cl"
    }
    ```
- **PUT**: `http://127.0.0.1:8000/api/instituciones/715515008/`  <----rut
    ```json
    { 
        "rut_institucion": "715515008",
        "nombre_institucion": "Universidad Santo Tomás",
        "direccion": "Av. Collao 1202, Concepción",
        "sitio_web": "https://santotomas.cl",
        "representante_legal": "EDUARDO JAVIER ITURRATE UGALDE",
        "telefono_institucion": "+56912345678",
        "correo_institucion": "contacto@tomas.cl"
    }
    ```
- **DELETE**: `http://127.0.0.1:8000/api/instituciones/715515008/`  <----rut

---

### Profesores

- **GET**: `http://127.0.0.1:8000/api/profesores/`
- **GET**: `http://127.0.0.1:8000/api/profesores/202752578`
- **POST**: `http://127.0.0.1:8000/api/profesores/`
    ```json
    {
        "rut_profesor": "114776017",
        "nombre_profesor": "Luis",
        "apellido_profesor": "Vera Quiroga",
        "correo_profesor": "lvera@ubiobio.cl",
        "sexo": "M",
        "altura": 173.0,
        "peso": 70.0,
        "antecedentes_medicos": "Ninguno :p",
        "area_docencia": "ELECTRONICA",
        "id_institucion": "Universidad del Bío-Bío"
    }
    ```
- **PUT**: `http://127.0.0.1:8000/api/profesores/114776017/`
    ```json
    {
        "rut_profesor": "114776017",
        "nombre_profesor": "Luis",
        "apellido_profesor": "Vera Quiroga",
        "correo_profesor": "lvera@ubiobio.cl",
        "sexo": "M",
        "altura": 173.0,
        "peso": 70.0,
        "antecedentes_medicos": "Alguna :p",
        "area_docencia": "ELECTRONICA",
        "id_institucion": "Universidad del Bío-Bío"
    }
    ```
- **DELETE**: `http://127.0.0.1:8000/api/profesores/114776017/`

---

### Aulas

- **GET**: `http://127.0.0.1:8000/api/aulas/?rut_institucion=609110066`
- **GET**: `http://127.0.0.1:8000/api/aulas/?nro_aula=101AB&rut_institucion=609110066`
- **POST**: `http://127.0.0.1:8000/api/aulas/`
    ```json
    {
        "nro_aula": "301AB",
        "tamaño": 300,
        "cantidad_alumnos": 50,
        "descripcion": "Alguna",
        "id_institucion": "609110066"
    }
    ```
- **PUT**: `http://127.0.0.1:8000/api/aulas/202AB/609110066/`
    ```json
    {
        "nro_aula": "202AB",
        "tamaño": 200,
        "cantidad_alumnos": 50,
        "descripcion": "Alguna",
        "id_institucion": "Universidad del Bío-Bío"
    }
    ```
- **DELETE**: `http://127.0.0.1:8000/api/aulas/301AB/609110066/`

---

### Horarios

- **GET**: `http://127.0.0.1:8000/api/horarios/`
- **GET**: `http://127.0.0.1:8000/api/horarios/?nro_aula=101AB&nombre_institucion=Universidad%20del%20Bío-Bío`
- **GET**: `http://127.0.0.1:8000/api/horarios/?rut_profesor=202752578`
- **POST**: `http://127.0.0.1:8000/api/horarios/`
    ```json
    {
        "dia": "Lunes",
        "hora_inicio": "14:00:00",
        "hora_termino": "15:00:00",
        "id_profesor": "202752578",
        "id_aula": {
            "nro_aula": "202AB",
            "nombre_institucion": "Universidad del Bío-Bío"
        }
    }
    ```
- **PUT**: `/api/horarios/202752578/102AB/Universidad%20del%20Bío-Bío/Lunes/11:00:00/12:00:00/`
    ```json
    {
        "dia": "Lunes",
        "hora_inicio": "11:30:00",  ##<--- Cambio la hora inicio
        "hora_termino": "12:00:00",
        "id_profesor": "202752578",
        "aula": {
            "nro_aula": "102AB",
            "nombre_institucion": "Universidad del Bío-Bío"
        }
    }
    ```
- **DELETE**: `/api/horarios/202752578/102AB/Universidad%20del%20Bío-Bío/Lunes/11:30:00/12:00:00/`
