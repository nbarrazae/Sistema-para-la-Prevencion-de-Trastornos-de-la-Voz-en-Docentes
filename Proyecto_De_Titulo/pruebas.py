import paho.mqtt.client as mqtt
import json
from datetime import datetime, timedelta
import random
from time import sleep

# ---------- CONFIGURACIÓN ----------
BROKER = "localhost"
TOPIC = "test/topic"
MAC = "00:1B:44:11:3A:B7"

TOTAL_MINUTOS = 60     # Ej. 1 hora de datos
INTERVALO = 60         # Un dato por minuto (en segundos)

# Inicializar cliente MQTT
client = mqtt.Client()
client.connect(BROKER)

# Tiempo base simulado
hora_inicio = datetime(2025, 7, 3, 14, 0, 0)  # Puedes cambiar la hora de inicio

print(f"Generando {TOTAL_MINUTOS} registros por variable...")

for i in range(TOTAL_MINUTOS):
    timestamp = hora_inicio + timedelta(seconds=i * INTERVALO)
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    # # Temperatura (°C)
    # temp = round(random.uniform(18.0, 28.0), 2)
    # payload_temp = {
    #     "Mac": MAC,
    #     "timestamp": timestamp_str,
    #     "temperatura": str(temp)
    # }
    # client.publish(TOPIC, json.dumps(payload_temp))
    # print("Temperatura:", payload_temp)
    # sleep(1)  # Esperar 1 segundo entre publicaciones   
    # # Humedad (%)
    # hum = round(random.uniform(30.0, 70.0), 2)
    # payload_hum = {
    #     "Mac": MAC,
    #     "timestamp": timestamp_str,
    #     "humedad": str(hum)
    # }
    # client.publish(TOPIC, json.dumps(payload_hum))
    # print("Humedad:", payload_hum)
    # sleep(1) 
    # # CO2 (ppm)
    # co2 = random.randint(400, 1200)
    # payload_co2 = {
    #     "Mac": MAC,
    #     "timestamp": timestamp_str,
    #     "CO2": str(co2)
    # }
    # client.publish(TOPIC, json.dumps(payload_co2))
    # sleep(1) 
    # print("CO2:", payload_co2)
    # #ruido = random.randint(30, 100)  # Nivel de ruido en dB
    ruido = round(random.uniform(30.0, 100.0), 2)  # Nivel de ruido en dB
    payload_ruido = {
        "Mac": MAC,
        "timestamp": timestamp_str,
        "ruido": str(ruido)
    }
    client.publish(TOPIC, json.dumps(payload_ruido))
    print("Ruido:", payload_ruido)
    sleep(1)

client.disconnect()
print("Finalizado.")
