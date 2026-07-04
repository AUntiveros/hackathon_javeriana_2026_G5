import './nino.css';

export type NinoMood = 'idle' | 'listening' | 'thinking' | 'happy' | 'concerned' | 'sleeping';

export interface NinoProps {
  /** Estado emocional del robot */
  mood?: NinoMood;
  /** true mientras Nino reproduce voz (anima la boca) */
  speaking?: boolean;
  /** Ancho en px o unidad CSS (alto se ajusta solo) */
  size?: number | string;
  className?: string;
}

/**
 * Nino — mascota robot kawaii del ecosistema de cuidado.
 * SVG inline animado por CSS. Sin dependencias.
 */
export default function Nino({
  mood = 'idle',
  speaking = false,
  size = 260,
  className = '',
}: NinoProps) {
  const width = typeof size === 'number' ? `${size}px` : size;

  return (
    <div
      className={`nino nino--${mood} ${speaking ? 'nino--speaking' : ''} ${className}`}
      style={{ width }}
      role="img"
      aria-label={`Nino está ${MOOD_LABEL[mood]}${speaking ? ' y hablando' : ''}`}
    >
      <svg viewBox="0 0 260 290" className="nino__svg">
        {/* ---------- sombra ---------- */}
        <ellipse className="nino__shadow" cx="130" cy="272" rx="62" ry="10" fill="#E8D5C4" />

        {/* ---------- todo el cuerpo (respira) ---------- */}
        <g className="nino__all">
          {/* ondas de escucha */}
          <g className="nino__waves" stroke="#F4A261" strokeWidth="6" fill="none" strokeLinecap="round">
            <path className="nino__wave nino__wave--1" d="M28 105 q -10 15 0 30" />
            <path className="nino__wave nino__wave--2" d="M14 95 q -16 25 0 50" />
            <path className="nino__wave nino__wave--1" d="M232 105 q 10 15 0 30" />
            <path className="nino__wave nino__wave--2" d="M246 95 q 16 25 0 50" />
          </g>

          {/* zzz de dormido */}
          <g className="nino__zzz" fill="#B9A99B" fontFamily="inherit" fontWeight="800">
            <text className="nino__z nino__z--1" x="196" y="46" fontSize="20">z</text>
            <text className="nino__z nino__z--2" x="214" y="32" fontSize="26">z</text>
            <text className="nino__z nino__z--3" x="236" y="18" fontSize="32">z</text>
          </g>

          {/* burbuja de pensamiento */}
          <g className="nino__thoughts">
            <circle className="nino__dot nino__dot--1" cx="196" cy="38" r="7" fill="#F4A261" />
            <circle className="nino__dot nino__dot--2" cx="218" cy="30" r="9" fill="#F4A261" />
            <circle className="nino__dot nino__dot--3" cx="241" cy="24" r="11" fill="#F4A261" />
          </g>

          {/* ---------- cuerpo ---------- */}
          <g className="nino__body">
            {/* brazos */}
            <g className="nino__arm nino__arm--left">
              <rect x="52" y="196" width="26" height="46" rx="13" fill="#FFD9B3" stroke="#5C4B44" strokeWidth="5" />
            </g>
            <g className="nino__arm nino__arm--right">
              <rect x="182" y="196" width="26" height="46" rx="13" fill="#FFD9B3" stroke="#5C4B44" strokeWidth="5" />
            </g>

            {/* torso */}
            <rect x="76" y="186" width="108" height="76" rx="34" fill="#FFF6EC" stroke="#5C4B44" strokeWidth="5" />
            {/* panel corazón */}
            <path
              className="nino__heart"
              d="M130 232 c -4 -7 -16 -8 -16 2 c 0 7 10 12 16 16 c 6 -4 16 -9 16 -16 c 0 -10 -12 -9 -16 -2 z"
              fill="#F28B82"
              stroke="#5C4B44"
              strokeWidth="4"
              strokeLinejoin="round"
            />
            {/* pies */}
            <rect x="92" y="252" width="32" height="18" rx="9" fill="#FFD9B3" stroke="#5C4B44" strokeWidth="5" />
            <rect x="136" y="252" width="32" height="18" rx="9" fill="#FFD9B3" stroke="#5C4B44" strokeWidth="5" />
          </g>

          {/* ---------- cabeza ---------- */}
          <g className="nino__head">
            {/* antena */}
            <g className="nino__antenna">
              <line x1="130" y1="34" x2="130" y2="18" stroke="#5C4B44" strokeWidth="5" strokeLinecap="round" />
              <circle className="nino__antenna-bulb" cx="130" cy="13" r="9" fill="#FFC85C" stroke="#5C4B44" strokeWidth="4" />
            </g>

            {/* orejitas */}
            <rect x="30" y="88" width="18" height="34" rx="9" fill="#F4A261" stroke="#5C4B44" strokeWidth="5" />
            <rect x="212" y="88" width="18" height="34" rx="9" fill="#F4A261" stroke="#5C4B44" strokeWidth="5" />

            {/* cabeza grande redonda */}
            <rect x="42" y="32" width="176" height="150" rx="72" fill="#FFF6EC" stroke="#5C4B44" strokeWidth="5" />

            {/* mechoncito */}
            <path d="M118 34 q 12 -14 24 0" fill="none" stroke="#5C4B44" strokeWidth="5" strokeLinecap="round" />

            {/* ---------- cara ---------- */}
            <g className="nino__face">
              {/* cejas (solo preocupado) */}
              <g className="nino__brows" stroke="#5C4B44" strokeWidth="5" strokeLinecap="round" fill="none">
                <path d="M76 78 q 14 -8 26 2" />
                <path d="M158 80 q 12 -10 26 -2" />
              </g>

              {/* ojos normales (idle / listening / thinking / concerned) */}
              <g className="nino__eyes nino__eyes--open">
                <g className="nino__eye">
                  <ellipse cx="92" cy="106" rx="15" ry="19" fill="#4A3F3A" />
                  <circle cx="97" cy="99" r="5.5" fill="#FFFFFF" />
                  <circle cx="88" cy="112" r="3" fill="#FFFFFF" opacity="0.7" />
                </g>
                <g className="nino__eye">
                  <ellipse cx="168" cy="106" rx="15" ry="19" fill="#4A3F3A" />
                  <circle cx="173" cy="99" r="5.5" fill="#FFFFFF" />
                  <circle cx="164" cy="112" r="3" fill="#FFFFFF" opacity="0.7" />
                </g>
              </g>

              {/* ojos felices ^ ^ */}
              <g className="nino__eyes nino__eyes--happy" stroke="#4A3F3A" strokeWidth="7" strokeLinecap="round" fill="none">
                <path d="M78 108 q 14 -16 28 0" />
                <path d="M154 108 q 14 -16 28 0" />
              </g>

              {/* cachetes */}
              <ellipse className="nino__cheek" cx="70" cy="128" rx="12" ry="8" fill="#FFB3AB" />
              <ellipse className="nino__cheek" cx="190" cy="128" rx="12" ry="8" fill="#FFB3AB" />

              {/* ---------- bocas (una por estado) ---------- */}
              {/* sonrisa suave por defecto */}
              <path
                className="nino__mouth nino__mouth--smile"
                d="M114 138 q 16 12 32 0"
                fill="none"
                stroke="#5C4B44"
                strokeWidth="6"
                strokeLinecap="round"
              />
              {/* boca abierta feliz */}
              <path
                className="nino__mouth nino__mouth--open"
                d="M112 136 q 18 24 36 0 z"
                fill="#5C4B44"
              />
              {/* boca preocupada */}
              <path
                className="nino__mouth nino__mouth--worried"
                d="M116 146 q 14 -10 28 0"
                fill="none"
                stroke="#5C4B44"
                strokeWidth="6"
                strokeLinecap="round"
              />
              {/* boca hablando (elipse que pulsa) */}
              <ellipse className="nino__mouth nino__mouth--talk" cx="130" cy="142" rx="13" ry="10" fill="#5C4B44" />
            </g>
          </g>
        </g>
      </svg>
    </div>
  );
}

const MOOD_LABEL: Record<NinoMood, string> = {
  idle: 'tranquilo',
  listening: 'escuchando',
  thinking: 'pensando',
  happy: 'feliz',
  concerned: 'un poco preocupado',
  sleeping: 'dormido',
};
