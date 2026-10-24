import { useState, useRef, useEffect, useCallback } from 'react';

const INITIAL = {
  nombre: '',
  organizacion: '',
  rol: '',
  interes: 'presentacion',
  mensaje: '',
};

export default function ContactModal({ open, onClose }) {
  const [form, setForm] = useState(INITIAL);
  const [errors, setErrors] = useState({});
  const [status, setStatus] = useState('idle'); // idle | processing | ready
  const [focused, setFocused] = useState(null);
  const backdropRef = useRef(null);
  const modalRef = useRef(null);
  const firstRef = useRef(null);

  useEffect(() => {
    if (!open) return;
    setForm(INITIAL);
    setErrors({});
    setStatus('idle');
    setFocused(null);
    setTimeout(() => firstRef.current?.focus(), 30);
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = '';
    };
  }, [open]);

  const onKey = useCallback((e) => {
    if (e.key === 'Escape' && open) {
      e.preventDefault();
      onClose();
    }
  }, [open, onClose]);

  useEffect(() => {
    if (!open) return;
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [open, onKey]);

  useEffect(() => {
    if (!open) return;
    const node = backdropRef.current;
    if (!node) return;
    node.addEventListener('click', (e) => {
      if (e.target === node) onClose();
    });
    return () => node.removeEventListener('click', () => {});
  }, [open, onClose]);

  const validate = (data) => {
    const errs = {};
    if (!data.nombre.trim()) errs.nombre = 'El nombre es requerido.';
    if (!data.organizacion.trim()) errs.organizacion = 'La organización o rol es requerido.';
    if (!data.interes) errs.interes = 'Selecciona una opción.';
    return errs;
  };

  const handleChange = (field) => (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setForm((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: '' }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const errs = validate(form);
    setErrors(errs);
    setFocused(Object.keys(errs)[0]);
    if (Object.keys(errs).length) return;
    setStatus('processing');
    const prepared = buildRequest(form);
    setTimeout(() => {
      setStatus('ready');
      const blob = new Blob([prepared.text], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Solicitud_SEDAC_${slug(form.nombre || ' Solicitud')}.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(() => URL.revokeObjectURL(url), 1200);
      setFocused('status');
    }, 320);
  };

  if (!open) return null;

  return (
    <div
      ref={backdropRef}
      className="fixed inset-0 z-70 flex items-start justify-center p-4 pt-[10vh] bg-sedac-graphite/55 backdrop-blur transition-opacity"
      aria-modal="true"
      role="dialog"
      aria-labelledby="modalTitle"
    >
      <div className="relative w-full max-w-[560px] bg-sedac-paper rounded-3xl border border-sedac-line shadow-2xl overflow-hidden">
        <div className="flex items-center justify-between px-6 py-5 border-b border-sedac-line">
          <div>
            <p className="text-[11px] tracking-[0.2em] uppercase text-sedac-muted mb-1">Solicitud</p>
            <h2 id="modalTitle" className="text-xl font-semibold tracking-[-0.02em] text-sedac-ink">
              Solicitar presentación
            </h2>
          </div>
          <button
            className="w-9 h-9 rounded-full border border-sedac-line flex items-center justify-center text-sedac-muted hover:text-sedac-amber hover:border-sedac-amber transition"
            onClick={onClose}
            aria-label="Cerrar modal"
          >
            <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round">
              <path d="M4 4l8 8M12 4l-8 8" />
            </svg>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-5" noValidate>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label htmlFor="f-nombre" className="block text-[12px] tracking-[0.14em] uppercase text-sedac-muted mb-1.5">
                Nombre
              </label>
              <input
                id="f-nombre"
                ref={focused === 'nombre' ? firstRef : firstRef}
                className="w-full rounded-xl border border-sedac-line bg-white px-4 py-3 text-sm outline-none transition placeholder-sedac-muted/60 focus:border-sedac-amber focus:ring-1 focus:ring-sedac-amber"
                placeholder="Tu nombre"
                value={form.nombre}
                onChange={handleChange('nombre')}
              />
              {errors.nombre && <p className="text-[12px] text-accent-red mt-1">{errors.nombre}</p>}
            </div>
            <div>
              <label htmlFor="f-org" className="block text-[12px] tracking-[0.14em] uppercase text-sedac-muted mb-1.5">
                Organización o rol
              </label>
              <input
                id="f-org"
                className="w-full rounded-xl border border-sedac-line bg-white px-4 py-3 text-sm outline-none transition placeholder-sedac-muted/60 focus:border-sedac-amber focus:ring-1 focus:ring-sedac-amber"
                placeholder="Brigada, institución, empresa, equipo…"
                value={form.organizacion}
                onChange={handleChange('organizacion')}
              />
              {errors.organizacion && <p className="text-[12px] text-accent-red mt-1">{errors.organizacion}</p>}
            </div>
          </div>

          <div>
            <label htmlFor="f-rol" className="block text-[12px] tracking-[0.14em] uppercase text-sedac-muted mb-1.5">
              Rol o contexto
            </label>
            <input
              id="f-rol"
              className="w-full rounded-xl border border-sedac-line bg-white px-4 py-3 text-sm outline-none transition placeholder-sedac-muted/60 focus:border-sedac-amber focus:ring-1 focus:ring-sedac-amber"
              placeholder="Operador, diseñador, responsable de equipamiento…"
              value={form.rol}
              onChange={handleChange('rol')}
            />
          </div>

          <div>
            <label className="block text-[12px] tracking-[0.14em] uppercase text-sedac-muted mb-2">
              Interés
            </label>
            <div className="grid grid-cols-2 gap-2">
              {[
                { value: 'presentacion', label: 'Presentación' },
                { value: 'colaboracion', label: 'Colaboración' },
                { value: 'evaluacion', label: 'Evaluación' },
                { value: 'informacion', label: 'Información' },
              ].map((opt) => (
                <label
                  key={opt.value}
                  className={`flex items-center gap-2 rounded-xl border px-3.5 py-2.5 text-sm cursor-pointer transition ${
                    form.interés === opt.value
                      ? 'border-sedac-amber bg-sedac-amber/8 text-sedac-ink'
                      : 'border-sedac-line bg-white text-sedac-muted/95 hover:border-sedac-amber/50'
                  }`}
                >
                  <input
                    type="radio"
                    name="interes"
                    value={opt.value}
                    checked={form.interés === opt.value}
                    onChange={() => setForm((p) => ({ ...p, interes: opt.value }))}
                    className="accent-sedac-amber"
                    aria-label={opt.label}
                  />
                  {opt.label}
                </label>
              ))}
            </div>
            {errors.interes && <p className="text-[12px] text-accent-red mt-1.5">{errors.interes}</p>}
          </div>

          <div>
            <label htmlFor="f-msg" className="block text-[12px] tracking-[0.14em] uppercase text-sedac-muted mb-1.5">
              Mensaje opcional
            </label>
            <textarea
              id="f-msg"
              className="w-full rounded-xl border border-sedac-line bg-white px-4 py-3 text-sm outline-none transition placeholder-sedac-muted/60 focus:border-sedac-amber focus:ring-1 focus:ring-sedac-amber resize-y min-h-[100px]"
              placeholder="Necesidades, contexto, lo que te gustaría ver o preguntar."
              value={form.mensaje}
              onChange={handleChange('mensaje')}
            />
          </div>

          <div className="flex items-center justify-between pt-2">
            <p className="text-[11.5px] text-sedac-muted/80">
              No se envía al hacer clic. Se prepara un archivo listo para enviar.
            </p>
            <button
              type="button"
              className="text-[11px] tracking-[0.14em] uppercase text-sedac-muted hover:text-sedac-amber transition px-3 py-1.5 rounded-lg border border-transparent hover:border-sedac-amber/40"
              onClick={onClose}
            >
              Cancelar
            </button>
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="submit"
              className="flex-1 rounded-full bg-sedac-amber text-graphite-2 font-semibold py-3.5 transition hover:bg-sedac-amber-soft active:scale-[0.98] disabled:opacity-50 disabled:pointer-events-none"
              disabled={status === 'processing'}
            >
              {status === 'processing' ? 'Preparando…' : status === 'ready' ? 'Preparado' : 'Preparar solicitud'}
            </button>
          </div>
        </form>

        {status === 'ready' && (
          <div className="m-0 mx-6 mb-6 rounded-xl border border-sedac-amber/40 bg-sedac-amber/6 px-4 py-3 text-sm text-sedac-ink/95">
            <p className="font-semibold flex items-center gap-2 text-sedac-ink">
              <svg className="w-4 h-4 flex-none text-sedac-amber" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round">
                <path d="M3 8h9M8 3l5 5-5 5" />
              </svg>
              Solicitud preparada; todavía no se envió.
            </p>
            <p className="mt-1 text-[13px] text-sedac-muted/90">
              Se descargó un archivo con tu solicitud. Si no hay destinatario confirmado, envíalo cuando puedas.
            </p>
          </div>
        )}

        {status !== 'ready' && (
          <p className="mt-5 text-[12px] text-sedac-muted/80 border-t border-sedac-line pt-4 text-center">
            No se comparte este contenido ni se envía sin tu acción posterior.
          </p>
        )}
      </div>
    </div>
  );
}

function buildRequest({ nombre, organizacion, rol, interes, mensaje }) {
  const lines = [
    'SEDAC — Solicitud de presentación',
    '-----------------------------------',
    '',
    `Nombre: ${nombre || '—'}`,
    `Organización o rol: ${organizacion || '—'}`,
    `Rol o contexto: ${rol || '—'}`,
    `Interés: ${labelInteres(interes)}`,
    '',
    'Selección: este formulario no se envió automáticamente.',
    'La solicitud está preparada para copiar o enviar.',
    '',
  ];
  if (mensaje.trim()) {
    lines.push('Mensaje:', '', mensaje.trim(), '');
  }
  lines.push('', 'Producto en desarrollo · prediseño CAD · validación física pendiente');
  return { text: lines.join('\n') };
}

function labelInteres(v) {
  return ({ presentacion: 'Presentación', colaboracion: 'Colaboración', evaluacion: 'Evaluación', informacion: 'Información' })[v] ?? v;
}

function slug(s) {
  return (s ?? '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}
