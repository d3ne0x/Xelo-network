"""Protect Phase 0 presets against accidental nonfree controller builds."""
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class FreePresetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "CMakePresets.json").read_text(encoding="utf-8"))
        cls.configure_presets = {p["name"]: p for p in cls.data["configurePresets"]}
        cls.build_presets = {p["name"]: p for p in cls.data["buildPresets"]}

    def test_linux_free_preset_excludes_nonfree(self):
        p = self.configure_presets["linux-free-release"]
        self.assertEqual(p["cacheVariables"]["ZT_NONFREE"], "OFF")

    def test_windows_free_preset_excludes_nonfree(self):
        p = self.configure_presets["windows-x64-free"]
        self.assertEqual(p["cacheVariables"]["ZT_NONFREE"], "OFF")

    def test_windows_release_uses_free_preset(self):
        self.assertEqual(
            self.build_presets["windows-x64-free-release"]["configurePreset"],
            "windows-x64-free",
        )

    def test_linux_release_uses_free_preset(self):
        self.assertEqual(
            self.build_presets["linux-free-release"]["configurePreset"],
            "linux-free-release",
        )


if __name__ == "__main__":
    unittest.main()
