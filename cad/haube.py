"""
Hanomag K 55 / K 55 E - Motorhaube, Kuehlermaske, Grillgitter und Scheinwerfer, 1:8 (build123d)

Haube und Kuehlermaske der K 55 E sind identisch mit der K 55
(Maske = Maske des Radschleppers R 45).

Koordinaten (Modell-mm, anders als die uebrigen Module direkt im Modellsystem):
  X = Laengsrichtung, Vorderkante Kuehlermaske bei x=0, nach hinten positiv
  Y = Querrichtung, +Y = rechte Fahrzeugseite (in Fahrtrichtung)
  Z = Hoehe, z=0 = MASKE_UNTEN (392 mm ueber Boden im Original, Nullebene des Modellsystems);
      die Maske selbst beginnt erst bei MASKE_UK = 525 (z = m(133)).

Masse in ORIGINAL-mm (mit m() bzw. _z() umgerechnet), Hauptmasse aus cad/common.py.
Druckparameter (Wandstaerke, Sickenhoehe ...) direkt in Modell-mm.

Fotobefund (blaue K 55 Bj. 1956: BS Seite rechts, BV Front; dazu PK, FL, WC):
  - Maske x 0..210, z 525..1410, 710 breit (h/b 1,35; Video 165/167, Flickr, DSC04737). Glatte Kappe
    ~115 (Vorderflaeche senkrecht, vorn oben R 35, Oberkante quer gewoelbt) mit Fluegellogo; durchgehendes
    Kuehlerfenster 620 x 640 (Randstreifen 45; Video 010/046/058/172-176/194-200, Flickr 26271249857) mit
    DREI senkrechten Staeben (4 Felder, keine Querbaender, kein Mittelsteg), dahinter senkrechte Lamellen
    (Teil "gitter"). Sockel ~205 mit Kurbelloch D 54 (Pumpenachse).
    Kuehlerverschluss (rot) sitzt auf der Maskenkappe bei x ~100..180, gehoert also zur Maske.
  - Haube x 210..1080 (dahinter Tank), Dach 1410 (Pfeilhoehe 42, Kantenradius R 85; Maske gleich), 690 breit,
    zwei Laengssicken auf dem Dach.
    Seite: vorderes Segment x 210..370 bis z 620 herunter, dann grosser, hinten offener
    Motorausschnitt bis zum Haubenende, Oberkante 1090 (Schriftband 1090..1410), vorn flacher, elliptischer
    Bogen (340 breit x 200 hoch, als zwei tangentiale Kreisbogen) in die senkrechte Vorderkante. Darueber nur
    das Schriftband: untere Laengssicke (geht vorn in die Bogensicke parallel zum Ausschnitt ueber), HANOMAG
    (Mitte x ~630, Teilung 78), obere Laengssicke.
    Gebordelter Ausschnittrand, Nietreihe an der Vorderkante, Haubenhalter mit Oese im Band.
    "K55" (ohne E, ~38 hoch, Mitte x ~298, z ~980) als freie erhabene Schrift im Segment
    (DSC04742, Video 066/070/173).
    Kein ovales und kein helles Schild an der Seite (auf keinem Foto).
    Durchbrueche mit Kragen fuer Auspuff (rechts) und Ansaugrohr (links) im Dach.
  - Seitenblech unter dem Motorausschnitt (Nordhorn-Video 2:44/2:53/2:58, DSC04729/42): Oberkante
    (= Unterkante des Motorfensters, Buerdel) bei z ~805..810; seitlich hinter den Greifern nur bis knapp ueber
    die Plattenoberseite (z ~660..680) gezogen, die Greiferspitzen (~735..750) ragen davor auf.
  - Scheinwerfer: an der Naht Maske/Haube oben (Video 165/172/196, Flickr 40431489714), Mitte x 230,
    |y| 430, z 1275, D 150; Topf mit gewoelbtem Ruecken, Chromring, Glas; Winkelhalter an der Haubenvorderkante
    unter der Lampe.

Hinweis zur Vernetzung: die Seitenwand ist eine einzige ebene Flaeche. Buchstaben, Schilder und
Sicken werden als einzelne, EINSENK tief eingesenkte Koerper mit der Wand verschmolzen (keine
koplanaren Booleans); Sicken sind Trapezprofile (Ebene/Kegel), deren Schnittkanten mit der Wand
Geraden bzw. Kreise sind.

Oeffentliche Teilfunktionen (von modell.py): kuehlermaske, maske_zier, gitter, haube, stirnwand, scheinwerfer.
"""
from __future__ import annotations

import contextlib
import math

from build123d import (
    Align,
    Axis,
    Box,
    BuildLine,
    BuildSketch,
    Circle,
    Cylinder,
    Ellipse,
    Face,
    GridLocations,
    Kind,
    Location,
    Locations,
    Mode,
    Part,
    Plane,
    PolarLocations,
    Polygon,
    Polyline,
    Pos,
    Rectangle,
    Rot,
    Shell,
    Solid,
    SortBy,
    Sphere,
    Text,
    ThreePointArc,
    Torus,
    Vector,
    Wire,
    extrude,
    fillet,
    make_face,
    offset,
    revolve,
    scale,
)

from .common import (
    ANSAUG_D,
    ANSAUG_XY,
    AUSPUFF_D,
    AUSPUFF_XY,
    DACH_R_KANTE,
    DACH_SAG,
    FONT,
    HAUBE_B,
    HAUBE_BAND_Z,
    HAUBE_DACH_Z,
    HAUBE_UNTEN_Z,
    HAUBE_X0,
    HAUBE_X1,
    KD_X,
    MASKE_B,
    MASKE_UK,
    MASKE_UNTEN,
    MASSSTAB,
    PUMPE,
    SCHEINWERFER,
    SEG_X1,
    m,
    rohr_glatt,
    sechskant,
    z_dach_orig,
)


def _z(z_orig: float) -> float:
    """Hoehe ueber Boden (Original-mm) -> Modell-z (z=0 bei MASKE_UNTEN)."""
    return m(z_orig - MASKE_UNTEN)


# ======================================================================================
# Parameter (nach Bauteil gegliedert)
# ======================================================================================

# --- Druckparameter (Modell-mm, nicht skaliert) ---
WAND = 1.6            # Blechstaerke Haube / Maske
SICKE_H = 0.5         # sichtbare Hoehe der Sicke ueber der Wand
SCHRIFT_H = 1.0       # Relief Schriftzug HANOMAG
TYP_H = 1.0           # Relief "K55" (ueber der Wand)
SCHRIFT_FETT = 0.1    # Konturversatz der Buchstaben
SCHRIFT_FASE = 0.3    # 45-Grad-Fase an der Oberkante der Buchstaben (faengt Licht)
EINSENK = 0.3         # Einsenktiefe aufgesetzter Teile (keine koplanaren Booleans)
NIET_R = 0.75         # Nietkopf-Radius (Kugelkappe, 0.6 hoch)

# --- Dachwoelbung (Maske und Haube gleich) ---
KM_B = m(MASKE_B)         # Maskenbreite
KM_H = _z(HAUBE_DACH_Z)  # Oberkante = Haubendach (1410 -> Modell-z 127)
KM_R_OBEN = m(DACH_R_KANTE)     # Radius Dachbogen -> senkrechte Seiten (Flickr 26271249857/39333958410: Schulter ~85-90)
KM_SAG = m(DACH_SAG)        # Pfeilhoehe des Dachbogens (Flickr-Frontfoto: Mitte zur Seite ~75 inkl. Ecke, Bogen allein ~42)

# --- Kuehlermaske (Original-mm, in Modell-mm umgerechnet) ---
# Fotos DSC04737/38 (frontal) und DSC04742 (Seite): Maske 710 x 897; Kappe glatt (Vorderflaeche senkrecht,
# Oberkante quer gewoelbt, vorn oben kleine Rundung); darunter das Grillfenster fast ueber die ganze Breite.
KM_Z0 = _z(MASKE_UK)  # Unterkante (z = m(133))
KM_T = m(HAUBE_X0)    # Tiefe (x 0..210)
KM_R_KAPPE = m(35)    # Rundung Kappe vorn oben (Seitenprofil, DSC04742: Oberkante flach, kleine Ecke)
KM_KAPPE = m(115)     # glatte Kappe ueber dem Fenster (Flickr 26271249857: ~112)
KM_SOCKEL = m(205)    # Sockel unter dem Kuehlerfenster (Flickr: ~205)
KM_RAND = m(45)       # seitlicher Randstreifen neben dem Fenster (Denkmal 40..55)
KURBEL_D = m(54)      # Kurbelloch (Foto 54; auf der Pumpenachse, von der Pumpe verdeckt)
KURBEL_Z = _z(PUMPE[2])
GRILL_STAEBE = 3      # senkrechte Staebe im durchgehenden Kuehlerfenster (4 Felder, Teilung ~155)
STAB_B = m(18)        # Stabbreite (Flickr 26271249857: duenne Rundstaebe)
STAB_X = -0.7         # Vorderseite der Staebe (Kappe/Maske bei x = 0)
STAB_TIEFE = 1.2      # Staebe reichen bis x = STAB_TIEFE (in die Wand eingebunden)
KD_XM = m(KD_X)    # Kuehlerverschluss Mitte x (Modell-mm)
KD_D = m(65)         # Kuehlerverschluss auf der Maskenkappe, Durchmesser (BS: x ~100..180, Mitte KD_X in common)

# --- Grillgitter (Kuehlerlamellen hinter dem Fenster) ---
GITTER_TEILUNG = 2.4  # Teilung der Lamellen
GITTER_STEG = 0.9     # Rippenbreite (>= 0.5)
GITTER_DICKE = 0.8
GITTER_X = 1.8        # Vorderseite Gittereinsatz (hinter der Maskenwand x 0..1.6)

# --- Haube (Original-mm, in Modell-mm umgerechnet) ---
H_X0 = KM_T                           # Haube beginnt direkt hinter der Maske (x = 210)
H_L = m(HAUBE_X1) - H_X0              # bis x = 1080 (dahinter Tank)
H_B = m(HAUBE_B)                      # Breite 690
H_UNTEN = _z(HAUBE_UNTEN_Z)           # Unterkante vorderes Seitensegment (z 780)
H_R_DACH = m(DACH_R_KANTE)                      # Radius Dachkanten (Dachbogen -> Seitenwand), gleich KM_R_OBEN
SEG_L = m(SEG_X1) - H_X0              # vorderes Seitensegment
DACH_SICKE_Y = m(150)                 # Laengssicken auf dem Dach (|y|)
AUSPUFF = (m(AUSPUFF_XY[0]), m(AUSPUFF_XY[1]), m(AUSPUFF_D))   # x, y, Durchmesser des Dachdurchbruchs
ANSAUG = (m(ANSAUG_XY[0]), m(ANSAUG_XY[1]), m(ANSAUG_D))

# --- Motorausschnitt und Sicken der Seitenwand ---
BOGEN_OBEN = _z(HAUBE_BAND_Z)         # Oberkante Motorausschnitt (z 1090 = HAUBE_BAND_Z)
# Ausschnittbogen vorn oben: flach/elliptisch (DSC04742, Video 173/066: ~300..450 breit x 200 hoch, gewaehlt 340;
# Bogenfuss z 890). Als zwei tangential anschliessende Kreisbogen (analytische Flaechen): r1 an der
# senkrechten Vorderkante, r2 an der Oberkante.
BOGEN_W, BOGEN_H = m(340), m(200)
BOGEN_R1 = m(130)
BOGEN_R2 = ((BOGEN_W - BOGEN_R1) ** 2 + BOGEN_H ** 2 - BOGEN_R1 ** 2) / (2 * (BOGEN_H - BOGEN_R1))
SICKE_Z = _z(1135)                    # untere Laengssicke (geht vorn in die Bogensicke ueber)
SICKE_OBEN_Z = _z(1240)               # obere Laengssicke (unter dem Dachradius, Wand eben bis ~1285)
SICKE_VORN_Z = _z(790)                # kurze Sicke im vorderen Segment = Ende der Bogensicke

# --- Beschriftung ---
SCHRIFT = "HANOMAG"
SCHRIFT_X, SCHRIFT_Z = m(630), _z(1190)  # Mitte Schriftzug (zwischen den Sicken; Video 165/010: Mitte 615..650)
SCHRIFT_TEILUNG = m(78)                  # Buchstabenteilung (Gesamtlaenge ~520)
SCHRIFT_VERSAL = m(55)                   # Versalhoehe
TYP = "K55"                              # Fotos DSC04729/42: Schriftzug "K55" (kein E sichtbar)
TYP_X, TYP_Z, TYP_TEILUNG, TYP_VERSAL = m(298), _z(980), m(38), m(38)   # Mitte x ~300, z 960..1000, Versalhoehe ~40
TYP_ABSTAND = 0.6                        # lichter Abstand der Glyphen (Modell-mm, >= 0.5)
TYP_FELD_H = m(50)                       # Hoehe des Platzhalters fuer die Nietreihe (freie Schrift ohne Rahmen)
TYP_FASE = 0.15                          # kleinere Fase: Strich ~1.0 mm, Deckflaeche >= 0.7 mm

# --- Seitenblech unter dem Motorausschnitt (Original-mm) ---
# Oberkante des Blechs (= Unterkante des Motorfensters, Buerdel) bei z ~805..810; direkt darunter reicht das Blech
# bis an die Kette (Nordhorn-Video 2:44 s164, Ausrichtung an 6 Laufrollen + Triebradnabe, Video 2:53/2:58).
BLECH_Z0, BLECH_Z1, BLECH_Z2 = 780.0, 800.0, 808.0
# Unterkante = Haubenkante auf Greiferhoehe (Nordhorn 2:44); Oberkante aussen / innen (schraege Lippe)

# --- Scheinwerfer (je Seite, separat drucken) ---
SW_D = m(150)                                # Aussendurchmesser
SW_TIEFE = 0.75                              # Streckung der Gehaeusekuppel in X
SW_TOPF = 1.2                                # zylindrischer Topfrand vor der Kuppel
SW_RING_L = 1.4                              # Chromring, Laenge nach vorn
SW_R = SW_D / 2                              # Aussenradius
SW_RA = SW_R - 1.4                           # lichte Weite Ring / Glas
SW_RT = SW_R - 0.3                           # Radius des Gehaeuses
# Frontebene Ring/Gehaeuse so, dass die Mitte des Gehaeuses (Topf + Kuppel) bei SCHEINWERFER x liegt
SW_X = m(SCHEINWERFER[0]) - (SW_TOPF + SW_TIEFE * SW_D / 2) / 2
SW_Y, SW_Z = m(SCHEINWERFER[1]), _z(SCHEINWERFER[2])   # Lampenmitte (Y = Betrag)


# ======================================================================================
# Helfer
# ======================================================================================
def z_dach(y: float) -> float:
    """Dachhoehe (Modell-z) bei Querlage y (Modell-mm); Kreisbogen aus common.z_dach_orig (Original-mm)."""
    return _z(z_dach_orig(y * MASSSTAB))


def _dach_flaeche(hb: float, z0: float, r_ecke: float) -> Face:
    """Querschnitt (Ebene YZ, lokal y/z) mit Dachbogen und verrundeten oberen Ecken."""
    zt = z_dach(hb)
    with BuildSketch(Plane.YZ) as sk:
        with BuildLine():
            Polyline((-hb, z0), (-hb, zt))
            ThreePointArc((-hb, zt), (0, z_dach(0)), (hb, zt))
            Polyline((hb, zt), (hb, z0), (-hb, z0))
        make_face()
    fl = sk.sketch.faces()[0]
    return fl.fillet_2d(r_ecke, [v for v in fl.vertices() if zt - 0.01 < v.Z])


def plane_side(x: float, z: float, side: int, y_abs: float = H_B / 2) -> Plane:
    """Ebene auf einer Seitenwand (Normale nach aussen), lesbar von aussen."""
    xd = (1, 0, 0) if side < 0 else (-1, 0, 0)
    return Plane(origin=(x, side * y_abs, z), x_dir=xd, z_dir=(0, side, 0))


def _vereinigen(teile: list[Part]) -> Part:
    """Liste von Solids zu einem Solid verschmelzen."""
    erg = teile[0]
    if len(teile) > 1:
        erg = erg.fuse(*teile[1:])
    return erg


# --- Schrift -------------------------------------------------------------------------
_versal_cache: dict[str, tuple[float, float]] = {}


def _versal(font: str) -> tuple[float, float]:
    """Versalhoehe und Lage der Versalmitte (bezogen auf font_size = 1)."""
    if font not in _versal_cache:
        bb = Text("H", font_size=10, font_path=font, align=(Align.CENTER, None)).bounding_box()
        _versal_cache[font] = ((bb.max.Y - bb.min.Y) / 10, (bb.max.Y + bb.min.Y) / 20)
    return _versal_cache[font]


def _glyph_versaetze(glyphen: list, teilung: float, abstand: float | None) -> list[float]:
    """Waagerechte Lage (Mitte) jedes Glyphen: feste Teilung oder gleiche lichte Abstaende."""
    n = len(glyphen)
    if abstand is None:
        return [(i - (n - 1) / 2) * teilung for i in range(n)]
    offs, x = [], 0.0
    for g in glyphen:
        bb = g.bounding_box() if g is not None else None
        w0, w1 = (bb.min.X, bb.max.X) if bb else (-teilung / 2, teilung / 2)
        offs.append(x - w0)
        x += (w1 - w0) + abstand
    breite = x - abstand
    return [o - breite / 2 for o in offs]


def buchstaben(pl: Plane, txt: str, teilung: float, versal: float, hoehe: float, font: str = FONT,
               fase: float = SCHRIFT_FASE, abstand: float | None = None) -> list[Part]:
    """Einzelne, kraeftig erhabene Buchstaben auf gemeinsamer Grundlinie, Oberkante umlaufend
    45 Grad gefast, damit sie auch bei flachem Licht lesbar sind. Feste Teilung (Mitte zu Mitte)
    oder, mit abstand, gleiche lichte Abstaende zwischen den Glyphen (fuer kleine Schrift).
    Jeder Buchstabe ist ein eigener Koerper, EINSENK tief in die Wand eingesenkt."""
    faktor, mitte = _versal(font)
    groesse = versal / faktor
    glyphen = []
    for ch in txt:
        g = Text(ch, font_size=groesse, font_path=font, align=(Align.CENTER, None)) if ch != " " else None
        if g is not None and SCHRIFT_FETT:
            g = offset(g, amount=SCHRIFT_FETT, kind=Kind.ARC)
        glyphen.append(g)
    offs = _glyph_versaetze(glyphen, teilung, abstand)
    out = []
    for off, glyph in zip(offs, glyphen, strict=True):
        if glyph is None:
            continue
        p = pl.shift_origin(pl.from_local_coords((off, -mitte * groesse))).offset(-EINSENK)
        for fc in glyph.faces():
            out.append(p * _gefaster_buchstabe(fc, hoehe + EINSENK, fase))
    return out


def _polygon_punkte(w: Wire, seg: float = 0.3) -> list[Vector]:
    """Kontur eines Glyphen als Punktfolge (Sehnenlaenge <= seg, Ecken bleiben erhalten)."""
    pts = []
    for e in w.edges():
        k = max(1, math.ceil(e.length / seg))
        for i in range(k):
            q = e.position_at(i / k)
            if not pts or (q - pts[-1]).length > 0.03:
                pts.append(q)
    if (pts[0] - pts[-1]).length < 0.03:
        pts.pop()
    return pts


def _tetraeder(p0: Vector, p1: Vector, p2: Vector, p3: Vector) -> Solid:
    """Tetraeder aus vier Punkten (Werkzeug fuer die Buchstabenfase)."""
    flaechen = [Face(Wire.make_polygon([a, b, c], close=True))
                for a, b, c in ((p0, p1, p2), (p0, p2, p3), (p0, p3, p1), (p1, p3, p2))]
    return Solid(Shell(flaechen))


def _fasenwerkzeuge(polys: list[list[Vector]], flaeche: Face, hoehe: float, fase: float) -> tuple[list, list]:
    """Keile (je Polygonkante) und Tetraeder (an konkaven Ecken) zum Abziehen der 45-Grad-Fase."""
    keile, kegel = [], []
    oben = Vector(0, 0, 1)
    for pts in polys:
        k = len(pts)
        rich = [(pts[(i + 1) % k] - pts[i]) for i in range(k)]
        # Materialseite der Schleife (links oder rechts der Laufrichtung), an einer Kante bestimmt
        i0 = max(range(k), key=lambda i: rich[i].length)
        t0 = rich[i0].normalized()
        links = flaeche.is_inside((pts[i0] + pts[(i0 + 1) % k]) * 0.5 + Vector(-t0.Y, t0.X, 0) * 0.02)
        sgn = 1 if links else -1

        for i in range(k):
            d = rich[i]
            if d.length < 1e-3:
                continue
            t = d.normalized()
            nrm = Vector(-t.Y, t.X, 0) * sgn                  # zeigt ins Material
            ebene = Plane(origin=pts[i], x_dir=nrm, z_dir=nrm.cross(oben))
            dreieck = ebene * Polygon((-0.1, hoehe - fase - 0.1), (fase + 0.1, hoehe + 0.1),
                                      (-0.1, hoehe + 0.1), align=None)
            keile.append(extrude(dreieck, amount=d.length, dir=t))
            # an (vom Material aus) konkaven Ecken laufen die Keilstreifen auseinander: Luecke mit
            # einer Pyramide schliessen (Spitze in der Ecke, Flanken = Stirnflaechen der Nachbarkeile,
            # Schraegflaeche = Sehne des 45-Grad-Kegels um die Ecke)
            ta = rich[i - 1].normalized()
            if (ta.X * t.Y - ta.Y * t.X) * sgn < -1e-9:
                na = Vector(-ta.Y, ta.X, 0) * sgn
                v = pts[i]
                r = fase + 0.1
                unten = Vector(v.X, v.Y, hoehe - fase)
                o0 = Vector(v.X, v.Y, hoehe + 0.1)
                oa = o0 + na * r
                ob = o0 + nrm * r
                with contextlib.suppress(Exception):
                    kegel.append(_tetraeder(unten, oa, ob, o0))
    return keile, kegel


def _gefaster_buchstabe(fc: Face, hoehe: float, fase: float) -> Part:
    """Glyphenflaeche (lokal, XY) extrudieren und die Oberkante 45 Grad fasen.
    OCCT-chamfer scheitert an manchen Glyphen (G, K, 5: spitze Winkel, Kurzkanten). Darum wird die
    Kontur polygonisiert und je Polygonkante ein dreieckiger Keil abgezogen: Schnitt mit
    {Abstand d zur Kante, z > hoehe - fase + d}; an konkaven Ecken (Streifen laufen auseinander)
    schliesst ein Tetraeder die Luecke. Ergebnis: 45-Grad-Fase der Polygonkontur, nur ebene Flaechen
    -> robust und sauber zu vernetzen."""
    polys = [_polygon_punkte(w) for w in [fc.outer_wire(), *fc.inner_wires()]]
    flaeche = Face(Wire.make_polygon(polys[0], close=True),
                   [Wire.make_polygon(q, close=True) for q in polys[1:]])
    koerper = extrude(flaeche, amount=hoehe)
    keile, kegel = _fasenwerkzeuge(polys, flaeche, hoehe, fase)
    for werkzeuge in (keile + kegel, keile):
        try:
            erg = koerper.cut(*werkzeuge)
            if erg.is_valid and len(erg.solids()) == 1:
                return erg
        except Exception:
            pass
    return koerper


def hanomag_logo(pl: Plane, h: float = 0.7) -> Part:
    """Hanomag-Fluegellogo (Modell-mm, ca. 15 x 7): ovaler Ring mit H, je 3 Federn links/rechts.
    Federn 0.7 -> 0.5 mm verjuengt, Spalt >= 0.6 mm."""
    with BuildSketch(pl) as sk:
        Ellipse(3.7, 3.4)
        Ellipse(3.0, 2.7, mode=Mode.SUBTRACT)
        # stilisiertes H
        with Locations((-1.1, 0), (1.1, 0)):
            Rectangle(0.7, 5.4)
        Rectangle(2.2, 0.7)
        # Federn: oben am laengsten, zur Spitze verjuengt und leicht angehoben
        for sx in (-1, 1):
            for zc, laenge in ((1.3, 7.6), (0.0, 6.9), (-1.3, 6.2)):
                x0, x1 = sx * 3.2, sx * laenge
                Polygon((x0, zc - 0.35), (x1, zc), (x1, zc + 0.5), (x0, zc + 0.35), align=None)
    return _logo_extrude(sk.sketch, pl, h)


def _logo_extrude(sketch: Face, pl: Plane, h: float) -> Part:
    """Skizze (bereits in pl) um EINSENK nach innen versetzen und erhaben extrudieren."""
    v = pl.z_dir * (-EINSENK)
    return extrude(sketch.moved(Location((v.X, v.Y, v.Z))), amount=h + EINSENK, dir=pl.z_dir)


# ======================================================================================
# Kuehlermaske
# ======================================================================================
def _grill() -> tuple[float, float, float]:
    """Grillfenster: (Breite, Hoehe, Unterkante) in Modell-mm."""
    g_b = KM_B - 2 * KM_RAND
    g_z0, g_z1 = KM_Z0 + KM_SOCKEL, KM_H - KM_KAPPE      # Fenster (hinter Querband / Wulst)
    return g_b, g_z1 - g_z0, g_z0


def _kuehlerverschluss() -> list[Part]:
    """Einfuellstutzen mit Kragen und Deckel mit Riffelrand und Knebel, auf der Maskenkappe."""
    r = KD_D / 2
    z_kappe = KM_H
    kragen = Pos(KD_XM, 0, z_kappe - EINSENK) * Cylinder(r * 0.95, 0.5 + EINSENK,
                                                       align=(Align.CENTER, Align.CENTER, Align.MIN))
    stutzen = Pos(KD_XM, 0, z_kappe - WAND) * Cylinder(r * 0.72, WAND + 2.0,
                                                     align=(Align.CENTER, Align.CENTER, Align.MIN))
    z_d = z_kappe + 2.0
    with BuildSketch(Plane.XY.offset(z_d)) as sk, Locations((KD_XM, 0)):
        Circle(r)
        with PolarLocations(r, 18):
            Circle(0.35, mode=Mode.SUBTRACT)
    deckel = extrude(sk.sketch, amount=2.2)
    deckel += Pos(KD_XM, 0, z_d + 2.2) * Cylinder(r - 1.2, 0.6, align=(Align.CENTER, Align.CENTER, Align.MIN))
    knebel = Pos(KD_XM, 0, z_d + 2.8 + 0.5) * Box(1.2, 2 * r - 2.0, 1.0)
    knebel = fillet(knebel.edges().filter_by(Axis.X), 0.45)
    return [kragen, stutzen, deckel, knebel]


def _maske_aussen(d: float = 0.0) -> Part:
    """Aussenform der Maske als Schnitt zweier Zylinderprofile: Seitenprofil (senkrechte Vorderflaeche, vorn oben
    Rundung KM_R_KAPPE, Oberkante flach) und Frontprofil (Dachbogen mit Pfeilhoehe KM_SAG, Ecken KM_R_OBEN).
    Senkrechte Kanten bleiben scharf.
    d > 0: Innenraum (um die Wandstaerke d eingerueckt, hinten und unten ueberstehend) zum Aushoehlen."""
    w = math.sqrt(0.5)
    rk = KM_R_KAPPE - d
    ht = KM_H - d
    x_hint = KM_T if d == 0 else KM_T + 5
    z_unten = KM_Z0 if d == 0 else KM_Z0 - 5
    with BuildSketch(Plane.XZ) as sx:
        with BuildLine():
            Polyline((d, z_unten), (x_hint, z_unten), (x_hint, ht), (d + rk, ht))
            ThreePointArc((d + rk, ht), (d + rk - rk * w, ht - rk + rk * w), (d, ht - rk))
            Polyline((d, ht - rk), (d, z_unten))
        make_face()
    seite = extrude(sx.sketch, amount=KM_B, both=True)
    fl = _dach_flaeche(KM_B / 2 - d, z_unten, max(KM_R_OBEN - d, 0.5))
    front = extrude(Pos(-1, 0, -d) * fl, amount=x_hint + 1)
    return seite & front


def _stab(z0: float, z1: float, y: float) -> Part:
    """Senkrechter Fensterstab (Rundprofil-artig): vorn verrundet, mit Laschen in Sockel und Kappe eingebunden."""
    st = Pos(STAB_X, y, z0) * Box(STAB_TIEFE - STAB_X, STAB_B, z1 - z0, align=(Align.MIN, Align.CENTER, Align.MIN))
    st = fillet(st.edges().filter_by(Axis.Z).filter_by_position(Axis.X, STAB_X - 0.01, STAB_X + 0.01), 0.6)
    lasche = Pos(0.2, y, z0 - 0.5) * Box(1.0, STAB_B, z1 - z0 + 1.0, align=(Align.MIN, Align.CENTER, Align.MIN))
    return st.fuse(lasche)


def kuehlermaske() -> tuple[Part, tuple[float, float, float]]:
    """Maskenschale (z 525..1410): glatte Kappe, durchgehendes Kuehlerfenster mit drei senkrechten Staeben,
    breiter Randstreifen, Kurbelloch, Kuehlerverschluss.
    Liefert (Solid, (Fensterbreite, Fensterhoehe, Fensterunterkante))."""
    outer = _maske_aussen()
    km = outer - _maske_aussen(WAND)

    g_b, g_h, g_z0 = _grill()
    g_z1 = g_z0 + g_h
    km -= Pos(-1, 0, g_z0) * Box(WAND + 2, g_b, g_h, align=(Align.MIN, Align.CENTER, Align.MIN))
    km -= Pos(-1, 0, KURBEL_Z) * Rot(0, 90, 0) * Cylinder(KURBEL_D / 2, WAND + 2,
                                                          align=(Align.CENTER, Align.CENTER, Align.MIN))

    teile = [_stab(g_z0, g_z1, -g_b / 2 + i * g_b / (GRILL_STAEBE + 1)) for i in range(1, GRILL_STAEBE + 1)]
    teile += _kuehlerverschluss()
    km = km.fuse(*teile)
    return km, (g_b, g_h, g_z0)


def maske_zier() -> list[Part]:
    """Fluegellogo auf der glatten Kappe (Chrom/Blech)."""
    # Foto DSC04738: Logo mittig, auf 2/3 der Kappenhoehe (von oben), vorn senkrecht
    z_logo = KM_H - 0.66 * KM_KAPPE
    logo = hanomag_logo(Plane(origin=(0, 0, z_logo), x_dir=(0, -1, 0), z_dir=(-1, 0, 0)), h=0.7)
    return [logo]


def gitter(g_b: float, g_h: float, g_z0: float) -> Part:
    """Kuehlerlamellen hinter dem Fenster: senkrechte Rippen in einem Rahmen (Video 058/173: Lamellen von der Seite
    als senkrechte Rippen, kein Drahtgitter). Ein Solid, innen an der Maskenwand."""
    w, h = g_b + 1.0, g_h + 2.0   # Breite: bleibt 0.08 vor der Maskenseitenwand
    n = int((w - 2) / GITTER_TEILUNG)
    zc = g_z0 + g_h / 2
    with BuildSketch(Plane.YZ.offset(GITTER_X)) as sk, Locations((0, zc)):
        Rectangle(w, h)
        Rectangle(w - 2, h - 2, mode=Mode.SUBTRACT)
        with GridLocations(GITTER_TEILUNG, 0, n, 1):
            Rectangle(GITTER_STEG, h - 1)
    return extrude(sk.sketch, amount=GITTER_DICKE)


# ======================================================================================
# Haube
# ======================================================================================
def _haube_aussen() -> Part:
    """Haubenkoerper: Dachbogen (gleicher Kreisbogen wie die Maske, bei den Haubenseiten y = +-345) und
    Dachecken H_R_DACH, bis H_UNTEN, x = H_X0..H_X0+H_L."""
    fl = _dach_flaeche(H_B / 2, H_UNTEN, H_R_DACH)
    return extrude(Pos(H_X0, 0, 0) * fl, amount=H_L)


def stirnwand() -> Part:
    """Stirnwand zwischen Haube und Tank (Modell-mm, fuer modell._haube_tank): Haubenquerschnitt oberhalb des
    Motorausschnitts, 0.5 mm Original schmaler/niedriger als die Haube; x = HAUBE_X1-6 .. TANK_X0+13."""
    d = m(0.5)
    fl = _dach_flaeche(H_B / 2 - d, BOGEN_OBEN, H_R_DACH - d)
    x0, x1 = m(HAUBE_X1 - 6.0), m(1085.0 + 7.0)      # bis 1098: schliesst die Stirnwulst-Keilspitze (Tank x 1085..1097) ein
    return Pos(0, 0, -d) * extrude(Pos(x0, 0, 0) * fl, amount=x1 - x0)


def _bogen_geometrie() -> tuple[float, tuple[float, float], tuple[float, float], float]:
    """Lage des Ausschnittbogens (zwei tangentiale Kreisbogen): (xa, c1, c2, phi).
    c1 = Mittelpunkt (x, z) des kleinen Bogens r1 (vorn, tangiert die senkrechte Vorderkante bei x = xa),
    c2 = Mittelpunkt des grossen Bogens r2 (tangiert die Oberkante BOGEN_OBEN bei x = xa + BOGEN_W),
    phi = Winkel des Uebergangspunkts (180 = -x, 90 = +z, wie in _sicke_bogen)."""
    xa = H_X0 + SEG_L
    c1 = (xa + BOGEN_R1, BOGEN_OBEN - BOGEN_H)
    c2 = (xa + BOGEN_W, BOGEN_OBEN - BOGEN_R2)
    phi = math.degrees(math.atan2(c1[1] - c2[1], c1[0] - c2[0]))
    return xa, c1, c2, phi


def _kp(c: tuple[float, float], r: float, ang: float) -> tuple[float, float]:
    """Punkt auf dem Kreis um c (x, z) mit Radius r bei Winkel ang (Grad)."""
    return (c[0] + r * math.cos(math.radians(ang)), c[1] + r * math.sin(math.radians(ang)))


def _ausschnitt() -> Part:
    """Motorausschnitt beider Seiten als Werkzeugkoerper: von SEG_X1 bis hinter das Haubenende
    (hinten offen), unten offen, Oberkante HAUBE_BAND_Z, Ecke vorn oben als flacher Ellipsenbogen."""
    xa, c1, c2, phi = _bogen_geometrie()
    x1 = H_X0 + H_L + 10
    z0 = H_UNTEN - 10
    pj = _kp(c1, BOGEN_R1, phi)
    with BuildSketch(Plane.XZ) as s:
        with BuildLine():
            Polyline((x1, z0), (xa, z0), (xa, c1[1]))
            ThreePointArc((xa, c1[1]), _kp(c1, BOGEN_R1, (180 + phi) / 2), pj)
            ThreePointArc(pj, _kp(c2, BOGEN_R2, (phi + 90) / 2), (c2[0], BOGEN_OBEN))
            Polyline((c2[0], BOGEN_OBEN), (x1, BOGEN_OBEN), (x1, z0))
        make_face()
    return extrude(s.sketch, amount=H_B, both=True)


def _profil_sicke(pl: Plane) -> Face:
    """Sickenquerschnitt (Trapez, 0.5 hoch, oben 0.6, an der Wand 1.2 breit, 0.3 eingesenkt).
    Lokales x = quer zur Sicke in der Wand, lokales y = Wandnormale nach aussen."""
    a0, a1 = -EINSENK, SICKE_H
    return pl * Polygon((-0.8, a0), (0.8, a0), (0.3, a1), (-0.3, a1), align=None)


def _profil_bordel(pl: Plane) -> Face:
    """Gebordelter Ausschnittrand: Band 1.2 breit, aussen 0.5 / innen 0.2 aufgedickt,
    zur Ausschnittseite (lokales +x) voll gerundet."""
    a0, a1 = -WAND - 0.2, SICKE_H
    rk = (a1 - a0) / 2
    with BuildSketch(pl) as sk:
        with Locations((-0.6, (a0 + a1) / 2)):
            Rectangle(1.2, a1 - a0)
        with Locations((0, (a0 + a1) / 2)):
            Circle(rk)
    return sk.sketch


def _sicke_gerade(profil, p0: tuple, p1: tuple, quer: tuple, side: int) -> Part:
    """Profil von p0 nach p1 extrudieren; quer = Querrichtung (lokales x) in der Wand."""
    p0, p1 = Vector(*p0), Vector(*p1)
    d = p1 - p0
    yn = Vector(0, side, 0)
    pl = Plane(origin=p0, x_dir=Vector(*quer), z_dir=Vector(*quer).cross(yn))
    return extrude(profil(pl), amount=d.length, dir=d.normalized())


def _sicke_bogen(profil, c: tuple[float, float], r_bahn: float, y: float, w_start: float, w_ende: float,
                 side: int) -> Part:
    """Profil auf dem Kreisbogen um c = (x, z) von Winkel w_start bis w_ende (Grad, 180 = vorn, 90 = oben) drehen.
    Lokales x zeigt zum Bogenmittelpunkt (= zur Ausschnittseite). Flaechen: Ebene/Kegel/Torus."""
    yn = Vector(0, side, 0)
    xd = Vector(1, 0, 0)
    pl = Plane(origin=(c[0] - r_bahn, y, c[1]), x_dir=xd, z_dir=xd.cross(yn))
    ax = Axis((c[0], y, c[1]), (0, 1, 0))
    seg = revolve(profil(pl), axis=ax, revolution_arc=w_start - w_ende)
    return seg.rotate(ax, 180 - w_start) if w_start < 179.99 else seg


def _dachsicke(y: float, x0: float, x1: float) -> Part:
    """Laengssicke auf dem Haubendach bei y (Trapezprofil, Normale +Z)."""
    pl = Plane(origin=(x0, y, z_dach(y)), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    return extrude(_profil_sicke(pl), amount=x1 - x0)


def _typ_feld_z() -> tuple[float, float]:
    """Hoehenbereich des K55-Schriftzugs (fuer die Nietreihe)."""
    return TYP_Z - TYP_FELD_H / 2, TYP_Z + TYP_FELD_H / 2


def _bordelrand(side: int) -> list[Part]:
    """Gebordelter Rand entlang des Motorausschnitts (senkrecht, zwei Bogen, waagerecht bis hinten)."""
    yw = side * H_B / 2                               # Wandaussenseite
    xe = H_X0 + H_L
    xa, c1, c2, phi = _bogen_geometrie()
    return [
        _sicke_gerade(_profil_bordel, (xa, yw, H_UNTEN - 2), (xa, yw, c1[1]), (1, 0, 0), side),
        _sicke_bogen(_profil_bordel, c1, BOGEN_R1, yw, 180, phi, side),
        _sicke_bogen(_profil_bordel, c2, BOGEN_R2, yw, phi, 90, side),
        _sicke_gerade(_profil_bordel, (c2[0], yw, BOGEN_OBEN), (xe + 2, yw, BOGEN_OBEN), (0, 0, -1), side),
    ]


def _bogensicke(side: int) -> list[Part]:
    """Bogensicke parallel zum Ausschnitt (gleiche Mittelpunkte, Radien + d); oben tangential in die untere
    Laengssicke, unten bis zur kurzen Quersicke ueber dem Typfeld."""
    yw = side * H_B / 2
    xa, c1, c2, phi = _bogen_geometrie()
    d = SICKE_Z - BOGEN_OBEN                          # Abstand Bogensicke zur Ausschnittkante
    xs = xa - d
    return [
        _sicke_gerade(_profil_sicke, (xs, yw, SICKE_VORN_Z - 0.3), (xs, yw, c1[1]), (1, 0, 0), side),
        _sicke_bogen(_profil_sicke, c1, BOGEN_R1 + d, yw, 180, phi, side),
        _sicke_bogen(_profil_sicke, c2, BOGEN_R2 + d, yw, phi, 90, side),
    ]


def _laengssicken(side: int) -> list[Part]:
    """Laengssicken im Schriftband (untere vorn bis zur Bogensicke geteilt, obere bis zur Hinterkante)
    und kurze Quersicke im vorderen Segment, die in der Bogensicke endet."""
    yw = side * H_B / 2
    xe = H_X0 + H_L
    xa, _c1, c2, _phi = _bogen_geometrie()
    xs = xa - (SICKE_Z - BOGEN_OBEN)
    x_v = H_X0 + 1.6
    return [
        _sicke_gerade(_profil_sicke, (x_v, yw, SICKE_Z), (c2[0], yw, SICKE_Z), (0, 0, 1), side),
        _sicke_gerade(_profil_sicke, (c2[0], yw, SICKE_Z), (xe + 2, yw, SICKE_Z), (0, 0, 1), side),
        _sicke_gerade(_profil_sicke, (x_v, yw, SICKE_OBEN_Z), (xe + 2, yw, SICKE_OBEN_Z), (0, 0, 1), side),
        _sicke_gerade(_profil_sicke, (x_v, yw, SICKE_VORN_Z), (xs + 0.3, yw, SICKE_VORN_Z), (0, 0, 1), side),
    ]


def _nietreihe_seite(side: int) -> list[Part]:
    """Nietreihe an der Vorderkante (Anschluss Maske); frei bleiben Haubenhalter, Typfeld, Sicken."""
    yn = side * (H_B / 2 + 0.6 - NIET_R)
    n = 13
    z_a, z_e = H_UNTEN + 3, z_dach(H_B / 2) - H_R_DACH - 2
    z_halter = (SICKE_Z + SICKE_OBEN_Z) / 2
    f0, f1 = _typ_feld_z()
    teile = []
    for i in range(n):
        z = z_a + i * (z_e - z_a) / (n - 1)
        if abs(z - z_halter) < 5.5 or f0 - 1.0 < z < f1 + 1.0:
            continue
        if any(abs(z - zs) < 1.6 for zs in (SICKE_Z, SICKE_OBEN_Z, SICKE_VORN_Z)):
            continue
        teile.append(Pos(H_X0 + 1.8, yn, z) * Sphere(NIET_R))
    return teile


def _seitensicken(side: int) -> list[Part]:
    """Sicken, Bordelrand und Nieten einer Seitenwand.
    Alle Sicken sind Trapezprofile (Ebenen/Kegel), der Rand ein Band mit Rundung - so gibt es nur
    analytische Flaechen und kreisfoermige bzw. gerade Schnittkanten mit der Wand."""
    return _bordelrand(side) + _bogensicke(side) + _laengssicken(side) + _nietreihe_seite(side)


def _typfeld(side: int) -> list[Part]:
    """Schriftzug "K55" (ohne E) frei auf dem vorderen Seitensegment (DSC04742, Video 066/070/173: kein Rahmen),
    Buchstaben TYP_H ueber der Wand."""
    pl = plane_side(TYP_X, TYP_Z, side)
    return buchstaben(pl, TYP, TYP_TEILUNG, TYP_VERSAL, TYP_H, fase=TYP_FASE, abstand=TYP_ABSTAND)


def _haubenhalter(side: int) -> list[Part]:
    """Haubenhalter vorn im Schriftband: Lasche, senkrechter Bolzen, Oese oben."""
    y0 = side * H_B / 2
    x, z = H_X0 + 4.0, (SICKE_Z + SICKE_OBEN_Z) / 2
    lasche = Pos(x, y0 + side * (0.6 - EINSENK), z - 2.5) * Box(2.6, 1.2 + EINSENK * 2, 2.4)
    lasche += Pos(x, y0 + side * (0.6 - EINSENK), z + 2.5) * Box(2.6, 1.2 + EINSENK * 2, 2.4)
    yb = y0 + side * 1.9
    bolzen = Pos(x, yb, z - 4.0) * Cylinder(0.55, 7.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    arm = Pos(x, (y0 + yb) / 2 + side * 0.3, z - 2.5) * Box(1.2, abs(yb - y0) + 0.4, 1.0)
    arm += Pos(x, (y0 + yb) / 2 + side * 0.3, z + 2.5) * Box(1.2, abs(yb - y0) + 0.4, 1.0)
    oese = Pos(x, yb, z + 3.0 + 1.1) * Rot(90, 0, 0) * Torus(1.0, 0.4)
    return [lasche, arm, bolzen, oese]


def _fensterblech(side: int) -> Part:
    """Seitenblech unter dem Motorfenster (Fotos DSC04729/42, Nordhorn-Video 2:44/2:53/2:58): durchgehender Blechstreifen,
    buendig mit der Haubenaussenkante (y 332..345), Oberkante mit schraeger Aussenlippe (innen z 808 -> aussen z 800),
    Unterkante BLECH_Z0 = 780 = HAUBE_UNTEN_Z (Haubenkante auf Greiferhoehe, Greifer oben 738..768) ueber dem oberen Kettentrum;
    die Greifer (Spitzen ~ 735..750) stehen davor; hintere Unterecke R 60.
    Beginnt bei x 365 (ueberlappt die Segmentkante, sonst schwebt das Blech) und endet am Haubenende x 1080 (im Video
    endet die Unterkante des Motorfensters dort an der Kupplungsglocke/dem A-Bock)."""
    yo, yi = H_B / 2, H_B / 2 - WAND
    z0, z1, z2 = _z(BLECH_Z0), _z(BLECH_Z1), _z(BLECH_Z2)
    pts = [(side * yi, z0), (side * yo, z0), (side * yo, z1), (side * yi, z2)]
    with BuildSketch(Plane.YZ) as sk:
        Polygon(*pts, align=None)
    x0 = m(SEG_X1 - 5.0)
    xe = H_X0 + H_L
    blech = extrude(Pos(x0, 0, 0) * sk.sketch, amount=xe - x0)
    r = m(60.0)                                       # hintere Unterecke gerundet
    ecke = Pos(xe - r / 2 + 0.05, side * H_B / 2, z0 + r / 2 - 0.05) * Box(r + 0.1, 4 * WAND, r + 0.1)
    ecke -= Pos(xe - r, side * H_B / 2, z0 + r) * Rot(90, 0, 0) * Cylinder(r, 6 * WAND)
    return blech - ecke


def _haubenschale() -> tuple[Part, Part]:
    """Hohle Haubenschale mit Motorausschnitten: (Schale, Aussenkoerper)."""
    outer = _haube_aussen()
    f = outer.faces()
    hb = offset(outer, amount=-WAND,
                openings=[f.sort_by(Axis.X)[0], f.sort_by(Axis.X)[-1], f.sort_by(Axis.Z)[0]])
    hb -= _ausschnitt()
    return hb, outer


def _versteifung(outer: Part) -> Part:
    """Versteifungswinkel innen an der Hinterkante (Dach und Schriftband ueber dem Ausschnitt)."""
    innen1 = offset(outer, amount=-WAND + 0.1)
    innen2 = offset(outer, amount=-WAND - 1.2)
    xe = H_X0 + H_L
    return (innen1 - innen2) & (Pos(xe - 3.0, 0, BOGEN_OBEN + 1.0) *
                                Box(3.0, H_B, KM_H, align=(Align.MIN, Align.CENTER, Align.MIN)))


def _dachnieten() -> list[Part]:
    """Nietreihe an der vorderen Dachkante (Dachsicken frei lassen)."""
    teile = []
    n = 9
    for i in range(n):
        y = -(H_B / 2 - H_R_DACH - 1.5) + i * (H_B - 2 * H_R_DACH - 3) / (n - 1)
        if abs(abs(y) - DACH_SICKE_Y) < 1.8:
            continue
        teile.append(Pos(H_X0 + 1.8, y, z_dach(y) + 0.6 - NIET_R) * Sphere(NIET_R))
    return teile


def _rohrkragen() -> list[Part]:
    """Kragen an den Rohrdurchbruechen (Auspuff rechts, Ansaugrohr links)."""
    teile = []
    for (x, y, d) in (AUSPUFF, ANSAUG):
        kr = Pos(x, y, z_dach(y) - 0.8) * Cylinder(d / 2 + 1.6, 0.6 + 0.8,
                                                  align=(Align.CENTER, Align.CENTER, Align.MIN))
        kr = fillet(kr.edges().group_by(Axis.Z)[-1].sort_by(SortBy.RADIUS)[-1:], 0.4)
        teile.append(kr)
    return teile


def haube() -> Part:
    """Motorhaube x 210..1080: Blech 1.6 mm, Dachkantenradius, grosse Motorausschnitte mit
    Bordelrand, Schriftband mit Sicken und HANOMAG, Schriftzug K55, Dachsicken, Nieten,
    Haubenhalter, Rohrdurchbrueche mit Kragen. Druck stehend auf der Hinterkante."""
    hb, outer = _haubenschale()
    xe = H_X0 + H_L

    teile = [_versteifung(outer)]
    for side in (-1, 1):
        teile += _seitensicken(side)
        teile += _haubenhalter(side)
        teile += buchstaben(plane_side(SCHRIFT_X, SCHRIFT_Z, side), SCHRIFT, SCHRIFT_TEILUNG,
                            SCHRIFT_VERSAL, SCHRIFT_H)
        teile += _typfeld(side)
        teile.append(_fensterblech(side))

    # zwei Laengssicken auf dem Dach (PK), hinter der vorderen Nietreihe bis zur Hinterkante
    for sy in (-1, 1):
        teile.append(_dachsicke(sy * DACH_SICKE_Y, H_X0 + 3.5, xe + 2))
    teile += _dachnieten()
    teile += _rohrkragen()

    hb = hb.fuse(*teile)
    # Durchbrueche zuletzt (schneiden Dach und Kragen sauber)
    for (x, y, d) in (AUSPUFF, ANSAUG):
        hb -= Pos(x, y, KM_H - 5) * Cylinder(d / 2, 10, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Abschluss: alles, was ueber Vorder-/Hinterkante oder Unterkante steht, kappen
    hb &= Pos(H_X0, 0, H_UNTEN) * Box(H_L, H_B + 20, KM_H, align=(Align.MIN, Align.CENTER, Align.MIN))
    return hb


# ======================================================================================
# Scheinwerfer
# ======================================================================================
def _sw_gehaeuse() -> Part:
    """Gehaeuse: zylindrischer Topfrand + gestreckte Halbkugel nach hinten, Nabe unten (lokal, Front bei x = 0)."""
    rt = SW_RT
    topf = Rot(0, 90, 0) * Cylinder(rt, SW_TOPF, align=(Align.CENTER, Align.CENTER, Align.MIN))
    kuppel = scale(Sphere(rt), by=(SW_TIEFE, 1, 1))
    kuppel = Pos(SW_TOPF, 0, 0) * (kuppel & Box(rt, 2 * rt + 1, 2 * rt + 1, align=(Align.MIN, Align.CENTER, Align.CENTER)))
    nabe = Pos(1.5, 0, -rt + 1.5) * Cylinder(1.8, 2.2, align=(Align.CENTER, Align.CENTER, Align.MAX))
    gehaeuse = topf.fuse(kuppel, nabe)
    gehaeuse -= Pos(-0.1, 0, 0) * Rot(0, 90, 0) * Cylinder(SW_RA, 0.6, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return gehaeuse


def _sw_ring() -> Part:
    """Chromring vorn, aussen verrundet (Aussendurchmesser = SW_D)."""
    ring = Rot(0, -90, 0) * (Cylinder(SW_R, SW_RING_L, align=(Align.CENTER, Align.CENTER, Align.MIN))
                             - Cylinder(SW_RA, SW_RING_L, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return fillet(ring.edges().group_by(Axis.X)[0].sort_by(SortBy.RADIUS)[-1:], 0.6)


def _sw_optik() -> tuple[Part, Part, Part]:
    """Reflektor (flache Schuessel), Birne und Glas (lokal): (refl, birne, glas)."""
    ra = SW_RA
    tiefe = 0.55
    rd = (ra ** 2 + tiefe ** 2) / (2 * tiefe)
    refl = Rot(0, 90, 0) * Cylinder(ra, 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    refl = Pos(-1.0, 0, 0) * refl - Pos(-0.35 - rd, 0, 0) * Sphere(rd)
    birne = Pos(-0.6, 0, 0) * Sphere(1.0)

    # Glas: flache Kugelkappe, Basis im Ring, 1.0 mm gewoelbt
    hk = 1.0
    rg = (ra ** 2 + hk ** 2) / (2 * hk)
    glas = Pos(-1.0 - hk + rg, 0, 0) * Sphere(rg)
    glas &= Pos(-1.0, 0, 0) * Box(hk + 1, 2 * ra, 2 * ra, align=(Align.MAX, Align.CENTER, Align.CENTER))
    glas &= Rot(0, 90, 0) * Cylinder(ra, 10)
    # Glas als massive Linse bis in die Reflektorschuessel: sonst laeuft die Kappe am Rand messerscharf aus
    # und der Raum zwischen Glas und Reflektor ist ein eingeschlossener Hohlraum (nicht druckbar).
    # In der App ist das Glas durchscheinend, der Reflektor bleibt sichtbar.
    schale = Pos(-1.0, 0, 0) * Rot(0, 90, 0) * Cylinder(ra, 0.7, align=(Align.CENTER, Align.CENTER, Align.MIN))
    schale &= Pos(-0.35 - rd, 0, 0) * Sphere(rd)
    glas = glas.fuse(schale)
    return refl, birne, glas


def _sw_halter(side: int, y: float, z_arm: float) -> Part:
    """Winkelhalter: Fussplatte an der Haubenvorderkante, Flachstahl-Arm unter die Lampe, Bolzen mit Muttern."""
    wand_y = side * H_B / 2                          # Halter sitzt an der Haubenvorderkante (Lampe an der Naht)
    x_h = SW_X + 1.5                                 # Bolzenachse (unter der Nabe)
    fuss = Pos(x_h - 1.5, wand_y + side * (0.6 - EINSENK), z_arm - 0.8) * Box(5.0, 1.2 + 2 * EINSENK, 6.0)
    fuss = fillet(fuss.edges().filter_by(Axis.Y), 0.8)
    arm = Pos(x_h, (wand_y + y) / 2, z_arm - 0.8) * Box(2.4, abs(y - wand_y), 1.6)
    arm += Pos(x_h, y, z_arm - 0.8) * Cylinder(1.2, 1.6)
    bolzen = Pos(x_h, y, z_arm - 2.6) * Cylinder(0.8, SW_Z - SW_RT + 1.0 - (z_arm - 2.6),
                                                 align=(Align.CENTER, Align.CENTER, Align.MIN))
    mutter_u = sechskant((x_h, y, z_arm - 1.6), (0, 0, -1), sw=2.4, hoehe=1.0)
    mutter_o = sechskant((x_h, y, z_arm), (0, 0, 1), sw=2.4, hoehe=0.8)
    halter = _vereinigen([fuss, arm, bolzen, mutter_u, mutter_o])
    for dz in (-2.6, 1.0):                           # zwei Schraubenkoepfe auf der Fussplatte
        halter = halter.fuse(sechskant((x_h - 2.6, wand_y + side * (1.2 - EINSENK), z_arm + dz),
                                       (0, side, 0), sw=1.6, hoehe=0.6))
    return halter


def _sw_kabel(side: int, y: float, z_arm: float) -> Part:
    """Kabel vom Gehaeuseboden in einer Schlaufe in die Haubenwand."""
    mw_y = side * (H_B / 2 - WAND / 2)               # Kabel endet in der Haubenwand
    return rohr_glatt([(SW_X + 5.0, y, SW_Z - SW_RT * 0.8),
                       (SW_X + 5.8, y + side * 0.5, z_arm - 4.0),
                       (SW_X + 5.8, (y + mw_y) / 2, z_arm - 6.0),
                       (SW_X + 5.8, mw_y + side * 1.5, z_arm - 5.0),
                       (SW_X + 5.8, mw_y, z_arm - 5.0)], 0.5, rb=2.0)


def scheinwerfer(side: int) -> dict[str, list[Part]]:
    """Scheinwerfer oben an der Maskenseite mit Winkelhalter (wird mit side=-1 gebaut, rechts
    gespiegelt). Die Lampe liegt mit dem Ring an der Maskenseite an (|y| 355 = SW_Y - SW_D/2).
    Liefert {material: [solids]}: Gehaeuse, Halter, Kabel schwarz; Ring, Reflektor chrom; Glas."""
    y = side * SW_Y
    refl, birne, glas = _sw_optik()

    loc = Pos(SW_X, y, SW_Z)
    gehaeuse, ring, refl, birne, glas = (loc * s for s in (_sw_gehaeuse(), _sw_ring(), refl, birne, glas))

    z_arm = SW_Z - SW_RT - 2.2                       # Oberkante Arm
    halter = _sw_halter(side, y, z_arm)
    kabel = _sw_kabel(side, y, z_arm)
    gehaeuse = gehaeuse.fuse(Pos(SW_X + 5.0, y, SW_Z - SW_RT * 0.8) * Sphere(0.8))   # Kabeltuelle
    return {"schwarz": [gehaeuse, halter, kabel], "chrom": [ring, refl], "glas": [glas, birne]}
