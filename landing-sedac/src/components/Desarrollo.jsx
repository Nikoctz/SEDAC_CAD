import { useEffect, useRef } from 'react';

export default function Desarrollo() {
  const ref = useRef(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.dataset.visible = 'true';
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return (
    <section className="section-section bg-sedac-graphite text-sedac-paper" aria-labelledby="desarrollo-title" id="evaluacion">
      <div className="wrap max-w-7xl mx-auto px-6 lg:px-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16">
          {/* left: estado de desarrollo */}
          <div className="lg:col-span-7 reveal" data-reveal="desarrollo-copy">
            <p className="eyebrow text-amber-400/80 mb-6">Estado de desarrollo</p>
            <h2
              id="desarrollo-title"
              className="display text-white mb-5"
              style={{ fontFamily: 'var(--font-display)', fontWeight: '700', letterSpacing: '-0.02em', lineHeight: '1.02' }}
            >
              Un producto con
              <br />
              <em className="text-amber-400">dirección definida</em>
              <br />
              y trabajo pendiente.
            </h2>
            <p className="lead text-white/70 mb-6" style={{ color: 'rgba(247,244,236,0.78)', maxWidth: '42ch' }}>
              La referencia vigente del producto real es P2.04. P2.05 sigue abierta y OPT1 no fue adoptada.
              No hay un prototipo fabricado ni ensayos publicados que respalden afirmaciones de rendimiento
              o seguridad.
            </p>
            <p className="text-sm text-white/60 leading-relaxed max-w-[42ch]">
              Lo que sí está determinado es la arquitectura elegida, los materiales que la componen y los
              objetivos pendientes de ensayo. Por encima de todo, queremos conversar con brigadas, instituciones
              y responsables de equipamiento para entender necesidades y explorar colaboraciones o evaluaciones
              futuras.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <button
                type="button"
                onClick={() => {}}
                className="btn gap-2 py-3 px-6 bg-amber-400 text-sedac-graphite hover:bg-amber-300"
              >
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                </svg>
                Conversemos sobre tu equipo
              </button>
            </div>
          </div>

          {/* right: etapas */}
          <div className="lg:col-span-5 reveal reveal-delay-1" data-reveal="desarrollo-stages">
            <div className="bg-sedac-graphite-2 rounded-2xl border border-sedac-line-light p-6">
              <p className="text-[11px] tracking-[0.18em] uppercase text-amber-400/80 mb-6 font-semibold">Hitos visibles</p>
              <div className="grid grid-cols-2 gap-6">
                {[
                  { title: 'Prediseño CAD', state: 'vigente', note: 'P2.04 como base actual' },
                  { title: 'Prototipo físico', state: 'por definir', note: 'no hay fabricación publicada' },
                  { title: 'Ensayos de carga', state: 'pendiente', note: 'no hay resultados de ensayo' },
                  { title: 'Validación IMU', state: 'por planificar', note: 'sección explicativa, no medición' },
                ].map((stage) => (
                  <div key={stage.title} className="relative pl-7 pb-6 border-b border-sedac-line-light last:border-0 last:pb-0">
                    <span
                      className={`absolute left-0 top-1.5 w-3.5 h-3.5 rounded-full border-2 border-current ${
                        stage.state === 'vigente' ? 'bg-amber-400 border-amber-400' : 'bg-transparent border-white/30'
                      }`}
                    />
                    <p className="text-sm font-medium text-white/90 mb-1" style={{ fontFamily: 'var(--font-display)', fontWeight: '600' }}>
                      {stage.title}
                    </p>
                    <p className="text-xs text-white/50">{stage.note}</p>
                  </div>
                ))}
              </div>
              <p className="mt-6 text-xs text-white/40 max-w-[30ch]">
                Los estados son informativos y reflejan el progreso del proyecto, no promesas de fecha ni
                entrega.
              </p>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        [data-reveal="desarrollo-copy"], [data-reveal="desarrollo-stages"] {
          opacity: 0;
          transform: translateY(18px);
          transition: opacity 0.7s cubic-bezier(0.22,1,0.36,1), transform 0.7s cubic-bezier(0.22,1,0.36,1);
        }
        [data-reveal="desarrollo-copy"].is-in, [data-reveal="desarrollo-stages"].is-in {
          opacity: 1;
          transform: none;
        }
      `}</style>
    </section>
  );
}
