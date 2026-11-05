"""Fatigue cycle counts and MTBF survival for the 50,000 h requirement.

A reliability prediction assumes a constant failure rate during useful life (decision D12),
so a population that just meets the MTBF follows R(t) = exp(-t / MTBF).
Prints Markdown tables quoted in docs/functional-design.md.

    python calcs/reliability.py
"""
from math import exp, log

MTBF_H = 50_000
SPEED_RPM = 3600
VANE_COUNTS = (6, 8)  # placeholders; the vane count is open
HOURS_PER_YEAR = 8760


def revolutions(hours=MTBF_H, rpm=SPEED_RPM):
    return rpm * 60 * hours


def reliability(hours, mtbf=MTBF_H):
    return exp(-hours / mtbf)


def cycle_table():
    revs = revolutions()
    rows = [
        ("Shaft, rotating bending under a fixed-direction load", "1", revs),
        ("Vane load and stroke, single-lobe", "1", revs),
        ("Vane load and stroke, balanced double-lobe", "2", 2 * revs),
    ]
    rows += [(f"Vane passes and pressure pulses on ring and housing (z = {z})", "z", z * revs) for z in VANE_COUNTS]
    print(f"| Load | Cycles per rev | Cycles in {MTBF_H:,} h at {SPEED_RPM} RPM |")
    print("|---|---|---|")
    for name, per_rev, n in rows:
        print(f"| {name} | {per_rev} | {n:.2e} |")
    print()


def mtbf_table():
    rate = 1 / MTBF_H
    print(f"Failure rate λ = 1/MTBF = {rate:.1e} per hour ({rate * HOURS_PER_YEAR:.3f} per unit-year).\n")
    print("| Running time | Hours | Fraction of units surviving |")
    print("|---|---|---|")
    rows = [
        ("1 year", HOURS_PER_YEAR),
        ("Median life (MTBF × ln 2)", MTBF_H * log(2)),
        ("MTBF", MTBF_H),
    ]
    for name, h in rows:
        print(f"| {name} | {h:,.0f} | {reliability(h):.1%} |")
    print()


def replacement_table():
    """Each failure is repaired or the pump swapped, so a pump position sees t/MTBF failures on average."""
    print(f"Mean time between failures: {MTBF_H / HOURS_PER_YEAR:.1f} years of continuous running.\n")
    print("| Years installed | Original pumps failed | Expected failures per installed position |")
    print("|---|---|---|")
    for years in (1, 2, 3, 5, 10):
        h = years * HOURS_PER_YEAR
        print(f"| {years} | {1 - reliability(h):.0%} | {h / MTBF_H:.2f} |")
    print()


if __name__ == "__main__":
    cycle_table()
    mtbf_table()
    replacement_table()
