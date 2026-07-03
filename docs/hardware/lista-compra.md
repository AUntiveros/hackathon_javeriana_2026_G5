# Lista de compra — prototipado rápido (UN solo dispositivo: Uno Q)

> DECISIÓN 2026-07-02: **todo en el Uno Q** (dual-brain). El ESP32 se descarta como aparato
> separado (queda como roadmap "wrist-band"). El Uno Q hace visión/voz (lado Linux) Y biométricos
> (lado MCU, headers Arduino). Menos plata, sin BLE, menos riesgo en vivo.

---

## A) Arduino Uno Q — visión + voz (es una compu, todo por USB)

| Componente | Imprescindible | Nota |
|---|---|---|
| **Webcam USB** (Logi prestada) | ✅ | Que tenga **micrófono integrado** → resuelve cámara + mic juntos. NO ESP32-CAM. |
| Micrófono USB (solo si la webcam no trae mic) | ⬜ opcional | Mini mic USB, o dongle USB de audio + mic electret |
| **Parlante USB** pequeño (o dongle USB-audio + parlante 3.5mm) | ✅ | Salida de voz del asistente. Plug-and-play en Linux |
| **Power bank USB 5V ≥2A** (10000mAh) + cable USB-C | ✅ | El Uno Q consume mucho para LiPo pequeña → power bank, NO LiPo+step-up |
| **Hub USB** pequeño (2-4 puertos) | ✅ | El Uno Q tiene pocos puertos: cámara + mic + parlante + teclado no entran directo |
| MicroSD (si el modelo lo pide) | ⬜ verificar | El de 2GB suele traer eMMC; confirmar si necesita SD para OS/almacenamiento |
| Para el setup inicial: monitor HDMI + teclado USB **o** acceso headless por WiFi/SSH | ✅ (una vía) | No te quedes sin forma de entrar al Debian la primera vez |

**Regla:** trata el Uno Q como una laptop. Cámara/mic/parlante = USB. Alimentación = power bank.

---

## B) Biométricos — se conectan a los HEADERS ARDUINO del Uno Q (lado MCU)

> Ya NO hay ESP32. Estos módulos se cablean a los pines Arduino del propio Uno Q; el sketch del
> MCU (`hardware/unoq_mcu/`) los lee y manda los datos al Python por el puente serial interno.

| Componente | Imprescindible | Nota |
|---|---|---|
| **MAX30102** (GY morado, con regulador) | ✅ | Frecuencia cardíaca / SpO2 → pines I2C del Uno Q (0x57) |
| **MPU6050** (IMU 6 ejes) | ✅ | Pasos + caída → mismo bus I2C (0x68) |
| **Motor vibrador** coin/ERM | ✅ | Recordatorio háptico → pin D3 |
| **Transistor 2N2222** + **R 1kΩ** + **diodo 1N4148** | ✅ | Driver del motor (no directo al pin) |
| **Push button** táctil | ✅ | Botón SOS → pin D2 (mantener 3s) |
| **OLED SSD1306 0.96" I2C** | ⬜ opcional | Mostrar hora/mensaje en el bracito de sensores |
| ~~ESP32 / LiPo / TP4056 / MT3608~~ | ❌ fuera | El Uno Q se alimenta por power bank (sección A); no hace falta |

---

## C) Común / no te olvides

| Componente | Nota |
|---|---|
| **Protoboard** x1-2 | Montaje sin soldar |
| **Jumpers** M-M, M-H, H-H (surtido) | Varios de cada |
| **Tira de headers (pines) + cautín + estaño** | Los módulos (MAX30102, MPU6050, OLED) vienen **sin pines soldados** → hay que soldarlos |
| **Cable microUSB** (para el ESP32) + **USB-C** (Uno Q) | Datos + energía |
| **Resistencias surtidas** | Por si acaso (pull-ups, etc.) |
| **Multímetro** | Si no tienen; para depurar conexiones/voltajes |

---

## Prioridad si el presupuesto/tiempo aprieta

1. **Uno Q base:** webcam USB (prestada) + parlante USB + power bank + hub USB. → wow de visión/voz.
2. **Biométricos:** MAX30102 + MPU6050 + motor + transistor + diodo + botón + protoboard + jumpers + tira de headers + cautín/estaño. → señales de salud + SOS + vibración.
3. Opcional (OLED): solo si sobra tiempo.

## Decisiones ya resueltas
- **Un solo aparato: el Uno Q** (dual-brain). ESP32 descartado (roadmap wrist-band).
- **Cámara:** USB (Logi), NO ESP32-CAM (no encaja limpio en el Uno Q).
- **Mic/parlante:** USB (el Uno Q es Linux).
- **Energía:** power bank USB, NO LiPo+step-up (el Uno Q consume demasiado).
- **Biométricos:** a los headers Arduino del Uno Q; el sketch MCU los manda al Python por serial.
