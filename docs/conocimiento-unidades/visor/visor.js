(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('knowledge').textContent);
  const $ = id => document.getElementById(id);
  const services = new Map(data.pilot.services.map(item => [item.id, item]));
  const asesor = new Map(data.asesor.map(item => [item.id, item]));
  const inventory = data.inventory;
  const inventoryGroups = [];
  const groupMap = new Map();
  const formatCount = value => value.toLocaleString('es-EC');
  const rawLabel = value => value === null ? '(NULL)' : value === '' ? '(cadena vacía)' : value;
  const inventoryKey = (kind, values) => `inventario/${kind}/${encodeURIComponent(JSON.stringify(values))}`;
  const isInventoryKey = key => key === 'inventario' || key.startsWith('inventario/');
  for (const row of inventory.rows) {
    if (!groupMap.has(row.servicio)) {
      const group = { service: row.servicio, total: 0, modalities: new Map() };
      groupMap.set(row.servicio, group);
      inventoryGroups.push(group);
    }
    const group = groupMap.get(row.servicio);
    group.total += row.unidades;
    if (!group.modalities.has(row.mod)) group.modalities.set(row.mod, []);
    group.modalities.get(row.mod).push(row);
  }
  const pilotSource = `https://github.com/sgde-mtdh/Geoportal-MTDH/blob/${data.commit}/servicios/index.html`;
  const cdiSource = `https://github.com/sgde-mtdh/Geoportal-MTDH/blob/${data.commit}/servicios/cdi/index.html`;
  const statusLabels = { 'sin-revisar': 'Sin revisar', observaciones: 'Con observaciones', revisado: 'Revisado en mesa' };
  const issues = [
    ['Inventario propio', 'Ya se capturaron las combinaciones reales en una consulta de solo lectura. Falta homologar sus denominaciones con el catálogo del piloto y validar el significado de mod_abv. Ver «Servicios y modalidades».'],
    ['Alcance del mapa', 'Decidir cuáles de los 18 grupos tendrán unidades en el mapa y cuáles tendrán únicamente orientación o enlaces.'],
    ['Diferencias entre modalidades', 'Validar qué distingue cada modalidad y qué preguntas pueden orientarla sin sustituir una valoración profesional.'],
    ['Límites de edad', 'Validar los extremos de edad de CDI/CNH y su expresión en años o meses. Los avisos del piloto no resuelven el límite exacto de 3 años.'],
    ['Ingreso familiar a CDI', 'Obtener los requisitos vigentes de ingreso. Los requisitos del permiso de funcionamiento no corresponden a las familias.'],
    ['Condiciones de transferencias', 'Validar montos, puntajes y metodologías de Registro Social por prestación, sin trasladar condiciones de una a otra.'],
    ['Contenido del BJGL', 'Confirmar porcentaje de discapacidad y corregir el metadato de normativa que menciona documentos de hoja de vida.'],
    ['Liquidaciones y focalización', 'Confirmar fórmula completa del BDHV, valores condicionados de 1000 días y diferencias de focalización.'],
    ['Documentos por etapa', 'Confirmar documentos de adopción según fase y completar textos truncados de permisos sin reconstruirlos por inferencia.'],
    ['Canales competentes', 'Verificar oficinas, direcciones, contactos y horarios. No asociar una oficina con una unidad solo porque esté cerca.'],
    ['Orientación o derivación', 'Decidir si el producto solo informa y ubica o si registrará/enviará una derivación formal. Las fuentes no prueban integración de casos.'],
    ['Recepción y capacidad', 'Definir quién recibe y sigue una derivación, y si existe información verificable de cupos o capacidad.'],
    ['Situaciones urgentes', 'Acordar un protocolo institucional de atención urgente y vulneración de derechos, sin inventar canales o prioridades.'],
    ['Respuestas y privacidad', 'Acordar qué se conservaría, con qué propósito y consentimiento. Los pilotos no justifican recoger cédulas.'],
  ].map(([title, text], index) => ({ id: `P${String(index + 1).padStart(2, '0')}`, title, text }));
  const ages = [
    ['under', 'Menos de 1 año', 'El piloto avisa que los centros públicos atienden desde 1 año y que para menores se requiere orientación sobre otros servicios. No cambia el filtro de centros.'],
    ['1', '1 año', 'No hay un aviso específico para esta selección. La edad no participa en la función que filtra centros.'],
    ['2', '2 años', 'No hay un aviso específico para esta selección. La edad no participa en la función que filtra centros.'],
    ['3', '3 años o más', 'El piloto avisa que los centros atienden principalmente de 1 a 3 años y recomienda consultar opciones correspondientes a la edad. No excluye centros ni resuelve el límite exacto de 3 años.'],
  ];
  const comparisons = {
    cdi: { ids: ['otorgamiento-de-permisos-de-funcionamiento-para-centros-de-desar'], text: 'No equivalente: permiso para operar una unidad, no requisitos de ingreso de una familia.' },
    cnh: { ids: ['bono-mil-dias'], text: 'Solo coincidencia de públicos. Bono 1000 días es una transferencia; no sustituye el acompañamiento CNH.' },
    adulto: { ids: ['pension-mejores-an'], text: 'Complemento económico posible, no equivalencia con cuidado residencial, diurno o domiciliario.' },
    discapacidad: { ids: ['pension-toda-una-vida', 'bono-joaquin-gallegos'], text: 'Complementos económicos posibles. No equivalen a atención en centros, acogida, hogar o comunidad.' },
    adopcion: { ids: ['solicitud-de-adopcion-nacional-de-ninas-ninos-y-adolescentes-con'], text: 'Correspondencia parcial: esta ficha cubre adopción nacional, no internacional.' },
    bonos: { ids: ['bono-desarrollo-humano', 'bono-desarrollo-humano-variable', 'bono-mil-dias', 'pension-mejores-an', 'pension-toda-una-vida', 'bono-joaquin-gallegos'], text: 'Grupo amplio frente a prestaciones distintas. Este desglose es una correspondencia candidata, no una recomendación automática.' },
    bjl: { ids: ['bono-joaquin-gallegos'], text: 'Coincide la denominación y finalidad. Los requisitos publicados aún necesitan validación institucional.' },
    permisos: { ids: ['otorgamiento-de-permisos-de-funcionamiento-para-centros-de-desar'], text: 'Correspondencia parcial: la ficha no cubre permisos de todas las unidades o modalidades.' },
    acompanamiento: { ids: ['bono-desarrollo-humano-variable'], text: 'Relación contextual de población usuaria, no equivalencia entre acompañamiento y transferencia.' },
  };
  const metadata = new Map([
    ['catalogo', 'Catálogo completo del piloto'],
    ['asesor', 'Fichas complementarias de Asesor593'],
    ['cdi', 'Flujo CDI independiente'],
    ['cdi/territorio', 'CDI: selección territorial'],
    ['cdi/resultados', 'CDI: resultados y límites'],
    ['cdi/todos', 'CDI: ver todos los centros'],
    ['pendientes', 'Decisiones pendientes de validación'],
    ['inventario', 'Inventario observado: servicios y modalidades'],
  ]);
  for (const population of data.pilot.paths) {
    for (const [id, title] of population.needs) metadata.set(`ruta/${population.id}/${id}`, `${population.label}: ${title}`);
  }
  for (const item of services.values()) metadata.set(`servicio/${item.id}`, item.title);
  for (const item of asesor.values()) metadata.set(`asesor/${item.id}`, item.nombre);
  for (const [id, title] of ages) metadata.set(`cdi/edad/${id}`, `CDI: ${title}`);
  for (const item of issues) metadata.set(`pendiente/${item.id}`, `${item.id}: ${item.title}`);
  for (const group of inventoryGroups) {
    metadata.set(inventoryKey('servicio', [group.service]), `Servicio observado: ${rawLabel(group.service)}`);
    for (const [modality, rows] of group.modalities) {
      metadata.set(inventoryKey('modalidad', [group.service, modality]), `${rawLabel(group.service)}: ${rawLabel(modality)}`);
      for (const row of rows) metadata.set(
        inventoryKey('combinacion', [row.servicio, row.mod, row.mod_abv]),
        `${rawLabel(row.servicio)} / ${rawLabel(row.mod)} / ${rawLabel(row.mod_abv)}`,
      );
    }
  }

  let state = { mode: 'routes', population: data.pilot.paths[0].id, need: data.pilot.paths[0].needs[0][0], selected: null };
  let currentKey = '';
  let notes = Object.create(null);
  let persistent = true;
  let externalChange = false;
  let storedVersion = null;
  const storageKey = `ua-content-review-v1-${data.datasetId}`;

  function validateDraft(draft) {
    if (!draft || draft.format !== 'ua-content-review' || draft.version !== 1 || draft.datasetId !== data.datasetId) {
      throw new Error('El borrador no pertenece a esta captura. No se ha importado.');
    }
    if (!draft.notes || typeof draft.notes !== 'object' || Array.isArray(draft.notes)) throw new Error('El borrador no contiene observaciones válidas.');
    const clean = Object.create(null);
    for (const [key, value] of Object.entries(draft.notes)) {
      if (!metadata.has(key) || !value || !Object.hasOwn(statusLabels, value.status) ||
          typeof value.notes !== 'string' || typeof value.proposal !== 'string' ||
          value.notes.length > 8000 || value.proposal.length > 8000 ||
          typeof value.updatedAt !== 'string' || !Number.isFinite(Date.parse(value.updatedAt))) {
        throw new Error('Hay elementos o campos no válidos en el borrador. No se ha importado.');
      }
      if (value.evidenceRevision !== undefined &&
          (typeof value.evidenceRevision !== 'string' || !Number.isFinite(Date.parse(value.evidenceRevision)))) {
        throw new Error('La fecha de evidencia de una observación no es válida.');
      }
      clean[key] = { status: value.status, notes: value.notes, proposal: value.proposal, updatedAt: value.updatedAt,
        ...(value.evidenceRevision ? { evidenceRevision: value.evidenceRevision } : {}) };
    }
    return clean;
  }
  try {
    storedVersion = localStorage.getItem(storageKey);
    if (storedVersion) notes = validateDraft(JSON.parse(storedVersion));
  } catch (error) {
    persistent = false;
    $('message').textContent = 'No se pudo recuperar el guardado local. Puedes trabajar en memoria y exportar tu revisión.';
  }

  function el(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined && text !== null) node.textContent = String(text);
    if (className) node.className = className;
    return node;
  }
  function button(text, action, className) {
    const node = el('button', text, className);
    node.type = 'button';
    node.addEventListener('click', action);
    return node;
  }
  function link(text, href, parent) {
    const node = el('a', text);
    node.href = href;
    node.target = '_blank';
    node.rel = 'noopener noreferrer';
    parent.append(node);
    return node;
  }
  function notice(parent, text, info = false) { parent.append(el('p', text, `notice${info ? ' info' : ''}`)); }
  function source(parent, title, url, documentPath) {
    const line = el('p', undefined, 'source');
    link(title, url, line);
    if (documentPath) link('Ver documento de análisis', documentPath, line);
    line.append(document.createTextNode(' · Consulta: 24/11/2026'));
    parent.append(line);
  }
  function section(parent, title, content) {
    const box = el('section', undefined, 'fact-section');
    box.append(el('h4', title));
    if (Array.isArray(content)) {
      const list = el('ul');
      for (const item of content) list.append(el('li', item));
      box.append(list);
    } else box.append(el('p', content || 'No publicado en esta captura.'));
    parent.append(box);
    return box;
  }
  function header(label, title, description) {
    $('section-label').textContent = label;
    $('content-title').textContent = title;
    $('content-description').textContent = description;
    $('stage').replaceChildren();
    $('message').textContent = '';
  }
  function envelope() {
    return { format: 'ua-content-review', version: 1, datasetId: data.datasetId, sourceDate: data.date,
      inventoryCapturedAt: inventory.capturedAt, commit: data.commit, exportedAt: new Date().toISOString(), notes };
  }
  function updateSaveStatus() {
    $('save-status').textContent = externalChange
      ? 'Otra ventana cambió el borrador. No se sobrescribirá: tus notas están en memoria. Expórtalas antes de recargar para recuperar el otro borrador.'
      : persistent
      ? 'Notas guardadas en este navegador. Exporta una copia para conservarlas o compartirlas.'
      : 'Trabajo en memoria: el navegador no permite guardar. Exporta antes de cerrar.';
    $('review-count').textContent = `${Object.keys(notes).length} elementos con revisión guardada.`;
  }
  function persist() {
    if (externalChange) { persistent = false; updateSaveStatus(); return; }
    try {
      if (localStorage.getItem(storageKey) !== storedVersion) {
        externalChange = true;
        persistent = false;
      } else {
        const serialized = JSON.stringify(envelope());
        localStorage.setItem(storageKey, serialized);
        storedVersion = serialized;
        persistent = true;
      }
    }
    catch { persistent = false; }
    updateSaveStatus();
  }
  function showEditor(key) {
    currentKey = key;
    const item = notes[key] || { status: 'sin-revisar', notes: '', proposal: '' };
    $('review-target').textContent = metadata.get(key);
    if (isInventoryKey(key) && notes[key] && notes[key].evidenceRevision !== inventory.capturedAt) {
      $('review-target').textContent += ' — Nota de otra captura: revisar los conteos antes de reutilizarla.';
    }
    $('review-status').value = item.status;
    $('review-notes').value = item.notes;
    $('review-proposal').value = item.proposal;
    updateSaveStatus();
  }
  function saveEditor() {
    if (!metadata.has(currentKey)) return;
    const status = $('review-status').value;
    const text = $('review-notes').value;
    const proposal = $('review-proposal').value;
    if (status === 'sin-revisar' && !text.trim() && !proposal.trim()) delete notes[currentKey];
    else notes[currentKey] = { status, notes: text, proposal, updatedAt: new Date().toISOString(),
      ...(isInventoryKey(currentKey) ? { evidenceRevision: inventory.capturedAt } : {}) };
    persist();
  }
  function normalize(value) { return String(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase(); }
  function matches(text) { return normalize(text).includes(normalize($('search').value.trim())); }

  const modes = [
    ['routes', 'Rutas del piloto', '20'],
    ['inventory', 'Servicios y modalidades', String(inventoryGroups.length)],
    ['catalogue', 'Catálogo del piloto', '18'],
    ['asesor', 'Complemento Asesor593', '8'],
    ['cdi', 'Flujo CDI separado', ''],
    ['issues', 'Pendientes de validación', '14'],
  ];
  function renderNavigation() {
    $('navigation').replaceChildren(...modes.map(([id, title, count]) => {
      const node = button(title, () => { state.mode = id; state.selected = null; $('search').value = ''; render(); });
      node.setAttribute('aria-pressed', String(state.mode === id));
      if (count) node.append(el('span', count, 'nav-number'));
      return node;
    }));
    let items;
    if (state.mode === 'routes') items = data.pilot.paths.map(p => ({
      id: p.id, title: p.label, search: `${p.label} ${p.needs.map(n => `${n[1]} ${n[2].map(id => services.get(id).title).join(' ')}`).join(' ')}`,
      action: () => { state.population = p.id; state.need = p.needs[0][0]; render(); },
      active: state.population === p.id,
    }));
    else if (state.mode === 'catalogue') items = [...services.values()].map(item => ({
      id: item.id, title: item.title, search: `${item.title} ${item.short}`, active: state.selected === item.id,
      action: () => { state.selected = item.id; render(); },
    }));
    else if (state.mode === 'asesor') items = [...asesor.values()].map(item => ({
      id: item.id, title: item.nombre, search: `${item.nombre} ${item.resumen}`, active: state.selected === item.id,
      action: () => { state.selected = item.id; render(); },
    }));
    else if (state.mode === 'inventory') items = inventoryGroups.map(group => ({
      id: inventoryKey('servicio', [group.service]), title: rawLabel(group.service),
      search: `${rawLabel(group.service)} ${[...group.modalities].map(([modality, rows]) => `${rawLabel(modality)} ${rows.map(row => rawLabel(row.mod_abv)).join(' ')}`).join(' ')}`,
      active: state.selected === inventoryKey('servicio', [group.service]),
      action: () => { state.selected = inventoryKey('servicio', [group.service]); render(); },
    }));
    else if (state.mode === 'issues') items = issues.map(item => ({
      id: item.id, title: `${item.id} · ${item.title}`, search: `${item.title} ${item.text}`, active: state.selected === item.id,
      action: () => { state.selected = item.id; render(); },
    }));
    else items = [{ title: 'Edad, territorio y resultados', search: 'CDI edad territorio resultados', active: true, action: () => { render(); } }];
    const filtered = items.filter(item => matches(item.search));
    $('items').replaceChildren(...filtered.map(item => {
      const node = button(item.title, item.action);
      node.setAttribute('aria-current', String(item.active));
      return node;
    }));
    if (!filtered.length) $('items').append(el('p', 'No hay coincidencias en esta sección.', 'empty'));
  }
  function openService(id) { state.mode = 'catalogue'; state.selected = id; $('search').value = ''; render(); }
  function openAsesor(id) { state.mode = 'asesor'; state.selected = id; $('search').value = ''; render(); }

  function renderRoutes() {
    const population = data.pilot.paths.find(item => item.id === state.population);
    header('Lógica observada en el piloto', '¿Para quién buscas ayuda?', 'Selecciona un público a la izquierda. Cada rama conserva la pregunta y los resultados del piloto; selecciona una necesidad para anotar tu revisión.');
    const stage = $('stage');
    const root = el('div', undefined, 'route-root');
    root.append(el('small', 'Pregunta 1 · Público seleccionado'), el('h3', population.label));
    stage.append(root);
    const labels = el('div', undefined, 'diagram-labels');
    labels.append(el('span', 'Pregunta 2 · ¿Qué necesitas?'), el('span', 'Servicios que muestra el piloto'));
    stage.append(labels);
    const branches = el('div', undefined, 'branches');
    for (const [id, title, results] of population.needs) {
      const row = el('div', undefined, 'branch');
      const columns = el('div', undefined, 'branch-columns');
      const need = button(title, () => { state.need = id; renderRoutes(); }, 'need');
      need.setAttribute('aria-pressed', String(state.need === id));
      need.append(el('small', 'Seleccionar para revisar esta asociación'));
      const resultNodes = el('div', undefined, 'service-nodes');
      for (const serviceId of results) resultNodes.append(button(services.get(serviceId).title, () => openService(serviceId), 'service-node'));
      if (!results.length) resultNodes.append(button('Abre el catálogo completo', () => { state.mode = 'catalogue'; state.selected = null; render(); }, 'service-node'));
      columns.append(need, resultNodes);
      row.append(columns);
      branches.append(row);
    }
    stage.append(branches);
    notice(stage, 'Son asociaciones fijas del piloto. No verifican edad, discapacidad, Registro Social, requisitos o disponibilidad.', true);
    if (population.id === 'infancia') notice(stage, 'Revisar: «Necesita protección» también devuelve Bono de orfandad, aunque el piloto no pregunta si existe orfandad.');
    source(stage, 'Fuente: paths y showMatches', pilotSource, '01-piloto.md');
    showEditor(`ruta/${population.id}/${state.need}`);
  }
  function renderCatalogue() {
    const item = services.get(state.selected);
    if (!item) {
      header('Texto del catálogo del piloto', 'Los 18 servicios', 'Explora las fichas sin completar el cuestionario. El contenido fuente es de solo lectura.');
      const entries = [...services.values()].filter(s => matches(`${s.title} ${s.short}`));
      for (const service of entries) {
        const node = button('', () => openService(service.id), 'list-entry');
        node.append(el('strong', service.title), el('span', service.short));
        $('stage').append(node);
      }
      if (!entries.length) $('stage').append(el('p', 'No hay coincidencias. Prueba otro término.', 'empty'));
      showEditor('catalogo');
      return;
    }
    header('Ficha del piloto · Contenido observado', item.title, 'Puedes proponer cambios en el panel de revisión sin modificar el texto original.');
    const stage = $('stage');
    stage.append(button('Volver al diagrama de rutas', () => { state.mode = 'routes'; state.selected = null; render(); }, 'back-link'));
    const fact = el('article', undefined, 'fact');
    fact.append(el('span', 'Publicado en el piloto', 'badge'));
    section(fact, 'Qué ofrece', item.short);
    section(fact, '¿Para quién?', item.who);
    section(fact, '¿Cómo acceder?', item.access);
    notice(fact, item.map
      ? 'Solo esta ficha abre un mapa en el catálogo original. La presencia de un punto no demuestra vacantes.'
      : 'En el piloto, el punto de atención de este servicio está pendiente de validación. No habilita un mapa.');
    stage.append(fact);
    const comparison = comparisons[item.id];
    const box = el('section', undefined, 'compare');
    box.append(el('h3', 'Complemento para comparar, no equivalencia aprobada'));
    box.append(el('p', comparison?.text || 'No se encontró una ficha específica en las ocho fichas de inclusión capturadas. Esto no significa que el servicio no exista.'));
    for (const id of comparison?.ids || []) {
      if (asesor.has(id)) box.append(button(`Leer: ${asesor.get(id).nombre}`, () => openAsesor(id)));
    }
    stage.append(box);
    source(stage, 'Fuente: catálogo del piloto', pilotSource, '03-cruce-y-pendientes.md');
    showEditor(`servicio/${item.id}`);
  }
  function renderAsesor() {
    const item = asesor.get(state.selected);
    if (!item) {
      header('Complemento publicado · No es un cuestionario', 'Fichas de Asesor593', 'Ocho fichas activas de inclusión en la captura. Requisitos y cifras son contenido publicado, pendiente de comprobar institucionalmente.');
      const entries = [...asesor.values()].filter(s => matches(`${s.nombre} ${s.resumen}`));
      for (const service of entries) {
        const node = button('', () => openAsesor(service.id), 'list-entry');
        node.append(el('strong', service.nombre), el('span', service.resumen));
        $('stage').append(node);
      }
      if (!entries.length) $('stage').append(el('p', 'No hay coincidencias. Prueba otro término.', 'empty'));
      showEditor('asesor');
      return;
    }
    header('Asesor593 · Ficha publicada en la captura', item.nombre, 'No usar automáticamente estos textos como reglas de admisión o aprobación de un beneficio.');
    const stage = $('stage');
    const fact = el('article', undefined, 'fact');
    fact.append(el('span', 'Fuente publicada, no validación jurídica', 'badge pending'));
    if (item.id.startsWith('otorgamiento-de-permisos')) notice(fact, 'Trámite para operar una unidad. No son requisitos para ingresar a una niña o niño a CDI.');
    if (item.id === 'bono-joaquin-gallegos') notice(fact, 'Falta el porcentaje concreto de discapacidad y el metadato normativa menciona hoja de vida. No completar por suposición.');
    section(fact, 'Resumen', item.resumen);
    section(fact, '¿En qué consiste?', item.consiste);
    section(fact, '¿A quién está dirigido?', item.dirigido);
    section(fact, '¿Qué obtienes?', item.beneficio);
    section(fact, 'Requisitos publicados', item.requisitos || []);
    const steps = section(fact, 'Pasos publicados', '');
    steps.lastChild.remove();
    for (const step of item.pasos || []) {
      const block = el('div', undefined, 'fact-section');
      block.append(el('h4', step.titulo), el('p', step.detalle));
      steps.append(block);
    }
    section(fact, 'Modalidad', item.modalidad);
    section(fact, 'Horarios publicados', item.horarios);
    section(fact, 'Tiempo estimado publicado', item.tiempo);
    const channels = section(fact, 'Canales publicados', '');
    channels.lastChild.remove();
    for (const channel of item.canales || []) {
      const block = el('div', undefined, 'fact-section');
      block.append(el('h4', channel.nombre));
      for (const [key, value] of Object.entries(channel)) {
        if (key !== 'nombre') block.append(el('p', `${key}: ${value}`));
      }
      channels.append(block);
    }
    const details = el('details');
    details.append(el('summary', 'Metadatos API: conservar sin inferir requisitos'));
    notice(details, 'Estos campos no aparecen como secciones en la plantilla pública consultada. Se muestran aquí como evidencia, incluidas sus erratas.');
    section(details, 'normativa', item.normativa);
    section(details, 'documentos', item.documentos);
    fact.append(details);
    stage.append(fact);
    source(stage, 'Abrir ficha en Asesor593', `https://asesor593.trabajo.gob.ec/servicios/${encodeURIComponent(item.id)}`, '02-asesor593.md');
    showEditor(`asesor/${item.id}`);
  }
  function renderCdi() {
    header('Flujo observado independiente del cuestionario general', 'CDI: edad, territorio y resultados', 'Este diagrama explica la segunda página CDI del piloto. No filtra centros ni simula la admisión de una persona.');
    const stage = $('stage');
    const ageStep = el('section', undefined, 'step');
    ageStep.append(el('h3', '1. ¿Qué edad tiene tu niña o niño?'), el('p', 'Las opciones solo cambian avisos informativos; no cambian los centros filtrados.'));
    const options = el('div', undefined, 'age-options');
    for (const [id, title, text] of ages) options.append(button(title, () => {
      $('age-explanation').textContent = text;
      showEditor(`cdi/edad/${id}`);
    }));
    ageStep.append(options, el('p', 'Selecciona una opción para leer y revisar su comportamiento.', 'notice info'));
    ageStep.lastChild.id = 'age-explanation';
    stage.append(ageStep);
    const territory = el('section', undefined, 'step');
    territory.append(el('h3', '2. ¿Dónde buscas un centro?'), el('p', 'Provincia requerida para continuar; cantón y parroquia filtran en cascada. No se solicita dirección escrita.'));
    territory.append(button('Revisar selección territorial', () => showEditor('cdi/territorio')));
    stage.append(territory);
    const results = el('section', undefined, 'step');
    results.append(el('h3', '3. Centros por territorio'), el('p', 'Resultado con mapa, listado, administración y enlace «Cómo llegar». El filtro usa únicamente provincia, cantón y parroquia.'));
    notice(results, 'El resultado no confirma cupos, horarios actuales ni aceptación de solicitudes. La edad no es un filtro.');
    results.append(button('Revisar resultados', () => showEditor('cdi/resultados')));
    stage.append(results);
    const alternative = el('section', undefined, 'fact');
    alternative.append(el('h3', 'Alternativa: Ver todos los centros'), el('p', 'Omite la selección de edad y utiliza los filtros territoriales que haya en pantalla.'));
    alternative.append(button('Revisar esta alternativa', () => showEditor('cdi/todos')));
    stage.append(alternative);
    notice(stage, 'No confundir con el localizador integrado del catálogo general: aquel permite provincia y radio de geolocalización. Son dos flujos distintos.');
    source(stage, 'Fuente: página CDI del piloto', cdiSource, '01-piloto.md');
    showEditor('cdi');
  }
  function renderIssues() {
    const selected = issues.find(item => item.id === state.selected);
    header('Pendientes identificados en la investigación', selected ? `${selected.id} · ${selected.title}` : 'Decisiones antes de diseñar', 'Estas dudas no se resuelven por inferencia. Anota acuerdos propuestos y la validación que falta; el estado de revisión no convierte una propuesta en norma.');
    const stage = $('stage');
    if (selected) {
      notice(stage, selected.text);
      source(stage, 'Ver cruce y pendientes documentados', '03-cruce-y-pendientes.md', '00-fuentes.md');
      showEditor(`pendiente/${selected.id}`);
    } else {
      for (const item of issues.filter(i => matches(`${i.title} ${i.text}`))) {
        const node = button('', () => { state.selected = item.id; render(); }, 'list-entry');
        node.append(el('strong', `${item.id} · ${item.title}`), el('span', item.text));
        stage.append(node);
      }
      showEditor('pendientes');
    }
  }
  function renderInventory() {
    const selected = inventoryGroups.find(group => inventoryKey('servicio', [group.service]) === state.selected);
    header('Relación observada en PostgreSQL · No es una taxonomía aprobada',
      selected ? rawLabel(selected.service) : 'Servicio, modalidad y valores de mod_abv',
      'Captura agregada de unidades_atencion. Los textos se conservan sin normalizar. Selecciona un servicio y después una modalidad o combinación para registrar observaciones.');
    const stage = $('stage');
    const totals = el('div', undefined, 'inventory-summary');
    for (const [label, value] of [
      ['Servicios no vacíos', inventory.totals.services], ['Modalidades no vacías', inventory.totals.modalities],
      ['Combinaciones exactas', inventory.totals.combinations], ['Filas de unidades', inventory.totals.units],
    ]) {
      const item = el('p');
      item.append(el('strong', formatCount(value)), el('span', label));
      totals.append(item);
    }
    stage.append(totals);
    notice(stage, 'Cada conexión significa «aparece en esos registros», no «regla oficial de pertenencia» ni «cumple requisitos». Los conteos no son cupos, personas ni códigos institucionales distintos.', true);
    if (!selected) {
      for (const group of inventoryGroups.filter(group => matches(`${rawLabel(group.service)} ${[...group.modalities.keys()].map(rawLabel).join(' ')} ${[...group.modalities.values()].flat().map(row => rawLabel(row.mod_abv)).join(' ')}`))) {
        const node = button('', () => { state.selected = inventoryKey('servicio', [group.service]); render(); }, 'list-entry');
        node.append(el('strong', rawLabel(group.service)),
          el('span', `${group.modalities.size} modalidades observadas · ${formatCount(group.total)} filas de unidades`));
        stage.append(node);
      }
      const shared = new Map();
      for (const row of inventory.rows) {
        if (!shared.has(row.mod_abv)) shared.set(row.mod_abv, new Set());
        shared.get(row.mod_abv).add(row.servicio);
      }
      const repeated = [...shared].filter(([, serviceSet]) => serviceSet.size > 1);
      if (repeated.length) {
        const box = el('section', undefined, 'fact');
        box.append(el('h3', 'Valores de mod_abv compartidos entre servicios'));
        for (const [value, serviceSet] of repeated) {
          section(box, rawLabel(value), [...serviceSet].map(rawLabel));
        }
        notice(box, 'No usar mod_abv como identificador único ni enlazar modalidades de servicios distintos por compartir esa etiqueta.');
        stage.append(box);
      }
      showEditor('inventario');
    } else {
      stage.append(button('Ver todos los servicios observados', () => { state.selected = null; render(); }, 'back-link'));
      const root = el('div', undefined, 'route-root');
      root.append(el('small', 'Servicio exacto en la base'), el('h3', rawLabel(selected.service)),
        el('p', `${formatCount(selected.total)} filas de unidades`));
      stage.append(root);
      const labels = el('div', undefined, 'diagram-labels');
      labels.append(el('span', 'Modalidad exacta: mod'), el('span', 'Valores observados de mod_abv'));
      stage.append(labels);
      const branches = el('div', undefined, 'branches');
      for (const [modality, rows] of selected.modalities) {
        const branch = el('div', undefined, 'branch');
        const columns = el('div', undefined, 'branch-columns');
        const count = rows.reduce((sum, row) => sum + row.unidades, 0);
        const node = button(rawLabel(modality), () => showEditor(inventoryKey('modalidad', [selected.service, modality])), 'need');
        node.append(el('small', `${formatCount(count)} filas · ${rows.length} combinación(es)`));
        const values = el('div', undefined, 'service-nodes');
        for (const row of rows) values.append(button(
          `${rawLabel(row.mod_abv)} · ${formatCount(row.unidades)} filas`,
          () => showEditor(inventoryKey('combinacion', [row.servicio, row.mod, row.mod_abv])),
          'service-node',
        ));
        columns.append(node, values);
        branch.append(columns);
        branches.append(branch);
      }
      stage.append(branches);
      if ([...selected.modalities.values()].some(rows => rows.length > 1)) {
        notice(stage, 'Una misma modalidad tiene varios valores de mod_abv. No asumir que este campo es una abreviatura literal o una submodalidad oficial.');
      }
      showEditor(inventoryKey('servicio', [selected.service]));
    }
    const missing = Object.entries(inventory.quality).filter(([, count]) => count > 0);
    if (missing.length) notice(stage, `Filas con campos ausentes: ${missing.map(([field, count]) => `${field}: ${formatCount(count)}`).join('; ')}.`);
    const provenance = el('p', `Captura: ${inventory.capturedAt}. Transacción de solo lectura confirmada.`, 'source');
    stage.append(provenance);
    const links = el('div', undefined, 'document-links');
    link('Consulta y captura agregada', 'fuentes/inventario-servicio-modalidad.md', links);
    link('Análisis de pertenencia y límites', '04-servicios-modalidades.md', links);
    stage.append(links);
  }
  function render() {
    renderNavigation();
    ({ routes: renderRoutes, inventory: renderInventory, catalogue: renderCatalogue, asesor: renderAsesor, cdi: renderCdi, issues: renderIssues })[state.mode]();
  }

  function download(content, filename, type) {
    const url = URL.createObjectURL(new Blob([content], { type }));
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = filename;
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url), 3000);
    $('message').textContent = 'Archivo preparado para descarga. Comprueba que el navegador lo haya guardado.';
  }
  $('review-form').addEventListener('submit', event => event.preventDefault());
  $('review-status').addEventListener('change', saveEditor);
  $('review-notes').addEventListener('input', saveEditor);
  $('review-proposal').addEventListener('input', saveEditor);
  $('search').addEventListener('input', render);
  $('export-json').addEventListener('click', () => download(JSON.stringify(envelope(), null, 2), 'borrador-revision-unidades.json', 'application/json;charset=utf-8'));
  $('export-md').addEventListener('click', () => {
    const quote = text => text.replace(/\r\n?/g, '\n').split('\n').map(line => `> ${line}`).join('\n');
    const lines = [
      '# Revisión de contenido: Unidades de Atención', '',
      `Captura fuente: ${data.date}.`, `Identificador: ${data.datasetId}.`, `Captura de inventario: ${inventory.capturedAt}.`,
      `Exportación: ${new Date().toISOString()}.`, '',
      'Este documento contiene observaciones y propuestas. No modifica las fuentes ni acredita aprobación institucional.', '',
      `Piloto: ${pilotSource}`, 'Asesor593: https://asesor593.trabajo.gob.ec/api/servicios', '',
    ];
    for (const [key, item] of Object.entries(notes)) {
      lines.push(`## ${metadata.get(key)}`, '', `Elemento: ${key}`, `Estado: ${statusLabels[item.status]}`,
        ...(item.evidenceRevision ? [`Captura de evidencia de la nota: ${item.evidenceRevision}`] : []), '',
        '### Observaciones', '', quote(item.notes || 'Sin observaciones.'), '',
        '### Redacción o cambio propuesto', '', quote(item.proposal || 'Sin propuesta.'), '');
    }
    if (!Object.keys(notes).length) lines.push('Todavía no se han registrado observaciones.');
    download(lines.join('\n'), 'revision-contenido-unidades.md', 'text/markdown;charset=utf-8');
  });
  $('import-button').addEventListener('click', () => $('import-file').click());
  window.addEventListener('storage', event => {
    if ((event.key === storageKey || event.key === null) && event.newValue !== storedVersion) {
      externalChange = true;
      persistent = false;
      updateSaveStatus();
    }
  });
  $('import-file').addEventListener('change', async event => {
    const file = event.target.files[0];
    if (!file) return;
    try {
      if (file.size > 5000000) throw new Error('El archivo supera el límite de 5 MB.');
      const imported = validateDraft(JSON.parse(await file.text()));
      const count = Object.keys(imported).length;
      if (!confirm(`Importar ${count} observaciones de esta captura? Se reemplazan las notas de los elementos incluidos; las demás se conservan.`)) return;
      for (const [key, value] of Object.entries(imported)) notes[key] = value;
      persist();
      showEditor(currentKey);
      $('message').textContent = `Se importaron ${count} elementos. Las fuentes no se modificaron.`;
    } catch (error) {
      $('message').textContent = error instanceof SyntaxError ? 'No se pudo leer el JSON. No se ha importado.' : error.message;
    } finally { event.target.value = ''; }
  });
  render();
})();
