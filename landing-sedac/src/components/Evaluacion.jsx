import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export default function Evaluacion() {
  const ref = useRef(null);
  const plotRef = useRef(null);

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

  useEffect(() => {
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: '.imu-flow',
          start: 'top 85%',
          end: 'top 45%',
          scrub: 1.1,
          invalidateOnRefresh: true,
        },
        defaults: { ease: 'power1.out', duration: 1.1 },
      });

      tl.fromTo('.imu-step', { opacity: 0, y: 24 }, { opacity: 1, y: 0, stagger: 0.12 });
      tl.fromTo(
        '.imu-plot svg .imu-line',
        { strokeDashoffset: 600 },
        { strokeDashoffset: 0, duration: 1.4, ease: 'power2.inOut' },
        0
      );
      tl.fromTo('.imu-plot svg .imu-dot', { opacity: 0, scale: 0 }, { opacity: 1, scale: 1, stagger: 0.12 }, 0.2);
      tl.fromTo('.imu-plot .plot-legend span', { opacity: 0, x: -8 }, { opacity: 1, x: 0, stagger: 0.1 }, 0.5);
    }, ref);

    return () => ctx.revert();
  }, []);

  return (
    <section className="section dark" aria-labelledby="imu-title" id="evaluacion-p">
      <div className="wrap max-w-7xl mx-auto px-6 lg:px-10" ref={ref}>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16">
          {/* left copy */}
          <div className="lg:col-span-6 reveal" data-reveal="imu-copy">
            <p className="eyebrow text-muted-dark mb-5">Sensores IMU · evaluación prevista</p>
            <h2 id="imu-title" className="display text-paper mb-5" style={{ color: 'var(--paper)' }}>
              Leer el movimiento para entender el movimiento.
            </h2>
            <p className="lead text-muted-dark mb-5">
              La idea es usar sensores IMU para registrar y analizar cómo se mueve el equipo durante el uso
              real. Cualquier gráfica o modelo en esta sección es demostrativo y está identificado como tal;
              no representa datos medidos ni una plataforma existente.
            </p>
            <p className="text-sm text-muted-dark mb-5">
              Las IMU miden movimiento y orientación, no presión ni fuerza directamente. Por eso la evaluación
              se plantea como un registro del movimiento que habría que interpretar junto con el resto del sistema.
            </p>

            <div className="callout">
              <strong className="text-paper">Gráfica ilustrativa.</strong>
              {' '}No hay mediciones reales, ni modelo de sensor, ni plataforma disponible. Lo que se muestra acá es una
              representación para explicar la idea.
            </div>

            <ul className="limits">
              <li>No se miden ni se declaran resultados de salud o seguridad.</li>
              <li>No se afirma una plataforma, un modelo de sensor ni un resultado.</li>
              <li>El valor aportado es la intención de evaluación, no un número publicado.</li>
            </ul>
          </div>

          {/* right: flow + plot */}
          <div className="lg:col-span-6 reveal reveal-delay-1" data-reveal="imu-visual">
            <div className="imu-head">
              <div className="imu-flow">
                {[
                  { idx: 'Paso 01', title: 'Movimiento', body: 'El equipo se mueve con el bombero durante el servicio.' },
                  { idx: 'Paso 02', title: 'Registro', body: 'Los sensores IMU registra la orientación y el movimiento del conjunto.' },
                  { idx: 'Paso 03', title: 'Análisis', body: 'Los datos se describen para entender cómo se comporta el sistema.' },
                  { idx: 'Paso 04', title: 'Intención', body: 'Usar esa lectura para orientar futuros ajustes y evaluaciones.' },
                ].map((step, i) => (
                  <div key={i} className="imu-step">
                    <p className="idx">{step.idx}</p>
                    <h3>{step.title}</h3>
                    <p>{step.body}</p>
                  </div>
                ))}
              </div>

              <div className="imu-plot">
                <div className="plot-box">
                  <svg viewBox="0 0 400 180" className="w-full" role="img" aria-label="Gráfica ilustrativa del movimiento registrado por IMU, etiquetada como demostrativa.">
                    <defs>
                      <linearGradient id="imu-grad" x1="0" y1="0" x2="1" y2="0">
                        <stop offset="0" stopColor="#ffc21a" stopOpacity="0.1" />
                        <stop offset="1" stopColor="#e0a400" stopOpacity="0.35" />
                      </linearGradient>
                    </defs>
                    {/* grid discreto */}
                    <g stroke="rgba(247,244,236,0.08)" strokeWidth="1">
                      {[0, 0.25, 0.5, 0.75, 1].map((t) => (
                        <line key={t} x1="40" y1={40 + t * 120} x2="360" y2={40 + t * 120} />
                      ))}
                      {[0, 0.25, 0.5, 0.75, 1].map((t) => (
                        <line key={t} x1={40 + t * 320} y1="40" x2={40 + t * 320} y2="160" />
                      ))}
                    </g>
                    {/* area */}
                    <path
                      className="imu-line"
                      d="M40 150 C 80 145, 110 90, 150 88 C 190 86, 220 110, 260 105 C 300 100, 330 120, 360 118 L 360 160 L 40 160 Z"
                      fill="url(#imu-grad)"
                      stroke="none"
                    />
                    {/* línea */}
                    <path
                      className="imu-line"
                      d="M40 150 C 80 145, 110 90, 150 88 C 190 86, 220 110, 260 105 C 300 100, 330 120, 360 118"
                      fill="none"
                      stroke="#ffc21a"
                      strokeWidth="2.2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                    {/* ejes */}
                    <line x1="40" y1="160" x2="360" y2="160" stroke="rgba(247,244,236,0.4)" strokeWidth="1.4" />
                    <line x1="40" y1="40" x2="40" y2="160" stroke="rgba(247,244,236,0.4)" strokeWidth="1.4" />
                    {/* etiquetas */}
                    <text x="360" y="174" fill="rgba(247,244,236,0.55)" fontSize="9" fontFamily="sans-serif" textAnchor="end">tiempo</text>
                    <text x="28" y="44" fill="rgba(247,244,236,0.55)" fontSize="9" fontFamily="sans-serif">ángulo / señal</text>
                    {/* puntos */}
                    {[60, 140, 220, 300, 345].map((x, i) => (
                      <circle key={i} className="imu-dot" cx={x} cy="150" r="3.4" fill="#141613" stroke="#ffc21a" strokeWidth="2" />
                    ))}
                  </svg>
                  <div className="plot-legend">
                    <span><span className="swatch" style={{ background: '#ffc21a' }} />señal ilustrativa</span>
                    <span>no datos medidos</span>
                  </div>
                </div>
                <div className="callout">
                  <strong className="text-paper">IMU ≠ fuerza.</strong>
                  {' '}Las IMU apuntan a movimiento y orientación; no miden presión ni fuerza directamente.
                  Qualquier gráfico acá es demostrativo y está identificado como tal.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        [data-reveal="imu-copy"], [data-reveal="imu-visual"] {
          opacity: 0;
          transform: translateY(18px);
          transition: opacity 0.7s ease, transform 0.7s ease;
        }
        [data-reveal="imu-copy"][data-visible="true"], [data-reveal="imu-visual"][data-visible="true"] {
          opacity: 1;
          transform: none;
        }
        .imu-plot .plot-legend { opacity: 0; }
        .imu-dot, .imu-line { stroke-dasharray: 600; }
      `}</style>
    </section>
  );
}
