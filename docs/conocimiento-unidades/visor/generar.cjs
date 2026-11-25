const fs = require('node:fs')
const path = require('node:path')
const crypto = require('node:crypto')

const base = path.resolve(__dirname, '..')
const inputs = ['piloto-catalogo-y-rutas.md', 'asesor593-inclusion-publicada.md']
const captures = inputs.map(name => fs.readFileSync(path.join(base, 'fuentes', name), 'utf8'))
const parse = (text) => {
  const match = text.match(/```json\r?\n([\s\S]*?)\r?\n```/)
  if (!match) throw new Error('La captura no contiene un bloque JSON.')
  return JSON.parse(match[1])
}
const pilot = parse(captures[0])
const asesor = parse(captures[1])
const inventoryText = fs.readFileSync(path.join(base, 'fuentes', 'inventario-servicio-modalidad.md'), 'utf8')
const inventory = parse(inventoryText)
if (inventory.format !== 'ua-service-modality-inventory' || inventory.version !== 1 ||
    inventory.transactionReadOnly !== true || !Array.isArray(inventory.rows) ||
    inventory.rows.some(row => ['servicio', 'mod', 'mod_abv'].some(key => row[key] !== null && typeof row[key] !== 'string') ||
      !Number.isSafeInteger(row.unidades) || row.unidades < 1) ||
    inventory.rows.reduce((sum, row) => sum + row.unidades, 0) !== inventory.totals.units ||
    inventory.rows.length !== inventory.totals.combinations) {
  throw new Error('La captura del inventario agregado no tiene el formato o los conteos esperados.')
}
if (pilot.services.length !== 18 || pilot.paths.length !== 6 || asesor.length !== 8) {
  throw new Error('Cambió la captura: revisar el alcance antes de regenerar el visor.')
}
const serviceIds = new Set(pilot.services.map(item => item.id))
const routes = pilot.paths.flatMap(item => item.needs)
if (routes.length !== 20 || routes.some(item => item[2].some(id => !serviceIds.has(id)))) {
  throw new Error('Las rutas de la captura no coinciden con el catálogo documentado.')
}
const data = {
  datasetId: crypto.createHash('sha256').update(captures.join('\n')).digest('hex'),
  date: '2026-11-24',
  commit: '36eec6664f38af0eb1dcd3c1f17aa79c65480468',
  pilot,
  asesor,
  inventory,
}
const replacements = {
  '/*__CSS__*/': fs.readFileSync(path.join(__dirname, 'visor.css'), 'utf8'),
  '/*__JS__*/': fs.readFileSync(path.join(__dirname, 'visor.js'), 'utf8'),
  '/*__DATA__*/': JSON.stringify(data).replace(/</g, '\\u003c'),
}
let html = fs.readFileSync(path.join(__dirname, 'index.template.html'), 'utf8')
for (const [marker, text] of Object.entries(replacements)) {
  if (!html.includes(marker)) throw new Error(`No se encontró ${marker}.`)
  html = html.replace(marker, () => text)
}
fs.writeFileSync(path.join(base, 'visor.html'), html, 'utf8')
console.log('Visor autónomo generado: docs/conocimiento-unidades/visor.html')
