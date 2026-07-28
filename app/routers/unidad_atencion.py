from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import func, select
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

    return FeatureCollection(
        features=[_unidad_to_feature(u) for u in unidades],
        total=total,
        limit=limit if limit else 0,
        offset=offset,
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
    return _unidad_to_feature(unidad)


@router.get("/{unidad_id}/raw", response_model=UnidadRaw)
async def get_unidad_raw(request: Request, unidad_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(UnidadAtencion).where(UnidadAtencion.id == unidad_id)
    )
    unidad = result.scalar_one_or_none()
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    return _unidad_to_raw(unidad)
