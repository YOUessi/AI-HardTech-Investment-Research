"""Generate public-listed Unitree reverse valuation & combined IC dashboard."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/"src"))
from investment_lab.unitree_report import generate_unitree_report
if __name__=="__main__":
    base=Path(__file__).resolve().parent
    for p in generate_unitree_report(base):
        print("generated",p.relative_to(base))
