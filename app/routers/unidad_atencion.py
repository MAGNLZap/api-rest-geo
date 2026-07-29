from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy import Float, Integer, func, literal as lit, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.unidad_atencion import UnidadAtencion
from app.schemas.unidad_atencion import (
    Feature,
    FeatureCollection,
    Point,
    UnidadProperties,
    UnidadRaw,
    UnidadRawList,
)

router = APIRouter(prefix="/unidades", tags=["unidades"])


def _parse_bbox(bbox: str) -> tuple[float, float, float, float]:
    parts = bbox.split(",")
    if len(parts) != 4:
        raise HTTPException(
            status_code=400,
            detail="bbox must have exactly 4 values: min_lng,min_lat,max_lng,max_lat",
        )
    try:
        return float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="bbox values must be numbers: min_lng,min_lat,max_lng,max_lat",
        )


def _zoom_to_grid_size(zoom: int) -> int:
    if zoom <= 5:
        return 4
    if zoom <= 8:
        return 8
    if zoom <= 11:
        return 12
    if zoom <= 14:
        return 16
    return 20


def _unidad_to_feature(u: UnidadAtencion) -> Feature:
    return Feature(
        geometry=Point(coordinates=(u.longitude, u.latitude)),
        properties=UnidadProperties(
            id=u.id,
            zon_plan=u.zon_plan,
            dis_sen=u.dis_sen,
            uni_des=u.uni_des,
            dpa_despro=u.dpa_despro,
            dpa_prov=u.dpa_prov,
            dpa_descan=u.dpa_descan,
            dpa_can=u.dpa_can,
            dpa_despar=u.dpa_despar,
            dpa_par=u.dpa_par,
            region=u.region,
            co_siimdh=u.co_siimdh,
            nombre=u.nombre,
            servicio=u.servicio,
            mod=u.mod,
            mod_abv=u.mod_abv,
            dir=u.dir,
            ref=u.ref,
            ruc=u.ruc,
            tipo_admin=u.tipo_admin,
            cooperante=u.cooperante,
            tipo=u.tipo,
            hombre=u.hombre,
            mujer=u.mujer,
            total=u.total,
            area=u.area,
            asis_prom=u.asis_prom,
            asistencia=u.asistencia,
            rs18=u.rs18,
            no_rs18=u.no_rs18,
            ext_pob18=u.ext_pob18,
            pob18=u.pob18,
            no_pob18=u.no_pob18,
            rs25=u.rs25,
            no_rs25=u.no_rs25,
            ext_pob25=u.ext_pob25,
            pob25=u.pob25,
            no_pob25=u.no_pob25,
            x=u.x,
            y=u.y,
            link_ubi=u.link_ubi,
            corte=u.corte,
        ),
        id=str(u.id),
    )


def _unidad_to_raw(u: UnidadAtencion) -> UnidadRaw:
    return UnidadRaw(
        id=u.id,
        zon_plan=u.zon_plan,
        dis_sen=u.dis_sen,
        uni_des=u.uni_des,
        dpa_despro=u.dpa_despro,
        dpa_prov=u.dpa_prov,
        dpa_descan=u.dpa_descan,
        dpa_can=u.dpa_can,
        dpa_despar=u.dpa_despar,
        dpa_par=u.dpa_par,
        region=u.region,
        co_siimdh=u.co_siimdh,
        nombre=u.nombre,
        servicio=u.servicio,
        mod=u.mod,
        mod_abv=u.mod_abv,
        dir=u.dir,
        ref=u.ref,
        ruc=u.ruc,
        tipo_admin=u.tipo_admin,
        cooperante=u.cooperante,
        tipo=u.tipo,
        hombre=u.hombre,
        mujer=u.mujer,
        total=u.total,
        area=u.area,
        asis_prom=u.asis_prom,
        asistencia=u.asistencia,
        rs18=u.rs18,
        no_rs18=u.no_rs18,
        ext_pob18=u.ext_pob18,
        pob18=u.pob18,
        no_pob18=u.no_pob18,
        rs25=u.rs25,
        no_rs25=u.no_rs25,
        ext_pob25=u.ext_pob25,
        pob25=u.pob25,
        no_pob25=u.no_pob25,
        x=u.x,
        y=u.y,
        longitude=u.longitude,
        latitude=u.latitude,
        link_ubi=u.link_ubi,
        corte=u.corte,
    )


def _unidad_to_clustered_feature(
    u: UnidadAtencion, cluster_count: int, cell_id: str
) -> Feature:
    props = UnidadProperties(
        id=u.id,
        cluster_count=cluster_count,
        cell_id=cell_id,
        zon_plan=u.zon_plan,
        dis_sen=u.dis_sen,
        uni_des=u.uni_des,
        dpa_despro=u.dpa_despro,
        dpa_prov=u.dpa_prov,
        dpa_descan=u.dpa_descan,
        dpa_can=u.dpa_can,
        dpa_despar=u.dpa_despar,
        dpa_par=u.dpa_par,
        region=u.region,
        co_siimdh=u.co_siimdh,
        nombre=u.nombre,
        servicio=u.servicio,
        mod=u.mod,
        mod_abv=u.mod_abv,
        dir=u.dir,
        ref=u.ref,
        ruc=u.ruc,
        tipo_admin=u.tipo_admin,
        cooperante=u.cooperante,
        tipo=u.tipo,
        hombre=u.hombre,
        mujer=u.mujer,
        total=u.total,
        area=u.area,
        asis_prom=u.asis_prom,
        asistencia=u.asistencia,
        rs18=u.rs18,
        no_rs18=u.no_rs18,
        ext_pob18=u.ext_pob18,
        pob18=u.pob18,
        no_pob18=u.no_pob18,
        rs25=u.rs25,
        no_rs25=u.no_rs25,
        ext_pob25=u.ext_pob25,
        pob25=u.pob25,
        no_pob25=u.no_pob25,
        x=u.x,
        y=u.y,
        link_ubi=u.link_ubi,
        corte=u.corte,
    )
    return Feature(
        geometry=Point(coordinates=(u.longitude, u.latitude)),
        properties=props,
        id=str(u.id),
    )


async def _cluster_unidades(
    db: AsyncSession,
    min_lng: float,
    min_lat: float,
    max_lng: float,
    max_lat: float,
    grid_size: int,
    filters: list,
) -> list[tuple[UnidadAtencion, int, str]]:
    bbox_lng = max_lng - min_lng
    bbox_lat = max_lat - min_lat
    cell_width = bbox_lng / grid_size
    cell_height = bbox_lat / grid_size

    cell_col = func.cast(
        (UnidadAtencion.longitude - min_lng) / cell_width, Integer
    )
    cell_row = func.cast(
        (UnidadAtencion.latitude - min_lat) / cell_height, Integer
    )
    cell_id_expr = func.concat(cell_col, lit(","), cell_row)

    center_lng = min_lng + (cell_col.cast(Float) + 0.5) * cell_width
    center_lat = min_lat + (cell_row.cast(Float) + 0.5) * cell_height
    diff_lng = UnidadAtencion.longitude - center_lng
    diff_lat = UnidadAtencion.latitude - center_lat
    dist_sq = diff_lng * diff_lng + diff_lat * diff_lat

    row_number = func.row_number().over(
        partition_by=[cell_col, cell_row], order_by=dist_sq
    )
    cluster_count = func.count("*").over(partition_by=[cell_col, cell_row])

    subq = (
        select(
            UnidadAtencion.id,
            cluster_count.label("_cc"),
            cell_id_expr.label("_cid"),
            row_number.label("_rn"),
        )
        .where(*filters)
        .where(
            UnidadAtencion.longitude >= min_lng,
            UnidadAtencion.longitude <= max_lng,
            UnidadAtencion.latitude >= min_lat,
            UnidadAtencion.latitude <= max_lat,
        )
        .subquery()
    )

    ids_result = await db.execute(
        select(subq.c.id, subq.c._cc, subq.c._cid)
        .where(subq.c._rn == 1)
        .limit(grid_size * grid_size)
    )
    rows = ids_result.all()

    if not rows:
        return []

    id_map = {}
    for row in rows:
        id_map[row[0]] = (row[1], row[2])

    unidades_result = await db.execute(
        select(UnidadAtencion).where(UnidadAtencion.id.in_(list(id_map.keys())))
    )
    unidades = {u.id: u for u in unidades_result.scalars().all()}

    return [
        (unidades[uid], count, cell_id)
        for uid, count, cell_id in [
            (row[0], row[1], row[2]) for row in rows
        ]
    ]




@router.get("", response_model=FeatureCollection)
async def list_unidades(
    request: Request,
    limit: int | None = Query(100, ge=0, le=1000),
    offset: int = Query(0, ge=0),
    region: str | None = Query(None),
    provincia: str | None = Query(None),
    canton: str | None = Query(None),
    servicio: str | None = Query(None),
    tipo: str | None = Query(None),
    area: str | None = Query(None),
    nombre: str | None = Query(None),
    bbox: str | None = Query(None),
    cluster: bool = Query(False),
    grid_size: int = Query(8, ge=2, le=32),
    zoom: int | None = Query(None, ge=0, le=19),
    db: AsyncSession = Depends(get_db),
):
    filters = []
    if region:
        filters.append(UnidadAtencion.region.ilike(f"%{region}%"))
    if provincia:
        filters.append(UnidadAtencion.dpa_despro.ilike(f"%{provincia}%"))
    if canton:
        filters.append(UnidadAtencion.dpa_descan.ilike(f"%{canton}%"))
    if servicio:
        filters.append(UnidadAtencion.servicio.ilike(f"%{servicio}%"))
    if tipo:
        filters.append(UnidadAtencion.tipo.ilike(f"%{tipo}%"))
    if area:
        filters.append(UnidadAtencion.area.ilike(f"%{area}%"))
    if nombre:
        filters.append(UnidadAtencion.nombre.ilike(f"%{nombre}%"))

    if cluster and bbox:
        min_lng, min_lat, max_lng, max_lat = _parse_bbox(bbox)

        effective_grid = _zoom_to_grid_size(zoom) if zoom is not None else grid_size

        bbox_filter = [
            UnidadAtencion.longitude >= min_lng,
            UnidadAtencion.longitude <= max_lng,
            UnidadAtencion.latitude >= min_lat,
            UnidadAtencion.latitude <= max_lat,
        ]
        count_result = await db.execute(
            select(func.count(UnidadAtencion.id)).where(*bbox_filter).where(*filters)
        )
        total_real = count_result.scalar()

        clustered = await _cluster_unidades(
            db, min_lng, min_lat, max_lng, max_lat, effective_grid, filters
        )
        return JSONResponse(
            content=FeatureCollection(
                features=[
                    _unidad_to_clustered_feature(u, count, cell_id)
                    for u, count, cell_id in clustered
                ],
                total=total_real,
                limit=effective_grid * effective_grid,
                offset=0,
            ).model_dump(),
            media_type="application/geo+json",
        )

    query = select(UnidadAtencion)
    count_query = select(func.count(UnidadAtencion.id))

    if bbox:
        min_lng, min_lat, max_lng, max_lat = _parse_bbox(bbox)
        bbox_filter = [
            UnidadAtencion.longitude >= min_lng,
            UnidadAtencion.longitude <= max_lng,
            UnidadAtencion.latitude >= min_lat,
            UnidadAtencion.latitude <= max_lat,
        ]
        query = query.where(*bbox_filter)
        count_query = count_query.where(*bbox_filter)

    if filters:
        query = query.where(*filters)
        count_query = count_query.where(*filters)

    total_result = await db.execute(count_query)
    total = total_result.scalar()

    if limit is None or limit > 0:
        effective_limit = limit if limit else 100
        query = query.offset(offset).limit(effective_limit)

    result = await db.execute(query)
    unidades = result.scalars().all()

    return JSONResponse(
        content=FeatureCollection(
            features=[_unidad_to_feature(u) for u in unidades],
            total=total,
            limit=limit if limit else 0,
            offset=offset,
        ).model_dump(),
        media_type="application/geo+json",
    )


@router.get("/raw", response_model=UnidadRawList)
async def list_unidades_raw(
    request: Request,
    limit: int | None = Query(100, ge=0, le=1000),
    offset: int = Query(0, ge=0),
    region: str | None = Query(None),
    provincia: str | None = Query(None),
    canton: str | None = Query(None),
    servicio: str | None = Query(None),
    tipo: str | None = Query(None),
    area: str | None = Query(None),
    nombre: str | None = Query(None),
    bbox: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(UnidadAtencion)
    count_query = select(func.count(UnidadAtencion.id))

    if bbox:
        min_lng, min_lat, max_lng, max_lat = _parse_bbox(bbox)
        bbox_filter = [
            UnidadAtencion.longitude >= min_lng,
            UnidadAtencion.longitude <= max_lng,
            UnidadAtencion.latitude >= min_lat,
            UnidadAtencion.latitude <= max_lat,
        ]
        query = query.where(*bbox_filter)
        count_query = count_query.where(*bbox_filter)

    if region:
        query = query.where(UnidadAtencion.region.ilike(f"%{region}%"))
        count_query = count_query.where(UnidadAtencion.region.ilike(f"%{region}%"))
    if provincia:
        query = query.where(UnidadAtencion.dpa_despro.ilike(f"%{provincia}%"))
        count_query = count_query.where(UnidadAtencion.dpa_despro.ilike(f"%{provincia}%"))
    if canton:
        query = query.where(UnidadAtencion.dpa_descan.ilike(f"%{canton}%"))
        count_query = count_query.where(UnidadAtencion.dpa_descan.ilike(f"%{canton}%"))
    if servicio:
        query = query.where(UnidadAtencion.servicio.ilike(f"%{servicio}%"))
        count_query = count_query.where(UnidadAtencion.servicio.ilike(f"%{servicio}%"))
    if tipo:
        query = query.where(UnidadAtencion.tipo.ilike(f"%{tipo}%"))
        count_query = count_query.where(UnidadAtencion.tipo.ilike(f"%{tipo}%"))
    if area:
        query = query.where(UnidadAtencion.area.ilike(f"%{area}%"))
        count_query = count_query.where(UnidadAtencion.area.ilike(f"%{area}%"))
    if nombre:
        query = query.where(UnidadAtencion.nombre.ilike(f"%{nombre}%"))
        count_query = count_query.where(UnidadAtencion.nombre.ilike(f"%{nombre}%"))

    total_result = await db.execute(count_query)
    total = total_result.scalar()

    if limit is None or limit > 0:
        effective_limit = limit if limit else 100
        query = query.offset(offset).limit(effective_limit)

    result = await db.execute(query)
    unidades = result.scalars().all()

    return UnidadRawList(
        data=[_unidad_to_raw(u) for u in unidades],
        total=total,
        limit=limit if limit else 0,
        offset=offset,
    )


@router.get("/{unidad_id}", response_model=Feature)
async def get_unidad(request: Request, unidad_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(UnidadAtencion).where(UnidadAtencion.id == unidad_id)
    )
    unidad = result.scalar_one_or_none()
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    return JSONResponse(
        content=_unidad_to_feature(unidad).model_dump(),
        media_type="application/geo+json",
    )


@router.get("/{unidad_id}/raw", response_model=UnidadRaw)
async def get_unidad_raw(request: Request, unidad_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(UnidadAtencion).where(UnidadAtencion.id == unidad_id)
    )
    unidad = result.scalar_one_or_none()
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    return _unidad_to_raw(unidad)
