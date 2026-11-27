"""Check built production images on an isolated Docker network, without a database."""

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from uuid import uuid4

STUB = """
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"mock": True, "path": self.path}).encode()
        known = ("/health", "/unidades", "/unidades/raw?limit=1",
                 "/dpa/provincias", "/ua_amenazas/data")
        self.send_response(200 if self.path in known else 404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)
HTTPServer(("0.0.0.0", 8001), Handler).serve_forever()
"""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def probe() -> None:
    opener = urllib.request.build_opener(NoRedirect)

    def get(path: str) -> tuple[int, object, bytes]:
        try:
            response = opener.open(f"http://web:8080{path}", timeout=10)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            return response.status, response.headers, response.read()

    for path in ("/", "/servicios_sociales", "/unidades_infancia", "/ua_amenazas"):
        status, headers, body = get(path)
        assert status == 200, (path, status)
        assert "text/html" in headers["Content-Type"], path
        assert b'id="app"' in body, path
        assert headers.get("X-Content-Type-Options") == "nosniff", path
        assert headers.get("Referrer-Policy") == "strict-origin-when-cross-origin", path
        assets = re.findall(rb'(?:src|href)="(/assets/[^"]+)"', body)
        assert assets, (path, "No hay recursos compilados con la base esperada")
        for asset in assets:
            asset_status, asset_headers, _ = get(asset.decode())
            assert asset_status == 200, asset
            assert "immutable" in asset_headers["Cache-Control"], asset
            assert asset_headers.get("X-Content-Type-Options") == "nosniff", asset
        print(f"OK Vue + assets: {path}", flush=True)
    redirects = ("/servicios_sociales/", "/unidades_infancia/", "/ua_amenazas/")
    for path in redirects:
        status, headers, _ = get(path)
        assert status == 302, (path, status)
        assert headers["Location"].startswith("/"), headers["Location"]
        assert "://" not in headers["Location"], headers["Location"]
        print(f"OK redirect relativo: {path}", flush=True)
    status, _, body = get("/health")
    assert status == 200 and json.loads(body) == {"mock": True, "path": "/health"}
    for path in ("/unidades", "/unidades/raw?limit=1", "/dpa/provincias", "/ua_amenazas/data"):
        status, headers, body = get(path)
        assert status == 200 and "application/json" in headers["Content-Type"], path
        assert json.loads(body)["path"] == path, body
        print(f"OK API conserva ruta y query: {path}", flush=True)
    for path in ("/unidades/999999999", "/dpa/inexistente", "/ruta-api-inexistente"):
        status, headers, body = get(path)
        assert status == 404 and "application/json" in headers["Content-Type"], path
        assert json.loads(body)["path"] == path, body
        print(f"OK API JSON sin fallback HTML: {path}", flush=True)
    assert get("/web-health")[0] == 200
    assert get("/assets/no-existe.js")[0] == 404


def run_docker(*args: str) -> None:
    subprocess.run(["docker", *args], check=True)


def check_images(api_image: str, web_image: str) -> None:
    name = f"geoportal-check-{uuid4().hex[:10]}"
    api, web = f"{name}-api", f"{name}-web"
    run_docker("network", "create", "--internal", name)
    try:
        run_docker("run", "-d", "--name", api, "--network", name,
                   "--network-alias", "api", "--entrypoint", "python", api_image, "-c", STUB)
        run_docker("run", "--rm", "--network", name, web_image, "nginx", "-t")
        run_docker("run", "-d", "--name", web, "--network", name,
                   "--network-alias", "web", web_image)
        run_docker("run", "--rm", "--network", name, "--mount",
                   f"type=bind,source={Path(__file__).resolve()},target=/probe.py,readonly",
                   "--entrypoint", "python", api_image, "/probe.py", "--probe")
    finally:
        subprocess.run(["docker", "rm", "-f", web, api], check=False)
        subprocess.run(["docker", "network", "rm", name], check=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api-image", default="geoportal-api:check")
    parser.add_argument("--web-image", default="geoportal-web:check")
    parser.add_argument("--probe", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.probe:
        probe()
    else:
        check_images(args.api_image, args.web_image)
        print("Validación aislada correcta. No se ha conectado a PostgreSQL ni al servidor público.")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, OSError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
