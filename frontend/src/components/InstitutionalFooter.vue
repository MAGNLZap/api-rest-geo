<script setup lang="ts">
import logo from '@amenazas/logo_encabezado.png'
import { portalUrl } from '../services/api'
</script>

<template>
  <footer class="institutional-footer">
    <div class="institutional-footer-inner">
      <a class="institutional-footer-brand" :href="portalUrl()" aria-label="Ir al inicio">
        <img :src="logo" alt="Gobierno del Ecuador · Ministerio de Trabajo y Desarrollo Humano">
      </a>
      <p class="institutional-footer-note">Información geográfica para la consulta y planificación territorial.</p>
    </div>
  </footer>
</template>

<style scoped>
.institutional-footer {
  flex: 0 0 auto;
  min-height: 132px;
  border-top: 3px solid var(--brand-gold);
  background: var(--brand-indigo-deep);
  color: var(--brand-white);
  font-family: SocialMontserrat, Montserrat, "Segoe UI", Arial, sans-serif;
}
.institutional-footer-inner {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(250px, .8fr) minmax(0, 1.2fr);
  align-items: center;
  gap: 64px;
  width: min(100%, 1180px);
  margin-inline: auto;
  padding: 32px 24px;
  color: rgb(255 255 255 / 78%);
  font-size: 12px;
}
.institutional-footer-brand {
  display: inline-flex;
  align-items: center;
  gap: 16px;
  min-width: 0;
  color: var(--brand-white);
  text-decoration: none;
  transition: opacity 180ms ease;
}
.institutional-footer-brand:hover { opacity: .86; }
.institutional-footer-brand:focus-visible {
  border-radius: 4px;
  outline: 2px solid var(--brand-gold);
  outline-offset: 5px;
}
.institutional-footer-brand img {
  display: block;
  width: min(270px, 100%);
  height: auto;
  object-fit: contain;
}
.institutional-footer-note {
  display: flex;
  align-items: center;
  justify-self: end;
  gap: 16px;
  max-width: 500px;
  color: rgb(255 255 255 / 82%);
  font-size: 15px;
  font-weight: 500;
  line-height: 1.55;
}
.institutional-footer-note::before {
  flex: 0 0 28px;
  height: 2px;
  background: var(--brand-gold);
  content: "";
}
@media (max-width: 760px) {
  .institutional-footer-inner { grid-template-columns: 1fr; gap: 22px; }
  .institutional-footer-note { justify-self: start; }
}
@media (max-width: 640px) {
  .institutional-footer-inner { gap: 18px; padding-inline: 18px; }
}
@media (max-width: 420px) {
  .institutional-footer-brand img { width: min(250px, 78vw); }
}
@media (prefers-reduced-motion: reduce) {
  .institutional-footer-brand { transition: none; }
}
</style>
