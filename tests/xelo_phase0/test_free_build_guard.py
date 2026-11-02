"""Unit tests for the fail-closed CMake license-boundary build guard."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from xelo_verify_free_build import check_cache, check_compile_commands


class FreeBuildGuardTests(unittest.TestCase):
    def test_explicitly_disabled_is_accepted(self):
        check_cache("ZT_NONFREE:BOOL=OFF\nZT1_CENTRAL_CONTROLLER:BOOL=OFF\n")

    def test_missing_setting_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "ZT_NONFREE"):
            check_cache("ZT1_CENTRAL_CONTROLLER:BOOL=OFF")

    def test_nonfree_controller_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "ZT_NONFREE"):
            check_cache("ZT_NONFREE:BOOL=ON\nZT1_CENTRAL_CONTROLLER:BOOL=OFF")

    def test_central_controller_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "ZT1_CENTRAL_CONTROLLER"):
            check_cache("ZT_NONFREE:BOOL=OFF\nZT1_CENTRAL_CONTROLLER:BOOL=ON")

    def test_only_mpl_sources_are_accepted(self):
        check_compile_commands('[{"file":"/repo/service/OneService.cpp"}, {"file":"/repo/node/Node.cpp"}]')

    def test_nonfree_compiled_source_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Nonfree source"):
            check_compile_commands('[{"file":"/repo/nonfree/controller/EmbeddedNetworkController.cpp"}]')

    def test_empty_source_list_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "empty"):
            check_compile_commands("[]")


if __name__ == "__main__":
    unittest.main()
