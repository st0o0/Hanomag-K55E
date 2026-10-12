"""
Hanomag K 55 / K 55 E - Motorhaube, Kuehlermaske, Grillgitter und Scheinwerfer, 1:8 (build123d)

Haube und Kuehlermaske der K 55 E sind identisch mit der K 55
(Maske = Maske des Radschleppers R 45).

Koordinaten (Modell-mm, anders als die uebrigen Module direkt im Modellsystem):
  X = Laengsrichtung, Vorderkante Kuehlermaske bei x=0, nach hinten positiv
  Y = Querrichtung, +Y = rechte Fahrzeugseite (in Fahrtrichtung)
  Z = Hoehe, z=0 = MASKE_UNTEN (392 mm ueber Boden im Original, historische Nullebene);
      die Maske selbst beginnt erst bei MASKE_UK = 450 (z = m(58)).

Masse in ORIGINAL-mm (mit m() bzw. _z() umgerechnet), Hauptmasse aus cad/common.py.
Druckparameter (Wandstaerke, Sickenhoehe ...) direkt in Modell-mm.

Fotobefund (blaue K 55 Bj. 1956: BS Seite rechts, BV Front; dazu PK, FL, WC):
  - Maske x 0..210, z 450..1347, 710 breit (h/b 1,26). Kappe ~125 mit Fluegellogo, Grillfenster
    ~600 hoch mit rotem Rahmen (Rollwulst) und Eckzwickeln, drei senkrechte Rundstaebe auf den
    Vierteln der Grillbreite vor dem Drahtgitter, KEINE waagerechten Staebe. Sockel ~175, davor die
    Hydraulikpumpe (planierschild.py, PUMPE), dahinter das Kurbelloch auf Pumpenachse.
    Kuehlerverschluss (rot) sitzt auf der Maskenkappe bei x ~100..180, gehoert also zur Maske.
  - Haube x 210..1080 (dahinter Tank), Dach 1347, 690 breit, zwei Laengssicken auf dem Dach.
    Seite: schmales vorderes Segment x 210..360 bis z 620 herunter, dann grosser, hinten offener
    Motorausschnitt bis zum Haubenende, Oberkante 1125, vorn Bogen R ~220 in die senkrechte
    Vorderkante. Darueber nur das Schriftband: untere Laengssicke (geht vorn in die Bogensicke
    parallel zum Ausschnitt ueber), HANOMAG in normaler Laufweite (Mitte x ~745), obere Laengssicke.
    Gebordelter Ausschnittrand, Nietreihe an der Vorderkante, Haubenhalter mit Oese im Band.
    "K55E" in einem erhabenen, eingerahmten Feld vorn unten im Segment (PK).
    Kein ovales und kein helles Schild an der Seite (auf keinem Foto).
    Durchbrueche mit Kragen fuer Auspuff (rechts) und Ansaugrohr (links) im Dach.
  - Scheinwerfer: oben an den Maskenseiten (BS, BV, PK, WC), Mitte x 110, |y| 430, z 1150, D 150;
    Topf mit gewoelbtem Ruecken, Chromring, Glas; Winkelhalter an der Maskenseite unter der Lampe.

Hinweis zur Vernetzung: die Seitenwand ist eine einzige ebene Flaeche. Buchstaben, Schilder und
Sicken werden als einzelne, EINSENK tief eingesenkte Koerper mit der Wand verschmolzen (keine
koplanaren Booleans); Sicken sind Trapezprofile (Ebene/Kegel), deren Schnittkanten mit der Wand
Geraden bzw. Kreise sind.
"""
import math
from build123d import *
from .common import (m, sechskant, rohr_glatt, MASKE_UNTEN, MASKE_UK, HAUBE_X0, HAUBE_X1, HAUBE_B,
                     HAUBE_DACH_Z, HAUBE_UNTEN_Z, HAUBE_BAND_Z, SEG_X1, AUSPUFF_XY, ANSAUG_XY,
                     SCHEINWERFER, PUMPE)


def _z(z_orig):
    """Hoehe ueber Boden (Original-mm) -> Modell-z (z=0 bei MASKE_UNTEN)."""
    return m(z_orig - MASKE_UNTEN)


# ---------------- Druck-Parameter (Modell-mm, nicht skaliert) ----------------
WAND = 1.6            # Blechstaerke Haube / Maske
SICKE_H = 0.5         # sichtbare Hoehe der Sicke ueber der Wand
PRAEGE_H = 0.7        # Hoehe Typfeld-Rahmen ueber der Wand
SCHRIFT_H = 1.0       # Relief Schriftzug HANOMAG
TYP_H = 1.0           # Relief "K55E" (ueber der Wand; Feldboden liegt 0.3 hoch)
SCHRIFT_FETT = 0.1    # Konturversatz der Buchstaben
SCHRIFT_FASE = 0.3    # 45-Grad-Fase an der Oberkante der Buchstaben (faengt Licht)
EINSENK = 0.3         # Einsenktiefe aufgesetzter Teile (keine koplanaren Booleans)
NIET_R = 0.75         # Nietkopf-Radius (Kugelkappe, 0.6 hoch)
GITTER_TEILUNG = 2.0  # Gittereinsatz: Maschenteilung
GITTER_STEG = 0.6     # Drahtstaerke (>= 0.5)
GITTER_DICKE = 0.8
GITTER_X = 1.8        # Vorderseite Gittereinsatz (hinter der Maskenwand x 0..1.6)

# Schrift: Century Gothic Bold - geometrische Grotesk wie das Original (runde O, gespreiztes M)
SCHRIFT_FONT = r"C:\Windows\Fonts\GOTHICB.TTF"

# ---------------- Kuehlermaske (Original-mm) ----------------
KM_B = m(710)                         # Breite
KM_Z0 = _z(MASKE_UK)                  # Unterkante (z = m(58))
KM_H = _z(HAUBE_DACH_Z)               # Oberkante = Haubendach (z = m(955))
KM_T = m(HAUBE_X0)                    # Tiefe (x 0..210)
KM_R_OBEN = m(80)     # Radius obere Laengskanten (Frontansicht)
KM_R_VORN = m(35)     # Radius obere Vorderkante
# Aufteilung nach Foto BV (Maske 897 hoch): Kappe 0,14 / Grill 0,66 / Sockel 0,20
KM_KAPPE = m(125)     # Kappe ueber dem Grill (Logo)
KM_SOCKEL = m(175)    # Sockel unter dem Grill (Kurbelloch hinter der Pumpe)
KM_RAND = m(44)       # seitlicher Rahmen neben dem Grill (Grill/Maske 0,875 breit)
RAHMEN_R = m(9)       # Rollwulst um das Grillfenster
ZWICKEL = m(56)       # Eckzwickel im Grillrahmen (Schenkellaenge)
GRILL_STAEBE = 3      # senkrechte Staebe auf den Vierteln der Grillbreite (BV, FL)
STAB_R = m(10)        # halbrunde senkrechte Staebe
STAB_X = 0.3          # Lage der Stabachse (Front bei x = 0)
KURBEL_D = m(47)      # Kurbelloch (auf der Pumpenachse, von der Pumpe verdeckt)
KURBEL_Z = _z(PUMPE[2])
TYPSCHILD = (m(118), _z(880), m(120), m(50))   # x-Mitte, z-Mitte, Breite, Hoehe (linke Maskenseite)
KD_X, KD_D = m(140), m(65)            # Kuehlerverschluss auf der Maskenkappe (BS: x ~100..180)

# ---------------- Haube (Original-mm) ----------------
H_X0 = KM_T                           # Haube beginnt direkt hinter der Maske (x = 210)
H_L = m(HAUBE_X1) - H_X0              # bis x = 1080 (dahinter Tank)
H_B = m(HAUBE_B)                      # Breite 690
H_UNTEN = _z(HAUBE_UNTEN_Z)           # Unterkante vorderes Seitensegment (z 620)
H_R_DACH = m(60)                      # Radius Dachkanten
SEG_L = m(SEG_X1) - H_X0              # vorderes Seitensegment x 210..360
BOGEN_OBEN = _z(HAUBE_BAND_Z)         # Oberkante Motorausschnitt (z 1125)
BOGEN_R = m(220)                      # Eckradius Motorausschnitt vorn oben
SICKE_Z = _z(1152)                    # untere Laengssicke (geht vorn in die Bogensicke ueber)
SICKE_OBEN_Z = _z(1272)               # obere Laengssicke (unter dem Dachradius, Wand eben bis 1287)
SICKE_VORN_Z = _z(790)                # kurze Sicke im vorderen Segment = Ende der Bogensicke
DACH_SICKE_Y = m(150)                 # Laengssicken auf dem Dach (|y|)
SCHRIFT = "HANOMAG"
SCHRIFT_X, SCHRIFT_Z = m(745), _z(1212)  # Mitte Schriftzug (zwischen den Sicken)
SCHRIFT_TEILUNG = m(88)                  # Buchstabenteilung (normale Laufweite)
SCHRIFT_VERSAL = m(55)                   # Versalhoehe
TYP = "K55E"
TYP_X, TYP_Z, TYP_TEILUNG, TYP_VERSAL = m(281), _z(700), m(25), m(31)
TYP_ABSTAND = 0.6                        # lichter Abstand der Glyphen (Modell-mm, >= 0.5)
TYP_FELD_B, TYP_FELD_H = m(126), m(60)   # erhabenes Feld (x 218..344, z 670..730), Nieten dort ausgespart
TYP_RAHMEN = 0.7                         # Rahmenbreite (Modell-mm)
TYP_FASE = 0.15                          # kleinere Fase: Strich ~1.0 mm, Deckflaeche >= 0.7 mm
AUSPUFF = (m(AUSPUFF_XY[0]), m(AUSPUFF_XY[1]), m(70))   # x, y, Durchmesser (motor.py nutzt h.AUSPUFF)
ANSAUG = (m(ANSAUG_XY[0]), m(ANSAUG_XY[1]), m(90))

# ---------------- Scheinwerfer (je Seite, separat drucken) ----------------
SW_D = m(150)                                # Aussendurchmesser
SW_TIEFE = 0.75                              # Streckung der Gehaeusekuppel in X
SW_TOPF = 1.2                                # zylindrischer Topfrand vor der Kuppel
SW_RING_L = 1.4                              # Chromring, Laenge nach vorn
# Frontebene Ring/Gehaeuse so, dass die Mitte des Gehaeuses (Topf + Kuppel) bei SCHEINWERFER x liegt
SW_X = m(SCHEINWERFER[0]) - (SW_TOPF + SW_TIEFE * SW_D / 2) / 2
SW_Y, SW_Z = m(SCHEINWERFER[1]), _z(SCHEINWERFER[2])   # Lampenmitte (Y = Betrag)


# ------------------------------------------------------------------
# Helfer
# ------------------------------------------------------------------
def plane_front(z, y=0.0, x=0.0):
    """Ebene auf der Front, Normale nach vorn (-X), lesbar von vorn."""
    return Plane(origin=(x, y, z), x_dir=(0, -1, 0), z_dir=(-1, 0, 0))


def plane_side(x, z, side, y_abs=H_B / 2):
    """Ebene auf einer Seitenwand (Normale nach aussen), lesbar von aussen."""
    xd = (1, 0, 0) if side < 0 else (-1, 0, 0)
    return Plane(origin=(x, side * y_abs, z), x_dir=xd, z_dir=(0, side, 0))


def _vereinigen(teile):
    """Liste von Solids zu einem Solid verschmelzen."""
    erg = teile[0]
    if len(teile) > 1:
        erg = erg.fuse(*teile[1:])
    return erg


_versal_cache = {}


def _versal(font):
    """Versalhoehe und Lage der Versalmitte (bezogen auf font_size = 1)."""
    if font not in _versal_cache:
        bb = Text("H", font_size=10, font_path=font, align=(Align.CENTER, None)).bounding_box()
        _versal_cache[font] = ((bb.max.Y - bb.min.Y) / 10, (bb.max.Y + bb.min.Y) / 20)
    return _versal_cache[font]


def buchstaben(pl: Plane, txt, teilung, versal, hoehe, font=SCHRIFT_FONT, fase=SCHRIFT_FASE, abstand=None):
    """Einzelne, kraeftig erhabene Buchstaben auf gemeinsamer Grundlinie, Oberkante umlaufend
    45 Grad gefast, damit sie auch bei flachem Licht lesbar sind. Feste Teilung (Mitte zu Mitte)
    oder, mit abstand, gleiche lichte Abstaende zwischen den Glyphen (fuer kleine Schrift).
    Jeder Buchstabe ist ein eigener Koerper, EINSENK tief in die Wand eingesenkt."""
    faktor, mitte = _versal(font)
    groesse = versal / faktor
    n = len(txt)
    glyphen = []
    for ch in txt:
        g = Text(ch, font_size=groesse, font_path=font, align=(Align.CENTER, None)) if ch != " " else None
        if g is not None and SCHRIFT_FETT:
            g = offset(g, amount=SCHRIFT_FETT, kind=Kind.ARC)
        glyphen.append(g)
    if abstand is None:
        offs = [(i - (n - 1) / 2) * teilung for i in range(n)]
    else:
        bbs = [g.bounding_box() if g is not None else None for g in glyphen]
        offs, x = [], 0.0
        for bb in bbs:
            w0, w1 = (bb.min.X, bb.max.X) if bb else (-teilung / 2, teilung / 2)
            offs.append(x - w0)
            x += (w1 - w0) + abstand
        breite = x - abstand
        offs = [o - breite / 2 for o in offs]
    out = []
    for off, glyph in zip(offs, glyphen):
        if glyph is None:
            continue
        p = pl.shift_origin(pl.from_local_coords((off, -mitte * groesse))).offset(-EINSENK)
        for fc in glyph.faces():
            out.append(p * _gefaster_buchstabe(fc, hoehe + EINSENK, fase))
    return out


def _polygon_punkte(w: Wire, seg=0.3):
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


def _tetraeder(p0, p1, p2, p3):
    """Tetraeder aus vier Punkten (Werkzeug fuer die Buchstabenfase)."""
    flaechen = [Face(Wire.make_polygon([a, b, c], close=True))
                for a, b, c in ((p0, p1, p2), (p0, p2, p3), (p0, p3, p1), (p1, p3, p2))]
    return Solid(Shell(flaechen))


def _gefaster_buchstabe(fc: Face, hoehe, fase):
    """Glyphenflaeche (lokal, XY) extrudieren und die Oberkante 45 Grad fasen.
    OCCT-chamfer scheitert an manchen Glyphen (G, K, 5: spitze Winkel, Kurzkanten). Darum wird die
    Kontur polygonisiert und je Polygonkante ein dreieckiger Keil abgezogen: Schnitt mit
    {Abstand d zur Kante, z > hoehe - fase + d}; an konkaven Ecken (Streifen laufen auseinander)
    schliesst ein Tetraeder die Luecke. Ergebnis: 45-Grad-Fase der Polygonkontur, nur ebene Flaechen
    -> robust und sauber zu vernetzen."""
    polys = [_polygon_punkte(w) for w in [fc.outer_wire()] + list(fc.inner_wires())]
    flaeche = Face(Wire.make_polygon(polys[0], close=True),
                   [Wire.make_polygon(q, close=True) for q in polys[1:]])
    koerper = extrude(flaeche, amount=hoehe)
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
                try:
                    kegel.append(_tetraeder(unten, oa, ob, o0))
                except Exception:
                    pass
    for werkzeuge in (keile + kegel, keile):
        try:
            erg = koerper.cut(*werkzeuge)
            if erg.is_valid and len(erg.solids()) == 1:
                return erg
        except Exception:
            pass
    return koerper


def wulst_pfad(kanten, r):
    """Rundsicke: Kreisquerschnitt entlang eines Kantenzugs."""
    w = Wire(kanten)
    e0 = w.edges()[0]
    return sweep(Plane(origin=e0.position_at(0), z_dir=e0.tangent_at(0)) * Circle(r), path=w,
                 transition=Transition.ROUND)


def stab_x(x0, x1, y, z, r):
    """Zylinder entlang X von x0 bis x1."""
    return Pos(x0, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0, align=(Align.CENTER, Align.CENTER, Align.MIN))


def stab_y(y0, y1, x, z, r):
    """Zylinder entlang Y von y0 bis y1."""
    return Pos(x, y0, z) * Rot(-90, 0, 0) * Cylinder(r, y1 - y0, align=(Align.CENTER, Align.CENTER, Align.MIN))


def hanomag_logo(pl: Plane, h=0.7):
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


def _logo_extrude(sketch, pl, h):
    """Skizze (bereits in pl) um EINSENK nach innen versetzen und erhaben extrudieren."""
    v = pl.z_dir * (-EINSENK)
    return extrude(sketch.moved(Location((v.X, v.Y, v.Z))), amount=h + EINSENK, dir=pl.z_dir)


# ------------------------------------------------------------------
# Kuehlermaske
# ------------------------------------------------------------------
def stab_z(z0, z1, x, y, r):
    """Zylinder entlang Z von z0 bis z1."""
    return Pos(x, y, z0) * Cylinder(r, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN))


def _grill():
    """Grillfenster: (Breite, Hoehe, Unterkante) in Modell-mm."""
    g_b = KM_B - 2 * KM_RAND
    g_z0, g_z1 = KM_Z0 + KM_SOCKEL, KM_H - KM_KAPPE
    return g_b, g_z1 - g_z0, g_z0


def _kuehlerverschluss():
    """Einfuellstutzen mit Kragen und Deckel mit Riffelrand und Knebel, auf der Maskenkappe."""
    r = KD_D / 2
    z_dach = KM_H
    kragen = Pos(KD_X, 0, z_dach - EINSENK) * Cylinder(r * 0.95, 0.5 + EINSENK,
                                                      align=(Align.CENTER, Align.CENTER, Align.MIN))
    stutzen = Pos(KD_X, 0, z_dach - WAND) * Cylinder(r * 0.72, WAND + 2.0,
                                                    align=(Align.CENTER, Align.CENTER, Align.MIN))
    z_d = z_dach + 2.0
    with BuildSketch(Plane.XY.offset(z_d)) as sk:
        with Locations((KD_X, 0)):
            Circle(r)
            with PolarLocations(r, 18):
                Circle(0.35, mode=Mode.SUBTRACT)
    deckel = extrude(sk.sketch, amount=2.2)
    deckel += Pos(KD_X, 0, z_d + 2.2) * Cylinder(r - 1.2, 0.6, align=(Align.CENTER, Align.CENTER, Align.MIN))
    knebel = Pos(KD_X, 0, z_d + 2.8 + 0.5) * Box(1.2, 2 * r - 2.0, 1.0)
    knebel = fillet(knebel.edges().filter_by(Axis.X), 0.45)
    return [kragen, stutzen, deckel, knebel]


def kuehlermaske():
    """Maskenschale (z 450..1347) mit Grillfenster, Rollwulst, Eckzwickeln, drei senkrechten
    Staeben, Kurbelloch und Kuehlerverschluss auf der Kappe.
    Liefert (Solid, (Grillbreite, Grillhoehe, Grillunterkante))."""
    outer = Pos(0, 0, KM_Z0) * Box(KM_T, KM_B, KM_H - KM_Z0, align=(Align.MIN, Align.CENTER, Align.MIN))
    outer = fillet(outer.edges().filter_by(Axis.X).group_by(Axis.Z)[-1], KM_R_OBEN)
    top_front = outer.edges().filter_by(Axis.Y).group_by(Axis.Z)[-1].group_by(Axis.X)[0]
    outer = fillet(top_front, KM_R_VORN)
    f = outer.faces()
    km = offset(outer, amount=-WAND, openings=[f.sort_by(Axis.X)[-1], f.sort_by(Axis.Z)[0]])

    g_b, g_h, g_z0 = _grill()
    g_z1 = g_z0 + g_h
    km -= Pos(-1, 0, g_z0) * Box(WAND + 2, g_b, g_h, align=(Align.MIN, Align.CENTER, Align.MIN))
    km -= Pos(-1, 0, KURBEL_Z) * Rot(0, 90, 0) * Cylinder(KURBEL_D / 2, WAND + 2,
                                                          align=(Align.CENTER, Align.CENTER, Align.MIN))

    teile = []
    # Rollwulst um das Grillfenster (geschlossener Rundstab, Ecken R 1.5)
    rr = 1.5
    yb, za, ze = g_b / 2, g_z0, g_z1
    xw = 0.0
    pts = [((xw, -yb + rr, za), (xw, yb - rr, za)), ((xw, yb, za + rr), (xw, yb, ze - rr)),
           ((xw, yb - rr, ze), (xw, -yb + rr, ze)), ((xw, -yb, ze - rr), (xw, -yb, za + rr))]
    ecken = [((xw, yb - rr, za), (xw, yb, za), (xw, yb, za + rr)),
             ((xw, yb, ze - rr), (xw, yb, ze), (xw, yb - rr, ze)),
             ((xw, -yb + rr, ze), (xw, -yb, ze), (xw, -yb, ze - rr)),
             ((xw, -yb, za + rr), (xw, -yb, za), (xw, -yb + rr, za))]
    kanten = []
    for (a, b), (p0, pe, p1) in zip(pts, ecken):
        kanten.append(Line(a, b))
        k = 1 - 1 / math.sqrt(2)            # Bogenmitte der 90-Grad-Ecke
        pm = (p0[0], pe[1] + (p0[1] - pe[1] + p1[1] - pe[1]) * k, pe[2] + (p0[2] - pe[2] + p1[2] - pe[2]) * k)
        kanten.append(ThreePointArc(p0, pm, p1))
    teile.append(wulst_pfad(kanten, RAHMEN_R))

    # Eckzwickel (Foto BV: rote Winkelbleche in den Rahmenecken): Dreieck mit hohl gerundeter
    # Hypotenuse, 1.0 dick; die spitzen Enden liegen im Rollwulst (keine freien duennen Spitzen)
    L = ZWICKEL
    for sy in (-1, 1):
        for zc, sz in ((za, 1), (ze, -1)):
            yc = sy * yb
            pl = Plane.YZ.offset(-0.4)
            dreieck = pl * Polygon((yc, zc), (yc - sy * L, zc), (yc, zc + sz * L), align=None)
            kehle = pl * Pos(yc - sy * 0.95 * L, zc + sz * 0.95 * L) * Circle(0.8 * L)
            teile.append(extrude(dreieck - kehle, amount=1.0))

    # drei senkrechte Rundstaebe auf den Vierteln der Grillbreite (der mittlere ersetzt den
    # frueheren Mittelsteg); Enden laufen in den Rollwulst
    for i in range(1, GRILL_STAEBE + 1):
        y = -yb + i * g_b / (GRILL_STAEBE + 1)
        teile.append(stab_z(g_z0 - 0.3, g_z1 + 0.3, STAB_X, y, STAB_R))

    # Ring um das Kurbelloch (aufgesetzter Kragen, hinter der Pumpe)
    ring = Pos(EINSENK, 0, KURBEL_Z) * Rot(0, -90, 0) * (
        Cylinder(KURBEL_D / 2 + 1.4, 0.6 + EINSENK, align=(Align.CENTER, Align.CENTER, Align.MIN))
        - Cylinder(KURBEL_D / 2, 0.6 + EINSENK, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    teile.append(ring)

    # Abschlusswulst ueber dem Sockel (Sockelblech-Kante unter dem Grill)
    teile.append(stab_y(-KM_B / 2 + WAND + 0.2, KM_B / 2 - WAND - 0.2, 0.2, g_z0 - RAHMEN_R - 1.6, 0.6))

    teile += _kuehlerverschluss()
    km = km.fuse(*teile)
    return km, (g_b, g_h, g_z0)


def maske_zier():
    """Fluegellogo (Kappe) und Typschild (linke Maskenseite, unter dem Scheinwerfer), Chrom/Blech."""
    g_b, g_h, g_z0 = _grill()
    z_logo = (g_z0 + g_h + RAHMEN_R + KM_H - KM_R_VORN) / 2
    logo = hanomag_logo(plane_front(z_logo))

    # Typschild: Platte mit Rand und 4 Nieten, auf der linken Maskenseite
    sx, sz, sb, sh = TYPSCHILD
    pl = plane_side(sx, sz, -1, y_abs=KM_B / 2)
    schild = extrude(pl.offset(-EINSENK) * RectangleRounded(sb, sh, 0.6), amount=0.5 + EINSENK)
    schild -= extrude(pl.offset(0.3) * RectangleRounded(sb - 1.6, sh - 1.6, 0.4), amount=0.3)
    for dx in (-sb / 2 + 1.0, sb / 2 - 1.0):
        for dz in (-sh / 2 + 1.0, sh / 2 - 1.0):
            schild += Pos(pl.from_local_coords((dx, dz, 0.5))) * Sphere(0.4)
    return [logo, schild]


def gitter(g_b, g_h, g_z0):
    """Drahtgitter-Einsatz hinter den senkrechten Staeben (innen an der Maskenwand).
    Zwei Lagen wie ein Drahtgewebe: vorn die senkrechten, dahinter die waagerechten Draehte,
    jede Lage mit eigenem Rahmen (je ein Solid, Lagen liegen flaechig aneinander).
    So entfallen die ~1700 Kreuzungs-Booleans (Bauzeit Sekunden statt Minuten)."""
    w, h = g_b + 2.0, g_h + 2.0
    lage = GITTER_DICKE / 2 + 0.1
    ny = int((w - 2) / GITTER_TEILUNG)
    nz = int((h - 2) / GITTER_TEILUNG)
    zc = g_z0 + g_h / 2

    def lage_bauen(x, senkrecht):
        with BuildSketch(Plane.YZ.offset(x)) as sk:
            with Locations((0, zc)):
                Rectangle(w, h)
                Rectangle(w - 2, h - 2, mode=Mode.SUBTRACT)
                if senkrecht:
                    with GridLocations(GITTER_TEILUNG, 0, ny, 1):
                        Rectangle(GITTER_STEG, h - 1)
                else:
                    with GridLocations(0, GITTER_TEILUNG, 1, nz):
                        Rectangle(w - 1, GITTER_STEG)
        return extrude(sk.sketch, amount=lage)

    return Compound(children=[lage_bauen(GITTER_X, True), lage_bauen(GITTER_X + lage, False)])


# ------------------------------------------------------------------
# Haube
# ------------------------------------------------------------------
def _haube_aussen():
    hh = KM_H - H_UNTEN
    b = Pos(H_X0, 0, H_UNTEN) * Box(H_L, H_B, hh, align=(Align.MIN, Align.CENTER, Align.MIN))
    return fillet(b.edges().filter_by(Axis.X).group_by(Axis.Z)[-1], H_R_DACH)


def _ausschnitt():
    """Motorausschnitt beider Seiten als Werkzeugkoerper: von SEG_X1 bis hinter das Haubenende
    (hinten offen), unten offen, Oberkante HAUBE_BAND_Z, Ecke vorn oben mit BOGEN_R."""
    xa, x1 = H_X0 + SEG_L, H_X0 + H_L + 10
    z0 = H_UNTEN - 10
    with BuildSketch(Plane.XZ) as s:
        with Locations(((xa + x1) / 2, (z0 + BOGEN_OBEN) / 2)):
            Rectangle(x1 - xa, BOGEN_OBEN - z0)
        fillet(s.vertices().group_by(Axis.X)[0].sort_by(Axis.Y)[-1], BOGEN_R)
    return extrude(s.sketch, amount=H_B, both=True)


def _profil_sicke(pl: Plane):
    """Sickenquerschnitt (Trapez, 0.5 hoch, oben 0.6, an der Wand 1.2 breit, 0.3 eingesenkt).
    Lokales x = quer zur Sicke in der Wand, lokales y = Wandnormale nach aussen."""
    a0, a1 = -EINSENK, SICKE_H
    return pl * Polygon((-0.8, a0), (0.8, a0), (0.3, a1), (-0.3, a1), align=None)


def _profil_bordel(pl: Plane):
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


def _sicke_gerade(profil, p0, p1, quer, side):
    """Profil von p0 nach p1 extrudieren; quer = Querrichtung (lokales x) in der Wand."""
    p0, p1 = Vector(*p0), Vector(*p1)
    d = p1 - p0
    yn = Vector(0, side, 0)
    pl = Plane(origin=p0, x_dir=Vector(*quer), z_dir=Vector(*quer).cross(yn))
    return extrude(profil(pl), amount=d.length, dir=d.normalized())


def _sicke_bogen(profil, cx, cz, r_bahn, y, w_ende, side):
    """Profil auf dem Kreisbogen um (cx, cz) von 180 Grad (vorn) bis w_ende drehen.
    Lokales x zeigt zum Bogenmittelpunkt (= zur Ausschnittseite). Flaechen: Ebene/Kegel/Torus."""
    yn = Vector(0, side, 0)
    xd = Vector(1, 0, 0)
    pl = Plane(origin=(cx - r_bahn, y, cz), x_dir=xd, z_dir=xd.cross(yn))
    return revolve(profil(pl), axis=Axis((cx, y, cz), (0, 1, 0)), revolution_arc=180 - w_ende)


def _dachsicke(y, x0, x1):
    """Laengssicke auf dem Haubendach bei y (Trapezprofil, Normale +Z)."""
    pl = Plane(origin=(x0, y, KM_H), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    return extrude(_profil_sicke(pl), amount=x1 - x0)


def _bogen_geometrie():
    """Lage des Ausschnittbogens: (xa, cx, cz, rs) mit rs = Radius der Bogensicke."""
    xa = H_X0 + SEG_L
    cx, cz = xa + BOGEN_R, BOGEN_OBEN - BOGEN_R
    rs = BOGEN_R + (SICKE_Z - BOGEN_OBEN)          # Bogensicke laeuft tangential in die untere Laengssicke
    return xa, cx, cz, rs


def _typ_feld_z():
    return TYP_Z - TYP_FELD_H / 2, TYP_Z + TYP_FELD_H / 2


def _seitensicken(side):
    """Sicken, Bordelrand und Nieten einer Seitenwand.
    Alle Sicken sind Trapezprofile (Ebenen/Kegel), der Rand ein Band mit Rundung - so gibt es nur
    analytische Flaechen und kreisfoermige bzw. gerade Schnittkanten mit der Wand."""
    yw = side * H_B / 2                               # Wandaussenseite
    xe = H_X0 + H_L
    xa, cx, cz, rs = _bogen_geometrie()
    teile = []

    # gebordelter Rand entlang des Motorausschnitts (senkrecht, Bogen, waagerecht bis hinten)
    teile.append(_sicke_gerade(_profil_bordel, (xa, yw, H_UNTEN - 2), (xa, yw, cz), (1, 0, 0), side))
    teile.append(_sicke_bogen(_profil_bordel, cx, cz, BOGEN_R, yw, 90, side))
    teile.append(_sicke_gerade(_profil_bordel, (cx, yw, BOGEN_OBEN), (xe + 2, yw, BOGEN_OBEN), (0, 0, -1), side))

    # Bogensicke parallel zum Ausschnitt; oben tangential in die untere Laengssicke, unten bis zur
    # kurzen Quersicke ueber dem Typfeld
    xs = cx - rs
    teile.append(_sicke_gerade(_profil_sicke, (xs, yw, SICKE_VORN_Z - 0.3), (xs, yw, cz), (1, 0, 0), side))
    teile.append(_sicke_bogen(_profil_sicke, cx, cz, rs, yw, 90, side))

    # Laengssicken im Schriftband: untere (vorn bis zur Bogensicke geteilt) und obere, hinten bis zur Kante
    x_v = H_X0 + 1.6
    teile.append(_sicke_gerade(_profil_sicke, (x_v, yw, SICKE_Z), (cx, yw, SICKE_Z), (0, 0, 1), side))
    teile.append(_sicke_gerade(_profil_sicke, (cx, yw, SICKE_Z), (xe + 2, yw, SICKE_Z), (0, 0, 1), side))
    teile.append(_sicke_gerade(_profil_sicke, (x_v, yw, SICKE_OBEN_Z), (xe + 2, yw, SICKE_OBEN_Z), (0, 0, 1), side))
    # kurze Quersicke im vorderen Segment, endet in der Bogensicke
    teile.append(_sicke_gerade(_profil_sicke, (x_v, yw, SICKE_VORN_Z), (xs + 0.3, yw, SICKE_VORN_Z), (0, 0, 1), side))

    # Nietreihe an der Vorderkante (Anschluss Maske); frei lassen: Haubenhalter, Typfeld, Sicken
    yn = side * (H_B / 2 + 0.6 - NIET_R)
    n = 13
    z_a, z_e = H_UNTEN + 3, KM_H - H_R_DACH - 2
    z_halter = (SICKE_Z + SICKE_OBEN_Z) / 2
    f0, f1 = _typ_feld_z()
    for i in range(n):
        z = z_a + i * (z_e - z_a) / (n - 1)
        if abs(z - z_halter) < 5.5 or f0 - 1.0 < z < f1 + 1.0:
            continue
        if any(abs(z - zs) < 1.6 for zs in (SICKE_Z, SICKE_OBEN_Z, SICKE_VORN_Z)):
            continue
        teile.append(Pos(H_X0 + 1.8, yn, z) * Sphere(NIET_R))
    return teile


def _typfeld(side):
    """Erhabenes, eingerahmtes Feld fuer "K55E" vorn unten im Seitensegment (PK):
    Platte PRAEGE_H hoch mit TYP_RAHMEN breitem Rand, Feldboden 0.3 ueber der Wand,
    Buchstaben TYP_H ueber der Wand."""
    pl = plane_side(TYP_X, TYP_Z, side)
    feld = extrude(pl.offset(-EINSENK) * RectangleRounded(TYP_FELD_B, TYP_FELD_H, 0.8),
                   amount=PRAEGE_H + EINSENK)
    feld -= extrude(pl.offset(0.3) * RectangleRounded(TYP_FELD_B - 2 * TYP_RAHMEN,
                                                      TYP_FELD_H - 2 * TYP_RAHMEN, 0.4), amount=1.0)
    return [feld] + buchstaben(pl, TYP, TYP_TEILUNG, TYP_VERSAL, TYP_H, fase=TYP_FASE,
                              abstand=TYP_ABSTAND)


def _haubenhalter(side):
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


def haube():
    """Motorhaube x 210..1080: Blech 1.6 mm, Dachkantenradius, grosse Motorausschnitte mit
    Bordelrand, Schriftband mit Sicken und HANOMAG, Typfeld K55E, Dachsicken, Nieten,
    Haubenhalter, Rohrdurchbrueche mit Kragen. Druck stehend auf der Hinterkante."""
    outer = _haube_aussen()
    f = outer.faces()
    hb = offset(outer, amount=-WAND,
                openings=[f.sort_by(Axis.X)[0], f.sort_by(Axis.X)[-1], f.sort_by(Axis.Z)[0]])
    hb -= _ausschnitt()

    teile = []
    # Versteifungswinkel innen an der Hinterkante (Dach und Schriftband ueber dem Ausschnitt)
    innen1 = offset(outer, amount=-WAND + 0.1)
    innen2 = offset(outer, amount=-WAND - 1.2)
    xe = H_X0 + H_L
    teile.append((innen1 - innen2) & (Pos(xe - 3.0, 0, BOGEN_OBEN + 1.0) *
                                      Box(3.0, H_B, KM_H, align=(Align.MIN, Align.CENTER, Align.MIN))))

    for side in (-1, 1):
        teile += _seitensicken(side)
        teile += _haubenhalter(side)
        teile += buchstaben(plane_side(SCHRIFT_X, SCHRIFT_Z, side), SCHRIFT, SCHRIFT_TEILUNG,
                            SCHRIFT_VERSAL, SCHRIFT_H)
        teile += _typfeld(side)

    # zwei Laengssicken auf dem Dach (PK), hinter der vorderen Nietreihe bis zur Hinterkante
    for sy in (-1, 1):
        teile.append(_dachsicke(sy * DACH_SICKE_Y, H_X0 + 3.5, xe + 2))

    # Nietreihe an der vorderen Dachkante (Dachsicken frei lassen)
    n = 9
    for i in range(n):
        y = -(H_B / 2 - H_R_DACH - 1.5) + i * (H_B - 2 * H_R_DACH - 3) / (n - 1)
        if abs(abs(y) - DACH_SICKE_Y) < 1.8:
            continue
        teile.append(Pos(H_X0 + 1.8, y, KM_H + 0.6 - NIET_R) * Sphere(NIET_R))

    # Kragen an den Rohrdurchbruechen (Auspuff rechts, Ansaugrohr links)
    for (x, y, d) in (AUSPUFF, ANSAUG):
        kr = Pos(x, y, KM_H - EINSENK) * Cylinder(d / 2 + 1.6, 0.6 + EINSENK,
                                                  align=(Align.CENTER, Align.CENTER, Align.MIN))
        kr = fillet(kr.edges().group_by(Axis.Z)[-1].sort_by(SortBy.RADIUS)[-1:], 0.4)
        teile.append(kr)

    hb = hb.fuse(*teile)
    # Durchbrueche zuletzt (schneiden Dach und Kragen sauber)
    for (x, y, d) in (AUSPUFF, ANSAUG):
        hb -= Pos(x, y, KM_H - 5) * Cylinder(d / 2, 10, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Abschluss: alles, was ueber Vorder-/Hinterkante oder Unterkante steht, kappen
    hb &= Pos(H_X0, 0, H_UNTEN) * Box(H_L, H_B + 20, KM_H, align=(Align.MIN, Align.CENTER, Align.MIN))
    return hb


# ------------------------------------------------------------------
# Scheinwerfer
# ------------------------------------------------------------------
def scheinwerfer(side):
    """Scheinwerfer oben an der Maskenseite mit Winkelhalter (wird mit side=-1 gebaut, rechts
    gespiegelt). Die Lampe liegt mit dem Ring an der Maskenseite an (|y| 355 = SW_Y - SW_D/2).
    Liefert {material: [solids]}: Gehaeuse, Halter, Kabel schwarz; Ring, Reflektor chrom; Glas."""
    r = SW_D / 2
    ra = r - 1.4                                    # lichte Weite Ring / Glas
    y = side * SW_Y

    # Gehaeuse: zylindrischer Topfrand + gestreckte Halbkugel nach hinten, Nabe unten
    rt = r - 0.3
    topf = Rot(0, 90, 0) * Cylinder(rt, SW_TOPF, align=(Align.CENTER, Align.CENTER, Align.MIN))
    kuppel = scale(Sphere(rt), by=(SW_TIEFE, 1, 1))
    kuppel = Pos(SW_TOPF, 0, 0) * (kuppel & Box(rt, 2 * rt + 1, 2 * rt + 1, align=(Align.MIN, Align.CENTER, Align.CENTER)))
    nabe = Pos(1.5, 0, -rt + 1.5) * Cylinder(1.8, 2.2, align=(Align.CENTER, Align.CENTER, Align.MAX))
    gehaeuse = topf.fuse(kuppel, nabe)
    gehaeuse -= Pos(-0.1, 0, 0) * Rot(0, 90, 0) * Cylinder(ra, 0.6, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Chromring vorn, aussen verrundet (Aussendurchmesser = SW_D)
    ring = Rot(0, -90, 0) * (Cylinder(r, SW_RING_L, align=(Align.CENTER, Align.CENTER, Align.MIN))
                            - Cylinder(ra, SW_RING_L, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    ring = fillet(ring.edges().group_by(Axis.X)[0].sort_by(SortBy.RADIUS)[-1:], 0.6)

    # Reflektor (flache Schuessel) hinter dem Glas
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

    loc = Pos(SW_X, y, SW_Z)
    gehaeuse, ring, refl, birne, glas = (loc * s for s in (gehaeuse, ring, refl, birne, glas))

    # Winkelhalter: Fussplatte an der Maskenseite, Flachstahl-Arm unter die Lampe, Bolzen mit Muttern
    wand_y = side * KM_B / 2
    z_arm = SW_Z - rt - 2.2                          # Oberkante Arm
    x_h = SW_X + 1.5                                 # Bolzenachse (unter der Nabe)
    fuss = Pos(x_h - 1.5, wand_y + side * (0.6 - EINSENK), z_arm - 0.8) * Box(5.0, 1.2 + 2 * EINSENK, 6.0)
    fuss = fillet(fuss.edges().filter_by(Axis.Y), 0.8)
    arm = Pos(x_h, (wand_y + y) / 2, z_arm - 0.8) * Box(2.4, abs(y - wand_y), 1.6)
    arm += Pos(x_h, y, z_arm - 0.8) * Cylinder(1.2, 1.6)
    bolzen = Pos(x_h, y, z_arm - 2.6) * Cylinder(0.8, SW_Z - rt + 1.0 - (z_arm - 2.6),
                                                align=(Align.CENTER, Align.CENTER, Align.MIN))
    mutter_u = sechskant((x_h, y, z_arm - 1.6), (0, 0, -1), sw=2.4, hoehe=1.0)
    mutter_o = sechskant((x_h, y, z_arm), (0, 0, 1), sw=2.4, hoehe=0.8)
    halter = _vereinigen([fuss, arm, bolzen, mutter_u, mutter_o])
    for dz in (-2.6, 1.0):                           # zwei Schraubenkoepfe auf der Fussplatte
        halter = halter.fuse(sechskant((x_h - 2.6, wand_y + side * (1.2 - EINSENK), z_arm + dz),
                                       (0, side, 0), sw=1.6, hoehe=0.6))

    # Kabel vom Gehaeuseboden in einer Schlaufe in die Maskenseite
    mw_y = side * (KM_B / 2 - WAND / 2)              # Kabel endet in der Maskenwand
    kabel = rohr_glatt([(SW_X + 5.0, y, SW_Z - rt * 0.8),
                        (SW_X + 5.8, y + side * 0.5, z_arm - 4.0),
                        (SW_X + 5.8, (y + mw_y) / 2, z_arm - 6.0),
                        (SW_X + 5.8, mw_y + side * 1.5, z_arm - 5.0),
                        (SW_X + 5.8, mw_y, z_arm - 5.0)], 0.5, rb=2.0)
    gehaeuse = gehaeuse.fuse(Pos(SW_X + 5.0, y, SW_Z - rt * 0.8) * Sphere(0.8))   # Kabeltuelle
    return {"schwarz": [gehaeuse, halter, kabel], "chrom": [ring, refl], "glas": [glas, birne]}
