"""Level 1 vane-pocket model of the single-lobe sliding-vane pump.

Follows every pocket between two vanes through a turn of the rotor: its volume from the ring geometry, whether it is
open to the inlet port, open to the outlet port or sealed between them, the liquid leaking in and out through the
small gaps, and its pressure. From the pocket pressures it works out the delivered flow, the shaft torque and power,
and the force holding each vane tip on the ring. Method, assumptions and results are in
docs/functional-design.md (Vane-pocket model).

Modelling choices agreed on 2026-11-10: single-lobe layout first; side gap swept from 0.0003 to 0.002 in; pass mark
85% volumetric efficiency at 150 °F; runs at 150 °F and -20 °F; both under-vane feeds compared; 6 to 12 vanes;
plain port edges (notches later); the vane material sets the vane-end and slot gaps through its expansion; tip
friction 0.15; ports big enough to have no pressure loss.

    python calcs/vane_pocket_model.py           # checks, sweep, tables and figures (a few minutes)
    python calcs/vane_pocket_model.py --quick   # checks and the reference pump only, no figures
"""
import argparse
import time
from pathlib import Path

import numpy as np
from CoolProp.CoolProp import PropsSI

import displacement
from r134a_properties import FLUID, PA_PER_PSI, f_to_k, psig_to_pa

M_PER_IN = 0.0254
N_PER_LBF = 4.448222
W_PER_HP = 745.7
M3S_PER_GPM = 231 * M_PER_IN**3 / 60
NM_PER_INLBF = N_PER_LBF * M_PER_IN
KGM3_PER_LBIN3 = 27679.9

# Brief
SPEED_RPM = 3600
P_IN_PSIG, P_OUT_PSIG = 55.0, 150.0
TEMPS_F = (150.0, -20.0)

# Placeholders until the vane, shaft and port design is done (each is listed in the docs)
VANE_T_IN = displacement.VANE_THICKNESS_IN   # 0.10 in
MIN_VANE_H_IN = 0.25        # vane height is max(6e, 0.25 in): two thirds of it stays in the slot at full stroke
SHAFT_R_IN = 0.375          # inner edge of the rotor face (0.75 in shaft)
TIP_GAP_IN = 0.0001         # effective gap of a vane tip in contact with the ring (surface roughness)
TIP_LAND_IN = 0.02          # width of the sealing land on a rounded vane tip
SLOT_GAP_IN = 0.0005        # vane-to-slot clearance at 68 °F
FRICTION = 0.15             # vane tip on ring and vane in slot
PORT_OVERLAP_DEG = 1.0      # how much wider each port land is than a pocket's opening
ASSEMBLY_F = 68.0           # temperature at which the gaps are set
STACK_CTE = 6.5e-6          # per °F: ring, side plates and rotor (cast iron and steel expand alike)

VANES = {  # density (lb/in³), expansion (per °F)
    "Tool steel": (0.283, 6.5e-6),
    "Carbon-graphite": (0.065, 2.5e-6),
    "PEEK wear grade": (0.053, 5.55e-6),
}
FEEDS = {"outlet": "Outlet pressure, always", "switching": "Pocket pressure, switching"}

REF = dict(e=0.05, L=1.0, z=8, gap=0.0005)
SIDE_GAPS_IN = (0.0003, 0.0005, 0.00075, 0.001, 0.0015, 0.002)
ECC_IN = (0.015, 0.02, 0.025, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10, 0.125, 0.15)
LENGTHS_IN = (0.5, 0.75, 1.0, 1.25, 1.5, 2.0)
VANE_COUNTS = tuple(range(6, 13))
ETA_TARGET = 0.85

INLET, OUTLET, SEALED = 0, 1, 2
P_IN, P_OUT = psig_to_pa(P_IN_PSIG), psig_to_pa(P_OUT_PSIG)
OMEGA = 2 * np.pi * SPEED_RPM / 60
FIG_DIR = Path(__file__).resolve().parent.parent / "docs" / "figures"

_LIQUID = {}


def liquid(t_f):
    """Saturated-liquid viscosity and bulk modulus (rho times the speed of sound squared), per D9."""
    if t_f not in _LIQUID:
        tk = f_to_k(t_f)
        rho = PropsSI("D", "T", tk, "Q", 0, FLUID)
        _LIQUID[t_f] = dict(mu=PropsSI("V", "T", tk, "Q", 0, FLUID),
                            beta=rho * PropsSI("A", "T", tk, "Q", 0, FLUID) ** 2)
    return _LIQUID[t_f]


class PeriodicIntegral:
    """Running integral of a function sampled on a uniform periodic grid, evaluated at any angle."""

    def __init__(self, q):
        m = len(q)
        d = 2 * np.pi / m
        qq = np.append(q, q[0])
        self.grid = np.arange(m + 1) * d
        self.cum = np.concatenate([[0.0], np.cumsum((qq[1:] + qq[:-1]) / 2 * d)])
        self.total = self.cum[-1]

    def __call__(self, th):
        k = np.floor(th / (2 * np.pi))
        return np.interp(th - 2 * np.pi * k, self.grid, self.cum) + k * self.total

    def arc(self, a, b):
        return self(b) - self(a)


class Geometry:
    """Ring, rotor, vanes, ports and side gap for one eccentricity, vane count and under-vane feed.

    SI units, angles in radians. The rotor centre is the origin and the rotor turns towards +θ. The round ring is
    offset by e so it touches the rotor at θ = 0 (top dead centre). Pockets grow over the inlet (0 < θ < π) and
    shrink over the outlet (π < θ < 2π). Vane k sits at θ_k; pocket k lies between vane k (behind) and vane k + 1.
    """

    def __init__(self, e_in, z, feed, overlap_deg=PORT_OVERLAP_DEG, m_side=2048):
        self.e_in, self.z, self.feed = e_in, z, feed
        self.R = displacement.ROTOR_DIA_IN / 2 * M_PER_IN
        self.e = e_in * M_PER_IN
        self.Rc = self.R + self.e
        self.t = VANE_T_IN * M_PER_IN
        self.H = max(6 * e_in, MIN_VANE_H_IN) * M_PER_IN
        self.Ri = self.R - self.H                   # slot bottoms, where the under-vane grooves are
        self.Rsh = SHAFT_R_IN * M_PER_IN
        self.delta = 2 * np.pi / z
        self.tau = self.t / self.R                  # vane thickness as an angle at the rim
        self.overlap = np.radians(overlap_deg)
        self.land = self.delta - self.tau + self.overlap
        th = np.linspace(0, 2 * np.pi, 20001)
        self._area = PeriodicIntegral(((self.rho(th) ** 2 - self.R**2) / 2)[:-1])
        self._side_gap(m_side)

    # Ring radius seen from the rotor centre, and its derivatives with θ
    def _s(self, th):
        return np.sqrt(self.Rc**2 - (self.e * np.sin(th)) ** 2)

    def rho(self, th):
        return -self.e * np.cos(th) + self._s(th)

    def drho(self, th):
        return self.e * np.sin(th) - self.e**2 * np.sin(th) * np.cos(th) / self._s(th)

    def d2rho(self, th):
        s = self._s(th)
        u = self.e**2 * np.sin(th) * np.cos(th)
        return self.e * np.cos(th) - self.e**2 * np.cos(2 * th) / s - u**2 / s**3

    def pocket_area(self, th, h, dh):
        """Cross-section of each pocket and its rate of change with shaft angle. Each vane takes t/2 × its
        extension from the pocket on either side."""
        hn, dhn = np.roll(h, -1), np.roll(dh, -1)
        area = self._area.arc(th, th + self.delta) - self.t / 2 * (h + hn)
        darea = (self.rho(th + self.delta) ** 2 - self.rho(th) ** 2) / 2 - self.t / 2 * (dh + dhn)
        return area, darea

    def status(self, th):
        """INLET, OUTLET or SEALED for each pocket. A pocket is sealed while its opening lies within a land."""
        c = np.mod(th + self.delta / 2, 2 * np.pi)
        sealed = (np.minimum(c, 2 * np.pi - c) <= self.overlap / 2) | (np.abs(c - np.pi) <= self.overlap / 2)
        return np.where(sealed, SEALED, np.where(c < np.pi, INLET, OUTLET))

    def under_vane(self, th):
        if self.feed == "outlet":
            return np.full(self.z, P_OUT)
        return np.where(np.mod(th, 2 * np.pi) < np.pi, P_IN, P_OUT)

    def displacement_per_rev(self, under_vane=True):
        """Exact swept volume per revolution per metre of rotor length, with under-vane pumping if fed that way."""
        area = []
        for c in (0.0, np.pi):                                  # pocket 0 centred on each dead centre
            th = c - self.delta / 2 + self.delta * np.arange(self.z)
            area.append(self.pocket_area(th, self.rho(th) - self.R, self.drho(th))[0][0])
        v = self.z * (area[1] - area[0])
        if self.feed == "switching" and under_vane:
            v += self.z * self.t * 2 * self.e                   # under-vane spaces fill at inlet, empty at outlet
        return v

    def side_gap_balance(self, P):
        """Flow into all pockets from the faces, and flow out of all grooves into the faces, for one pressure set
        (per unit c³/12μ). They must be equal."""
        th = self.delta * np.arange(self.z)
        into_pockets = (np.einsum("kj,j->k", self.A, P) + self.face_g(th)).sum()
        per_in, per_out, k_in, k_out = self.groove_split(th)
        return into_pockets, (P * (per_in + per_out)).sum() + k_in + k_out

    def _side_gap(self, m):
        """Thin-film (Reynolds) flow in the gap between each rotor face and its side plate.

        The face is an annulus from the slot bottoms (Ri) to the rotor rim (R). With a uniform gap, pressure in the
        film obeys Laplace's equation, which on an annulus solves mode by mode in a Fourier series. The rim sees the
        pocket pressures, ramping linearly across each vane end; the inner edge sees the under-vane grooves. For the
        switching feed the region inside the grooves (to the shaft) is a dead end that still carries flow between
        the inlet and outlet grooves.
        """
        th = np.arange(m) * 2 * np.pi / m
        n = np.arange(m // 2 + 1)
        lam = np.log(self.R / self.Ri)
        lam_in = np.log(self.Ri / self.Rsh)
        x = np.minimum(np.maximum(n, 1) * lam, 700.0)
        coth, csch = 1 / np.tanh(x), 1 / np.sinh(x)
        tanh_in = np.tanh(np.minimum(np.maximum(n, 1) * lam_in, 700.0))

        def solve(f, g):
            """Flow (per radian, per unit c³/12μ) entering the film at the rim and at the grooves."""
            F, G = np.fft.rfft(f), np.fft.rfft(g)
            rim = n * (F * coth - G * csch)
            rim[0] = (F[0] - G[0]) / lam
            groove = n * (G * coth - F * csch)
            groove[0] = (G[0] - F[0]) / lam
            disk = n * G * tanh_in
            disk[0] = 0
            return np.fft.irfft(rim, m), np.fft.irfft(groove, m), np.fft.irfft(disk, m)

        # Pocket 0 shape on the rim: 1 across its opening, ramping to 0 across each vane end
        w = np.mod(th + np.pi, 2 * np.pi) - np.pi
        half = self.tau / 2
        b0 = np.clip((w + half) / self.tau, 0, 1) - np.clip((w - self.delta + half) / self.tau, 0, 1)
        rim0, groove0, _ = solve(b0, np.zeros(m))
        rim0_int = PeriodicIntegral(rim0)
        col = np.array([-rim0_int.arc(k * self.delta, (k + 1) * self.delta) for k in range(self.z)])
        self.A = np.array([np.roll(col, j) for j in range(self.z)]).T   # A[k, j]: into pocket k per Pa in pocket j
        self._groove0 = PeriodicIntegral(groove0)

        # Groove pressures, fixed to the ring
        if self.feed == "outlet":
            g = np.full(m, P_OUT)
        else:
            # Inlet groove over 0..π, outlet groove over π..2π, pressure ramping linearly across each land
            d0 = np.mod(th + np.pi, 2 * np.pi) - np.pi          # signed angle from top dead centre
            dpi = np.pi - th                                     # signed angle from bottom dead centre
            d = np.where(np.abs(d0) < np.abs(dpi), d0, dpi)
            g_in = np.clip(0.5 + d / self.land, 0, 1)
            g = P_IN * g_in + P_OUT * (1 - g_in)
        rim_g, groove_g, disk_g = solve(np.zeros(m), g)
        self._rim_g = PeriodicIntegral(rim_g)
        gg = PeriodicIntegral(groove_g + disk_g)
        self._groove_g = (gg.arc(0, np.pi), gg.arc(np.pi, 2 * np.pi))

    def face_g(self, th):
        """Flow into each pocket across the rotor faces driven by the grooves (per unit c³/12μ)."""
        return -self._rim_g.arc(th, th + self.delta)

    def groove_split(self, th):
        """Flow out of the inlet and outlet grooves into the faces, per Pa in each pocket, plus the groove-only
        part. Returns (per_pocket_in (z,), per_pocket_out (z,), const_in, const_out)."""
        if self.feed == "outlet":
            per = self._groove0.arc(-th, 2 * np.pi - th)
            return np.zeros(self.z), per, 0.0, sum(self._groove_g)
        per_in = self._groove0.arc(-th, np.pi - th)
        per_out = self._groove0.arc(np.pi - th, 2 * np.pi - th)
        return per_in, per_out, self._groove_g[0], self._groove_g[1]


def simulate(geom, cases, *, friction=FRICTION, tip_gap_in=TIP_GAP_IN, slot_gap_in=SLOT_GAP_IN, beta_scale=1.0,
             mass_scale=1.0, drag=True, traces=False, steps_per_overlap=20):
    """Run the pump through one vane pitch (after a pitch of warm-up) for a batch of cases sharing one geometry.

    cases: dict of equal-length sequences 'L_in', 'gap_in', 'material', 't_f'. Returns a dict of arrays, one value
    per case. The whole pump repeats every vane pitch, so one pitch covers every pocket and vane over a full turn.
    """
    z, t, H, R = geom.z, geom.t, geom.H, geom.R

    def col(v):
        return np.asarray(v, dtype=float)[:, None]

    L = col(cases["L_in"]) * M_PER_IN
    cs = col(cases["gap_in"]) * M_PER_IN
    mu = col([liquid(tf)["mu"] for tf in cases["t_f"]])
    beta = col([liquid(tf)["beta"] for tf in cases["t_f"]]) * beta_scale
    dens = col([VANES[mat][0] for mat in cases["material"]]) * KGM3_PER_LBIN3
    cte = col([VANES[mat][1] for mat in cases["material"]])
    d_temp = col(cases["t_f"]) - ASSEMBLY_F
    c_ve = cs + (STACK_CTE - cte) * L * d_temp / 2       # each vane end; rotor and ring expand alike
    s_gap = slot_gap_in * M_PER_IN + (STACK_CTE - cte) * t * d_temp
    rub, bind = (c_ve <= 0)[:, 0], (s_gap <= 0)[:, 0]
    c_ve, s_gap = np.maximum(c_ve, 1e-9), np.maximum(s_gap, 1e-9)
    ks = 2 * cs**3 / (12 * mu)                            # both rotor faces
    g_tip = (tip_gap_in * M_PER_IN) ** 3 * L / (12 * mu * TIP_LAND_IN * M_PER_IN)
    mass = dens * t * L * H * mass_scale
    t_visc = (np.pi * mu * OMEGA * (R**4 - geom.Rsh**4) / cs)[:, 0] * drag
    B = L.shape[0]

    dphi = min(geom.overlap / steps_per_overlap, geom.delta / 600)
    n = int(np.ceil(2 * geom.delta / dphi))
    dphi = 2 * geom.delta / n
    dt = dphi / OMEGA
    period = geom.delta / OMEGA
    diag_a = np.diag(geom.A)

    th0 = -geom.delta + geom.delta * np.arange(z)
    st0 = geom.status(th0)
    c0 = np.mod(th0 + geom.delta / 2, 2 * np.pi)
    P = np.tile(np.where(st0 == INLET, P_IN, np.where(st0 == OUTLET, P_OUT,
                                                       np.where(np.minimum(c0, 2 * np.pi - c0) < 1, P_OUT, P_IN))),
                (B, 1)).astype(float)
    prev = st0
    vol_in = np.zeros(B)
    vol_out = np.zeros(B)
    out_series, torque_series = [], []
    e_tip, e_slot = np.zeros(B), np.zeros(B)
    n_min, n_max = np.full(B, np.inf), np.full(B, -np.inf)
    p_min, p_max = np.full(B, np.inf), np.full(B, -np.inf)
    tr = dict(th=[], P=[], N=[]) if traces else None

    for i in range(n):
        rec = i >= n // 2
        th = -geom.delta + i * dphi + geom.delta * np.arange(z)
        rho, drho = geom.rho(th), geom.drho(th)
        h = rho - R
        area, darea = geom.pocket_area(th, h, drho)
        V, Vdot = L * area, L * darea * OMEGA
        st = geom.status(th)
        conn = st != SEALED
        port_p = np.where(st == INLET, P_IN, P_OUT)
        opened = conn & (prev == SEALED)
        if rec and opened.any():
            jump = np.where(opened, V * (port_p - P) / beta, 0.0)   # volume the port pushes in as it opens
            vol_in += jump[:, st == INLET].sum(1)
            vol_out += jump[:, st == OUTLET].sum(1)
        P = np.where(conn, port_p, P)
        pu = geom.under_vane(th)

        face = ks * (np.einsum("bj,kj->bk", P, geom.A) + geom.face_g(th))
        gv = 2 * c_ve**3 * h / (12 * mu * t) + g_tip           # across each vane: both ends plus the tip
        p_back = np.roll(P, 1, axis=1)
        qv = gv * (p_back - P)
        vane_in = qv - np.roll(qv, -1, axis=1)
        gs = s_gap**3 * L / (12 * mu * (H - h))
        d_back, d_front = pu - p_back, pu - P
        to_front = np.abs(d_front) >= np.abs(d_back)           # open side of the slot faces the bigger Δp
        qs = gs * np.where(to_front, d_front, d_back)
        slot_in = np.where(to_front, qs, 0.0) + np.roll(np.where(to_front, 0.0, qs), -1, axis=1)
        leak = face + vane_in + slot_in

        if rec:
            q_port = Vdot - leak
            cav = t * L * drho * OMEGA + qs                     # groove into each under-vane space
            per_in, per_out, k_in, k_out = geom.groove_split(th)
            g_in = ks[:, 0] * (np.einsum("bj,j->b", P, per_in) + k_in)
            g_out = ks[:, 0] * (np.einsum("bj,j->b", P, per_out) + k_out)
            in_half = (np.mod(th, 2 * np.pi) < np.pi) if geom.feed == "switching" else np.zeros(z, bool)
            f_in = q_port[:, st == INLET].sum(1) + cav[:, in_half].sum(1) + g_in
            f_out = q_port[:, st == OUTLET].sum(1) + cav[:, ~in_half].sum(1) + g_out
            vol_in += f_in * dt
            vol_out += f_out * dt
            out_series.append(-f_out)

            d2 = geom.d2rho(th)
            hd, hdd = OMEGA * drho, OMEGA**2 * d2
            gam = np.arctan2(drho, rho)
            rcg = rho - H / 2
            base = mass * (OMEGA**2 * rcg - hdd) + (pu - (p_back + P) / 2) * t * L
            press_t = (p_back - P) * L * h
            N = base / np.cos(gam)
            for _ in range(5):
                fs = 2 * mass * OMEGA * hd - press_t - N * (np.sin(gam) - friction * np.cos(gam))
                N = (base - friction * np.abs(fs) * np.sign(hd)) / (np.cos(gam) + friction * np.sin(gam))
            nc = np.maximum(N, 0.0)
            torque = ((P - p_back) * L * (rho**2 - R**2) / 2
                      + rho * nc * (friction * np.cos(gam) - np.sin(gam))
                      + 2 * mass * OMEGA * rcg * hd).sum(1) + t_visc
            torque_series.append(torque)
            e_tip += (friction * nc * OMEGA * np.sqrt(rho**2 + drho**2)).sum(1) * dt
            e_slot += (friction * np.abs(fs) * np.abs(hd)).sum(1) * dt
            n_min, n_max = np.minimum(n_min, N.min(1)), np.maximum(n_max, N.max(1))
            p_min, p_max = np.minimum(p_min, P.min(1)), np.maximum(p_max, P.max(1))
            if traces:
                tr["th"].append(th.copy())
                tr["P"].append(P.copy())
                tr["N"].append(N.copy())

        if not conn.all():
            b = (-ks * diag_a + gv + np.roll(gv, -1, axis=1) + np.where(to_front, gs, 0.0)
                 + np.roll(np.where(to_front, 0.0, gs), -1, axis=1))
            a = leak + b * P
            p_inf = (a - Vdot) / b
            p_new = p_inf + (P - p_inf) * np.exp(-beta * b * dt / V)
            P = np.where(conn, P, p_new)
        prev = st

    q_th = geom.displacement_per_rev() * L[:, 0] * SPEED_RPM / 60
    q_del = -vol_out / period
    q_inlet = vol_in / period
    torque = np.array(torque_series)
    out = np.array(out_series)
    t_mean = torque.mean(0)
    p_shaft = t_mean * OMEGA
    p_hyd = q_del * (P_OUT - P_IN)
    res = dict(q_th=q_th, q_del=q_del, q_inlet=q_inlet, eta_v=q_del / q_th,
               t_mean=t_mean, t_max=torque.max(0), p_shaft=p_shaft, p_hyd=p_hyd,
               p_tip=e_tip / period, p_slot=e_slot / period, p_visc=t_visc * OMEGA,
               n_min=n_min, n_max=n_max, p_min=p_min, p_max=p_max,
               ripple=(out.max(0) - out.min(0)) / q_del, rub=rub, bind=bind,
               c_ve=c_ve[:, 0], s_gap=s_gap[:, 0])
    res["energy_resid"] = (p_shaft - (q_th * (P_OUT - P_IN) + res["p_tip"] + res["p_slot"] + res["p_visc"])) / p_shaft
    if traces:
        res["traces"] = {k: np.array(v) for k, v in tr.items()}
    return res


def cases_for(L_in=(REF["L"],), gaps=(REF["gap"],), materials=tuple(VANES), temps=TEMPS_F):
    rows = [(l, g, m, tf) for l in L_in for g in gaps for m in materials for tf in temps]
    return dict(L_in=[r[0] for r in rows], gap_in=[r[1] for r in rows], material=[r[2] for r in rows],
                t_f=[r[3] for r in rows])


# ----------------------------------------------------------------------------------------------------------- output
def gpm(q):
    return q / M3S_PER_GPM


def lbf(f):
    return f / N_PER_LBF


def psig(p):
    return p / PA_PER_PSI - 14.696


def verification():
    print("### Verification\n")
    print("| Check | Expected | Model | Result |")
    print("|---|---|---|---|")
    e, L, z = REF["e"], REF["L"], REF["z"]
    for feed in FEEDS:
        # A rigid liquid trapped in a shrinking pocket has nowhere to go, so this check uses a near-zero land overlap
        g = Geometry(e, z, feed, overlap_deg=0.01)
        no_gaps = cases_for(gaps=(1e-7,), materials=("Tool steel",), temps=(150.0,))
        ideal = simulate(g, no_gaps, friction=0.0, tip_gap_in=1e-7, slot_gap_in=1e-7, beta_scale=1e6,
                         steps_per_overlap=1)
        q_th, q_del = gpm(ideal["q_th"][0]), gpm(ideal["q_del"][0])
        print(f"| Rigid liquid, no gaps, no friction ({FEEDS[feed].lower()}): delivered flow equals the swept volume "
              f"| {q_th:.3f} GPM | {q_del:.3f} GPM | {abs(q_del / q_th - 1) * 100:.2f}% off |")
        lossless = simulate(g, no_gaps, friction=0.0, tip_gap_in=1e-7, slot_gap_in=1e-7, drag=False,
                            steps_per_overlap=1)
        t_ideal = lossless["q_th"][0] * (P_OUT - P_IN) / OMEGA
        print(f"| No gaps, no friction, no drag: mean shaft torque equals swept volume × Δp / 2π "
              f"| {t_ideal / NM_PER_INLBF:.2f} in·lbf | {lossless['t_mean'][0] / NM_PER_INLBF:.2f} in·lbf "
              f"| {abs(lossless['t_mean'][0] / t_ideal - 1) * 100:.2f}% off |")
    g = Geometry(e, z, "outlet")
    formula = displacement.gpm(displacement.single_lobe_in3(e, L, z, VANE_T_IN))
    exact = gpm(g.displacement_per_rev() * L * M_PER_IN * SPEED_RPM / 60)
    print(f"| Swept volume against displacement.py's V = 2eL(πD_c − zt), z = {z} | {formula:.3f} GPM | {exact:.3f} GPM "
          f"| {(exact / formula - 1) * 100:+.1f}%: the formula is exact only for many vanes (see docs) |")
    crescent = displacement.gpm(np.pi * ((displacement.ROTOR_DIA_IN / 2 + e) ** 2 - (displacement.ROTOR_DIA_IN / 2) ** 2) * L)
    print(f"| Esposito's (π/2)(D_c + D_r)eL is the crescent volume, not the swept volume | {crescent:.3f} GPM "
          f"| {exact:.3f} GPM | ratio {exact / crescent:.2f}: the swept volume is about twice the crescent |")
    for feed in FEEDS:
        g = Geometry(e, z, feed)
        test_p = P_IN + (P_OUT - P_IN) * np.random.default_rng(1).random(z)    # uneven, so the flows are large
        into, out_of = g.side_gap_balance(test_p)
        print(f"| Side gap, {FEEDS[feed].lower()}: flow into the pockets from the faces = flow out of the grooves "
              f"| {out_of:.4g} | {into:.4g} | {abs(into / out_of - 1) * 100:.3f}% off |")
        r = simulate(g, cases_for(materials=("Tool steel",), temps=(150.0,)))
        print(f"| Energy balance, 150 °F, {FEEDS[feed].lower()}: shaft power = swept volume × Δp + friction + drag "
              f"| 0% | {r['energy_resid'][0] * 100:+.2f}% | {abs(r['energy_resid'][0]) * 100:.2f}% unaccounted |")
        dv = (g.displacement_per_rev(under_vane=False) * L * M_PER_IN * SPEED_RPM / 60 * (P_OUT - P_IN)
              / liquid(150.0)["beta"])
        got = r["q_inlet"][0] - r["q_del"][0]
        print(f"| Volume balance, {FEEDS[feed].lower()}: inlet flow − outlet flow = compression of the pockets' swept volume "
              f"| {gpm(dv):.4f} GPM | {gpm(got):.4f} GPM | {abs(got / dv - 1) * 100:.1f}% off |")
    fine = Geometry(e, z, "switching", m_side=8192)
    coarse = Geometry(e, z, "switching")
    a, b = simulate(coarse, cases_for(materials=("Tool steel",), temps=(150.0,))), \
        simulate(fine, cases_for(materials=("Tool steel",), temps=(150.0,)))
    print(f"| Side-gap solver: 2,048 against 8,192 points round the rim (leakage) "
          f"| {gpm(b['q_th'][0] - b['q_del'][0]):.4f} GPM | {gpm(a['q_th'][0] - a['q_del'][0]):.4f} GPM "
          f"| {abs((a['q_th'][0] - a['q_del'][0]) / (b['q_th'][0] - b['q_del'][0]) - 1) * 100:.2f}% off |")
    print()


def reference_tables():
    e, L, z = REF["e"], REF["L"], REF["z"]
    print(f"### Reference pump: e = {e} in, L = {L} in, z = {z}, t = {VANE_T_IN} in, side gap {REF['gap']} in\n")
    print("| Under-vane feed | Vane | Temp (°F) | Swept (GPM) | Delivered (GPM) | Vol. eff. | Shaft (hp) | "
          "Hydraulic (hp) | Overall eff. | Tip friction (hp) | Mean / peak torque (in·lbf) | Tip force min / max "
          "(lbf) | Flags |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    results = {}
    for feed in FEEDS:
        g = Geometry(e, z, feed)
        cs = cases_for()
        r = simulate(g, cs)
        results[feed] = (cs, r)
        for i in range(len(cs["t_f"])):
            flags = []
            if r["n_min"][i] < 0:
                flags.append("vane lifts off")
            if r["rub"][i]:
                flags.append("vane ends rub")
            if r["bind"][i]:
                flags.append("vane binds in slot")
            if r["p_min"][i] < 0:
                flags.append("pocket in tension")
            print(f"| {FEEDS[feed]} | {cs['material'][i]} | {cs['t_f'][i]:.0f} | {gpm(r['q_th'][i]):.2f} "
                  f"| {gpm(r['q_del'][i]):.2f} | {r['eta_v'][i] * 100:.1f}% | {r['p_shaft'][i] / W_PER_HP:.2f} "
                  f"| {r['p_hyd'][i] / W_PER_HP:.2f} | {r['p_hyd'][i] / r['p_shaft'][i] * 100:.0f}% "
                  f"| {r['p_tip'][i] / W_PER_HP:.2f} | {r['t_mean'][i] / NM_PER_INLBF:.1f} / "
                  f"{r['t_max'][i] / NM_PER_INLBF:.1f} | {lbf(r['n_min'][i]):.1f} / {lbf(r['n_max'][i]):.1f} "
                  f"| {', '.join(flags) or '—'} |")
    print()
    print("Sealed-pocket pressure (pocket switching between ports), steel vanes:\n")
    print("| Under-vane feed | Temp (°F) | Lowest pocket pressure (psig) | Highest pocket pressure (psig) |")
    print("|---|---|---|---|")
    for feed in FEEDS:
        cs, r = results[feed]
        for i in range(len(cs["t_f"])):
            if cs["material"][i] == "Tool steel":
                print(f"| {FEEDS[feed]} | {cs['t_f'][i]:.0f} | {psig(r['p_min'][i]):.0f} | {psig(r['p_max'][i]):.0f} |")
    print()
    print("Gap changes with temperature (set equal to the side gap and 0.0005 in at 68 °F):\n")
    print("| Vane | Temp (°F) | Vane-end gap, each end (in) | Slot gap (in) |")
    print("|---|---|---|---|")
    cs, r = results["switching"]
    for i in range(len(cs["t_f"])):
        print(f"| {cs['material'][i]} | {cs['t_f'][i]:.0f} | {r['c_ve'][i] / M_PER_IN:.5f} "
              f"| {r['s_gap'][i] / M_PER_IN:.5f} |")
    print()
    return results


def sweep():
    """Every eccentricity, length, vane count, side gap, vane material, feed and temperature."""
    rows = []
    start = time.time()
    for feed in FEEDS:
        for e in ECC_IN:
            for z in VANE_COUNTS:
                g = Geometry(e, z, feed)
                cs = cases_for(L_in=LENGTHS_IN, gaps=SIDE_GAPS_IN)
                r = simulate(g, cs)
                for i in range(len(cs["t_f"])):
                    rows.append(dict(feed=feed, e=e, z=z, L=cs["L_in"][i], gap=cs["gap_in"][i],
                                     material=cs["material"][i], t_f=cs["t_f"][i],
                                     **{k: r[k][i] for k in ("q_th", "q_del", "eta_v", "p_shaft", "p_hyd",
                                                             "t_max", "n_min", "rub", "bind")}))
    print(f"<!-- sweep: {len(rows):,} cases in {time.time() - start:.0f} s -->\n")
    return rows


def eff(x):
    return f"{x * 100:.0f}%" if x > 0 else "flows backwards"


def sweep_tables(rows):
    def pick(**kw):
        return [r for r in rows if all(r[k] == v for k, v in kw.items())]

    ref = dict(e=REF["e"], L=REF["L"], material="Tool steel")
    print(f"### Volumetric efficiency against side gap: e = {REF['e']} in, L = {REF['L']} in, {REF['z']} steel "
          "vanes\n")
    print("| Side gap (in) | " + " | ".join(f"{FEEDS[f]}, {tf:.0f} °F" for f in FEEDS for tf in TEMPS_F) + " |")
    print("|---|" + "---|" * 4)
    for gap in SIDE_GAPS_IN:
        cells = [eff(pick(feed=f, z=REF["z"], gap=gap, t_f=tf, **ref)[0]["eta_v"]) for f in FEEDS for tf in TEMPS_F]
        print(f"| {gap} | " + " | ".join(cells) + " |")
    print()

    print(f"### Smallest practical pump: smallest swept volume with volumetric efficiency ≥ {ETA_TARGET:.0%} at "
          f"150 °F, {REF['z']} steel vanes\n")
    print("Each cell: e × L (in), then delivered flow and volumetric efficiency. `*` marks the smallest size tried "
          f"(e = {ECC_IN[0]} in, L = {LENGTHS_IN[0]} in): the limit lies below the sweep.\n")
    print("| Side gap (in) | " + " | ".join(FEEDS.values()) + " |")
    print("|---|---|---|")
    for gap in SIDE_GAPS_IN:
        cells = []
        for f in FEEDS:
            ok = [r for r in pick(feed=f, z=REF["z"], gap=gap, material="Tool steel", t_f=150.0)
                  if r["eta_v"] >= ETA_TARGET]
            if not ok:
                cells.append("none in the sweep")
                continue
            best = min(ok, key=lambda r: (r["q_th"], -r["eta_v"]))
            floor = "*" if (best["e"], best["L"]) == (ECC_IN[0], LENGTHS_IN[0]) else ""
            cells.append(f"{best['e']} × {best['L']}{floor}: {gpm(best['q_del']):.1f} GPM, {best['eta_v']:.0%}")
        print(f"| {gap} | " + " | ".join(cells) + " |")
    print()

    print(f"### Vane count: e = {REF['e']} in, L = {REF['L']} in, side gap {REF['gap']} in, steel vanes, 150 °F\n")
    print("| Vanes | " + " | ".join(f"{FEEDS[f]}: {k}" for f in FEEDS
                                    for k in ("vol. eff.", "shaft hp", "lowest tip force (lbf)")) + " |")
    print("|---|" + "---|" * 6)
    for z in VANE_COUNTS:
        cells = []
        for f in FEEDS:
            r = pick(feed=f, z=z, gap=REF["gap"], t_f=150.0, **ref)[0]
            cells += [f"{r['eta_v']:.1%}", f"{r['p_shaft'] / W_PER_HP:.2f}", f"{lbf(r['n_min']):.1f}"]
        print(f"| {z} | " + " | ".join(cells) + " |")
    print()

    print("### Vane materials at the reference size, 150 °F, z = 8\n")
    print("| Under-vane feed | Side gap (in) | " + " | ".join(VANES) + " |")
    print("|---|---|" + "---|" * len(VANES))
    for f in FEEDS:
        for gap in (0.0005, 0.001):
            cells = []
            for m in VANES:
                r = pick(feed=f, e=REF["e"], L=REF["L"], z=8, gap=gap, material=m, t_f=150.0)[0]
                note = " (lifts off)" if r["n_min"] < 0 else ""
                cells.append(f"{r['eta_v'] * 100:.1f}%{note}")
            print(f"| {FEEDS[f]} | {gap} | " + " | ".join(cells) + " |")
    print()


# ---------------------------------------------------------------------------------------------------------- figures
INK, INK2, MUTED, GRID, AXIS, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
SERIES = ("#2a78d6", "#eb6834", "#1baf7a")


def _style(ax):
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.xaxis.label.set_color(INK2)
    ax.yaxis.label.set_color(INK2)


def _rev(th, values):
    """Unfold one pitch of per-pocket or per-vane values into one curve over a full turn."""
    ang = np.degrees(np.mod(th, 2 * np.pi)).ravel()
    order = np.argsort(ang)
    return ang[order], values.ravel()[order]


def figures():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    FIG_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "sans-serif", "font.size": 10, "figure.facecolor": SURFACE})
    e, L, z = REF["e"], REF["L"], REF["z"]
    written = []

    # 1. Pocket pressure over one turn, with the two sealed zones enlarged
    g = Geometry(e, z, "outlet")
    r = simulate(g, cases_for(materials=("Tool steel",)), traces=True)
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.6), dpi=200, sharey=True, gridspec_kw=dict(width_ratios=[2.2, 1, 1]))
    windows = ((0, 360, "One full turn"), (178, 182, "Near bottom dead centre"),
               (-2, 2, "Near top dead centre"))
    for ax, (lo, hi, title) in zip(axes, windows):
        _style(ax)
        for i, tf in enumerate(TEMPS_F):
            th = r["traces"]["th"] + g.delta / 2
            a, p = _rev(th, psig(r["traces"]["P"][:, i, :]))
            if lo < 0:
                a = np.where(a > 180, a - 360, a)
                order = np.argsort(a)
                a, p = a[order], p[order]
            ax.plot(a, p, color=SERIES[i], linewidth=1.6, label=f"{tf:.0f} °F")
        ax.set_xlim(lo, hi)
        ax.set_title(title, color=INK, fontsize=9, loc="left")
        if lo < 0 or lo > 100:
            seal = np.degrees(g.overlap) / 2
            centre = 0 if lo < 0 else 180
            ax.axvspan(centre - seal, centre + seal, color=GRID, alpha=0.6, linewidth=0)
            y, va = (0.97, "top") if centre else (0.06, "bottom")     # keep clear of the lines
            ax.text(centre, y, "sealed", ha="center", va=va, color=INK2, fontsize=8,
                    transform=ax.get_xaxis_transform())
    axes[0].set_xticks(range(0, 361, 90))
    axes[0].text(90, 60, "open to inlet", ha="center", color=INK2, fontsize=9)
    axes[0].text(270, 140, "open to outlet", ha="center", va="top", color=INK2, fontsize=9)
    axes[0].set_ylabel("Pocket pressure (psig)")
    axes[1].set_xlabel("Pocket position, degrees from top dead centre")
    axes[0].legend(frameon=False, labelcolor=INK2, loc="center left")
    fig.suptitle(f"Pocket pressure: e = {e} in, L = {L} in, {z} steel vanes, side gap {REF['gap']} in, "
                 f"under-vane fed from the outlet", color=INK, fontsize=10, x=0.01, ha="left")
    fig.tight_layout()
    path = FIG_DIR / "vane-pocket-pressure.png"
    fig.savefig(path)
    plt.close(fig)
    written.append(path)

    # 2. Volumetric efficiency against side gap
    gaps = np.array(SIDE_GAPS_IN)
    fig, ax = plt.subplots(figsize=(7.5, 3.6), dpi=200)
    _style(ax)
    for i, feed in enumerate(FEEDS):
        r = simulate(Geometry(e, z, feed), cases_for(gaps=SIDE_GAPS_IN, materials=("Tool steel",), temps=(150.0,)))
        ax.plot(gaps * 1000, r["eta_v"] * 100, color=SERIES[i], linewidth=1.6, marker="o", markersize=4,
                label=FEEDS[feed])
        k = list(SIDE_GAPS_IN).index(0.001)
        ax.annotate(FEEDS[feed], (gaps[k] * 1000, r["eta_v"][k] * 100), xytext=(8, 0), textcoords="offset points",
                    ha="left", va="center", color=INK2, fontsize=9)
    ax.axhline(ETA_TARGET * 100, color=MUTED, linewidth=1, linestyle="--")
    ax.text(gaps[0] * 1000, ETA_TARGET * 100 + 1, f"pass mark {ETA_TARGET:.0%}", color=INK2, fontsize=9)
    ax.set_xlabel("Side gap between rotor face and side plate (thousandths of an inch)")
    ax.set_ylabel("Volumetric efficiency (%)")
    ax.set_ylim(0, 100)
    ax.set_title(f"Volumetric efficiency at 150 °F (e = {e} in, L = {L} in, {z} steel vanes)", color=INK,
                 fontsize=10, loc="left")
    ax.legend(frameon=False, labelcolor=INK2, loc="lower left")
    fig.tight_layout()
    path = FIG_DIR / "vane-pocket-efficiency.png"
    fig.savefig(path)
    plt.close(fig)
    written.append(path)

    # 3. Vane tip force over one turn
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.6), dpi=200, sharey=True)
    for ax, feed in zip(axes, FEEDS):
        _style(ax)
        r = simulate(Geometry(e, z, feed), cases_for(temps=(150.0,)), traces=True)
        for i, mat in enumerate(VANES):
            a, nn = _rev(r["traces"]["th"], lbf(r["traces"]["N"][:, i, :]))
            ax.plot(a, nn, color=SERIES[i], linewidth=1.6, label=mat)
        ax.axhline(0, color=AXIS, linewidth=1)
        ax.set_xlim(0, 360)
        ax.set_xticks(range(0, 361, 90))
        ax.set_xlabel("Vane position, degrees from top dead centre")
        ax.set_title(FEEDS[feed], color=INK, fontsize=10, loc="left")
    axes[0].set_ylabel("Tip force on the ring (lbf)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, labelcolor=INK2, fontsize=9, ncol=3, loc="lower center")
    axes[1].text(270, -1.2, "below 0: the vane lifts off", ha="center", va="top", color=INK2, fontsize=8)
    fig.suptitle(f"Vane tip force at 150 °F: e = {e} in, L = {L} in, {z} vanes, side gap {REF['gap']} in",
                 color=INK, fontsize=10, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    path = FIG_DIR / "vane-pocket-tip-force.png"
    fig.savefig(path)
    plt.close(fig)
    written.append(path)
    for p in written:
        print(f"Wrote {p.relative_to(FIG_DIR.parent.parent)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--quick", action="store_true", help="checks and reference pump only")
    args = ap.parse_args()
    verification()
    results = reference_tables()
    if not args.quick:
        sweep_tables(sweep())
        figures()


if __name__ == "__main__":
    main()
