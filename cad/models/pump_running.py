"""The team's pump assembly (Onshape, 2026-11-19), running.

Reads the assembly STEP in cad/ and adds the mechanism: the shaft, rotor, keys and inner magnet hub turn as one; the
outer magnet hub turns with them through the magnetic coupling (1:1, slip ignored); each vane slides in its slot so
its tip stays on the cam ring bore. The motor is drawn as one solid, so only the outer hub turns on the motor side.

The vanes are radial, and the STEP draws them all pushed in. Here each vane is placed where its 0.25 in tip radius
touches the ring: the tip centre sits R_bore - r_tip from the ring centre. Ring, rotor and vane sizes are measured
from the STEP, as calcs/cad_check.py measures them.

Direction of turn: counterclockwise seen from the front cover (-Y), so the chambers grow on the -X side. That follows
the working assumption of Q34, that the -X housing port is the inlet. Set TURN to +1 to reverse it if the team
says otherwise.

The motion "running" is one revolution in 3 s, 1/180 of real speed (3600 RPM). Two models:

- pump_running: the whole assembly.
- pump_running_open: the front cover, front end plate, front bushing and cover screws left off, to look into the
  pumping element from the front.

Play the motion on each model's page (the view: link the run prints). With --gif, the run also draws one turn of the
open model from the front into docs/figures/pump_running.gif (frames in tmp/, about 10 s).

    cad run cad/models/pump_running.py [--gif]
"""
import math
import json
import subprocess
import sys
from pathlib import Path

import build123d as bd
from cad import model, step
from cad.build123d import configuration_sequence, gear_pair, leaves, mechanism_state

HERE = Path(__file__).resolve().parent
STEP = HERE / ".." / "2026-11-19__Mag_pump_assembly.step"

TURN = -1                    # -1: counterclockwise from the front cover (Q34 working assumption)
REV_SECONDS = 3.0            # one revolution of the animation
STEP_DEG = 2                 # waypoint spacing; linear between them

ROTATING = {"08 Shaft", "06 Rotor", "15a Rotor Key", "15b Hub Key", "10 Inner Magnet Hub"}
FRONT = {"02 Front Cover", "03 Front End Plate", "Socket head cap screw with low head 5/16-18 x 1.25"}

COLOURS = {
    "01 Housing": "#b9bec5",
    "02 Front Cover": "#c8ccd2",
    "03 Front End Plate": "#a3aab3",
    "05 Rear End Plate": "#a3aab3",
    "04 Cam Ring": "#6f7883",
    "06 Rotor": "#3f6fb0",
    "07 Vane": "#e8892c",
    "08 Shaft": "#59636e",
    "09 Bushing": "#2f3338",
    "10 Inner Magnet Hub": "#7d5ba6",
    "12 Outer Magnet Hub": "#7d5ba6",
    "11 Containment CAN": "#d6c08a",
    "13 Motor Adapter": "#b9bec5",
    "14 Motor": "#3b4048",
    "15a Rotor Key": "#59636e",
    "15b Hub Key": "#59636e",
}
FASTENER_COLOUR = "#2b2e33"


def onshape_name(label):
    """Onshape names reach the file with "_" for spaces and for the point in "1.5"."""
    out = []
    for i, ch in enumerate(label):
        if ch == "_" and 0 < i < len(label) - 1 and label[i - 1].isdigit() and label[i + 1].isdigit():
            out.append(".")
        else:
            out.append(" " if ch == "_" else ch)
    return "".join(out)


def cylinders_along_y(solid):
    """(radius, x, z) of each cylindrical face whose axis runs along Y, in mm."""
    out = []
    for f in solid.faces():
        if f.geom_type != bd.GeomType.CYLINDER:
            continue
        circles = [e for e in f.edges() if e.geom_type == bd.GeomType.CIRCLE]
        if circles and abs(abs(circles[0].normal().Y) - 1) < 1e-6:     # its end circles face Y
            c = circles[0].arc_center
            out.append((circles[0].radius, c.X, c.Z))
    return out


def snap(v):
    return 0.0 if abs(v) < 1e-9 else v


def tip_centre_radius(theta, ring_x, ring_z, reach):
    """Distance from the rotor axis, along the radial line at theta (degrees from +Z towards +X), to the centre of a
    vane tip that touches the ring bore. reach = R_bore - r_tip."""
    ux, uz = math.sin(math.radians(theta)), math.cos(math.radians(theta))
    uc = ux * ring_x + uz * ring_z
    return uc + math.sqrt(reach**2 - (ring_x**2 + ring_z**2) + uc**2)


def running_pump(open_front):
    tree = step.read(STEP)
    parts = []
    by_name = {}
    for leaf in leaves(tree):
        name = onshape_name(leaf.label)
        if open_front and (name in FRONT or (name == "09 Bushing" and leaf.center().Y < 0)):
            continue
        leaf.color = COLOURS.get(name, FASTENER_COLOUR)
        parts.append(leaf)
        by_name.setdefault(name, []).append(leaf)

    def one(name):
        (part,) = by_name[name]
        return part

    housing, rotor, ring, shaft = one("01 Housing"), one("06 Rotor"), one("04 Cam Ring"), one("08 Shaft")
    motor, outer_hub = one("14 Motor"), one("12 Outer Magnet Hub")

    # Pumping element, measured
    r_rotor = max(r for r, x, z in cylinders_along_y(rotor) if math.hypot(x, z) < 1e-3)
    r_bore, ring_x, ring_z = max((c for c in cylinders_along_y(ring) if math.hypot(c[1], c[2]) > 1e-3
                                  and c[0] > r_rotor), key=lambda c: c[0])
    vanes = by_name["07 Vane"]
    r_tip, *_ = cylinders_along_y(vanes[0])[0]
    reach = r_bore - r_tip

    # Shaft group turns about Y; the outer hub turns with it through the coupling
    axis = bd.Axis((0, 0, 0), (0, 1, 0))
    shaft_joint = bd.RevoluteJoint("shaft", housing, axis=axis, angular_range=(-360, 360))
    bd.RigidJoint("shaft", shaft, shaft_joint.location)
    shaft_joint.connect_to(shaft.joints["shaft"], angle=0)
    for name in sorted(ROTATING - {"08 Shaft"}):
        part = one(name)
        label = "fix_" + name.split()[0]
        bd.RigidJoint(label, shaft, bd.Location())
        bd.RigidJoint(label, part, bd.Location())
        shaft.joints[label].connect_to(part.joints[label])

    motor_joint = bd.RevoluteJoint("motor", motor, axis=axis, angular_range=(-360, 360))
    bd.RigidJoint("motor", outer_hub, motor_joint.location)
    motor_joint.connect_to(outer_hub.joints["motor"], angle=0)

    # Vanes slide along their radial slots; numbered from the top towards +X
    slides = []
    for vane in vanes:
        c = vane.center()
        theta0 = math.degrees(math.atan2(c.X, c.Z)) % 360
        slides.append((theta0, vane))
    slides.sort(key=lambda s: s[0])
    vane_poses = []
    for i, (theta0, vane) in enumerate(slides, start=1):
        _, tx, tz = cylinders_along_y(vane)[0]
        drawn = math.hypot(tx, tz)                    # tip centre radius as the STEP draws it
        u = (snap(math.sin(math.radians(theta0))), 0.0, snap(math.cos(math.radians(theta0))))
        label = f"vane_{i}"
        slide = bd.Axis((tx, 0, tz), u)
        stroke = 2 * math.hypot(ring_x, ring_z)       # 2e
        guide = bd.LinearJoint(label, rotor, axis=slide, linear_range=(-1.0, stroke + 1.0))
        # The STEP places the rotor turned about Y, so the vane's frame takes the rotor's orientation
        bd.RigidJoint(label, vane, rotor.location * bd.Location(guide.relative_axis.position))
        as_built = tip_centre_radius(theta0, ring_x, ring_z, reach) - drawn
        rotor.joints[label].connect_to(vane.joints[label], position=as_built)
        vane_poses.append((label, theta0, drawn))
        vane.label = label

    pump = bd.Compound(children=parts, label="pump")
    gear_pair(pump, "drive", shaft=1.0, motor=1.0)    # the magnetic coupling: synchronous, slip ignored

    def pose(angle):
        values = {"drive": angle}
        for label, theta0, drawn in vane_poses:
            values[label] = tip_centre_radius(theta0 + angle, ring_x, ring_z, reach) - drawn
        return values

    steps = 360 // STEP_DEG
    waypoints = [(REV_SECONDS * k / steps, pose(TURN * STEP_DEG * k)) for k in range(steps + 1)]
    mechanism_state(pump, "quarter_turn", **pose(TURN * 90))
    return configuration_sequence(pump, "running", waypoints, ease="linear")


@model
def pump_running():
    return running_pump(open_front=False)


@model
def pump_running_open():
    return running_pump(open_front=True)


def draw_gif(doc, frames=45):
    """One turn of the open model, from the front, as a looping GIF with its labels."""
    from PIL import Image, ImageDraw, ImageFont

    root = HERE.parent.parent
    tmp = root / "tmp" / "pump_running_frames"
    tmp.mkdir(parents=True, exist_ok=True)
    jobs = [{"input": doc.id, "camera": "front", "jointValues": f"running@{REV_SECONDS * k / frames:.4f}",
             "outputs": [{"path": str(tmp / f"f{k:02d}.png"), "width": 900, "height": 900}]}
            for k in range(frames)]
    (tmp / "jobs.json").write_text(json.dumps(jobs))
    subprocess.run(["cad", "model", "snapshot", "--job", str(tmp / "jobs.json")], check=True, capture_output=True)

    font, small = ImageFont.load_default(size=21), ImageFont.load_default(size=16)
    dark, grey = (40, 44, 52), (90, 96, 106)
    out = []
    for k in range(frames):
        pic = Image.open(tmp / f"f{k:02d}.png").convert("RGB").resize((560, 560), Image.LANCZOS)
        im = Image.new("RGB", (560, 664), (240, 243, 247))
        im.paste(pic, (0, 70))
        d = ImageDraw.Draw(im)
        d.text((12, 10), "Team CAD 2026-11-19, seen from the front", fill=dark, font=font)
        d.text((12, 40), "Cover and end plate off. 1/180 speed. Direction assumed (Q34)", fill=grey, font=small)
        d.text((12, 634), "inlet (-X)", fill=dark, font=font)
        d.text((430, 634), "outlet (+X)", fill=dark, font=font)
        out.append(im.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE))
    gif = root / "docs" / "figures" / "pump_running.gif"
    out[0].save(gif, save_all=True, append_images=out[1:], duration=int(1000 * REV_SECONDS / frames), loop=0,
                optimize=True)
    print(f"wrote {gif.relative_to(root)}")


if __name__ == "__main__":
    pump_running()
    opened = pump_running_open()
    if "--gif" in sys.argv:
        draw_gif(opened)
