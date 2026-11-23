<script setup lang="ts">
import { onBeforeUnmount, ref } from 'vue'
import ecuadorHero from '@portal/ecuador_hero.svg'
import '../../../app/static/portal/map-loading.css'

const busy = ref(true)
const hidden = ref(false)
const finished = ref(false)
const error = ref('')
let hideTimer: ReturnType<typeof setTimeout> | undefined

function finish() {
  busy.value = false
  finished.value = true
  hideTimer = setTimeout(() => { hidden.value = true }, 350)
}

function fail(message = 'Comprueba la conexión e inténtalo de nuevo.') {
  if (hideTimer) clearTimeout(hideTimer)
  hidden.value = false
  finished.value = false
  error.value = `No se pudo cargar el mapa. ${message}`
  busy.value = false
}

function retry() { window.location.reload() }
onBeforeUnmount(() => { if (hideTimer) clearTimeout(hideTimer) })
defineExpose({ finish, fail })
</script>

<template>
  <div id="mapLoading" class="map-loading-screen" :class="{ 'is-hidden': finished, 'is-error': error }"
    :hidden="hidden" role="status" aria-live="polite" :aria-busy="busy">
    <div class="map-loading-panel">
      <div class="map-loading-visual" aria-hidden="true">
        <img class="map-loading-map" :src="ecuadorHero" alt="">
      </div>
      <p id="mapLoadingDetail" class="map-loading-detail">{{ error || 'Cargando el mapa y sus capas geográficas…' }}</p>
      <div class="map-loading-track" aria-hidden="true"><span></span></div>
      <button id="mapLoadingRetry" class="map-loading-retry" type="button" :hidden="!error" @click="retry">Reintentar</button>
    </div>
  </div>
</template>
