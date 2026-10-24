import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [
    react({
      runtime: 'automatic',
      importSource: 'react',
      babel: false,
    }),
  ],
  build: {
    target: 'es2020',
  },
});
