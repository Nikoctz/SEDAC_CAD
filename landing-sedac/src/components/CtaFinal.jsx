import { useEffect, useRef } from 'react';

export default function CtaFinal({ onRequestPresentation }) {
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
    <section
      className="section dark relative overflow-hidden"
      aria-labelledby="cta-title"
      id="cta-final"
      style={{ background: 'var(--graphite)' }}
    >
      {/* ambiente */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden" aria-hidden="true">
        <div className="absolute top-[-10%] right-[-8%] w-[60%] h-[60%] rounded-full bg-amber-500/10 blur-[140px]" />
        <div className="absolute bottom-[-12%] left-[-6%] w-[50%] h-[50%] rounded-full bg-amber-600/8 blur-[100px]" />
      </div>

      <div className="wrap max-w-7xl mx-auto px-6 lg:px-10 relative z-10" ref={ref}>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16 items-center">
          {/* copy */}
          <div className="lg:col-span-6 reveal" data-reveal="cta-copy">
            <p className="eyebrow text-amber-400/80 mb-5">Cierre</p>
            <h2
              id="cta-title"
              className="display text-white mb-5"
              style={{ color: 'var(--paper)', fontFamily: 'var(--font-display)', fontWeight: '700', letterSpacing: '-0.02em', lineHeight: '1.02' }}
            >
              ¿Tu equipo está listo
              <br />
              para <em className="text-amber-400">explorar</em> SEDAC?
            </h2>
            <p className="lead text-white/70 mb-8" style={{ color: 'rgba(247,244,236,0.8)', maxWidth: '40ch' }}>
              Si estás buscando entender cómo un sistema auxiliar puede acompañar tu mochila de agua, te
              invitamos a preparar una solicitud y conversar. Sin prisa, sin inventar lo que aún no existe.
            </p>
            <div className="flex flex-wrap gap-4">
              <button
                type="button"
                onClick={onRequestPresentation}
                className="group inline-flex items-center gap-2.5 rounded-full bg-amber-400 px-8 py-4 text-sm font-semibold text-sedac-graphite shadow-2xl shadow-amber-600/25 transition hover:bg-amber-300 hover:-translate-y-0.5 active:scale-[0.97]"
              >
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M5 12h14M13 6l6 6-6 6" />
                </svg>
                Solicitar presentación
              </button>
              <a
                href="#preguntas"
                className="group inline-flex items-center gap-2.5 rounded-full border border-white/20 px-8 py-4 text-sm font-medium text-white/90 transition hover:border-amber-400 hover:text-amber-400 hover:-translate-y-0.5"
              >
                Preguntas Frequentes
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                  <path d="M7 13l5 5 5-5M7 6l5 5 5-5" />
                </svg>
              </a>
            </div>
            <p className="mt-6 text-xs text-white/40 max-w-[34ch]">
             Producto en desarrollo · prediseño CAD · validación física pendiente.
            </p>
          </div>

          {/* checklist visual */}
          <div className="lg:col-span-6 reveal reveal-delay-1" data-reveal="cta-list">
            <div className="bg-sedac-graphite-2 rounded-2xl border border-sedac-line-light p-6">
              <p className="text-[11px] tracking-[0.18em] uppercase text-amber-400/80 mb-5 font-semibold">Navegación útil</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {[
                  { label: 'Sistema', href: '#sistema', desc: 'Visor interactivo del producto' },
                  { label: 'Diseño', href: '#diseno', desc: 'Arquitectura, materiales y uniones' },
                  { label: 'Evaluación', href: '#evaluacion', desc: 'Sensores IMU y movimiento previsto' },
                  { label: 'Preguntas', href: '#preguntas', desc: 'Preguntas frecuentes del producto' },
                ].map((link) => (
                  <a
                    key={link.label}
                    href={link.href}
                    className="flex items-start gap-3 p-3 rounded-xl border border-sedac-line-light hover:border-amber-400/40 hover:bg-white/5 transition group"
                  >
                    <span className="mt-0.5 w-6 h-6 rounded-full border border-sedac-line-light flex items-center justify-center text-xs text-amber-400/80 group-hover:border-amber-400 group-hover:text-amber-400 transition">
                      <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round">
                        <path d="M5 12h14M12 5l7 7-7 7" />
                      </svg>
                    </span>
                    <div>
                      <p className="text-sm font-medium text-white/90 group-hover:text-amber-400 transition" style={{ fontFamily: 'var(--font-display)', fontWeight: '500' }}>
                        {link.label}
                      </p>
                      <p className="text-xs text-white/50 mt-0.5">{link.desc}</p>
                    </div>
                  </a>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        [data-reveal="cta-copy"], [data-reveal="cta-list"] {
          opacity: 0;
          transform: translateY(18px);
          transition: opacity 0.7s cubic-bezier(0.22,1,0.36,1), transform 0.7s cubic-bezier(0.22,1,0.36,1);
        }
        [data-reveal="cta-copy"].is-in, [data-reveal="cta-list"].is-in {
          opacity: 1;
          transform: none;
        }
      `}</style>
    </section>
  );
}
