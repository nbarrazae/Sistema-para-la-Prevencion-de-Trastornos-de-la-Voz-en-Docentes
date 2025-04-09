import paho.mqtt.client as mqtt
import json
import logging
import os
from django.conf import settings

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
    """ Callback cuando se recibe un mensaje """
    #imprime el mensaje recibido
    print(f"Mensaje recibido({len(msg.payload.decode())}): {msg.topic} {msg.payload.decode()}")

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

