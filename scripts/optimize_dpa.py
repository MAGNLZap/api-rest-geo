"""
Optimiza archivos GeoJSON DPA reduciendo precisión de coordenadas a 6 decimales.
Genera archivos nuevos sin modificar los originales.

Uso: python scripts/optimize_dpa.py
"""
import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "app" / "data"

DPA_FILES = {
    "provincias": "provincias.json",
    "cantones": "cantones.json",
    "parroquias": "parroquias.json",
}

TARGET_DECIMALS = 6


def reduce_precision(coords, decimals):
    if isinstance(coords[0], (int, float)):
        return [round(c, decimals) for c in coords]
    return [reduce_precision(c, decimals) for c in coords]


def optimize_geojson(input_path, output_path, decimals):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for feature in data["features"]:
        feature["geometry"]["coordinates"] = reduce_precision(
            feature["geometry"]["coordinates"], decimals
        )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))

    return os.path.getsize(input_path), os.path.getsize(output_path)


if __name__ == "__main__":
    print(f"Optimizando GeoJSON DPA (precisión: {TARGET_DECIMALS} decimales)\n")

    total_before = 0
    total_after = 0

    for name, filename in DPA_FILES.items():
        input_path = DATA_DIR / filename
        output_name = filename.replace(".json", "_6dec.json")
        output_path = DATA_DIR / output_name

        if not input_path.is_file():
            print(f"  {filename}: no encontrado, omitiendo")
            continue

        before, after = optimize_geojson(input_path, output_path, TARGET_DECIMALS)
        reduction = (1 - after / before) * 100
        total_before += before
        total_after += after

        print(
            f"  {filename} -> {output_name}: "
            f"{before / 1024 / 1024:.1f} MB -> {after / 1024 / 1024:.1f} MB (-{reduction:.0f}%)"
        )

    if total_before > 0:
        total_reduction = (1 - total_after / total_before) * 100
        print(
            f"\nTotal: {total_before / 1024 / 1024:.1f} MB -> "
            f"{total_after / 1024 / 1024:.1f} MB (-{total_reduction:.0f}%)"
        )
