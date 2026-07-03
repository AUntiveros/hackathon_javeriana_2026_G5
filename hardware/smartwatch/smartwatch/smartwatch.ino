/*
 * Smartwatch Nino — ESP32 + MAX30102 (PPG)
 * -------------------------------------------------------------
 * Mide FC y variabilidad (HRV/RMSSD) por PPG, botón SOS y recordatorio
 * háptico. Envía vitales al backend por WiFi (POST /vitals). Monitoreo
 * CARDIOVASCULAR (para hipertensos), NO evalúa deterioro cognitivo.
 *
 * Flujo:
 *   MAX30102 -> FC + RR intervals -> RMSSD (HRV)
 *   WiFi POST http://<BACKEND>/vitals  {"patient_id":1,"hr":..,"hrv_ms":..}
 *   El backend estima presión (no invasiva) y la muestra al médico/cuidador.
 *   Botón SOS + motor vibrador para recordatorios.
 *
 * Conexiones (ESP32 DevKit):
 *   MAX30102  SDA=21 SCL=22 3V3 GND
 *   Motor vib GPIO13 (via 2N2222 + R1k + diodo)
 *   Botón SOS GPIO14 -> GND (INPUT_PULLUP)
 *
 * Librerías: SparkFun MAX3010x, heartRate.h, WiFi.h, HTTPClient.h
 */
#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "MAX30105.h"
#include "heartRate.h"

const char* WIFI_SSID = "TU_WIFI";
const char* WIFI_PASS = "TU_PASS";
const char* BACKEND   = "http://192.168.1.100:8000";  // IP del backend
const int   PATIENT_ID = 1;

const int PIN_MOTOR = 13;
const int PIN_SOS = 14;

MAX30105 sensor;

long lastBeat = 0;
float rr[10];          // últimos intervalos RR (ms)
int rrIdx = 0, rrCount = 0;
int beatAvg = 0;
byte rates[4]; byte rateSpot = 0;
unsigned long lastSend = 0;

void buzz(int ms){ digitalWrite(PIN_MOTOR,HIGH); delay(ms); digitalWrite(PIN_MOTOR,LOW); }

float rmssd(){
  if (rrCount < 3) return 0;
  float sum = 0; int n = 0;
  for (int i=1;i<rrCount;i++){ float d=rr[i]-rr[i-1]; sum+=d*d; n++; }
  return n? sqrt(sum/n):0;
}

void setup(){
  Serial.begin(115200);
  pinMode(PIN_MOTOR,OUTPUT); digitalWrite(PIN_MOTOR,LOW);
  pinMode(PIN_SOS,INPUT_PULLUP);
  Wire.begin(21,22);
  if(sensor.begin(Wire, I2C_SPEED_FAST)){
    sensor.setup(); sensor.setPulseAmplitudeRed(0x0A); sensor.setPulseAmplitudeGreen(0);
  } else Serial.println("MAX30102 no detectado");
  WiFi.begin(WIFI_SSID, WIFI_PASS);
}

void readPPG(){
  long ir = sensor.getIR();
  if (ir < 50000) return;
  if (checkForBeat(ir)){
    long now = millis();
    float interval = now - lastBeat;   // RR en ms
    lastBeat = now;
    int bpm = 60000.0 / interval;
    if (bpm>20 && bpm<255){
      rates[rateSpot++%4]=(byte)bpm;
      int s=0; for(byte i=0;i<4;i++) s+=rates[i]; beatAvg=s/4;
      rr[rrIdx++%10]=interval; if(rrCount<10) rrCount++;
    }
  }
}

void enviarVital(){
  if (WiFi.status()!=WL_CONNECTED) return;
  HTTPClient http;
  http.begin(String(BACKEND)+"/vitals");
  http.addHeader("Content-Type","application/json");
  String body = "{\"patient_id\":"+String(PATIENT_ID)+",\"hr\":"+String(beatAvg)+
                ",\"hrv_ms\":"+String(rmssd(),1)+"}";
  http.POST(body);
  http.end();
}

void loop(){
  readPPG();
  if (digitalRead(PIN_SOS)==LOW){ buzz(500); /* TODO: POST /alertas SOS */ delay(1000); }
  if (millis()-lastSend > 15000){   // cada 15s
    lastSend = millis();
    Serial.printf("HR=%d HRV=%.1f\n", beatAvg, rmssd());
    enviarVital();
  }
}
