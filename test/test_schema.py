import pathlib, subprocess, sys

root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "scripts"))
import check


def test_schema_parses_and_is_valid():
    assert check.load()["paths"]


def test_notes_are_current():
    subprocess.run([sys.executable, str(root / "scripts" / "check.py"), "--check"], check=True)
