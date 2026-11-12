"""Theoretical displacement and flow for a sliding-vane pump with the fixed 3.1 in rotor.

Derivation is in docs/functional-design.md. Both layouts ignore the running clearance at the
sealing arc and assume under-vane volumes are ported so vane stroke subtracts from delivery.

Single-lobe (round ring offset by e, rotor tangent at the seal arc, D_c = D_r + 2e):
    V = 2 e L (pi D_c - z t)
Balanced double-lobe (cam ring major radius R_a, minor radius R_b = R_r, stroke s = R_a - R_b):
    V = 2 L [pi (R_a^2 - R_b^2) - z t s]

Vane count z and thickness t are placeholders until the vane design is done.

    uv run calcs/displacement.py
"""
from math import pi

ROTOR_DIA_IN = 3.1
SPEED_RPM = 3600
DELTA_P_PSI = 150 - 55
VANES = 8
VANE_THICKNESS_IN = 0.10
IN3_PER_GAL = 231.0

LENGTHS_IN = [0.75, 1.0, 1.5, 2.0]
STROKES_IN = [0.050, 0.075, 0.100, 0.125, 0.150]


def single_lobe_in3(e, length, z=VANES, t=VANE_THICKNESS_IN):
    d_ring = ROTOR_DIA_IN + 2 * e
    return 2 * e * length * (pi * d_ring - z * t)


def balanced_in3(s, length, z=VANES, t=VANE_THICKNESS_IN):
    r_b = ROTOR_DIA_IN / 2
    r_a = r_b + s
    return 2 * length * (pi * (r_a**2 - r_b**2) - z * t * s)


def gpm(in3_per_rev, rpm=SPEED_RPM):
    return in3_per_rev * rpm / IN3_PER_GAL


def hydraulic_hp(flow_gpm):
    return flow_gpm * DELTA_P_PSI / 1714


def table(name, fn, stroke_label):
    print(f"### {name}: theoretical flow (GPM) at {SPEED_RPM} RPM, z = {VANES}, t = {VANE_THICKNESS_IN} in\n")
    print(f"| {stroke_label} (in) | " + " | ".join(f"L = {l} in" for l in LENGTHS_IN) + " |")
    print("|---|" + "---|" * len(LENGTHS_IN))
    for s in STROKES_IN:
        print(f"| {s:.3f} | " + " | ".join(f"{gpm(fn(s, l)):.1f}" for l in LENGTHS_IN) + " |")
    print()


if __name__ == "__main__":
    table("Single-lobe", single_lobe_in3, "Eccentricity e")
    table("Balanced double-lobe", balanced_in3, "Cam stroke s")
    print(f"Hydraulic power at Δp = {DELTA_P_PSI} psi: {hydraulic_hp(1):.3f} hp per GPM "
          f"(e.g. 10 GPM → {hydraulic_hp(10):.2f} hp, before efficiency losses).")
