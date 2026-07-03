# Smartwatch Nino — PPG (FC/HRV + presión estimada)

Monitoreo **cardiovascular** (para pacientes hipertensos, la mayoría de los pacientes con
Alzheimer). **No evalúa deterioro cognitivo** (respeta la prohibición del hackathon).

## Qué hace
- Mide **FC** y **variabilidad (HRV/RMSSD)** por PPG (MAX30102).
- Envía vitales al backend por WiFi → `POST /vitals` → el backend **estima presión** no invasiva.
- Botón **SOS** + motor **vibrador** para recordatorios hápticos.

## Hardware (reusa el del wearable, ver `docs/hardware/lista-compra.md`)
ESP32 + MAX30102 + motor vibrador (2N2222+R1k+diodo) + botón + power bank.

## Conexiones
```
MAX30102  SDA=21 SCL=22 3V3 GND
Motor vib GPIO13 (via transistor)
Botón SOS GPIO14 -> GND
```

## Configurar y flashear
1. En `smartwatch/smartwatch.ino` editar `WIFI_SSID`, `WIFI_PASS`, `BACKEND` (IP:puerto del backend).
2. Librerías: SparkFun MAX3010x. Placa: ESP32 Dev Module.
3. Flashear; Serial Monitor 115200 muestra `HR=.. HRV=..`.
4. El backend recibe `POST /vitals` y responde con presión estimada + categoría (normal/elevada/hipertensión).

## Integración
- Backend endpoint: `POST /vitals {patient_id, hr, hrv_ms}` → guarda `Vital` + estima presión.
- Dashboard del equipo: `GET /vitals/:id` para la serie; se muestra al médico/cuidador.
- Alternativa sin WiFi: enviar por BLE al celular y que la app haga el POST (reusar patrón Web Bluetooth de `hardware/esp32/test_webbluetooth.html`).

## Roadmap
- Presión por PPG real (modelo entrenado + calibración por paciente); aquí es estimación-concepto.
- AirTag/UWB de larga duración en la correa para ubicación (entrevista: paciente se desorienta al salir).
