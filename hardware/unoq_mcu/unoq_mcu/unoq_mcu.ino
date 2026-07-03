/*
 * Uno Q — sketch del MCU (STM32U585) para biometricos
 * -------------------------------------------------------------
 * Lee FC (MAX30102) + pasos/caida (MPU6050) + boton SOS, controla
 * el motor vibrador. Se comunica con el lado Linux (Python) por
 * Serial (puente interno del Uno Q) — NO usa BLE.
 *
 * SALIDA (Serial, una linea JSON):
 *   {"hr":72,"steps":1240,"act":"quieto","fall":false,"sos":false}
 * ENTRADA (Serial, comandos de texto):
 *   remind   -> vibra 2s
 *
 * Conexiones (headers Arduino del Uno Q):
 *   MAX30102  SDA/SCL (pines I2C del Uno Q)  3V3  GND   (0x57)
 *   MPU6050   SDA/SCL (mismo bus I2C)         3V3  GND   (0x68)
 *   Motor vib D3 -> base 2N2222 (R1k); colector->motor->5V; emisor->GND; diodo flyback
 *   Boton SOS D2 -> GND (INPUT_PULLUP), mantener 3s
 *
 * NOTA: confirmar en la placa las etiquetas de los pines I2C del Uno Q.
 * Librerias: SparkFun MAX3010x, Adafruit MPU6050 (+ Unified Sensor).
 * Compilar el sketch desde Arduino App Lab (target MCU del Uno Q).
 */

#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

const int PIN_MOTOR = 3;
const int PIN_SOS = 2;

MAX30105 hrSensor;
Adafruit_MPU6050 mpu;

const byte RATE_SIZE = 4;
byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0;
int beatAvg = 0;

long steps = 0;
bool stepHigh = false;
unsigned long lastStepMs = 0;
bool fallFlag = false;
bool sosFlag = false;

unsigned long lastPublish = 0;
unsigned long sosPressStart = 0;

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

  Wire.begin();
  if (hrSensor.begin(Wire, I2C_SPEED_FAST)) {
    hrSensor.setup();
    hrSensor.setPulseAmplitudeRed(0x0A);
    hrSensor.setPulseAmplitudeGreen(0);
  }
  if (mpu.begin()) {
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  }
}

void readHeartRate() {
  long ir = hrSensor.getIR();
  if (ir < 50000) return;  // sin dedo
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
  sensors_event_t a, g, t;
  mpu.getEvent(&a, &g, &t);
  float mag = sqrt(a.acceleration.x * a.acceleration.x +
                   a.acceleration.y * a.acceleration.y +
                   a.acceleration.z * a.acceleration.z) / 9.81;
  if (mag > 1.2 && !stepHigh && millis() - lastStepMs > 300) {
    steps++;
    stepHigh = true;
    lastStepMs = millis();
  }
  if (mag < 1.05) stepHigh = false;
  if (mag > 2.5) fallFlag = true;
}

const char *activity() {
  return (millis() - lastStepMs < 5000) ? "activo" : "quieto";
}

void handleSerial() {
  if (!Serial.available()) return;
  String cmd = Serial.readStringUntil('\n');
  cmd.trim();
  if (cmd == "remind") buzz(2000);
}

void loop() {
  readHeartRate();
  readMotion();
  handleSerial();

  // SOS: mantener boton 3s
  if (digitalRead(PIN_SOS) == LOW) {
    if (sosPressStart == 0) sosPressStart = millis();
    else if (millis() - sosPressStart > 3000) {
      sosFlag = true;
      buzz(500);
      sosPressStart = 0;
    }
  } else {
    sosPressStart = 0;
  }

  if (millis() - lastPublish > 3000) {
    lastPublish = millis();
    char buf[112];
    snprintf(buf, sizeof(buf),
             "{\"hr\":%d,\"steps\":%ld,\"act\":\"%s\",\"fall\":%s,\"sos\":%s}",
             beatAvg, steps, activity(),
             fallFlag ? "true" : "false", sosFlag ? "true" : "false");
    Serial.println(buf);
    fallFlag = false;
    sosFlag = false;
  }
}
