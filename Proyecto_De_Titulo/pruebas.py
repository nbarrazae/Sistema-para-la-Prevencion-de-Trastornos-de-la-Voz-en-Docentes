import paho.mqtt.client as mqtt
import json
from datetime import datetime, timedelta
import random
from time import sleep

# ---------- CONFIGURACIÓN ----------
BROKER = "146.83.194.142"
TOPIC = "test/topic"
MAC = "cc:db:a7:35:6c:a4"

TOTAL_MINUTOS = 60 * 6     # Ej. 1 hora de datos
INTERVALO = 60         # Un dato por minuto (en segundos)

# # Inicializar cliente MQTT
# client = mqtt.Client()
# client.connect(BROKER)
# # Inicializar cliente MQTT
client = mqtt.Client()
client.connect(BROKER, port=1712)

# Tiempo base simulado
hora_inicio = datetime(2025, 7, 14, 8 , 0, 0)  # Puedes cambiar la hora de inicio

print(f"Generando {TOTAL_MINUTOS} registros por variable...")

for i in range(TOTAL_MINUTOS):
    timestamp = hora_inicio + timedelta(seconds=i * INTERVALO)
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    # Temperatura (°C)
    temp = round(random.uniform(18.0, 28.0), 2)
    payload_temp = {
        "Mac": MAC,
        "timestamp": timestamp_str,
        "temperatura": str(temp)
    }
    client.publish(TOPIC, json.dumps(payload_temp))
    print("Temperatura:", payload_temp)
    #sleep(1)  # Esperar 1 segundo entre publicaciones   
    # Humedad (%)
    hum = round(random.uniform(30.0, 70.0), 2)
    payload_hum = {
        "Mac": MAC,
        "timestamp": timestamp_str,
        "humedad": str(hum)
    }
    client.publish(TOPIC, json.dumps(payload_hum))
    print("Humedad:", payload_hum)
    #sleep(1) 
    # CO2 (ppm)
    co2 = random.randint(400, 1200)
    payload_co2 = {
        "Mac": MAC,
        "timestamp": timestamp_str,
        "CO2": str(co2)
    }
    client.publish(TOPIC, json.dumps(payload_co2))
    #sleep(1) 
    print("CO2:", payload_co2)
    #ruido = random.randint(30, 100)  # Nivel de ruido en dB
    ruido = round(random.uniform(30.0, 100.0), 2)  # Nivel de ruido en dB
    payload_ruido = {
        "Mac": MAC,
        "timestamp": timestamp_str,
        "ruido": str(ruido)
    }
    client.publish(TOPIC, json.dumps(payload_ruido))
    print("Ruido:", payload_ruido)
    sleep(1)  # Esperar 1 segundo entre publicaciones

client.disconnect()
print("Finalizado.")

########## Datos de Voz  ################
# import paho.mqtt.client as mqtt
# import json
# from datetime import datetime, timedelta
# import random

# # ---------- CONFIGURACIÓN ----------
# BROKER = "localhost"
# TOPIC = "test/topic"
# MAC = "00:1A:2B:3C:4D:5E"

# # Cantidad total de datos a generar
# TOTAL_MINUTOS = 60 * 5  # Por ejemplo, una hora de datos
# DATOS_POR_MINUTO = 6  # Uno cada 10 segundos

# # Inicializar cliente MQTT
# client = mqtt.Client()
# client.connect(BROKER)

# # Tiempo base (simulado)
# hora_inicio = datetime(2025, 7, 1, 12, 0, 0)  # Puedes cambiar la hora de inicio
# delta = timedelta(seconds=60 // DATOS_POR_MINUTO)

# print(f"Generando {TOTAL_MINUTOS * DATOS_POR_MINUTO} registros...")

# # Bucle para enviar todos los datos simulados
# for i in range(TOTAL_MINUTOS * DATOS_POR_MINUTO):
#     timestamp = hora_inicio + i * delta
#     timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

#     FF = str(random.randint(100, 200))
#     IV = str(random.randint(50, 100))

#     payload = {
#         "Mac": MAC,
#         "timestamp": timestamp_str,
#         "FF": FF,
#         "IV": IV
#     }

#     client.publish(TOPIC, json.dumps(payload))
#     print("Enviado: ", payload)

# client.disconnect()
# print("Finalizado.")

