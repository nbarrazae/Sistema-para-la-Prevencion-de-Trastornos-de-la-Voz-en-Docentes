# Sistema Accesible de Dosimetría Vocal y Monitorización Ambiental para la Prevención de Trastornos de la Voz en Docentes

Este proyecto ha sido presentado para optar al título de Ingeniero Civil Informático

## 📄 Resumen del Proyecto

El sistema busca **definir las bases para el desarrollo de prototipos de dispositivos de dosimetría vocal y monitorización ambiental**. Estos dispositivos abordan la problemática de los trastornos de la voz que afectan a los docentes debido al uso prolongado de sus capacidades vocales en condiciones ambientales adversas, impactando negativamente su salud, calidad de vida y desempeño educativo.

La implementación integra **tecnologías accesibles y de bajo costo** para medir y analizar variables clave de la voz y parámetros ambientales mediante sensores especializados. Los datos se visualizan a través de una **plataforma web intuitiva** que permite el seguimiento constante para prevenir complicaciones. El sistema prioriza la simplicidad, funcionalidad y portabilidad, facilitando su adopción en comunidades educativas con recursos limitados.

## 💡 Problema Abordado

El problema principal es la **falta de acceso a dispositivos de dosimetría vocal y monitorización ambiental debido a sus altos costos**, lo que dificulta el monitoreo continuo y la investigación en fonoaudiología.

## 🚀 Propuesta de Solución

La solución es el desarrollo de un **sistema accesible de dosimetría vocal y monitorización ambiental** que integra hardware de bajo costo y software especializado. Esto incluye:
*   Un **prototipo de dosímetro de voz** para registrar la intensidad y frecuencia de la voz con mayor precisión.
*   Un **registrador de variables ambientales** para medir la intensidad de ruido de forma confiable, además de temperatura, humedad y dióxido de carbono.
*   Los dispositivos se conectan a un **servidor remoto para almacenar los datos**.
*   Una **plataforma web intuitiva** para visualizar gráficos que relacionan los registros vocales de cada docente con las mediciones ambientales de las aulas donde impartió clases, y la posibilidad de exportar los datos para análisis adicionales.

## 🏗️ Arquitectura del Sistema

<img width="1315" height="761" alt="image" src="https://github.com/user-attachments/assets/bb7cff9d-0e50-4318-bd65-e9c8c9de6007" />
 
## 🛠️ Tecnologías Utilizadas

*   **Backend**:
    *   **Lenguaje**: Python.
    *   **Framework**: Django.
    *   **Base de Datos**: PostgreSQL.
*   **Frontend**:
    *   **Framework**: Bootstrap.
    *   **Lenguajes**: HTML, CSS, JavaScript.
*   **Dispositivos IoT**:
    *   **Microcontroladores**: WeMos D1 R32 ESP32.
    *   **Sensores**: Micrófono digital MEMS I2S SPH0645 (voz), Módulo SCD-30 (humedad, temperatura, CO2), Sensor de ruido ZTS-ZS-BZ-485-05.
    *   **Plataforma de Programación**: Arduino IDE (para microcontroladores).
*   **Broker MQTT**: Mosquitto MQTT.
*   **Herramientas de Desarrollo**:
    *   Visual Studio Code (editor de código).
    *   Postman (pruebas de API).
    *   DBeaver CE (cliente SQL multiplataforma).
    *   Git (control de versiones).
    *   Nginx (servidor web/proxy inverso).
    *   Gunicorn (servidor WSGI).

## ⚙️ Estructura del Código

El proyecto se organiza en directorios clave:

```bash
.
├── manage.py                   # Script principal de Django
├── Proyecto_De_Titulo/         # Configuración global del proyecto
│   ├── settings.py             # Configuraciones de Django (DB, apps, etc.)
│   ├── urls.py                 # Enrutador raíz del proyecto
│   └── ...
├── staticfiles/                # Archivos estáticos servidos (CSS, JS, imágenes)
├── web_monitor/                # Aplicación principal de Django
│   ├── admin.py                # Configuración del panel de administración
│   ├── models.py               # Modelos de datos para la base de datos
│   ├── mqtt_client.py          # Cliente MQTT para suscripción y recepción de datos
│   ├── static/                 # Archivos estáticos específicos de la app
│   ├── templates/              # Plantillas HTML para el frontend
│   ├── urls.py                 # Enrutamiento de la aplicación
│   ├── views.py                # Vistas que responden a peticiones HTTP
│   └── ...
└── requirements.txt            # Dependencias Python del proyecto
```




Universidad del Bío-Bío, Chile, Facultad de Ciencias Empresariales, Departamento de Ciencias de la Computación y Tecnologías
