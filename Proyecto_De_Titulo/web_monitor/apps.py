from django.apps import AppConfig
import threading
from .mqtt_client import start_mqtt  # Asegúrate de que este archivo existe en web_monitor

class WebMonitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_monitor'

    def ready(self):
        print("Ejecutando MQTT desde apps.py...")  # Para verificar que ready() se ejecuta

        # Iniciar MQTT en un hilo separado para no bloquear Django
        threading.Thread(target=start_mqtt, daemon=True).start()
