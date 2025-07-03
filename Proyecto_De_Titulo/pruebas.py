import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime, timedelta
import random

# ---------- CONFIGURACIÓN ----------
BROKER = "localhost"
TOPIC = "test/topic"
MAC = "00:1A:2B:3C:4D:5E"  # Cambiado según el formato solicitado

# Intervalos
intervalo_ruido = 1       # segundos
intervalo_ambiente = 30   # segundos

# Inicializar cliente MQTT
client = mqtt.Client()
client.connect(BROKER)

# Control de tiempo
ultimo_envio_ambiente = time.time()
N = 0 + (24*0)
print("Enviando datos... Ctrl+C para detener.")

try:
    while True:
        now = datetime.now()
        # Actualizar el timestamp dinámicamente
        timestamp_str = (now - timedelta(hours=N)).strftime("%Y-%m-%d %H:%M:%S")

        # Enviar datos cada segundo
        FF = str(random.randint(100, 200))  # Valor aleatorio para FF
        IV = str(random.randint(50, 100))  # Valor aleatorio para IV
        payload = {
            "Mac": MAC,
            "timestamp": timestamp_str,
            "FF": FF,
            "IV": IV
        }
        client.publish(TOPIC, json.dumps(payload))
        print("Enviado: ", payload)

        # Cada N segundos se envía el mismo formato
        if (time.time() - ultimo_envio_ambiente) >= intervalo_ambiente:
            FF = str(random.randint(100, 200))  # Valor aleatorio para FF
            IV = str(random.randint(50, 100))  # Valor aleatorio para IV
            payload = {
                "Mac": MAC,
                "timestamp": timestamp_str,
                "FF": FF,
                "IV": IV
            }
            client.publish(TOPIC, json.dumps(payload))
            print("Enviado: ", payload)

            ultimo_envio_ambiente = time.time()

        time.sleep(intervalo_ruido)

except KeyboardInterrupt:
    print("Finalizado.")
    client.disconnect()
