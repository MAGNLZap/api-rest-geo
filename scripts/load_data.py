import argparse
import asyncio
import gzip
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from shapely import from_geojson, make_valid, set_precision, to_geojson
from shapely.geometry import GeometryCollection, MultiPolygon, Polygon
from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.database import async_session, engine
from app.models.base import Base
from app.models.unidad_atencion import UnidadAtencion

ROOT = Path(__file__).resolve().parent.parent
MIGRATIONS_DIR = ROOT / "scripts" / "sql" / "migrations"
SEED_DIR = ROOT / "data" / "seed"
EXPORT_DIR = ROOT / "app" / "data"
GRID_SIZE = 0.0001

DPA_SPECS = (
    {
        "level": "provincias",
        "table": "provinces",
        "file": "provincias.json",
        "columns": ("id", "name"),
    },
    {
        "level": "cantones",
        "table": "cantons",
        "file": "cantones.json",
        "columns": ("id", "name", "province_id"),
    },
    {
        "level": "parroquias",
        "table": "parishes",
        "file": "parroquias.json",
        "columns": ("id", "name", "canton_id", "province_id"),
    },
)


def _backend() -> str:
    if settings.DATABASE_URL.startswith("sqlite"):
        return "sqlite"
    if settings.DATABASE_URL.startswith("postgresql"):
        return "pg"
    raise SystemExit(f"DATABASE_URL no soportado: {settings.DATABASE_URL.split('://')[0]}://")


def _mask_url(url: str) -> str:
    return re.sub(r"://[^@]+@", "://***@", url)


async def _run_statements(conn: Any, sql: str) -> None:
    for statement in (part.strip() for part in sql.split(";")):
        if statement:
            await conn.execute(text(statement))


async def run_migrations() -> None:
    backend = _backend()
    paths = sorted(MIGRATIONS_DIR.glob(f"*.{backend}.sql"))
    if not paths:
        raise SystemExit(f"No hay migraciones para el backend {backend}")

    async with engine.begin() as conn:
        await conn.execute(
            text(
                "CREATE TABLE IF NOT EXISTS schema_migrations ("
                "version TEXT PRIMARY KEY, "
                "applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)"
            )
        )
        result = await conn.execute(text("SELECT version FROM schema_migrations"))
        applied = {row[0] for row in result}

        pending = 0
        for path in paths:
            version = path.name.split(".", 1)[0]
            if version in applied:
                continue
            await _run_statements(conn, path.read_text(encoding="utf-8"))
            await conn.execute(
                text("INSERT INTO schema_migrations (version) VALUES (:version)"),
                {"version": version},
            )
            pending += 1
            print(f"Migracion aplicada: {path.name}")

    if pending == 0:
        print(f"Migraciones al dia ({backend})")


def _polygonal(geometry: Any) -> MultiPolygon:
    if isinstance(geometry, Polygon):
        return MultiPolygon([geometry])
    if isinstance(geometry, MultiPolygon):
        return geometry
    if isinstance(geometry, GeometryCollection):
        polygons = []
        for part in geometry.geoms:
            if isinstance(part, Polygon):
                polygons.append(part)
            elif isinstance(part, MultiPolygon):
                polygons.extend(part.geoms)
        if polygons:
            return MultiPolygon(polygons)
    raise ValueError(f"Geometria no poligonal: {geometry.geom_type}")


def _round_coordinates(value: Any) -> Any:
    if isinstance(value, list):
        if value and isinstance(value[0], (int, float)):
            return [round(float(number), 4) for number in value]
        return [_round_coordinates(item) for item in value]
    return value


def _normalize_geometry(raw: dict[str, Any]) -> dict[str, Any]:
    geometry = from_geojson(json.dumps(raw, separators=(",", ":")))
    geometry = _polygonal(make_valid(geometry))
    geometry = _polygonal(set_precision(geometry, GRID_SIZE, mode="valid_output"))
    geometry = _polygonal(make_valid(geometry))
    normalized = json.loads(to_geojson(geometry))
    normalized["coordinates"] = _round_coordinates(normalized["coordinates"])

    final_geometry = from_geojson(json.dumps(normalized, separators=(",", ":")))
    if not final_geometry.is_valid:
        raise ValueError("La geometria sigue siendo invalida despues de normalizar")
    return normalized


def _feature(properties: dict[str, str], geometry: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "Feature",
        "id": properties["id"],
        "geometry": geometry,
        "properties": properties,
    }


def _validate_collections(collections: dict[str, dict[str, Any]]) -> None:
    ids: dict[str, set[str]] = {}
    for spec in DPA_SPECS:
        level = spec["level"]
        collection = collections[level]
        if collection.get("type") != "FeatureCollection":
            raise ValueError(f"{level} no es FeatureCollection")
        level_ids = [str(f["properties"]["id"]) for f in collection["features"]]
        if len(level_ids) != len(set(level_ids)):
            raise ValueError(f"Hay id duplicados en {level}")
        ids[level] = set(level_ids)

        for feature in collection["features"]:
            properties = feature["properties"]
            missing = set(spec["columns"]) - set(properties)
            if missing:
                raise ValueError(f"Faltan propiedades en {level}: {sorted(missing)}")
            geometry = from_geojson(json.dumps(feature["geometry"], separators=(",", ":")))
            if not geometry.is_valid or geometry.geom_type != "MultiPolygon":
                raise ValueError(f"Geometria invalida en {level} {properties['id']}")

    canton_provinces = {}
    for feature in collections["cantones"]["features"]:
        canton_id = feature["properties"]["id"]
        province_id = feature["properties"]["province_id"]
        if province_id not in ids["provincias"]:
            raise ValueError(f"Provincia inexistente: {province_id}")
        canton_provinces[canton_id] = province_id

    for feature in collections["parroquias"]["features"]:
        properties = feature["properties"]
        if properties["province_id"] not in ids["provincias"]:
            raise ValueError(f"Provincia inexistente: {properties['province_id']}")
        if properties["canton_id"] not in ids["cantones"]:
            raise ValueError(f"Canton inexistente: {properties['canton_id']}")
        if properties["province_id"] != canton_provinces[properties["canton_id"]]:
            raise ValueError(f"Jerarquia inconsistente en parroquia: {properties['id']}")


def _read_seed() -> dict[str, dict[str, Any]]:
    collections = {}
    for spec in DPA_SPECS:
        path = SEED_DIR / spec["file"]
        if not path.is_file():
            raise SystemExit(f"No se encontro la semilla DPA: {path}")
        collections[spec["level"]] = json.loads(path.read_text(encoding="utf-8"))
    _validate_collections(collections)
    return collections


def _upsert_sql(spec: dict[str, Any], backend: str) -> str:
    columns = (*spec["columns"], "geom")
    geom = (
        "ST_Multi(ST_CollectionExtract(ST_MakeValid(ST_SetSRID(ST_GeomFromGeoJSON(:geom), 4326)), 3))"
        if backend == "pg"
        else ":geom"
    )
    values = ", ".join(geom if column == "geom" else f":{column}" for column in columns)
    updates = ", ".join(f"{column} = EXCLUDED.{column}" for column in columns if column != "id")
    return (
        f"INSERT INTO {spec['table']} ({', '.join(columns)}) VALUES ({values}) ON CONFLICT (id) DO UPDATE SET {updates}"
    )


async def load_dpa(clear: bool = False) -> None:
    await run_migrations()
    backend = _backend()
    collections = _read_seed()
    print(f"Backend: {backend} ({_mask_url(settings.DATABASE_URL)})")

    async with engine.begin() as conn:
        if backend == "sqlite":
            await conn.execute(text("PRAGMA foreign_keys = ON"))
        if clear:
            for spec in reversed(DPA_SPECS):
                await conn.execute(text(f"DELETE FROM {spec['table']}"))
            print("Tablas DPA limpiadas")

        total = 0
        for spec in DPA_SPECS:
            rows = []
            for feature in collections[spec["level"]]["features"]:
                row = dict(feature["properties"])
                row["geom"] = json.dumps(feature["geometry"], separators=(",", ":"))
                rows.append(row)
            await conn.execute(text(_upsert_sql(spec, backend)), rows)
            total += len(rows)
            print(f"{spec['table']}: {len(rows)} upserts")

    print(f"Total DPA: {total}")
    await validate_database()


async def validate_database() -> None:
    backend = _backend()
    async with async_session() as session:
        print("Validacion:")
        for spec in DPA_SPECS:
            count = (await session.execute(text(f"SELECT count(*) FROM {spec['table']}"))).scalar_one()
            print(f"  {spec['table']}: {count}")

            if backend == "pg":
                invalid = (
                    await session.execute(
                        text(
                            f"SELECT count(*) FROM {spec['table']} "
                            "WHERE ST_SRID(geom) <> 4326 "
                            "OR GeometryType(geom) <> 'MULTIPOLYGON' "
                            "OR NOT ST_IsValid(geom)"
                        )
                    )
                ).scalar_one()
                if invalid:
                    raise ValueError(f"{spec['table']} tiene {invalid} geometrías invalidas")
                print("    geometria: OK")


async def _collection_from_database(spec: dict[str, Any]) -> dict[str, Any]:
    backend = _backend()
    columns = ", ".join(spec["columns"])
    geom = "ST_AsGeoJSON(geom, 4) AS geom" if backend == "pg" else "geom"
    query = text(f"SELECT {columns}, {geom} FROM {spec['table']} ORDER BY id")
    async with async_session() as session:
        result = await session.execute(query)
        features = []
        for row in result.mappings():
            properties = {column: str(row[column]) for column in spec["columns"]}
            geometry = _normalize_geometry(json.loads(row["geom"]))
            features.append(_feature(properties, geometry))
    return {"type": "FeatureCollection", "features": features}


def _atomic_export(path: Path, collection: dict[str, Any]) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    data = json.dumps(collection, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    with tmp_path.open("wb") as raw_output:
        with gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=raw_output, mtime=0) as output:
            output.write(data)

    if path.exists():
        shutil.copy2(path, Path(str(path) + ".bak"))
    os.replace(tmp_path, path)
    print(f"Exportado: {path.name} ({path.stat().st_size / 1024:.0f} KB; GeoJSON {len(data) / 1024:.0f} KB)")


async def export_dpa(levels: list[str] | None = None) -> None:
    await run_migrations()
    selected = set(levels or [spec["level"] for spec in DPA_SPECS])
    collections = {}
    for spec in DPA_SPECS:
        if spec["level"] in selected:
            collections[spec["level"]] = await _collection_from_database(spec)

    all_collections = {}
    for spec in DPA_SPECS:
        if spec["level"] in collections:
            all_collections[spec["level"]] = collections[spec["level"]]
        else:
            all_collections[spec["level"]] = await _collection_from_database(spec)
    _validate_collections(all_collections)

    for spec in DPA_SPECS:
        if spec["level"] in selected:
            _atomic_export(EXPORT_DIR / f"{spec['file']}.gz", collections[spec["level"]])


async def load_unidades(file_path: str, clear: bool = False) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    if clear:
        async with engine.begin() as conn:
            await conn.execute(text("DELETE FROM unidades_atencion"))
        print("Tabla limpiada")

    with open(file_path, encoding="utf-8") as source:
        data = json.load(source)
    print(f"Registros encontrados: {len(data)}")

    batch_size = 500
    total_inserted = 0
    skipped = 0
    errors = 0
    for index in range(0, len(data), batch_size):
        batch = data[index : index + batch_size]
        objects = []
        for item in batch:
            if item.get("long") is None or item.get("lat") is None:
                skipped += 1
                continue
            objects.append(
                UnidadAtencion(
                    zon_plan=item.get("zon_plan"),
                    dis_sen=item.get("dis_sen"),
                    uni_des=item.get("uni_des"),
                    dpa_despro=item.get("dpa_despro"),
                    dpa_prov=item.get("dpa_prov"),
                    dpa_descan=item.get("dpa_descan"),
                    dpa_can=item.get("dpa_can"),
                    dpa_despar=item.get("dpa_despar"),
                    dpa_par=item.get("dpa_par"),
                    region=item.get("region"),
                    co_siimdh=item.get("co_siimdh"),
                    nombre=item.get("nombre", ""),
                    servicio=item.get("servicio"),
                    mod=item.get("mod"),
                    mod_abv=item.get("mod_abv"),
                    dir=item.get("dir"),
                    ref=item.get("ref"),
                    ruc=item.get("ruc"),
                    tipo_admin=item.get("tipo_admin"),
                    cooperante=item.get("cooperante"),
                    tipo=item.get("tipo"),
                    hombre=item.get("hombre"),
                    mujer=item.get("mujer"),
                    total=item.get("total"),
                    area=item.get("area"),
                    asis_prom=item.get("asis_prom"),
                    asistencia=item.get("asistencia"),
                    rs18=item.get("rs18"),
                    no_rs18=item.get("no_rs18"),
                    ext_pob18=item.get("ext_pob18"),
                    pob18=item.get("pob18"),
                    no_pob18=item.get("no_pob18"),
                    rs25=item.get("rs25"),
                    no_rs25=item.get("no_rs25"),
                    ext_pob25=item.get("ext_pob25"),
                    pob25=item.get("pob25"),
                    no_pob25=item.get("no_pob25"),
                    x=item.get("x"),
                    y=item.get("y"),
                    longitude=item["long"],
                    latitude=item["lat"],
                    link_ubi=item.get("link_ubi"),
                    corte=item.get("corte"),
                )
            )

        try:
            async with async_session() as session:
                session.add_all(objects)
                await session.commit()
            total_inserted += len(objects)
            print(f"Batch {index // batch_size + 1}: {len(objects)} insertados")
        except Exception as error:
            errors += 1
            print(f"Batch {index // batch_size + 1}: ERROR - {error}")

    print(f"Insertados: {total_inserted}")
    print(f"Sin coordenadas: {skipped}")
    print(f"Errores: {errors}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Migraciones, carga y exportacion de datos geograficos")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("migrate", help="Aplica migraciones pendientes")
    dpa = subparsers.add_parser("dpa", help="Carga la semilla DPA a la base")
    dpa.add_argument("--clear", action="store_true", help="Limpia antes de cargar")

    dpa_export = subparsers.add_parser("dpa-export", help="Exporta DPA desde la base a GeoJSON y gzip")
    dpa_export.add_argument(
        "--level",
        action="append",
        choices=[spec["level"] for spec in DPA_SPECS],
        help="Nivel a exportar; puede repetirse. Por defecto exporta todos",
    )

    unidades = subparsers.add_parser("unidades", help="Carga JSON de unidades de atencion")
    unidades.add_argument("--file", default="data/06_ua_validadas_0626 (1).json")
    unidades.add_argument("--clear", action="store_true")
    return parser


async def main() -> None:
    argv = sys.argv[1:]
    commands = {"migrate", "dpa", "dpa-export", "unidades"}
    show_help = "-h" in argv or "--help" in argv
    if not show_help and not any(arg in commands for arg in argv):
        argv = ["unidades", *argv]
    args = _build_parser().parse_args(argv)
    engine.echo = False

    try:
        if args.command == "migrate":
            await run_migrations()
        elif args.command == "dpa":
            await load_dpa(clear=args.clear)
        elif args.command == "dpa-export":
            await export_dpa(levels=args.level)
        else:
            await load_unidades(args.file, clear=args.clear)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
