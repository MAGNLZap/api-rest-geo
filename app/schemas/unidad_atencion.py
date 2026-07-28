from pydantic import BaseModel


class Point(BaseModel):
    type: str = "Point"
    coordinates: tuple[float, float]


class UnidadProperties(BaseModel):
    id: int
    cluster_count: int | None = None
    cell_id: str | None = None
    zon_plan: str | None = None
    dis_sen: str | None = None
    uni_des: str | None = None
    dpa_despro: str | None = None
    dpa_prov: str | None = None
    dpa_descan: str | None = None
    dpa_can: str | None = None
    dpa_despar: str | None = None
    dpa_par: str | None = None
    region: str | None = None
    co_siimdh: int | None = None
    nombre: str
    servicio: str | None = None
    mod: str | None = None
    mod_abv: str | None = None
    dir: str | None = None
    ref: str | None = None
    ruc: str | None = None
    tipo_admin: str | None = None
    cooperante: str | None = None
    tipo: str | None = None
    hombre: int | None = None
    mujer: int | None = None
    total: int | None = None
    area: str | None = None
    asis_prom: float | None = None
    asistencia: int | None = None
    rs18: int | None = None
    no_rs18: int | None = None
    ext_pob18: int | None = None
    pob18: int | None = None
    no_pob18: int | None = None
    rs25: int | None = None
    no_rs25: int | None = None
    ext_pob25: int | None = None
    pob25: int | None = None
    no_pob25: int | None = None
    x: float | None = None
    y: float | None = None
    link_ubi: str | None = None
    corte: str | None = None


class Feature(BaseModel):
    type: str = "Feature"
    geometry: Point
    properties: UnidadProperties
    id: str


class FeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: list[Feature]
    total: int
    limit: int
    offset: int


class UnidadRaw(BaseModel):
    id: int
    zon_plan: str | None = None
    dis_sen: str | None = None
    uni_des: str | None = None
    dpa_despro: str | None = None
    dpa_prov: str | None = None
    dpa_descan: str | None = None
    dpa_can: str | None = None
    dpa_despar: str | None = None
    dpa_par: str | None = None
    region: str | None = None
    co_siimdh: int | None = None
    nombre: str
    servicio: str | None = None
    mod: str | None = None
    mod_abv: str | None = None
    dir: str | None = None
    ref: str | None = None
    ruc: str | None = None
    tipo_admin: str | None = None
    cooperante: str | None = None
    tipo: str | None = None
    hombre: int | None = None
    mujer: int | None = None
    total: int | None = None
    area: str | None = None
    asis_prom: float | None = None
    asistencia: int | None = None
    rs18: int | None = None
    no_rs18: int | None = None
    ext_pob18: int | None = None
    pob18: int | None = None
    no_pob18: int | None = None
    rs25: int | None = None
    no_rs25: int | None = None
    ext_pob25: int | None = None
    pob25: int | None = None
    no_pob25: int | None = None
    x: float | None = None
    y: float | None = None
    longitude: float
    latitude: float
    link_ubi: str | None = None
    corte: str | None = None


class UnidadRawList(BaseModel):
    data: list[UnidadRaw]
    total: int
    limit: int
    offset: int
