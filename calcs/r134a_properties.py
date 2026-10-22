"""R-134a liquid properties over the specified temperature range.

Per the instructor the fluid is treated as liquid at all times (decision D9), so saturated-liquid
density and viscosity at each temperature are the design properties. The actual state at the
55 psig inlet is printed alongside to show where that simplification departs from reality.
Prints Markdown tables quoted in docs/requirements.md.

    python calcs/r134a_properties.py
"""
from CoolProp.CoolProp import PropsSI

FLUID = "R134a"
PA_PER_PSI = 6894.757
ATM_PSI = 14.696
LBFT3_PER_KGM3 = 0.062428

P_INLET_PSIG = 55.0
P_OUTLET_PSIG = 150.0
TEMPS_F = [-20, 0, 20, 40, 58, 80, 100, 112, 120, 150]


def psig_to_pa(psig):
    return (psig + ATM_PSI) * PA_PER_PSI


def pa_to_psig(pa):
    return pa / PA_PER_PSI - ATM_PSI


def f_to_k(f):
    return (f - 32) * 5 / 9 + 273.15


def k_to_f(k):
    return (k - 273.15) * 9 / 5 + 32


def tsat_f(psig):
    return k_to_f(PropsSI("T", "P", psig_to_pa(psig), "Q", 0, FLUID))


def saturation_points():
    print("| Point | Pressure (psig) | Pressure (psia) | Saturation temp (°F) |")
    print("|---|---|---|---|")
    for name, psig in (("Inlet", P_INLET_PSIG), ("Outlet", P_OUTLET_PSIG)):
        print(f"| {name} | {psig:.0f} | {psig + ATM_PSI:.1f} | {tsat_f(psig):.1f} |")
    ratio = (P_OUTLET_PSIG + ATM_PSI) / (P_INLET_PSIG + ATM_PSI)
    print(f"\nAbsolute pressure ratio: {ratio:.2f}. Differential pressure: {P_OUTLET_PSIG - P_INLET_PSIG:.0f} psi.")
    print(f"Critical temperature: {k_to_f(PropsSI('Tcrit', FLUID)):.1f} °F\n")


def range_table():
    p_in = psig_to_pa(P_INLET_PSIG)
    print("| Fluid temp (°F) | ρ (lb/ft³) | μ (cP) | ν (cSt) | Psat (psig) | Actual state at 55 psig |")
    print("|---|---|---|---|---|---|")
    for t in TEMPS_F:
        tk = f_to_k(t)
        psat = PropsSI("P", "T", tk, "Q", 0, FLUID)
        rho = PropsSI("D", "T", tk, "Q", 0, FLUID)
        mu = PropsSI("V", "T", tk, "Q", 0, FLUID)
        state = "liquid" if psat < p_in else "vapor"
        print(f"| {t} | {rho * LBFT3_PER_KGM3:.1f} | {mu * 1000:.3f} | {mu / rho * 1e6:.3f} "
              f"| {pa_to_psig(psat):.1f} | {state} |")
    water_mu = PropsSI("V", "T", f_to_k(68), "P", 101325, "Water")
    water_rho = PropsSI("D", "T", f_to_k(68), "P", 101325, "Water")
    print(f"\nFor comparison, water at 68 °F: μ = {water_mu * 1000:.2f} cP, ν = {water_mu / water_rho * 1e6:.2f} cSt.\n")


if __name__ == "__main__":
    saturation_points()
    range_table()
