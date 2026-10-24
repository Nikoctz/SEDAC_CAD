import { useEffect, useRef, useState } from 'react';
import Nav from './components/Nav';
import MobileMenu from './components/MobileMenu';
import Hero from './components/Hero';
import Contexto from './components/Contexto';
import Producto from './components/Producto';
import Diseno from './components/Diseno';
import Evaluacion from './components/Evaluacion';
import Desarrollo from './components/Desarrollo';
import Faq from './components/Faq';
import CtaFinal from './components/CtaFinal';
import ContactModal from './components/ContactModal';

export default function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const rootRef = useRef(null);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 48);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    document.body.parentElement.classList.toggle('menu-open', menuOpen);
  }, [menuOpen]);

  const openModal = () => setModalOpen(true);
  const closeModal = () => setModalOpen(false);

  return (
    <div ref={rootRef} className="app-root">
      <Nav
        menuOpen={menuOpen}
        onToggleMenu={() => setMenuOpen((v) => !v)}
        onRequestPresentation={openModal}
        scrolled={scrolled}
      />
      <MobileMenu
        open={menuOpen}
        onClose={() => setMenuOpen(false)}
        links={[
          { label: 'Sistema', href: '#sistema' },
          { label: 'Diseño', href: '#diseno' },
          { label: 'Evaluación', href: '#evaluacion' },
          { label: 'Preguntas', href: '#preguntas' },
        ]}
      />

      <main className="main">
        <Hero onRequestPresentation={openModal} />
        <Contexto />
        <Producto />
        <Diseno />
        <Evaluacion />
        <Desarrollo />
        <Faq />
        <CtaFinal onRequestPresentation={openModal} />
      </main>      <footer className="site-footer">
        <div className="wrap foot-inner">
          <div>
            <span className="brand-name" style={{ color: 'var(--paper)', fontWeight: 700, letterSpacing: '0.18em' }}>SEDAC</span>
            <span className="brand-sub" style={{ marginLeft: 8, color: 'var(--paper-3)' }}>sistema auxiliar · desarrollo</span>
          </div>
          <div className="foot-meta">
            <span className="note">Producto en desarrollo · prediseño CAD · validación física pendiente</span>
            <button type="button" onClick={openModal} className="ml-4 text-[11px] tracking-widest uppercase text-amber-400/80 hover:text-amber-300 underline underline-offset-4 decoration-white/20 hover:decoration-amber-400/50 transition">
              Solicitar presentación
            </button>
          </div>
        <div>&copy; 2026 SEDAC. Todos los derechos reservados.</div>
        </div>
      </footer>

      <ContactModal open={modalOpen} onClose={closeModal} />
    </div>
  );
}
