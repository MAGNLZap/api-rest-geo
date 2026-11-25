<script setup lang="ts">
import { computed, defineAsyncComponent, h, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import SocialIcon from '../components/SocialIcon.vue'
import InstitutionalFooter from '../components/InstitutionalFooter.vue'
import AnimatedNumber from '../components/AnimatedNumber.vue'
import { portalUrl } from '../services/api'
import orientacionAcompanamiento from '../assets/illustrations/orientacion-acompanamiento.png'
import {
  servicios, publicos, fechaContenido, fechaRedaccion, fuentePiloto, fuenteAsesor, fuenteInstitucional,
  iconosPublico, iconosNecesidad, iconosServicio, etiquetasPublico, categoriasServicio, type Servicio,
} from '../features/orientacion/contenido'
import { useCentros, comoLlegar, distanciaLegible, nombreLegible } from '../features/orientacion/useCentros'
import '../styles/servicios.css'
import '../styles/servicios-resultados.css'
import '../styles/orientacion-typography.css'

const ServiciosMap = defineAsyncComponent({
  loader: () => import('../components/ServiciosMap.vue'),
  loadingComponent: { render: () => h('p', { class: 'social-map-placeholder', role: 'status' }, 'Preparando el mapa…') },
  errorComponent: { render: () => h('p', { class: 'social-map-placeholder', role: 'alert' }, 'No se pudo preparar el mapa. Usa el listado o recarga la página.') },
  timeout: 20000,
})
document.title = 'Encuentra orientación y servicios sociales'
const paso = ref<'publico' | 'necesidad' | 'resultados' | 'centros'>('publico')
const publicoId = ref('')
const necesidadId = ref('')
const verCatalogo = ref(false)
const consultaCatalogo = ref('')
const servicioAbierto = ref<Servicio | null>(null)
const presentacion = ref<'list' | 'map'>('list')
const heading = ref<HTMLElement | null>(null)
const detail = ref<HTMLDialogElement | null>(null)
const finCentros = ref<HTMLElement | null>(null)
const cargaAutomatica = typeof IntersectionObserver !== 'undefined'
let observadorCentros: IntersectionObserver | null = null
let returnFocus: HTMLElement | null = null
const publico = computed(() => publicos.find(p => p.id === publicoId.value))
const necesidad = computed(() => publico.value?.needs.find(n => n[0] === necesidadId.value))
const resultados = computed(() => {
  const ids = necesidad.value?.[2] || []
  const selected = verCatalogo.value || ids.length === 0
    ? servicios : ids.map(id => servicios.find(s => s.id === id)!).filter(Boolean)
  const query = consultaCatalogo.value.toLocaleLowerCase('es').normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  return selected.filter(s => `${s.title} ${s.short}`.toLocaleLowerCase('es').normalize('NFD').replace(/[\u0300-\u036f]/g, '').includes(query))
})
const {
  cargando, cargado, error, sinCoordenadas, cargar, provincia, canton, parroquia,
  busqueda, provincias, cantones, parroquias, resultados: centros, visibles, limite,
  seleccionado, seleccionar, limpiarFiltros, distribucion, ubicacion, ubicando,
  avisoUbicacion, localizar, quitarUbicacion,
} = useCentros()
function mostrarMasCentros() {
  if (paso.value === 'centros' && cargado.value && !cargando.value) {
    limite.value = Math.min(limite.value + 12, centros.value.length)
  }
}
watch(finCentros, elemento => {
  observadorCentros?.disconnect()
  observadorCentros = null
  if (!elemento || !cargaAutomatica) return
  observadorCentros = new IntersectionObserver(entries => {
    if (entries.some(entry => entry.isIntersecting)) mostrarMasCentros()
  }, { rootMargin: '0px 0px 160px 0px' })
  observadorCentros.observe(elemento)
}, { flush: 'post' })
const territorio = computed(() => parroquias.value.find(p => p.value === parroquia.value)?.label ||
  cantones.value.find(c => c.value === canton.value)?.label ||
  provincias.value.find(p => p.value === provincia.value)?.label || 'Todo Ecuador')
const title = computed(() => ({
  publico: '¿Para quién buscas ayuda?',
  necesidad: '¿Qué necesitas?',
  resultados: verCatalogo.value ? 'Conoce los servicios sociales' : 'Estas opciones pueden ayudarte',
  centros: 'Encuentra un centro infantil',
})[paso.value])
const activeStep = computed(() => paso.value === 'publico' ? 1 : paso.value === 'necesidad' ? 2 : 3)
const consultaDirecta = computed(() => verCatalogo.value && (paso.value === 'resultados' || paso.value === 'centros'))
const progressDescription = computed(() => ({
  publico: '',
  necesidad: 'Cuéntanos qué necesitas',
  resultados: 'Explora tus opciones de ayuda',
  centros: 'Consulta las ubicaciones de centros',
})[paso.value])
async function focusHeading() { await nextTick(); heading.value?.focus() }
watch(paso, () => {
  focusHeading()
  window.scrollTo({ top: 0, behavior: 'instant' })
})
function elegirPublico(id: string) {
  if (publicoId.value !== id) { publicoId.value = id; necesidadId.value = ''; servicioAbierto.value = null }
  paso.value = 'necesidad'
}
function elegirNecesidad(id: string) {
  necesidadId.value = id
  verCatalogo.value = false
  consultaCatalogo.value = ''
  paso.value = 'resultados'
}
function catalogo() { verCatalogo.value = true; consultaCatalogo.value = ''; paso.value = 'resultados' }
function volver() {
  if (paso.value === 'centros') paso.value = 'resultados'
  else if (paso.value === 'resultados') paso.value = necesidad.value && !verCatalogo.value ? 'necesidad' : 'publico'
  else paso.value = 'publico'
}
function iniciar() {
  cerrarDetalle()
  publicoId.value = ''; necesidadId.value = ''; consultaCatalogo.value = ''; verCatalogo.value = false
  limpiarFiltros(); quitarUbicacion()
  paso.value = 'publico'
  focusHeading()
}
function abrirServicio(servicio: Servicio, event: Event) {
  returnFocus = event.currentTarget as HTMLElement
  servicioAbierto.value = servicio
  nextTick(() => detail.value?.showModal())
}
function cerrarDetalle() { detail.value?.close() }
function detalleCerrado() {
  servicioAbierto.value = null
  returnFocus?.focus()
}
function buscarCentros() {
  cerrarDetalle()
  paso.value = 'centros'
  presentacion.value = 'list'
  cargar()
}
onMounted(() => {
  if (new URLSearchParams(window.location.search).get('vista') === 'centros') {
    verCatalogo.value = true
    buscarCentros()
    presentacion.value = 'map'
  }
})
async function seleccionarCentro(id: number) {
  seleccionar(id)
  presentacion.value = 'map'
  await nextTick()
  document.getElementById('social-selected-detail')?.focus({ preventScroll: false })
}
const estadoResultados = computed(() => cargando.value ? 'Cargando centros…'
  : error.value ? 'No se pudieron cargar los centros.'
  : `${centros.value.length.toLocaleString('es-EC')} centros en ${territorio.value}.`)
onBeforeUnmount(() => { detail.value?.close(); observadorCentros?.disconnect() })
</script>

<template>
  <div class="social-page">
    <a class="social-skip" href="#social-content">Ir al contenido</a>
    <header class="social-header">
      <a class="social-brand" :href="portalUrl()" aria-label="Ir al inicio del geoportal">
        <span class="social-brand-mark"><SocialIcon name="hand-heart" :size="30" /></span>
        <span><strong>Orientación y servicios sociales</strong><small>Ministerio de Trabajo y Desarrollo Humano</small></span>
      </a>
      <nav class="social-header-nav" aria-label="Navegación de servicios">
        <a :href="portalUrl()" class="social-home-link" aria-label="Volver al inicio" title="Volver al inicio"><SocialIcon name="home" :size="21" /><span>Inicio</span></a>
        <button type="button" class="social-header-explore" @click="catalogo"><SocialIcon name="grid" :size="18" /><span>Explorar servicios</span></button>
        <button type="button" class="social-original-link" @click="buscarCentros(); presentacion = 'map'"><SocialIcon name="map" :size="21" /> Centros infantiles <SocialIcon name="chevron-right" :size="16" /></button>
      </nav>
    </header>

    <main id="social-content" :class="['social-main', { 'social-main--explore': paso === 'centros' }]">

      <section class="social-heading" :class="{ 'social-heading--compact': paso === 'centros', 'social-heading--with-back': paso !== 'publico' }">
        <div>
          <div class="social-heading-title">
            <button v-if="paso !== 'publico'" type="button" class="social-back" @click="volver"><SocialIcon name="chevron-left" :size="22" /> Volver</button>
            <h1 ref="heading" tabindex="-1">{{ title }}</h1>
          </div>
          <p v-if="paso === 'publico'">Encuentra orientación sobre los servicios del Ministerio para ti y tu familia.</p>
          <p v-else-if="paso === 'necesidad'">Buscas ayuda para <strong>{{ publico?.label.toLocaleLowerCase('es') }}</strong>. Elige lo que mejor describa tu necesidad.</p>
          <p v-else-if="paso === 'resultados'">{{ verCatalogo ? 'Conoce qué ofrece cada servicio, a quién está dirigido y cómo acceder.' : 'Estas opciones corresponden a la necesidad que elegiste. Consulta qué ofrecen y cómo acceder.' }}</p>
          <p v-else>Centros de Desarrollo Infantil para niñas y niños de 1 a 3 años. Consulta sus ubicaciones y solicita orientación sobre el ingreso.</p>
        </div>
        <img v-if="paso === 'publico'" class="social-hero-art" :src="orientacionAcompanamiento" alt="" aria-hidden="true">
      </section>

      <div v-if="!consultaDirecta" class="social-progress">
        <div class="social-progress-caption"><strong>Paso {{ activeStep }} de 3</strong><span v-if="progressDescription">{{ progressDescription }}</span></div>
        <div class="social-progress-track" role="progressbar" aria-label="Avance de orientación" :aria-valuenow="activeStep - 1" :aria-valuemax="2" :aria-valuemin="0" :aria-valuetext="`Paso ${activeStep} de 3${progressDescription ? `. ${progressDescription}` : ''}`"><span :style="{ width: `${(activeStep - 1) * 50}%` }"></span></div>
        <ol class="social-steps" aria-label="Pasos de orientación">
          <li :aria-current="activeStep === 1 ? 'step' : undefined" :class="{ done: activeStep > 1 }"><span><SocialIcon v-if="activeStep > 1" name="check" :size="13" /><template v-else>1</template></span><b>Para quién</b></li>
          <li :aria-current="activeStep === 2 ? 'step' : undefined" :class="{ done: activeStep > 2 }"><span><SocialIcon v-if="activeStep > 2" name="check" :size="13" /><template v-else>2</template></span><b>Qué necesitas</b></li>
          <li :aria-current="activeStep === 3 ? 'step' : undefined"><span>3</span><b>Opciones de ayuda</b></li>
        </ol>
      </div>

      <template v-if="paso === 'publico' || paso === 'necesidad'">
        <section class="social-question-form" aria-label="Selecciona una opción para avanzar">
          <fieldset>
            <legend class="social-sr-only">{{ title }}</legend>
            <div v-if="paso === 'publico'" class="social-audiences">
              <button v-for="p in publicos" :key="p.id" type="button" :aria-pressed="publicoId === p.id" :class="['social-choice', { chosen: publicoId === p.id }]" @click="elegirPublico(p.id)">
                <span class="social-choice-icon"><SocialIcon :name="iconosPublico[p.id] || 'compass'" :size="30" /></span>
                <span class="social-choice-text"><strong>{{ p.label }}</strong><small>{{ etiquetasPublico[p.id] }}</small></span>
                <span class="social-choice-check" aria-hidden="true"><SocialIcon v-if="publicoId === p.id" name="check" :size="16" /></span>
              </button>
            </div>
            <div v-else class="social-needs">
              <button v-for="need in publico?.needs" :key="need[0]" type="button" :aria-pressed="necesidadId === need[0]" :class="['social-choice', { chosen: necesidadId === need[0] }]" @click="elegirNecesidad(need[0])">
                <span class="social-choice-icon"><SocialIcon :name="iconosNecesidad[`${publicoId}/${need[0]}`] || 'compass'" :size="28" /></span>
                <span class="social-choice-text"><strong>{{ need[1] }}</strong></span>
                <span class="social-choice-check" aria-hidden="true"><SocialIcon v-if="necesidadId === need[0]" name="check" :size="16" /></span>
              </button>
            </div>
          </fieldset>
          <div class="social-question-actions">
            <p>Solo orientación. No necesitas ingresar documentos ni datos personales.</p>
          </div>
        </section>
        <div class="social-browse-invite"><SocialIcon name="compass" :size="22" /><p>¿Prefieres conocer todas las opciones?</p><button type="button" class="social-inline-action" @click="catalogo">Ver los 18 servicios <SocialIcon name="chevron-right" :size="18" /></button></div>
      </template>

      <template v-else-if="paso === 'resultados'">
        <div v-if="!verCatalogo && publico && necesidad" class="social-answer-summary">
          <span>{{ publico.label }}</span><span>{{ necesidad[1] }}</span>
          <button type="button" class="social-inline-action" @click="paso = 'publico'"><SocialIcon name="edit" :size="17" /> Cambiar respuestas</button>
        </div>
        <label v-if="verCatalogo || !necesidad?.[2].length" class="social-catalog-search">
          <SocialIcon name="search" :size="21" /><span class="social-sr-only">Buscar un servicio</span>
          <input v-model="consultaCatalogo" type="search" placeholder="Busca por nombre o tipo de ayuda">
        </label>
        <p class="social-disclaimer">Estas opciones son informativas. La institución verifica requisitos y disponibilidad de atención.</p>
        <div class="social-service-list">
          <article v-for="service in resultados" :key="service.id" class="social-service" :aria-labelledby="`service-title-${service.id}`">
            <div class="social-service-main">
              <span class="social-service-icon"><SocialIcon :name="iconosServicio[service.id] || 'compass'" :size="34" /></span>
              <div class="social-service-copy"><small>{{ categoriasServicio[service.id] }}</small><h2 :id="`service-title-${service.id}`">{{ service.title }}</h2><p>{{ service.short }}</p></div>
              <span class="social-service-detail-label" aria-hidden="true"><span>Ver detalles</span><SocialIcon name="chevron-right" :size="23" /></span>
              <button type="button" class="social-service-open" :aria-label="`Ver detalles de ${service.title}`" @click="abrirServicio(service, $event)"></button>
            </div>
            <div v-if="service.id === 'cdi'" class="social-service-map-action">
              <p><SocialIcon name="pin" :size="17" /> Consulta las ubicaciones de los Centros de Desarrollo Infantil</p>
              <button type="button" class="social-button social-map-cta" @click="buscarCentros"><SocialIcon name="map" :size="22" /> Ver centros en el mapa <SocialIcon name="chevron-right" :size="20" /></button>
            </div>
          </article>
        </div>
        <div v-if="!resultados.length" class="social-empty"><SocialIcon name="search" :size="34" /><h2>No encontramos ese servicio</h2><p>Prueba con otra palabra o consulta todas las opciones.</p><button type="button" class="social-button social-button--light" @click="consultaCatalogo = ''"><SocialIcon name="grid" :size="19" /> Ver todos</button></div>
        <div class="social-bottom-actions"><button v-if="!verCatalogo" type="button" class="social-text-button" @click="catalogo"><SocialIcon name="grid" :size="18" /> Explorar los 18 servicios</button><button type="button" class="social-text-button" @click="iniciar"><SocialIcon name="reset" :size="18" /> Empezar de nuevo</button></div>
      </template>

      <template v-else>
        <section class="social-location-search" aria-label="Buscar centros por ubicación">
          <div class="social-location-field">
            <span class="social-location-label">Mi ubicación</span>
            <button type="button" :class="['social-button', 'social-location-toggle', { 'is-active': ubicacion }]" :disabled="!cargado" :aria-pressed="!!ubicacion" :aria-label="ubicando ? 'Cancelar búsqueda de ubicación' : ubicacion ? 'Desactivar mi ubicación' : 'Activar mi ubicación'" :title="ubicando ? 'Cancelar búsqueda' : ubicacion ? 'Pulsa para desactivar tu ubicación' : 'Ordenar centros por cercanía'" @click="ubicacion || ubicando ? quitarUbicacion() : localizar()"><SocialIcon name="locate" :size="19" /><span>{{ ubicando ? 'Buscando…' : ubicacion ? 'Ubicación activa' : 'Usar mi ubicación' }}</span></button>
          </div>
          <div class="social-territory">
            <label>Provincia<select v-model="provincia" :disabled="!cargado"><option value="">Todo Ecuador</option><option v-for="p in provincias" :key="p.value" :value="p.value">{{ p.label }}</option></select></label>
            <label>Cantón<select v-model="canton" :disabled="!provincia || !cargado"><option value="">Todos los cantones</option><option v-for="c in cantones" :key="c.value" :value="c.value">{{ c.label }}</option></select></label>
            <label>Parroquia<select v-model="parroquia" :disabled="!canton || !cargado"><option value="">Todas las parroquias</option><option v-for="p in parroquias" :key="p.value" :value="p.value">{{ p.label }}</option></select></label>
          </div>
        </section>
        <p v-if="avisoUbicacion" class="social-notice" role="status">{{ avisoUbicacion }}</p>

        <div v-if="cargando" class="social-loading" role="status"><span class="social-loading-dot"></span><h2>Estamos buscando los centros</h2><p>Preparando el listado y sus ubicaciones.</p></div>
        <div v-else-if="error" class="social-empty" role="alert"><h2>No pudimos cargar los centros</h2><p>{{ error }}</p><button type="button" class="social-button" @click="cargar"><SocialIcon name="refresh" :size="19" /> Volver a intentar</button></div>
        <template v-else-if="cargado">
          <p class="social-sr-only" role="status" aria-live="polite">{{ estadoResultados }}</p>
          <p v-if="sinCoordenadas" class="social-notice">{{ sinCoordenadas }} registros sin coordenadas utilizables no se incluyen en los resultados.</p>
          <section class="social-explorer" aria-label="Resultados de centros infantiles">
            <div class="social-results-pane">
              <div class="social-list-toolbar">
                <label class="social-center-search"><SocialIcon name="search" :size="18" /><span class="social-sr-only">Buscar centro o dirección dentro de los filtros elegidos</span><input v-model="busqueda" type="search" placeholder="Centro o dirección"></label>
                <button v-if="provincia || canton || parroquia || busqueda" type="button" class="social-text-button" @click="limpiarFiltros"><SocialIcon name="clear" :size="17" /> Limpiar filtros</button>
              </div>
              <p class="social-order-note">{{ ubicacion ? 'Más cercanos primero · distancia en línea recta' : 'Orden alfabético · usa tu ubicación para ordenar por cercanía' }}</p>
              <div class="social-mobile-switch" role="group" aria-label="Presentación de resultados"><button type="button" :aria-pressed="presentacion === 'list'" @click="presentacion = 'list'"><SocialIcon name="list" :size="18" /> Lista</button><button type="button" :aria-pressed="presentacion === 'map'" @click="presentacion = 'map'"><SocialIcon name="map" :size="18" /> Mapa</button></div>
              <div :class="['social-centers-list', { 'social-mobile-hidden': presentacion === 'map' }]">
                <div v-if="!centros.length" class="social-empty"><SocialIcon name="search" :size="32" /><h3>No hay centros con esta búsqueda</h3><p>Prueba otra provincia o elimina los filtros. Esto no significa que no exista atención en tu territorio.</p><button type="button" class="social-button social-button--light" @click="limpiarFiltros"><SocialIcon name="clear" :size="18" /> Limpiar filtros</button></div>
                <article v-for="(centro, i) in visibles" :key="centro.id" :class="['social-center', { selected: seleccionado?.id === centro.id }]">
                  <div class="social-center-main">
                    <span class="social-center-number" aria-hidden="true">{{ i + 1 }}</span>
                    <h3>{{ nombreLegible(centro.nombre) }}</h3>
                    <div class="social-center-location"><SocialIcon name="pin" :size="15" /><div><p>{{ [centro.parroquia, centro.canton, centro.provincia].filter(Boolean).map(nombreLegible).join(', ') }}</p><span v-if="centro.distancia !== null" class="social-distance">{{ distanciaLegible(centro.distancia) }} de tu ubicación</span></div></div>
                    <SocialIcon class="social-center-chevron" name="chevron-right" :size="20" />
                  </div>
                  <button type="button" class="social-center-select" :aria-pressed="seleccionado?.id === centro.id" :aria-label="`Seleccionar ${nombreLegible(centro.nombre)} y ver su ubicación y detalles`" @click="seleccionarCentro(centro.id)"></button>
                </article>
                <div v-if="centros.length" class="social-list-more">
                  <div v-if="visibles.length < centros.length" ref="finCentros" class="social-list-sentinel" aria-hidden="true"></div>
                  <p>Mostrando {{ visibles.length }} de {{ centros.length.toLocaleString('es-EC') }} centros</p>
                  <button v-if="visibles.length < centros.length" type="button" :class="['social-button', 'social-button--light', 'social-load-more', { 'social-sr-only': cargaAutomatica }]" @click="mostrarMasCentros">Ver más centros <SocialIcon name="chevron-down" :size="19" /></button>
                </div>
              </div>
            </div>
            <div class="social-map-column">
              <section v-if="seleccionado" id="social-selected-detail" class="social-selected-center" aria-labelledby="social-selected-title" tabindex="-1">
                <div class="social-selected-copy">
                  <h3 id="social-selected-title">{{ nombreLegible(seleccionado.nombre) }}</h3>
                  <p>{{ [seleccionado.parroquia, seleccionado.canton, seleccionado.provincia].filter(Boolean).map(nombreLegible).join(', ') }}</p>
                  <p v-if="seleccionado.direccion"><strong>Dirección:</strong> {{ seleccionado.direccion }}</p><p v-if="seleccionado.referencia"><strong>Referencia:</strong> {{ seleccionado.referencia }}</p>
                  <p v-if="!seleccionado.direccion">Dirección escrita no disponible. Consulta el punto del mapa.</p>
                  <p v-if="seleccionado.distancia !== null">{{ distanciaLegible(seleccionado.distancia) }} en línea recta desde tu ubicación.</p>
                </div>
                <a class="social-directions-button" :href="comoLlegar(seleccionado)" target="_blank" rel="noopener noreferrer" :aria-label="`Cómo llegar a ${nombreLegible(seleccionado.nombre)}. Abre Google Maps en otra pestaña.`"><SocialIcon name="map" :size="18" /> Cómo llegar <SocialIcon name="external" :size="14" /></a>
              </section>
              <section class="social-results-summary" aria-labelledby="social-summary-title">
                <div class="social-count">
                  <span class="social-count-symbol"><SocialIcon name="pin" :size="24" /></span>
                  <strong class="social-count-number"><AnimatedNumber :value="centros.length" /></strong>
                  <div class="social-count-copy"><h2 id="social-summary-title">Centros</h2><p>{{ territorio }} <span v-if="busqueda">· «{{ busqueda }}»</span></p></div>
                </div>
                <div v-if="distribucion.length" class="social-chart" role="img" :aria-label="`Centros por provincia: ${distribucion.map(d => `${d.label}, ${d.count}`).join('; ')}`">
                  <p class="social-sr-only">Distribución por provincia</p>
                  <div class="social-chart-bar" aria-hidden="true"><span v-for="(d, i) in distribucion" :key="d.label" :style="{ width: `${d.percent}%` }" :class="`segment-${i}`"></span></div>
                  <ul><li v-for="(d, i) in distribucion" :key="d.label"><i :class="`segment-${i}`"></i>{{ d.label }} <b><AnimatedNumber :value="d.count" /></b></li></ul>
                </div>
              </section>
              <div :class="['social-map-pane', { 'social-mobile-hidden': presentacion === 'list' }]">
                <ServiciosMap :centros="centros" :selected="seleccionado?.id" :location="ubicacion ?? undefined" @select="seleccionarCentro" />
              </div>
            </div>
          </section>
          <p class="social-disclaimer social-map-disclaimer">Las ubicaciones corresponden a registros de unidades. Consulta las condiciones de ingreso y disponibilidad con la institución. Para direcciones y rutas se utilizan servicios externos.</p>
        </template>
      </template>
    </main>

    <aside class="social-footer" aria-label="Información sobre la orientación">
      <p>Información para orientar, no para aprobar beneficios ni asignar cupos.</p>
      <div><a :href="fuenteInstitucional" target="_blank" rel="noopener noreferrer">Información institucional <SocialIcon name="external" :size="13" /></a><details><summary><SocialIcon name="info" :size="15" /> Sobre esta orientación</summary><p>Contenido adaptado del <a :href="fuentePiloto" target="_blank" rel="noopener noreferrer">piloto de servicios</a>, con información complementaria de <a :href="fuenteAsesor" target="_blank" rel="noopener noreferrer">Asesor593</a> donde corresponde. Fuentes consultadas: {{ fechaContenido }}. Revisión de redacción: {{ fechaRedaccion }}. Las respuestas no determinan el cumplimiento de requisitos.</p></details></div>
    </aside>
    <InstitutionalFooter />

    <dialog ref="detail" class="social-dialog" aria-labelledby="social-service-title" @close="detalleCerrado" @click="($event.target === detail) && cerrarDetalle()">
      <article v-if="servicioAbierto">
        <button type="button" class="social-detail-close" aria-label="Cerrar información del servicio" @click="cerrarDetalle"><SocialIcon name="close" /></button>
        <span class="social-dialog-service-icon"><SocialIcon :name="iconosServicio[servicioAbierto.id] || 'compass'" :size="32" /></span>
        <span class="social-service-category">{{ categoriasServicio[servicioAbierto.id] }}</span>
        <h2 id="social-service-title">{{ servicioAbierto.title }}</h2>
        <h3>¿En qué consiste?</h3><p>{{ servicioAbierto.description }}</p>
        <h3>¿A quién está dirigido?</h3><p>{{ servicioAbierto.who }}</p>
        <h3>¿Cómo acceder?</h3><p>{{ servicioAbierto.access }}</p>
        <section v-if="servicioAbierto.complements?.length" class="social-service-complements" aria-label="Prestaciones publicadas en Asesor593">
          <h3>Prestaciones que puedes consultar</h3>
          <ul><li v-for="complement in servicioAbierto.complements" :key="complement.sourceId"><h4>{{ complement.title }}</h4><p>{{ complement.text }}</p></li></ul>
        </section>
        <p v-if="servicioAbierto.important" class="social-notice">{{ servicioAbierto.important }}</p>
        <p class="social-disclaimer">Esta información no confirma que cumplas los requisitos. La institución verifica cada caso.</p>
        <button v-if="servicioAbierto.id === 'cdi'" type="button" class="social-button" @click="buscarCentros">Buscar centros infantiles <SocialIcon name="map" :size="20" /></button>
        <template v-else><p class="social-notice">Las ubicaciones de este servicio todavía no están habilitadas en esta vista. Puedes consultar la información institucional.</p><a class="social-button" :href="fuenteInstitucional" target="_blank" rel="noopener noreferrer">Consultar información institucional <SocialIcon name="external" :size="18" /></a></template>
        <details class="social-content-sources"><summary><SocialIcon name="info" :size="16" /> Fuentes del contenido</summary><p>Consulta de fuentes: {{ fechaContenido }}. Redacción adaptada: {{ fechaRedaccion }}. No sustituye la verificación de condiciones vigentes.</p><ul><li v-for="source in servicioAbierto.sources" :key="source.url"><a :href="source.url" target="_blank" rel="noopener noreferrer">{{ source.label }} <SocialIcon name="external" :size="13" /></a></li></ul></details>
      </article>
    </dialog>
  </div>
</template>
