<script setup>
import { h, render, onMounted, onBeforeUnmount, watch, useTemplateRef, ref } from 'vue'
import SocialIcon from './SocialIcon.vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { createCentrosIndex } from '../features/orientacion/clusters'
import { nombreLegible, distanciaLegible } from '../features/orientacion/useCentros'

const props = defineProps({
  centros: { type: Array, required: true },
  selected: { type: Number, default: null },
  location: { type: Object, default: null },
})
const emit = defineEmits(['select'])
const container = useTemplateRef('container')
const tileError = ref(false)
let map
let layer
let locationLayer
let tiles
let index
let observer
let byId = new Map()
let pendingFrame = false
let chevronSvg

function createChevron() {
  if (!chevronSvg) {
    const host = document.createElement('span')
    render(h(SocialIcon, { name: 'chevron-right', size: 16 }), host)
    chevronSvg = host.firstElementChild.cloneNode(true)
    render(null, host)
  }
  return chevronSvg.cloneNode(true)
}

function openGroup(clusterId, latlng) {
  const leaves = index.getLeaves(clusterId, 100, 0)
  const content = document.createElement('div')
  content.className = 'social-map-group'
  const title = document.createElement('strong')
  title.className = 'social-tooltip-name'
  title.textContent = 'Centros en este punto'
  content.append(title)
  for (const leaf of leaves) {
    const centro = byId.get(leaf.properties.centroId)
    if (!centro) continue
    const button = document.createElement('button')
    button.type = 'button'
    button.textContent = nombreLegible(centro.nombre)
    button.addEventListener('click', () => { emit('select', centro.id); map.closePopup() })
    content.append(button)
  }
  if (leaves.length === 100) {
    const note = document.createElement('p')
    note.textContent = 'Se muestran hasta 100 centros aquí. Usa el listado para ver todos los resultados.'
    content.append(note)
  }
  L.popup({ maxWidth: 300, className: 'social-group-popup' }).setLatLng(latlng).setContent(content).openOn(map)
}
function draw() {
  if (!map || !index) return
  layer.clearLayers()
  const bounds = map.getBounds()
  const features = index.getClusters([bounds.getWest(), bounds.getSouth(), bounds.getEast(), bounds.getNorth()], Math.floor(map.getZoom()))
  for (const feature of features) {
    const [lng, lat] = feature.geometry.coordinates
    const p = feature.properties
    if (p.cluster) {
      const selectedHere = props.selected !== null && byId.has(props.selected) &&
        index.getLeaves(p.cluster_id, Infinity).some(item => item.properties.centroId === props.selected)
      const marker = L.marker([lat, lng], {
        icon: L.divIcon({
          className: `social-cluster${selectedHere ? ' is-selected' : ''}`,
          html: `<span>${p.point_count}</span>`, iconSize: [42, 42],
        }),
        title: `${p.point_count} centros. Acercar para explorar.`, keyboard: true,
      })
      const zoom = index.getClusterExpansionZoom(p.cluster_id)
      const label = document.createElement('div')
      label.className = 'social-tooltip-content'
      const category = document.createElement('span')
      category.className = 'social-tooltip-category'
      category.textContent = 'Centros de Desarrollo Infantil'
      const count = document.createElement('strong')
      count.className = 'social-tooltip-name'
      count.textContent = `${p.point_count.toLocaleString('es-EC')} centros`
      const description = document.createElement('p')
      description.className = 'social-tooltip-territory'
      description.textContent = zoom > 18 ? 'Varios centros comparten esta ubicación.' : 'Acerca el mapa para explorar sus ubicaciones.'
      const hint = document.createElement('span')
      hint.className = 'social-tooltip-hint'
      hint.textContent = zoom > 18 ? 'Selecciona el grupo para elegir un centro' : 'Selecciona el grupo para acercar'
      hint.append(createChevron())
      label.append(category, count, description, hint)
      marker.bindTooltip(label, { className: 'social-center-tooltip', direction: 'top', offset: [0, -18], opacity: 1 })
      marker.on('click', () => {
        if (zoom > 18) openGroup(p.cluster_id, [lat, lng])
        else map.setView([lat, lng], zoom)
      })
      layer.addLayer(marker)
    } else {
      const centro = byId.get(p.centroId)
      if (!centro) continue
      const marker = L.marker([lat, lng], {
        icon: L.divIcon({
          className: `social-pin${props.selected === centro.id ? ' is-selected' : ''}`,
          html: '<span></span>', iconSize: [26, 32], iconAnchor: [13, 30],
        }),
        keyboard: true, title: centro.nombre, alt: centro.nombre,
      })
      const label = document.createElement('div')
      label.className = 'social-tooltip-content'
      const category = document.createElement('span')
      category.className = 'social-tooltip-category'
      category.textContent = 'Centro de Desarrollo Infantil'
      const name = document.createElement('strong')
      name.className = 'social-tooltip-name'
      name.textContent = nombreLegible(centro.nombre)
      const territory = document.createElement('p')
      territory.className = 'social-tooltip-territory'
      territory.textContent = [centro.parroquia, centro.canton, centro.provincia].filter(Boolean).map(nombreLegible).join(', ') || 'Territorio no informado'
      label.append(category, name, territory)
      if (typeof centro.distancia === 'number' && Number.isFinite(centro.distancia)) {
        const distance = document.createElement('p')
        distance.className = 'social-tooltip-distance'
        distance.textContent = `${distanciaLegible(centro.distancia)} en línea recta`
        label.append(distance)
      }
      const hint = document.createElement('span')
      hint.className = 'social-tooltip-hint'
      hint.textContent = 'Selecciona el punto para ver detalles'
      hint.append(createChevron())
      label.append(hint)
      marker.bindTooltip(label, { className: 'social-center-tooltip', direction: 'top', offset: [0, -25], opacity: 1 })
      marker.on('click', () => emit('select', centro.id))
      layer.addLayer(marker)
    }
  }
}
function frameResults() {
  if (!map || !pendingFrame || !container.value?.clientWidth || !container.value?.clientHeight) return
  map.invalidateSize({ animate: false })
  const selected = byId.get(props.selected)
  if (selected) {
    map.setView([selected.lat, selected.lng], Math.max(map.getZoom(), 15), { animate: false })
  } else if (props.centros.length) {
    const initialView = props.location ? props.centros.slice(0, 12) : props.centros
    map.fitBounds(L.latLngBounds(initialView.map(centro => [centro.lat, centro.lng])), { padding: [40, 40], maxZoom: 14, animate: false })
  }
  pendingFrame = false
}
function rebuild() {
  if (!map) return
  byId = new Map(props.centros.map(centro => [centro.id, centro]))
  index = createCentrosIndex(props.centros)
  map.closePopup()
  pendingFrame = true
  frameResults()
  draw()
}
function showLocation() {
  if (!locationLayer) return
  locationLayer.clearLayers()
  if (!props.location) return
  const palette = getComputedStyle(container.value)
  L.circleMarker([props.location.lat, props.location.lng], {
    radius: 8, color: palette.getPropertyValue('--s-action').trim(), weight: 3,
    fillColor: palette.getPropertyValue('--s-location').trim(), fillOpacity: 1,
  }).bindTooltip('Tu ubicación aproximada').addTo(locationLayer)
}
function retryTiles() { tileError.value = false; tiles?.redraw() }
watch(() => props.centros, rebuild)
watch(() => props.selected, id => {
  const centro = byId.get(id)
  if (centro && map) { pendingFrame = true; frameResults() }
  draw()
})
watch(() => props.location, showLocation)
onMounted(() => {
  map = L.map(container.value, { zoomControl: false, minZoom: 3, maxZoom: 18, scrollWheelZoom: false })
    .setView([-1.5, -78.5], 7)
  L.control.zoom({ position: 'bottomright', zoomInTitle: 'Acercar', zoomOutTitle: 'Alejar' }).addTo(map)
  tiles = L.tileLayer('https://mt1.google.com/vt/lyrs=m&hl=es&gl=EC&x={x}&y={y}&z={z}', {
    maxZoom: 20, attribution: '© Google',
  }).addTo(map)
  tiles.on('tileerror', () => { tileError.value = true })
  layer = L.layerGroup().addTo(map)
  locationLayer = L.layerGroup().addTo(map)
  map.on('moveend', draw)
  observer = new ResizeObserver(() => {
    if (!map || !container.value?.clientWidth || !container.value?.clientHeight) return
    map.invalidateSize({ animate: false })
    frameResults()
  })
  observer.observe(container.value)
  rebuild()
  showLocation()
})
onBeforeUnmount(() => { observer?.disconnect(); map?.remove(); map = undefined })
</script>

<template>
  <div class="social-map-wrap">
    <div ref="container" class="social-map" role="region" aria-label="Mapa de centros. Los mismos centros están disponibles en el listado." />
    <div v-if="tileError" class="social-tile-notice" role="status">
      El fondo del mapa no se pudo cargar. Puedes seguir usando el listado.
      <button type="button" @click="retryTiles">Reintentar mapa</button>
    </div>
  </div>
</template>
