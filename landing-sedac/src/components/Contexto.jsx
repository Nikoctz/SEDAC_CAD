import { useEffect, useRef } from 'react';

export default function Contexto() {
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
      { threshold: 0.15 }
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return (
    <section className="section-section bg-sedac-paper" aria-labelledby="contexto-title">
      <div className="wrap max-w-7xl mx-auto px-6 lg:px-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16">
          {/* left: propuesta */}
          <div className="lg:col-span-6 reveal" data-reveal="contexto-copy">
            <p className="eyebrow mb-6">El problema</p>
            <h2 id="contexto-title" className="display mb-5" style={{ color: 'var(--sedac-ink)', fontFamily: 'var(--font-display)', fontWeight: '700', letterSpacing: '-0.02em', lineHeight: '1.02' }}>
              La bolsa de agua tiene su propio peso. El equipo, el resto.
            </h2>
            <p className="lead" style={{ color: 'var(--sedac-muted)' }}>
              SEDAC no reemplaza la mochila de agua. Es un sistema auxiliar desmontable que se adjunta al
              equipo del bombero forestal para dar a la bolsa un soporte dedicado: estructura, contacto con
              el cuerpo y soporte textil, pensados para acompañar el movimiento sin agregar inercia innecesaria.
            </p>
            <p className="mt-4 text-[15px] leading-relaxed text-sedac-muted max-w-[42ch]">
              Mientras el producto sigue en desarrollo, lo que sí es verificable es la arquitectura elegida y
              los materiales que la componen. No hay clientes, ni alianzas confirmadas, ni resultados de
              ensayo que publicar. Lo que vemos aquí es el diseño en su estado actual.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <a
                href="#diseno"
                className="flex items-center gap-2 rounded-full border border-sedac-line-dark px-6 py-3 text-sm font-medium text-sedac-ink transition hover:border-accent hover:text-accent"
              >
                Ver arquitectura
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </a>
            </div>
          </div>

          {/* right: dataset de confianza */}
          <div className="lg:col-span-6 reveal reveal-delay-1" data-reveal="contexto-numbers">
            <div className="grid grid-cols-2 gap-4">
              {[
                {
                  k: 'Versión de referencia',
                  v: 'P2.04',
                  sub: 'prediseño vigente',
                },
                {
                  k: 'Material principal',
                  v: '6061-T6',
                  sub: 'canales y uniones',
                },
                {
                  k: 'Contacto con el usuario',
                  v: 'HDPE + textil',
                  sub: 'sin resistencia estructural asignada',
                },
                {
                  k: 'Estado del producto',
                  v: 'en desarrollo',
                  sub: 'pendiente validar físicamente',
                },
              ].map((row, i) => (
                <div
                  key={row.k}
                  className={`bg-sedac-paper-2 rounded-xl border border-sedac-line p-5 transition-transform duration-700 hover:border-accent/40 hover:shadow-sm hover:-translate-y-0.5 ${
                    i % 2 === 0 ? 'col-start-1 row-start-1' : 'col-start-2 row-start-1'
                  }`}
                  style={{ opacity: 'var(--ctx-opacity, 0)', transform: 'var(--ctx-y, translateY(18px))' }}
                  data-i={i}
                >
                  <p className="text-[11px] uppercase tracking-[0.18em] text-sedac-muted font-medium">{row.k}</p>
                  <p className="mt-2 text-2xl font-semibold text-sedac-ink" style={{ fontFamily: 'var(--font-display)', fontWeight: '600' }}>{row.v}</p>
                  <p className="mt-1 text-sm text-sedac-muted">{row.sub}</p>
                </div>
              ))}
            </div>

            <p className="mt-6 text-xs text-sedac-muted/70 max-w-[34ch]">
              Los valores mostrados son del estado del proyecto, no de un producto entregado o certificado.
              No se incluyen cifras de usuarios, instituciones ni avales.
            </p>
          </div>
        </div>
      </div>

      <style>{`
        [data-reveal="contexto-copy"],
        [data-reveal="contexto-numbers"] {
          opacity: 0;
          transform: translateY(18px);
          transition: opacity 0.7s ease, transform 0.7s ease;
        }
        [data-reveal="contexto-copy"][data-visible="true"],
        [data-reveal="contexto-numbers"][data-visible="true"] {
          opacity: 1;
          transform: none;
        }
      `}</style>
    </section>
  );
}
