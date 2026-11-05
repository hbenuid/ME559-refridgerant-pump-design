"""Rotor and vane kinematics at 3600 RPM, and the tip-wear budget, from the team notes of 2026-11-05.

The 3.22 in cam bore and 6 vanes in the team notes are illustrative (a round ring with e = 0.06 in); the vane count
and layout are still open (D7). The 50 um tip-wear allowance is the team's working value.
Prints Markdown tables quoted in docs/requirements.md and docs/functional-design.md.

    python calcs/vane_kinematics.py
"""
from math import pi

SPEED_RPM = 3600
LIFE_H = 50_000
ROTOR_D_IN = 3.10
CAM_BORE_D_IN = 3.22        # illustrative
WEAR_ALLOWANCE_UM = 50.0    # team working value, about 0.002 in
G_IN_S2 = 386.1
M_PER_IN = 0.0254


def kinematics_table():
    omega = 2 * pi * SPEED_RPM / 60
    print(f"Angular speed ω = 2πn/60 = {omega:.0f} rad/s.\n")
    print("| Diameter | D (in) | Surface speed (ft/min) | Surface speed (m/s) | Centripetal acceleration (g) |")
    print("|---|---|---|---|---|")
    for name, d in (("Rotor rim", ROTOR_D_IN), ("Cam bore (illustrative)", CAM_BORE_D_IN)):
        v_fpm = pi * d * SPEED_RPM / 12
        a_g = omega ** 2 * (d / 2) / G_IN_S2
        print(f"| {name} | {d:.2f} | {v_fpm:,.0f} | {v_fpm * 0.3048 / 60:.1f} | {a_g:.0f} |")
    print()


def wear_budget():
    v_tip = pi * CAM_BORE_D_IN * M_PER_IN * SPEED_RPM / 60
    distance_m = v_tip * LIFE_H * 3600
    rate = WEAR_ALLOWANCE_UM / (distance_m / 1e6)
    print(f"Sliding distance over {LIFE_H:,} h at {v_tip:.1f} m/s: {distance_m:.2e} m ({distance_m / 1e3:.2e} km).")
    print(f"A {WEAR_ALLOWANCE_UM:.0f} µm tip allowance allows at most {rate:.3f} µm of wear per 1,000 km "
          f"({rate / 1000:.1e} µm per km).\n")


if __name__ == "__main__":
    kinematics_table()
    wear_budget()
