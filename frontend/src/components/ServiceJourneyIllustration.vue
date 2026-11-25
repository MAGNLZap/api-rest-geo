<script setup lang="ts">
import familyIllustration from '../assets/illustrations/familia-orientacion.png'
</script>

<template>
  <svg class="home-service-journey" viewBox="0 0 600 300" fill="none" aria-hidden="true" focusable="false">
    <path d="M35 184C16 136 45 58 108 46c54-10 84 27 90 80s-18 105-71 112S54 230 35 184Z" fill="var(--brand-white)" fill-opacity=".6" />
    <path d="M428 76c40-33 118-17 139 24s-3 103-51 119-100-3-108-45 0-81 20-98Z" fill="var(--brand-white)" fill-opacity=".6" />
    <path class="home-journey-route" d="M129 244c49 0 51-21 85-21h137c48 0 53 20 89 20 31 0 40-20 58-27" stroke="var(--brand-gold)" stroke-width="5" stroke-linecap="round" stroke-dasharray="3 10" />
    <ellipse cx="125" cy="244" rx="84" ry="7" fill="var(--brand-indigo)" fill-opacity=".09" />
    <ellipse cx="304" cy="246" rx="84" ry="7" fill="var(--brand-indigo)" fill-opacity=".09" />

    <image :href="familyIllustration" x="35" y="32" width="180" height="210" preserveAspectRatio="xMidYMax meet" />

    <g>
      <rect x="234" y="35" width="145" height="204" rx="23" fill="var(--brand-white)" stroke="var(--brand-indigo)" stroke-width="3" />
      <path d="M281 45h50" stroke="var(--brand-indigo)" stroke-width="5" stroke-linecap="round" />
      <circle cx="306.5" cy="223" r="5" fill="var(--brand-indigo-soft)" />
      <text x="250" y="77" fill="var(--brand-indigo)" font-size="12" font-weight="700">¿Para quién?</text>
      <rect x="248" y="89" width="117" height="35" rx="10" fill="var(--brand-indigo-soft)" />
      <circle cx="262" cy="106" r="6" fill="var(--brand-gold)" />
      <path d="m259 106 2 2 4-4" stroke="var(--brand-indigo)" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" />
      <text x="275" y="110" fill="var(--brand-indigo)" font-size="11">Mi familia</text>
      <text x="250" y="150" fill="var(--brand-indigo)" font-size="12" font-weight="700">¿Qué necesitas?</text>
      <rect x="248" y="162" width="117" height="35" rx="10" fill="var(--brand-indigo)" />
      <circle cx="262" cy="179" r="6" fill="var(--brand-gold)" />
      <path d="m259 179 2 2 4-4" stroke="var(--brand-indigo)" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" />
      <text x="275" y="183" fill="var(--brand-white)" font-size="10">Apoyo familiar</text>
    </g>

    <g>
      <rect x="428" y="92" width="133" height="120" rx="16" fill="var(--brand-white)" stroke="var(--brand-indigo)" stroke-width="1.6" />
      <path d="M444 92h101" stroke="var(--brand-gold)" stroke-width="4" stroke-linecap="round" />
      <circle cx="451" cy="118" r="12" fill="var(--brand-indigo-soft)" />
      <path d="m451 110-7 3v5c0 4 7 8 7 8s7-4 7-8v-5l-7-3Z" stroke="var(--brand-indigo)" stroke-width="1.4" stroke-linejoin="round" />
      <text x="444" y="151" fill="var(--brand-indigo)" font-size="14" font-weight="700">Servicios</text>
      <text x="444" y="174" fill="var(--brand-muted)" font-size="11">Qué ofrecen</text>
      <text x="444" y="192" fill="var(--brand-muted)" font-size="11">Cómo acceder</text>
      <path d="m541 170 5 5-5 5m0 8 5 5-5 5" stroke="var(--brand-indigo)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
      <path d="M560 54c0 13-13 24-13 24s-13-11-13-24a13 13 0 0 1 26 0Z" fill="var(--brand-gold)" />
      <circle cx="547" cy="54" r="4" fill="var(--brand-indigo)" />
    </g>

    <g fill="var(--brand-indigo)" font-size="16" font-weight="650" text-anchor="middle">
      <text x="112" y="280">Tu familia</text>
      <text x="306" y="280">Dos preguntas</text>
      <text x="496" y="280">Orientación</text>
    </g>
  </svg>
</template>

<style scoped>
.home-service-journey{display:block;position:relative;z-index:1;width:100%;max-width:560px;height:auto;font-family:Montserrat,"Segoe UI",Arial,sans-serif}
.home-journey-route{transition:stroke-width 180ms ease}
@media(hover:hover) and (pointer:fine){.home-services-featured:hover .home-journey-route{stroke-width:6}}
@media(prefers-reduced-motion:reduce){.home-journey-route{transition:none}}
</style>
