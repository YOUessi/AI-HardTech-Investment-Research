"""Reproduce models and build CSV / JSON / HTML reports locally, no external APIs."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from investment_lab.report import generate

if __name__ == "__main__":
    paths = generate(Path(__file__).resolve().parent)
    print("Built", len(paths), "artifacts:")
    for path in paths:
        print(" -", path.relative_to(Path(__file__).resolve().parent))
