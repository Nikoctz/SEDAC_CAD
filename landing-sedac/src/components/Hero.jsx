import { useState, useEffect } from 'react';

export default function Hero({ onRequestPresentation }) {
  const [imgReady, setImgReady] = useState(false);

  useEffect(() => {
    const img = document.getElementById('hero-img');
    if (!img) return;
    const onLoad = () => setImgReady(true);
    if (img.complete) onLoad();
    else img.addEventListener('load', onLoad);
    return () => img.removeEventListener('load', onLoad);
  }, []);

  return (
    <section className="hero" aria-labelledby="hero-title" id="hero">
      {/* ambiente */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden z-0" aria-hidden="true">
        <div className="absolute top-[-10%] left-[-8%] w-[65%] h-[65%] rounded-full bg-amber-500/10 blur-[120px]" />
        <div className="absolute bottom-[-12%] right-[-6%] w-[55%] h-[55%] rounded-full bg-amber-600/8 blur-[100px]" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16 items-center">
          {/* copy */}
          <div className="lg:col-span-6 reveal z-10" data-reveal="hero-copy">
            <p className="eyebrow mb-5 text-amber-400/90" style={{ color: 'rgba(255,194,26,0.85)' }}>
              Sistema auxiliar · desarrollo
            </p>
            <h1 id="hero-title" className="display font-bold tracking-tight text-white leading-[0.96] max-w-[14ch]">
              Diseñado para
              <br />
              <em>acompañar</em>
              <br />
              el movimiento.
            </h1>
            <p className="mt-6 text-lg text-white/70 leading-relaxed max-w-[46ch]">
              SEDAC es un sistema auxiliar desmontable que acompaña la bolsa de agua del equipo de
              bombero forestal: estructura, contacto y soporte textil pensados para no acompañar la carga
              del agua, sino redistribuirla.
            </p>
            <div className="flex flex-wrap gap-4 mt-8">
              <button
                type="button"
                onClick={onRequestPresentation}
                className="group inline-flex items-center gap-2.5 rounded-full bg-amber-400 px-7 py-4 text-sm font-semibold text-[#141613] shadow-2xl shadow-amber-600/25 transition hover:bg-amber-300 hover:-translate-y-0.5 active:scale-[0.97]"
              >
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M5 12h14M13 6l6 6-6 6" />
                </svg>
                Solicitar presentación
              </button>
              <a
                href="#sistema"
                className="group inline-flex items-center gap-2.5 rounded-full border border-white/20 px-7 py-4 text-sm font-medium text-white/90 transition hover:border-amber-400 hover:text-amber-400 hover:-translate-y-0.5"
              >
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                  <path d="M7 13l5 5 5-5M7 6l5 5 5-5" />
                </svg>
                Conocer SEDAC
              </a>
            </div>
            <div className="mt-10 pt-6 border-t border-white/10 flex flex-wrap gap-x-8 gap-y-3 text-xs uppercase tracking-[0.14em] text-white/50">
              <span className="flex items-center gap-2">
                <svg className="w-4 h-4 text-amber-400/80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round">
                  <circle cx="12" cy="12" r="9" />
                  <path d="M12 8v4l3 3" />
                </svg>
                Entrega P2.04 vigente
              </span>
              <span className="flex items-center gap-2">
                <svg className="w-4 h-4 text-amber-400/80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round">
                  <path d="M4 12h16M12 4v16" />
                </svg>
                Prediseño CAD · no producto fabricado
              </span>
            </div>
          </div>

          {/* figura */}
          <div className="lg:col-span-6 reveal z-10 relative lg:after:-top-20 lg:after:right-[-6%] lg:after:w-[540px] lg:after:h-[540px] lg:after:bg-amber-500/10 lg:after:rounded-full lg:after:blur-[140px]" style={{ order: 'inherit' }}>
            <div className="relative rounded-2xl overflow-hidden bg-[#1d201b] border border-white/10 shadow-2xl shadow-black/40 transform hover:-translate-y-1 transition-transform duration-500">
              <div className="aspect-[4/3] max-h-[560px] mx-auto w-full overflow-hidden">
                {!imgReady && (
                  <div className="absolute inset-0 bg-gradient-to-t from-[#141613] via-transparent to-transparent flex items-end justify-center pb-10">
                    <span className="text-[11px] uppercase tracking-[0.18em] text-white/40">Cargando vista</span>
                  </div>
                )}
                <img
                  id="hero-img"
                  src="/assets/product/VISTA_ESTRUCTURA.png"
                  alt="Vista de estructura del sistema auxiliar SEDAC, composición asimétrica con canales abiertos de aluminio y cuna textil."
                  className={`w-full h-full object-cover transition-opacity duration-700 ${
                    imgReady ? 'opacity-100' : 'opacity-0'
                  }`}
                  loading="eager"
                />
              </div>
              {/* decoraciones */}
              <div className="absolute -top-3 -right-3 w-24 h-24 bg-amber-400/20 rounded-full blur-2xl pointer-events-none" />
              <div className="absolute -bottom-6 -left-6 w-32 h-32 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />
              {/* tags */}
              <div className="absolute bottom-4 left-4 right-4 flex flex-wrap gap-2">
                <span className="rounded-full bg-[#141613]/70 backdrop-blur border border-white/10 px-3 py-1 text-[10px] tracking-[0.2em] uppercase text-white/60">
                  Vista estructura
                </span>
                <span className="rounded-full bg-amber-400/15 border border-amber-400/25 px-3 py-1 text-[10px] tracking-[0.2em] uppercase text-amber-300 font-medium">
                  Producto en desarrollo
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
