import './familiar.css';

/**
 * F4 — Vista Familiar: estado general + sugerencia de contacto + temas
 * (scope RBAC: sin datos clínicos — privacidad del paciente).
 */
export default function FamiliarView() {
  return (
    <div className="vista">
      <section className="tarjeta familiar__estado">
        <span className="familiar__emoji" aria-hidden="true">😊</span>
        <div>
          <h2>Tu papá está bien hoy</h2>
          <p>Durmió tranquilo, desayunó completo y estuvo conversador con Tito.</p>
        </div>
      </section>

      <section className="tarjeta">
        <h2>📞 Buen momento para llamarlo</h2>
        <p className="familiar__destacado">Hoy entre 4 y 6 de la tarde</p>
        <p>Después de su siesta suele estar más animado y con ganas de conversar.</p>
        <a className="familiar__llamar" href="tel:+51999999999">Llamar ahora</a>
      </section>

      <section className="tarjeta">
        <h2>💡 Temas que le encantan esta semana</h2>
        <ul className="familiar__temas">
          <li>🎵 Los valses de Chabuca Granda — estuvo cantando ayer</li>
          <li>🌱 Su chacra: pregúntale por la cosecha de papa</li>
          <li>⚽ El mundial del 70 — lo cuenta con detalles</li>
        </ul>
        <p className="familiar__tip">
          Tip: no le preguntes "¿te acuerdas de mí?". Salúdalo diciendo tu nombre: <em>"Hola papá, soy Rosa"</em>.
        </p>
      </section>
    </div>
  );
}
