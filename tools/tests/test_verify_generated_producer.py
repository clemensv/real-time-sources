import contextlib
import io
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from ci.verify_generated_producer import main


class GeneratedProducerVerificationTests(unittest.TestCase):
    def test_missing_output_fails_even_when_other_output_compiles(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            valid = root / "valid"
            valid.mkdir()
            (valid / "producer.py").write_text("class Producer:\n    pass\n", encoding="utf-8")
            missing = root / "missing"
            for outputs in ([missing], [valid, missing]):
                with self.subTest(outputs=outputs), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(1, main([str(path) for path in outputs]))

    def test_empty_and_build_only_output_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            empty = root / "empty"
            empty.mkdir()
            build_only = root / "build-only"
            (build_only / "build").mkdir(parents=True)
            (build_only / "build" / "producer.py").write_text("class Producer:\n    pass\n", encoding="utf-8")
            for output in (empty, build_only):
                with self.subTest(output=output), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(1, main([str(output)]))

    def test_valid_package_with_empty_initializer_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "__init__.py").write_text("", encoding="utf-8")
            (root / "producer.py").write_text("class Producer:\n    pass\n", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0, main([str(root)]))

    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell is not installed")
    def test_generation_wrapper_rejects_missing_producer_outputs(self):
        helper = pathlib.Path(__file__).resolve().parents[1] / "require-xrcg.ps1"
        with tempfile.TemporaryDirectory() as directory:
            helper_path = str(helper).replace("'", "''")
            source_path = directory.replace("'", "''")
            result = subprocess.run(
                ["pwsh", "-NoProfile", "-NonInteractive", "-Command",
                 f"$ErrorActionPreference = 'Stop'; . '{helper_path}'; "
                 f"Convert-GeneratedPyprojects -SourceDir '{source_path}'"],
                capture_output=True, text=True,
            )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("No generated producer directories", result.stderr)
