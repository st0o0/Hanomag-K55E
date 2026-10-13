"""Baut alle Teile und schreibt die Dateien fuer die Web-App.

  python tools/build.py              # alles
  python tools/build.py motor haube  # nur diese Teile (Steckbrief wird aktualisiert)
  python tools/build.py --ohne-step

Ausgabe: docs/modelle/<id>/{ansicht,druck}/*.stl, <id>_1-8.step.zip, modell.json
"""
from __future__ import annotations

import json
import sys
import time
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build123d import Compound, export_step, export_stl  # noqa: E402

import druck  # noqa: E402  (tools/druck.py: druckfertige STLs)
from cad.modell import INFO, TEILE  # noqa: E402

ZIEL = ROOT / "docs" / "modelle" / INFO["id"]
ANSICHT, DRUCK = ZIEL / "ansicht", ZIEL / "druck"


def main(argv: list[str]) -> None:
    """Kommandozeile: Teile bauen und Web-App-Dateien schreiben."""
    nur = [a for a in argv if not a.startswith("--")]
    ohne_step = "--ohne-step" in argv
    for d in (ANSICHT, DRUCK):
        d.mkdir(parents=True, exist_ok=True)

    alt = {}
    mf = ZIEL / "modell.json"
    if mf.exists():
        alt = {t["id"]: t for t in json.loads(mf.read_text(encoding="utf-8")).get("teile", [])}

    if not nur:                                       # veraltete Ansichtsdateien entfernen
        for f in ANSICHT.glob("*.stl"):
            f.unlink()

    eintraege, alle, druckliste = [], [], []
    for t in TEILE:
        if nur and t.id not in nur:
            if t.id in alt:
                eintraege.append(alt[t.id])
            continue
        t0 = time.time()
        schichten = t.bauen()                          # {material: Compound}
        for f in ANSICHT.glob(f"{t.id}__*.stl"):
            f.unlink()
        liste = []
        for mat, comp in schichten.items():
            datei = f"ansicht/{t.id}__{mat}.stl"
            export_stl(comp, str(ZIEL / datei), tolerance=0.08, angular_tolerance=0.3)
            liste.append({"material": mat, "ansicht": datei})
        c = Compound(children=list(schichten.values()))
        alle.append(c)
        if t.druck:
            druckliste.append((t, c))
        bb = c.bounding_box()
        e = {
            "id": t.id, "name": t.name, "gruppe": t.gruppe, "material": t.material,
            "hinweis": t.hinweis, "explode": list(t.explode),
            "schichten": liste,
            "druck": f"druck/{t.id}.stl" if t.druck else None,
            "druck_mb": None,
            "masse_mm": [round(bb.size.X, 1), round(bb.size.Y, 1), round(bb.size.Z, 1)],
        }
        eintraege.append(e)
        print(f"{t.id:22s} {e['masse_mm']}  {time.time() - t0:5.1f}s")

    # Druckdateien: Passung zwischen den Teilen, vereinigt, dicht, flach aufs Bett gelegt (tools/druck.py)
    druckberichte = druck.alle_exportieren(druckliste, DRUCK) if druckliste else []
    for db in druckberichte:
        for e in eintraege:
            if e["id"] == db["id"]:
                e["druck_mb"] = round((DRUCK / f"{db['id']}.stl").stat().st_size / 1e6, 2)
                e["druck_koerper"] = len(db.get("koerper_liste") or []) or db["koerper"]   # Stuecke nach dem Teilen
                e["druck_bett_mm"] = db["bett_mm"]
                # Kurzfassung des Pruefberichts fuer die Druckansicht der App
                e["druck_pruefung"] = {
                    "dicht": db["dicht"],
                    "hinweise": [p for p in db["probleme"] if "repariert" not in p],
                    "koerper": [{"masse_mm": k["masse_mm"], "volumen_mm3": round(k["volumen_mm3"], 1),
                                 "wand_min": k.get("wand_min"), "ueberhang": k.get("ueberhang")}
                                for k in db.get("koerper_liste", [])],
                }
    if not nur:                                       # veraltete Druckdateien entfernen
        gueltig = {f"{t.id}.stl" for t in TEILE if t.druck}
        for f in DRUCK.glob("*.stl"):
            if f.name not in gueltig:
                f.unlink()
    if druckberichte:
        (ROOT / "out").mkdir(exist_ok=True)
        druck.bericht_md(druckberichte, ROOT / "out" / "druckpruefung.md")
        fehler = [d["id"] for d in druckberichte if not d["dicht"]]
        print("Druckpruefung: out/druckpruefung.md" + (f"  NICHT DICHT: {fehler}" if fehler else "  alle dicht"))

    step_name = f"{INFO['id']}_1-8.step"
    if not nur and not ohne_step:
        tmp = ZIEL / step_name
        export_step(Compound(children=alle), str(tmp))
        with zipfile.ZipFile(ZIEL / f"{step_name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            z.write(tmp, step_name)
        tmp.unlink()
        print("STEP", round((ZIEL / f"{step_name}.zip").stat().st_size / 1e6, 1), "MB (zip)")

    info = dict(INFO)
    info["teile"] = eintraege
    info["step"] = f"{step_name}.zip" if (ZIEL / f"{step_name}.zip").exists() else None
    info["vorschau"] = "vorschau.png" if (ZIEL / "vorschau.png").exists() else None
    info["stand"] = time.strftime("%Y-%m-%d")
    info["build"] = time.strftime("%Y%m%d%H%M%S")      # Cache-Schluessel fuer die App
    qf = ROOT / "referenz" / "quellen.json"                 # Quellenseite der Web-App
    if qf.exists():
        info["quellen"] = json.loads(qf.read_text(encoding="utf-8"))
    mf.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")

    idx = ROOT / "docs" / "modelle" / "index.json"
    liste = json.loads(idx.read_text(encoding="utf-8")) if idx.exists() else []
    liste = [x for x in liste if x["id"] != INFO["id"]]
    liste.append({"id": INFO["id"], "name": INFO["name"], "untertitel": INFO["untertitel"],
                  "massstab": INFO["massstab"], "vorschau": info["vorschau"]})
    idx.write_text(json.dumps(liste, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ok ->", ZIEL)


if __name__ == "__main__":
    main(sys.argv[1:])
