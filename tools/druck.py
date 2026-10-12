"""Druckfertige STL-Dateien: je Teil alle Solids boolesch vereinigen, in Einzelkoerper zerlegen,
pruefen und flach auf das Druckbett legen.

  python tools/druck.py                 # alle druckbaren Teile bauen, docs/.../druck/*.stl + Bericht
  python tools/druck.py haube motor     # nur diese Teile
  (tools/build.py ruft exportiere() fuer jedes Teil auf)

Warum: Die CAD-Teile bestehen aus vielen einzeln modellierten Solids (Schrauben, Rippen, Rohre ...), die sich
absichtlich ueberschneiden oder 0,3 mm eingesenkt sind. Als einfacher STL-Export ist das ein Haufen sich
durchdringender Huellen, teils mit offenen Kanten an den Flaechengrenzen, und alles schwebt in Einbaulage.
Hier wird jedes Solid mit der Druck-Toleranz trianguliert, mit manifold3d vereinigt (Ergebnis garantiert
dicht und ohne Selbstueberschneidung), in zusammenhaengende Koerper zerlegt und jeder Koerper auf z = 0 gelegt.

Pruefungen je Koerper (Modell-mm):
  * dicht (geschlossen, mannigfaltig) - nach der Vereinigung immer, sonst Fehler
  * Volumen und kleinste Ausdehnung (zu kleine Koerper gehen beim Druck verloren)
  * Wandstaerke als Stichprobe: Strahlen von Oberflaechenpunkten nach innen, erster Treffer = lokale Dicke
  * Ueberhang: Anteil der nach unten zeigenden Flaeche steiler als 45 Grad, die nicht auf dem Bett liegt
"""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import manifold3d as mf
import trimesh

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

TOL, ANG = 0.02, 0.15          # Triangulierung fuer den Druck (Modell-mm, rad)
MIN_WAND = 0.5                 # duennste noch druckbare Stelle (FDM 0,4er Duese, Resin deutlich weniger)
WARN_WAND = 0.8
MIN_KOERPER = 1.0              # kleinste Ausdehnung eines Einzelkoerpers in mm
MIN_VOL = 0.05                 # kleinere Koerper sind Splitter aus der Vereinigung und werden verworfen
ABSTAND = 4.0                  # Abstand der Koerper auf dem Bett
REIHE = 220.0                  # Breite einer Reihe auf dem Bett (typisch 220 ... 256 mm)
PROBEN = 400                   # Strahlen je Koerper fuer die Wandstaerke


def _manifold_aus_solid(s):
    """build123d-Solid -> manifold3d.Manifold (oder None mit Grund)."""
    verts, tris = s.tessellate(TOL, ANG)
    if not tris:
        return None, "keine Dreiecke"
    v = np.array([[p.X, p.Y, p.Z] for p in verts], dtype=np.float32)
    t = np.array(tris, dtype=np.uint32)
    mesh = mf.Mesh(vert_properties=v, tri_verts=t)
    mesh.merge()                                    # gleiche Punkte an Flaechengrenzen zusammenfuehren
    m = mf.Manifold(mesh)
    if m.status() == mf.Error.NoError and m.volume() > 0:
        return m, None
    # Rettung: ueber trimesh reparieren (Punkte verschmelzen, Normalen, Loecher)
    tm = trimesh.Trimesh(v, t, process=True)
    tm.merge_vertices(digits_vertex=5)
    trimesh.repair.fix_normals(tm)
    trimesh.repair.fill_holes(tm)
    if tm.is_watertight:
        m = mf.Manifold(mf.Mesh(vert_properties=tm.vertices.astype(np.float32), tri_verts=tm.faces.astype(np.uint32)))
        if m.status() == mf.Error.NoError and m.volume() > 0:
            return m, "repariert"
    return None, f"nicht dicht ({m.status()})"


def _koerper_bereinigen(roh):
    """Zerlegung aufraeumen: Hohlraeume fuellen, eingeschlossene Teile und Splitter verwerfen.

    manifold3d.decompose() liefert die Innenflaeche eines eingeschlossenen Hohlraums als eigene Schale mit
    negativem Volumen. Diese Schalen werden weggelassen, damit ist der Hohlraum gefuellt (fuer den Druck
    besser: keine eingeschlossene Luft, keine duennen Innenwaende). Koerper, die danach ganz in einem
    groesseren Koerper liegen (frueher im Hohlraum), und Splitter unter MIN_VOL werden verworfen."""
    hinweise = []
    neg = [k for k in roh if k.volume() < 0]
    pos = sorted((k for k in roh if k.volume() > 0), key=lambda k: -k.volume())
    if neg:
        hinweise.append(f"{len(neg)} eingeschlossene Hohlraeume gefuellt")
    splitter = [k for k in pos if k.volume() < MIN_VOL]
    pos = [k for k in pos if k.volume() >= MIN_VOL]
    if splitter:
        hinweise.append(f"{len(splitter)} Splitter unter {MIN_VOL} mm3 verworfen")
    behalten, meshes = [], []
    for k in pos:
        lo, hi = np.array(k.bounding_box()[:3]), np.array(k.bounding_box()[3:])
        drin = False
        for g, gm in zip(behalten, meshes):
            glo, ghi = np.array(g.bounding_box()[:3]), np.array(g.bounding_box()[3:])
            if np.all(lo >= glo - 1e-3) and np.all(hi <= ghi + 1e-3):
                v = np.asarray(k.to_mesh().vert_properties)[:, :3]
                probe = v[np.linspace(0, len(v) - 1, min(len(v), 24)).astype(int)]
                if gm.contains(probe).all():
                    drin = True
                    break
        if drin:
            continue
        behalten.append(k)
        meshes.append(_trimesh(k))
    if len(behalten) < len(pos):
        hinweise.append(f"{len(pos) - len(behalten)} eingeschlossene Innenteile im gefuellten Hohlraum verworfen")
    return behalten, hinweise


def _trimesh(m):
    me = m.to_mesh()
    return trimesh.Trimesh(np.asarray(me.vert_properties)[:, :3], np.asarray(me.tri_verts), process=False)


def _wandstaerke(tm, n=PROBEN, seed=1):
    """Stichprobe der lokalen Wandstaerke (Strahl nach innen bis zur Gegenwand)."""
    if len(tm.faces) == 0:
        return None
    pts, fi = trimesh.sample.sample_surface(tm, n, seed=seed)
    nrm = tm.face_normals[fi]
    start = pts - nrm * 1e-3
    loc, idx_ray, _ = tm.ray.intersects_location(start, -nrm, multiple_hits=False)
    if len(idx_ray) == 0:
        return None
    d = np.full(n, np.nan)
    d[idx_ray] = np.linalg.norm(loc - start[idx_ray], axis=1)
    d = d[~np.isnan(d)]
    return d if len(d) else None


def _ueberhang(tm):
    """Anteil der Flaeche, die steiler als 45 Grad nach unten zeigt und nicht auf dem Bett liegt."""
    n = tm.face_normals
    a = tm.area_faces
    z = tm.triangles_center[:, 2]
    unten = (n[:, 2] < -math.cos(math.radians(45))) & (z > 0.05)
    return float(a[unten].sum() / max(a.sum(), 1e-9))


def _drehen(m, rot):
    rx, ry, rz = rot
    if rx:
        m = m.rotate((rx, 0, 0))
    if ry:
        m = m.rotate((0, ry, 0))
    if rz:
        m = m.rotate((0, 0, rz))
    return m


def manifolds(teil, comp):
    """Alle Solids eines Teils als manifold3d-Koerper (Modell-mm, Einbaulage) + Hinweise."""
    teile, probleme = [], []
    for i, s in enumerate(comp.solids()):
        m, grund = _manifold_aus_solid(s)
        if m is None:
            probleme.append(f"Solid {i}: {grund}, weggelassen")
        else:
            if grund:
                probleme.append(f"Solid {i}: {grund}")
            teile.append(m)
    if not teile:
        raise ValueError(f"{teil.id}: keine druckbaren Solids")
    return teile, probleme


def _bb(m):
    b = m.bounding_box()
    return np.array(b[:3]), np.array(b[3:])


def passung(eintraege):
    """Passung zwischen getrennt gedruckten Teilen.

    Im CAD greifen angesetzte Teile 0,3 mm (Modell) in ihr Gegenstueck (keine koplanaren Booleans, sichtbar
    geschlossene Fuge). Fuer den Druck waere das Uebermass: die Teile passen nicht buendig. Hier wird bei jeder
    Ueberschneidung zweier Solids aus verschiedenen Teilen das kleinere Solid um das groessere gekuerzt; danach
    liegen die Flaechen exakt aneinander. eintraege: Liste von dicts mit 'teil', 'mfs' (Liste), 'probleme'."""
    for e in eintraege:
        e["bbs"] = [_bb(m) for m in e["mfs"]]
        lo = np.min([b[0] for b in e["bbs"]], axis=0); hi = np.max([b[1] for b in e["bbs"]], axis=0)
        e["bb"] = (lo, hi)
    def schneiden(a, b, tol=0.0):
        return np.all(a[0] <= b[1] + tol) and np.all(b[0] <= a[1] + tol)
    for i, A in enumerate(eintraege):
        for B in eintraege[i + 1:]:
            if not schneiden(A["bb"], B["bb"]):
                continue
            n = 0
            for ia, ma in enumerate(A["mfs"]):
                for ib, mb in enumerate(B["mfs"]):
                    if not schneiden(A["bbs"][ia], B["bbs"][ib]):
                        continue
                    if (ma ^ mb).volume() < 1e-4:
                        continue
                    if ma.volume() <= mb.volume():
                        ma = ma - mb
                        A["mfs"][ia] = ma
                        A["bbs"][ia] = _bb(ma) if ma.volume() > 0 else A["bbs"][ia]
                    else:
                        mb = mb - ma
                        B["mfs"][ib] = mb
                        B["bbs"][ib] = _bb(mb) if mb.volume() > 0 else B["bbs"][ib]
                    n += 1
            if n:
                A["probleme"].append(f"Passung zu {B['teil'].id}: {n} Ansatzstellen buendig gekuerzt")
                B["probleme"].append(f"Passung zu {A['teil'].id}: {n} Ansatzstellen buendig gekuerzt")
    for e in eintraege:
        e["mfs"] = [m for m in e["mfs"] if m.volume() > 0]


def alle_exportieren(liste, ordner):
    """liste: [(teil, comp)] -> Passung untereinander, dann je Teil exportieren. Gibt Berichte zurueck."""
    eintraege = []
    for teil, comp in liste:
        mfs, pr = manifolds(teil, comp)
        eintraege.append({"teil": teil, "mfs": mfs, "probleme": pr})
    passung(eintraege)
    berichte = []
    for e in eintraege:
        b = exportiere(e["teil"], None, Path(ordner) / f"{e['teil'].id}.stl", mfs=e["mfs"], probleme=e["probleme"])
        berichte.append(b)
        print(f"  Druck {b['id']:20s} {b['solids']:5d} Solids -> {b['koerper']:4d} Koerper  dicht={b['dicht']}  "
              f"{len(b['probleme'])} Hinweise  {b['sekunden']}s")
    return berichte


def exportiere(teil, comp, ziel, mfs=None, probleme=None):
    """Vereinigt alle Solids (aus `comp` oder fertig als `mfs`), legt die Koerper aufs Bett, schreibt `ziel` (STL)."""
    t0 = time.time()
    if mfs is None:
        teile, probleme = manifolds(teil, comp)
    else:
        teile, probleme = mfs, list(probleme or [])
    ges = mf.Manifold.batch_boolean(teile, mf.OpType.Add)
    ges = _drehen(ges, getattr(teil, "druck_rot", (0, 0, 0)))
    koerper, hinweise = _koerper_bereinigen(ges.decompose())
    probleme += hinweise

    # Anordnung: Reihen von links nach rechts, jeder Koerper mit Unterseite auf z = 0
    platziert, berichte = [], []
    x = y = reihe_h = 0.0
    for k in koerper:
        lo, hi = np.array(k.bounding_box()[:3]), np.array(k.bounding_box()[3:])
        dx, dy = hi[0] - lo[0], hi[1] - lo[1]
        if x > 0 and x + dx > REIHE:
            x, y, reihe_h = 0.0, y + reihe_h + ABSTAND, 0.0
        k2 = k.translate((x - lo[0], y - lo[1], -lo[2]))
        platziert.append(k2)
        x += dx + ABSTAND
        reihe_h = max(reihe_h, dy)
        tm = _trimesh(k2)
        ext = hi - lo
        w = _wandstaerke(tm)
        mitte = (lo + hi) / 2                              # Lage im zusammengebauten Modell (Original-mm)
        b = {
            "ort_original_mm": [round(float(mitte[0]) * 8), round(float(mitte[1]) * 8), round(float(mitte[2]) * 8 + 392)],
            "volumen_mm3": round(k.volume(), 2),
            "masse_mm": [round(float(e), 1) for e in ext],
            "dicht": bool(tm.is_watertight),
            "wand_min": round(float(w.min()), 2) if w is not None else None,
            "wand_p02": round(float(np.percentile(w, 2)), 2) if w is not None else None,
            "wand_unter_min": int((w < MIN_WAND).sum()) if w is not None else 0,
            "proben": int(len(w)) if w is not None else 0,
            "ueberhang": round(_ueberhang(tm), 3),
        }
        if not b["dicht"]:
            probleme.append(f"Koerper {len(berichte)} nicht dicht")
        if ext.min() < MIN_KOERPER:
            probleme.append(f"Koerper {len(berichte)} sehr klein ({ext.min():.2f} mm, {k.volume():.2f} mm3) bei x/y/z "
                            f"{b['ort_original_mm']} Original-mm, geht beim Druck evtl. verloren")
        if w is not None and b["wand_unter_min"] > max(2, 0.05 * len(w)):
            probleme.append(f"Koerper {len(berichte)} (bei {b['ort_original_mm']}): {b['wand_unter_min']}/{len(w)} Proben duenner als {MIN_WAND} mm")
        berichte.append(b)

    bett = mf.Manifold.batch_boolean(platziert, mf.OpType.Add) if len(platziert) > 1 else platziert[0]
    tm = _trimesh(bett)
    tm.export(str(ziel))
    lo, hi = tm.bounds
    return {
        "id": teil.id, "solids": len(teile), "koerper": len(koerper),
        "dicht": bool(tm.is_watertight), "bett_mm": [round(float(v), 1) for v in (hi - lo)],
        "volumen_mm3": round(float(tm.volume), 1), "dreiecke": int(len(tm.faces)),
        "probleme": probleme, "koerper_liste": berichte, "sekunden": round(time.time() - t0, 1),
    }


def bericht_md(berichte, pfad):
    z = ["# Druckpruefung", "",
         f"Je Teil vereinigt (manifold3d), in Einzelkoerper zerlegt, flach aufs Bett gelegt. Masse in Modell-mm (1:8). "
         f"Wandstaerke als Stichprobe ({PROBEN} Strahlen je Koerper), Grenze {MIN_WAND} mm, Warnung unter {WARN_WAND} mm. "
         f"Ueberhang = Flaechenanteil steiler als 45 Grad nach unten (braucht Stuetzen).", "",
         "| Teil | Solids | Koerper | dicht | Bettflaeche x × y × z | Volumen mm³ | duennste Probe | Ueberhang max | Probleme |",
         "|---|---:|---:|---|---|---:|---:|---:|---:|"]
    for b in berichte:
        wm = [k["wand_min"] for k in b["koerper_liste"] if k["wand_min"] is not None]
        uh = max((k["ueberhang"] for k in b["koerper_liste"]), default=0)
        z.append(f"| {b['id']} | {b['solids']} | {b['koerper']} | {'ja' if b['dicht'] else 'NEIN'} | "
                 f"{' × '.join(str(v) for v in b['bett_mm'])} | {b['volumen_mm3']} | {min(wm) if wm else '-'} | "
                 f"{uh:.0%} | {len(b['probleme'])} |")
    for b in berichte:
        if b["probleme"]:
            z += ["", f"## {b['id']}", ""] + [f"- {p}" for p in b["probleme"]]
    Path(pfad).write_text("\n".join(z) + "\n", encoding="utf-8")


def main(argv):
    from cad.modell import TEILE, INFO
    from build123d import Compound
    nur = [a for a in argv if not a.startswith("--")]
    ziel = ROOT / "docs" / "modelle" / INFO["id"] / "druck"
    ziel.mkdir(parents=True, exist_ok=True)
    liste = [(t, Compound(children=list(t.bauen().values()))) for t in TEILE
             if t.druck and (not nur or t.id in nur)]
    if nur:
        print("Hinweis: Passung nur zwischen den angegebenen Teilen; fuer die endgueltigen Dateien alle Teile bauen.")
    berichte = alle_exportieren(liste, ziel)
    (ROOT / "out").mkdir(exist_ok=True)
    bericht_md(berichte, ROOT / "out" / "druckpruefung.md")
    (ROOT / "out" / "druckpruefung.json").write_text(json.dumps(berichte, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Bericht: out/druckpruefung.md")


if __name__ == "__main__":
    main(sys.argv[1:])
