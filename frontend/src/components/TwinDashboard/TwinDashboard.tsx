import { useEffect, useState } from 'react';
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { getTwinAlerts, getTwinSnapshot, getTwinTrend, PATIENT_ID } from '../../api/client';
import type { Alerta, Snapshot, TrendPoint } from '../../api/types';
import './twin-dashboard.css';

/* Paleta validada (scripts/validate_palette.js, surface #fff):
   series habla: azul/naranja/aqua ΔE adj 25.0 — aqua <3:1 → direct labels.
   riesgo: rojo #e34948 pasa solo. Status: fijos, con icono+texto. */
const C = {
  riesgo: '#e34948',
  fluidez: '#2a78d6',
  riqueza: '#eb6834',
  pausas: '#1baf7a',
  grid: '#e1e0d9',
  eje: '#898781',
};

const STATUS = {
  info: { color: '#0ca30c', icono: '✓', etiqueta: 'Info' },
  media: { color: '#b57900', icono: '⚠', etiqueta: 'Atención' },
  alta: { color: '#d03b3b', icono: '⛔', etiqueta: 'Urgente' },
} as const;

interface Props {
  /** 'completo' = snapshot + riesgo + habla + alertas · 'resumen' = snapshot + alertas */
  variante?: 'completo' | 'resumen';
}

/** F3 — Dashboard Gemelo Cognitivo: pegamento visual del ecosistema. */
export default function TwinDashboard({ variante = 'completo' }: Props) {
  const [trend, setTrend] = useState<TrendPoint[]>([]);
  const [alertas, setAlertas] = useState<Alerta[]>([]);
  const [snap, setSnap] = useState<Snapshot | null>(null);

  useEffect(() => {
    void getTwinTrend(PATIENT_ID).then(setTrend);
    void getTwinAlerts(PATIENT_ID).then(setAlertas);
    void getTwinSnapshot(PATIENT_ID).then(setSnap);
  }, []);

  if (!snap) return <p className="cargando">Cargando gemelo cognitivo…</p>;

  const datos = trend.map((p) => ({
    ...p,
    riesgo100: +(p.riesgo * 100).toFixed(1),
    dia: p.fecha.slice(8) + '/' + p.fecha.slice(5, 7),
  }));

  const ultimo = datos[datos.length - 1];

  return (
    <div className="twin">
      {/* ---------- snapshot: 4 stat tiles ---------- */}
      <div className="twin__tiles">
        <Tile titulo="Cognitivo" valor={snap.estado_cognitivo.valor} nota={snap.estado_cognitivo.etiqueta} />
        <Tile titulo="Ánimo" valor={snap.estado_emocional.valor} nota={snap.estado_emocional.etiqueta} />
        <Tile titulo="Adherencia" valor={snap.adherencia.valor} nota={snap.adherencia.etiqueta} sufijo="%" />
        <Tile titulo="Riesgo" valor={snap.riesgo.valor} nota={snap.riesgo.etiqueta} alerta />
      </div>

      {variante === 'completo' && (
        <>
          {/* ---------- riesgo 30 días (serie única — sin leyenda) ---------- */}
          <section className="tarjeta twin__chart">
            <h2>Riesgo del habla — 30 días</h2>
            <p className="twin__sub">
              Índice 0–100 del clasificador · hoy: <strong style={{ color: C.riesgo }}>{ultimo?.riesgo100}</strong>
            </p>
            <ResponsiveContainer width="100%" height={180}>
              <LineChart data={datos} margin={{ top: 8, right: 34, bottom: 0, left: -22 }}>
                <CartesianGrid stroke={C.grid} vertical={false} />
                <XAxis dataKey="dia" tick={{ fontSize: 12, fill: C.eje }} tickLine={false} stroke={C.grid} interval={6} />
                <YAxis domain={[35, 60]} tick={{ fontSize: 12, fill: C.eje }} tickLine={false} stroke={C.grid} />
                <Tooltip contentStyle={estiloTooltip} formatter={(v) => [v, 'Riesgo']} />
                <Line
                  type="monotone"
                  dataKey="riesgo100"
                  stroke={C.riesgo}
                  strokeWidth={2}
                  dot={false}
                  activeDot={{ r: 5 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </section>

          {/* ---------- métricas del habla (3 series) ---------- */}
          <section className="tarjeta twin__chart">
            <h2>Métricas del habla — 30 días</h2>
            <p className="twin__sub">Índices 0–100 normalizados al promedio personal</p>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={datos} margin={{ top: 8, right: 12, bottom: 0, left: -22 }}>
                <CartesianGrid stroke={C.grid} vertical={false} />
                <XAxis dataKey="dia" tick={{ fontSize: 12, fill: C.eje }} tickLine={false} stroke={C.grid} interval={6} />
                <YAxis domain={[20, 90]} tick={{ fontSize: 12, fill: C.eje }} tickLine={false} stroke={C.grid} />
                <Tooltip contentStyle={estiloTooltip} />
                <Line type="monotone" dataKey="fluidez" name="Fluidez" stroke={C.fluidez} strokeWidth={2} dot={false} activeDot={{ r: 5 }} />
                <Line type="monotone" dataKey="riqueza_lexica" name="Riqueza léxica" stroke={C.riqueza} strokeWidth={2} dot={false} activeDot={{ r: 5 }} />
                <Line type="monotone" dataKey="pausas" name="Pausas" stroke={C.pausas} strokeWidth={2} dot={false} activeDot={{ r: 5 }} />
              </LineChart>
            </ResponsiveContainer>
            {/* leyenda con valor de hoy: identidad + valor legibles sin depender del color */}
            <ul className="twin__leyenda">
              <li><i style={{ background: C.fluidez }} /> Fluidez · hoy <strong>{ultimo?.fluidez}</strong></li>
              <li><i style={{ background: C.riqueza }} /> Riqueza léxica · hoy <strong>{ultimo?.riqueza_lexica}</strong></li>
              <li><i style={{ background: C.pausas }} /> Pausas · hoy <strong>{ultimo?.pausas}</strong></li>
            </ul>
          </section>
        </>
      )}

      {/* ---------- alertas ---------- */}
      <section className="tarjeta">
        <h2>Alertas</h2>
        <ul className="twin__alertas">
          {alertas.map((a) => {
            const s = STATUS[a.severidad];
            return (
              <li key={a.id} className="twin__alerta" style={{ borderLeftColor: s.color }}>
                <span className="twin__alerta-tag" style={{ color: s.color }}>
                  <span aria-hidden="true">{s.icono}</span> {s.etiqueta} · {a.fecha.slice(8)}/{a.fecha.slice(5, 7)}
                </span>
                <strong>{a.titulo}</strong>
                <p>{a.detalle}</p>
              </li>
            );
          })}
        </ul>
      </section>
    </div>
  );
}

const estiloTooltip = {
  borderRadius: 12,
  border: '2px solid #F1DECB',
  fontSize: 14,
};

function Tile({
  titulo,
  valor,
  nota,
  sufijo = '',
  alerta = false,
}: {
  titulo: string;
  valor: number;
  nota: string;
  sufijo?: string;
  alerta?: boolean;
}) {
  return (
    <div className={`twin__tile ${alerta ? 'twin__tile--alerta' : ''}`}>
      <span className="twin__tile-titulo">{titulo}</span>
      <span className="twin__tile-valor">
        {valor}
        {sufijo}
      </span>
      <span className="twin__tile-nota">{nota}</span>
    </div>
  );
}
