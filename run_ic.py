"""Build point-in-time publicly-traded equity IC packet; no networking required."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/"src"))
from investment_lab.ic_report import generate_ic_report
if __name__=="__main__":
    base=Path(__file__).resolve().parent
    for f in generate_ic_report(base):
        print("generated",f.relative_to(base))
