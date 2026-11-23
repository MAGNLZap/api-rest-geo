<script setup lang="ts">
import { onMounted, onBeforeUnmount, useTemplateRef } from 'vue'
import MapLoading from '../components/MapLoading.vue'
import { portalUrl } from '../services/api'
import { mountUnidades } from '../features/unidades/map'
import 'leaflet/dist/leaflet.css'
import '../styles/unidades.css'

document.title = 'Unidades de Atención - Ecuador'
const loading = useTemplateRef('loading')
let controller: ReturnType<typeof mountUnidades> | undefined
onMounted(() => {
  if (!loading.value) return
  try { controller = mountUnidades(loading.value) }
  catch (error) {
    console.error(error)
    loading.value.fail('No se pudieron inicializar las unidades.')
  }
})
onBeforeUnmount(() => { controller?.destroy() })
</script>

<template>
<MapLoading ref="loading" />
<div class="topbar">
    <a class="icon-btn" :href="portalUrl()" title="Volver a la vista principal" aria-label="Volver a la vista principal">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3 10 9-7 9 7"/><path d="M5 9v11h14V9"/><path d="M9 20v-6h6v6"/></svg>
    </a>
    <div class="topbar-brand">
        <div class="topbar-brand-top">
            <div class="panel-icon"><svg viewBox="0 0 24 24" fill="white" stroke="none"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5S10.62 6.5 12 6.5s2.5 1.12 2.5 2.5S13.38 11.5 12 11.5z"/></svg></div>
            <h2>Unidades de Atención</h2>
        </div>
        <div class="brand-loading" id="brandLoading"></div>
    </div>
    <div class="dpa-seg">
        <label class="dpa-pill active">Provincias<input type="radio" name="dpaLevel" value="provincias" checked></label>
        <label class="dpa-pill">Cantones<input type="radio" name="dpaLevel" value="cantones"></label>
        <label class="dpa-pill">Parroquias<input type="radio" name="dpaLevel" value="parroquias"></label>
    </div>
    <button class="icon-btn map-filter-toggle" id="filterToggle" type="button" aria-label="Abrir filtros" aria-expanded="false" aria-controls="filterDrawer" title="Filtros">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 6h16M7 12h10m-7 6h4"/><circle cx="8" cy="6" r="1.5" fill="currentColor" stroke="none"/><circle cx="15" cy="12" r="1.5" fill="currentColor" stroke="none"/><circle cx="12" cy="18" r="1.5" fill="currentColor" stroke="none"/></svg>
        <span>Filtros</span>
    </button>
    <button class="icon-btn" @click="controller?.resetMapView()" title="Restablecer filtros y vista" aria-label="Restablecer filtros y vista"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-2.6-6.3"/><path d="M21 3v6h-6"/></svg></button>
</div>
<aside class="filter-drawer" id="filterDrawer" aria-labelledby="filterTitle" hidden>
    <div class="filter-drawer-head">
        <div><h3 id="filterTitle">Filtros del mapa</h3><p id="filterResults">Cargando unidades…</p></div>
        <button class="filter-close" id="filterClose" type="button" aria-label="Cerrar filtros">×</button>
    </div>
    <label class="filter-field filter-field--wide">Buscar unidad
        <input class="filter-control" id="filterSearch" type="search" placeholder="Nombre, servicio o código" autocomplete="off">
    </label>
    <section class="filter-section" aria-labelledby="territoryFiltersTitle">
        <h4 id="territoryFiltersTitle">Territorio</h4>
        <label class="filter-field">Región<select class="filter-control" id="filterRegion"><option value="">Todas</option></select></label>
        <label class="filter-field">Provincia<select class="filter-control" id="filterProvince"><option value="">Todas</option></select></label>
        <label class="filter-field">Cantón<select class="filter-control" id="filterCanton"><option value="">Todos</option></select></label>
        <label class="filter-field">Parroquia<select class="filter-control" id="filterParish"><option value="">Todas</option></select></label>
    </section>
    <section class="filter-section" aria-labelledby="serviceFiltersTitle">
        <h4 id="serviceFiltersTitle">Servicios</h4>
        <label class="filter-field filter-field--wide">Servicio<select class="filter-control" id="filterService"><option value="">Todos</option></select></label>
        <label class="filter-field filter-field--wide">Modalidad<select class="filter-control" id="filterModality"><option value="">Todas</option></select></label>
        <label class="filter-field">Área<select class="filter-control" id="filterArea"><option value="">Todas</option></select></label>
        <label class="filter-field">Tipo de atención<select class="filter-control" id="filterType"><option value="">Todos</option></select></label>
    </section>
    <label class="filter-field">Visualización del mapa
        <select class="filter-control" id="filterMapMode">
            <option value="points">Ubicaciones</option>
            <option value="units">Unidades por territorio</option>
            <option value="users">Usuarios registrados</option>
        </select>
    </label>
    <details class="filter-advanced">
        <summary>Más criterios</summary>
        <div class="filter-section">
            <label class="filter-field">Administración<select class="filter-control" id="filterAdmin"><option value="">Todas</option></select></label>
            <label class="filter-field">Entidad cooperante<select class="filter-control" id="filterCooperator"><option value="">Todas</option></select></label>
        </div>
    </details>
    <div class="filter-actions">
        <span class="filter-results" id="filterUserTotal">—</span>
        <button class="filter-clear" id="clearFilters" type="button">Limpiar filtros</button>
    </div>
</aside>
<div class="map-legend" id="mapLegend" aria-live="polite"></div>
<div class="map-summary" id="mapSummary" aria-live="polite">
    <div class="summary-item"><span class="summary-value" id="summaryUnits">—</span><span class="summary-label">Unidades</span></div>
    <div class="summary-item"><span class="summary-value" id="summaryUsers">—</span><span class="summary-label">Usuarios</span></div>
    <div class="summary-item"><span class="summary-value" id="summaryArea">—</span><span class="summary-label">Urbano / rural</span></div>
</div>
<div class="map-empty" id="mapEmpty" hidden><strong>No hay unidades con estos filtros</strong><span>Prueba otra combinación o limpia los filtros.</span><button class="filter-clear" type="button" @click="controller?.clearMapFilters()">Limpiar filtros</button></div>
<div id="map"></div>
<div class="dpa-legend" id="dpaLegend">
    <div class="dpa-legend-label" id="dpaLegendLabel">Zona</div>
    <div class="dpa-legend-value" id="dpaLegendValue">—</div>
</div>
<div class="source-chip">Datos: Ministerio de Trabajo y Desarrollo Humano · Unidades de Atención</div>
</template>
