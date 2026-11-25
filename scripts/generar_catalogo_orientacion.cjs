const fs = require('node:fs')
const path = require('node:path')
const crypto = require('node:crypto')

const root = path.resolve(__dirname, '..')
const source = 'docs/conocimiento-unidades/fuentes/piloto-catalogo-y-rutas.md'
const text = fs.readFileSync(path.join(root, source), 'utf8')
const match = text.match(/```json\r?\n([\s\S]*?)\r?\n```/)
if (!match) throw new Error('No se encontró la captura JSON del piloto.')
const content = JSON.parse(match[1])
const ids = new Set(content.services.map(item => item.id))
if (ids.size !== 18 || content.paths.length !== 6 ||
    content.paths.reduce((n, item) => n + item.needs.length, 0) !== 20 ||
    content.paths.some(item => item.needs.some(need => need[2].some(id => !ids.has(id))))) {
  throw new Error('La captura cambió: revisar el alcance antes de generar.')
}
const output = 'frontend/src/features/orientacion/catalogo.json'
fs.mkdirSync(path.dirname(path.join(root, output)), { recursive: true })
fs.writeFileSync(path.join(root, output), JSON.stringify({
  source, capturedAt: '2026-11-24',
  sha256: crypto.createHash('sha256').update(text).digest('hex'),
  ...content,
}, null, 2) + '\n')
console.log(`Catálogo generado sin modificar las fuentes: ${output}`)
