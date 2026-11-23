<script setup lang="ts">
import ecuadorHero from '@portal/ecuador_hero.svg'
import previewUnidades from '@portal/preview_unidades.svg'
import previewAmenazas from '@portal/preview_amenazas.svg'
import logo from '@amenazas/logo_encabezado.png'
import { portalUrl } from '../services/api'
import '../styles/home.css'

document.title = 'Geoportal del Ministerio de Trabajo y Desarrollo Humano'
</script>

<template>
<header class="masthead">
    <div class="hero">
      <div class="hero-copy">
        <p class="hero-institution"><span class="hero-chip-dot" aria-hidden="true"></span>Información geográfica</p>
        <h1>Geoportal del Ministerio de Trabajo y Desarrollo Humano</h1>
        <p>Insumos cartográficos institucionales a nivel nacional.</p>
      </div>
      <img class="ecuador-visual" :src="ecuadorHero" alt="" aria-hidden="true">
    </div>
  </header>

  <main>
    <div class="main-content">
      <section aria-labelledby="maps-heading">
        <div class="section-intro">
          <h2 id="maps-heading">Cada mapa, una mirada del territorio</h2>
        </div>

        <div class="map-grid">
          <a class="map-card map-card--units" :href="portalUrl('unidades_infancia')" aria-labelledby="units-title">
            <div class="card-art">
              <img :src="previewUnidades" alt="Vista cartográfica de la distribución de las Unidades de Atención" loading="lazy">
            </div>
            <div class="card-body">
              <span class="card-kicker">Servicios de atención social</span>
              <h3 id="units-title">Unidades de Atención</h3>
              <p>Explora los servicios, modalidades y unidades de atención por provincia, cantón y parroquia.</p>
            </div>
          </a>

          <a class="map-card map-card--hazards" :href="portalUrl('ua_amenazas')" aria-labelledby="hazards-title">
            <div class="card-art">
              <img :src="previewAmenazas" alt="Vista cartográfica de los niveles de susceptibilidad a inundaciones" loading="lazy">
            </div>
            <div class="card-body">
              <span class="card-kicker">Planificación y amenazas</span>
              <h3 id="hazards-title">Plan de Activación Fenómeno de El Niño</h3>
              <p>Consulta las Unidades de Atención que se encuentran en zonas susceptibles a amenazas asociadas al Evento El Niño.</p>
            </div>
          </a>
        </div>
      </section>
    </div>
  </main>

  <footer class="footer">
    <div class="footer-inner">
      <a class="footer-brand" :href="portalUrl()" aria-label="Ir al inicio">
        <img :src="logo" alt="Gobierno del Ecuador · Ministerio de Trabajo y Desarrollo Humano">
      </a>
      <p class="footer-note">Información geográfica para la consulta y planificación territorial.</p>
    </div>
  </footer>
</template>
