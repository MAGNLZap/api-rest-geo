"""Captura documental agregada. Ejecutar solo con autorización de lectura de BD."""

import asyncio
import json
import sys
from pathlib import Path

from dotenv import dotenv_values
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "docs/conocimiento-unidades/fuentes/inventario-servicio-modalidad.md"
QUERY = """SELECT servicio, mod, mod_abv, count(*) AS unidades
FROM unidades_atencion
GROUP BY servicio, mod, mod_abv
ORDER BY servicio NULLS FIRST, mod NULLS FIRST, mod_abv NULLS FIRST"""


def label(value: str | None) -> str:
    if value is None:
        return "(NULL)"
    if value == "":
        return "(cadena vacía)"
    return json.dumps(value, ensure_ascii=False).replace("|", "\\|")


async def main() -> None:
    database_url = dotenv_values(ROOT / ".env").get("DATABASE_URL") or ""
    if not database_url.startswith("postgresql+asyncpg://"):
        raise ValueError("La conexión de .env no utiliza PostgreSQL/asyncpg.")
    engine = create_async_engine(
        database_url,
        echo=False,
        isolation_level="REPEATABLE READ",
        connect_args={
            "timeout": 15,
            "server_settings": {
                "default_transaction_read_only": "on",
                "statement_timeout": "15000",
                "lock_timeout": "3000",
                "application_name": "ApiRestGeo-documentacion-inventario",
            },
        },
    )
    try:
        async with engine.connect() as connection, connection.begin():
            check = (
                await connection.execute(
                    text("SELECT current_setting('transaction_read_only') AS read_only, "
                         "transaction_timestamp() AS captured_at")
                )
            ).mappings().one()
            if check["read_only"] != "on":
                raise RuntimeError("No se confirmó una transacción de solo lectura.")
            result = await connection.execute(text(QUERY))
            rows = [
                {"servicio": row["servicio"], "mod": row["mod"], "mod_abv": row["mod_abv"],
                 "unidades": int(row["unidades"])}
                for row in result.mappings()
            ]
            captured_at = check["captured_at"].isoformat()
    finally:
        await engine.dispose()

    def present(value: str | None) -> bool:
        return value is not None and bool(value.strip())

    inventory = {
        "format": "ua-service-modality-inventory",
        "version": 1,
        "capturedAt": captured_at,
        "transactionReadOnly": True,
        "source": {"table": "unidades_atencion", "query": QUERY},
        "totals": {
            "units": sum(row["unidades"] for row in rows),
            "combinations": len(rows),
            "services": len({row["servicio"] for row in rows if present(row["servicio"])}),
            "modalities": len({row["mod"] for row in rows if present(row["mod"])}),
            "abbreviations": len({row["mod_abv"] for row in rows if present(row["mod_abv"])}),
        },
        "quality": {
            field: sum(row["unidades"] for row in rows if not present(row[field]))
            for field in ("servicio", "mod", "mod_abv")
        },
        "rows": rows,
    }
    lines = [
        "# Captura agregada: servicio, modalidad y abreviatura", "",
        f"Instante de la transacción: `{captured_at}`.", "",
        "Fuente: `unidades_atencion` de la conexión PostgreSQL configurada en el `.env` existente.",
        "No se publican servidor, base, credenciales, nombres de unidades ni datos de personas.", "",
        "**Transacción confirmada de solo lectura y snapshot REPEATABLE READ.**",
        "Solo se consultaron metadatos de la transacción y la agrupación siguiente.",
        "No se ejecutaron migraciones, cargas o modificaciones.", "",
        "```sql", QUERY, "```", "",
        "Las relaciones son combinaciones observadas, no una taxonomía oficial ni reglas de acceso.",
        "Se preservan los textos exactos, mayúsculas y espacios; NULL y cadena vacía son distintos.",
        "`unidades` cuenta filas de la tabla, no cupos ni códigos institucionales distintos.", "",
        "| Servicio exacto | Modalidad exacta | Abreviatura exacta | Filas de unidades |",
        "|---|---|---|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {label(row['servicio'])} | {label(row['mod'])} | "
            f"{label(row['mod_abv'])} | {row['unidades']} |"
        )
    lines.extend(["", "## Captura estructurada", "", "```json",
                  json.dumps(inventory, ensure_ascii=False, indent=2), "```", ""])
    OUTPUT.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(json.dumps({"capturedAt": captured_at, "totals": inventory["totals"],
                      "missingFieldRows": inventory["quality"]}, ensure_ascii=False, indent=2))
    print(f"Captura escrita: {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print(f"No se completó la captura ({type(error).__name__}). No se muestran datos de conexión.", file=sys.stderr)
        sys.exit(1)
