<script setup lang="ts">
import { onMounted, onBeforeUnmount, useTemplateRef } from 'vue'
import MapLoading from '../components/MapLoading.vue'
import SocialIcon from '../components/SocialIcon.vue'
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
        <SocialIcon name="home" :size="20" />
    </a>
    <div class="topbar-brand">
        <div class="topbar-brand-top">
            <div class="panel-icon"><SocialIcon name="pin" :size="20" /></div>
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
        <SocialIcon name="filters" :size="20" />
        <span>Filtros</span>
    </button>
    <button class="icon-btn" @click="controller?.resetMapView()" title="Restablecer filtros y vista" aria-label="Restablecer filtros y vista"><SocialIcon name="reset" :size="20" /></button>
</div>
<aside class="filter-drawer" id="filterDrawer" aria-labelledby="filterTitle" hidden>
    <div class="filter-drawer-head">
        <div><h3 id="filterTitle">Filtros del mapa</h3><p id="filterResults">Cargando unidades…</p></div>
        <button class="filter-close" id="filterClose" type="button" aria-label="Cerrar filtros"><SocialIcon name="close" :size="20" /></button>
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
