/*
 * Wearable ESP32 — Ecosistema Alzheimer (H1)
 * -------------------------------------------------------------
 * Mide frecuencia cardiaca (MAX30102) + pasos/caida (MPU6050),
 * boton SOS y recordatorio haptico (motor vibrador).
 * Publica biometricos por BLE (notify) y recibe comandos (write).
 *
 * Servicio BLE:
 *   BIO  (notify)  -> {"hr":72,"steps":1240,"act":"quieto","fall":false}
 *   SOS  (notify)  -> "SOS"
 *   CMD  (write)   -> {"cmd":"remind"}  activa vibracion 2s
 *
 * Pinout (ESP32 DevKit v1):
 *   MAX30102  SDA=21 SCL=22 3V3 GND   (I2C 0x57)
 *   MPU6050   SDA=21 SCL=22 3V3 GND   (I2C 0x68, bus compartido)
 *   Motor vib GPIO13 (via transistor 2N2222 + R1k + diodo flyback)
 *   Boton SOS GPIO14 -> GND (INPUT_PULLUP), mantener 3s
 *
 * Librerias (Library Manager):
 *   - SparkFun MAX3010x Pulse and Proximity Sensor Library
 *   - Adafruit MPU6050  + Adafruit Unified Sensor
 *   - (BLE nativa del core ESP32)
 * Placa: "ESP32 Dev Module". Board Manager URL:
 *   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
 */

#include <Wire.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include "MAX30105.h"
#include "heartRate.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// ---- UUIDs (deben coincidir con el frontend / test page) ----
#define SERVICE_UUID "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
#define CHAR_BIO_UUID "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
#define CHAR_SOS_UUID "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
#define CHAR_CMD_UUID "6e400004-b5a3-f393-e0a9-e50e24dcca9e"

const int PIN_MOTOR = 13;
const int PIN_SOS = 14;

MAX30105 hrSensor;
Adafruit_MPU6050 mpu;

BLECharacteristic *chBio;
BLECharacteristic *chSos;
bool deviceConnected = false;

// ---- Estado HR ----
const byte RATE_SIZE = 4;
byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0;
int beatAvg = 0;

// ---- Estado pasos / caida ----
long steps = 0;
float lastMag = 1.0;
bool stepHigh = false;
unsigned long lastStepMs = 0;
bool fallFlag = false;

// ---- Timers ----
unsigned long lastPublish = 0;
unsigned long sosPressStart = 0;

class ServerCB : public BLEServerCallbacks {
  void onConnect(BLEServer *s) { deviceConnected = true; }
  void onDisconnect(BLEServer *s) {
    deviceConnected = false;
    s->getAdvertising()->start();  // re-anunciar
  }
};

// Recibe comandos del navegador/app
class CmdCB : public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic *c) {
    String v = c->getValue().c_str();
    if (v.indexOf("remind") >= 0) buzz(2000);
  }
};

void buzz(int ms) {
  digitalWrite(PIN_MOTOR, HIGH);
  delay(ms);
  digitalWrite(PIN_MOTOR, LOW);
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_MOTOR, OUTPUT);
  digitalWrite(PIN_MOTOR, LOW);
  pinMode(PIN_SOS, INPUT_PULLUP);

  Wire.begin(21, 22);

  if (hrSensor.begin(Wire, I2C_SPEED_FAST)) {
    hrSensor.setup();                 // config por defecto
    hrSensor.setPulseAmplitudeRed(0x0A);
    hrSensor.setPulseAmplitudeGreen(0);
  } else {
    Serial.println("MAX30102 no detectado");
  }

  if (!mpu.begin()) Serial.println("MPU6050 no detectado");
  else {
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  }

  // ---- BLE ----
  BLEDevice::init("Wearable-DonJose");
  BLEServer *server = BLEDevice::createServer();
  server->setCallbacks(new ServerCB());
  BLEService *svc = server->createService(SERVICE_UUID);

  chBio = svc->createCharacteristic(CHAR_BIO_UUID, BLECharacteristic::PROPERTY_NOTIFY);
  chBio->addDescriptor(new BLE2902());
  chSos = svc->createCharacteristic(CHAR_SOS_UUID, BLECharacteristic::PROPERTY_NOTIFY);
  chSos->addDescriptor(new BLE2902());
  BLECharacteristic *chCmd =
      svc->createCharacteristic(CHAR_CMD_UUID, BLECharacteristic::PROPERTY_WRITE);
  chCmd->setCallbacks(new CmdCB());

  svc->start();
  server->getAdvertising()->addServiceUUID(SERVICE_UUID);
  server->getAdvertising()->start();
  Serial.println("BLE anunciando: Wearable-DonJose");
}

void readHeartRate() {
  long ir = hrSensor.getIR();
  if (ir < 50000) return;  // sin dedo sobre el sensor
  if (checkForBeat(ir)) {
    long delta = millis() - lastBeat;
    lastBeat = millis();
    int bpm = 60 / (delta / 1000.0);
    if (bpm > 20 && bpm < 255) {
      rates[rateSpot++] = (byte)bpm;
      rateSpot %= RATE_SIZE;
      int sum = 0;
      for (byte x = 0; x < RATE_SIZE; x++) sum += rates[x];
      beatAvg = sum / RATE_SIZE;
    }
  }
}

void readMotion() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  float mag = sqrt(a.acceleration.x * a.acceleration.x +
                   a.acceleration.y * a.acceleration.y +
                   a.acceleration.z * a.acceleration.z) /
              9.81;  // en g

  // Conteo de pasos por picos con debounce
  if (mag > 1.2 && !stepHigh && millis() - lastStepMs > 300) {
    steps++;
    stepHigh = true;
    lastStepMs = millis();
  }
  if (mag < 1.05) stepHigh = false;

  // Caida: pico fuerte (>2.5g)
  if (mag > 2.5) fallFlag = true;
  lastMag = mag;
}

const char *activity() {
  if (millis() - lastStepMs < 5000) return "activo";
  return "quieto";
}

void loop() {
  readHeartRate();
  readMotion();

  // SOS: mantener boton 3s
  if (digitalRead(PIN_SOS) == LOW) {
    if (sosPressStart == 0) sosPressStart = millis();
    else if (millis() - sosPressStart > 3000) {
      if (deviceConnected) {
        chSos->setValue("SOS");
        chSos->notify();
      }
      buzz(500);
      sosPressStart = 0;
      delay(1000);
    }
  } else {
    sosPressStart = 0;
  }

  // Publicar biometricos cada 3s
  if (millis() - lastPublish > 3000) {
    lastPublish = millis();
    char buf[96];
    snprintf(buf, sizeof(buf), "{\"hr\":%d,\"steps\":%ld,\"act\":\"%s\",\"fall\":%s}",
             beatAvg, steps, activity(), fallFlag ? "true" : "false");
    Serial.println(buf);
    if (deviceConnected) {
      chBio->setValue(buf);
      chBio->notify();
    }
    fallFlag = false;
  }
}
