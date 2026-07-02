# Guía de hardware — wearable prototipo

Dos rutas. **ESP32 = ruta segura (comprar).** **Arduino Uno Q = stretch (si lo prestan).**

---

## Ruta A — ESP32 (RECOMENDADA, ~S/ 60-90 total)

### BOM (lista de compra)

| Componente | Para qué | Precio aprox (Perú) |
|---|---|---|
| **ESP32 DevKit v1** (WiFi+BLE) | Cerebro, BLE al navegador | S/ 25-35 |
| **MAX30102** | Frecuencia cardíaca + SpO2 | S/ 12-18 |
| **MPU6050** (IMU 6 ejes) | Pasos, detección de caída, actividad | S/ 8-12 |
| **Motor vibrador** (coin/ERM) + transistor 2N2222 | Recordatorio háptico | S/ 5-8 |
| **Push button** | Botón SOS | S/ 2 |
| Protoboard + jumpers + cable USB | Montaje | S/ 15-20 |
| (Opcional) OLED SSD1306 0.96" | Mostrar hora/mini-chatbot | S/ 12-15 |
| (Opcional) batería LiPo 3.7V + TP4056 | Portátil | S/ 15-20 |

**Comprar en:** tiendas de electrónica (ej. en Lima: Paruro / mercado libre / AliExpress si hay tiempo). Confirmar que el MAX30102 sea el módulo con regulador (versión morada GY-MAX30102).

### Pinout (ESP32 DevKit v1)

```
MAX30102   → SDA=GPIO21, SCL=GPIO22, VIN=3V3, GND=GND   (I2C, dir 0x57)
MPU6050    → SDA=GPIO21, SCL=GPIO22, VCC=3V3, GND=GND   (I2C, dir 0x68, comparte bus)
Motor vib. → base transistor ← GPIO13 (con R 1kΩ); colector→motor→5V; emisor→GND; diodo flyback
Botón SOS  → GPIO14 → GND (INPUT_PULLUP)
OLED (opc) → SDA=GPIO21, SCL=GPIO22
```

### Firmware — lógica (H1)

Librerías: `SparkFun MAX3010x`, `MPU6050` (Electronic Cats o Jeff Rowberg), `BLEDevice` (nativa ESP32), `Adafruit_SSD1306` (opc).

Servicio BLE con 3 características:
- **Notify** biométricos: JSON `{"hr":72,"steps":1240,"act":"sedentary"}` cada 30s.
- **Notify** SOS: al presionar botón 3s → evento de emergencia.
- **Write** comando: navegador escribe `{"cmd":"remind"}` → activa vibración 2s.

Máquina de estados en `docs/diagrams/arquitectura.md §6`. Pasos = algoritmo de conteo por picos del acelerómetro (magnitud > umbral con debounce). Caída = pico de aceleración seguido de inmovilidad.

### Integración
Frontend usa **Web Bluetooth API** (tarea F5) → conecta por UUID del servicio, se suscribe a notify, escribe comando de recordatorio. Chrome/Edge en escritorio soportan Web Bluetooth (Firefox no).

### Backup obligatorio
**Grabar video del ESP32 funcionando** (FC en vivo + vibración al recordar + SOS). Si la BLE falla en la presentación en vivo, se muestra el video. Nunca depender solo del demo en vivo del hardware.

---

## Ruta B — Arduino Uno Q (STRETCH, solo si lo prestan)

El **Arduino Uno Q** (Qualcomm Dragonwing) corre Linux + tiene MPU de aplicaciones → puede correr modelos de visión on-device. Habilita el demo de **smart glasses: "¿qué estoy viendo?"**

- **Objeto:** cámara USB/CSI + modelo ligero de detección (YOLOv8n o MobileNet-SSD) → responde "estás viendo tu taza / tus lentes / tu medicina".
- **Reconocimiento facial (opc):** `face_recognition` (dlib) entrenado con fotos de la familia → "te está hablando Sofía, tu nieta".
- **Flujo:** foto → inferencia local → texto → TTS. Se conecta al backend por WiFi para loguear el evento en el Gemelo.
- **Riesgo:** setup Linux + drivers de cámara consume tiempo. Solo abordar si ESP32 ya está cerrado y sobra un día.
- **Decisión:** si NO llega el Uno Q, las smart glasses quedan en **Capa C (roadmap en slides)** con los papers de respaldo (ESP32-CAM George et al. 2025, patente US 12,191,035).

---

## Regla de decisión de hardware

```
¿Prestan Arduino Uno Q a tiempo (día 1)?
   SÍ  → ESP32 (wearable, seguro) + Uno Q (gafas visión, wow) en paralelo
   NO  → Solo ESP32; gafas = roadmap Capa C en slides
```
