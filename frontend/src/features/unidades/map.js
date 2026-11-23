import L from '../leaflet'
import Supercluster from 'supercluster'
import { union } from '@turf/union'
import { apiUrl } from '../../services/api'

export function mountUnidades(loading) {
let disposed=false;
const requests=new AbortController();
const fetch=(url)=>globalThis.fetch(url,{signal:requests.signal});
const API=apiUrl('/unidades');
const map=L.map("map",{zoomControl:false,minZoom:6,maxZoom:20});
L.control.zoom({position:'bottomright'}).addTo(map);
const baseLayer=L.tileLayer("https://mt1.google.com/vt/lyrs=m&hl=es&gl=EC&x={x}&y={y}&z={z}",{maxZoom:20,attribution:'© Google'});
const baseTilesReady=new Promise(function(resolve){
    let settled=false;
    function finish(){if(!settled){settled=true;resolve()}}
    baseLayer.once('load',finish);
    window.setTimeout(finish,5000);
});
baseLayer.addTo(map);
map.setView([-1.83,-78.18],7);

const maskLayer=L.layerGroup().addTo(map);
const outlineLayer=L.layerGroup().addTo(map);
const markersLayer=L.layerGroup().addTo(map);

const ECUADOR_GEOJSON_URL="https://raw.githubusercontent.com/jpmarindiaz/geo-collection/master/ecu/ecuador.geojson";

const regionKeys=['costa','sierra','amazonia','galapagos'];

const regionColors={
    costa:{fill:'#FFCD56',border:'#e6b800',label:'#b8860b',text:'rgba(0,0,0,.8)'},
    sierra:{fill:'#5C9EFF',border:'#3a7fd9',label:'#2563eb',text:'white'},
    amazonia:{fill:'#FF6978',border:'#e04858',label:'#dc2626',text:'white'},
    galapagos:{fill:'#18B2A2',border:'#128f82',label:'#0d7a6e',text:'white'}
};

const provinceRegion={};
'07,08,09,12,13,23,24'.split(',').forEach(function(c){provinceRegion[c]='costa'});
'01,02,03,04,05,06,10,11,17,18'.split(',').forEach(function(c){provinceRegion[c]='sierra'});
'14,15,16,19,21,22'.split(',').forEach(function(c){provinceRegion[c]='amazonia'});
'20'.split(',').forEach(function(c){provinceRegion[c]='galapagos'});

const regionNames={costa:'Costa',sierra:'Sierra',amazonia:'Amazonía',galapagos:'Galápagos'};

const dpaConfig={
    provincias:{url:apiUrl('/dpa/provincias'),prop:'name',label:'Provincia'},
    cantones:{url:apiUrl('/dpa/cantones'),prop:'name',label:'Cantón'},
    parroquias:{url:apiUrl('/dpa/parroquias'),prop:'name',label:'Parroquia'}
};

const legendEl=document.getElementById('dpaLegend');
const legendLabelEl=document.getElementById('dpaLegendLabel');
const legendValueEl=document.getElementById('dpaLegendValue');

const dpaLayers={};
const dpaData={};
let activeDpa='provincias';

function getDpaStyle(feature){
    const region=provinceRegion[feature.properties.province_id||feature.properties.id];
    const colors=region?regionColors[region]:regionColors.sierra;
    const mode=document.getElementById('filterMapMode').value;
    if(mode!=='points'){
        const field=activeDpa==='provincias'?'dpa_despro':activeDpa==='cantones'?'dpa_descan':'dpa_despar';
        const name=String(feature.properties.name||'').trim().toLocaleLowerCase('es');
        const values=filteredFeatures.filter(function(f){return fieldValue(f,field).toLocaleLowerCase('es')===name});
        const metric=mode==='users'?values.reduce(function(total,f){return total+(Number(f.properties.total)||0)},0):values.length;
        const intensity=Math.min(1,metric/(activeDpa==='provincias'?50000:activeDpa==='cantones'?10000:2000));
        return {fillColor:metric?'#29265f':'#e7e8ef',fillOpacity:0.2+intensity*.65,color:'white',weight:activeDpa==='parroquias'?1:activeDpa==='cantones'?2:3,opacity:.9};
    }
    return {
        fillColor:colors.fill,
        fillOpacity:0.4,
        color:'white',
        weight:activeDpa==='parroquias'?1:activeDpa==='cantones'?2:3,
        opacity:0.9
    };
}

async function loadDpaLayer(level){
    if(!dpaData[level]){
        const r=await fetch(dpaConfig[level].url);
        if(!r.ok)throw new Error('HTTP '+r.status);
        dpaData[level]=await r.json();
        if(disposed)return;
    }
    dpaLayers[level].clearLayers();
    L.geoJSON(dpaData[level],{
        style:getDpaStyle,
        onEachFeature:function(feature,layer){
            layer.on('mouseover',function(){
                layer.setStyle({fillOpacity:0.75});
                layer.bringToFront();
                const name=feature.properties[dpaConfig[level].prop];
                legendLabelEl.textContent=dpaConfig[level].label;
                legendValueEl.textContent=name||'—';
                legendEl.classList.add('visible');
            });
            layer.on('mouseout',function(){
                layer.setStyle(getDpaStyle(feature));
                legendEl.classList.remove('visible');
            });
            layer.on('click',function(){
                map.fitBounds(layer.getBounds(),{padding:[30,30],maxZoom:14});
            });
        }
    }).addTo(dpaLayers[level]);
}

async function setDpaLevel(level){
    activeDpa=level;
    Object.keys(dpaLayers).forEach(function(k){map.removeLayer(dpaLayers[k])});
    document.querySelectorAll('.dpa-pill').forEach(function(opt){
        opt.classList.toggle('active',opt.querySelector('input').value===level);
    });
    const loading=document.getElementById('brandLoading');
    loading.style.display='block';
    try{
        await loadDpaLayer(level);
        if(activeDpa===level)map.addLayer(dpaLayers[level]);
        return true;
    }catch(error){
        console.error('Error loading DPA layer:',error);
        return false;
    }finally{
        loading.style.display='none';
    }
}

document.querySelectorAll('input[name="dpaLevel"]').forEach(function(input){
    input.addEventListener('change',function(){setDpaLevel(this.value)});
});

function getRegionKey(provCode){
    return provinceRegion[provCode]||null;
}



let ecuadorGeo=null;

async function loadEcuadorGeo(){
    try{
        const r=await fetch(ECUADOR_GEOJSON_URL);
        ecuadorGeo=await r.json();
    }catch(e){
        console.warn("Could not load Ecuador GeoJSON, using fallback");
    }
}

function buildMask(){
    maskLayer.clearLayers();
    if(!ecuadorGeo)return;
    const worldCoords=[[-90,-180],[-90,180],[90,180],[90,-180],[-90,-180]];
    const holes=[];
    ecuadorGeo.features.forEach(function(f){
        const geom=f.geometry;
        if(geom.type==="Polygon"){
            geom.coordinates.forEach(function(ring,i){
                if(i===0) holes.push(ring.map(function(c){return[c[1],c[0]]}));
            });
        }else if(geom.type==="MultiPolygon"){
            geom.coordinates.forEach(function(poly){
                poly.forEach(function(ring,i){
                    if(i===0) holes.push(ring.map(function(c){return[c[1],c[0]]}));
                });
            });
        }
    });
    if(holes.length>0){
        const maskCoords=[worldCoords,...holes];
        L.polygon(maskCoords,{color:'transparent',fillColor:'white',fillOpacity:0.8,weight:0,interactive:false}).addTo(maskLayer);
    }
}

function buildOutline(){
    outlineLayer.clearLayers();
    if(!ecuadorGeo)return;
    try{
        let merged=null;
        ecuadorGeo.features.forEach(function(f){
            if(merged===null){
                merged=f.geometry;
            }else{
                merged=union({
                    type:'FeatureCollection',
                    features:[
                        {type:'Feature',properties:{},geometry:merged},
                        {type:'Feature',properties:{},geometry:f.geometry}
                    ]
                }).geometry;
            }
        });
        if(merged){
            L.geoJSON(merged,{
                style:{color:'white',weight:9,fillOpacity:0,opacity:0.95,smoothFactor:1}
            }).addTo(outlineLayer);
        }
    }catch(e){
        console.warn("Could not build outline:",e);
    }
}

let stickyMarker=null;
let currentPopup=null;
let allFeatures=[];
let filteredFeatures=[];
let index=new Supercluster({radius:80,maxZoom:14});

const filterFields={search:'filterSearch',region:'filterRegion',province:'filterProvince',canton:'filterCanton',parish:'filterParish',service:'filterService',modality:'filterModality',area:'filterArea',type:'filterType',admin:'filterAdmin',cooperator:'filterCooperator'};
const filterDefaults={region:'Todas',province:'Todas',canton:'Todos',parish:'Todas',service:'Todos',modality:'Todas',area:'Todas',type:'Todos',admin:'Todas',cooperator:'Todas'};
function fieldValue(feature,key){return String(feature.properties[key]??'').trim()}
function uniqueValues(features,key){return Array.from(new Set(features.map(function(f){return fieldValue(f,key)}).filter(Boolean))).sort(function(a,b){return a.localeCompare(b,'es')})}
function fillSelect(id,values,first){const el=document.getElementById(id);const previous=el.value;el.replaceChildren(new Option(first,''));values.forEach(function(v){el.add(new Option(v,v))});if(values.includes(previous))el.value=previous}
function populateFilters(){
    fillSelect('filterRegion',Object.keys(regionNames).map(function(k){return regionNames[k]}),'Todas');
    fillSelect('filterProvince',uniqueValues(allFeatures,'dpa_despro'),'Todas');
    fillSelect('filterCanton',uniqueValues(allFeatures,'dpa_descan'),'Todos');
    fillSelect('filterParish',uniqueValues(allFeatures,'dpa_despar'),'Todas');
    [['filterService','servicio','Todos'],['filterModality','mod','Todas'],['filterArea','area','Todas'],['filterType','tipo','Todos'],['filterAdmin','tipo_admin','Todas'],['filterCooperator','cooperante','Todas']].forEach(function(item){fillSelect(item[0],uniqueValues(allFeatures,item[1]),item[2])});
}
function selected(id){return document.getElementById(id).value}
function applyFilters(){
    const q=selected('filterSearch').trim().toLocaleLowerCase('es');
    const region=selected('filterRegion'),province=selected('filterProvince'),canton=selected('filterCanton');
    filteredFeatures=allFeatures.filter(function(feature){
        const p=feature.properties;
        if(region&&String(p.region||regionNames[getRegionKey(p.dpa_prov)]||'').toLocaleLowerCase('es')!==region.toLocaleLowerCase('es'))return false;
        if(province&&fieldValue(feature,'dpa_despro')!==province)return false;
        if(canton&&fieldValue(feature,'dpa_descan')!==canton)return false;
        if(selected('filterParish')&&fieldValue(feature,'dpa_despar')!==selected('filterParish'))return false;
        if(selected('filterService')&&fieldValue(feature,'servicio')!==selected('filterService'))return false;
        if(selected('filterModality')&&fieldValue(feature,'mod')!==selected('filterModality'))return false;
        if(selected('filterArea')&&fieldValue(feature,'area')!==selected('filterArea'))return false;
        if(selected('filterType')&&fieldValue(feature,'tipo')!==selected('filterType'))return false;
        if(selected('filterAdmin')&&fieldValue(feature,'tipo_admin')!==selected('filterAdmin'))return false;
        if(selected('filterCooperator')&&fieldValue(feature,'cooperante')!==selected('filterCooperator'))return false;
        if(q&&!['nombre','servicio','ruc','codigo'].some(function(key){return fieldValue(feature,key).toLocaleLowerCase('es').includes(q)}))return false;
        return true;
    });
    const mapMode=document.getElementById('filterMapMode').value;
    if(dpaLayers[activeDpa])dpaLayers[activeDpa].eachLayer(function(layer){if(layer.feature)layer.setStyle(getDpaStyle(layer.feature))});
    index=new Supercluster({radius:80,maxZoom:14});index.load(filteredFeatures);
    const users=filteredFeatures.reduce(function(total,f){return total+(Number(f.properties.total)||0)},0);
    const urban=filteredFeatures.filter(function(f){return fieldValue(f,'area').toLocaleLowerCase('es').includes('urb')}).length;
    document.getElementById('summaryUnits').textContent=filteredFeatures.length.toLocaleString('es');
    document.getElementById('summaryUsers').textContent=users.toLocaleString('es');
    document.getElementById('summaryArea').textContent=urban.toLocaleString('es')+' / '+(filteredFeatures.length-urban).toLocaleString('es');
    document.getElementById('filterResults').textContent=filteredFeatures.length.toLocaleString('es')+' unidades encontradas';
    document.getElementById('filterUserTotal').textContent=users.toLocaleString('es')+' usuarios';
    document.getElementById('mapEmpty').hidden=filteredFeatures.length>0;
    updateClusters();
}
function clearMapFilters(){document.querySelectorAll('#filterDrawer select').forEach(function(el){el.value=''});document.getElementById('filterSearch').value='';populateFilters();applyFilters()}
function resetMapView(){clearMapFilters();map.setView([-1.83,-78.18],7)}
document.getElementById('filterToggle').addEventListener('click',function(){const drawer=document.getElementById('filterDrawer');drawer.hidden=!drawer.hidden;this.setAttribute('aria-expanded',String(!drawer.hidden))});
document.getElementById('filterClose').addEventListener('click',function(){document.getElementById('filterDrawer').hidden=true;document.getElementById('filterToggle').setAttribute('aria-expanded','false')});
document.getElementById('clearFilters').addEventListener('click',clearMapFilters);
document.getElementById('filterMapMode').addEventListener('change',function(){
    document.getElementById('mapLegend').innerHTML=this.value==='points'?'<p class="map-legend-title">Servicios</p><div class="map-legend-row"><span class="legend-swatch legend-swatch--dii"></span>Desarrollo infantil</div><div class="map-legend-row"><span class="legend-swatch legend-swatch--adult"></span>Personas adultas mayores</div><div class="map-legend-row"><span class="legend-swatch legend-swatch--disability"></span>Discapacidad y protección</div>':'<p class="map-legend-title">'+(this.value==='users'?'Usuarios registrados':'Unidades por territorio')+'</p><div class="map-legend-row"><span class="legend-swatch" style="background:#29265f"></span>Mayor concentración</div>';
    applyFilters();
});
Object.keys(filterFields).forEach(function(key){const el=document.getElementById(filterFields[key]);el.addEventListener(key==='search'?'input':'change',function(){
    if(key==='region'){document.getElementById('filterProvince').value='';document.getElementById('filterCanton').value='';document.getElementById('filterParish').value=''}
    if(key==='province'){document.getElementById('filterCanton').value='';document.getElementById('filterParish').value=''}
    if(key==='canton')document.getElementById('filterParish').value='';
    if(['region','province','canton'].includes(key))refreshTerritoryOptions();
    applyFilters();
})});
function refreshTerritoryOptions(){
    const region=selected('filterRegion'),province=selected('filterProvince'),canton=selected('filterCanton');
    const inRegion=allFeatures.filter(function(f){return !region||String(f.properties.region||regionNames[getRegionKey(f.properties.dpa_prov)]||'').toLocaleLowerCase('es')===region.toLocaleLowerCase('es')});
    fillSelect('filterProvince',uniqueValues(inRegion,'dpa_despro'),'Todas');
    const inProvince=inRegion.filter(function(f){return !province||fieldValue(f,'dpa_despro')===province});
    fillSelect('filterCanton',uniqueValues(inProvince,'dpa_descan'),'Todos');
    const inCanton=inProvince.filter(function(f){return !canton||fieldValue(f,'dpa_descan')===canton});
    fillSelect('filterParish',uniqueValues(inCanton,'dpa_despar'),'Todas');
}

function openPopupFor(marker,feature){
    closePopup();
    const isCluster=feature.properties.cluster;
    currentPopup=L.popup({maxWidth:320,minWidth:isCluster?0:280})
        .setLatLng(marker.getLatLng())
        .setContent(popup(feature))
        .addTo(map);
    requestAnimationFrame(function(){
        const el=currentPopup.getElement();
        if(!el)return;
        if(isCluster)el.querySelector('.leaflet-popup-content').classList.add('cluster-popup');
        const btn=el.querySelector('.popup-link');
        if(btn){
            btn.addEventListener('click',function(e){
                e.stopPropagation();
                window.open(btn.getAttribute('data-href'),'_blank');
            });
        }
    });
}

function closePopup(){
    if(currentPopup){map.closePopup(currentPopup);currentPopup=null}
}

function createMarkerIcon(feature){
    const service=String(feature.properties.servicio||'').toLocaleLowerCase('es');
    const color=service.includes('adult')?'#d6a21d':service.includes('discap')?'#5453a6':service.includes('protecci')?'#dd7666':'#168f86';
    return L.divIcon({
        className:"marker-pin",
        iconSize:[80,80],iconAnchor:[40,40],popupAnchor:[0,-42],
        html:'<div style="display:flex;align-items:flex-start;justify-content:center;width:80px;height:80px;padding-top:40px"><svg pointer-events="none" width="28" height="38" viewBox="0 0 28 38" fill="none"><path d="M14 0C6.268 0 0 6.268 0 14c0 10.5 14 24 14 24s14-13.5 14-24C28 6.268 21.732 0 14 0z" fill="'+color+'"/><circle cx="14" cy="13" r="7" fill="white"/><path d="M14 9v8M10 13h8" stroke="#f5c842" stroke-width="2" stroke-linecap="round"/></svg></div>'
    });
}

function createClusterIcon(count,size){
    const r=size==='large'?22:size==='medium'?17:13;
    const fs=size==='large'?11:size==='medium'?10:9;
    return L.divIcon({
        className:"cluster-pin",
        iconSize:[r*2,r*2],iconAnchor:[r,r],
        html:'<div style="width:'+r*2+'px;height:'+r*2+'px;background:linear-gradient(135deg,#29265f,#201e4c);border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:'+fs+'px;border:2px solid #f5c842;box-shadow:0 2px 10px rgba(32,30,76,.3);font-family:Montserrat,sans-serif">'+count+'</div>'
    });
}

function popup(feature){
    const p=feature.properties;
    if(p.cluster){
        return '<div class="popup-card"><div class="popup-cluster"><div class="popup-cluster-header"><div class="popup-cluster-count">'+p.point_count+'</div><div class="popup-cluster-label">unidades</div></div><div class="popup-cluster-body"><div class="popup-cluster-hint">Click para acercar</div></div></div></div>';
    }
    const regionKey=getRegionKey(p.dpa_prov);
    const region=regionKey?regionNames[regionKey]:'';
    const headerBg=regionKey?'background:'+regionColors[regionKey].fill:'background:linear-gradient(135deg,#29265f,#201e4c)';
    const headerColor=regionKey?regionColors[regionKey].text:'white';
    let rows='';
    [['RUC',p.ruc],['Modalidad',p.mod],['Servicio',p.servicio],['Provincia',p.dpa_despro],['Cantón',p.dpa_descan],['Área',p.area],['Tipo',p.tipo],['Dirigido a',p.corte]].forEach(function(f){
        if(f[1]) rows+='<div class="popup-row"><span class="label">'+f[0]+'</span><span class="value">'+f[1]+'</span></div>';
    });
    const btnBg=regionKey?regionColors[regionKey].fill:'#29265f';
    const dataHref=p.link_ubi?p.link_ubi.replace(/"/g,'&quot;'):'';
    let link=dataHref?('<div style="padding:8px 16px 12px;text-align:center"><button class="popup-link" data-href="'+dataHref+'" style="background:'+btnBg+'">Abrir en Google Maps</button></div>'):'';
    const regionBadge=region?('<span class="popup-tag" style="background:rgba(255,255,255,.25);color:'+regionColors[regionKey].text+';font-weight:600">'+region+'</span>'):'';
    return '<div class="popup-card"><div class="popup-header" style="'+headerBg+';color:'+headerColor+'"><h3>'+p.nombre+'</h3>'+regionBadge+'</div><div class="popup-body">'+rows+'</div>'+link+'</div>';
}

function getBBox(){const b=map.getBounds();return[b.getWest(),b.getSouth(),b.getEast(),b.getNorth()]}

function updateClusters(){
    if(!allFeatures.length)return;
    closePopup();stickyMarker=null;
    markersLayer.clearLayers();
    if(!filteredFeatures.length)return;
    const clusters=index.getClusters(getBBox(),Math.floor(map.getZoom()));
    clusters.forEach(function(feature){
        const coordinates=feature.geometry.coordinates;
        const latLng=[coordinates[1],coordinates[0]];
        let marker;
        if(feature.properties.cluster){
            const count=feature.properties.point_count;
            const size=count>50?'large':count>10?'medium':'small';
            marker=L.marker(latLng,{icon:createClusterIcon(count,size)});
            marker.on('mouseover',function(){marker.openPopup()});
            marker.on('mouseout',function(){marker.closePopup()});
            marker.on('click',function(){
                const zoom=index.getClusterExpansionZoom(feature.properties.cluster_id);
                map.setView(latLng,zoom);
            });
            marker.bindPopup(popup(feature),{maxWidth:320,minWidth:0});
            marker.on('popupopen',function(){
                const element=marker.getElement();
                const content=element&&element.querySelector('.leaflet-popup-content');
                if(content)content.classList.add('cluster-popup');
            });
        }else{
            marker=L.marker(latLng,{icon:createMarkerIcon(feature)});
            marker.on('mouseover',function(){
                if(stickyMarker!==marker)openPopupFor(marker,feature);
            });
            marker.on('mouseout',function(){
                if(stickyMarker!==marker)closePopup();
            });
            marker.on('click',function(event){
                L.DomEvent.stopPropagation(event);
                L.DomEvent.preventDefault(event);
                if(stickyMarker===marker){
                    closePopup();
                    stickyMarker=null;
                }else{
                    stickyMarker=marker;
                    openPopupFor(marker,feature);
                }
            });
        }
        markersLayer.addLayer(marker);
    });
}

async function loadAllData(){
    const loading=document.getElementById('brandLoading');
    loading.style.display='block';
    try{
        const response=await fetch(API+'?limit=0');
        if(!response.ok)throw new Error('HTTP '+response.status);
        const collection=await response.json();
        if(disposed)return false;
        if(collection.type!=='FeatureCollection'||!Array.isArray(collection.features)){
            throw new Error('La API no devolvió una FeatureCollection');
        }
        allFeatures=collection.features;
        filteredFeatures=allFeatures;
        populateFilters();
        applyFilters();
        return true;
    }catch(error){
        console.error('Error loading unit data:',error);
        return false;
    }finally{
        loading.style.display='none';
    }
}

async function reloadData(){
    markersLayer.clearLayers();
    allFeatures=[];
    filteredFeatures=[];
    index=new Supercluster({radius:80,maxZoom:14});
    if(await loadAllData())updateClusters();
}

map.on('moveend zoomend',updateClusters);
map.on('click',function(){
    if(stickyMarker){closePopup();stickyMarker=null}
});

(async function init(){
    ['provincias','cantones','parroquias'].forEach(function(k){dpaLayers[k]=L.layerGroup()});
    loadEcuadorGeo().then(function(){if(!disposed){buildMask();buildOutline()}});
    try{
        const ready=await Promise.all([setDpaLevel('provincias'),loadAllData(),baseTilesReady]);
        if(disposed)return;
        if(ready[0]&&ready[1]){
            updateClusters();
            applyFilters();
            document.getElementById('filterMapMode').dispatchEvent(new Event('change'));
            loading.finish();
        }
        else loading.fail('No se pudieron cargar las capas de unidades.');
    }catch(error){
        console.error('Error initializing map:',error);
        loading.fail('Comprueba la conexión e inténtalo de nuevo.');
    }
})();

return {
    resetMapView,
    clearMapFilters,
    destroy(){
        disposed=true;
        requests.abort();
        map.remove();
    }
};
}
