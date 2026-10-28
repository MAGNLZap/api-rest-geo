import argparse
import csv
import json
import os
import posixpath
import re
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any
from xml.etree import ElementTree
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent
WORKBOOK = ROOT / "au_amenazadas_data.xlsx"
MAP_HTML = ROOT / "demo" / "ua_amenazas.html"
SEED_DIR = ROOT / "data" / "seed"
TARGET = SEED_DIR / "ua_amenazas_pg.csv"
MONTHS = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}
FIELDS = (
    "fecha_corte",
    "codigo_ua",
    "nombre_ua",
    "servicio",
    "modalidad",
    "modalidad_etiqueta_reporte",
    "zona_planificacion",
    "codigo_distrito",
    "unidad_desconcentrada",
    "region",
    "province_id",
    "canton_id",
    "parish_id",
    "codigo_parroquia_origen",
    "provincia_origen",
    "canton_origen",
    "parroquia_origen",
    "codigo_cabecera_cantonal",
    "nombre_cabecera_cantonal",
    "tipo_atencion",
    "area",
    "tipo_administracion",
    "cooperante",
    "usuarios_hombres",
    "usuarios_mujeres",
    "usuarios_hombres_mapa",
    "usuarios_mujeres_mapa",
    "usuarios_total",
    "direccion",
    "referencia",
    "ruc",
    "asistencia_promedio",
    "asistencia_norma_tecnica",
    "usuarios_con_registro_social_2018",
    "usuarios_sin_registro_social_2018",
    "usuarios_extrema_pobreza_2018",
    "usuarios_pobreza_2018",
    "usuarios_no_pobres_2018",
    "usuarios_con_registro_social_2025",
    "usuarios_sin_registro_social_2025",
    "usuarios_extrema_pobreza_2025",
    "usuarios_pobreza_2025",
    "usuarios_no_pobres_2025",
    "coordenada_x_utm",
    "coordenada_y_utm",
    "geom",
    "nivel_susceptibilidad_inundaciones",
    "nivel_susceptibilidad_movimientos_en_masa",
    "nivel_susceptibilidad_sequias",
    "nivel_susceptibilidad_incendios_forestales",
    "categoria_susceptibilidad_inundaciones",
    "categoria_susceptibilidad_movimientos_en_masa",
    "categoria_susceptibilidad_sequias",
    "categoria_susceptibilidad_incendios_forestales",
    "multiamenaza",
)
MATRIX_FIELDS = {
    "codigo_ua": "co_siimdh",
    "nombre_ua": "nombre",
    "servicio": "servicio",
    "modalidad": "mod",
    "modalidad_etiqueta_reporte": "mod_abv",
    "zona_planificacion": "zon_plan",
    "codigo_distrito": "dis_sen",
    "unidad_desconcentrada": "uni_des",
    "region": "region",
    "codigo_cabecera_cantonal": "cod_cc",
    "nombre_cabecera_cantonal": "cabe_canto",
    "provincia_origen": "dpa_despro",
    "canton_origen": "dpa_descan",
    "parroquia_origen": "dpa_despar",
    "codigo_parroquia_origen": "dpa_par",
    "tipo_atencion": "tipo",
    "area": "area",
    "tipo_administracion": "tipo_admin",
    "cooperante": "cooperante",
    "usuarios_hombres": "hombre",
    "usuarios_mujeres": "mujer",
    "usuarios_total": "total",
    "direccion": "dir",
    "referencia": "ref",
    "ruc": "ruc",
    "asistencia_promedio": "asis_prom",
    "asistencia_norma_tecnica": "asistencia",
    "usuarios_con_registro_social_2018": "rs18",
    "usuarios_sin_registro_social_2018": "no_rs18",
    "usuarios_extrema_pobreza_2018": "ext_pob18",
    "usuarios_pobreza_2018": "pob18",
    "usuarios_no_pobres_2018": "no_pob18",
    "usuarios_con_registro_social_2025": "rs25",
    "usuarios_sin_registro_social_2025": "no_rs25",
    "usuarios_extrema_pobreza_2025": "ext_pob25",
    "usuarios_pobreza_2025": "pob25",
    "usuarios_no_pobres_2025": "no_pob25",
    "coordenada_x_utm": "x",
    "coordenada_y_utm": "y",
    "categoria_susceptibilidad_inundaciones": "susc_inundacion",
    "categoria_susceptibilidad_movimientos_en_masa": "susc_movimientos_masa",
    "categoria_susceptibilidad_sequias": "susc_sequia",
    "categoria_susceptibilidad_incendios_forestales": "susc_inc_forestales",
    "multiamenaza": "multiamenaza",
}
INTEGER_FIELDS = {
    "usuarios_hombres",
    "usuarios_mujeres",
    "usuarios_hombres_mapa",
    "usuarios_mujeres_mapa",
    "usuarios_total",
    "asistencia_norma_tecnica",
    "usuarios_con_registro_social_2018",
    "usuarios_sin_registro_social_2018",
    "usuarios_extrema_pobreza_2018",
    "usuarios_pobreza_2018",
    "usuarios_no_pobres_2018",
    "usuarios_con_registro_social_2025",
    "usuarios_sin_registro_social_2025",
    "usuarios_extrema_pobreza_2025",
    "usuarios_pobreza_2025",
    "usuarios_no_pobres_2025",
    "nivel_susceptibilidad_inundaciones",
    "nivel_susceptibilidad_movimientos_en_masa",
    "nivel_susceptibilidad_sequias",
    "nivel_susceptibilidad_incendios_forestales",
}
NULLABLE_FIELDS = {
    "usuarios_hombres",
    "usuarios_mujeres",
    "direccion",
    "referencia",
    "ruc",
    "asistencia_promedio",
    "asistencia_norma_tecnica",
    "usuarios_con_registro_social_2018",
    "usuarios_sin_registro_social_2018",
    "usuarios_extrema_pobreza_2018",
    "usuarios_pobreza_2018",
    "usuarios_no_pobres_2018",
    "usuarios_con_registro_social_2025",
    "usuarios_sin_registro_social_2025",
    "usuarios_extrema_pobreza_2025",
    "usuarios_pobreza_2025",
    "usuarios_no_pobres_2025",
    "multiamenaza",
}
NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def _column_index(reference: str) -> int:
    letters = re.match(r"[A-Z]+", reference)
    if letters is None:
        raise ValueError(f"Referencia Excel invalida: {reference}")
    result = 0
    for char in letters.group():
        result = result * 26 + ord(char) - ord("A") + 1
    return result - 1


def _read_excel() -> list[dict[str, Any]]:
    with ZipFile(WORKBOOK) as workbook:
        book = ElementTree.fromstring(workbook.read("xl/workbook.xml"))
        relations = ElementTree.fromstring(workbook.read("xl/_rels/workbook.xml.rels"))
        rel_targets = {item.attrib["Id"]: item.attrib["Target"] for item in relations}
        sheets = book.findall(f"{{{NS_MAIN}}}sheets/{{{NS_MAIN}}}sheet")
        if len(sheets) != 1:
            raise ValueError(f"Se esperaba una hoja fuente; encontradas: {len(sheets)}")
        relation_id = sheets[0].attrib[f"{{{NS_REL}}}id"]
        sheet_target = rel_targets[relation_id].lstrip("/")
        if not sheet_target.startswith("xl/"):
            sheet_target = posixpath.normpath(posixpath.join("xl", sheet_target))

        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in workbook.namelist():
            strings_root = ElementTree.fromstring(workbook.read("xl/sharedStrings.xml"))
            shared_strings = [
                "".join(node.text or "" for node in item.iter(f"{{{NS_MAIN}}}t"))
                for item in strings_root.findall(f"{{{NS_MAIN}}}si")
            ]

        worksheet = ElementTree.fromstring(workbook.read(sheet_target))
        raw_rows: list[list[Any]] = []
        for row in worksheet.findall(f"{{{NS_MAIN}}}sheetData/{{{NS_MAIN}}}row"):
            cells: dict[int, Any] = {}
            for cell in row.findall(f"{{{NS_MAIN}}}c"):
                if cell.find(f"{{{NS_MAIN}}}f") is not None:
                    raise ValueError("El Excel contiene formulas; requiere revisión antes de importar")
                kind = cell.attrib.get("t")
                if kind == "inlineStr":
                    value: Any = "".join(node.text or "" for node in cell.iter(f"{{{NS_MAIN}}}t"))
                else:
                    value_node = cell.find(f"{{{NS_MAIN}}}v")
                    value = None if value_node is None else value_node.text
                    if value is not None and kind == "s":
                        value = shared_strings[int(value)]
                    elif value is not None and kind == "b":
                        value = value == "1"
                    elif value is not None and kind not in {"str", "e"}:
                        value = Decimal(value)
                cells[_column_index(cell.attrib["r"])] = value
            if cells:
                raw_rows.append([cells.get(index) for index in range(max(cells) + 1)])

    if not raw_rows:
        raise ValueError("El Excel no contiene filas")
    headers = raw_rows[0]
    if any(not isinstance(value, str) or not value for value in headers):
        raise ValueError("La fila de encabezados Excel tiene celdas vacias o invalidas")
    records = []
    for row_number, values in enumerate(raw_rows[1:], start=2):
        values += [None] * (len(headers) - len(values))
        if len(values) != len(headers):
            raise ValueError(f"Fila Excel {row_number}: cantidad de celdas inesperada")
        if all(value is None for value in values):
            continue
        records.append(dict(zip(headers, values, strict=True)))
    return records


def _read_map_source() -> tuple[dict[str, dict[str, Any]], str]:
    html = MAP_HTML.read_text(encoding="utf-8")
    marker = '<script type="application/json" id="embedded-ua">'
    start = html.index(marker) + len(marker)
    end = html.index("</script>", start)
    source = json.loads(html[start:end], parse_float=Decimal)
    map_fields = (
        "codigo",
        "nombre",
        "serv",
        "mod",
        "prov",
        "can",
        "par",
        "parNombre",
        "ud",
        "tipo",
        "area",
        "adm",
        "usuarios",
        "inund",
        "mm",
        "seq",
        "inc",
        "lat",
        "lon",
        "despro",
        "descan",
        "despar",
        "hombre",
        "mujer",
    )
    category_indices = {"serv": 2, "mod": 3, "ud": 8, "tipo": 9, "area": 10, "adm": 11}
    units: dict[str, dict[str, Any]] = {}
    for row_number, values in enumerate(source["rows"], start=1):
        if len(values) != len(map_fields):
            raise ValueError(f"embedded-ua fila {row_number}: ancho inesperado")
        unit = dict(zip(map_fields, values, strict=True))
        for field, column in category_indices.items():
            index = unit[field]
            categories = source["dict"][field]
            if type(index) is not int or not 0 <= index < len(categories):
                raise ValueError(f"embedded-ua fila {row_number}: indice invalido en {field}")
            unit[field] = categories[index]
        key = f"{unit['codigo']}\0{unit['mod']}"
        if key in units:
            raise ValueError(f"embedded-ua contiene codigo-modalidad repetido: {key!r}")
        units[key] = unit
    return units, source["corte"]


def _cutoff_date(label: str) -> str:
    parts = label.strip().casefold().split()
    if len(parts) != 2 or parts[0] not in MONTHS or not parts[1].isdigit():
        raise ValueError(f"Corte no reconocido: {label!r}")
    return date(int(parts[1]), MONTHS[parts[0]], 1).isoformat()


def _numeric(value: Any, field: str) -> int | Decimal | None:
    if value is None:
        return None
    try:
        number = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError(f"Valor no numerico en {field}: {value!r}") from error
    if not number.is_finite():
        raise ValueError(f"Valor no finito en {field}: {value!r}")
    if field in INTEGER_FIELDS:
        if number != number.to_integral_value():
            raise ValueError(f"Se esperaba entero en {field}: {value!r}")
        return int(number)
    return number


def _row(excel: dict[str, Any], map_unit: dict[str, Any], cutoff: str) -> dict[str, Any]:
    row = {field: excel[source] for field, source in MATRIX_FIELDS.items()}
    row.update(
        {
            "fecha_corte": cutoff,
            "province_id": str(map_unit["prov"]),
            "canton_id": str(map_unit["can"]),
            "parish_id": str(map_unit["par"]),
            "usuarios_hombres": _numeric(excel["hombre"], "usuarios_hombres"),
            "usuarios_mujeres": _numeric(excel["mujer"], "usuarios_mujeres"),
            "usuarios_hombres_mapa": _numeric(map_unit["hombre"], "usuarios_hombres_mapa"),
            "usuarios_mujeres_mapa": _numeric(map_unit["mujer"], "usuarios_mujeres_mapa"),
            "usuarios_total": _numeric(excel["total"], "usuarios_total"),
            "asistencia_promedio": _numeric(excel["asis_prom"], "asistencia_promedio"),
            "asistencia_norma_tecnica": _numeric(excel["asistencia"], "asistencia_norma_tecnica"),
            "coordenada_x_utm": _numeric(excel["x"], "coordenada_x_utm"),
            "coordenada_y_utm": _numeric(excel["y"], "coordenada_y_utm"),
            "geom": f"SRID=4326;POINT({map_unit['lon']} {map_unit['lat']})",
            "nivel_susceptibilidad_inundaciones": _numeric(map_unit["inund"], "nivel_susceptibilidad_inundaciones"),
            "nivel_susceptibilidad_movimientos_en_masa": _numeric(
                map_unit["mm"], "nivel_susceptibilidad_movimientos_en_masa"
            ),
            "nivel_susceptibilidad_sequias": _numeric(map_unit["seq"], "nivel_susceptibilidad_sequias"),
            "nivel_susceptibilidad_incendios_forestales": _numeric(
                map_unit["inc"], "nivel_susceptibilidad_incendios_forestales"
            ),
        }
    )
    for year, fields in {
        "2018": ("rs18", "no_rs18", "ext_pob18", "pob18", "no_pob18"),
        "2025": ("rs25", "no_rs25", "ext_pob25", "pob25", "no_pob25"),
    }.items():
        names = (
            f"usuarios_con_registro_social_{year}",
            f"usuarios_sin_registro_social_{year}",
            f"usuarios_extrema_pobreza_{year}",
            f"usuarios_pobreza_{year}",
            f"usuarios_no_pobres_{year}",
        )
        for name, source in zip(names, fields, strict=True):
            row[name] = _numeric(excel[source], name)
    return row


def _validate_dpa_codes(rows: list[dict[str, Any]]) -> None:
    dpa_files = {
        "province_id": "provincias.json",
        "canton_id": "cantones.json",
        "parish_id": "parroquias.json",
    }
    maps = {
        field: {
            feature["properties"]["id"]: feature["properties"]
            for feature in json.loads((SEED_DIR / filename).read_text(encoding="utf-8"))["features"]
        }
        for field, filename in dpa_files.items()
    }
    for row in rows:
        province = maps["province_id"].get(row["province_id"])
        canton = maps["canton_id"].get(row["canton_id"])
        parish = maps["parish_id"].get(row["parish_id"])
        if province is None or canton is None or parish is None:
            raise ValueError(f"Codigo DPA oficial inexistente para codigo_ua={row['codigo_ua']}")
        if canton["province_id"] != row["province_id"]:
            raise ValueError(f"Provincia/canton inconsistentes para codigo_ua={row['codigo_ua']}")
        if parish["province_id"] != row["province_id"] or parish["canton_id"] != row["canton_id"]:
            raise ValueError(f"Jerarquia parroquial inconsistente para codigo_ua={row['codigo_ua']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepara el CSV plano UA-Amenazas para PostgreSQL")
    parser.add_argument("--force", action="store_true", help="Sobrescribe el CSV existente")
    args = parser.parse_args()
    if TARGET.exists() and not args.force:
        raise SystemExit(f"El archivo ya existe; no se sobrescribe: {TARGET}. Use --force si lo revisó.")

    excel_rows = _read_excel()
    map_units, map_cutoff = _read_map_source()
    excel_by_key: dict[str, dict[str, Any]] = {}
    cutoff_label: str | None = None
    discrepancies = {"usuarios_hombres": 0, "usuarios_mujeres": 0, "codigo_parroquia": 0}

    rows: list[dict[str, Any]] = []
    for row_number, excel in enumerate(excel_rows, start=2):
        key = f"{excel['co_siimdh']}\0{excel['mod']}"
        if key in excel_by_key:
            raise ValueError(f"Excel codigo-modalidad duplicado en fila {row_number}: {key!r}")
        excel_by_key[key] = excel
        map_unit = map_units.get(key)
        if map_unit is None:
            raise ValueError(f"No existe fila correspondiente en embedded-ua: {key!r}")
        if cutoff_label is None:
            cutoff_label = str(excel["corte"])
        if str(excel["corte"]) != cutoff_label or cutoff_label != map_cutoff:
            raise ValueError(f"Corte inconsistente en fila Excel {row_number}")

        shared = (
            ("nombre", "nombre"),
            ("servicio", "serv"),
            ("mod", "mod"),
            ("uni_des", "ud"),
            ("tipo", "tipo"),
            ("area", "area"),
            ("tipo_admin", "adm"),
            ("dpa_prov", "prov"),
            ("dpa_can", "can"),
        )
        for excel_field, map_field in shared:
            if str(excel[excel_field]) != str(map_unit[map_field]):
                raise ValueError(f"Valor no homologado en codigo-modalidad {key!r}: {excel_field}/{map_field}")
        if int(excel["total"]) != int(map_unit["usuarios"]):
            raise ValueError(f"usuarios/total no coincide en codigo-modalidad {key!r}")
        if map_unit["hombre"] == 0 and excel["hombre"] is None:
            discrepancies["usuarios_hombres"] += 1
        if map_unit["mujer"] == 0 and excel["mujer"] is None:
            discrepancies["usuarios_mujeres"] += 1
        if str(excel["dpa_par"]) != str(map_unit["par"]):
            discrepancies["codigo_parroquia"] += 1

        row = _row(excel, map_unit, _cutoff_date(cutoff_label))
        for field in FIELDS:
            if row[field] is None and field not in NULLABLE_FIELDS:
                raise ValueError(f"Campo obligatorio nulo en {key!r}: {field}")
        for field, value, minimum, maximum in (
            ("longitude", map_unit["lon"], -180, 180),
            ("latitude", map_unit["lat"], -90, 90),
        ):
            if value is None or not Decimal(minimum) <= value <= Decimal(maximum):
                raise ValueError(f"Coordenada fuera de rango en {key!r}: {field}={value}")
        rows.append(row)

    if excel_by_key.keys() != map_units.keys():
        raise ValueError("Los bloques del Excel y embedded-ua no contienen las mismas claves codigo-modalidad")
    _validate_dpa_codes(rows)

    tmp_path = TARGET.with_suffix(TARGET.suffix + ".tmp")
    try:
        with tmp_path.open("w", encoding="utf-8", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        os.replace(tmp_path, TARGET)
    finally:
        tmp_path.unlink(missing_ok=True)

    print(f"CSV preparado desde Excel + suplemento cartografico del HTML: {TARGET.relative_to(ROOT)}")
    print(f"Filas: {len(rows)}; claves codigo-modalidad unicas: {len(excel_by_key)}")
    print(f"Corte: {cutoff_label} -> {rows[0]['fecha_corte']} (convencion del primer dia del mes)")
    print(f"Codigos parroquiales del Excel conservados junto al DPA mapa: {discrepancies['codigo_parroquia']}")
    print(
        "Nulos de informe donde mapa expresa cero: "
        f"hombres={discrepancies['usuarios_hombres']}, "
        f"mujeres={discrepancies['usuarios_mujeres']}"
    )
    print("Coordenadas WGS84 originales preservadas en geom EWKT; no se redondean ni reproyectan.")
    print("No se conecto ni se cargo informacion en PostgreSQL.")


if __name__ == "__main__":
    main()
