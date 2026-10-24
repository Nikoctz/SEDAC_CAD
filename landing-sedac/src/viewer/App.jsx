import { forwardRef } from 'react';

const ViewerShell = forwardRef(({ children, label, description, ...rest }, ref) => {
  return (
    <div
      ref={ref}
      className="product-stage"
      role="region"
      aria-label={label}
      {...rest}
    >
      <div className="viewport" aria-label={description}>
        <div className="img-frame">{children}</div>
        <div className="slider-deco" aria-hidden="true" />
        <div className="grain-overlay" aria-hidden="true" />
        <div className="tag-banner">
          <strong>Vista</strong> · movimiento con el ratón o dedos
        </div>
        <div className="zoom-hint" aria-hidden="true">
          <svg className="w-4 h-4" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round">
            <circle cx="7" cy="7" r="4.5" />
            <path d="M10.5 10.5 L13 13" />
            <path d="M5.5 7 L8.5 7 L8.5 10.5" />
          </svg>
          Ampliar · clic o doble toque
        </div>
      </div>
    </div>
  );
});

ViewerShell.displayName = 'ViewerShell';

export default ViewerShell;
