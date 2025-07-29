import paho.mqtt.publish as publish
import time
# Importar la librería paho-mqtt para publicar mensajes MQTT
# Configuración del broker y del topic
broker = "146.83.194.142"
port = 1712
topic = "test/topic"
archivo = "2025-07-25-13-46.txt"

# Leer el archivo línea por línea y publicar cada una
with open(archivo, "r") as file:
    for linea in file:
        linea = linea.strip()
        if linea:
            print(f"Enviando: {linea}")
            try:
                publish.single(topic, payload=linea, hostname=broker, port=port)
            except Exception as e:
                print(f"Error al enviar mensaje: {e}")
        time.sleep(0.5)
