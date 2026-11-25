import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { apiUrl } from '../../services/api'

export interface Centro {
  id: number
  nombre: string
  provincia: string
  canton: string
  parroquia: string
  provinciaId: string
  cantonId: string
  parroquiaId: string
  direccion: string
  referencia: string
  corte: string
  lat: number
  lng: number
}
export interface ResultadoCentro extends Centro { distancia: number | null }
export interface Ubicacion { lat: number; lng: number }

export function nombreLegible(value: string): string {
  return value.toLocaleLowerCase('es').replace(/(^|[\s/-])\p{L}/gu, char => char.toLocaleUpperCase('es'))
}
function texto(value: unknown): string { return typeof value === 'string' ? value.trim() : '' }
function normalize(value: string): string {
  return value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('es')
}
function km(a: Ubicacion, b: Ubicacion): number {
  const rad = Math.PI / 180
  const h = Math.sin((b.lat - a.lat) * rad / 2) ** 2 +
    Math.cos(a.lat * rad) * Math.cos(b.lat * rad) * Math.sin((b.lng - a.lng) * rad / 2) ** 2
  return 6371.0088 * 2 * Math.atan2(Math.sqrt(Math.min(1, h)), Math.sqrt(Math.max(0, 1 - h)))
}
export function distanciaLegible(value: number): string {
  return value < 1 ? `${Math.max(1, Math.round(value * 1000))} m` : `${value.toLocaleString('es-EC', { maximumFractionDigits: 1 })} km`
}
export function comoLlegar(centro: Centro): string {
  return `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(`${centro.lat},${centro.lng}`)}`
}

export function useCentros() {
  const centros = ref<Centro[]>([])
  const cargando = ref(false)
  const cargado = ref(false)
  const error = ref('')
  const sinCoordenadas = ref(0)
  const provincia = ref('')
  const canton = ref('')
  const parroquia = ref('')
  const busqueda = ref('')
  const seleccion = ref<number | null>(null)
  const ubicacion = ref<Ubicacion | null>(null)
  const ubicando = ref(false)
  const avisoUbicacion = ref('')
  const limite = ref(12)
  let geoRequest = 0
  let disposed = false
  let request: AbortController | null = null

  async function cargar() {
    if (cargando.value || cargado.value) return
    request = new AbortController()
    const timeout = window.setTimeout(() => request?.abort(), 25000)
    cargando.value = true
    error.value = ''
    try {
      const params = new URLSearchParams({ limit: '0', servicio: 'DESARROLLO INFANTIL INTEGRAL' })
      const response = await fetch(apiUrl(`/unidades?${params}`), { signal: request.signal })
      if (!response.ok) throw new Error('No se pudo consultar el servicio.')
      const result = await response.json()
      if (!Array.isArray(result.features) || !Number.isSafeInteger(result.total) ||
          result.total !== result.features.length) throw new Error('La respuesta está incompleta.')
      const parsed: Centro[] = []
      let omitted = 0
      const ids = new Set<number>()
      for (const feature of result.features) {
        const p = feature?.properties
        if (!p || p.servicio !== 'DESARROLLO INFANTIL INTEGRAL' ||
            p.mod !== 'CENTROS DE DESARROLLO INFANTIL - CDI') continue
        const coordinates = feature.geometry?.coordinates
        const lng = coordinates?.[0]
        const lat = coordinates?.[1]
        if (feature.geometry?.type !== 'Point' || !Number.isFinite(lng) || !Number.isFinite(lat) ||
            Math.abs(lng) > 180 || Math.abs(lat) > 90 || (lat === 0 && lng === 0)) {
          omitted++
          continue
        }
        if (!Number.isSafeInteger(p.id) || ids.has(p.id)) throw new Error('Identificadores no válidos.')
        ids.add(p.id)
        const provinceId = texto(p.dpa_prov) || texto(p.dpa_despro)
        const cantonId = JSON.stringify([provinceId, texto(p.dpa_can) || texto(p.dpa_descan)])
        const parishId = JSON.stringify([cantonId, texto(p.dpa_par) || texto(p.dpa_despar)])
        parsed.push({
          id: p.id, nombre: texto(p.nombre) || 'Centro de Desarrollo Infantil',
          provincia: texto(p.dpa_despro), canton: texto(p.dpa_descan), parroquia: texto(p.dpa_despar),
          provinciaId: provinceId, cantonId, parroquiaId: parishId,
          direccion: texto(p.dir), referencia: texto(p.ref), corte: texto(p.corte), lat, lng,
        })
      }
      if (disposed) return
      centros.value = parsed
      sinCoordenadas.value = omitted
      cargado.value = true
    } catch (cause) {
      if (!disposed) {
        error.value = 'No pudimos cargar los centros. Puedes volver a intentarlo; la orientación sigue disponible.'
      }
    } finally { window.clearTimeout(timeout); if (!disposed) cargando.value = false }
  }

  function options(items: Centro[], key: 'provincia' | 'canton' | 'parroquia', id: 'provinciaId' | 'cantonId' | 'parroquiaId') {
    const values = new Map<string, string>()
    for (const item of items) if (item[key] && item[id]) values.set(item[id], nombreLegible(item[key]))
    return [...values].map(([value, label]) => ({ value, label })).sort((a, b) => a.label.localeCompare(b.label, 'es'))
  }
  const provincias = computed(() => options(centros.value, 'provincia', 'provinciaId'))
  const cantones = computed(() => options(centros.value.filter(c => c.provinciaId === provincia.value), 'canton', 'cantonId'))
  const parroquias = computed(() => options(centros.value.filter(c => c.provinciaId === provincia.value && c.cantonId === canton.value), 'parroquia', 'parroquiaId'))
  watch(provincia, () => { canton.value = ''; parroquia.value = '' }, { flush: 'sync' })
  watch(canton, () => { parroquia.value = '' }, { flush: 'sync' })
  watch([provincia, canton, parroquia], () => {
    if (ubicacion.value || ubicando.value) quitarUbicacion()
  }, { flush: 'sync' })
  const resultados = computed<ResultadoCentro[]>(() => {
    const q = normalize(busqueda.value.trim())
    return centros.value.filter(c =>
      (!provincia.value || c.provinciaId === provincia.value) &&
      (!canton.value || c.cantonId === canton.value) &&
      (!parroquia.value || c.parroquiaId === parroquia.value) &&
      (!q || normalize(`${c.nombre} ${c.direccion} ${c.parroquia} ${c.canton}`).includes(q)),
    ).map(c => ({ ...c, distancia: ubicacion.value ? km(ubicacion.value, c) : null }))
      .sort((a, b) => (a.distancia !== null && b.distancia !== null ? a.distancia - b.distancia : 0) ||
        a.nombre.localeCompare(b.nombre, 'es') || a.id - b.id)
  })
  const visibles = computed(() => resultados.value.slice(0, limite.value))
  const seleccionado = computed(() => resultados.value.find(c => c.id === seleccion.value) || null)
  const distribucion = computed(() => {
    const counts = new Map<string, number>()
    for (const centro of resultados.value) {
      const label = nombreLegible(centro.provincia || 'Sin provincia informada')
      counts.set(label, (counts.get(label) || 0) + 1)
    }
    const sorted = [...counts].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'es'))
    const top = sorted.slice(0, 3)
    if (sorted.length > 3) top.push(['Otros', sorted.slice(3).reduce((sum, [, count]) => sum + count, 0)])
    return top.map(([label, count]) => ({ label, count, percent: count / resultados.value.length * 100 }))
  })
  watch([provincia, canton, parroquia, busqueda, ubicacion], () => { limite.value = 12; seleccion.value = null }, { flush: 'sync' })
  function seleccionar(id: number) {
    const position = resultados.value.findIndex(c => c.id === id)
    if (position < 0) return
    limite.value = Math.max(limite.value, Math.ceil((position + 1) / 12) * 12)
    seleccion.value = id
  }
  function limpiarFiltros() { provincia.value = ''; canton.value = ''; parroquia.value = ''; busqueda.value = '' }
  function quitarUbicacion() {
    geoRequest++
    ubicando.value = false
    ubicacion.value = null
    avisoUbicacion.value = ''
  }
  function localizar() {
    if (ubicando.value) return
    if (!navigator.geolocation) {
      avisoUbicacion.value = 'Este navegador no permite usar tu ubicación. Elige una provincia para buscar.'
      return
    }
    const token = ++geoRequest
    ubicando.value = true
    avisoUbicacion.value = 'Tu navegador te pedirá permiso. La ubicación solo se usa para ordenar los centros.'
    navigator.geolocation.getCurrentPosition(position => {
      if (disposed || token !== geoRequest) return
      ubicando.value = false
      const { latitude: lat, longitude: lng } = position.coords
      if (!Number.isFinite(lat) || !Number.isFinite(lng) || Math.abs(lat) > 90 || Math.abs(lng) > 180) {
        avisoUbicacion.value = 'No obtuvimos una ubicación válida. Puedes buscar por provincia.'
        return
      }
      provincia.value = ''; canton.value = ''; parroquia.value = ''
      ubicacion.value = { lat, lng }
      avisoUbicacion.value = 'Ubicación activa. Centros ordenados por cercanía; distancia en línea recta.'
    }, () => {
      if (disposed || token !== geoRequest) return
      ubicando.value = false
      avisoUbicacion.value = 'No pudimos obtener tu ubicación. Puedes elegir provincia, cantón y parroquia sin dar permiso.'
    }, { timeout: 12000, maximumAge: 60000, enableHighAccuracy: false })
  }
  onBeforeUnmount(() => { disposed = true; geoRequest++; request?.abort() })
  return {
    centros, cargando, cargado, error, sinCoordenadas, cargar, provincia, canton, parroquia,
    busqueda, provincias, cantones, parroquias, resultados, visibles, limite, seleccionado,
    seleccion, seleccionar, limpiarFiltros, distribucion, ubicacion, ubicando, avisoUbicacion,
    localizar, quitarUbicacion,
  }
}
