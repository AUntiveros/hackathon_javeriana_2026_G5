import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * F5 — Wearable ESP32 vía Web Bluetooth.
 * Contrato BLE (hardware-guide.md): servicio con 3 características —
 * notify biométricos JSON {"hr":72,"steps":1240,"act":"sedentary"},
 * notify SOS, write comando {"cmd":"remind"} (vibración 2s).
 *
 * UUIDs definidos AQUÍ como contrato; el firmware (H1) debe usar los mismos.
 * Sin hardware o sin Web Bluetooth (Firefox, iOS) → modo simulador.
 */

export const BLE_SERVICE_UUID = '4fa4f8a0-9c0a-4f4e-b0aa-91b0d6a1e001';
export const BLE_CHAR_BIO_UUID = '4fa4f8a0-9c0a-4f4e-b0aa-91b0d6a1e002';
export const BLE_CHAR_SOS_UUID = '4fa4f8a0-9c0a-4f4e-b0aa-91b0d6a1e003';
export const BLE_CHAR_CMD_UUID = '4fa4f8a0-9c0a-4f4e-b0aa-91b0d6a1e004';

export type ModoWearable = 'desconectado' | 'ble' | 'simulador';

export interface EstadoWearable {
  modo: ModoWearable;
  fc: number;
  pasos: number;
  actividad: string;
  sos: boolean;
  error: string | null;
  bleDisponible: boolean;
  conectarBle: () => Promise<void>;
  iniciarSimulador: () => void;
  desconectar: () => void;
  enviarRecordatorio: () => Promise<void>;
  vibrando: boolean;
  descartarSos: () => void;
}

export function useWearable(): EstadoWearable {
  const [modo, setModo] = useState<ModoWearable>('desconectado');
  const [fc, setFc] = useState(0);
  const [pasos, setPasos] = useState(0);
  const [actividad, setActividad] = useState('—');
  const [sos, setSos] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [vibrando, setVibrando] = useState(false);

  const simRef = useRef<number | null>(null);
  const cmdCharRef = useRef<BluetoothRemoteGATTCharacteristicLike | null>(null);
  const deviceRef = useRef<BluetoothDeviceLike | null>(null);

  const bleDisponible = Boolean(navigator.bluetooth);

  const limpiar = useCallback(() => {
    if (simRef.current) {
      clearInterval(simRef.current);
      simRef.current = null;
    }
    deviceRef.current?.gatt?.disconnect();
    deviceRef.current = null;
    cmdCharRef.current = null;
  }, []);

  useEffect(() => limpiar, [limpiar]);

  const desconectar = useCallback(() => {
    limpiar();
    setModo('desconectado');
    setFc(0);
    setPasos(0);
    setActividad('—');
  }, [limpiar]);

  // ---------- BLE real ----------

  const conectarBle = useCallback(async () => {
    setError(null);
    if (!navigator.bluetooth) {
      setError('Este navegador no soporta Web Bluetooth (usa Chrome/Edge).');
      return;
    }
    try {
      const device = await navigator.bluetooth.requestDevice({
        filters: [{ services: [BLE_SERVICE_UUID] }],
      });
      deviceRef.current = device;
      const server = await device.gatt!.connect();
      const servicio = await server.getPrimaryService(BLE_SERVICE_UUID);

      const bio = await servicio.getCharacteristic(BLE_CHAR_BIO_UUID);
      await bio.startNotifications();
      bio.addEventListener('characteristicvaluechanged', (e: Event) => {
        const dv = (e.target as BluetoothRemoteGATTCharacteristicLike).value;
        if (!dv) return;
        try {
          const json = JSON.parse(new TextDecoder().decode(dv.buffer as ArrayBuffer));
          if (typeof json.hr === 'number') setFc(json.hr);
          if (typeof json.steps === 'number') setPasos(json.steps);
          if (typeof json.act === 'string') setActividad(json.act);
        } catch {
          /* frame malformado: ignorar */
        }
      });

      const sosChar = await servicio.getCharacteristic(BLE_CHAR_SOS_UUID);
      await sosChar.startNotifications();
      sosChar.addEventListener('characteristicvaluechanged', () => setSos(true));

      cmdCharRef.current = await servicio.getCharacteristic(BLE_CHAR_CMD_UUID);

      device.addEventListener('gattserverdisconnected', () => desconectar());
      setModo('ble');
    } catch (e) {
      setError(e instanceof Error ? e.message : 'No se pudo conectar al wearable.');
    }
  }, [desconectar]);

  // ---------- simulador ----------

  const iniciarSimulador = useCallback(() => {
    limpiar();
    setError(null);
    setModo('simulador');
    let steps = 1240;
    let t = 0;
    setFc(72);
    setPasos(steps);
    setActividad('caminando');
    simRef.current = window.setInterval(() => {
      t += 1;
      setFc(70 + Math.round(Math.sin(t / 3) * 4 + Math.random() * 3));
      steps += Math.round(Math.random() * 6);
      setPasos(steps);
      setActividad(t % 10 < 7 ? 'caminando' : 'sedentario');
    }, 1500);
  }, [limpiar]);

  // ---------- comando recordatorio ----------

  const enviarRecordatorio = useCallback(async () => {
    setVibrando(true);
    setTimeout(() => setVibrando(false), 2000);
    if (modo === 'ble' && cmdCharRef.current) {
      try {
        await cmdCharRef.current.writeValue(new TextEncoder().encode('{"cmd":"remind"}'));
      } catch (e) {
        setError(e instanceof Error ? e.message : 'No se pudo enviar el comando.');
      }
    }
    // en simulador solo se muestra el feedback visual
  }, [modo]);

  const descartarSos = useCallback(() => setSos(false), []);

  return {
    modo,
    fc,
    pasos,
    actividad,
    sos,
    error,
    bleDisponible,
    conectarBle,
    iniciarSimulador,
    desconectar,
    enviarRecordatorio,
    vibrando,
    descartarSos,
  };
}
