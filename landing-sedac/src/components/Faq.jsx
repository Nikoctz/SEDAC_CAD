import { useEffect, useRef, useState } from 'react';

const items = [
  {
    q: '¿Qué incluye el sistema SEDAC?',
    a: 'Un conjunto auxiliar desmontable formado por estructura, contacto con el usuario y soporte textil. No incluye la bolsa de agua ni la bomba de referencia; es un sistema que acompaña al equipo, no un reemplazo de la mochila.',
  },
  {
    q: '¿SEDAC sustituye a la bomba Scotty o a la bolsa de agua?',
    a: 'No. La bomba de referencia mencionada es una mochila Scotty; SEDAC se diferencia de la bolsa de agua y del sistema auxiliar, y se presenta como un sistema auxiliar encima del equipo. La bolsa de agua no está modelada en las vistas actuales.',
  },
  {
    q: '¿Es compatible con cualquier mochila de agua?',
    a: 'Aún no se puede afirmar compatibilidad completa. El diseño actual está asociado al estado del proyecto P2.04 y requiere confirmar dimensiones reales de la bomba, la bolsa llena/vacía, costuras, manguera y tapa antes de hablar de compatibilidad concreta.',
  },
  {
    q: '¿Está disponible para comprar o recibir?',
    a: 'El producto continúa en desarrollo. No hay disponibilidad, precios ni canal de compra publicados. Lo que se puede ofrecer ahora son presentaciones y conversaciones sobre necesidades y posibles colaboraciones.',
  },
  {
    q: '¿Ha pasado SEDAC por ensayos físicos o certificaciones?',
    a: 'No. Las prestaciones siguen pendientes de validación física y no se publican certificaciones. La página incluye una animación IMU y gráficas demostrativas, todas identificadas como tales, sin mediciones reales.',
  },
  {
    q: '¿Cómo puedo solicitar una presentación o más información?',
    a: 'Usa el formulario de “Solicitar presentación”. Permite preparar una solicitud descargable o copiable. No hay envío automático ni backend configurado, por lo que la página indica “solicitud preparada; todavía no enviada” y deja que copies o descargues el texto.',
  },
];

export default function Faq() {
  const [open, setOpen] = useState(0);

  useEffect(() => {
    const els = document.querySelectorAll('[data-faq-item]');
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.dataset.visible = 'true';
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.1 }
    );
    els.forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, []);

  return (
    <section className="section-section bg-sedac-paper2" aria-labelledby="faq-title" id="preguntas">
      <div className="wrap max-w-3xl mx-auto px-6 lg:px-10">
        <div className="mb-12 reveal" data-reveal="faq-head">
          <p className="eyebrow mb-4">Preguntas frecuentes</p>
          <h2
            id="faq-title"
            className="display"
            style={{ color: 'var(--sedac-ink)', fontFamily: 'var(--font-display)', fontWeight: '700', letterSpacing: '-0.02em', lineHeight: '1.02' }}
          >
            Preguntas sobre
            <br />
            <em className="text-accent">un producto en desarrollo</em>
          </h2>
        </div>

        <div className="space-y-3 reveal" data-reveal="faq-list" role="list">
          {items.map((item, i) => (
            <div
              key={i}
              data-faq-item
              className={`rounded-2xl border border-sedac-line bg-white overflow-hidden transition-all duration-300 ${open === i ? 'border-accent/40 shadow-sm' : ''}`}
              style={{ opacity: 'var(--faq-opacity, 0)' }}
            >
              <button
                type="button"
                data-faq-btn
                aria-expanded={open === i}
                aria-controls={`faq-panel-${i}`}
                className="w-full flex items-center justify-between gap-4 px-6 py-5 text-left focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-inset"
                onClick={() => setOpen(open === i ? -1 : i)}
              >
                <span className="text-sm font-semibold text-sedac-ink pr-4" style={{ fontFamily: 'var(--font-display)' }}>
                  {item.q}
                </span>
                <svg
                  className={`w-5 h-5 flex-none text-sedac-muted transition-transform duration-300 ${open === i ? 'rotate-180' : ''}`}
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                >
                  <path d="M6 9l6 6 6-6" />
                </svg>
              </button>
              <div
                id={`faq-panel-${i}`}
                role="region"
                aria-labelledby={`faq-btn-${i}`}
                className={`overflow-hidden transition-all duration-300 ${open === i ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'}`}
              >
                <div className="px-6 pb-5 text-sm leading-relaxed text-sedac-muted border-t border-sedac-line pt-4">
                  {item.a}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <style>{`
        [data-reveal="faq-head"], [data-reveal="faq-list"] {
          opacity: 0;
          transform: translateY(16px);
          transition: opacity 0.6s cubic-bezier(0.22,1,0.36,1), transform 0.6s cubic-bezier(0.22,1,0.36,1);
        }
        [data-reveal="faq-head"].is-in, [data-reveal="faq-list"].is-in {
          opacity: 1;
          transform: none;
        }
      `}</style>
    </section>
  );
}
