"""Argparse should work without optional inference packages or model weights."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "data" / "check_images.py"


class CliStartupTests(unittest.TestCase):
    def run_cli(self, *arguments):
        with tempfile.TemporaryDirectory() as directory:
            # -E ignores injected Python paths; -S excludes site-packages.
            # Use another cwd so the command cannot depend on local image data.
            return subprocess.run(
                [sys.executable, "-E", "-S", str(SCRIPT), *arguments],
                cwd=directory, text=True, capture_output=True, check=False,
            )

    def test_help_works_without_inference_dependencies(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        for option in ("--dir", "--arch", "--dogfile"):
            self.assertIn(option, result.stdout)
        self.assertEqual(result.stderr, "")

    def test_unknown_argument_gets_argparse_error_before_model_import(self):
        result = self.run_cli("--unknown-option")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unrecognized arguments", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_missing_option_value_gets_argparse_error(self):
        result = self.run_cli("--arch")
        self.assertEqual(result.returncode, 2)
        self.assertIn("expected one argument", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
