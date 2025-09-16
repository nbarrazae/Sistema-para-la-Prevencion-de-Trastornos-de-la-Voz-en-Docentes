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
*   Una **registrador de variables ambientales** para medir la intensidad de ruido de forma confiable, además de temperatura, humedad y dióxido de carbono.
*   Los dispositivos se conectan a un **servidor remoto para almacenar los datos**.
*   Una **plataforma web intuitiva** para visualizar gráficos que relacionan los registros vocales de cada docente con las mediciones ambientales de las aulas donde impartió clases, y la posibilidad de exportar los datos para análisis adicionales.

## 🏗️ Arquitectura del Sistema

El sistema implementado sigue una arquitectura modular (Modelo-Template-Views similar a MVC):
*   **Dispositivos IoT**: Los prototipos de dosimetría vocal y monitorización ambiental capturan datos y los envían utilizando el protocolo MQTT.
*   **Broker MQTT**: **Mosquitto** actúa como intermediario, recibiendo los mensajes de los dispositivos.
*   **Backend**: Desarrollado con **Python y Django**, se comunica constantemente con Mosquitto para validar y almacenar los nuevos mensajes en la base de datos.
*   **Base de Datos**: **PostgreSQL** se utiliza como base de datos relacional para garantizar la integridad de los datos capturados y la información de gestión del sistema.
*   **Servidor Web**: **Nginx** se encarga de la entrega de contenido web y la gestión del tráfico (como proxy inverso para HTTPS y sirviendo archivos estáticos). Se complementa con **Gunicorn** como servidor WSGI para la aplicación Django.
*   **Frontend**: Utiliza **Bootstrap, HTML, CSS y JavaScript** para renderizar plantillas desde el backend, proporcionando una interfaz de usuario interactiva y dinámica.

## ✨ Características Principales

### Hardware (Dispositivos IoT)
*   **Dosímetro de Voz**:
    *   **Microcontrolador**: Placa WeMos D1 R32 ESP32.
    *   **Sensor de voz**: Micrófono digital MEMS I2S SPH0645, posicionado en el cuello para capturar vibraciones de cuerdas vocales, reduciendo ruido externo.
    *   **Mediciones**: Frecuencia fundamental de la voz (80-350 Hz) e Intensidad de la voz (30-80 dB).
    *   **Algoritmos**: Autocorrelación simple con normalización para frecuencia fundamental; cálculo de nivel continuo equivalente con filtro IIR biquad para intensidad, siguiendo la norma UNE-EN 61672.
    *   **Detección de voz**: Algoritmo para definir si el usuario está hablando basado en amplitud y varianza de los bloques de audio.
*   **Registrador de Variables Ambientales**:
    *   **Microcontrolador**: Placa WeMos D1 R32 ESP32.
    *   **Sensores**: Módulo SCD-30 para CO2, temperatura y humedad relativa. Sensor de ruido industrial ZTS-ZS-BZ-485-05 (con conversor MAX485) capaz de medir por encima de 80 dB.
    *   **Indicador visual**: Tres LEDs de 3mm (verde, amarillo, rojo) para indicar el nivel de ruido (0-50 dB, 51-85 dB, >86 dB respectivamente).
    *   **Calibración**: Compensa lecturas del sensor de ruido basadas en calibración con Brüel & Kjaer modelo 4231.
*   **Almacenamiento y Transmisión de Datos**: Ambos dispositivos guardan datos temporalmente en una tarjeta SD y los envían al servidor remoto a través de MQTT en horarios preestablecidos, en formato JSON.

### Software (Plataforma Web)
*   **Objetivo**: Recepción, almacenamiento y análisis de variables de voz y parámetros ambientales, facilitando la visualización de datos y el seguimiento de patrones relacionados con trastornos vocales.
*   **Gestión de Usuarios**: Roles definidos (Administrador, Fonoaudiólogo, Académico) con permisos específicos para control de acceso y protección de información sensible.
*   **Gestión de Entidades**: Permite la creación, gestión y eliminación de instituciones, aulas, docentes, horarios y dispositivos IoT.
*   **Visualización de Datos**: Interfaz intuitiva y dinámica con herramientas de filtrado y **gráficos que relacionan los parámetros vocales de un docente con las variables ambientales de las aulas** donde impartió clases.
*   **Exportación de Datos**: Funcionalidad para exportar estadísticas y datos en formatos como CSV o Excel para análisis adicionales y respaldo externo.

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




Universidad del Bío-Bío, Chile, Facultad de Ciencias Empresariales, Departamento de Sistemas de Información
