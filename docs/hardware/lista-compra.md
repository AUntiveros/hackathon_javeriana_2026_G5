# Lista de compra — prototipado rápido (2 dispositivos)

> Dos dispositivos separados. Los componentes NO se comparten.
> **Uno Q = mini-PC Linux → periféricos USB.** **ESP32 = electrónica → sensores I2C + batería.**

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

## B) ESP32 wearable — biométricos (FC, pasos, SOS, vibración)

| Componente | Imprescindible | Nota |
|---|---|---|
| **ESP32 DevKit v1** (WiFi+BLE) | ✅ | Cerebro del wearable |
| **MAX30102** (GY morado, con regulador) | ✅ | Frecuencia cardíaca / SpO2 (I2C 0x57) |
| **MPU6050** (IMU 6 ejes) | ✅ | Pasos + caída (I2C 0x68, comparte bus) |
| **Motor vibrador** coin/ERM | ✅ | Recordatorio háptico |
| **Transistor 2N2222** + **R 1kΩ** + **diodo 1N4148** | ✅ | Driver del motor (no lo conectes directo al GPIO) |
| **Push button** táctil | ✅ | Botón SOS (mantener 3s) |
| **OLED SSD1306 0.96" I2C** | ⬜ opcional | Mostrar hora / mini-mensaje. Lindo pero no crítico |
| **LiPo 3.7V 500–1000mAh** | ⬜ para portátil | Si no, aliméntalo por power bank/USB y ahorras lo de abajo |
| **TP4056** (módulo de carga LiPo) | ⬜ con LiPo | Carga segura de la batería |
| **MT3608** (step-up a 5V) | ⬜ con LiPo | Solo si algún módulo necesita 5V; el ESP32 va a 3.7V directo |

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

1. **Uno Q:** webcam USB (prestada) + parlante USB + power bank + hub USB. → habilita el wow de visión/voz.
2. **ESP32:** ESP32 + MAX30102 + MPU6050 + motor + transistor + botón + protoboard + jumpers + headers/cautín. → habilita el wearable.
3. Opcionales (OLED, LiPo+TP4056+MT3608): solo si sobra tiempo para hacerlo portátil y bonito.

## Decisiones ya resueltas
- **Cámara:** USB (Logi), NO ESP32-CAM (no encaja limpio en el Uno Q).
- **Mic/parlante:** USB (el Uno Q es Linux).
- **Energía Uno Q:** power bank, NO LiPo+step-up (consume demasiado).
- **Energía ESP32:** power bank/USB basta; LiPo+TP4056+MT3608 solo para versión portátil.
