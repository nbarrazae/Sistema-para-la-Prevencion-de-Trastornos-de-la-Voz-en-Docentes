import paho.mqtt.client as mqtt
import json
import logging
import os
from django.conf import settings
from datetime import datetime
from django.utils.timezone import make_aware
from pytz import timezone

logger = logging.getLogger(__name__)

MQTT_BROKER = settings.MQTT_BROKER
MQTT_PORT = settings.MQTT_PORT
MQTT_TOPIC = settings.MQTT_TOPIC

def on_connect(client, userdata, flags, rc):
    """ Callback cuando se conecta al broker """
    if rc == 0:
        logger.info("Conectado a MQTT Broker")
        client.subscribe(MQTT_TOPIC)
    else:
        logger.error(f"Fallo en la conexión MQTT, código de error: {rc}")

def on_message(client, userdata, msg):
    from .models import Aula_Ruido, Aula_Humedad, Aula_Temperatura, Aula_CO2, Relacion_Aula, Profesor_Voz, Relacion_Profesor
    """ Callback cuando se recibe un mensaje """
    try:
        payload = json.loads(msg.payload.decode())
        mac = payload.get("Mac")
        timestamp = payload.get("timestamp")
        data_type = next((key for key in payload.keys() if key not in ["Mac", "timestamp"]), None)
        value = payload.get(data_type)

        if not mac or not timestamp or not data_type or value is None:
            logger.error("Datos incompletos en el mensaje recibido.")
            return

        # Buscar la relación entre el dispositivo y el aula
        relacion_aula = Relacion_Aula.objects.filter(mac=mac).first()
        relacion_profesor = None  # inicializar por si se necesita más tarde

        if not relacion_aula:
            # Si no se encuentra la relación con el aula, buscar si es un profesor
            relacion_profesor = Relacion_Profesor.objects.filter(mac=mac).first()
            if relacion_profesor:
                # Usar el dispositivo del profesor para buscar su aula (si existe)
                dispositivo = relacion_profesor.id_dispositivo
                relacion_aula = Relacion_Aula.objects.filter(id_dispositivo=dispositivo).first()
            else:
                logger.error(f"No se encontró relación para el dispositivo con MAC: {mac}")
                return


        # Convertir timestamp a objeto datetime
        tz = timezone("America/Santiago")
        fecha_hora = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        fecha_hora = tz.localize(fecha_hora)
        print(f"Timestamp recibido: {timestamp}")  # ← Agregado para depurar
        print(f"Fecha y hora convertidas: {fecha_hora}")  # ← Agregado para depurar
        # Guardar los datos en la base de datos según el tipo
        if data_type == "ruido":
            if not Aula_Ruido.objects.filter(fecha_hora=fecha_hora, id_aula=relacion_aula.id_aula).exists():
                Aula_Ruido.objects.create(fecha_hora=fecha_hora, ruido=value, id_aula=relacion_aula.id_aula)
                print(f"Datos guardados: {data_type} - {value}")  # ← Agregado para depurar
            else:
                logger.warning(f"Registro duplicado detectado: fecha_hora={fecha_hora}, id_aula={relacion_aula.id_aula}")
        elif data_type == "humedad":
            if not Aula_Humedad.objects.filter(fecha_hora=fecha_hora, id_aula=relacion_aula.id_aula).exists():
                Aula_Humedad.objects.create(fecha_hora=fecha_hora, humedad=value, id_aula=relacion_aula.id_aula)
            else:
                logger.warning(f"Registro duplicado detectado: fecha_hora={fecha_hora}, id_aula={relacion_aula.id_aula}")
        elif data_type == "temperatura":
            if not Aula_Temperatura.objects.filter(fecha_hora=fecha_hora, id_aula=relacion_aula.id_aula).exists():
                Aula_Temperatura.objects.create(fecha_hora=fecha_hora, temperatura=value, id_aula=relacion_aula.id_aula)
            else:
                logger.warning(f"Registro duplicado detectado: fecha_hora={fecha_hora}, id_aula={relacion_aula.id_aula}")
        elif data_type == "CO2":
            if not Aula_CO2.objects.filter(fecha_hora=fecha_hora, id_aula=relacion_aula.id_aula).exists():
                Aula_CO2.objects.create(fecha_hora=fecha_hora, co2=value, id_aula=relacion_aula.id_aula)
            else:
                logger.warning(f"Registro duplicado detectado: fecha_hora={fecha_hora}, id_aula={relacion_aula.id_aula}")
        # elif {'Mac': '00:1B:44:11:3A:B7', 'timestamp': '2025-07-02 15:01:54', 'FF': '150', 'IV': '60'}
        elif data_type == "FF":
            profesor_voz = Profesor_Voz(
                fecha_hora=fecha_hora,
                Freq=float(value),
                Intensidad=float(payload.get("IV", 0)),  # Valor por defecto si IV no está presente
                id_profesor=relacion_profesor.id_profesor if relacion_profesor else None
            )
            print(f"Datos guardados: {data_type} - Freq: {value}, Intensidad: {payload.get('IV', 0)}")  # ← Agregado para depurar
            profesor_voz.save()

        else:
            logger.error(f"Tipo de dato desconocido: {data_type}")
            return

        logger.info(f"Datos guardados correctamente: {data_type} - {value}")
    except Exception as e:
        logger.error(f"Error al procesar el mensaje: {e}")
    

def start_mqtt():
    """ Inicia el cliente MQTT con autenticación opcional """
    print("Intentando conectar al broker MQTT...")  # ← Agregado para depurar
    logger.info("Intentando conectar al broker MQTT...")

    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, settings.MQTT_KEEPALIVE)
        client.loop_start()
        print("Conexión iniciada correctamente.")  # ← Agregado para depurar
        logger.info("Conexión iniciada correctamente.")
    except Exception as e:
        print(f"Error al conectar con MQTT: {e}")  # ← Agregado para depurar
        logger.error(f"Error al conectar con MQTT: {e}")

    return client