"""
Optimiza archivos GeoJSON DPA:
1. Reduce precisión de coordenadas a 6 decimales
2. Genera archivos pre-comprimidos .gz

Uso: python scripts/optimize_dpa.py
"""
import gzip
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

    json_bytes = json.dumps(data, separators=(",", ":")).encode("utf-8")
    with open(output_path, "wb") as f:
        f.write(json_bytes)

    gz_path = str(output_path) + ".gz"
    with gzip.open(gz_path, "wb", compresslevel=9) as f:
        f.write(json_bytes)

    return os.path.getsize(input_path), os.path.getsize(output_path), os.path.getsize(gz_path)


if __name__ == "__main__":
    print(f"Optimizando GeoJSON DPA (precisión: {TARGET_DECIMALS} decimales)\n")

    total_before = 0
    total_after = 0
    total_gz = 0

    for name, filename in DPA_FILES.items():
        input_path = DATA_DIR / filename
        output_name = filename.replace(".json", "_6dec.json")
        output_path = DATA_DIR / output_name

        if not input_path.is_file():
            print(f"  {filename}: no encontrado, omitiendo")
            continue

        before, after, gz_size = optimize_geojson(input_path, output_path, TARGET_DECIMALS)
        reduction = (1 - after / before) * 100
        gz_reduction = (1 - gz_size / before) * 100
        total_before += before
        total_after += after
        total_gz += gz_size

        print(
            f"  {filename}: {before / 1024 / 1024:.1f} MB -> "
            f"{after / 1024 / 1024:.1f} MB (-{reduction:.0f}%) "
            f"gz:{gz_size / 1024:.0f}KB (-{gz_reduction:.0f}%)"
        )

    if total_before > 0:
        total_reduction = (1 - total_after / total_before) * 100
        gz_reduction = (1 - total_gz / total_before) * 100
        print(
            f"\nTotal: {total_before / 1024 / 1024:.1f} MB -> "
            f"{total_after / 1024 / 1024:.1f} MB (-{total_reduction:.0f}%) "
            f"gz:{total_gz / 1024:.0f}KB (-{gz_reduction:.0f}%)"
        )
