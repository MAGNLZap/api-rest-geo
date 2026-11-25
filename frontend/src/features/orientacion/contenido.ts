import snapshot from './catalogo.json'
import { redaccion, fechaRedaccion, type ComplementoServicio } from './redaccion'

export interface Servicio {
  id: string
  title: string
  short: string
  who: string
  access: string
  description: string
  important?: string
  complements?: ComplementoServicio[]
  sources: { label: string; url: string }[]
  map?: boolean
}
export interface Publico {
  id: string
  label: string
  needs: [string, string, string[]][]
}
export const publicos = snapshot.paths as Publico[]
export const fechaContenido = snapshot.capturedAt
export { fechaRedaccion }
export const fuentePiloto = 'https://sgde-mtdh.github.io/Geoportal-MTDH/servicios/index.html'
export const fuenteInstitucional = 'https://www.desarrollohumano.gob.ec/programas-y-servicios/'
export const fuenteAsesor = 'https://asesor593.trabajo.gob.ec/'
const nombresAsesor: Record<string, string> = {
  'solicitud-de-adopcion-nacional-de-ninas-ninos-y-adolescentes-con': 'Solicitud de adopción nacional',
  'otorgamiento-de-permisos-de-funcionamiento-para-centros-de-desar': 'Permiso de funcionamiento CDI',
}
export const servicios: Servicio[] = snapshot.services.map(original => {
  const texto = redaccion[original.id]
  if (!texto) throw new Error(`Falta la redacción del servicio ${original.id}.`)
  const ids = [...new Set([...(texto.asesorIds || []), ...(texto.complements || []).map(item => item.sourceId)])]
  return {
    ...original, ...texto,
    sources: [
      { label: 'Catálogo del piloto', url: fuentePiloto },
      ...ids.map(id => ({
        label: `Asesor593: ${texto.complements?.find(item => item.sourceId === id)?.title || nombresAsesor[id] || original.title}`,
        url: `https://asesor593.trabajo.gob.ec/servicios/${id}`,
      })),
    ],
  }
})
export const iconosPublico: Record<string, string> = {
  infancia: 'child', mayor: 'senior', discapacidad: 'access',
  familia: 'family', proteccion: 'shield', otros: 'help',
}
export const iconosNecesidad: Record<string, string> = {
  'infancia/cuidado': 'nursery', 'infancia/proteccion': 'shield', 'infancia/otra': 'grid',
  'mayor/atencion': 'senior', 'mayor/dinero': 'coins', 'mayor/otra': 'grid',
  'discapacidad/atencion': 'access', 'discapacidad/bono': 'coins', 'discapacidad/otra': 'hand-heart',
  'familia/credito': 'briefcase', 'familia/emergencia': 'lifebuoy', 'familia/bonos': 'wallet', 'familia/otra': 'family',
  'proteccion/derechos': 'shield', 'proteccion/orfandad': 'hand-heart', 'proteccion/otra': 'message',
  'otros/adopcion': 'heart-home', 'otros/joven': 'graduation', 'otros/tramite': 'clipboard', 'otros/otra': 'grid',
}
export const iconosServicio: Record<string, string> = {
  cdi: 'nursery', cnh: 'heart-home', adulto: 'senior', discapacidad: 'access',
  proteccion: 'shield', adopcion: 'heart', credito: 'wallet', bonos: 'coins',
  contingencia: 'lifebuoy', jovenes: 'graduation', emprendimiento: 'briefcase',
  orfandad: 'hand-heart', sustituto: 'badge', bjl: 'hand-heart', ciudadania: 'message',
  organizaciones: 'community', permisos: 'clipboard', acompanamiento: 'family',
}
export const etiquetasPublico: Record<string, string> = {
  infancia: 'Desarrollo infantil, protección y otras ayudas',
  mayor: 'Cuidado, actividades y apoyo económico',
  discapacidad: 'Atención, bonos y otros apoyos',
  familia: 'Apoyo familiar, emprendimiento y ayudas económicas',
  proteccion: 'Orientación ante vulneración de derechos',
  otros: 'Adopción, formación, información y trámites',
}
export const categoriasServicio: Record<string, string> = {
  cdi: 'Cuidado infantil', cnh: 'Desarrollo infantil', adulto: 'Personas mayores',
  discapacidad: 'Discapacidad', proteccion: 'Protección', adopcion: 'Adopciones',
  credito: 'Inclusión económica', bonos: 'Apoyo económico', contingencia: 'Apoyo familiar',
  jovenes: 'Juventudes', emprendimiento: 'Emprendimiento', orfandad: 'Apoyo económico',
  sustituto: 'Certificaciones', bjl: 'Apoyo económico', ciudadania: 'Atención ciudadana',
  organizaciones: 'Organizaciones', permisos: 'Trámites', acompanamiento: 'Apoyo familiar',
}
