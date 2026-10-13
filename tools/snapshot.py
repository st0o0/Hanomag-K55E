"""Geometrie-Snapshot der gebauten Ansicht-STLs fuer Regressionsvergleiche (z. B. vor/nach einem Refactoring).

  python tools/snapshot.py save out/snapshot_vorher.json
  python tools/snapshot.py diff out/snapshot_vorher.json [--tol 0.01]
  python tools/snapshot.py diff out/snapshot_vorher.json --quelle out/vorschau_x   # STLs aus vorschau.py statt docs/

Erfasst je Teil und Material Volumen, Oberflaeche und Bounding-Box der STL in docs/modelle/<id>/ansicht/.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pyvista as pv

ROOT = Path(__file__).resolve().parents[1]
MODELL = ROOT / "docs" / "modelle" / "hanomag-k55e"


def erfassen(quelle: Path | None = None) -> dict[str, dict[str, float | list[float]]]:
    """Kennwerte aller Schichten; liegt in `quelle` eine STL <teil>__<material>.stl (vorschau.py), wird diese genommen."""
    info = json.loads((MODELL / "modell.json").read_text(encoding="utf-8"))
    werte: dict[str, dict[str, float | list[float]]] = {}
    for teil in info["teile"]:
        for schicht in teil["schichten"]:
            pfad = MODELL / schicht["ansicht"]
            if quelle is not None and (quelle / f"{teil['id']}__{schicht['material']}.stl").exists():
                pfad = quelle / f"{teil['id']}__{schicht['material']}.stl"
            mesh = pv.read(pfad)
            werte[f"{teil['id']}/{schicht['material']}"] = {
                "volumen": round(abs(mesh.volume), 3),
                "flaeche": round(mesh.area, 3),
                "bbox": [round(v, 3) for v in mesh.bounds],
            }
    return werte


def vergleichen(alt: dict, neu: dict, tol: float) -> int:
    """Gibt Abweichungen aus und liefert ihre Anzahl."""
    abweichungen = 0
    for key in sorted(set(alt) | set(neu)):
        if key not in alt or key not in neu:
            print(f"{'NEU ' if key in neu else 'WEG '} {key}")
            abweichungen += 1
            continue
        a, n = alt[key], neu[key]
        dv = abs(n["volumen"] - a["volumen"]) / max(a["volumen"], 1e-9)
        db = max(abs(x - y) for x, y in zip(a["bbox"], n["bbox"], strict=True))
        if dv > tol or db > tol * 10:
            print(f"DIFF {key}: Volumen {a['volumen']} -> {n['volumen']} ({dv:.2%}), bbox max. {db:.3f} mm")
            abweichungen += 1
    print("keine Abweichungen" if not abweichungen else f"{abweichungen} Abweichung(en)")
    return abweichungen


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("modus", choices=("save", "diff"))
    p.add_argument("datei", type=Path)
    p.add_argument("--tol", type=float, default=0.01, help="relative Volumentoleranz (bbox: 10x in Modell-mm)")
    p.add_argument("--quelle", type=Path, help="Ordner mit STLs aus tools/vorschau.py (ersetzt docs/-Dateien gleichen Namens)")
    args = p.parse_args(argv)
    werte = erfassen(args.quelle)
    if args.modus == "save":
        args.datei.parent.mkdir(parents=True, exist_ok=True)
        args.datei.write_text(json.dumps(werte, indent=1), encoding="utf-8")
        print(f"{len(werte)} Schichten gespeichert -> {args.datei}")
        return 0
    return 1 if vergleichen(json.loads(args.datei.read_text(encoding="utf-8")), werte, args.tol) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
