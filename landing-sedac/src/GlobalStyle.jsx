const prefersReduced = typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const CSS = `
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

  *, *::before, *::after { box-sizing: border-box; }

  :root {
    --graphite: #141613;
    --graphite-2: #1d201b;
    --graphite-3: #2a2e27;
    --paper: #f7f4ec;
    --paper-2: #ede8dc;
    --ink: #191b17;
    --muted: #6c7066;
    --muted-dark: #a2a89b;
    --amber: #ffc21a;
    --amber-deep: #e0a400;
    --amber-soft: rgba(255,194,26,0.12);
    --line: rgba(25,27,23,0.14);
    --line-dark: rgba(247,244,236,0.16);
    --max: 1180px;
    --pad: clamp(20px, 5vw, 64px);
    --r: 14px;
    --font-display: "Outfit", "Helvetica Neue", system-ui, sans-serif;
    --font-body: "Inter", "Helvetica Neue", system-ui, sans-serif;
    --font-mono: ui-monospace, "SF Mono", Menlo, monospace;
  }

  html {
    scroll-behavior: ${prefersReduced ? 'auto' : 'smooth'};
  }
  section[id] { scroll-margin-top: 84px; }
  @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }

  body {
    margin: 0;
    background: var(--paper);
    color: var(--ink);
    font-family: var(--font-body);
    font-size: 16px;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }

  img, svg { display: block; max-width: 100%; }
  a { color: inherit; text-decoration: none; }
  button { font-family: inherit; }

  h1, h2, h3, h4 {
    margin: 0;
    line-height: 1.02;
    letter-spacing: -0.02em;
    font-weight: 700;
    font-family: var(--font-display);
  }

  p { margin: 0 0 1em; }

  .wrap { width: 100%; max-width: var(--max); margin: 0 auto; padding: 0 var(--pad); }

  :focus-visible {
    outline: 3px solid var(--amber);
    outline-offset: 3px;
    border-radius: 4px;
  }

  ::selection { background: var(--amber); color: #17190f; }
`;

export default function GlobalStyle() {
  return <style dangerouslySetInnerHTML={{ __html: CSS }} />;
}
