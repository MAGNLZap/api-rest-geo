import asyncio
import json
import math
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Any

from shapely.geometry import MultiPolygon, Polygon, shape
from shapely.ops import unary_union
from sqlalchemy import text

from app.database import engine

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "app" / "static" / "portal"
WIDTH = 560
HEIGHT = 210
MAIN_FRAME = (145.0, 8.0, 355.0, 202.0)
ISLAND_FRAME = (25.0, 22.0, 104.0, 76.0)
HERO_MAIN_FRAME = (118.0, 14.0, 390.0, 376.0)
HERO_ISLAND_FRAME = (18.0, 245.0, 82.0, 292.0)
UNIT_COLOR = "#147c83"
RISK_COLORS = ("#cbd3df", "#edbd49", "#bd5949")
BOUNDARY = "#bac3d2"


def _polygons(geometry: Any) -> list[Polygon]:
    if isinstance(geometry, Polygon):
        return [geometry]
    if isinstance(geometry, MultiPolygon):
        return list(geometry.geoms)
    return []


def _bounds(polygons: list[Polygon]) -> tuple[float, float, float, float]:
    min_x = min(polygon.bounds[0] for polygon in polygons)
    min_y = min(polygon.bounds[1] for polygon in polygons)
    max_x = max(polygon.bounds[2] for polygon in polygons)
    max_y = max(polygon.bounds[3] for polygon in polygons)
    return min_x, min_y, max_x, max_y


def _projector(
    bounds: tuple[float, float, float, float],
    frame: tuple[float, float, float, float],
):
    min_x, min_y, max_x, max_y = bounds
    left, top, right, bottom = frame
    scale = min((right - left) / (max_x - min_x), (bottom - top) / (max_y - min_y))
    drawn_width = (max_x - min_x) * scale
    drawn_height = (max_y - min_y) * scale
    x_offset = left + ((right - left) - drawn_width) / 2
    y_offset = top + ((bottom - top) - drawn_height) / 2

    def project(longitude: float, latitude: float) -> tuple[float, float]:
        return (
            x_offset + (longitude - min_x) * scale,
            y_offset + (max_y - latitude) * scale,
        )

    return project


def _polygon_path(polygon: Polygon, project) -> str:
    points = [project(x, y) for x, y in polygon.simplify(0.018, preserve_topology=True).exterior.coords]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in points) + " Z"


def _topographic_paths() -> list[str]:
    root = ET.parse(ROOT / "demo" / "patron-topografico.svg").getroot()
    line_group = next(element for element in root.iter() if element.get("id") == "lineas")
    return [element.get("d", "") for element in line_group if element.tag.endswith("path")]


def _group_unit_points(
    points: list[tuple[float, float, str]], main_project, island_project, columns: int, rows: int, limit: int
) -> list[tuple[float, float, int, str]]:
    cells: dict[tuple[str, int, int], list[float]] = defaultdict(lambda: [0.0, 0.0, 0.0])
    for longitude, latitude, category in points:
        is_island = longitude < -85
        project = island_project if is_island else main_project
        x, y = project(longitude, latitude)
        if is_island:
            key = (category, -1, 0)
        else:
            left, top, right, bottom = MAIN_FRAME
            column = min(columns - 1, max(0, int((x - left) / (right - left) * columns)))
            row = min(rows - 1, max(0, int((y - top) / (bottom - top) * rows)))
            key = (category, column, row)
        cell = cells[key]
        cell[0] += x
        cell[1] += y
        cell[2] += 1
    grouped: dict[str, list[tuple[float, float, int, str]]] = defaultdict(list)
    offsets = {"DCI": -2.2, "CNH": 2.2}
    for (category, _, _), (sum_x, sum_y, count) in cells.items():
        grouped[category].append((sum_x / count + offsets[category], sum_y / count, int(count), category))
    return [
        point
        for category in ("DCI", "CNH")
        for point in sorted(grouped[category], key=lambda item: (-item[2], item[1], item[0]))[:limit]
    ]


def _append_unit_links(svg: list[str], markers: list[tuple[float, float, int, str]]) -> None:
    colors = {"DCI": "#147c83", "CNH": "#b38c21"}
    for category in ("DCI", "CNH"):
        points = [(x, y) for x, y, _, marker_category in markers if marker_category == category]
        links: set[tuple[int, int]] = set()
        for index, (x, y) in enumerate(points):
            neighbors = sorted(
                (
                    (math.hypot(other_x - x, other_y - y), other_index)
                    for other_index, (other_x, other_y) in enumerate(points)
                    if other_index != index
                )
            )
            if neighbors and neighbors[0][0] <= 76:
                links.add(tuple(sorted((index, neighbors[0][1]))))
        for start, end in sorted(links):
            x1, y1 = points[start]
            x2, y2 = points[end]
            bend_x = (x1 + x2) / 2
            svg.append(
                f'<path d="M{x1:.1f},{y1:.1f} L{bend_x:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}" '
                f'fill="none" stroke="{colors[category]}" stroke-opacity=".42" '
                'stroke-width="1" stroke-linecap="square" stroke-linejoin="miter"/>'
            )


def _svg_base(
    provinces: list[tuple[str, list[Polygon]]],
    main_project,
    island_project,
    fill_for_province,
) -> list[str]:
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img">',
        '<rect width="560" height="210" fill="#ffffff" fill-opacity=".84"/>',
    ]
    for province_id, parts in provinces:
        project = island_project if province_id == "20" else main_project
        fill = fill_for_province(province_id)
        for polygon in parts:
            svg.append(
                f'<path d="{_polygon_path(polygon, project)}" fill="{fill}" '
                f'stroke="{BOUNDARY}" stroke-width=".85" stroke-linejoin="round"/>'
            )
    return svg


def _append_card_outlines(
    svg: list[str], provinces: list[tuple[str, list[Polygon]]], main_project, island_project
) -> None:
    mainland = [polygon for province_id, parts in provinces if province_id != "20" for polygon in parts]
    islands = [polygon for province_id, parts in provinces if province_id == "20" for polygon in parts]
    for polygon in _polygons(unary_union(mainland)):
        svg.append(
            f'<path d="{_polygon_path(polygon, main_project)}" fill="none" '
            'stroke="#29265f" stroke-width="1.45" stroke-linejoin="round"/>'
        )
    for polygon in _polygons(unary_union(islands)):
        svg.append(
            f'<path d="{_polygon_path(polygon, island_project)}" fill="none" '
            'stroke="#29265f" stroke-width="1.1" stroke-linejoin="round"/>'
        )


def _hero_svg(
    provinces: list[tuple[str, list[Polygon]]], main_project, island_project, topographic_paths: list[str]
) -> str:
    mainland = [parts for province_id, parts in provinces if province_id != "20"]
    islands = [parts for province_id, parts in provinces if province_id == "20"]
    mainland_outline = _polygons(unary_union([polygon for parts in mainland for polygon in parts]))
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 390" role="img" aria-labelledby="title desc">',
        '<title id="title">Mapa topográfico de Ecuador</title>',
        '<desc id="desc">Silueta del Ecuador con límites provinciales y curvas topográficas '
        'decorativas.</desc>',
        "<defs>",
        '<linearGradient id="terrain" x1="0" y1="1" x2="1" y2="0">',
        '<stop offset="0" stop-color="#147c83"/>',
        '<stop offset=".38" stop-color="#168b91"/>',
        '<stop offset=".76" stop-color="#343978"/>',
        '<stop offset="1" stop-color="#29265f"/>',
        "</linearGradient>",
        '<radialGradient id="aura">',
        '<stop stop-color="#147c83" stop-opacity=".58"/>',
        '<stop offset="1" stop-color="#147c83" stop-opacity="0"/>',
        "</radialGradient>",
        '<pattern id="wallpaper" patternUnits="userSpaceOnUse" width="416" height="240">',
        '<g transform="scale(.65)" fill="#fff" fill-rule="evenodd">',
    ]
    svg.extend(f'<path d="{path}"/>' for path in topographic_paths)
    svg.extend(
        [
            "</g>",
            "</pattern>",
        '<clipPath id="mainland">',
        ]
    )
    for parts in mainland:
        for polygon in parts:
            svg.append(f'<path d="{_polygon_path(polygon, main_project)}"/>')
    svg.extend(
        [
            "</clipPath>",
            "</defs>",
            '<ellipse cx="254" cy="190" rx="170" ry="205" fill="url(#aura)"/>',
            '<g fill="url(#terrain)" stroke="#d8dcf4" stroke-opacity=".48" '
            'stroke-width="1.05" stroke-linejoin="round">',
        ]
    )
    for parts in mainland:
        for polygon in parts:
            svg.append(f'<path d="{_polygon_path(polygon, main_project)}"/>')
    svg.extend(
        [
            "</g>",
            '<g clip-path="url(#mainland)" opacity=".18">',
            '<rect width="420" height="390" fill="url(#wallpaper)"/>',
            "</g>",
            '<g fill="none" stroke="#f5c842" stroke-opacity=".82" stroke-width="1.6" '
            'stroke-linejoin="round">',
        ]
    )
    for polygon in mainland_outline:
        svg.append(f'<path d="{_polygon_path(polygon, main_project)}"/>')
    svg.extend(
        [
            "</g>",
            '<g fill="url(#terrain)" stroke="#d8dcf4" stroke-opacity=".55" '
            'stroke-width=".8" stroke-linejoin="round">',
        ]
    )
    for parts in islands:
        for polygon in parts:
            svg.append(f'<path d="{_polygon_path(polygon, island_project)}"/>')
    svg.extend(
        [
            "</g>",
            '<path d="M79 268 C101 263 111 251 126 237" fill="none" stroke="#f5c842" '
            'stroke-opacity=".55" stroke-width="1.2" stroke-dasharray="2 5"/>',
            "</svg>",
        ]
    )
    return "\n".join(svg)


async def _read_map_data() -> tuple[list[dict[str, Any]], list[tuple[float, float, str]]]:
    async with engine.connect() as connection:
        province_result = await connection.execute(
            text("SELECT id, ST_AsGeoJSON(geom) AS geometry FROM provinces ORDER BY id")
        )
        province_features = [
            {"id": row["id"], "geometry": json.loads(row["geometry"])} for row in province_result.mappings()
        ]
        units_result = await connection.execute(
            text(
                "SELECT longitude, latitude, mod_abv FROM unidades_atencion "
                "WHERE longitude IS NOT NULL AND latitude IS NOT NULL "
                "AND (mod_abv ILIKE '%CNH%' OR mod_abv ILIKE '%CDI%' OR mod_abv ILIKE '%DCI%')"
            )
        )
        unit_points = [
            (float(row[0]), float(row[1]), "CNH" if "CNH" in row[2].upper() else "DCI")
            for row in units_result
        ]
    return province_features, unit_points


async def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    features, unit_points = await _read_map_data()
    provinces = [(str(feature["id"]), _polygons(shape(feature["geometry"]))) for feature in features]
    mainland = [polygon for province_id, polygons in provinces if province_id != "20" for polygon in polygons]
    islands = [polygon for province_id, polygons in provinces if province_id == "20" for polygon in polygons]
    if not mainland or not islands:
        raise ValueError("No se encontraron geometrías continentales y de Galápagos en provincias")

    main_project = _projector(_bounds(mainland), MAIN_FRAME)
    island_project = _projector(_bounds(islands), ISLAND_FRAME)
    hero_main_project = _projector(_bounds(mainland), HERO_MAIN_FRAME)
    hero_island_project = _projector(_bounds(islands), HERO_ISLAND_FRAME)
    topographic_paths = _topographic_paths()

    units_svg = _svg_base(provinces, main_project, island_project, lambda _: "#f7fafb")
    _append_card_outlines(units_svg, provinces, main_project, island_project)
    unit_markers = _group_unit_points(unit_points, main_project, island_project, 4, 4, 6)
    _append_unit_links(units_svg, unit_markers)
    for x, y, count, category in unit_markers:
        size = min(5.8, 3.7 + math.log2(count + 1) * 0.32)
        if category == "DCI":
            path = f"M{x:.1f},{y - size:.1f} L{x + size:.1f},{y:.1f} L{x:.1f},{y + size:.1f} L{x - size:.1f},{y:.1f} Z"
            fill = UNIT_COLOR
            stroke = "#fff"
        else:
            path = (
                f"M{x - size:.1f},{y - size:.1f} L{x + size:.1f},{y - size:.1f} "
                f"L{x + size:.1f},{y + size:.1f} L{x - size:.1f},{y + size:.1f} Z"
            )
            fill = "#f5c842"
            stroke = "#29265f"
        units_svg.append(
            f'<path d="{path}" fill="{fill}" fill-opacity=".96" stroke="{stroke}" stroke-width="1.1"/>'
        )
    units_svg.extend(
        [
            '<path d="M392 69 L397 74 L392 79 L387 74 Z" fill="#147c83" stroke="#fff" stroke-width="1"/>',
            '<text x="405" y="78" fill="#485267" font-family="Arial,sans-serif" '
            'font-size="11" font-weight="600">DCI</text>',
            '<path d="M388 91 H396 V99 H388 Z" fill="#f5c842" stroke="#29265f" stroke-width=".9"/>',
            '<text x="405" y="99" fill="#485267" font-family="Arial,sans-serif" '
            'font-size="11" font-weight="600">CNH</text>',
            "</svg>",
        ]
    )

    exposure_counts: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    async with engine.connect() as connection:
        result = await connection.execute(
            text(
                "SELECT province_id, count(*), "
                "count(*) FILTER (WHERE nivel_susceptibilidad_inundaciones > 0) "
                "FROM ua_amenazas GROUP BY province_id"
            )
        )
        for province_id, total, exposed in result:
            exposure_counts[str(province_id)] = [int(total), int(exposed)]

    rates = sorted(exposed / total for total, exposed in exposure_counts.values() if total)
    thresholds = [rates[len(rates) // 3], rates[(2 * len(rates)) // 3]] if rates else [0, 0]
    threat_fills = ("#e8eef2", "#a8c0cf", "#5e88a5")

    def fill_threat(province_id: str) -> str:
        total, exposed = exposure_counts.get(province_id, (0, 0))
        if total == 0 or exposed == 0:
            return "#f7fafb"
        rate = exposed / total
        return (
            threat_fills[0] if rate <= thresholds[0] else threat_fills[1] if rate <= thresholds[1] else threat_fills[2]
        )

    threat_svg = _svg_base(provinces, main_project, island_project, fill_threat)
    _append_card_outlines(threat_svg, provinces, main_project, island_project)
    threat_svg.extend(
        [
            '<text x="386" y="57" fill="#29265f" font-family="Arial,sans-serif" '
            'font-size="10" font-weight="600">Capas de amenaza</text>',
            '<path d="M386 68 H394 V76 H386 Z" fill="#2f6690"/>',
            '<text x="402" y="76" fill="#485267" font-family="Arial,sans-serif" font-size="9.5">Inundaciones</text>',
            '<path d="M386 91 H394 V99 H386 Z" fill="#e8740c"/>',
            '<text x="402" y="99" fill="#485267" font-family="Arial,sans-serif" '
            'font-size="9.5">Movimientos en masa</text>',
            '<path d="M386 114 H394 V122 H386 Z" fill="#9c6b1c"/>',
            '<text x="402" y="122" fill="#485267" font-family="Arial,sans-serif" font-size="9.5">Sequía</text>',
            '<path d="M386 137 H394 V145 H386 Z" fill="#b3261e"/>',
            '<text x="402" y="145" fill="#485267" font-family="Arial,sans-serif" '
            'font-size="9.5">Incendios forestales</text>',
            "</svg>",
        ]
    )

    (OUTPUT_DIR / "preview_unidades.svg").write_text("\n".join(units_svg), encoding="utf-8")
    (OUTPUT_DIR / "preview_amenazas.svg").write_text("\n".join(threat_svg), encoding="utf-8")
    (OUTPUT_DIR / "ecuador_hero.svg").write_text(
        _hero_svg(provinces, hero_main_project, hero_island_project, topographic_paths), encoding="utf-8"
    )
    print(f"Previews generados: {len(unit_markers)} grupos DCI/CNH y cuatro capas de amenazas.")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
