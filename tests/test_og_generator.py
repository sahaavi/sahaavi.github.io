from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import generate_og_image


class OgImageGeneratorTests(unittest.TestCase):
    def test_missing_required_fonts_fail_with_actionable_error(self) -> None:
        for bold, filename in (
            (False, "DejaVuSans.ttf"),
            (True, "DejaVuSans-Bold.ttf"),
        ):
            with self.subTest(filename=filename):
                with patch.object(Path, "is_file", return_value=False):
                    with self.assertRaisesRegex(
                        RuntimeError,
                        rf"{filename}.*fonts-dejavu-core",
                    ):
                        generate_og_image.font(20, bold=bold)
