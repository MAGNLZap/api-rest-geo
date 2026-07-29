import asyncio
import json
import sys
from pathlib import Path

from sqlalchemy import select, text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import async_session, engine
from app.models.base import Base
from app.models.unidad_atencion import UnidadAtencion


async def load_json(file_path: str, clear: bool = False):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    if clear:
        async with engine.begin() as conn:
            await conn.execute(text("DELETE FROM unidades_atencion"))
        print("Tabla limpiada.")

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    print(f"Registros encontrados: {len(data)}")

    batch_size = 500
    total_inserted = 0
    skipped = 0
    errors = 0

    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]
        batch_num = i // batch_size + 1
        objetos = []

        for item in batch:
            if not item.get("long") or not item.get("lat"):
                skipped += 1
                continue

            objetos.append(
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
                session.add_all(objetos)
                await session.commit()
            total_inserted += len(objetos)
            print(f"Batch {batch_num}: {len(objetos)} insertados ({total_inserted}/{len(data)})")
        except Exception as e:
            errors += 1
            print(f"Batch {batch_num}: ERROR - {e}")

    print(f"\nResumen:")
    print(f"  Insertados: {total_inserted}")
    print(f"  Sin coordenadas: {skipped}")
    print(f"  Errores: {errors}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cargar datos JSON a SQLite")
    parser.add_argument("--file", default="data/06_ua_validadas_0626 (1).json", help="Archivo JSON")
    parser.add_argument("--clear", action="store_true", help="Limpiar tabla antes de cargar")
    args = parser.parse_args()

    asyncio.run(load_json(args.file, args.clear))
