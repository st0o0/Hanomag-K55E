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

Aufteilen grosser Koerper (Bett BETT x BETT, Hoehe HOEHE; per Umgebungsvariable DRUCK_BETT=300 / DRUCK_HOEHE aenderbar):
Passt ein Koerper nicht (auch nicht um z gedreht), wird er mit achsparallelen Ebenen geschnitten - so wenige wie moeglich,
die Schnittlage mit kleinster Querschnittsflaeche nahe der Mitte. An jeder Schnittflaeche kommen 2 (bei kleiner Flaeche 1)
Passloecher Dm 2,0 x 4 mm Tiefe in BEIDE Haelften, nur wo rundum mindestens 1,2 mm Wand bleibt. Als Stifte dienen
1,75-mm-Filamentstuecke von 7,5 mm Laenge (Spiel 0,125 mm radial; ein gedruckter Stift von 1,8 mm waere zu schwach und
zu fein fuer FDM). Jedes Stueck wird mit der groessten Schnittflaeche nach unten gelegt, wenn das den Ueberhang nicht
deutlich verschlechtert.
"""
import json
import math
import os
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
MIN_SPLITTER = 5.0              # beim Teilen abgetrennte Splitter darunter (mm3, duenner als MIN_KOERPER) verwerfen
MIN_VOL = 0.05                 # kleinere Koerper sind Splitter aus der Vereinigung und werden verworfen
ABSTAND = 4.0                  # Abstand der Koerper auf dem Bett
BETT = float(os.environ.get("DRUCK_BETT", 220))     # Bettkante in mm (quadratisch); 300 fuer grosse Drucker
HOEHE = float(os.environ.get("DRUCK_HOEHE", 250))   # maximale Bauhoehe
MARGE = 1.0                    # Abstand zum Bettrand je Seite
REIHE = BETT                   # Breite einer Reihe auf dem Bett
PIN_D_LOCH, PIN_TIEFE, PIN_LAENGE = 2.0, 4.0, 7.5   # Passloch Dm / Tiefe je Haelfte; Stiftlaenge (1,75-mm-Filament)
KIPP_HOEHE = 100.0             # gekippt nur akzeptieren, wenn die Bauhoehe danach hoechstens so gross ist
KIPP_AUFLAGE = 0.15            # ... und die Auflageflaeche mindestens so viel der Huellen-Grundflaeche ausmacht
HOEHE_STRAFE = 0.003           # Bewertung der Drucklage: Ueberhang + HOEHE_STRAFE je mm Bauhoehe
PIN_WAND = 1.2                 # Mindestwand rund um ein Passloch
PIN_WAND_MIN = 0.9             # Notfall bei duennen Schnitten (Ketten): zwei 0,45er Perimeter
PROBEN = 1500                  # Strahlen je Koerper (hoechstens) fuer die Wandstaerke


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


def _wandstaerke(tm, n=None, seed=1):
    """Stichprobe der lokalen Wandstaerke. Strahl von der Oberflaeche entlang -Normale nach innen; gezaehlt wird der erste
    echte Austritt (Trefferflaeche mit fast entgegengesetzter Normale, cos >= 0,7). Streifende Treffer an Kanten und Ecken
    sowie schraege Austritte (Keilspitzen) werden verworfen.
    Gibt (Dicken, Punkte) zurueck oder (None, None)."""
    if len(tm.faces) == 0:
        return None, None
    if n is None:
        n = int(min(PROBEN, max(150, tm.area / 25)))
    pts, fi = trimesh.sample.sample_surface(tm, n, seed=seed)
    nrm = tm.face_normals[fi]
    start = pts - nrm * 2e-3
    loc, idx_ray, idx_tri = tm.ray.intersects_location(start, -nrm, multiple_hits=True)
    if len(idx_ray) == 0:
        return None, None
    dist = np.linalg.norm(loc - start[idx_ray], axis=1)
    cosw = np.einsum("ij,ij->i", tm.face_normals[idx_tri], -nrm[idx_ray])
    ordn = np.lexsort((dist, idx_ray))
    d_out, p_out = [], []
    letzt = -1
    for o in ordn:
        r = idx_ray[o]
        if r == letzt:
            continue
        if dist[o] < 5e-3 or cosw[o] <= 0:             # Selbsttreffer / Eintritt: naechster Treffer
            continue
        letzt = r
        if cosw[o] >= 0.7:
            d_out.append(dist[o] + 2e-3)
            p_out.append(pts[r])
    if not d_out:
        return None, None
    return np.array(d_out), np.array(p_out)


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


# ---------------------------------------------------------------- Aufteilen grosser Koerper

def _limits():
    L = BETT - 2 * MARGE
    return np.array([L, L, HOEHE])


def _bett_winkel(v, L):
    """Kleinster z-Drehwinkel (Grad, 2-Grad-Schritte), bei dem die xy-Ausdehnung der Punkte v in L x L passt, sonst None."""
    xy = v[:, :2]
    if len(xy) > 200:
        from scipy.spatial import ConvexHull
        xy = xy[ConvexHull(xy).vertices]
    for ang in range(0, 90, 2):
        a = math.radians(ang)
        c, s_ = math.cos(a), math.sin(a)
        x = xy[:, 0] * c - xy[:, 1] * s_
        y = xy[:, 0] * s_ + xy[:, 1] * c
        if np.ptp(x) <= L and np.ptp(y) <= L:
            return ang
    return None


def _passt(k):
    """Passt der Koerper (ggf. um z gedreht) in Bett x Hoehe?"""
    lo, hi = _bb(k)
    e = hi - lo
    lim = _limits()
    if e[2] > lim[2]:
        return False
    if e[0] <= lim[0] and e[1] <= lim[1]:
        return True
    if e.max() > lim[0] * 1.45:
        return False
    v = np.asarray(k.to_mesh().vert_properties)[:, :3]
    return _bett_winkel(v, lim[0]) is not None


def _perm(a):
    """3x4-Matrix, die Achse a nach z legt (zyklisch): neu = (alt[a+1], alt[a+2], alt[a])."""
    m = np.zeros((3, 4))
    m[0, (a + 1) % 3] = m[1, (a + 2) % 3] = m[2, a] = 1
    return m


def _punkt_in(poly_list, pts):
    """Gerade-ungerade-Regel fuer mehrere Konturen (Loecher inklusive)."""
    inside = np.zeros(len(pts), bool)
    for poly in poly_list:
        P = np.asarray(poly)
        x0, y0 = P[:, 0], P[:, 1]
        x1, y1 = np.roll(x0, -1), np.roll(y0, -1)
        for i in range(len(P)):
            if y0[i] == y1[i]:
                continue
            cond = (y0[i] > pts[:, 1]) != (y1[i] > pts[:, 1])
            xs = x0[i] + (pts[:, 1] - y0[i]) * (x1[i] - x0[i]) / (y1[i] - y0[i])
            inside ^= cond & (pts[:, 0] < xs)
    return inside


def _komponenten(m):
    """Zusammenhaengende Teile eines Manifolds (Splitter und negative Schalen weg), groesste zuerst."""
    return sorted((t for t in m.decompose() if t.volume() >= MIN_VOL), key=lambda t: -t.volume())


def _gut(k, ebenen=()):
    """Passt der Koerper ohne Schnitt aufs Bett? Niedrig (<= KIPP_HOEHE) in Einbaulage/Kipplage, sonst in einer stabilen
    Lage bis HOEHE (auch Einbaulage, wenn sie stabil steht). Hohe Koerper brauchen eine stabile Auflage."""
    lo, hi = _bb(k)
    if hi[2] - lo[2] <= KIPP_HOEHE and _passt(k):
        return True
    if _beste_lage(k, list(ebenen), HOEHE, streng=True) is not None:
        return True
    # Einbaulage ohne gute Auflage: trotzdem nicht schneiden, solange der Koerper nicht schlank/hochkant ist
    return _passt(k) and (hi[2] - lo[2] <= 140 or hi[2] - lo[2] <= 1.65 * min(hi[0] - lo[0], hi[1] - lo[1]))


def _brauchen(t):
    """Grobe Zahl der Stuecke, die ein Teil noch braucht (Produkt der Ueberschreitungen je Achse)."""
    if _gut(t):
        return 1
    lo, hi = _bb(t)
    return max(2, int(np.prod(np.ceil((hi - lo) / _limits() - 1e-9).clip(1))))


def _teilung(k, a, c):
    """Schnitt senkrecht zu Achse a bei c ohne Loecher. Kleine Reststuecke, die mit einem Nachbarn der Gegenseite
    noch aufs Bett passen, werden dort wieder angesetzt (nicht abgetrennt). Gibt (Teile, Masken) zurueck;
    Masken = Querschnitte (in der Frame von _perm(a)) der wieder angesetzten Reststuecke."""
    nrm = [0.0, 0.0, 0.0]
    nrm[a] = 1.0
    oben, unten = k.split_by_plane(tuple(nrm), c)
    co, cu = _komponenten(oben), _komponenten(unten)
    masken = []
    for quelle, ziel, sg in ((co, cu, 1), (cu, co, -1)):
        for r in list(quelle[1:]):
            rlo, rhi = _bb(r)
            for i, m in enumerate(ziel):
                mlo, mhi = _bb(m)
                if np.any(rlo > mhi + 1e-3) or np.any(mlo > rhi + 1e-3):
                    continue
                u = m + r
                if len(_komponenten(u)) == 1 and _passt(u):
                    ziel[i] = u
                    quelle.remove(r)
                    masken.append(r.transform(_perm(a)).slice(c + sg * 0.05))
                    break
    return cu + co, masken


def _stifte(k, a, c, loecher, masken=(), wand=PIN_WAND):
    """Passstift-Positionen (3D) fuer die Schnittebene a = c: Punkte, an denen rundum >= PIN_WAND Material bleibt."""
    kp = k.transform(_perm(a))
    r = PIN_D_LOCH / 2 + wand
    sec = None
    for d in (0.05, 1.0, 2.0, 3.0, 4.0):
        for sg in (1, -1):
            cs = kp.slice(c + sg * d)
            sec = cs if sec is None else sec ^ cs
    if sec is None or sec.is_empty():
        return []
    for mk in masken:
        if not mk.is_empty():
            sec = sec - mk.offset(wand + 1.0)
    er = sec.offset(-r)
    if er.is_empty():
        return []
    polys = er.to_polygons()
    b = er.bounds()
    step = max(0.75, max(b[2] - b[0], b[3] - b[1]) / 70)
    gx, gy = np.meshgrid(np.arange(b[0], b[2] + step, step), np.arange(b[1], b[3] + step, step))
    pts = np.column_stack([gx.ravel(), gy.ravel()])
    pts = pts[_punkt_in(polys, pts)]
    if len(pts) == 0:
        return []

    def zu3(uv):
        p = np.zeros(3)
        p[(a + 1) % 3], p[(a + 2) % 3], p[a] = uv[0], uv[1], c
        return p
    frei = np.array([all(np.linalg.norm(zu3(u) - q) > 7 for _, q in loecher) for u in pts])
    pts = pts[frei]
    if len(pts) == 0:
        return []
    mitte = pts.mean(axis=0)
    p1 = pts[np.argmax(np.linalg.norm(pts - mitte, axis=1))]
    d1 = np.linalg.norm(pts - p1, axis=1)
    p2 = pts[np.argmax(d1)]
    if d1.max() >= 8.0:
        return [zu3(p1), zu3(p2)]
    return [zu3(pts[np.argmin(np.linalg.norm(pts - mitte, axis=1))])]


def _loch(a, p):
    z = mf.Manifold.cylinder(2 * PIN_TIEFE, PIN_D_LOCH / 2, PIN_D_LOCH / 2, 32, True)
    if a == 0:
        z = z.rotate((0, 90, 0))
    elif a == 1:
        z = z.rotate((90, 0, 0))
    return z.translate(tuple(float(v) for v in p))


def _beste_ebene(k, loecher):
    """Bester Schnitt (Achse, Lage) fuer einen zu grossen Koerper: je Achse mit Ueberschreitung Kandidaten im
    zulaessigen Fenster, vorsortiert nach Querschnitt/Inseln, dann echt geteilt und nach Stueckzahl, Passstiften
    und Querschnitt bewertet."""
    lo, hi = _bb(k)
    ext = hi - lo
    lim = _limits()
    achsen = [a for a in range(3) if ext[a] > lim[a]]
    if not achsen:                                    # passt in Einbaulage, aber nur instabil/hochkant: Achsen > KIPP_HOEHE kuerzen
        lim = np.minimum(lim, KIPP_HOEHE)
        achsen = [a for a in range(3) if ext[a] > lim[a]]
    best = None
    for a in achsen:
        n = max(2, math.ceil(ext[a] / lim[a] - 1e-9))
        nominal = lo[a] + ext[a] / n
        w0 = max(lo[a] + ext[a] - (n - 1) * lim[a], lo[a] + 2)
        w1 = min(lo[a] + lim[a], hi[a] - 2)
        if w1 < w0:
            w0 = w1 = min(max(nominal, lo[a] + ext[a] - (n - 1) * lim[a]), lo[a] + lim[a])
        kp = k.transform(_perm(a))
        vor = []
        for c in np.linspace(w0, w1, 41 if w1 > w0 else 1):
            if any(abs(p[a] - c) < PIN_D_LOCH / 2 + 2.5 for ax, p in loecher if ax != a):
                continue
            cs = kp.slice(float(c))
            ar = cs.area()
            if ar <= 0:
                continue
            isl = len(cs.decompose())
            platz = cs.offset(-(PIN_D_LOCH / 2 + PIN_WAND_MIN)).area() > 3.0      # irgendwo Platz fuer ein Passloch?
            vor.append((0 if platz else 1, ar * (1 + 0.5 * abs(c - nominal) / max(w1 - w0, 1e-6)) + 3000 * (isl - 1),
                        float(c), ar))
        vor.sort()
        mit = [v for v in vor if v[0] == 0][:6]
        for _, _, c, ar in mit + [v for v in vor if v[0] == 1][:3]:
            teile, masken = _teilung(k, a, c)
            stuecke = sum(_brauchen(t) for t in teile)
            wand = PIN_WAND
            pins = _stifte(k, a, c, loecher, masken, wand)
            if not pins:
                wand = PIN_WAND_MIN
                pins = _stifte(k, a, c, loecher, masken, wand)
            kost = stuecke * 1e5 + (0 if pins else 3e4) + (5e3 if pins and wand < PIN_WAND else 0) + ar
            if best is None or kost < best[0]:
                best = (kost, a, c, teile, masken, pins, wand)
    return best


def _steht(v0, F, t2=None):
    """Steht der auf z = 0 gelegte Koerper stabil? Auflageflaeche >= KIPP_AUFLAGE der Huellen-Grundflaeche und
    Schwerpunkt (Draufsicht) innerhalb der Auflage. Gibt (ok, Auflageflaeche) zurueck."""
    from scipy.spatial import ConvexHull, Delaunay
    t2 = trimesh.Trimesh(v0, F, process=False) if t2 is None else t2
    kontakt = (t2.triangles_center[:, 2] < 1.0) & (t2.face_normals[:, 2] < -0.99)   # Nietkoepfe etc. bis 1 mm
    flach = float(t2.area_faces[kontakt].sum())
    if flach < 100:
        return False, flach
    grund = ConvexHull(v0[:, :2]).volume              # 2D: Flaeche der Huelle in der Draufsicht
    if flach < KIPP_AUFLAGE * grund:
        return False, flach
    kp = np.unique(t2.faces[kontakt].ravel())
    try:
        return bool(Delaunay(v0[kp, :2]).find_simplex(t2.center_mass[:2]) >= 0), flach
    except Exception:
        return False, flach


def _beste_lage(k, ebenen, maxh, streng=False):
    """Beste Lage eines Koerpers mit Bauhoehe <= maxh, passend auf das Bett und stabil (Auflage >= KIPP_AUFLAGE der
    Grundflaeche, Schwerpunkt ueber der Auflage). Kandidaten: Einbaulage, Schnittflaechen, sechs Achsen, grosse ebene
    Huellflaechen. Bewertung: Ueberhang + HOEHE_STRAFE je mm Bauhoehe - Bonus fuer grosse Auflage + Strafe, wenn die
    groesste ebene Flaeche senkrecht steht. Gibt (score, R, ang) oder None zurueck."""
    me = k.to_mesh()
    V = np.asarray(me.vert_properties)[:, :3].astype(float)
    F = np.asarray(me.tri_verts)
    tm = trimesh.Trimesh(V, F, process=False)
    lim = _limits()
    kand = [(np.eye(3), streng)]
    for a, c in ebenen:
        sel = (np.abs(tm.triangles_center[:, a] - c) < 1e-3) & (np.abs(tm.face_normals[:, a]) > 0.999)
        for sg in (1, -1):
            if tm.area_faces[sel & (np.sign(tm.face_normals[:, a]) == sg)].sum() > 50:
                n = np.zeros(3)
                n[a] = sg
                kand.append((_rot_unten(n), True))
    for a in range(3):
        for sg in (1, -1):
            n = np.zeros(3)
            n[a] = sg
            kand.append((_rot_unten(n), True))
    grosse = []                                       # (Normale, Flaeche) der groessten ebenen Huellflaechen
    try:
        hull = tm.convex_hull
        for fi in np.argsort(-np.asarray(hull.facets_area))[:25]:
            kand.append((_rot_unten(hull.facets_normal[fi]), True))
            if hull.facets_area[fi] > 400 and len(grosse) < 3:
                grosse.append((hull.facets_normal[fi], float(hull.facets_area[fi])))
    except Exception:
        pass
    gesehen, best = set(), None
    for R, pruef in kand:
        key = tuple(np.round(R[2], 3))                # z-Zeile bestimmt die Lage bis auf z-Drehung
        if key in gesehen:
            continue
        gesehen.add(key)
        v = V @ R.T
        h = float(np.ptp(v[:, 2]))
        if h > maxh or h > lim[2]:
            continue
        if streng and h > KIPP_HOEHE and h > 1.5 * min(np.ptp(v[:, 0]), np.ptp(v[:, 1])):
            continue                                  # hohe, schlanke Lage (Turm) gilt nicht als stabil
        ang = _bett_winkel(v, lim[0])
        if ang is None:
            continue
        v0 = v - [0, 0, v[:, 2].min()]
        t2 = trimesh.Trimesh(v0, F, process=False)
        ok, flach = _steht(v0, F, t2)
        if pruef and not ok:
            continue
        score = _ueberhang(t2) + HOEHE_STRAFE * h + 3 * HOEHE_STRAFE * max(0.0, h - KIPP_HOEHE)
        if flach > 0:
            score -= 0.06 + 0.00005 * min(flach, 4000)
        for n, fl in grosse:                          # grosse ebene Flaeche nicht senkrecht stellen
            if abs((R @ n)[2]) < 0.3:
                score += 0.00005 * min(fl, 4000)
        if best is None or score < best[0]:
            best = (score, R, ang)
    return best


def _schneiden(k, loecher=None, ebenen=None, info=None):
    """Rekursiv teilen, bis jedes Stueck aufs Bett passt. Gibt ([(Manifold, Ebenen, Mitte)], info) zurueck."""
    loecher = [] if loecher is None else loecher
    ebenen = [] if ebenen is None else ebenen
    info = {"schnitte": [], "stifte": 0, "ohne_stifte": 0, "gekippt": 0} if info is None else info
    lo, hi = _bb(k)
    mitte = (lo + hi) / 2
    if _gut(k, ebenen):
        return [(k, ebenen, mitte)], info
    best = _beste_ebene(k, loecher)
    if best is None:
        return [(k, ebenen, mitte)], info
    _, a, c, teile, masken, pins, wand = best
    if pins:
        H = mf.Manifold.batch_boolean([_loch(a, p) for p in pins], mf.OpType.Add)
        hlo, hhi = _bb(H)
        neu_teile = []
        for t in teile:
            tlo, thi = _bb(t)
            if np.all(tlo <= hhi) and np.all(hlo <= thi):
                t = t - H
            neu_teile.append(t)
        teile = neu_teile
    info["schnitte"].append((a, c))
    info["stifte"] += len(pins)
    info["ohne_stifte"] += 0 if pins else 1
    info["duenn"] = info.get("duenn", 0) + (1 if pins and wand < PIN_WAND else 0)
    neu = loecher + [(a, p) for p in pins]
    eb = ebenen + [(a, c)]
    out = []
    for t in teile:
        for t2 in _komponenten(t):
            res, _ = _schneiden(t2, neu, eb, info)
            out += res
    return out, info


def _rot_unten(n):
    """Drehmatrix, die die Achsrichtung n nach -z legt."""
    n = np.asarray(n, float)
    t = np.array([0, 0, -1.0])
    if np.allclose(n, t):
        return np.eye(3)
    if np.allclose(n, -t):
        return np.diag([1.0, -1.0, -1.0])
    v = np.cross(n, t)
    s_ = np.linalg.norm(v)
    cth = float(n @ t)
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx * ((1 - cth) / (s_ ** 2))


def _drucklage(k, ebenen):
    """Drucklage eines Stuecks: erst mit Bauhoehe <= KIPP_HOEHE, sonst (Notfall) bis zur Maximalhoehe.
    Dreht ggf. um z, damit es aufs Bett passt. Gibt (Manifold, ok) zurueck."""
    best = _beste_lage(k, ebenen, KIPP_HOEHE) or _beste_lage(k, ebenen, HOEHE)
    if best is None:
        return k, False
    _, R, ang = best
    out = k.transform(np.hstack([R, np.zeros((3, 1))]))
    if ang:
        out = out.rotate((0, 0, float(ang)))
    return out, True


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

    # Grosse Koerper teilen (Passstifte), dann Anordnung: Reihen von links nach rechts, Unterseite auf z = 0
    stuecke = []                                     # (Manifold in Drucklage, Mitte vor dem Drehen, Manifold in Einbaulage)
    lim = _limits()

    def ort(a, c):
        return "xyz"[a] + "=" + str(round(float(c) * 8 + (392 if a == 2 else 0)))
    for ki, k in enumerate(koerper):
        lo, hi = _bb(k)
        if hi[0] - lo[0] <= lim[0] and hi[1] - lo[1] <= lim[1] and hi[2] - lo[2] <= lim[2]:
            if hi[2] - lo[2] <= KIPP_HOEHE:
                stuecke.append((k, (lo + hi) / 2, k))
                continue
        if True:
            teilstuecke, info = _schneiden(k)
            if info["schnitte"]:
                sch = " / ".join(ort(a, c) for a, c in sorted(info["schnitte"]))
                txt = (f"Koerper {ki} geteilt in {len(teilstuecke)} Stuecke bei {sch} (Original-mm, Einbaulage), "
                       f"{info['stifte']} Passstifte (Loch {PIN_D_LOCH} x {PIN_TIEFE} mm je Haelfte, Stift: "
                       f"1,75-mm-Filament {PIN_LAENGE} mm lang)")
                if info.get("duenn"):
                    txt += (f"; {info['duenn']} Schnittflaeche(n) nur mit schmaler Wand {PIN_WAND_MIN} mm um das Loch "
                            f"(duenner Querschnitt, z.B. Kettenglieder)")
                if info["ohne_stifte"]:
                    txt += f"; {info['ohne_stifte']} Schnittflaeche(n) ohne Stifte (kein Platz fuer Wand >= {PIN_WAND} mm)"
                probleme.append(txt)
            if info["gekippt"]:
                probleme.append(f"Koerper {ki} passt nur gekippt (auf grosser ebener Huellflaeche) auf das Bett "
                                f"{BETT:g} x {BETT:g}, {info['gekippt']} Stueck(e)")
            for t, eb, tmitte in teilstuecke:
                m, ok = _drucklage(t, eb)
                if not ok:
                    probleme.append(f"Koerper {ki}: Teilstueck bei {[round(float(v) * 8) for v in tmitte]} "
                                    f"passt nicht aufs Bett")
                stuecke.append((m, tmitte, t))

    solid_bb = [(_bb(m), m.volume()) for m in teile]

    def bauteil(p):
        """Vermutetes Solid zu einem Punkt (Modell-mm, Einbaulage): kleinstes Solid, dessen Huellquader den Punkt enthaelt."""
        kand = [(v, i, bb) for i, (bb, v) in enumerate(solid_bb) if np.all(bb[0] - 0.6 <= p) and np.all(p <= bb[1] + 0.6)]
        if not kand:
            return "?"
        v, i, bb = min(kand)
        e = (bb[1] - bb[0]) * 8
        return f"Solid {i} ({e[0]:.0f}x{e[1]:.0f}x{e[2]:.0f} Original-mm)"

    platziert, berichte = [], []
    x = y = reihe_h = 0.0
    for k, mitte, pre in stuecke:
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
        w, wp = _wandstaerke(_trimesh(pre))              # Dicke ist drehinvariant; Ort in Einbaulage
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
        if w is not None and b["wand_unter_min"]:
            # Duennstellen zu Orten (6-mm-Raster im Modell) zusammenfassen
            d = w < MIN_WAND
            cl = {}
            for dd, pp in zip(w[d], wp[d]):
                cl.setdefault(tuple(np.floor(pp / 6).astype(int)), []).append((dd, pp))
            zeilen = []
            for lst in sorted(cl.values(), key=lambda l: min(q[0] for q in l))[:6]:
                dmin = min(q[0] for q in lst)
                pm = np.mean([q[1] for q in lst], axis=0)
                zeilen.append(f"{dmin:.2f} mm ({len(lst)} Probe{'n' if len(lst) > 1 else ''}) bei x/y/z "
                              f"[{round(float(pm[0]) * 8)}, {round(float(pm[1]) * 8)}, {round(float(pm[2]) * 8 + 392)}] "
                              f"Original-mm, {bauteil(pm)}")
            b["duennstellen"] = zeilen
            probleme.append(f"Koerper {len(berichte)}: {b['wand_unter_min']}/{b['proben']} Proben duenner als {MIN_WAND} mm: "
                            + "; ".join(zeilen) + (f" (+{len(cl) - 6} weitere Stellen)" if len(cl) > 6 else ""))
        berichte.append(b)

    bett = mf.Manifold.batch_boolean(platziert, mf.OpType.Add) if len(platziert) > 1 else platziert[0]
    tm = _trimesh(bett)
    tm.export(str(ziel))
    lo, hi = tm.bounds
    return {
        "id": teil.id, "solids": len(teile), "koerper": len(stuecke),
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
    # Beispiel Testlauf: python tools/druck.py rumpf planierschild --out=out/druck_test
    ziel = ROOT / "docs" / "modelle" / INFO["id"] / "druck"
    aus = ROOT / "out"
    for a in argv:                                    # --out=ordner: Testlauf, schreibt nur dorthin (nicht nach docs/)
        if a.startswith("--out="):
            aus = ziel = Path(a[6:]).resolve()
    ziel.mkdir(parents=True, exist_ok=True)
    liste = [(t, Compound(children=list(t.bauen().values()))) for t in TEILE
             if t.druck and (not nur or t.id in nur)]
    if nur:
        print("Hinweis: Passung nur zwischen den angegebenen Teilen; fuer die endgueltigen Dateien alle Teile bauen.")
    berichte = alle_exportieren(liste, ziel)
    aus.mkdir(exist_ok=True)
    bericht_md(berichte, aus / "druckpruefung.md")
    (aus / "druckpruefung.json").write_text(json.dumps(berichte, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Bericht: {aus / 'druckpruefung.md'}")


if __name__ == "__main__":
    main(sys.argv[1:])
