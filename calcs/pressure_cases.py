"""Real-fluid pressure and temperature cases for R-134a, from the team notes of 2026-11-05.

The course basis treats the fluid as liquid at all times (decision D9). These cases check what real R-134a does:
the inlet margin to boiling, the outlet temperature rise, the pressure in an idle pump (decision D32), a relief set
in gauge pressure, and liquid trapped between closed isolation valves (Q27).
Prints Markdown tables quoted in docs/requirements.md and docs/functional-design.md.

    python calcs/pressure_cases.py
"""
from CoolProp.CoolProp import PropsSI

FLUID = "R134a"
PA_PER_PSI = 6894.757
ATM_PSI = 14.696

P_INLET_PSIG = 55.0
P_OUTLET_PSIG = 150.0
DESIGN_PSIG = 300.0      # D32
RELIEF_PSIG = 225.0      # team proposal, Q27
ETA = 0.40               # overall efficiency in the team's temperature-rise bound


def psig_to_pa(psig):
    return (psig + ATM_PSI) * PA_PER_PSI


def pa_to_psig(pa):
    return pa / PA_PER_PSI - ATM_PSI


def f_to_k(f):
    return (f - 32) * 5 / 9 + 273.15


def k_to_f(k):
    return (k - 273.15) * 9 / 5 + 32


def psat_psig(t_f):
    return pa_to_psig(PropsSI("P", "T", f_to_k(t_f), "Q", 0, FLUID))


def tsat_f(psig):
    return k_to_f(PropsSI("T", "P", psig_to_pa(psig), "Q", 0, FLUID))


def inlet_margin_table():
    print(f"| Inlet temp (°F) | Psat (psig) | Margin below the {P_INLET_PSIG:.0f} psig inlet (psi) |")
    print("|---|---|---|")
    for t in (-20, 40, 45, 50, 55, 58):
        p = psat_psig(t)
        print(f"| {t} | {p:.1f} | {P_INLET_PSIG - p:.1f} |")
    print(f"\nR-134a freezes (triple point) at {k_to_f(PropsSI('Ttriple', FLUID)):.0f} °F.\n")


def temperature_rise_table():
    """All shaft work treated as heat in the liquid: dT <= dp / (rho * eta * cp)."""
    dp = (P_OUTLET_PSIG - P_INLET_PSIG) * PA_PER_PSI
    print(f"| Inlet temp (°F) | ρ (kg/m³) | c_p (J/kg·K) | ΔT bound at η = {ETA:.0%} (°F) | Outlet temp (°F) "
          f"| Margin below Tsat at {P_OUTLET_PSIG:.0f} psig (°F) |")
    print("|---|---|---|---|---|---|")
    t_boil = tsat_f(P_OUTLET_PSIG)
    for t in (-20, 50):
        rho = PropsSI("D", "T", f_to_k(t), "Q", 0, FLUID)
        cp = PropsSI("C", "T", f_to_k(t), "Q", 0, FLUID)
        dt_f = dp / (rho * ETA * cp) * 9 / 5
        print(f"| {t} | {rho:.0f} | {cp:.0f} | {dt_f:.1f} | {t + dt_f:.1f} | {t_boil - t - dt_f:.0f} |")
    print()


def idle_pressure_table():
    print("| Idle pump temperature (°F) | Pressure in the pump (psig) |")
    print("|---|---|")
    for t in (80, 100, 120, 130, 140, 150):
        print(f"| {t} | {psat_psig(t):.0f} |")
    print(f"\nDesign pressure {DESIGN_PSIG:.0f} psig is the saturation pressure at {tsat_f(DESIGN_PSIG):.0f} °F.")
    print(f"A relief venting at {RELIEF_PSIG:.0f} psig (gauge) would open in an idle pump at "
          f"{tsat_f(RELIEF_PSIG):.0f} °F.\n")


def trapped_liquid_table(t0_f=50.0, p0_psig=P_INLET_PSIG):
    """Liquid-full pump, both isolation valves closed: heating at constant volume (rigid housing)."""
    d0 = PropsSI("D", "T", f_to_k(t0_f), "P", psig_to_pa(p0_psig), FLUID)
    print(f"Start: liquid-full at {t0_f:.0f} °F and {p0_psig:.0f} psig, housing taken as rigid.\n")
    print("| Warming (°F) | Pressure (psig) |")
    print("|---|---|")
    for dt in (1, 2, 5, 10):
        p = PropsSI("P", "T", f_to_k(t0_f + dt), "D", d0, FLUID)
        print(f"| {dt} | {pa_to_psig(p):,.0f} |")
    print()


if __name__ == "__main__":
    inlet_margin_table()
    temperature_rise_table()
    idle_pressure_table()
    trapped_liquid_table()
