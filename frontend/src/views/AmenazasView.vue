<script setup lang="ts">
import { onMounted, onBeforeUnmount, useTemplateRef } from 'vue'
import MapLoading from '../components/MapLoading.vue'
import SocialIcon from '../components/SocialIcon.vue'
import logo from '@amenazas/logo_encabezado.png'
import { portalUrl } from '../services/api'
import { mountAmenazas } from '../features/amenazas/map'
import 'leaflet/dist/leaflet.css'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet-draw/dist/leaflet.draw.css'
import '../styles/amenazas.css'

document.title = 'Plan de Activación Fenómeno de El Niño · Geoportal MTDH'
const loading = useTemplateRef('loading')
let controller: ReturnType<typeof mountAmenazas> | undefined
onMounted(() => {
  if (!loading.value) return
  try { controller = mountAmenazas(loading.value) }
  catch (error) {
    console.error(error)
    loading.value.fail('No se pudo inicializar el mapa de amenazas.')
  }
})
onBeforeUnmount(() => { controller?.destroy() })
</script>

<template>
<MapLoading ref="loading" />
<header class="topbar">
  <div class="brand">
    <a class="btn btn-home" :href="portalUrl()" title="Volver al menú principal" aria-label="Volver al menú principal">
      <SocialIcon name="home" :size="20" />
    </a>
    <div class="brand-text">
      <h1>Plan de Activación Fenómeno de El Niño</h1>
      <p>Subsecretaría de Gestión de Datos y Estudios · Dirección de Gestión de Información y Datos</p>
    </div>
  </div>
  <img class="logo-gob" :src="logo">
</header>

<main class="layout">
  <!-- ============ PANEL IZQUIERDO ============ -->
  <aside class="panel panel-left">
    <section class="card">
      <h2><span class="dot"></span>Filtros territoriales</h2>
      <label>Provincia<select id="fProv"><option value="">Todas</option></select></label>
      <label>Cantón<select id="fCan" disabled><option value="">Todos</option></select></label>
      <label>Parroquia<select id="fPar" disabled><option value="">Todas</option></select></label>
    </section>

    <section class="card">
      <h2><span class="dot"></span>Servicio y modalidad</h2>
      <label>Servicio<select id="fServ"><option value="">Todos</option></select></label>
      <label>Modalidad<select id="fMod"><option value="">Todas</option></select></label>
    </section>

    <section class="card">
      <h2><span class="dot"></span>Capas de susceptibilidad</h2>
      <label class="chk switch" title="Desactive la capa para ver el mapa base"><input type="checkbox" id="layerOn" checked> Mostrar capa en el mapa</label>
      <div class="layer-list" id="layerList"></div>
      <p class="sub">Categorías a visualizar</p>
      <div class="checks" id="fCat">
        <label class="chk"><input type="checkbox" value="1" checked> Media</label>
        <label class="chk"><input type="checkbox" value="2" checked> Alta</label>
        <label class="chk"><input type="checkbox" value="3" checked> Muy alta</label>
      </div>
      <p class="sub">Regiones del Ecuador</p>
      <div class="checks" id="fReg">
        <label class="chk"><input type="checkbox" value="Costa" checked> Costa</label>
        <label class="chk"><input type="checkbox" value="Sierra" checked> Sierra</label>
        <label class="chk"><input type="checkbox" value="Amazonía" checked> Amazonía</label>
        <label class="chk"><input type="checkbox" value="Insular" checked> Insular</label>
      </div>
      <div class="seg" role="group" aria-label="Indicador">
        <button class="seg-btn active" data-metric="n">N.º de UA</button>
        <button class="seg-btn" data-metric="p">% de UA</button>
      </div>
      <button class="btn btn-yellow full" id="btnExport" style="margin-top:12px" title="Descargar el reporte Excel de los resultados filtrados">
        <SocialIcon name="download" :size="20" />
        Descargar resultados filtrados
      </button>
    </section>

    <section class="card">
      <h2><span class="dot"></span>Unidades de Atención</h2>
      <div class="pts">
        <label class="chk"><input type="checkbox" id="ptExp" checked><span class="pt pt-exp"></span> UA expuestas <b id="nExp"></b></label>
        <label class="chk"><input type="checkbox" id="ptNoExp"><span class="pt pt-noexp"></span> UA no expuestas <b id="nNoExp"></b></label>
      </div>
      <p class="note">El código de la UA se muestra a partir de la escala aproximada 1:20.000. Haga clic en un punto para ver sus variables.</p>
      <p class="sub" style="margin-top:12px">Selección por polígono</p>
      <div class="btn-row">
        <button class="btn btn-outline sm" id="btnDraw">
          <SocialIcon name="polygon" :size="20" />Dibujar polígono</button>
        <button class="btn btn-outline sm" id="btnClearSel" disabled><SocialIcon name="clear" :size="20" />Quitar selección</button>
      </div>
      <p class="note" id="selInfo">Dibuje un polígono sobre el mapa para seleccionar las UA que quedan dentro (según los filtros activos).</p>
      <button class="btn btn-azul full" id="btnExportSel" disabled>
        <SocialIcon name="download" :size="20" />Descargar UA seleccionadas por polígono</button>
    </section>

    <button class="btn btn-outline full" id="btnClear"><SocialIcon name="clear" :size="20" />Limpiar filtros</button>
    <p class="note">Las UA ubicadas en parroquias urbanas se representan agrupadas en la cabecera cantonal correspondiente.</p>
  </aside>

  <!-- ============ MAPA ============ -->
  <section class="map-wrap">
    <div id="map"></div>
    <div class="map-chip" id="mapChip"></div>
    <div class="map-export" id="mapExport">
      <span>Exportar mapa</span>
      <button data-fmt="png" title="Descargar el mapa y las estadísticas como imagen PNG">PNG</button>
      <button data-fmt="jpg" title="Descargar el mapa y las estadísticas como imagen JPG">JPG</button>
      <button data-fmt="print" title="Imprimir el mapa y las estadísticas">Imprimir</button>
    </div>
  </section>

  <!-- ============ PANEL DERECHO ============ -->
  <aside class="panel panel-right">
    <div class="kpis">
      <div class="kpi"><span class="kpi-v" id="kUA">–</span><span class="kpi-l">Unidades de Atención filtradas</span></div>
      <div class="kpi"><span class="kpi-v" id="kExp">–</span><span class="kpi-l" id="kExpL">Unidades de Atención expuestas</span></div>
      <div class="kpi"><span class="kpi-v" id="kUsr">–</span><span class="kpi-l">Usuarios en UA expuestas</span></div>
    </div>
    <p class="note tight" id="kNote"></p>

    <section class="card">
      <h2><span class="dot"></span><span id="statsTitle">UA por categoría de susceptibilidad</span></h2>
      <div id="stats"></div>
    </section>

    <section class="card">
      <h2><span class="dot"></span><span id="topTitle">Territorios con más UA expuestas</span></h2>
      <div id="top"></div>
    </section>
  </aside>
</main>

<footer class="foot">
  <p id="footSrc">Fuentes: Reporte de Unidades de Atención – SIIMTDH (septiembre 2026) · Susceptibilidad a inundaciones y sequía (MAGAP, 2015) · Movimientos en masa (SNGR, 2011) · Incendios forestales (SNGR, 2015) · Límites DPA (MDG, 2026). Elaboración: DGID – SGDE – MTDH.</p>
  <p class="foot-note">Nota: Se considera que una UA está expuesta cuando se encuentra dentro de zonas con susceptibilidad media, alta o muy alta de las capas consideradas en este análisis. Las UA clasificadas como “no expuestas” se encuentran fuera de estas categorías y no implica ausencia absoluta de amenaza o riesgo.</p>
  <p class="foot-note">El análisis de exposición considera las Unidades de Atención que cuentan con georreferenciación validada a nivel de parroquia, las cuales corresponden al 88 % del total. Este porcentaje puede variar según el reporte mensual del SIIMTDH.</p>
</footer>
</template>
