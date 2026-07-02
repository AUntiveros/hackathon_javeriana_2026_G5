# Firmware ESP32 — flasheo y prueba

## 1. Preparar Arduino IDE
1. Instalar **Arduino IDE 2.x**.
2. File → Preferences → Additional Board Manager URLs:
   `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
3. Boards Manager → instalar **esp32 by Espressif**.
4. Library Manager → instalar:
   - **SparkFun MAX3010x Pulse and Proximity Sensor Library**
   - **Adafruit MPU6050** (jala **Adafruit Unified Sensor** y **Adafruit BusIO**)

## 2. Conexiones (ESP32 DevKit v1)
```
MAX30102  SDA→GPIO21  SCL→GPIO22  VIN→3V3  GND→GND
MPU6050   SDA→GPIO21  SCL→GPIO22  VCC→3V3  GND→GND   (bus I2C compartido)
Motor vib GPIO13 → base 2N2222 (R1kΩ); colector→motor→5V; emisor→GND; diodo flyback sobre motor
Botón SOS GPIO14 → GND    (usa INPUT_PULLUP; mantener 3s dispara SOS)
```

## 3. Flashear
1. Abrir `esp32_wearable/esp32_wearable.ino`.
2. Tools → Board → **ESP32 Dev Module**; Port → el COM del ESP32.
3. Upload. Abrir Serial Monitor a **115200** para ver los JSON de biométricos.

## 4. Probar sin frontend (backup de demo)
1. Abrir `test_webbluetooth.html` en **Chrome o Edge de escritorio** (Web Bluetooth no va en Firefox).
   - Debe servirse por `https://` o `file://` con flag; lo más simple: abrir el archivo directo o
     `python -m http.server` y entrar por `http://localhost`.
2. Clic **Conectar** → elegir `Wearable-DonJose`.
3. Poner el dedo en el MAX30102 → aparece FC. Mover el sensor → suben pasos.
4. Clic **Enviar recordatorio** → el motor vibra 2s.
5. Mantener el botón SOS 3s → aparece "SOS ACTIVADO".

**Grabar este flujo en video** como respaldo por si la BLE falla en vivo.

## 5. Integración con el frontend (tarea F5)
Los UUIDs y el formato JSON del firmware coinciden con `test_webbluetooth.html`. El frontend
reutiliza esa misma lógica de Web Bluetooth: suscribirse a BIO (FC/pasos/actividad), a SOS
(alerta), y escribir en CMD `{"cmd":"remind"}` para el recordatorio háptico. Opcional: reenviar
los biométricos al backend (`POST` a un endpoint de ingesta) para alimentar el Gemelo Cognitivo.

## Notas
- SpO2 no incluido (el algoritmo del MAX30102 es más pesado); la FC basta para la demo. Ampliable
  con `spo2_algorithm.h` si sobra tiempo.
- Detección de caída = pico >2.5g (simple). Suficiente para demo; refinar con ventana de
  inmovilidad posterior si hay tiempo.
- Ruta alternativa Arduino Uno Q (visión) en `docs/hardware/hardware-guide.md §B`.
