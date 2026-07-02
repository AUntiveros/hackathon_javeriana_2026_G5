import { useWearable } from '../../hooks/useWearable';
import './wearable-panel.css';

/**
 * F5 — Panel del wearable ESP32: FC + pasos en vivo (BLE o simulador),
 * comando de recordatorio (vibración) y alerta SOS.
 */
export default function WearablePanel() {
  const w = useWearable();

  return (
    <section className="tarjeta wearable">
      <div className="wearable__cabecera">
        <h2>⌚ Wearable de Don José</h2>
        <span className={`wearable__estado wearable__estado--${w.modo}`}>
          {w.modo === 'desconectado' && 'Sin conexión'}
          {w.modo === 'ble' && '● BLE en vivo'}
          {w.modo === 'simulador' && '● Simulador'}
        </span>
      </div>

      {w.sos && (
        <div className="wearable__sos" role="alert">
          🆘 <strong>Botón SOS presionado.</strong> Llama a Don José de inmediato.
          <button onClick={w.descartarSos}>Atendido</button>
        </div>
      )}

      {w.modo === 'desconectado' ? (
        <div className="wearable__conectar">
          <p>Conecta la pulsera para ver frecuencia cardiaca y pasos en vivo.</p>
          <div className="wearable__botones">
            {w.bleDisponible && (
              <button className="wearable__btn" onClick={() => void w.conectarBle()}>
                Conectar por Bluetooth
              </button>
            )}
            <button className="wearable__btn wearable__btn--sec" onClick={w.iniciarSimulador}>
              Modo demo (simulador)
            </button>
          </div>
          {!w.bleDisponible && (
            <p className="wearable__nota">Web Bluetooth no disponible aquí (usa Chrome/Edge de escritorio o Android).</p>
          )}
        </div>
      ) : (
        <>
          <div className="wearable__datos">
            <div className="wearable__dato">
              <span className="wearable__valor wearable__valor--fc">
                {w.fc || '—'} <small>bpm</small>
              </span>
              <span className="wearable__label">❤️ Frec. cardiaca</span>
            </div>
            <div className="wearable__dato">
              <span className="wearable__valor">{w.pasos.toLocaleString('es-PE')}</span>
              <span className="wearable__label">👟 Pasos hoy</span>
            </div>
            <div className="wearable__dato">
              <span className="wearable__valor wearable__valor--txt">{w.actividad}</span>
              <span className="wearable__label">Actividad</span>
            </div>
          </div>

          <div className="wearable__botones">
            <button
              className="wearable__btn"
              onClick={() => void w.enviarRecordatorio()}
              disabled={w.vibrando}
            >
              {w.vibrando ? '📳 Vibrando…' : '🔔 Enviar recordatorio (vibrar)'}
            </button>
            <button className="wearable__btn wearable__btn--sec" onClick={w.desconectar}>
              Desconectar
            </button>
          </div>
        </>
      )}

      {w.error && <p className="wearable__error">{w.error}</p>}
    </section>
  );
}
