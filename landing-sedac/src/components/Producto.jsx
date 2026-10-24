import { useState, useEffect, useRef, useCallback } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import ViewerShell from '../viewer/App';

gsap.registerPlugin(ScrollTrigger);

const FRAMES = Array.from({ length: 24 }, (_, i) =>
  `/assets/seq/conjunto/${String(i).padStart(3, '0')}.webp`
);

const STRUCT_FRAMES = Array.from({ length: 24 }, (_, i) =>
  `/assets/seq/estructura/${String(i).padStart(3, '0')}.webp`
);

const ANNOTATIONS = {
  conjunto: [
    {
      x: '18%',
      y: '34%',
      title: 'Dos canales independientes',
      text: 'Canales abiertos de aluminio 6061-T6, separados, que recorren el conjunto sin unirse entre sí.',
    },
    {
      x: '62%',
      y: '28%',
      title: 'Cuna textil',
      text: 'Soporte inferior para la bolsa de agua, con dos superficies laterales y apertura central nominal.',
    },
    {
      x: '40%',
      y: '70%',
      title: 'Funda de cobertura',
      text: 'Envoltura textil que cubre la cara abierta de los canales y completa el soporte alrededor de la bolsa.',
    },
  ],
  estructura: [
    {
      x: '22%',
      y: '30%',
      title: 'Arquitectura desmontable',
      text: 'Conjunto de piezas rígidas que se ensamblan y desmontan; unión por tornillo, arandela y pasador hueco.',
    },
    {
      x: '58%',
      y: '44%',
      title: 'Interfaz lumbar',
      text: 'Cuerpo de 3 mm con refuerzos locales; panel de contacto HDPE de 1 mm recortado para ventilación.',
    },
    {
      x: '36%',
      y: '78%',
      title: 'Yugos e hombros',
      text: 'Yugos superiores con placa de 6 mm, mejillas de 3 mm y ranuras para cinturón y cuna.',
    },
  ],
};

function useFrames(base) {
  const [frames, setFrames] = useState([]);
  const loaded = useRef(0);

  useEffect(() => {
    loaded.current = 0;
    const imgs = [];
    let cancelled = false;
    const next = (i) => {
      if (cancelled) return;
      if (i >= FRAMES.length && base === FRAMES) {
        setFrames(imgs);
        return;
      }
      if (i >= STRUCT_FRAMES.length && base !== FRAMES) {
        setFrames(imgs);
        return;
      }
      const src = base === FRAMES ? FRAMES[i] : STRUCT_FRAMES[i];
      const img = new Image();
      img.src = src;
      img.onload = () => {
        loaded.current += 1;
        imgs.push({ src, img, ready: true });
        if (i === 11 || (base === FRAMES && i === FRAMES.length - 1) || (base !== FRAMES && i === STRUCT_FRAMES.length - 1)) {
          setFrames([...imgs]);
        }
        if (i < (base === FRAMES ? FRAMES.length : STRUCT_FRAMES.length) - 1) {
          const raf = requestAnimationFrame(() => next(i + 1));
          if (!cancelled) return raf;
        }
      };
      img.onerror = () => {
        imgs.push({ src, img, ready: false });
        if (i === (base === FRAMES ? FRAMES.length - 1 : STRUCT_FRAMES.length - 1)) setFrames([...imgs]);
        if (i < (base === FRAMES ? FRAMES.length : STRUCT_FRAMES.length) - 1) next(i + 1);
      };
    };
    next(0);
    return () => { cancelled = true; };
  }, [base]);

  return frames;
}

function useSequence(base) {
  const [frames, setFrames] = useState([]);
  const [progress, setProgress] = useState(0);
  const rafRef = useRef(null);
  const framesRef = useRef(frames);
  const progressRef = useRef(progress);

  useEffect(() => { framesRef.current = frames; }, [frames]);
  useEffect(() => { progressRef.current = progress; }, [progress]);

  useEffect(() => {
    const ctx = gsap.context(() => {
      ScrollTrigger.create({
        trigger: document.querySelector('[data-sequence-scroll]'),
        start: 'top 88%',
        end: 'top 40%',
        scrub: 1.2,
        onUpdate: (self) => {
          if (self.progress <= 0.02) return;
          setProgress(self.progress);
        },
      });
    });
    return () => ctx.revert();
  }, []);

  const setFrame = useCallback(
    (value) => {
      const v = Math.max(0, Math.min(FRAMES.length - 1, Math.round(value)));
      setProgress(v);
      if (framesRef.current[v]?.img?.ready) {
        const img = framesRef.current[v]?.img;
        const wrap = document.getElementById('viewer-frame-img');
        if (wrap) {
          gsap.fromTo(
            wrap.querySelector('img'),
            { opacity: 0, scale: 1.04, rotate: 0 },
            {
              opacity: 1,
              scale: 1,
              rotate: 0,
              duration: 0.45,
              ease: 'power2.out',
              overwrite: 'auto',
            }
          );
          wrap.querySelector('img').src = img.src;
        }
      }
    },
    []
  );

  useEffect(() => {
    if (progress > 0) {
      setFrame(progress);
      const idx = Math.round(progress);
      if (idx > 0 && idx < FRAMES.length - 1 && framesRef.current[idx]?.img?.ready) {
        const wrap = document.getElementById('viewer-frame-img');
        if (wrap) {
          const img = wrap.querySelector('img');
          const src = framesRef.current[idx]?.img?.src;
          if (src && img.src !== src) {
            img.src = src;
            gsap.fromTo(
              img,
              { opacity: 0, scale: 1.02, rotate: 0 },
              { opacity: 1, scale: 1, rotate: 0, duration: 0.4, ease: 'power2.out', overwrite: 'auto' }
            );
          }
        }
      }
    }
  }, [progress, setFrame]);

  return { frames, progress, setFrame, setProgress };
}

export default function Producto() {
  const [view, setView] = useState('conjunto');
  const [drag, setDrag] = useState(false);
  const [angle, setAngle] = useState(0);
  const [zoom, setZoom] = useState(false);
  const [activeAnnot, setActiveAnnot] = useState(null);

  const frames = useFrames(view === 'conjunto' ? FRAMES : STRUCT_FRAMES);
  const seq = useSequence(view === 'conjunto' ? FRAMES : STRUCT_FRAMES);
  const viewportRef = useRef(null);
  const lastRef = useRef({ x: 0, y: 0 });
  const panRef = useRef(0);

  useEffect(() => {
    const frame = frames[Math.round(seq.progress)]?.img;
    if (!frame?.ready) return;
    const img = document.getElementById('viewer-frame-img')?.querySelector('img');
    if (img && img.src !== frame.src) {
      gsap.fromTo(img, { opacity: 0, scale: 1.03 }, { opacity: 1, scale: 1, duration: 0.4, ease: 'power2.out' });
      img.src = frame.src;
    }
  }, [frames, seq.progress]);

  const setFrame = useCallback(
    (value) => {
      const idx = Math.max(0, Math.min(FRAMES.length - 1, Math.round(value)));
      seq.setProgress(idx);
      const frame = frames[idx];
      if (frame?.img?.ready) {
        const img = document.getElementById('viewer-frame-img')?.querySelector('img');
        if (img && img.src !== frame.src) {
          gsap.fromTo(img, { opacity: 0, scale: 1.03 }, { opacity: 1, scale: 1, duration: 0.4, ease: 'power2.out' });
          img.src = frame.src;
        }
      }
    },
    [frames, seq]
  );

  const rotateBy = useCallback(
    (deg) => {
      const next = (((angle + deg) % 360) + 360) % 360;
      setAngle(next);
      const idx = Math.round((next / 360) * (FRAMES.length - 1));
      setFrame(idx);
    },
    [angle, setFrame]
  );

  const onPointerDown = (e) => {
    if (e.button !== undefined && e.button !== 0) return;
    setDrag(true);
    const p = e.touches ? e.touches[0] : e;
    lastRef.current = { x: p.clientX, y: p.clientY };
  };

  const onPointerMove = (e) => {
    if (!drag) return;
    const p = e.touches ? e.touches[0] : e;
    const dx = p.clientX - lastRef.current.x;
    lastRef.current = { x: p.clientX, y: p.clientY };
    rotateBy(dx * 0.55);
  };

  const onPointerUp = () => setDrag(false);

  useEffect(() => {
    const el = viewportRef.current;
    if (!el) return;
    el.addEventListener('mousemove', onPointerMove);
    el.addEventListener('mouseup', onPointerUp);
    el.addEventListener('mouseleave', onPointerUp);
    el.addEventListener('touchmove', onPointerMove, { passive: true });
    el.addEventListener('touchend', onPointerUp, { passive: true });
    return () => {
      el.removeEventListener('mousemove', onPointerMove);
      el.removeEventListener('mouseup', onPointerUp);
      el.removeEventListener('mouseleave', onPointerUp);
      el.removeEventListener('touchmove', onPointerMove);
      el.removeEventListener('touchend', onPointerUp);
    };
  }, [drag, onPointerMove, onPointerUp]);

  const toggleZoom = () => setZoom((z) => !z);

  return (
    <section className="section-section bg-sedac-paper2" aria-labelledby="producto-title" data-sequence-scroll id="sistema">
      <div className="wrap max-w-7xl mx-auto px-6 lg:px-10">
        {/* header */}
        <div className="max-w-3xl reveal" data-reveal="producto-head">
          <p className="eyebrow mb-4">Sistema · interactivo</p>
          <h2
            id="producto-title"
            className="display mb-4"
            style={{ color: 'var(--sedac-ink)', fontFamily: 'var(--font-display)', fontWeight: '700', letterSpacing: '-0.02em', lineHeight: '1.02' }}
          >
            Producto protagonista
          </h2>
          <p className="lead mb-6" style={{ color: 'var(--sedac-muted)' }}>
            Un visor de secuencia real de la geometría. Arrastra para recorrer los ángulos o usa los controles.
            No es un modelo 3D; son capturas del CAD.
          </p>
        </div>

        {/* visor */}
        <div className="mt-14 reveal" data-reveal="producto-viewer">
          <ViewerShell
            ref={viewportRef}
            label="Visor del producto"
            description="Visor de secuencia; cambia de ángulo o vista con los controles o arrastrando."
          >
            <div id="viewer-frame-img" className="img-frame" style={{ position: 'relative', width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              {frames.length === 0 ? (
                <div className="absolute inset-0 flex items-center justify-center bg-sedac-graphite-2 rounded-2xl border border-sedac-line-dark">
                  <span className="text-sedac-muted text-sm tracking-widest uppercase">precargando secuencia…</span>
                </div>
              ) : (
                frames.map((f, i) => (
                  <img
                    key={i}
                    className="img"
                    src={f.src}
                    alt={`Vista ${i} de la secuencia ${view === 'conjunto' ? 'conjunto' : 'estructura'}`}
                    loading="lazy"
                    style={{ opacity: i === Math.round(seq.progress) ? 1 : 0, transform: 'scale(1)' }}
                  />
                ))
              )}
            </div>
            <div className="slider-deco" aria-hidden="true" />
            <div className="grain-overlay" aria-hidden="true" />
            <div className="tag-banner" aria-live="polite">
              <strong>{view === 'conjunto' ? 'Conjunto' : 'Estructura'}</strong> · ángulo {Math.round(angle)}°
            </div>
            <div className="zoom-hint">
              <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round">
                <circle cx="7" cy="7" r="4.5" />
                <path d="M10.5 10.5 L13 13" />
                <path d="M5.5 7 L8.5 7 L8.5 10.5" />
              </svg>
              <button type="button" onClick={toggleZoom} className="hover:text-sedac-amber transition-colors">
                {zoom ? 'Reducir' : 'Ampliar'}
              </button>
            </div>
          </ViewerShell>

          {/* selector Conjunto / Estructura */}
          <div className="mt-6 flex flex-wrap gap-2">
            <button
              type="button"
              aria-pressed={view === 'conjunto'}
              onClick={() => {
                setView('conjunto');
                setAngle(0);
                seq.setProgress(0);
              }}
              className={`btn gap-2 py-3 px-5 ${view === 'conjunto' ? 'btn-primary' : 'btn-ghost'}`}
            >
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="3" />
                <path d="M9 12h6M12 9v6" />
              </svg>
              Conjunto
            </button>
            <button
              type="button"
              aria-pressed={view === 'estructura'}
              onClick={() => {
                setView('estructura');
                setAngle(0);
                seq.setProgress(0);
              }}
              className={`btn gap-2 py-3 px-5 ${view === 'estructura' ? 'btn-primary' : 'btn-ghost'}`}
            >
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <path d="M3 20 L9 4 L15 20 L21 4" />
                <path d="M3 12 L9 12 M15 12 L21 12" />
              </svg>
              Estructura
            </button>
          </div>
        </div>

        {/* anotaciones */}
        <div className="mt-14 grid grid-cols-1 md:grid-cols-3 gap-6 reveal" data-reveal="producto-annotations">
          {ANNOTATIONS[view].map((a, i) => (
            <div
              key={i}
              className="relative h-24 rounded-2xl border border-sedac-line bg-sedac-paper overflow-hidden group"
            >
              <div
                className="absolute inset-0 opacity-0 transition-opacity duration-300 group-hover:opacity-100"
                style={{
                  backgroundImage: `radial-gradient(circle at ${a.x} ${a.y}, rgba(255,194,26,0.28) 0, transparent 32%)`,
                }}
              />
              <div className="relative z-10 h-full flex flex-col justify-center px-5">
                <p className="text-[11px] tracking-[0.18em] uppercase text-accent mb-1.5 font-semibold">
                  {a.title}
                </p>
                <p className="text-sm leading-relaxed text-sedac-muted">{a.text}</p>
              </div>
            </div>
          ))}
        </div>

        {/* control strip */}
        <div className="mt-10 reveal flex flex-wrap items-center gap-5" data-reveal="producto-controls">
          <div className="flex gap-2">
            {[0, 60, 120, 180, 240, 300].map((deg) => (
              <button
                key={deg}
                type="button"
                aria-label={`Ángulo ${deg}°`}
                aria-pressed={Math.round(angle) === deg}
                onClick={() => rotateBy(deg - angle)}
                className={`rounded-full border ${Math.round(angle) === deg ? 'border-accent bg-accent/10 text-accent' : 'border-sedac-line-dark text-sedac-muted hover:border-accent hover:text-accent'} transition px-3.5 py-1.5 text-xs font-medium`}
              >
                {deg}°
              </button>
            ))}
          </div>
          <span className="text-xs uppercase tracking-widest text-sedac-muted">
            arrastra el visor para girar · scroll vinculado en escritorio
          </span>
        </div>
      </div>

      <style>{`
        [data-reveal="producto-head"], [data-reveal="producto-viewer"], [data-reveal="producto-annotations"], [data-reveal="producto-controls"] {
          opacity: 0;
          transform: translateY(18px);
          transition: opacity 0.7s cubic-bezier(0.22,1,0.36,1), transform 0.7s cubic-bezier(0.22,1,0.36,1);
        }
        [data-reveal="producto-head"].is-in, [data-reveal="producto-viewer"].is-in, [data-reveal="producto-annotations"].is-in, [data-reveal="producto-controls"].is-in {
          opacity: 1;
          transform: none;
        }
      `}</style>
    </section>
  );
}
