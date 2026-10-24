import { useEffect, useRef, useCallback } from 'react';

export default function MobileMenu({ open, onClose, links }) {
  const panelRef = useRef(null);
  const firstRef = useRef(null);
  const lastRef = useRef(null);

  useEffect(() => {
    if (!open) return;
    const focusable = panelRef.current?.querySelectorAll(
      'button, a[href], [tabindex]:not([tabindex="-1"])'
    );
    if (focusable?.length) {
      firstRef.current = focusable[0];
      lastRef.current = focusable[focusable.length - 1];
      firstRef.current.focus();
    }
  }, [open]);

  const handleKey = useCallback(
    (e) => {
      if (e.key !== 'Escape' || !open) return;
      e.preventDefault();
      onClose();
    },
    [open, onClose]
  );

  useEffect(() => {
    if (!open) return;
    document.addEventListener('keydown', handleKey);
    return () => document.removeEventListener('keydown', handleKey);
  }, [open, handleKey]);

  useEffect(() => {
    if (!open) return;
    const onPointerDown = (e) => {
      if (panelRef.current && !panelRef.current.contains(e.target)) {
        onClose();
      }
    };
    document.addEventListener('pointerdown', onPointerDown);
    return () => document.removeEventListener('pointerdown', onPointerDown);
  }, [open, onClose]);

  const handleTab = useCallback(
    (e) => {
      if (!open || !firstRef.current || !lastRef.current) return;
      if (e.key !== 'Tab') return;
      if (e.shiftKey) {
        if (document.activeElement === firstRef.current) {
          e.preventDefault();
          lastRef.current.focus();
        }
      } else if (document.activeElement === lastRef.current) {
        e.preventDefault();
        firstRef.current.focus();
      }
    },
    [open]
  );

  useEffect(() => {
    if (!open) return;
    document.addEventListener('keydown', handleTab);
    return () => document.removeEventListener('keydown', handleTab);
  }, [open, handleTab]);

  if (!open) return null;

  return (
    <div
      ref={panelRef}
      className="fixed inset-0 z-40 bg-[#141613] flex flex-col items-center justify-center px-6 md:px-10 text-white"
      role="dialog"
      aria-modal="true"
      aria-label="Menú de navegación"
    >
      <div className="flex-1 w-full max-w-md flex flex-col justify-center gap-2">
        {links.map((l, i) => (
          <a
            key={l.href}
            href={l.href}
            className="text-2xl font-medium border-b border-white/10 pb-4 hover:text-amber-400 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-amber-400 rounded"
            onClick={onClose}
          >
            {l.label}
          </a>
        ))}
      </div>
      <div className="flex gap-4">
        {[
          { label: 'Enviar solicitud', onClick: onClose },
          { label: 'Cancelar', onClick: onClose },
        ].map((b) => (
          <button
            key={b.label}
            type="button"
            onClick={b.onClick}
            className="rounded-full border border-white/20 px-6 py-3 text-sm font-semibold text-white/80 hover:text-amber-400 hover:border-amber-400 transition focus:outline-none focus-visible:ring-2 focus-visible:ring-amber-400"
          >
            {b.label}
          </button>
        ))}
      </div>
    </div>
  );
}
