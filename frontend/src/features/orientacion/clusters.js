import Supercluster from 'supercluster'

export function createCentrosIndex(centros) {
  return new Supercluster({ radius: 46, maxZoom: 18 }).load(
    centros.map(centro => ({
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [centro.lng, centro.lat] },
      properties: { centroId: centro.id },
    })),
  )
}
