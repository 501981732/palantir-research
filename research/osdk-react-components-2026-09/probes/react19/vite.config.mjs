import { defineConfig } from 'vite';
export default defineConfig({
  test: {
    environment: 'happy-dom', include: ['checks.test.jsx'], css: false,
    server: { deps: { inline: ['@osdk/react-components'] } },
  },
});
