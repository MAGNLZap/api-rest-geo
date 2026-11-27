import { fileURLToPath, URL } from 'node:url'
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const base = env.VITE_PUBLIC_BASE || '/'
  if (!base.startsWith('/') || !base.endsWith('/') || base.includes('//')) {
    throw new Error('VITE_PUBLIC_BASE debe ser una ruta con / inicial y final, por ejemplo /.')
  }
  const apiProxy = {
    target: env.API_PROXY_TARGET || 'http://127.0.0.1:8001',
    changeOrigin: true,
  }
  return {
    base,
    plugins: [vue()],
    resolve: {
      alias: {
        '@portal': fileURLToPath(new URL('../app/static/portal', import.meta.url)),
        '@amenazas': fileURLToPath(new URL('../app/static/ua_amenazas', import.meta.url)),
        '@demo': fileURLToPath(new URL('../demo', import.meta.url)),
      },
    },
    server: {
      host: '127.0.0.1',
      port: 5173,
      strictPort: true,
      fs: {
        allow: [
          fileURLToPath(new URL('.', import.meta.url)),
          fileURLToPath(new URL('../app/static', import.meta.url)),
          fileURLToPath(new URL('../demo/patron-topografico.svg', import.meta.url)),
        ],
      },
      watch: env.CHOKIDAR_USEPOLLING === 'true' ? { usePolling: true } : undefined,
      proxy: {
        '^/unidades(?:/|\\?|$)': apiProxy,
        '^/dpa(?:/|\\?|$)': apiProxy,
        '^/ua_amenazas/data(?:/|\\?|$)': apiProxy,
        '^/(?:health|docs|redoc|openapi\\.json)(?:/|\\?|$)': apiProxy,
      },
    },
    preview: {
      host: '127.0.0.1',
      port: 4173,
      strictPort: true,
    },
  }
})
