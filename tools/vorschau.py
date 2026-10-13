"""Einzelne Teile bauen, pruefen und mit dem Rest des Modells als Kontext rendern.

  python tools/vorschau.py laufwerk_links kette_links            # baut diese Teile neu
  python tools/vorschau.py laufwerk_links --out out/lw             # Zielordner fuer PNGs
  python tools/vorschau.py laufwerk_links --ohne-kontext            # nur das Teil
  python tools/vorschau.py laufwerk_links --kontext rumpf,haube     # nur diese Teile als Kontext

Schreibt NICHT nach docs/ (kein Konflikt mit anderen Baustellen). Die neu gebauten Teile
liegen als STL im Zielordner, der Kontext kommt aus docs/modelle/<id>/ansicht/*.stl.
Ausgabe: <out>/<teil>__<material>.stl, <out>/<ansicht>.png, Pruefbericht auf stdout.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pyvista as pv  # noqa: E402
from build123d import Compound, export_stl  # noqa: E402

from cad.modell import INFO, TEILE  # noqa: E402

MODELL = ROOT / "docs" / "modelle" / INFO["id"]


def bauen(ids: set[str], out: Path) -> dict[tuple[str, str], Path]:
    """Baut die Teile, prueft die Solids und schreibt je Material eine STL; Rueckgabe {(teil, material): Pfad}."""
    out.mkdir(parents=True, exist_ok=True)
    neu = {}
    for t in TEILE:
        if t.id not in ids:
            continue
        t0 = time.time()
        schichten = t.bauen()
        fehler = []
        for mat, comp in schichten.items():
            solids = comp.solids()
            if not comp.is_valid:
                fehler.append(f"{mat}: Compound ungueltig")
            for i, s in enumerate(solids):
                if not s.is_valid:
                    fehler.append(f"{mat}: Solid {i} ungueltig")
                if s.volume < 1e-4:
                    fehler.append(f"{mat}: Solid {i} Volumen ~0")
            for f in out.glob(f"{t.id}__{mat}.stl"):
                f.unlink()
            export_stl(comp, str(out / f"{t.id}__{mat}.stl"), tolerance=0.05, angular_tolerance=0.25)
            neu[(t.id, mat)] = out / f"{t.id}__{mat}.stl"
        c = Compound(children=list(schichten.values()))
        bb = c.bounding_box()
        n_solids = sum(len(x.solids()) for x in schichten.values())
        print(f"{t.id:22s} bbox Modell-mm [{bb.min.X:7.1f}..{bb.max.X:7.1f}] "
              f"[{bb.min.Y:7.1f}..{bb.max.Y:7.1f}] [{bb.min.Z:7.1f}..{bb.max.Z:7.1f}]  "
              f"{n_solids} Solids  {time.time() - t0:5.1f}s")
        print(f"{'':22s} Original-mm x {bb.min.X*8:7.0f}..{bb.max.X*8:7.0f}  "
              f"y {bb.min.Y*8:7.0f}..{bb.max.Y*8:7.0f}  "
              f"z {(bb.min.Z-INFO['boden_z'])*8:7.0f}..{(bb.max.Z-INFO['boden_z'])*8:7.0f}")
        for f in fehler:
            print("   FEHLER:", f)
    return neu


def rendern(ids: set[str], neu: dict[tuple[str, str], Path], out: Path, kontext: set[str] | None, ansichten: list[str]) -> None:
    """Rendert die neuen Teile (deckend) mit dem Rest des Modells als Kontext (transparent)."""
    info = json.loads((MODELL / "modell.json").read_text(encoding="utf-8"))
    pal = info["materialien"]
    meshes = []
    for t in info["teile"]:
        if t["id"] in ids:
            continue
        if kontext is not None and t["id"] not in kontext:
            continue
        for sch in t["schichten"]:
            p = MODELL / sch["ansicht"]
            if p.exists():
                meshes.append((pv.read(p), pal[sch["material"]], False))
    for (_tid, mat), p in neu.items():
        meshes.append((pv.read(p), pal.get(mat, {"farbe": "#ff00ff", "metall": 0, "rauheit": 0.5}), True))
    if not meshes:
        return
    eigene = [m for m, _, n in meshes if n]
    if eigene:
        b = [m.bounds for m in eigene]
        bb = [min(x[0] for x in b), max(x[1] for x in b), min(x[2] for x in b),
              max(x[3] for x in b), min(x[4] for x in b), max(x[5] for x in b)]
    else:
        bb = meshes[0][0].bounds
    cx, cy, cz = (bb[0] + bb[1]) / 2, (bb[2] + bb[3]) / 2, (bb[4] + bb[5]) / 2
    diag = max(1.0, ((bb[1] - bb[0]) ** 2 + (bb[3] - bb[2]) ** 2 + (bb[5] - bb[4]) ** 2) ** 0.5)
    d = diag * 1.6
    views = {
        "iso_vl": ((cx - d * .7, cy - d * .7, cz + d * .45), (cx, cy, cz), (0, 0, 1)),
        "iso_hr": ((cx + d * .7, cy + d * .7, cz + d * .45), (cx, cy, cz), (0, 0, 1)),
        "links": ((cx, cy - d, cz), (cx, cy, cz), (0, 0, 1)),
        "rechts": ((cx, cy + d, cz), (cx, cy, cz), (0, 0, 1)),
        "vorn": ((cx - d, cy, cz), (cx, cy, cz), (0, 0, 1)),
        "hinten": ((cx + d, cy, cz), (cx, cy, cz), (0, 0, 1)),
        "oben": ((cx, cy, cz + d), (cx, cy, cz), (1, 0, 0)),
        "unten": ((cx, cy, cz - d), (cx, cy, cz), (1, 0, 0)),
    }
    for name in ansichten:
        pl = pv.Plotter(off_screen=True, window_size=(1400, 1000))
        pl.set_background("white")
        for m, mt, eigen in meshes:
            pl.add_mesh(m, color=mt["farbe"], opacity=0.25 if (not eigen and eigene) else mt.get("deckkraft", 1.0),
                        pbr=False, smooth_shading=False, specular=0.3, ambient=0.25, diffuse=0.8)
        pl.camera_position = views[name]
        if name in ("links", "rechts", "vorn", "hinten", "oben", "unten"):
            pl.enable_parallel_projection()
            pl.reset_camera(bounds=bb)
            pl.camera.zoom(1.3)
        pl.enable_anti_aliasing("ssaa")
        pl.screenshot(out / f"{name}.png")
        pl.close()
        print("ok", out / f"{name}.png")


def main(argv: list[str]) -> None:
    """Kommandozeile siehe Modul-Docstring."""
    optionen_mit_wert = ("--out", "--kontext", "--ansichten")
    ids = [a for i, a in enumerate(argv) if not a.startswith("--") and not (i > 0 and argv[i - 1] in optionen_mit_wert)]
    out = ROOT / "out" / "vorschau"
    kontext = None
    ansichten = ["iso_vl", "iso_hr", "links", "vorn", "oben"]
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
        if not out.is_absolute():
            out = ROOT / out
    if "--kontext" in argv:
        kontext = set(argv[argv.index("--kontext") + 1].split(","))
    if "--ohne-kontext" in argv:
        kontext = set()
    if "--ansichten" in argv:
        ansichten = argv[argv.index("--ansichten") + 1].split(",")
    bekannt = {t.id for t in TEILE}
    for i in ids:
        if i not in bekannt:
            sys.exit(f"unbekanntes Teil {i!r}; bekannt: {sorted(bekannt)}")
    neu = bauen(set(ids), out)
    rendern(set(ids), neu, out, kontext, ansichten)


if __name__ == "__main__":
    main(sys.argv[1:])
