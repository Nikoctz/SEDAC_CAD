import { useEffect, useRef } from 'react';

export default function Nav({ menuOpen, onToggleMenu, onRequestPresentation, scrolled }) {
  const heroRef = useRef(null);

  useEffect(() => {
    const el = heroRef.current;
    if (el && menuOpen) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, [menuOpen]);

  return (
    <header
      className={`fixed z-50 flex items-center justify-between h-16 px-4 md:px-8 text-white transition-shadow ${
        scrolled ? 'bg-[#141613]/95 shadow-lg shadow-black/20' : 'bg-[#141613]/70 backdrop-blur-md'
      }`}
      onMouseEnter={() => {}}
    >
      {/* marca */}
      <a
        href="#hero"
        className="flex items-center gap-2 group"
        onClick={onToggleMenu}
        ref={heroRef}
      >
        <div className="relative w-8 h-8 flex items-center justify-center">
          <svg
            className="w-7 h-7 text-amber-400 drop-shadow-sm"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.6"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M3 20 L9 4 L15 20 L21 4" />
            <path d="M9 4 L15 20" strokeOpacity="0.5" />
            <circle cx="10.5" cy="12" r="2" fill="currentColor" stroke="none" />
          </svg>
        </div>
        <div className="flex flex-col leading-tight">
          <span className="text-lg font-bold tracking-widest text-white">SEDAC</span>
          <span className="text-[10px] tracking-[0.2em] uppercase text-white/50 -mt-0.5">sistema auxiliar</span>
        </div>
      </a>

      {/* navegación desktop */}
      <nav className="hidden md:flex items-center gap-10 text-sm font-medium text-white/80">
        <a
          href="#sistema"
          className="relative after:absolute after:left-0 after:bottom-0 after:h-0.5 after:w-0 after:bg-amber-400 after:transition-all hover:text-amber-400 hover:after:w-full transition-colors"
        >
          Sistema
        </a>
        <a
          href="#diseno"
          className="relative after:absolute after:left-0 after:bottom-0 after:h-0.5 after:w-0 after:bg-amber-400 after:transition-all hover:text-amber-400 hover:after:w-full transition-colors"
        >
          Diseño
        </a>
        <a
          href="#evaluacion"
          className="relative after:absolute after:left-0 after:bottom-0 after:h-0.5 after:w-0 after:bg-amber-400 after:transition-all hover:text-amber-400 hover:after:w-full transition-colors"
        >
          Evaluación
        </a>
        <a
          href="#preguntas"
          className="relative after:absolute after:left-0 after:bottom-0 after:h-0.5 after:w-0 after:bg-amber-400 after:transition-all hover:text-amber-400 hover:after:w-full transition-colors"
        >
          Preguntas
        </a>
      </nav>

      {/* CTAs */}
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={onRequestPresentation}
          className="hidden sm:inline-flex items-center gap-2 rounded-full bg-amber-400 px-5 py-2.5 text-[13px] font-semibold text-[#141613] transition hover:bg-amber-300 active:scale-[0.97]"
        >
          Solicitar presentación
        </button>
        <a
          href="#sistema"
          className="rounded-full border border-white/20 px-4 py-2 text-sm font-medium text-white/80 transition hover:border-amber-400 hover:text-amber-400 md:hidden"
        >
          Conocer SEDAC
        </a>
        <button
          type="button"
          onClick={onToggleMenu}
          className="md:hidden rounded-full border border-white/20 p-2 text-white/80 transition hover:border-amber-400"
          aria-label={menuOpen ? 'Cerrar menú' : 'Abrir menú'}
        >
          <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            {menuOpen ? (
              <>
                <path d="M6 6 L18 18" />
                <path d="M18 6 L6 18" />
              </>
            ) : (
              <>
                <path d="M4 6 L20 6" />
                <path d="M4 12 L20 12" />
                <path d="M4 18 L20 18" />
              </>
            )}
          </svg>
        </button>
      </div>
    </header>
  );
}
