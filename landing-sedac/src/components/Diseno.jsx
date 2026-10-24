import { useEffect, useRef } from 'react';

export default function Diseno() {
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
    <section className="section-section bg-sedac-paper" aria-labelledby="diseno-title" id="diseno">
      <div className="wrap max-w-7xl mx-auto px-6 lg:px-10">
        <div className="max-w-3xl reveal" data-reveal="diseno-head">
          <p className="eyebrow mb-4">Arquitectura · materiales · ajuste</p>
          <h2
            id="diseno-title"
            className="display mb-5"
            style={{ color: 'var(--sedac-ink)', fontFamily: 'var(--font-display)', fontWeight: '700', letterSpacing: '-0.02em', lineHeight: '1.02' }}
          >
            Diseño para
            <br />
            <em className="text-accent">no resistir solo</em>
            <br />
            a la bolsa de agua.
          </h2>
          <p className="lead" style={{ color: 'var(--sedac-muted)' }}>
            El conjunto se organiza en tres entornos: una estructura que recorre y separa, un contacto que
            ampara y protege, y un soporte textil que acompaña la bolsa. Los objetivos siguientes se formulan
            como intenciones aún por ensayar.
          </p>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 reveal" data-reveal="diseno-grid">
          {/* bloque 1: estructura — grande, sin selector de tarjetas iguales */}
          <article className="md:col-span-2 relative rounded-2xl border border-sedac-line bg-white p-8 hover:border-accent/50 transition-colors group overflow-hidden">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-[11px] tracking-[0.18em] uppercase text-accent mb-2 font-semibold">Estructura</p>
                <h3 className="h3 mb-3" style={{ color: 'var(--sedac-ink)', fontFamily: 'var(--font-display)', fontWeight: '700' }}>
                  Dos canales abiertos, no una sola pieza.
                </h3>
                <p className="text-sm leading-relaxed text-sedac-muted max-w-[46ch]">
                  Canales de aluminio 6061-T6, 32 × 24 × 3 mm y 480 mm de largo, separados 190 mm y con la
                  cara abierta hacia la bolsa. La continuidad de material se conserva donde entran las fuerzas;
                  el material se retira en la interfaz lumbar, los yugos y el panel de contacto.
                </p>
              </div>
              <div className="flex-none w-14 h-14 rounded-full bg-accent/10 flex items-center justify-center text-accent">
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round">
                  <path d="M4 19 L9 5 L14 19 L19 5" />
                  <path d="M9 5 L14 19" strokeOpacity="0.4" />
                </svg>
              </div>
            </div>

            <div className="mt-6 grid grid-cols-2 gap-4 text-left">
              {[
                { k: 'Longitud nominal', v: '480 mm' },
                { k: 'Separación entre canales', v: '190 mm' },
                { k: 'Sección del canal', v: '32 × 24 × 3 mm' },
                { k: 'Material de carga', v: '6061-T6' },
              ].map((row) => (
                <div key={row.k} className="border-t border-sedac-line pt-4">
                  <p className="text-[11px] tracking-[0.1em] uppercase text-sedac-muted">{row.k}</p>
                  <p className="mt-0.5 text-base font-semibold text-sedac-ink" style={{ fontFamily: 'var(--font-display)' }}>
                    {row.v}
                  </p>
                </div>
              ))}
            </div>
          </article>

          {/* bloque 2: contacto */}
          <article className="rounded-2xl border border-sedac-line bg-white p-8 hover:border-accent/50 transition-colors group">
            <p className="text-[11px] tracking-[0.18em] uppercase text-accent mb-3 font-semibold">Contacto con el usuario</p>
            <h3 className="h3 mb-3" style={{ color: 'var(--sedac-ink)', fontFamily: 'var(--font-display)', fontWeight: '700' }}>
              Amparar, no solo ponerse entre el cuerpo y la carga.
            </h3>
            <p className="text-sm leading-relaxed text-sedac-muted max-w-[30ch]">
              Panel HDPE de 1 mm, recortado para ventilación y pequeña flexión, que distribuye el contacto sin
              recibir carga estructural. Láminas de acabado y bordes protegidos completan el entorno de contacto.
            </p>
            <p className="mt-4 text-sm text-sedac-muted">
              Textiles y acolchados se representan para edición; patrones, costuras y ajuste antropométrico
              siguen pendientes.
            </p>
          </article>

          {/* bloque 3: soporte textil */}
          <article className="rounded-2xl border border-sedac-line bg-white p-8 hover:border-accent/50 transition-colors group">
            <p className="text-[11px] tracking-[0.18em] uppercase text-accent mb-3 font-semibold">Soporte textil</p>
            <h3 className="h3 mb-3" style={{ color: 'var(--sedac-ink)', fontFamily: 'var(--font-display)', fontWeight: '700' }}>
              Acompañar la bolsa y no atarla.
            </h3>
            <p className="text-sm leading-relaxed text-sedac-muted max-w-[30ch]">
              Cuna y cintas representadas para edición. Correas transversales para limitar el desplazamiento
              lateral; ajuste, protección de costuras y eficacia con agua en movimiento por confirmar.
            </p>
          </article>

          {/* bloque 4: objetivos — editorial, asimétrico */}
          <article className="md:col-span-2 relative rounded-2xl border border-sedac-line bg-sedac-graphite p-8 text-sedac-paper hover:border-accent/40 transition-colors">
            <div className="flex gap-6 items-start">
              <div className="flex-none w-12 h-12 rounded-full bg-accent/10 flex items-center justify-center text-accent">
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M3 12h4l2 7 4-14 2 7h4" />
                </svg>
              </div>
              <div>
                <p className="text-[11px] tracking-[0.18em] uppercase text-accent mb-2 font-semibold">Objetivos de diseño</p>
                <h3 className="h3 mb-3" style={{ color: 'var(--sedac-paper)', fontFamily: 'var(--font-display)', fontWeight: '700' }}>
                  Reducir masa añadida, facilitar el ajuste y acompañar el movimiento.
                </h3>
                <p className="text-sm leading-relaxed opacity-80 max-w-[58ch]">
                  Estas son intenciones de diseño pendientes de ensayo físico. No representan resultados
                  medidos ni mejoras comprobadas de salud o seguridad. La bolsa de agua no está modelada en
                  las vistas actuales.
                </p>
              </div>
            </div>
          </article>

          {/* bloque 5: uniones */}
          <article className="rounded-2xl border border-sedac-line bg-white p-8 hover:border-accent/50 transition-colors group">
            <p className="text-[11px] tracking-[0.18em] uppercase text-accent mb-3 font-semibold">Uniones desmontables</p>
            <h3 className="h3 mb-3" style={{ color: 'var(--sedac-ink)', fontFamily: 'var(--font-display)', fontWeight: '700' }}>
              Ocho uniones, tornillo, arandela y pasador hueco.
            </h3>
            <p className="text-sm leading-relaxed text-sedac-muted max-w-[30ch]">
              Tornillo M5×55, dos arandelas gruesas y tuerca autofrenante por unión; pasador hueco extraíble de
              6061-T6 y separador interno que mantiene las alas abiertas durante el apriete.
            </p>
          </article>
        </div>

        {/* nota de integridad visual */}
        <p className="mt-8 text-xs text-sedac-muted italic max-w-3xl">
          Las vistas provienen del CAD vigente P2.04 y conservan sus proporciones; no son fotografías de un
          producto fabricado y no muestran una bolsa de agua instalada.
        </p>
      </div>

      <style>{`
        [data-reveal="diseno-head"], [data-reveal="diseno-grid"] {
          opacity: 0;
          transform: translateY(18px);
          transition: opacity 0.7s cubic-bezier(0.22,1,0.36,1), transform 0.7s cubic-bezier(0.22,1,0.36,1);
        }
        [data-reveal="diseno-head"].is-in, [data-reveal="diseno-grid"].is-in {
          opacity: 1;
          transform: none;
        }
      `}</style>
    </section>
  );
}
