"""
G.R.A.C.E. — Cost & Downtime Scenario Model
============================================

Reproduces the downtime-avoided and financial-exposure-avoided figures from the
G.R.A.C.E. consulting presentation, and regenerates the charts in /visuals.

All inputs are ILLUSTRATIVE MODELLING ASSUMPTIONS, not verified client data.
See docs/assumptions-and-limitations.md.

Usage:
    python analysis/scenario_model.py            # print results + write CSV + charts
    python analysis/scenario_model.py --no-plots # results + CSV only
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOURS_PER_DAY = 24

# --- Inputs ------------------------------------------------------------------

D_OEM_DAYS = 14  # reference downtime for a full OEM replacement (fixed)

# PLC spare-part replacement cases, within the stated 1–7 day service range
PLC_CASES = {
    "Fast replacement (3-day)": 3,
    "Slow replacement (7-day)": 7,
}


@dataclass(frozen=True)
class PlantScale:
    name: str
    employees: str
    cost_range_per_hour: str
    modelled_cost_per_hour: float  # lower end of the range, for conservatism


PLANTS = [
    PlantScale("Small", "10–49", "$10,000 – $50,000", 10_000),
    PlantScale("Medium", "50–249", "$50,000 – $150,000", 50_000),
    PlantScale("Large", "250+", "$200,000 – $1M+", 200_000),
]


# --- Formulas ----------------------------------------------------------------

def downtime_avoided(d_oem: float, d_plc: float) -> float:
    """ΔD = D_OEM − D_PLC  (days)"""
    return d_oem - d_plc


def downtime_reduction_pct(delta_d: float, d_oem: float) -> float:
    """D_reduction = ΔD / D_OEM × 100%"""
    return delta_d / d_oem * 100


def exposure_avoided(delta_d_days: float, cost_per_hour: float) -> float:
    """C_savings = ΔD × C_day, where C_day = cost per hour × 24"""
    return delta_d_days * cost_per_hour * HOURS_PER_DAY


# --- Run ---------------------------------------------------------------------

def run() -> list[dict]:
    rows = []
    for plant in PLANTS:
        for case, d_plc in PLC_CASES.items():
            dd = downtime_avoided(D_OEM_DAYS, d_plc)
            rows.append(
                {
                    "plant_scale": plant.name,
                    "employees": plant.employees,
                    "case": case,
                    "d_oem_days": D_OEM_DAYS,
                    "d_plc_days": d_plc,
                    "downtime_avoided_days": dd,
                    "downtime_reduction_pct": round(downtime_reduction_pct(dd, D_OEM_DAYS), 1),
                    "cost_per_hour_usd": plant.modelled_cost_per_hour,
                    "exposure_avoided_usd": exposure_avoided(dd, plant.modelled_cost_per_hour),
                }
            )
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def print_table(rows: list[dict]) -> None:
    print(f"{'Plant':<8}{'Case':<28}{'ΔD (d)':>8}{'Reduction':>11}{'Exposure avoided':>20}")
    for r in rows:
        print(
            f"{r['plant_scale']:<8}{r['case']:<28}{r['downtime_avoided_days']:>8}"
            f"{r['downtime_reduction_pct']:>10}%{r['exposure_avoided_usd'] / 1e6:>18.2f} M"
        )


# --- Charts ------------------------------------------------------------------

def make_charts(rows: list[dict], outdir: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    BLUE, ORANGE, GRAY = "#2a78d6", "#eb6834", "#a3a29c"
    INK, INK2, SURFACE, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#e6e5e0"

    def style(ax):
        ax.set_facecolor(SURFACE)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        ax.tick_params(colors=INK2, length=0)
        ax.xaxis.grid(True, color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)

    # 1) Downtime comparison
    fig, ax = plt.subplots(figsize=(8, 3.2), facecolor=SURFACE)
    labels = ["Full OEM replacement", *PLC_CASES.keys()]
    days = [D_OEM_DAYS, *PLC_CASES.values()]
    colors = [GRAY, BLUE, BLUE]
    y = range(len(labels))[::-1]
    ax.barh(list(y), days, color=colors, height=0.55)
    for yi, d in zip(y, days):
        ax.text(d + 0.2, yi, f"{d} days", va="center", color=INK, fontsize=10)
    ax.set_yticks(list(y), labels, color=INK, fontsize=10)
    ax.set_xlim(0, 16)
    ax.set_xlabel("Downtime per incident (days)", color=INK2)
    style(ax)
    ax.set_title("Downtime per incident: OEM vs PLC spare-part replacement",
                 loc="left", color=INK, fontsize=12, pad=12)
    fig.tight_layout()
    fig.savefig(outdir / "downtime-comparison.png", dpi=160)
    plt.close(fig)

    # 2) Exposure avoided by plant scale
    fig, ax = plt.subplots(figsize=(8, 3.8), facecolor=SURFACE)
    plants = [p.name for p in PLANTS]
    h = 0.36
    for i, (case, color) in enumerate(zip(PLC_CASES, (BLUE, ORANGE))):
        vals = [r["exposure_avoided_usd"] / 1e6 for r in rows if r["case"] == case]
        ys = [len(plants) - 1 - k + (h / 2 + 0.02) * (1 if i == 0 else -1) for k in range(len(plants))]
        ax.barh(ys, vals, height=h, color=color, label=case)
        for yy, v in zip(ys, vals):
            ax.text(v + 0.6, yy, f"${v:,.2f}M", va="center", color=INK, fontsize=9)
    ax.set_yticks(range(len(plants))[::-1], [f"{p} plant" for p in plants], color=INK)
    ax.set_xlim(0, 62)
    ax.set_xlabel("Modelled exposure avoided per incident (USD millions)", color=INK2)
    style(ax)
    ax.legend(frameon=False, loc="upper right", labelcolor=INK)
    ax.set_title("Modelled exposure avoided grows with plant scale",
                 loc="left", color=INK, fontsize=12, pad=12)
    fig.text(0.01, 0.01, "Illustrative only — lower-bound cost per hour for each plant size; not realised savings.",
             color=INK2, fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(outdir / "exposure-by-plant-scale.png", dpi=160)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-plots", action="store_true")
    args = ap.parse_args()

    rows = run()
    print_table(rows)
    write_csv(rows, ROOT / "analysis" / "scenario_results.csv")
    if not args.no_plots:
        make_charts(rows, ROOT / "visuals")


if __name__ == "__main__":
    main()
