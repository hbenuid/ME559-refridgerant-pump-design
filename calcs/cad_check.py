"""Check the team's CAD against the design docs.

Reads the Onshape assembly snapshot in cad/ and measures the parts that set how the pump works: rotor, cam ring,
vanes, side gaps, kidney ports, under-vane grooves, housing ports, bushings, containment can, magnetic coupling and
motor face. From those sizes it works out the eccentricity, the swept volume and flow (calcs/displacement.py), the
containment can's stress at the design pressure (calcs/pressure_cases.py), which parts share volume, and whether each
bolted joint has a screw in every hole.

Parts are found by their Onshape names and features by their geometry. The shaft axis is Y and the rotor centre is at
X = Z = 0. Angles are measured from +Z (the top, where the rotor comes closest to the ring) towards +X.

The can stresses are thin-shell and flat-plate hand formulas (Roark, Table 11.2 cases 10a and 10b), not FEA.

Prints Markdown tables quoted in docs/functional-design.md (CAD check). Takes a few seconds.

    uv run calcs/cad_check.py [assembly.step]
"""
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

import build123d as bd
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane

from displacement import ROTOR_DIA_IN, gpm, single_lobe_in3
from pressure_cases import DESIGN_PSIG

STEP = Path(__file__).resolve().parent.parent / "cad" / "2026-11-19__Mag_pump_assembly.step"
MM = 25.4                    # build123d works in mm; everything printed is in inches
TOL = 1e-4                   # in, for matching radii and positions
SLIP_RPM = 3450              # a 2-pole induction motor under load (Q4)
POISSON = 0.3                # steel
YIELD_316_PSI = 30_000       # 316 stainless, annealed: ASTM A240 minimum yield (check)
NEMA_56C = {"pilot (AK)": 4.500, "bolt circle (AJ)": 5.875, "shaft (U)": 0.625}   # NEMA MG 1 (check)
# Model reference pump and its smallest passing size (docs/functional-design.md, vane-pocket model)
REFERENCE = "e = 0.05 in, L = 1.0 in, 8 vanes: 14.1 GPM"
MODEL_SIDE_GAP_IN = 0.0005


# ---------- geometry helpers ----------

def angle(x, z):
    """Degrees from +Z towards +X, 0-360."""
    return math.degrees(math.atan2(x, z)) % 360


def ybox(solid):
    bb = solid.bounding_box()
    return bb.min.Y / MM, bb.max.Y / MM


def cylinders(solid):
    out = []
    for f in solid.faces():
        s = BRepAdaptor_Surface(f.wrapped)
        if s.GetType() != GeomAbs_Cylinder:
            continue
        c = s.Cylinder()
        d, p = c.Axis().Direction(), c.Axis().Location()
        bb, cen = f.bounding_box(), f.center()
        along_y, along_x = abs(d.Y()) > 0.999, abs(d.X()) > 0.999
        out.append({
            "r": c.Radius() / MM,
            "along_y": along_y,
            "along_x": along_x,
            "oblique": not (along_y or along_x or abs(d.Z()) > 0.999),
            "x": p.X() / MM if along_y else None,     # axis position, for cylinders along Y
            "z": p.Z() / MM if along_y else None,
            "y0": bb.min.Y / MM,
            "y1": bb.max.Y / MM,
            "span": math.degrees(s.LastUParameter() - s.FirstUParameter()),
            "mid": angle(cen.X, cen.Z),
            "cx": cen.X / MM,
        })
    return out


def on_axis(c):
    return c["along_y"] and math.hypot(c["x"], c["z"]) < TOL


def planes(solid):
    for f in solid.faces():
        s = BRepAdaptor_Surface(f.wrapped)
        if s.GetType() == GeomAbs_Plane:
            n = s.Plane().Axis().Direction()
            yield f, (n.X(), n.Y(), n.Z())


def arcs(faces):
    """Arc faces as (start, end, span) in degrees, sorted by start."""
    out = []
    for c in faces:
        if c["span"] < 359:
            out.append(((c["mid"] - c["span"] / 2) % 360, (c["mid"] + c["span"] / 2) % 360, c["span"]))
    return sorted(out)


def lands(arc_list):
    """Gaps between consecutive arcs, as (centre, width) in degrees."""
    out = []
    for (s0, e0, _), (s1, _, _) in zip(arc_list, arc_list[1:] + arc_list[:1]):
        width = (s1 - e0) % 360
        out.append(((e0 + width / 2) % 360, width))
    return out


def covers(arc, a):
    start, _, span = arc
    return (a - start) % 360 <= span


def side(a):
    return "+X" if 0 < a < 180 else "−X"


def one(parts, name):
    found = parts[name]
    if len(found) != 1:
        raise ValueError(f"expected one {name!r}, found {len(found)}")
    return found[0]


def load(path):
    asm = bd.import_step(str(path))
    parts = defaultdict(list)
    for solid in asm.leaves:
        # Onshape names reach the file with "_" for spaces and for the point in "1.5"
        name = re.sub(r"(?<=\d)_(?=\d)", ".", solid.label).replace("_", " ")
        parts[name].append(solid)
    return dict(parts)


# ---------- measurements ----------

def pumping_element(parts):
    rotor, ring = one(parts, "06 Rotor"), one(parts, "04 Cam Ring")
    front, rear = one(parts, "03 Front End Plate"), one(parts, "05 Rear End Plate")
    m = {}
    m["r_rotor"] = max(c["r"] for c in cylinders(rotor) if on_axis(c))
    assert abs(2 * m["r_rotor"] - ROTOR_DIA_IN) < 1e-3, "rotor diameter is not the 3.1 in of D5"
    ry0, ry1 = ybox(rotor)
    m["L_rotor"] = ry1 - ry0
    root = [c for c in cylinders(rotor) if c["along_y"] and not on_axis(c)]
    m["slot_root_holes"] = len(root)
    m["slot_root_d"] = 2 * root[0]["r"]
    m["slot_root_radius"] = sum(math.hypot(c["x"], c["z"]) for c in root) / len(root)

    bore = max((c for c in cylinders(ring) if c["along_y"] and not on_axis(c) and c["r"] > m["r_rotor"]),
               key=lambda c: c["r"])
    m["r_bore"] = bore["r"]
    m["e"] = math.hypot(bore["x"], bore["z"])
    m["ring_centre_angle"] = angle(bore["x"], bore["z"])
    gy0, gy1 = ybox(ring)
    m["ring_t"] = gy1 - gy0
    m["seal_gap"] = m["r_bore"] - m["e"] - m["r_rotor"]
    m["max_protrusion"] = m["r_bore"] + m["e"] - m["r_rotor"]

    # end plates must close the ring faces, and their port edges follow the ring bore
    assert abs(ybox(front)[1] - gy0) < 1e-5 and abs(ybox(rear)[0] - gy1) < 1e-5, "end plates don't touch the ring"
    for plate in (front, rear):
        edge = [c for c in cylinders(plate) if c["along_y"] and abs(c["r"] - m["r_bore"]) < TOL]
        assert edge and all(abs(math.hypot(c["x"], c["z"]) - m["e"]) < TOL for c in edge), "ports don't follow bore"
    m["gap_front"] = ry0 - gy0
    m["gap_rear"] = gy1 - ry1

    vanes = parts["07 Vane"]
    m["z"] = len(vanes)
    v = vanes[0]
    big = sorted(((f, n) for f, n in planes(v) if abs(n[1]) < 0.5), key=lambda fn: fn[0].area)[-2:]
    n = big[1][1]
    c0, c1 = big[0][0].center(), big[1][0].center()
    m["t_vane"] = abs((c1.X - c0.X) * n[0] + (c1.Y - c0.Y) * n[1] + (c1.Z - c0.Z) * n[2]) / MM
    tip = cylinders(v)[0]
    m["r_tip"] = tip["r"]
    d = (-n[2], 0.0, n[0])                       # along the vane, in the XZ plane
    proj = [(p.X * d[0] + p.Z * d[2]) / MM for p in v.vertices()]
    ax = tip["x"] * d[0] + tip["z"] * d[2]
    if ax < sum(proj) / len(proj):
        proj, ax = [-p for p in proj], -ax
    m["h_vane"] = max(max(proj), ax + m["r_tip"]) - min(proj)
    vy0, vy1 = ybox(v)
    m["L_vane"] = vy1 - vy0
    m["vane_end_gap"] = (m["ring_t"] - m["L_vane"]) / 2
    m["pitch"] = 360 / m["z"]

    m["swept"] = single_lobe_in3(m["e"], m["L_rotor"], z=m["z"], t=m["t_vane"])
    m["gpm"] = gpm(m["swept"])
    m["gpm_slip"] = gpm(m["swept"], SLIP_RPM)
    return m


def plate_porting(plate, r_rotor):
    """Kidney ports (arcs at the rotor radius) and under-vane groove (shallow arcs inside it) of one end plate."""
    cyl = cylinders(plate)
    ports = arcs([c for c in cyl if on_axis(c) and abs(c["r"] - r_rotor) < TOL])
    groove = [c for c in cyl if on_axis(c) and 0.6 < c["r"] < r_rotor - 0.1 and c["y1"] - c["y0"] < 0.1]
    r_out = max(c["r"] for c in groove)
    r_in = min(c["r"] for c in groove)
    outer = [c for c in groove if abs(c["r"] - r_out) < TOL]
    return ports, arcs(outer), r_in, r_out, outer[0]["y1"] - outer[0]["y0"]


def porting(parts, m):
    front = plate_porting(one(parts, "03 Front End Plate"), m["r_rotor"])
    rear = plate_porting(one(parts, "05 Rear End Plate"), m["r_rotor"])
    flat = lambda p: [round(x, 1) for arc in p[0] + p[1] for x in arc] + [round(x, 4) for x in p[2:]]
    assert flat(front) == flat(rear), "front and rear end plates are ported differently"
    ports, g_arcs, r_in, r_out, depth = front
    seal = lands(ports)
    housing = one(parts, "01 Housing")
    hc = cylinders(housing)
    hports = {}
    for s in ("−X", "+X"):
        faces = [c for c in hc if c["along_x"] and (c["cx"] < 0) == (s == "−X")]
        hports[s] = (2 * min(c["r"] for c in faces), 2 * max(c["r"] for c in faces))
    drains = [c for c in hc if c["oblique"]]
    return {
        "ports": ports, "seal": seal, "groove_arcs": g_arcs, "groove_lands": lands(g_arcs),
        "groove_r": (r_in, r_out), "groove_depth": depth,
        "housing_ports": hports,
        "drains": (len(drains), 2 * drains[0]["r"] if drains else 0,
                   min(c["y0"] for c in drains) if drains else 0, max(c["y1"] for c in drains) if drains else 0,
                   sorted("−X" if c["cx"] < 0 else "+X" for c in drains)),
    }


def drive(parts):
    m = {}
    bushings = parts["09 Bushing"]
    bc = cylinders(bushings[0])
    m["bushings"] = len(bushings)
    m["bush_bore"] = 2 * min(c["r"] for c in bc)
    m["bush_od"] = sorted({round(2 * c["r"], 4) for c in bc})[1:]
    by0, by1 = ybox(bushings[0])
    m["bush_len"] = by1 - by0
    centres = sorted(sum(ybox(b)) / 2 for b in bushings)
    m["bush_span"] = centres[-1] - centres[0]
    shaft = one(parts, "08 Shaft")
    journal = max(c["r"] for c in cylinders(shaft) if on_axis(c) and c["r"] <= m["bush_bore"] / 2)
    m["journal"] = 2 * journal
    m["bush_clearance"] = m["bush_bore"] - m["journal"]

    can = one(parts, "11 Containment CAN")
    cc = [c for c in cylinders(can) if on_axis(c)]
    tube = [c for c in cc if c["y1"] - c["y0"] > 1.0]
    m["can_ri"], m["can_ro"] = min(c["r"] for c in tube), max(c["r"] for c in tube)
    flange = max(cc, key=lambda c: c["r"])
    m["can_flange_t"] = flange["y1"] - flange["y0"]
    ends = sorted(f.center().Y / MM for f, n in planes(can)
                  if abs(n[1]) > 0.999 and f.bounding_box().size.X / MM / 2 <= m["can_ro"] + TOL)
    m["can_end_t"] = ends[-1] - ends[-2]
    curved = [f for f in can.faces()
              if BRepAdaptor_Surface(f.wrapped).GetType() not in (GeomAbs_Plane, GeomAbs_Cylinder)]
    m["can_flat_end"] = not curved

    inner, outer = one(parts, "10 Inner Magnet Hub"), one(parts, "12 Outer Magnet Hub")
    m["inner_od"] = 2 * max(c["r"] for c in cylinders(inner) if on_axis(c))
    m["inner_y"] = ybox(inner)
    obore = min((c for c in cylinders(outer) if on_axis(c) and c["r"] > m["can_ro"]), key=lambda c: c["r"])
    m["outer_bore"] = 2 * obore["r"]
    m["outer_y"] = (obore["y0"], obore["y1"])
    m["gap_inner"] = m["can_ri"] - m["inner_od"] / 2
    m["gap_outer"] = obore["r"] - m["can_ro"]
    m["gap_total"] = obore["r"] - m["inner_od"] / 2
    m["magnet_overlap"] = min(m["inner_y"][1], m["outer_y"][1]) - max(m["inner_y"][0], m["outer_y"][0])
    m["hub_overhang"] = sum(m["inner_y"]) / 2 - centres[-1]
    m["room_inside"] = ends[-2] - m["inner_y"][1]      # inner hub's end face to the can end
    m["room_outside"] = obore["y1"] - ends[-1]         # can end to the bottom of the outer hub's bore

    adapter, motor = one(parts, "13 Motor Adapter"), one(parts, "14 Motor")
    ac = cylinders(adapter)
    m["pilot"] = 2 * min(c["r"] for c in ac if on_axis(c))
    amid = sum(ybox(adapter)) / 2
    bolts = [c for c in ac if c["along_y"] and not on_axis(c) and c["y0"] > amid]
    m["bolt_circle"] = 2 * sum(math.hypot(c["x"], c["z"]) for c in bolts) / len(bolts)
    m["motor_shaft"] = 2 * min(c["r"] for c in cylinders(motor) if on_axis(c))
    return m


def can_stress(m):
    p, t, t_end = DESIGN_PSIG, m["can_ro"] - m["can_ri"], m["can_end_t"]
    r_mean, a = (m["can_ri"] + m["can_ro"]) / 2, m["can_ri"]
    return {
        "p": p, "t": t, "t_end": t_end, "r_mean": r_mean, "a": a,
        "hoop": p * r_mean / t,
        "axial": p * r_mean / (2 * t),
        "flat_clamped": 3 * p * a**2 / (4 * t_end**2),                       # Roark 10b, at the edge
        "flat_simple": 3 * (3 + POISSON) * p * a**2 / (8 * t_end**2),        # Roark 10a, at the centre
        "t_clamped": a * math.sqrt(3 * p / (4 * YIELD_316_PSI)),
        "t_simple": a * math.sqrt(3 * (3 + POISSON) * p / (8 * YIELD_316_PSI)),
        "hemi": p * r_mean / (2 * t_end),
    }


def fasteners(parts):
    """For each screw type, the part it passes through, that part's matching holes, and the screws in them."""
    cache = {name: [cylinders(s) for s in solids] for name, solids in parts.items()
             if "screw" not in name.lower() and "dowel" not in name.lower()}
    rows = []
    for name, screws in parts.items():
        if "screw" not in name.lower():
            continue
        shank_r = min(c["r"] for c in cylinders(screws[0]) if c["along_y"])
        found = defaultdict(set)
        hole_r = {}
        for i, s in enumerate(screws):
            sc = next(c for c in cylinders(s) if c["along_y"] and abs(c["r"] - shank_r) < TOL)
            sy0, sy1 = ybox(s)
            for pname, per_solid in cache.items():
                for cyls in per_solid:
                    for h in cyls:
                        if (h["along_y"] and not on_axis(h) and shank_r < h["r"] <= shank_r + 0.06
                                and math.hypot(h["x"] - sc["x"], h["z"] - sc["z"]) < 0.005
                                and h["y0"] < sy1 and h["y1"] > sy0):
                            found[pname].add(i)
                            hole_r[pname] = (h["r"], h["y0"])
        for pname, placed in found.items():
            r, y0 = hole_r[pname]
            holes = {(round(h["x"], 3), round(h["z"], 3)) for cyls in cache[pname] for h in cyls
                     if h["along_y"] and abs(h["r"] - r) < TOL and abs(h["y0"] - y0) < TOL}
            rows.append((name, pname, 2 * r, len(holes), len(placed)))
    return sorted(rows, key=lambda row: row[1])


def overlaps(parts):
    solids = [(name, s) for name, ss in parts.items() for s in ss]
    boxes = [s.bounding_box() for _, s in solids]
    found = defaultdict(list)
    for i in range(len(solids)):
        for j in range(i + 1, len(solids)):
            a, b = boxes[i], boxes[j]
            if (a.min.X >= b.max.X or b.min.X >= a.max.X or a.min.Y >= b.max.Y or b.min.Y >= a.max.Y
                    or a.min.Z >= b.max.Z or b.min.Z >= a.max.Z):
                continue
            common = solids[i][1].intersect(solids[j][1])
            pieces = list(common) if isinstance(common, (list, bd.ShapeList)) else [common] if common else []
            vol = sum(piece.volume for piece in pieces) / MM**3
            if vol < 1e-7:
                continue
            names = tuple(sorted((solids[i][0], solids[j][0])))
            text = " ".join(names).lower()
            if "14 motor" in text:
                kind = "Motor drawn as a solid block with no tapped holes (expected)"
            elif "screw" in text:
                kind = "Screw drawn at full size in a tapped hole (expected)"
            elif "dowel" in text:
                kind = "Dowel press fit (expected)"
            else:
                shared = bd.Compound(pieces)
                radii = [c["r"] for c in cylinders(shared) if on_axis(c)]
                cy0, cy1 = ybox(shared)
                depth = max(radii) - min(radii) if len(radii) > 1 else float("nan")
                kind = (f"**Clash**: {depth:.4f} in deep on the radius, from {2 * min(radii):.3f} to "
                        f"{2 * max(radii):.3f} in diameter, Y {cy0:.3f} to {cy1:.3f} in")
            found[(names, kind)].append(vol)
    return found


# ---------- output ----------

def main(path):
    parts = load(path)
    pe = pumping_element(parts)
    po = porting(parts, pe)
    dr = drive(parts)
    st = can_stress(dr)

    print(f"## CAD check: {Path(path).name}\n")
    print(f"{len(parts)} distinct parts, {sum(len(v) for v in parts.values())} in all. Lengths in inches.\n")
    print("### Parts\n")
    print("| Part | Count |")
    print("|---|---|")
    for name in sorted(parts):
        print(f"| {name} | {len(parts[name])} |")

    print("\n### Pumping element\n")
    print("| Item | CAD | Docs |")
    print("|---|---|---|")
    print(f"| Rotor diameter | {2 * pe['r_rotor']:.4f} | 3.1 ([D5](decisions.md)) |")
    print(f"| Rotor length L | {pe['L_rotor']:.4f} | Model reference: {REFERENCE} |")
    print(f"| Cam ring bore | {2 * pe['r_bore']:.4f}, round (single-lobe) | Layout open ([D7](decisions.md)) |")
    print(f"| Eccentricity e | {pe['e']:.4f}; ring centre at {pe['ring_centre_angle']:.0f}° | — |")
    print(f"| Rotor to ring at the top | {pe['seal_gap']:.4f} | Model and displacement.py take 0 |")
    print(f"| Vane stroke (2e) and largest protrusion | {2 * pe['e']:.4f}, {pe['max_protrusion']:.4f} | — |")
    print(f"| Vanes | {pe['z']}, pitch {pe['pitch']:.1f}° | Model swept 6–12; reference 8 |")
    print(f"| Vane thickness × height × length | {pe['t_vane']:.4f} × {pe['h_vane']:.3f} × {pe['L_vane']:.4f} "
          f"| displacement.py placeholder t = 0.10 |")
    print(f"| Vane tip radius | {pe['r_tip']:.3f} | — |")
    held = pe['h_vane'] - pe['max_protrusion']
    print(f"| Vane left in its slot at full protrusion | {held:.3f} ({held / pe['h_vane']:.0%} of its height) | — |")
    print(f"| Slot-root holes | {pe['slot_root_holes']} × {pe['slot_root_d']:.3f} dia at radius "
          f"{pe['slot_root_radius']:.3f} | — |")
    print(f"| Ring thickness | {pe['ring_t']:.4f} | — |")
    print(f"| Side gap, rotor (front, rear) | {pe['gap_front']:.4f}, {pe['gap_rear']:.4f} | Model reference "
          f"{MODEL_SIDE_GAP_IN} ([Q31](open-questions.md)) |")
    print(f"| Side gap, vane ends (each) | {pe['vane_end_gap']:.4f} | — |")
    print(f"| Swept volume | {pe['swept']:.3f} in³/rev | — |")
    print(f"| Ideal flow | {pe['gpm']:.2f} GPM at 3600 RPM, {pe['gpm_slip']:.2f} at {SLIP_RPM} | Smallest passing "
          f"pump 2.0–4.8 GPM at a 0.0005 in side gap ([Q2](open-questions.md)) |")

    print("\n### Ports and under-vane grooves (the front and rear end plates match)\n")
    print("| Item | CAD |")
    print("|---|---|")
    for s, e, span in po["ports"]:
        print(f"| Kidney port, {side((s + span / 2) % 360)} side | {s:.0f}° to {e:.0f}° ({span:.0f}°) |")
    for c, w in po["seal"]:
        ok = "wider" if w > pe["pitch"] else "**narrower**"
        print(f"| Sealing land at {c:.0f}° | {w:.0f}°, {ok} than one vane pitch ({pe['pitch']:.1f}°) |")
    r_in, r_out = po["groove_r"]
    print(f"| Under-vane groove | {2 * r_in:.3f} to {2 * r_out:.3f} dia, {po['groove_depth']:.3f} deep; slot-root "
          f"holes at radius {pe['slot_root_radius']:.3f} sit over it |")
    for arc in po["groove_arcs"]:
        s, e, span = arc
        seals = [f"{c:.0f}°" for c, _ in po["seal"] if covers(arc, c)]
        where = f"covers the sealing lands at {', '.join(seals)}" if seals else "covers no sealing land"
        print(f"| Groove arc, {side((s + span / 2) % 360)} side | {s:.0f}° to {e:.0f}° ({span:.0f}°), {where} |")
    for c, w in po["groove_lands"]:
        print(f"| Groove break at {c:.0f}° | {w:.0f}° |")
    for s, (bore, face) in po["housing_ports"].items():
        print(f"| Housing port, {s} side | bore {bore:.3f} dia, largest step {face:.3f} dia |")
    n, d, y0, y1, sides = po["drains"]
    print(f"| Drilled holes from the can space to the side passages | {n} × {d:.3f} dia, Y {y0:.2f} to {y1:.2f}, "
          f"on the {' and '.join(sides)} sides |")

    print("\n### Shaft, bushings, coupling and motor\n")
    print("| Item | CAD | Docs |")
    print("|---|---|---|")
    print(f"| Bushings | {dr['bushings']} flanged sleeves, bore {dr['bush_bore']:.4f}, OD "
          f"{' / '.join(f'{x:.3f}' for x in dr['bush_od'])}, {dr['bush_len']:.3f} long | Sleeve option of "
          f"[D16](decisions.md) (open) |")
    print(f"| Shaft journal, diametral clearance | {dr['journal']:.4f}, {dr['bush_clearance']:.4f} | — |")
    print(f"| Bushing centres apart; inner hub centre beyond the rear bushing | {dr['bush_span']:.3f}, "
          f"{dr['hub_overhang']:.3f} | For step 5 (bearing load) |")
    print(f"| Containment can | ID {2 * dr['can_ri']:.3f}, OD {2 * dr['can_ro']:.3f}, wall "
          f"{dr['can_ro'] - dr['can_ri']:.3f}, {'flat' if dr['can_flat_end'] else 'curved'} end "
          f"{dr['can_end_t']:.3f} thick, flange {dr['can_flange_t']:.3f} | Material open "
          f"([Q28](open-questions.md)) |")
    print(f"| Inner magnet hub | OD {dr['inner_od']:.3f}, Y {dr['inner_y'][0]:.2f} to {dr['inner_y'][1]:.2f} | "
          f"Magnets not drawn |")
    print(f"| Outer magnet hub bore | {dr['outer_bore']:.3f}, Y {dr['outer_y'][0]:.2f} to {dr['outer_y'][1]:.2f} | "
          f"Magnets not drawn |")
    print(f"| Radial gaps: inner hub to can, can to outer hub, total | {dr['gap_inner']:.3f}, {dr['gap_outer']:.3f}, "
          f"{dr['gap_total']:.3f} | — |")
    print(f"| Axial overlap of the two hubs | {dr['magnet_overlap']:.3f} | — |")
    print(f"| Axial room at the can end: inside (to the inner hub), outside (to the outer hub) | "
          f"{dr['room_inside']:.3f}, {dr['room_outside']:.3f} | — |")
    print(f"| Motor face: pilot, bolt circle, shaft | {dr['pilot']:.3f}, {dr['bolt_circle']:.3f}, "
          f"{dr['motor_shaft']:.3f} | NEMA 56C: " + ", ".join(f"{k} {v:.3f}" for k, v in NEMA_56C.items()) + " |")

    print(f"\n### Containment can at the {st['p']:.0f} psig design pressure ([D32](decisions.md))\n")
    print(f"Wall {st['t']:.3f} in at mean radius {st['r_mean']:.3f} in; end {st['t_end']:.3f} in thick over radius "
          f"{st['a']:.3f} in. Compared with the {YIELD_316_PSI:,} psi minimum yield of annealed 316 stainless (check), "
          f"with no safety factor.\n")
    print("| Stress | psi | Times the 316 yield |")
    print("|---|---|---|")
    rows = [("Tube, hoop (p·r/t)", st["hoop"]), ("Tube, axial (p·r/2t)", st["axial"]),
            ("Flat end, edge held fixed (3pa²/4t²)", st["flat_clamped"]),
            ("Flat end, edge simply supported (3(3+ν)pa²/8t²), at the centre", st["flat_simple"]),
            (f"Hemispherical end of the same {st['t_end']:.3f} in (p·r/2t)", st["hemi"])]
    for label, s in rows:
        print(f"| {label} | {s:,.0f} | {s / YIELD_316_PSI:.2f} |")
    print(f"\nA flat end reaches the yield stress at {st['t_clamped']:.3f} in thick with a fixed edge, or "
          f"{st['t_simple']:.3f} in simply supported.")

    print("\n### Bolted joints\n")
    print("| Screw | Through | Hole dia | Holes | Screws placed |")
    print("|---|---|---|---|---|")
    for name, pname, d, holes, placed in fasteners(parts):
        print(f"| {name} | {pname} | {d:.3f} | {holes} | {placed} |")

    print("\n### Parts that share volume\n")
    print("| Parts | Pairs | in³ each | What it is |")
    print("|---|---|---|---|")
    found = overlaps(parts)
    for (names, kind), vols in sorted(found.items(), key=lambda kv: ("Clash" not in kv[0][1], kv[0][0])):
        print(f"| {names[0]} / {names[1]} | {len(vols)} | {max(vols):.5f} | {kind} |")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else STEP)
