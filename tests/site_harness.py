from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HugoSiteTestCase(unittest.TestCase):
    """Render the production Hugo site once per test class into a temp directory."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._temporary_directory = tempfile.TemporaryDirectory(prefix="portfolio-site-")
        cls.addClassCleanup(cls._temporary_directory.cleanup)
        cls.output_dir = Path(cls._temporary_directory.name)
        command = [
            "hugo",
            "--gc",
            "--minify",
            "--cleanDestinationDir",
            "--destination",
            str(cls.output_dir),
        ]
        result = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise AssertionError(
                "Hugo build failed.\nSTDOUT:\n"
                + result.stdout
                + "\nSTDERR:\n"
                + result.stderr
            )

    def page_path(self, route: str) -> Path:
        normalized = route.strip("/")
        if not normalized:
            return self.output_dir / "index.html"
        return self.output_dir / normalized / "index.html"

    def page_html(self, route: str) -> str:
        path = self.page_path(route)
        self.assertTrue(path.is_file(), f"Expected generated page: {path}")
        return path.read_text(encoding="utf-8")
