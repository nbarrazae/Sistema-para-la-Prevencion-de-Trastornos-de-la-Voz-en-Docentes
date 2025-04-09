#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "time.h"
#include <SPI.h>
#include <SD.h>
#include <PubSubClient.h>

// Configuración de WiFi
const char* ssid = "motog34";
const char* password = "98765432";

// Configuración NTP
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = -10800; // UTC-3 para Chile
const int daylightOffset_sec = 0;

// Configuración SD
const int chipSelect = 5;
const char* filePath = "/mediciones.txt";

// Configuración MQTT
const char* mqttServer = "192.168.226.95";  // IP del servidor MQTT
const int mqttPort = 1883;
WiFiClient espClient;
PubSubClient client(espClient);

// Estructura para almacenar horas de envío
struct HoraEnvio {
    int hora;
    int minuto;
};

const HoraEnvio horasEnvio[] = {
    {17, 10},
    {17, 11},
    {17, 12},
    {17, 13},
    {17, 14},
    {17, 35},
    {17, 36},
    {17, 37},
    {17, 38},
    {17, 39}
};

const int numHorasEnvio = sizeof(horasEnvio) / sizeof(horasEnvio[0]);

int ultimaHora = -1;
int ultimoMinuto = -1;

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Conectando a WiFi...");
    }
    Serial.println("Conectado a WiFi!");

    // Configurar tiempo NTP
    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
    Serial.println("Tiempo NTP configurado.");

    // Inicializar SD
    Serial.print("Iniciando tarjeta SD...");
    if (!SD.begin(chipSelect)) {
        Serial.println("Error al inicializar SD.");
        return;
    }
    Serial.println("Tarjeta SD lista.");

    // Configurar MQTT
    client.setServer(mqttServer, mqttPort);
}

void loop() {
    registrarMedicion();  // Siempre guardar datos
    verificarEnvio();  // Verificar si es hora de enviar datos
    delay(2000);  // Cada 2 segundos para test
}

void registrarMedicion() {
    DynamicJsonDocument doc(256);
    doc["timestamp"] = obtenerHoraNTP();
    doc["temperatura"] = random(20, 30);
    doc["humedad"] = random(40, 60);
    doc["co2"] = random(300, 600);
    doc["ruido"] = random(50, 80);

    String jsonString;
    serializeJson(doc, jsonString);

    File dataFile = SD.open(filePath, FILE_APPEND);
    if (dataFile) {
        dataFile.println(jsonString);
        dataFile.close();
        Serial.println("Medición guardada en SD.");
    } else {
        Serial.println("Error al escribir en SD.");
    }
}

void verificarEnvio() {
    int horaActual, minutoActual;
    if (!obtenerHoraActual(horaActual, minutoActual)) return;

    for (int i = 0; i < numHorasEnvio; i++) {
        if (horaActual == horasEnvio[i].hora && minutoActual == horasEnvio[i].minuto) {
            if (horaActual != ultimaHora || minutoActual != ultimoMinuto) {
                enviarLineaPorLinea();
                ultimaHora = horaActual;
                ultimoMinuto = minutoActual;
            }
            break;
        }
    }
}

void enviarLineaPorLinea() {
    if (!client.connected()) {
        Serial.println("Conectando a MQTT...");
        if (client.connect("ESP32Client")) {
            Serial.println("Conectado a MQTT!");
        } else {
            Serial.print("Fallo MQTT, estado: ");
            Serial.println(client.state());
            return;  // Si no se conecta, no intentamos enviar
        }
    }

    File dataFile = SD.open(filePath);
    if (dataFile) {
        Serial.println("Enviando mediciones línea por línea:");

        // Leer el archivo línea por línea
        while (dataFile.available()) {
            String linea = dataFile.readStringUntil('\n');  // Leer una línea
            linea.trim();  // Eliminar espacios en blanco y saltos de línea

            // Enviar la línea leída a través de MQTT
            if (linea.length() > 0) {
                Serial.println(linea);  // Imprimir en el monitor serie
                if (client.publish("test/topic", linea.c_str(), true)) {
                    Serial.println("Línea enviada a MQTT!");
                } else {
                    Serial.println("Error enviando línea a MQTT.");
                }
            }

            delay(1000);  // Pequeña espera entre mensajes para evitar sobrecargar el servidor MQTT
        }

        dataFile.close();  // Cerrar el archivo después de leer

        // Borrar el archivo después de enviarlo
        if (SD.remove(filePath)) {
            Serial.println("Archivo borrado exitosamente después de enviar.");
        } else {
            Serial.println("Error al borrar el archivo.");
        }
    } else {
        Serial.println("No se pudo abrir el archivo mediciones.txt.");
    }
}

bool obtenerHoraActual(int &hora, int &minuto) {
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo)) {
        Serial.println("Error obteniendo la hora");
        return false;
    }
    hora = timeinfo.tm_hour;
    minuto = timeinfo.tm_min;
    return true;
}

String obtenerHoraNTP() {
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo)) {
        Serial.println("Error obteniendo la hora");
        return "0000-00-00 00:00:00";
    }

    char buffer[20];
    snprintf(buffer, sizeof(buffer), "%04d-%02d-%02d %02d:%02d:%02d",
             timeinfo.tm_year + 1900, timeinfo.tm_mon + 1, timeinfo.tm_mday,
             timeinfo.tm_hour, timeinfo.tm_min, timeinfo.tm_sec);

    return String(buffer);
}