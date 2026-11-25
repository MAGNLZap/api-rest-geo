<script setup lang="ts">
import ecuadorHero from '@portal/ecuador_hero.svg'
import previewUnidades from '@portal/preview_unidades.svg'
import previewAmenazas from '@portal/preview_amenazas.svg'
import logo from '@amenazas/logo_encabezado.png'
import SocialIcon from '../components/SocialIcon.vue'
import ServiceJourneyIllustration from '../components/ServiceJourneyIllustration.vue'
import { portalUrl } from '../services/api'
import '../styles/home.css'
import '../styles/home-orientacion.css'
import '../styles/orientacion-typography.css'

document.title = 'Geoportal del Ministerio de Trabajo y Desarrollo Humano'
</script>

<template>
<header class="masthead masthead--welcome">
    <div class="hero">
      <div class="hero-copy">
        <p class="hero-institution"><span class="hero-chip-dot" aria-hidden="true"></span>Ministerio de Trabajo y Desarrollo Humano</p>
        <h1>¿Qué te gustaría consultar?</h1>
        <p>Conoce los servicios del Ministerio para ti y tu familia o explora información territorial del Ecuador.</p>
      </div>
      <img class="ecuador-visual" :src="ecuadorHero" alt="" aria-hidden="true">
    </div>
  </header>

  <main>
    <div class="main-content">
      <section aria-labelledby="maps-heading">
        <div class="section-intro">
          <h2 id="maps-heading">Elige cómo empezar</h2>
        </div>

          <a class="map-card map-card--services home-services-featured" :href="portalUrl('servicios_sociales')" aria-labelledby="services-title">
            <div class="card-art">
              <ServiceJourneyIllustration />
            </div>
            <div class="card-body">
              <span class="card-kicker">Para la ciudadanía</span>
              <h3 id="services-title">Encuentra servicios para ti y tu familia</h3>
              <p>Cuéntanos qué necesitas. Te orientamos sobre los 18 servicios del Ministerio y cómo acceder. También puedes consultar ubicaciones de Centros de Desarrollo Infantil.</p>
              <span class="card-cue">Conocer servicios <SocialIcon name="chevron-right" :size="20" /></span>
            </div>
          </a>

        <div class="map-grid">
          <a class="map-card map-card--units" :href="portalUrl('unidades_infancia')" aria-labelledby="units-title">
            <div class="card-art">
              <img :src="previewUnidades" alt="Vista cartográfica de la distribución de las unidades de atención" loading="lazy">
            </div>
            <div class="card-body">
              <span class="card-kicker">Mapa general de unidades</span>
              <h3 id="units-title">Unidades de Atención</h3>
              <p>Explora los servicios, modalidades y unidades de atención por provincia, cantón y parroquia.</p>
              <span class="card-cue">Explorar mapa de unidades <SocialIcon name="chevron-right" :size="20" /></span>
            </div>
          </a>
          <a class="map-card map-card--hazards" :href="portalUrl('ua_amenazas')" aria-labelledby="hazards-title">
            <div class="card-art">
              <img :src="previewAmenazas" alt="Vista cartográfica de los niveles de susceptibilidad a inundaciones" loading="lazy">
            </div>
            <div class="card-body">
              <span class="card-kicker">Información territorial</span>
              <h3 id="hazards-title">Evento El Niño y unidades de atención</h3>
              <p>Explora las amenazas y la exposición de las unidades de atención para apoyar la consulta y planificación territorial.</p>
              <span class="card-cue">Explorar información territorial <SocialIcon name="chevron-right" :size="20" /></span>
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
