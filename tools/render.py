"""Vorschaubilder aus docs/modelle/<id>/ansicht/*.stl

  python tools/render.py                 # alle Ansichten nach out/
  python tools/render.py --vorschau      # zusaetzlich docs/.../vorschau.png
  python tools/render.py seite detail_motor
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pyvista as pv

ROOT = Path(__file__).resolve().parents[1]
MODELL = ROOT / "docs" / "modelle" / "hanomag-k55e"
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

C = (130, 0, 40)
VIEWS = {
    "schraeg_vorn": [(-430, -400, 300), C, (0, 0, 1)],
    "schraeg_hinten": [(660, 400, 330), C, (0, 0, 1)],
    "seite": [(130, -900, 40), C, (0, 0, 1)],
    "vorn": [(-900, 0, 40), (0, 0, 40), (0, 0, 1)],
    "oben": [(130, 0, 900), C, (1, 0, 0)],
    "detail_motor": [(60, -330, 130), (90, 0, 60), (0, 0, 1)],
    "detail_laufwerk": [(120, -330, 10), (160, -80, -10), (0, 0, 1)],
    "detail_fahrerstand": [(420, -230, 260), (240, 0, 90), (0, 0, 1)],
}
PARALLEL = {"seite", "vorn", "oben"}


def main(argv: list[str]) -> None:
    """Rendert die genannten (sonst alle) Ansichten nach out/."""
    info = json.loads((MODELL / "modell.json").read_text(encoding="utf-8"))
    pal = info["materialien"]
    meshes = [(pv.read(MODELL / sch["ansicht"]), pal[sch["material"]])
              for t in info["teile"] for sch in t["schichten"]]
    namen = [a for a in argv if not a.startswith("--")] or list(VIEWS)
    for name in namen:
        pl = pv.Plotter(off_screen=True, window_size=(1400, 1000))
        pl.set_background("white")
        for m, mt in meshes:
            # flaches Shading: STL-Flaechennormalen, keine Interpolation ueber grosse Dreiecke
            pl.add_mesh(m, color=mt["farbe"], opacity=mt.get("deckkraft", 1.0), pbr=True,
                        metallic=mt["metall"] * 0.6, roughness=mt["rauheit"], smooth_shading=False)
        pl.camera_position = VIEWS[name]
        if name in PARALLEL:
            pl.enable_parallel_projection()
            pl.reset_camera()
            pl.camera.zoom(1.25)
        pl.enable_anti_aliasing("ssaa")
        pl.screenshot(OUT / f"{name}.png")
        if name == "schraeg_vorn" and "--vorschau" in argv:
            pl.window_size = (1200, 800)
            pl.screenshot(MODELL / "vorschau.png")
        pl.close()
        print("ok", name)


if __name__ == "__main__":
    main(sys.argv[1:])
