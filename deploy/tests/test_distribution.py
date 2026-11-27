import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class DistributionTests(unittest.TestCase):
    def test_production_identity_and_root_routes(self) -> None:
        compose = (ROOT / "compose.yaml").read_text(encoding="utf-8")
        self.assertIn("name: geoportal-mtdh", compose)
        for name in ("geoportal-api", "geoportal-web"):
            self.assertIn(f"container_name: {name}", compose)
            self.assertIn(f"image: {name}:", compose)
        self.assertIn('ROOT_PATH: ""', compose)
        self.assertIn("PUBLIC_BASE: /", compose)
        self.assertNotIn("/api-geo", compose)

    def test_only_one_production_configuration(self) -> None:
        for name in (
            "deploy/compose.root.yaml", "deploy/nginx/root.conf.template",
            "deploy/INSTALL-ROOT-APACHE.md", "deploy/.env.root.production.example",
            "scripts/package_release.py",
        ):
            self.assertFalse((ROOT / name).exists(), name)

    def test_environment_examples_and_safety(self) -> None:
        example = (ROOT / "deploy/.env.production.example").read_text(encoding="utf-8")
        self.assertIn("WEB_PORT=18081", example)
        self.assertNotIn("release-001", example)
        nginx = (ROOT / "deploy/nginx/default.conf.template").read_text(encoding="utf-8")
        self.assertIn("location = /servicios_sociales", nginx)
        self.assertIn("location / {", nginx)
        self.assertNotIn("PUBLIC_PATH", nginx)
        self.assertNotIn("try_files $uri /index.html", nginx)

    def test_private_files_are_ignored(self) -> None:
        paths = (
            ".env", "frontend/.env.staging", "deploy/.env.production",
            "credentials.pem", "client.pfx", "data/private.csv",
            "au_amenazadas_data.xlsx", "docs/backups/example.txt",
            "docs/superpowers/plans/private.md", "releases/source.tar.gz",
        )
        for name in paths:
            result = subprocess.run(
                ["git", "check-ignore", "--no-index", "-q", name], cwd=ROOT, check=False
            )
            self.assertEqual(result.returncode, 0, name)
        for name in (".env.example", "deploy/.env.production.example", "frontend/.env.example"):
            result = subprocess.run(
                ["git", "check-ignore", "--no-index", "-q", name], cwd=ROOT, check=False
            )
            self.assertEqual(result.returncode, 1, name)

    def test_operational_data_not_in_public_index(self) -> None:
        tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
        for name in tracked:
            self.assertFalse(name.endswith((".xlsx", ".csv", ".pem", ".pfx", ".db")), name)
            self.assertFalse(name.startswith(("docs/backups/", "docs/superpowers/")), name)


if __name__ == "__main__":
    unittest.main()
