<script setup lang="ts">
import { defineAsyncComponent } from 'vue'
import { pagePath } from './services/api'

const pages = {
  '/': () => import('./views/HomeView.vue'),
  '/unidades_infancia': () => import('./views/UnidadesView.vue'),
  '/ua_amenazas': () => import('./views/AmenazasView.vue'),
}
const path = pagePath(window.location.pathname)
const loadPage = pages[path as keyof typeof pages]
if (!loadPage) window.location.replace(import.meta.env.BASE_URL)
const page = defineAsyncComponent({
  loader: loadPage || pages['/'],
  onError(error, _retry, fail) {
    console.error('No se pudo cargar la vista del portal:', error)
    fail()
  },
})
</script>

<template>
  <component :is="page" />
</template>

<style>
html, body, #app { min-height: 100%; }
#app { height: 100%; }
</style>
