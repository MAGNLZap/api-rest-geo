const publicBase = import.meta.env.BASE_URL.replace(/\/$/, '')
const apiBase = (import.meta.env.VITE_API_BASE ?? publicBase).replace(/\/$/, '')

export function apiUrl(path: string): string {
  return `${apiBase}/${path.replace(/^\.?\//, '')}`
}

export function portalUrl(path = ''): string {
  return `${publicBase}/${path.replace(/^\//, '')}`
}

export function pagePath(path: string): string {
  const local = publicBase && path.startsWith(`${publicBase}/`)
    ? path.slice(publicBase.length)
    : path
  return local.replace(/\/$/, '') || '/'
}
