"""Motor Hanomag D57 (4 Zyl.-Vorkammerdiesel, 5702 cm3, Bohrung ~110, Hub ~150) mit Kuehler,
Luefter, Riementrieb, Einspritzanlage, Lichtmaschine, Anlasser und Schwungradgehaeuse;
Auspuffanlage und Ansaugung.

Original-mm, X ab Vorderkante Kuehlermaske nach hinten, Y nach rechts, Z ab Boden.
Linke Seite (y < 0): Der Kasten "HANOMAG DIESEL" ist die Einspritzpumpe (Hanomag-Eigenbau, es gibt keine
Bosch-Reihenpumpe): Gusskasten mit Schriftplatte, Rahmendeckel mit den 4 Druckventilhaltern, runder Reglerkopf an
der Stirn (Antrieb ueber ein Gehaeuse vom Steuergehaeuse), Elementverschluesse unten, Foerderpumpe (Messing) mit
Handpumpe. Dazu Vorreiniger, Kraftstoff-Doppelfilter oben, Stoesselkammerdeckel, Anlasser am Schwungradgehaeuse,
Ansaugkruemmer. Belege: Haendlerfotos traktorteile-maier R40-94 (ausgebaute Pumpe D52/D57), Nordhorn 1:37-1:49
(eingebaut, linke Seite).
Rechte Seite (y > 0): Lichtmaschine vorn oben, Oelfilter, Oelmessstab, Abgaskruemmer.

Fotobefund: Foto BS (rechte Seite): Haube endet bei x ~1080, Auspuffrohr steht bei x ~640 aus
dem Dach; der Motor ist durch den grossen Seitenausschnitt sichtbar. fz_06m (linke Seite):
Pumpe vorn unten, Deckel "HANOMAG DIESEL" unten dahinter, Filterglocke oben.
Zylinderabstand ZYL_T = 155: Block x 400..1030, Steuergehaeuse/Riementrieb davor
(x 364..402), Schwungradgehaeuse x 1030..FLANSCH_GLOCKE_X.

Raumgrenzen (common.py): Maske x 0..210, z 450..1410; Haube x 210..1080,
Dach aussen z 1410, Wand innen y = +-332; Motorausschnitt offen x ~360..1080, z 620..1090 (Band 1090..1410).
Motor innerhalb y +-325, x 225 (Kuehler) .. FLANSCH_GLOCKE_X = 1090; Tank x 1085..1455 ab z 1000
(Schwungradgehaeuse bleibt darunter, Oberkante <= 950); Kupplungsglocke (rumpf.py) ab x 1090.
Laengstraeger y = +-(195..285), z = 380..520, Querblattfeder x = 505..615 bis z = 580.
Auspuff und Ansaugrohr durchs Haubendach bei AUSPUFF_XY / ANSAUG_XY.

Oeffentliche Teilfunktionen (von modell.py): motor() und auspuff(), beide liefern einen Sammler.
"""
from __future__ import annotations

import math
from collections.abc import Sequence

from build123d import (
    Align,
    Axis,
    Box,
    Circle,
    Cylinder,
    Location,
    Part,
    Plane,
    Polygon,
    Pos,
    Rectangle,
    Rot,
    Sphere,
    Text,
    Torus,
    Vector,
    chamfer,
    extrude,
    fillet,
    scale,
)

from .common import (
    ANSAUG_D,
    ANSAUG_XY,
    AUSPUFF_D,
    AUSPUFF_XY,
    FLANSCH_GLOCKE_X,
    FONT,
    HAUBE_DACH_Z,
    KD_X,
    TANK_Z0,
    TRAEGER_Z1,
    Sammler,
    box,
    kasten_rund,
    rad_x,
    rad_y,
    ring_x,
    rohr_glatt,
    schraubenkreis,
    schraubenreihe,
    sechskant,
    stab,
)

Punkt = Sequence[float]

# ======================================================================================
# Parameter (Original-mm, nach Bauteil gegliedert)
# ======================================================================================

# --- Bezug zur Haube ---
HAUBE_TOP = HAUBE_DACH_Z                # Dach aussen (1410)
HAUBE_KRAGEN = HAUBE_TOP + 6.4          # Oberkante Kragen der Haubendurchbrueche (0,8 mm Modell)

# --- Block, Kopf, Wanne ---
ZYL_T = 155.0                           # Zylinderabstand (Bohrung ~110)
ZYL_X = [480.0 + i * ZYL_T for i in range(4)]   # Zylindermitten 480, 635, 790, 945
X_VORN, X_HINTEN = 380.0, 1030.0        # Block inkl. Steuergehaeuse
Y_BLOCK = 190.0
Z_KW = 600.0                            # Kurbelwelle
Z_WANNE = 320.0                         # Unterkante Oelwanne
Z_KURBEL_U = 585.0                      # Unterkante Kurbelgehaeuse vorn (ueber der Querfeder)
DZ_OBEN = 70.0                          # Absenkung von Kopf und Aufbauten (Bezug: Kopf-Unterkante 1000)
Z_KOPF0 = 1000.0 - DZ_OBEN              # Block-Oberkante / Kopf-Unterkante (930)
Z_KOPF1 = Z_KOPF0 + 105.0               # Oberkante Zylinderkopf (1035)
Z_VD = Z_KOPF1 + 48.0                   # Oberkante Ventildeckel (1083); Hutmuttern bis ~1098
Z_AK0 = Z_KOPF1 - 26.0                  # Unterkante Ansaugkruemmer
Z_TRAEGER = TRAEGER_Z1                  # Oberkante Laengstraeger (520)
Z_DUESE = Z_KOPF0 + 50.0                # Duesenhalter (seitlich im Kopf)
SCHEIBE_MIN = 4.0                       # Mindestdicke Unterlegscheibe (0,5 mm Modell)

# --- Riementrieb und Luefter (Ebene x = RIEMEN_X0..X1), Kreise (y, z, Wirkradius) ---
RIEMEN_X0, RIEMEN_X1 = 364.0, 380.0
SCHEIBE_KW = (0.0, Z_KW, 105.0)
SCHEIBE_WP = (0.0, 860.0, 70.0)
SCHEIBE_LIMA = (255.0, 960.0, 46.0)     # Lichtmaschine Mitte z 960 (Fotos DSC04729/33); Abgaskruemmer liegt darueber
LUEFTER_X, LUEFTER_R = 354.0, 245.0
HAUBE_BLECH = 10.0                      # Luefterhaube (>= 1,2 mm Modell)

# --- Kuehler (hinter der Maske, z innerhalb MASKE_UK 525 .. Dach) ---
K_X0, K_X1 = 225.0, 335.0
K_Y = 320.0
K_Z0, K_Z1 = 520.0, HAUBE_DACH_Z - 77.0   # Unterkante Wasserkasten = MASKE_UK 525 - 5 (Nordhorn 0:10-0:30: kein Kuehler
                                          # sichtbar, Querblech/Traeger darunter); Oberkante unter der gewoelbten Dachecke (1333)
K_NETZ_Z0, K_NETZ_Z1 = 580.0, HAUBE_DACH_Z - 167.0   # Netz bis 1243
K_ZULAUF_Z = K_NETZ_Z1 + 60.0           # Hoehe Zulaufstutzen/Oberschlauch (1303)
KD_Z = HAUBE_DACH_Z - 13.0              # Unterseite Maskendach innen (~1397, Wand 1,6 mm Modell)

# --- Einspritzanlage (linke Seite): der Kasten SD_* ist die Pumpe ---
DV_TEILUNG = 55.0                       # Teilung der Druckventilhalter (Haendlerfotos R40-94)
DV_Y = -262.0                           # Druckventilhalter auf dem Rahmendeckel
DL_R = 3.5                              # Radius der Druckleitungen
DL_H = 1006.0                           # waagerechte Leitungsabschnitte (unter dem Ansaugtopf z 1020, neben dem Kruemmer)
DL_Y = [-270.0 - 10.0 * i for i in range(4)]   # gestaffelt nach aussen (i = vorderster Zylinder innen), keine Kreuzung
FILTER_X = (655.0, 770.0)               # zwei Kraftstofffilter (Nordhorn 1:34/1:43: Zylinder Ø ~105 stehen fast aneinander,
                                        # Mittenabstand ~115 statt 231; Massstab Kasten 360 = 745 px)
FILTER_Y = -270.0
FILTER_Z = 1095.0                       # Mitte der Glasbirnen (Ø 100); Oberteil liegt hinter dem Haubenband (z > 1090)
FILTER_KOPF_Z = FILTER_Z + 58.0         # Mitte Anschlusskopf (1153)
VR_X = 765.0                            # Vorreiniger mit Glasschale hinter dem Regler
# Nordhorn 1:37-1:49 / Haendlerfotos R40-94: messingfarbene Foerderpumpe mit Handpumpe unten vor dem Kasten
FP_X0, FP_X1 = 545.0, 650.0             # Pumpenkoerper (Nordhorn 1:34: Messingblock ~115 lang, x 535..650)
FP_Y0, FP_Y1 = -302.0, -252.0           # Pumpenkoerper quer
FP_Z0, FP_Z1 = 735.0, 785.0             # Pumpenkoerper senkrecht (unter dem Reglerkopf)
FP_KNOPF_X, FP_KNOPF_Y = 562.0, -288.0  # Handpumpe: Raendelstange (Oe 20) vor dem Regler
FP_KNOPF_H = 60.0                       # Hoehe der Stange ueber dem Koerper
VF_X, VF_Y = 505.0, -268.0              # Vorreiniger (Glasschale Oe 56, Mitte x 420..505 / z 830..845)
VF_Z0, VF_Z1 = 826.0, 872.0             # Glasschale Ø 36 x 46 (Nordhorn 1:34); Kopf bis 888
VF_R = 18.0                             # Radius der Glasschale

# --- Seitendeckel / Kastenpumpe "HANOMAG DIESEL" (unten hinter der Pumpe, ueber dem Anlasser) ---
# Nordhorn 1:37-1:49 (linke Seite, Kamera seitlich; Massstab Kastenbreite 360, Fensterblech-Lippe z 808): Gussgehaeuse mit
# Schriftfeld z 815..890, darueber umlaufender Deckelflansch mit Schrauben, darauf aufgesetzter Blechdeckel mit Einfuellkappe.
# Der Kasten steht ~100 vom Block ab (Block y -190).
SD_X0, SD_X1 = 665.0, 1025.0                                   # Gussgehaeuse (Nordhorn: 360 breit)
SD_Z0, SD_ZF0, SD_Z1 = 785.0, 912.0, 936.0                     # Unterkante / Flansch-Unterkante / Flansch-Oberkante (Deckelfuge)
SD_Y0, SD_Y1 = -184.0, -285.0                                  # Block-Seite (leicht eingesenkt) bis Gehaeuse-Aussenflaeche
SD_Y_OBEN = -238.0                                             # Flansch/Deckel nur aussen (Druckleitungen y -228 daneben)
SD_DK_Z1 = 958.0                                               # Deckelplatte (flach), Rahmenrand 8 hoeher
SD_RAHMEN_H = 8.0
SD_XM, SD_ZM = (SD_X0 + SD_X1) / 2, (SD_Z0 + SD_ZF0) / 2       # Mitte Schriftfeld 845 / 848,5
SD_Y_PLATTE = SD_Y1 - 8.0                                      # Plattenflaeche
SD_Y_ERHABEN = SD_Y_PLATTE - 6.0                               # erhabenes Kissenfeld
DV_X = [SD_XM + (i - 1.5) * DV_TEILUNG for i in range(4)]      # Druckventilhalter 762..927 auf dem Deckel
# Reglerkopf an der Stirn (Haendlerfotos: rund, Oe ~104, ~80 lang), Achse x
REG_X0, REG_X1 = SD_X0 - 60.0, SD_X0
REG_Y, REG_Z, REG_R = -243.0, 840.0, 44.0   # Nordhorn 1:34: Reglerkopf Ø ~88, ~60 lang (Massstab Kasten 360)
SK_X0, SK_X1, SK_Z0, SK_Z1 = 495.0, 580.0, 795.0, 865.0        # Stoesselkammerdeckel (vorn, hinter den Druckleitungen)

# --- Schwungradgehaeuse ---
SG_X0, SG_X1, SG_X2 = X_HINTEN, FLANSCH_GLOCKE_X - 12, FLANSCH_GLOCKE_X   # SG_X2 = Flansch Glocke
SG_Z, SG_R = 640.0, 300.0               # Oberkante 940 < Tank-Unterkante TANK_Z0 und <= 950
SG_OBEN = min(950.0, TANK_Z0 - 50.0)    # Schnitt oben (Kupplungsglocke <= 950, Tank darueber)

# --- Anlasser (rechts am Schwungradgehaeuse, schwarz; Fotos DSC04729/33/35); der linke Anlasser ist nicht belegt ---
ANL_Y, ANL_Z = 272.0, 870.0             # Video 2:44/2:58: Unterkante ~812 direkt ueber der Fensterblech-Lippe 808

# --- Rechte Seite: Oelfilter, Oelmessstab ---
OELF_X, OELF_Z = 720.0, 840.0           # Oelfilter-Flanschplatte am Block (Spec 650/930 kollidiert mit Lichtmaschine/Kruemmer)
OELF_R, OELF_L = 34.0, 52.0                # Kanister Ø 68, Zylinderlaenge zwischen den Kugelenden (Gesamt 120)
MESS_X = 790.0                          # Oelmessstab (vor dem Anlasser)

# --- Auspuff (Abgaskruemmer rechts) ---
Z_KRUEMMER = Z_KOPF1 + 49.0             # Achse Abgassammelrohr 1084 (ueber der Lichtmaschine); Oberkante 1120 verschwindet
                                        # teils hinter dem Band ab 1090 (Video 177-182: nur dunkler Spalt unter dem Bogen;
                                        # tiefer schneidet es Einspritzleitungen/Raeder; Material schwarz)
RK_KRUEMMER = 36.0
YK_KRUEMMER = 255.0                     # Sammelrohr-Lage in y (ueber der Lichtmaschine)
AUSPUFF_Z_TOP = 1850.0                  # Rohrende (Nordhorn 2:46 / Foto 0:10: ~440 ueber dem Dach, ~110 ueber der Ansaugkappe)

# --- Ansaugung (Oelbadluftfilter links) ---
ANSAUG_R_ROHR = ANSAUG_D / 2 - 5        # 33
ANSAUG_ZP0, ANSAUG_ZP1 = 1020.0, 1194.0  # Topf (Unterkante ~1020, Ø 190..210)
ANSAUG_R_TOPF = 95.0                    # y = iy - 95 = -331 bleibt innerhalb der Wand (-332)
ANSAUG_ZS = HAUBE_KRAGEN - 0.5          # Gummimanschette auf dem Kragen
# Kappe (Nordhorn 0:10/2:46, Massstab Deckel Ø 140): glatter Becher Ø 92 x 115, Deckel Ø 140 x 44
ANSAUG_Z_TOP = 1740.0
ANSAUG_KAPPE_DECKEL_H, ANSAUG_KAPPE_BECHER_H = 44.0, 115.0
ANSAUG_KAPPE_Z0 = ANSAUG_Z_TOP - ANSAUG_KAPPE_DECKEL_H - ANSAUG_KAPPE_BECHER_H   # Becher-Unterkante 1581


# ======================================================================================
# Helfer
# ======================================================================================
def schraube(p: Punkt, normal: Punkt, sw: float = 24, hoehe: float = 14, scheibe: bool = True) -> list[Part]:
    """Sechskantkopf mit Unterlegscheibe; Scheibe mindestens SCHEIBE_MIN dick (druckbar),
    der Kopf sitzt auf der Scheibe. (Anders als common.schraube: Scheibe 4 statt 5 mm, Kopf in die Scheibe versenkt.)"""
    pl = Plane(origin=Vector(*p), z_dir=Vector(*normal))
    if not scheibe:
        return [sechskant(p, normal, sw, hoehe)]
    d = max(SCHEIBE_MIN, hoehe * 0.2)
    kopf = Vector(*p) + Vector(*normal).normalized() * (d - 0.5)
    return [extrude(pl * Circle(sw * 0.95), amount=d), sechskant(kopf, normal, sw, hoehe)]


def _gummi_schelle(t: Sammler, p: Punkt, achse: Punkt, r: float, b: float = 10, schloss: Punkt = (0, 0, 1)) -> None:
    """Schlauchschelle (blanker Ring) an Punkt p, Achse als Vektor; Schraubschloss Richtung `schloss`."""
    pl = Plane(origin=Vector(*p) - Vector(*achse).normalized() * (b / 2), z_dir=achse)
    ring = extrude(pl * Circle(r + 5), amount=b) - extrude(pl * Circle(r - 1), amount=b)
    t.mat("blank", ring)
    # Schraubschloss der Schelle
    n = Vector(*achse).normalized()
    quer = Vector(*schloss)
    quer = (quer - n * quer.dot(n)).normalized()
    t.mat("blank", Pos(*(Vector(*p) + quer * (r + 7))) * Box(12, 12, 12))


def _riemen_profil(kreise: Sequence[Punkt], dr: float) -> Part:
    """Konvexe Huelle aus Kreisen (y, z, r+dr) als Skizze in lokalen Koordinaten."""
    cy = sum(k[0] for k in kreise) / len(kreise)
    cz = sum(k[1] for k in kreise) / len(kreise)
    ks = sorted(kreise, key=lambda k: math.atan2(k[1] - cz, k[0] - cy))   # gegen Uhrzeigersinn
    pts = []
    for i in range(len(ks)):
        (y1, z1, r1), (y2, z2, r2) = ks[i], ks[(i + 1) % len(ks)]
        r1, r2 = r1 + dr, r2 + dr
        dy, dz = y2 - y1, z2 - z1
        L = math.hypot(dy, dz)
        ey, ez = dy / L, dz / L
        fy, fz = ez, -ey                      # rechts der Laufrichtung = aussen
        a = (r1 - r2) / L
        b = math.sqrt(1 - a * a)
        ny, nz = a * ey + b * fy, a * ez + b * fz
        pts += [(y1 + r1 * ny, z1 + r1 * nz), (y2 + r2 * ny, z2 + r2 * nz)]
    sk = Polygon(*pts, align=None)
    for (y, z, r) in ks:
        sk += Pos(y, z) * Circle(r + dr)
    return sk


def _ebene_x(x: float) -> Plane:
    """Skizzenebene senkrecht zu X, lokale Koordinaten (u, v) = (y, z)."""
    return Plane(origin=(x, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))


def _schrift_mass(t: Sammler, mitte_x: float, mitte_z: float, y_flaeche: float, txt: str, breite: float, hoehe: float,
                  erhaben: float = 5.0) -> None:
    """Erhabene Schrift auf einer Flaeche mit Normale -Y, auf Sollbreite und Soll-Versalhoehe gestreckt
    (Mitte mitte_x / mitte_z). Material blank."""
    roh = extrude(Text(txt, font_size=40, font_path=FONT, align=(Align.CENTER, Align.CENTER)), amount=1.0)
    bb = roh.bounding_box()
    roh = Pos(-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, 0) * roh
    roh = scale(roh, by=(breite / bb.size.X, hoehe / bb.size.Y, 1.0))
    roh = scale(roh, by=(1.0, 1.0, (erhaben + 0.5)))               # Dicke 1 -> erhaben + 0,5 (Einsenkung)
    pl = Plane(origin=(mitte_x, y_flaeche + 0.5, mitte_z), x_dir=(1, 0, 0), z_dir=(0, -1, 0))   # lokales +Y = +Z
    for dx, dz in ((0.7, 0.7), (-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7)):        # Strich fetter (Foto: kraeftige Schrift)
        t.mat("blank", Location(pl) * Pos(dx, dz, 0) * roh)


# ======================================================================================
# Block, Kopf, Wanne
# ======================================================================================
def _gehaeuse(t: Sammler) -> None:
    """Kurbelgehaeuse, Zylinderblock mit Gussleisten, Steuergehaeuse mit Antriebsauge."""
    # Kurbelgehaeuse (vorn hochgezogen ueber der Querblattfeder)
    t.append(kasten_rund(400, X_HINTEN, -185, 185, Z_KURBEL_U, 800, 15))
    # Zylinderblock (Wassermantel), leicht breiter, mit Gussleisten
    t.append(kasten_rund(400, X_HINTEN - 10, -Y_BLOCK, Y_BLOCK, 780, Z_KOPF0, 20))
    for s in (-1, 1):
        t.append(box(405, X_HINTEN - 15, s * Y_BLOCK - 4, s * Y_BLOCK + 4, 775, 790))   # Leiste unten
        t.append(box(405, X_HINTEN - 15, s * Y_BLOCK - 4, s * Y_BLOCK + 4, Z_KOPF0 - 10, Z_KOPF0))  # Leiste oben
    # Steuergehaeuse vorn mit Auge fuer den Pumpenantrieb
    t.append(kasten_rund(X_VORN, 402, -170, 170, 490, 820, 40, Axis.X))
    t += schraubenreihe((X_VORN, -150, 510), (X_VORN, 150, 510), 5, (-1, 0, 0), 16, 6)


def _oelwanne(t: Sammler) -> None:
    """Oelwanne: tiefer Sumpf hinten, Flansch mit Schraubenreihe, Rippen, Ablassschraube."""
    xw0, xw1 = 650.0, X_HINTEN - 25
    seite = Polygon((xw0, Z_KURBEL_U), (xw0, 450), (xw0 + 130, Z_WANNE), (xw1, Z_WANNE), (xw1, Z_KURBEL_U),
                    align=None)
    wanne = extrude(Plane.XZ.offset(170) * seite, amount=-340)      # Plane.XZ: Normale -Y
    wanne = fillet(wanne.edges().filter_by(Axis.Y), 15)
    t.append(wanne)
    t.append(box(640, X_HINTEN - 15, -182, 182, Z_KURBEL_U - 12, Z_KURBEL_U))
    for s in (-1, 1):
        t += schraubenreihe((680, s * 182, Z_KURBEL_U - 6), (X_HINTEN - 50, s * 182, Z_KURBEL_U - 6),
                            6, (0, s, 0), 16, 6)
        for x in (790, 900):                                         # Verstaerkungsrippen
            t.append(box(x - 6, x + 6, s * 170 - (6 if s > 0 else -6), s * 170 + (6 if s > 0 else -6),
                         Z_WANNE + 30, Z_KURBEL_U - 12))
    t += schraube((X_HINTEN - 90, 0, Z_WANNE), (0, 0, -1), 26, 14)


def _motorfuesse_vorn(t: Sammler) -> None:
    """Motorfuesse vorn (auf den Laengstraegern)."""
    for s in (-1, 1):
        t.append(box(640, 720, s * 186, s * 282, Z_TRAEGER, Z_TRAEGER + 16))
        t.append(box(672, 688, s * 182, s * 270, Z_TRAEGER + 16, 700))
        t.append(box(640, 720, s * 182, s * 196, Z_TRAEGER + 16, 700))
        for x in (655, 705):
            t += schraube((x, s * 245, Z_TRAEGER + 16), (0, 0, 1), 22, 12)


def _block(t: Sammler) -> None:
    """Kurbelgehaeuse, Zylinderblock, Steuergehaeuse, Oelwanne, Motorfuesse."""
    _gehaeuse(t)
    _oelwanne(t)
    _motorfuesse_vorn(t)


def _zylinderkopf(t: Sammler) -> None:
    """Zylinderkopf mit Kopfschrauben."""
    kopf = box(400, X_HINTEN - 10, -185, 185, Z_KOPF0, Z_KOPF1)
    t.append(chamfer(kopf.edges().group_by(Axis.Z)[-1], 6))
    for s in (-1, 1):                                                # Kopfschrauben von oben
        for i in range(9):
            x = 425 + i * (X_HINTEN - 30 - 425) / 8                  # 2 je Zylinder + 1
            if s < 0 and abs(x - ANSAUG_XY[0]) < 62:
                continue                                             # unter dem Ansaugflansch
            t += schraube((x, s * 168, Z_KOPF1), (0, 0, 1), 22, 12)


def _ventildeckel(t: Sammler) -> None:
    """Ventildeckel mit Fussflansch, Laengssicken, Hutmuttern, Oeleinfuellstutzen."""
    t.append(kasten_rund(430, X_HINTEN - 40, -150, 150, Z_KOPF1, Z_KOPF1 + 10, 12))
    vd = box(440, X_HINTEN - 50, -140, 140, Z_KOPF1 + 10, Z_VD)
    vd = fillet(vd.edges().filter_by(Axis.X).group_by(Axis.Z)[-1], 24)
    vd = fillet(vd.edges().filter_by(Axis.Y).group_by(Axis.Z)[-1], 16)
    t.append(vd)
    for y in (-60, 60):
        t.append(box(495, X_HINTEN - 105, y - 7, y + 7, Z_VD - 2, Z_VD + 5))
    for x in (480, 640, 800, X_HINTEN - 90):                          # Hutmuttern
        t += schraube((x, 0, Z_VD), (0, 0, 1), 26, 10)
        t.append(Pos(x, 0, Z_VD + 6) * Sphere(9))
    xo = 560.0                                                        # Oeleinfuellstutzen
    t.mat("schwarz", Pos(xo, 85, Z_VD - 5) * Cylinder(30, 20, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("schwarz", Pos(xo, 85, Z_VD + 10) * Cylinder(36, 5, align=(Align.CENTER, Align.CENTER, Align.MIN)))


def _thermostat(t: Sammler) -> None:
    """Thermostatgehaeuse vorn auf dem Kopf, Stutzen nach vorn zum Kuehler."""
    z_th = Z_KOPF1 + 48.0                                             # Oberkante Thermostatgehaeuse
    t.append(kasten_rund(405, 465, -45, 45, Z_KOPF1, z_th, 12))
    t.append(rad_x(392, 0, Z_KOPF1 + 24, 24, 30))
    t += schraubenreihe((415, -35, z_th), (455, 35, z_th), 2, (0, 0, 1), 16, 7)


def _ansaugkruemmer(t: Sammler) -> None:
    """Ansaugkruemmer links mit 4 Flanschen und Steigflansch."""
    ak = kasten_rund(ZYL_X[0] - 45, ZYL_X[-1] + 50, -236, -185, Z_AK0, Z_KOPF1, 12, Axis.X)
    t.append(ak)
    for x in ZYL_X:
        t.append(kasten_rund(x - 45, x + 45, -198, -185, Z_AK0 - 4, Z_KOPF1, 8, Axis.Y))
        t += [sechskant((x + dx, -198, Z_AK0 + 14), (0, -1, 0), 18, 8) for dx in (-32, 32)]
    xa = ANSAUG_XY[0]                                                 # Steigflansch unter dem Ansaugrohr
    t.append(kasten_rund(xa - 50, xa + 50, -265, -180, Z_KOPF1 - 2, Z_KOPF1 + 10, 12))
    for dx in (-38, 38):
        for y in (-252, -193):
            t += schraube((xa + dx, y, Z_KOPF1 + 10), (0, 0, 1), 14, 7, scheibe=False)


def _duesenhalter(t: Sammler) -> None:
    """Duesenhalter (seitlich, je Zylinder) mit Flansch, Muttern und Anschlussstutzen unten; Leckoelleitung darueber."""
    for x in ZYL_X:
        t.append(kasten_rund(x - 28, x + 28, -195, -184, Z_DUESE - 18, Z_DUESE + 18, 8, Axis.Y))
        t += [sechskant((x + dx, -195, Z_DUESE), (0, -1, 0), 16, 8) for dx in (-21, 21)]
        t.mat("blank", stab((x, -190, Z_DUESE), (x, -242, Z_DUESE), 16))
        t.mat("blank", sechskant((x, -242, Z_DUESE), (0, -1, 0), 26, 10))
        t.mat("blank", stab((x, -228, Z_DUESE), (x, -228, Z_DUESE - 10), 8))
        t.mat("blank", sechskant((x, -228, Z_DUESE - 8), (0, 0, -1), 18, 8))
    # Leckoelleitung ueber den Duesenhaltern
    z_leck = Z_DUESE + 20.0
    t.mat("blank", stab((ZYL_X[0] - 15, -236, z_leck), (ZYL_X[-1] + 15, -236, z_leck), 3.5))
    for x in ZYL_X:
        t.mat("blank", stab((x, -236, z_leck - 10), (x, -236, z_leck + 2), 4.5))


def _kopf(t: Sammler) -> None:
    """Zylinderkopf, Ventildeckel, Kopfschrauben, Thermostat, Ansaugkruemmer, Duesenhalter."""
    _zylinderkopf(t)
    _ventildeckel(t)
    _thermostat(t)
    _ansaugkruemmer(t)
    _duesenhalter(t)


# ======================================================================================
# Seitendeckel (Kastenpumpe), linke Zusatzteile
# ======================================================================================
def _pumpenkasten(t: Sammler) -> None:
    """Gussgehaeuse, Deckelplatte mit Schrauben, erhabenes Kissenfeld mit Schrift, Ablassschraube,
    Deckelflansch mit Schraubenreihe."""
    xm = SD_XM
    y_pl, y_er = SD_Y_PLATTE, SD_Y_ERHABEN
    # Gussgehaeuse (Kasten), Ecken gerundet, Aussenkante abgerundet (Guss)
    kasten = box(SD_X0, SD_X1, SD_Y1, SD_Y0, SD_Z0, SD_ZF0)
    kasten = fillet(kasten.edges().filter_by(Axis.Y), 22)
    kasten = fillet(kasten.edges().group_by(Axis.Y)[0], 5)
    t.append(kasten)
    # Deckelflansch: nur aussen, Oberkante SD_Z1; Druckleitungen laufen daneben (y -228)
    flansch = box(SD_X0, SD_X1, SD_Y1, SD_Y_OBEN, SD_ZF0, SD_Z1)
    flansch = fillet(flansch.edges().filter_by(Axis.Z), 10)
    flansch = fillet(flansch.edges().group_by(Axis.Y)[0], 4)
    t.append(flansch)
    xs0, xs1 = SD_X0 + 22, SD_X1 - 22
    for i in range(8):                                                       # Flanschschrauben (Nordhorn: 8 Stueck)
        t.mat("blank", sechskant((xs0 + (xs1 - xs0) * i / 7, SD_Y1 + 0.3, (SD_ZF0 + SD_Z1) / 2), (0, -1, 0), 16, 7))
    # Deckelplatte 320 x 113
    px0, px1, pz0, pz1 = xm - 160, xm + 160, SD_Z0 + 8, SD_ZF0 - 6
    platte = box(px0, px1, SD_Y1 + 1, y_pl, pz0, pz1)
    platte = fillet(platte.edges().filter_by(Axis.Y), 14)
    platte = fillet(platte.edges().group_by(Axis.Y)[0], 3.0)
    t.append(platte)
    # erhabenes Kissenfeld, Ecken R 25, Kante stark abgerundet (keine harte Stufe)
    ex0, ex1, ez0, ez1 = xm - 148, xm + 148, pz0 + 8, pz1 - 8
    erh = box(ex0, ex1, y_pl + 0.5, y_er, ez0, ez1)
    erh = fillet(erh.edges().filter_by(Axis.Y), 25)
    erh = fillet(erh.edges().group_by(Axis.Y)[0], 5.0)
    t.append(erh)
    # Ablassschraube (Bund + Sechskant SW 28) unten links im Feld
    ax, az = ex0 + 30, ez0 + 28
    t.append(Pos(ax, y_er + 0.5, az) * Rot(90, 0, 0) * Cylinder(18, 5.5, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("blank", sechskant((ax, y_er - 5.0, az), (0, -1, 0), 28, 11))
    # Schrift (fett, serifenlos): HANOMAG fast ueber die ganze Feldbreite, DIESEL eingerueckt darunter
    z_top = ez1 - 8.0
    _schrift_mass(t, xm - 2, z_top - 20, y_er, "HANOMAG", 262.0, 40.0)
    _schrift_mass(t, xm + 12, z_top - 62, y_er, "DIESEL", 178.0, 36.0)
    # Plattenschrauben: je eine in jeder Ecke, unten drei dazwischen
    s_sw, s_h = 14.0, 6.0
    xr, xl = px1 - 13, px0 + 13
    for x in (xl, xr):
        for z in (pz1 - 13, pz0 + 13):
            t.mat("blank", sechskant((x, y_pl + 0.3, z), (0, -1, 0), s_sw, s_h))
    for i in range(1, 4):
        t.mat("blank", sechskant((xl + (xr - xl) * i / 4, y_pl + 0.3, pz0 + 9), (0, -1, 0), s_sw, s_h))


def _pumpendeckel(t: Sammler) -> None:
    """Rahmendeckel (flache Platte mit Rahmenrand, Haendlerfotos) mit Einfuellkappe und Verschraubung; die 4 Druckventilhalter
    sitzen im Deckel (Sechskant SW 24, Anschlussverschraubung darauf)."""
    xm = SD_XM
    y0, y1 = SD_Y1 + 6.0, SD_Y_OBEN - 2.0
    ym = (y0 + y1) / 2
    dk = box(xm - 160, xm + 160, y0, y1, SD_Z1, SD_DK_Z1)
    dk = fillet(dk.edges().filter_by(Axis.Z), 8)
    dk = fillet(dk.edges().group_by(Axis.Z)[-1], 3)
    t.append(dk)
    rahmen = box(xm - 160, xm + 160, y0, y1, SD_DK_Z1, SD_DK_Z1 + SD_RAHMEN_H) - box(
        xm - 152, xm + 152, y0 + 8, y1 - 8, SD_DK_Z1 - 1, SD_DK_Z1 + SD_RAHMEN_H + 1)
    t.append(rahmen)
    for x in DV_X:                                                            # Druckventilhalter
        t.mat("blank", sechskant((x, DV_Y, SD_DK_Z1), (0, 0, 1), 24, 14))
        t.mat("blank", Pos(x, DV_Y, SD_DK_Z1 + 14) * Cylinder(9, 16, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    xk = xm - 135                                                             # Einfuellkappe (Oe 30, Raendelrand)
    t.append(Pos(xk, ym, SD_DK_Z1 - 1) * Cylinder(11, 8, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("blank", Pos(xk, ym, SD_DK_Z1 + 6) * Cylinder(15, 18, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("blank", Pos(xk, ym, SD_DK_Z1 + 22) * Cylinder(13, 4, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    xv = xm + 135                                                             # kleine Verschraubung
    t.mat("blank", Pos(xv, ym, SD_DK_Z1 - 1) * Cylinder(6, 8, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("blank", sechskant((xv, ym, SD_DK_Z1 + 7), (0, 0, 1), 16, 7))


def _kraftstoffleitung(t: Sammler) -> None:
    """Schlichte Stahl-Kraftstoffleitung (Oe 8, blank) vom Vorreiniger unauffaellig unter dem Schriftfeld entlang zur
    Rueckseite des Kastens, zwei Verschraubungen (Nordhorn 1:42: die Geflechtschlaeuche sind moderne Ersatzteile)."""
    pts = [(VF_X + 18, VF_Y, VF_Z1 + 8), (535.0, -310.0, VF_Z1 + 8), (535.0, -310.0, 797.0), (1015.0, -310.0, 797.0),
           (1015.0, -288.0, 797.0)]
    t.mat("blank", rohr_glatt(pts, 4.0, 24))
    t.mat("blank", sechskant((VF_X + 14, VF_Y, VF_Z1 + 8), (1, 0, 0), 16, 8))
    t.mat("blank", sechskant((1015.0, SD_Y1 - 1.0, 797.0), (0, -1, 0), 14, 7))


def _reglerwelle(t: Sammler) -> None:
    """Reglerwelle rechts: Lagerhals am Gehaeuse, Welle waagerecht nach hinten, Hebel mit Kugelknopf nach unten;
    Gusslaschen unter dem Gehaeuse (Klemme mitte, Block mit Drahtbuegel rechts)."""
    hz = SD_Z1 - 45
    t.append(rad_x(SD_X1 + 12, -203.0, hz, 17, 24))
    t.append(stab((SD_X1, -203.0, hz), (1050.0, -203.0, hz), 8))
    t.mat("blank", rad_y(1042.0, -212.0, hz, 12, 24))
    t.mat("blank", stab((1042.0, -222.0, hz), (1046.0, -232.0, hz - 28), 6))      # Hebel steht hinter dem Gehaeuse (x > 1025)
    t.mat("blank", stab((1046.0, -232.0, hz - 28), (1048.0, -236.0, hz - 52), 6))
    t.mat("blank", Pos(1048.0, -236.0, hz - 56) * Sphere(12))
    # Gusslaschen unter dem Gehaeuse (Klemme mitte, Block mit Drahtbuegel rechts)
    for x, b, h in ((SD_X0 + 222, 22.0, 18.0), (SD_X0 + 305, 24.0, 16.0)):
        t.mat("blank", box(x - b / 2, x + b / 2, -214.0, -196.0, SD_Z0 - h, SD_Z0 + 1))
    t.mat("blank", stab((SD_X0 + 296, -214.0, SD_Z0 - 12), (SD_X0 + 312, -221.0, SD_Z0 - 18), 2.5))


def _typenschild_und_stoesseldeckel(t: Sammler) -> None:
    """Typenschild mit Nieten (am Block, links vor den Druckleitungen) und Stoesselkammer-Kontrolldeckel
    mit Schraubenkranz (am Block hinter den Druckleitungen)."""
    tx0, tx1, tz0, tz1 = 408.0, 464.0, 850.0, 890.0
    t.mat("blank", box(tx0, tx1, -194, -190, tz0, tz1))
    for x in (tx0 + 8, tx1 - 8):
        for z in (tz0 + 8, tz1 - 8):
            t.mat("blank", Pos(x, -194, z) * Sphere(4))
    t.append(kasten_rund(SK_X0, SK_X1, -200, -189, SK_Z0, SK_Z1, 15, Axis.Y))
    for z in (SK_Z0 + 12, SK_Z1 - 12):
        t += schraubenreihe((SK_X0 + 15, -200, z), (SK_X1 - 15, -200, z), 4, (0, -1, 0), 16, 7)


def _seitendeckel(t: Sammler) -> None:
    """Hanomag-Kastenpumpe 'HANOMAG DIESEL' an der linken Blockseite: Gussgehaeuse 360 x 127 hoch, ~100 vom Block,
    Deckelplatte mit Schrauben, erhabenes Schriftfeld, Deckelflansch mit Schraubenreihe, aufgesetzter Blechdeckel mit
    Einfuellkappe, Stahl-Kraftstoffleitung darunter, Abstellhebel mit Kugelknopf hinten, Typenschild."""
    _pumpenkasten(t)
    _pumpendeckel(t)
    _kraftstoffleitung(t)
    _reglerwelle(t)
    _typenschild_und_stoesseldeckel(t)


def _links_zusatz(t: Sammler) -> None:
    """Linke Seite (DSC04742): Oelschild an der Kopfwand ueber dem Pumpenkasten, Gusszylinder vorn im Fenster
    mit Flansch und Gestaenge zum Kasten."""
    # Oelschild (Messing/Emaille; Video 095/100/108, DSC04644), 150 x 70, z 965..1035, am Kopf y -185
    t.mat("schild", box(700, 850, -189, -185, 965, 1035))
    t.mat("blank", box(706, 844, -190, -189, 971, 975))
    for x in (708, 842):
        for z in (972, 1028):
            t.mat("blank", Pos(x, -189, z) * Sphere(3))
    # Gusszylinder: senkrecht, Ø 90, z 838..1000, unterer Flansch Ø 106, Deckel, Anschluss zum Wassereinlass
    x, y = 416.0, -262.0
    zyl = Pos(x, y, 838) * Cylinder(45, 162, align=(Align.CENTER, Align.CENTER, Align.MIN))
    zyl = fillet(zyl.edges().group_by(Axis.Z)[-1], 8)
    t.append(zyl)
    t.append(Pos(x, y, 828) * Cylinder(53, 10, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    for a in range(0, 360, 60):                                       # Flanschschrauben
        t.append(sechskant((x + 46 * math.cos(math.radians(a)), y + 46 * math.sin(math.radians(a)), 838),
                           (0, 0, 1), 12, 5))
    t.append(Pos(x, y, 1000) * Cylinder(30, 6, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.append(Pos(x, y, 925) * Cylinder(49, 12, align=(Align.CENTER, Align.CENTER, Align.MIN)))     # Rippe
    # Gestaenge zum Kasten (waagerecht, z 905) mit Gabelkopf
    t.mat("blank", stab((x + 40, -250, 905), (640, -250, 905), 5))
    t.mat("blank", Pos(640, -250, 905) * Sphere(8))
    t.mat("blank", stab((x + 40, y, 905), (x + 40, -250, 905), 5))


# ======================================================================================
# Einspritzanlage
# ======================================================================================
def _einspritzpumpe(t: Sammler) -> None:
    """Hanomag-Einspritzpumpe = Kasten SD_*: Reglerkopf mit Deckel und Stellhebel an der Stirn, Antriebsgehaeuse zum
    Steuergehaeuse, Elementverschluesse unten, Foerderpumpe (Messing) mit Handpumpe (Haendlerfotos R40-94, Nordhorn)."""
    xr = (REG_X0 + REG_X1) / 2
    t.append(rad_x(xr, REG_Y, REG_Z, REG_R, REG_X1 - REG_X0))
    t.append(rad_x(REG_X0 - 5, REG_Y, REG_Z, REG_R - 8, 10))                      # Reglerdeckel
    t += schraubenkreis((REG_X0 - 10, REG_Y, REG_Z), (-1, 0, 0), REG_R - 18, 4, 12, 5, 45)
    t.mat("blank", rad_x(REG_X0 - 12, REG_Y, REG_Z, 12, 8))                       # Nabe Stellhebel
    t.mat("blank", stab((REG_X0 - 12, REG_Y, REG_Z), (558.0, -262.0, 795.0), 4))
    t.mat("blank", Pos(558.0, -262.0, 795.0) * Sphere(7))
    # Antriebsgehaeuse: Auge am Steuergehaeuse, Rohr nach hinten in den Reglerkopf
    t.append(stab((391.0, -170.0, 800.0), (391.0, -218.0, 800.0), 22))
    t.append(stab((391.0, -218.0, 800.0), (REG_X0 + 15, -218.0, 800.0), 14))
    # Elementverschluesse: Leiste unter dem Kasten mit 5 Stopfen
    xm = SD_XM
    t.append(box(xm - 150, xm + 150, SD_Y1 + 2, SD_Y1 + 24, SD_Z0 - 10, SD_Z0))
    for i in range(5):
        t.mat("blank", sechskant((xm - 120 + 60 * i, SD_Y1 + 13, SD_Z0 - 10), (0, 0, -1), 16, 8))
    # Foerderpumpe unter dem Regler: Messingkoerper mit Anschluessen, Handpumpe (Raendelstange)
    yf = (FP_Y0 + FP_Y1) / 2
    zm = (FP_Z0 + FP_Z1) / 2
    t.mat("messing", fillet(box(FP_X0, FP_X1, FP_Y0, FP_Y1, FP_Z0, FP_Z1).edges(), 8))
    t.append(box(575.0, 625.0, -286.0, -262.0, FP_Z1, 815.0))                      # Stuetze zum Reglerkopf
    t.mat("messing", rad_x((FP_X0 + FP_X1) / 2, yf, zm, 9, FP_X1 - FP_X0 + 30))   # zwei seitliche Anschluesse
    t.mat("messing", sechskant((FP_X0 - 15, yf, zm), (-1, 0, 0), 20, 8))
    t.mat("messing", sechskant((FP_X1 + 15, yf, zm), (1, 0, 0), 20, 8))
    xk, yk = FP_KNOPF_X, FP_KNOPF_Y
    t.mat("messing", Pos(xk, yk, FP_Z1) * Cylinder(14, 12, align=(Align.CENTER, Align.CENTER, Align.MIN)))     # Buchse
    t.mat("messing", Pos(xk, yk, FP_Z1 + 12) * Cylinder(10, FP_KNOPF_H - 12, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("messing", Pos(xk, yk, FP_Z1 + FP_KNOPF_H - 4) * Cylinder(12, 4, align=(Align.CENTER, Align.CENTER, Align.MIN)))


def _druckleitungen(t: Sammler) -> None:
    """Druckleitungen: senkrecht aus den Druckventilhaltern im Deckel, jede auf eigener y-Bahn (DL_Y) waagerecht auf
    DL_H zum Duesenhalter, dort senkrecht herunter und von aussen in den Anschlusssechskant."""
    z_ende = Z_DUESE
    for xo, xt, y in zip(DV_X, ZYL_X, DL_Y, strict=True):
        pts = [(xo, DV_Y, SD_DK_Z1 + 26), (xo, DV_Y, DL_H), (xo, y, DL_H), (xt, y, DL_H), (xt, y, z_ende), (xt, -253.0, z_ende)]
        t.mat("blank", rohr_glatt(pts, DL_R, 12))


def _kraftstofffilter(t: Sammler) -> None:
    """Zwei getrennte Kraftstofffilter (DSC04742): Glasbirne Ø 100, Anschlusskopf oben, Fuss + Ablassstutzen
    unten; Konsolen stehen auf dem Zylinderkopf, die Birnenoberteile liegen hinter dem Haubenband."""
    zc = FILTER_Z
    zh = FILTER_KOPF_Z
    for x in FILTER_X:
        t.mat("glas", Pos(x, FILTER_Y, zc) * Sphere(50))
        t.append(kasten_rund(x - 35, x + 35, FILTER_Y - 28, FILTER_Y + 28, zh - 15, zh + 15, 10))   # Kopf
        t.mat("blank", sechskant((x, FILTER_Y, zh + 15), (0, 0, 1), 18, 10))                       # Entlueftung
        t.mat("blank", Pos(x, FILTER_Y, zc - 52) * Cylinder(24, 10, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        t.mat("blank", Pos(x, FILTER_Y, zc - 76) * Cylinder(9, 26, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        t.mat("blank", sechskant((x, FILTER_Y, zc - 76), (0, 0, -1), 16, 8))                       # Ablassschraube
        t.append(stab((x, -170, Z_KOPF1), (x, -170, zh), 8))                                       # Konsole
        t.append(stab((x, -170, zh), (x, FILTER_Y, zh), 8))
        t.append(kasten_rund(x - 16, x + 16, -184, -156, Z_KOPF1, Z_KOPF1 + 8, 6))                  # Fussplatte


def _kraftstoffleitungen(t: Sammler) -> None:
    """Kraftstoffleitungen: Foerderpumpe -> Filter 1 -> Filter 2 -> Pumpenkasten (aussen bei y ~ -314/-322)."""
    zh = FILTER_KOPF_Z
    x1, x2 = FILTER_X
    xs = x1 - 47                                                      # Steigleitung vor dem ersten Filter
    t.mat("blank", rohr_glatt([(FP_X0 + 12, FP_Y0 + 1, 760.0), (FP_X0 + 12, -314.0, 760.0), (xs, -314.0, 760.0),
                               (xs, -314.0, zh), (x1 - 35, FILTER_Y, zh)], 4, 14))
    t.mat("blank", stab((x1 + 35, FILTER_Y, zh), (x2 - 35, FILTER_Y, zh), 4))                      # Filter 1 -> 2
    # aussen um den Kasten herum (y -322), unter dem Gehaeuse (z 770), dann hoch zur Flanschfront
    t.mat("blank", rohr_glatt([(x2 + 35, FILTER_Y, zh), (810, FILTER_Y, zh), (810, -322, zh), (810, -322, 770),
                               (709, -322, 770), (709, -322, 924), (709, SD_Y1 - 2, 924)], 4, 14))
    t.mat("blank", sechskant((x1 - 35, FILTER_Y, zh), (-1, 0, 0), 16, 8))
    t.mat("blank", sechskant((x2 + 35, FILTER_Y, zh), (1, 0, 0), 16, 8))
    t.mat("blank", sechskant((709, SD_Y1, 924), (0, -1, 0), 14, 6))


def _vorreiniger(t: Sammler) -> None:
    """Zweiter Vorreiniger mit Glasschale hinter dem Regler (fz_06m), Leitung zur Foerderpumpe."""
    t.append(kasten_rund(VR_X - 20, VR_X + 20, -312, -262, 690, 722, 8))
    t.append(box(VR_X - 10, VR_X + 10, -262, -194, 696, 716))         # Halter zum Block
    t.mat("glas", Pos(VR_X, -290, 632) * Cylinder(19, 58, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("blank", Pos(VR_X, -290, 622) * Cylinder(10, 10, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    for dy in (-22, 22):
        t.mat("blank", stab((VR_X, -290 + dy, 690), (VR_X, -290 + dy, 627), 3))
    t.mat("blank", stab((VR_X, -312, 627), (VR_X, -268, 627), 3.5))
    t.mat("blank", rohr_glatt([(VR_X - 20, -300, 706), (645, -300, 706), (645, -277, 752), (FP_X1 + 1, -277, 752)], 4, 14))


def _vorreiniger_vorn(t: Sammler) -> None:
    """Vorreiniger mit Glasschale und Buegel vorn im Fenster (Nordhorn: Mitte x ~430..505, z 815..890), Messinganschluss
    zum Gusszylinder."""
    zk = VF_Z1
    t.mat("glas", Pos(VF_X, VF_Y, VF_Z0) * Cylinder(VF_R, VF_Z1 - VF_Z0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("messing", Pos(VF_X, VF_Y, zk) * Cylinder(VF_R + 5, 16, align=(Align.CENTER, Align.CENTER, Align.MIN)))     # Kopf
    t.mat("blank", Pos(VF_X, VF_Y, VF_Z0 - 8) * Cylinder(VF_R + 3, 8, align=(Align.CENTER, Align.CENTER, Align.MIN)))  # Boden
    for dx in (-VF_R - 3, VF_R + 3):                                  # Buegel
        t.mat("blank", stab((VF_X + dx, VF_Y, VF_Z0 - 4), (VF_X + dx, VF_Y, zk), 2.5))
    t.mat("messing", stab((461.0, VF_Y, zk + 8), (VF_X - 20, VF_Y, zk + 8), 8))                  # Anschluss zum Gusszylinder
    t.mat("messing", sechskant((470.0, VF_Y, zk + 8), (1, 0, 0), 20, 8))


def _einspritzanlage(t: Sammler) -> None:
    """Einspritzpumpe, Druckleitungen, Kraftstofffilter und -leitungen, Vorreiniger."""
    _einspritzpumpe(t)
    _druckleitungen(t)
    _kraftstofffilter(t)
    _kraftstoffleitungen(t)
    _vorreiniger(t)
    _vorreiniger_vorn(t)


# ======================================================================================
# Riementrieb, Luefter, Lichtmaschine
# ======================================================================================
def _luefter(t: Sammler) -> None:
    """Luefter: Nabe + 4 angestellte Fluegel, Spitzen gerundet; Luefterhaube (Blech auf dem Kuehler mit Ring)."""
    t.mat("schwarz", rad_x((LUEFTER_X - 10 + RIEMEN_X0) / 2, 0, 860, 50, RIEMEN_X0 - LUEFTER_X + 10))
    huelle = rad_x(LUEFTER_X, 0, 860, LUEFTER_R, 40)
    for i in range(4):
        fl = Pos(LUEFTER_X, 0, 860) * Rot(i * 90 + 20, 0, 0) * Pos(0, 0, 150) * Rot(0, 0, 10) * Box(6, 62, 200)
        t.mat("schwarz", fl & huelle)
    # Luefterhaube: Blech auf dem Kuehler mit Ring
    blech = box(K_X1, K_X1 + HAUBE_BLECH, -300, 300, K_NETZ_Z0, K_NETZ_Z1) - rad_x(K_X1 + 5, 0, 860, 262, 20)
    t.mat("schwarz", blech)
    rx0, rx1 = K_X1 + HAUBE_BLECH, RIEMEN_X0 - 2                          # Ring um den Luefter
    t.mat("schwarz", ring_x((rx0 + rx1) / 2, 0, 860, 272, 262, rx1 - rx0))


def _riementrieb(t: Sammler) -> None:
    """Keilriemen Kurbelwelle - Wasserpumpe - Lichtmaschine, Scheiben, Wasserpumpe, Luefter mit Haube."""
    pl = _ebene_x(RIEMEN_X0)
    kreise = [SCHEIBE_KW, SCHEIBE_WP, SCHEIBE_LIMA]
    # geschlossener Riemen (Wirkradius -4 .. +8)
    band = _riemen_profil(kreise, 8) - _riemen_profil(kreise, -4)
    t.mat("gummi", extrude(pl.offset(4) * band, amount=RIEMEN_X1 - RIEMEN_X0 - 8))   # 8 breit
    # Riemenscheiben: Nabe + zwei Bordscheiben
    for (y, z, r) in kreise:
        t.mat("blank", rad_x((RIEMEN_X0 + RIEMEN_X1) / 2, y, z, r - 4, RIEMEN_X1 - RIEMEN_X0))
        for xb in (RIEMEN_X0 + 2, RIEMEN_X1 - 2):
            t.mat("blank", rad_x(xb, y, z, r + 10, 4))
    # Wasserpumpe am Blockkopf vorn
    t.append(rad_x(392, 0, 860, 72, 24))
    t.append(rad_x(390, 0, 860, 40, 20))
    t += schraubenkreis((X_VORN, 0, 860), (-1, 0, 0), 58, 6, 14, 6, 30)
    _luefter(t)


def _lichtmaschine(t: Sammler) -> None:
    """Lichtmaschine rechts oben am Block (Fotos DSC04729/33: Zollstock, Laenge ~190 + Gussschilde),
    Riemenscheibe in der Riemenebene, Spannlasche vorn, Halter zum Block."""
    y, z = SCHEIBE_LIMA[0], SCHEIBE_LIMA[1]
    t.mat("zink", rad_x(495, y, z, 60, 190))                          # Gehaeuse x 400..590
    for x in (402, 588):                                              # Gussschilde
        t.mat("motor", rad_x(x, y, z, 64, 14))
    t.mat("motor", rad_x(603, y, z, 38, 12))                          # Lagerdeckel hinten
    t.mat("blank", rad_x(387, y, z, 12, 14))                          # Welle
    for a in (45, 225):                                               # Zuganker
        dy, dz = 63 * math.cos(math.radians(a)), 63 * math.sin(math.radians(a))
        t.mat("blank", stab((395, y + dy, z + dz), (595, y + dy, z + dz), 5))
    for dy in (-16, 16):                                              # Anschlussklemmen hinten
        t.mat("blank", stab((609, y + dy, z + 24), (646, y + dy, z + 24), 6))
        t.mat("blank", sechskant((646, y + dy, z + 24), (1, 0, 0), 14, 6))
    t.mat("schild", box(470, 540, y + 57, y + 63, z - 15, z + 15))     # Typschild
    # Halter: Schwenkfuesse unten zum Block, Spannlasche vorn zur Wasserpumpe
    for x in (420, 570):
        t.append(box(x, x + 28, 185, y - 10, z - 72, z - 50))
        t.append(box(x, x + 28, y - 30, y + 10, z - 70, z - 40))
    t.append(box(386, 398, 60, y - 40, z + 5, z + 25))


# ======================================================================================
# Kuehler
# ======================================================================================
def _kuehlernetz(t: Sammler) -> None:
    """Netz mit Lamellen vorn und hinten, senkrechte Stuetzbleche."""
    t.mat("auspuff", box(K_X0 + 10, K_X1 - 10, -300, 300, K_NETZ_Z0, K_NETZ_Z1))
    z = K_NETZ_Z0 + 12
    while z < K_NETZ_Z1 - 8:
        for x0, x1 in ((K_X0 + 6, K_X0 + 10), (K_X1 - 10, K_X1 - 6)):
            t.mat("blank", box(x0, x1, -298, 298, z, z + 5))
        z += 20
    for y in range(-270, 271, 90):                                    # senkrechte Stuetzbleche
        t.mat("auspuff", box(K_X0 + 4, K_X0 + 10, y - 3, y + 3, K_NETZ_Z0, K_NETZ_Z1))


def _wasserkasten_oben(t: Sammler) -> None:
    """Oberer Wasserkasten; Einfuellrohr vom Kasten nach vorn in die (hinten offene) Maske gekroepft,
    Muendung unter dem Verschluss auf der Maskenkappe (KD_X), 0,5 mm Luft zum Maskendach; Ueberlaufrohr."""
    t.mat("auspuff", kasten_rund(K_X0, K_X1, -K_Y, K_Y, K_NETZ_Z1, K_Z1, 25, Axis.X))
    xs, ze, zr = 280.0, KD_Z - 0.5, HAUBE_DACH_Z - 112.0                           # Abgang, Muendungsoberkante, Rohrhoehe
    t.mat("auspuff", Pos(xs, 0, K_Z1 - 5) * Cylinder(32, 12, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("auspuff", rohr_glatt([(xs, 0, K_Z1 - 5), (xs, 0, zr), (KD_X, 0, zr), (KD_X, 0, ze - 20)], 22, 40))
    t.mat("auspuff", Pos(KD_X, 0, ze - 24) * Cylinder(29, 24, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("auspuff", rad_x(K_X1 + 8, 0, K_ZULAUF_Z, 24, 16))                 # Zulaufstutzen
    # Ueberlaufrohr: vom Einfuellrohr nach rechts, hinter dem Seitenteil nach unten
    zu = zr - 30                                                       # unter der gewoelbten Dachecke
    t.mat("blank", rohr_glatt([(250, 15, zr), (250, 15, zu), (250, 312, zu), (K_X1 + 7, 312, zu), (K_X1 + 7, 312, 560)],
                              4, 15))


def _wasserkasten_unten(t: Sammler) -> None:
    """Unterer Wasserkasten: Mitte bis z = 480 zwischen den Traegern, aussen auf den Traegern; Ablasshahn und -stutzen."""
    t.mat("auspuff", kasten_rund(K_X0, K_X1, -K_Y, K_Y, K_Z0, K_NETZ_Z0, 20, Axis.X))   # flacher Kasten, UK >= 520
    t.mat("blank", rad_x(K_X1 + 8, 0, K_Z0 + 24, 9, 16))               # Ablasshahn an der Rueckseite (nicht unter der Maske)
    t.mat("blank", sechskant((K_X1 + 16, 0, K_Z0 + 24), (1, 0, 0), 22, 12))
    t.mat("auspuff", rad_x(K_X1 + 8, -300, 552, 22, 16))               # Ablaufstutzen links


def _kuehler_seitenteile(t: Sammler) -> None:
    """Seitenteile (U-Profil) und Fuesse auf den Laengstraegern, Stehbolzen der Wasserkastenverschraubung."""
    for s in (-1, 1):
        t.mat("auspuff", box(K_X0, K_X1, s * 300, s * K_Y, Z_TRAEGER + 8, K_Z1 - 20))
        t.mat("auspuff", box(K_X0 + 15, K_X1 - 15, s * 196, s * 290, Z_TRAEGER, Z_TRAEGER + 10))
        for x in (250, 310):
            t += schraube((x, s * 245, Z_TRAEGER + 10), (0, 0, 1), 20, 10)
        # Stehbolzen der Wasserkastenverschraubung
        t.mat("auspuff", schraubenreihe((K_X0, s * 260, K_NETZ_Z1 + 10), (K_X0, s * 260, K_Z1 - 30), 2, (-1, 0, 0), 16, 6))


def _kuehlerschlaeuche(t: Sammler) -> None:
    """Schlaeuche mit Schellen (oben zum Thermostat, unten zum Wassereinlass) und Wassereinlass am Block."""
    oben = [(K_X1 + 14, 0, K_ZULAUF_Z), (362, 0, K_ZULAUF_Z - 18), (378, 0, 1130), (388, 0, Z_KOPF1 + 60),
            (392, 0, Z_KOPF1 + 24)]
    t.mat("gummi", rohr_glatt(oben, 27, 45))
    _gummi_schelle(t, (K_X1 + 18, 0, K_ZULAUF_Z), (1, 0, 0), 27)
    _gummi_schelle(t, (390, 0, Z_KOPF1 + 40), (0.1, 0, -1), 27, schloss=(0, 1, 0))
    unten = [(K_X1 + 14, -300, 552), (395, -300, 560), (412, -300, 760), (440, -232, 800)]
    t.mat("gummi", rohr_glatt(unten, 25, 50))
    _gummi_schelle(t, (K_X1 + 20, -300, 552), (1, 0, 0), 25)
    # Wassereinlass am Block (Gusskruemmer)
    t.append(stab((440, -185, 800), (440, -236, 800), 26))
    _gummi_schelle(t, (440, -225, 800), (0, -1, 0), 25)


def _kuehler(t: Sammler) -> None:
    """Kuehler: Lamellenblock, Wasserkaesten, Seitenteile, Fuesse, Einfuellstutzen, Schlaeuche."""
    _kuehlernetz(t)
    _wasserkasten_oben(t)
    _wasserkasten_unten(t)
    _kuehler_seitenteile(t)
    _kuehlerschlaeuche(t)


# ======================================================================================
# Schwungradgehaeuse, Anlasser
# ======================================================================================
def _schwungradgehaeuse(t: Sammler) -> None:
    """Kupplungs-/Schwungradgehaeuse mit Schraubenkranz und hinteren Motorfuessen."""
    pl = _ebene_x(SG_X0)
    kreis = Pos(0, SG_Z) * Circle(SG_R)
    oben = Pos(0, (Z_TRAEGER + 5 + SG_OBEN) / 2) * Rectangle(2 * 320, SG_OBEN - Z_TRAEGER - 5)
    unten = Pos(0, (300 + Z_TRAEGER + 5) / 2) * Rectangle(2 * 186, Z_TRAEGER + 5 - 300)
    profil = kreis & (oben + unten)
    t.append(extrude(pl * profil, amount=14))                          # Flansch vorn
    innen = Pos(0, SG_Z) * Circle(SG_R - 14) & (oben + unten)
    t.append(extrude(pl.offset(14) * innen, amount=SG_X1 - SG_X0 - 14))
    stutzen = Pos(0, SG_Z) * Circle(SG_R - 20) & Pos(0, (360 + 760) / 2) * Rectangle(2 * 190, 760 - 360)
    t.append(extrude(_ebene_x(SG_X1) * stutzen, amount=SG_X2 - SG_X1))
    _schwungrad_schrauben(t)
    # Schwungrad-Schauloch-Deckel unten
    t.append(box(SG_X0 + 16, SG_X1 - 4, -60, 60, 330, 352))
    # hintere Motorfuesse auf den Traegern
    for s in (-1, 1):
        t.append(box(SG_X0 + 5, SG_X1 - 3, s * 186, s * 282, Z_TRAEGER, Z_TRAEGER + 18))
        t.append(box(SG_X0 + 5, SG_X1 - 3, s * 186, s * 200, Z_TRAEGER, 620))
        t += schraube(((SG_X0 + SG_X1) / 2, s * 250, Z_TRAEGER + 18), (0, 0, 1), 22, 12)


def _schwungrad_schrauben(t: Sammler) -> None:
    """Schraubenkranz auf dem Flansch (nur ausserhalb des Blocks sichtbar)."""
    for i in range(24):
        a = math.radians(i * 15 + 7.5)
        y, z = (SG_R - 16) * math.cos(a), SG_Z + (SG_R - 16) * math.sin(a)
        im_block = abs(y) < 200 and z > Z_WANNE - 10
        im_traeger = abs(y) > 175 and z < Z_TRAEGER + 20
        unter_anlasser = y > 195 and ANL_Z - 70 < z < ANL_Z + 70       # Antriebsflansch des Anlassers sitzt dort
        if im_block or im_traeger or unter_anlasser:
            continue
        t.append(sechskant((SG_X0, y, z), (-1, 0, 0), 18, 8))


def _anlasser(t: Sammler) -> None:
    """Anlasser RECHTS am Schwungradgehaeuse (Fotos DSC04729/33/35): tuerkises Gehaeuse, rotes Antriebsteil,
    grauer Magnetschalter oben mit 2 Klemmen, Antriebsflansch zum Schwungradgehaeuse, Panzerkabel."""
    y, z, xf = ANL_Y, ANL_Z, SG_X0                                    # xf = Flanschflaeche 1030
    t.mat("motor", rad_x(xf - 6, y, z, 62, 12))                       # Antriebsflansch
    t.mat("motor", rad_x(xf - 30, y, z, 52, 36))                      # Antriebslager (grau) x 975..1018
    t.append(rad_x(xf - 77, y, z, 55, 50))                     # rotes Antriebsteil x 928..978
    t.mat("schwarz", rad_x(xf - 160, y, z, 57.5, 115))                # schwarzes Gehaeuse (Video 177/180) x 813..928
    t.mat("blank", ring_x(xf - 160, y, z, 59, 55, 14))                # Deckband
    t.mat("motor", rad_x(xf - 222, y, z, 50, 12))                     # Kollektordeckel
    t.mat("blank", rad_x(xf - 232, y, z, 14, 10))
    # Magnetschalter oben (grau) mit 2 Klemmen
    t.mat("zink", rad_x(xf - 62, y, z + 80, 28, 84))
    t.mat("zink", box(xf - 100, xf - 24, y - 16, y + 16, z + 45, z + 62))
    for x in (xf - 85, xf - 40):
        t.mat("blank", Pos(x, y, z + 106) * Cylinder(6, 16, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        t.mat("blank", sechskant((x, y, z + 118), (0, 0, 1), 14, 5))
    # Panzerkabel Ø 32: aus Richtung Fahrerstand/Batterie (x ~ 1083, z 905) im Bogen zur hinteren Klemme
    t.mat("gummi", rohr_glatt([(1083.0, 298, 905), (1050, 298, 912), (1010, 292, 960), (xf - 40, y + 4, 980)], 16, 40))
    t.mat("blank", rad_x(1078.0, 298, 905, 21, 10))                    # Kabelschelle am Ende


# ======================================================================================
# Rechte Seite
# ======================================================================================
def _oelfilter(t: Sammler) -> None:
    """Oelfilter-Kanister (grau, geneigt) auf Vierschrauben-Flanschplatte."""
    x, zf = OELF_X, OELF_Z
    # Flanschplatte (4 Schrauben) am Block, Stutzen nach aussen, Kanister 32 Grad nach vorn geneigt
    t.append(box(x - 45, x + 45, 188, 197, zf - 45, zf + 45))
    for dx in (-33, 33):
        for dz in (-33, 33):
            t.mat("blank", sechskant((x + dx, 197, zf + dz), (0, 1, 0), 16, 7))
    t.append(stab((x, 196, zf), (x, 238, zf), 26))
    b = Vector(x, 238, zf)
    # Nordhorn 2:58/3:00 (Massstab Anlasser Ø 115): Kanister Ø ~68, Gesamthoehe ~120, nahezu senkrecht (~8 Grad)
    d = Vector(-math.sin(math.radians(8)), 0, math.cos(math.radians(8)))
    t.mat("zink", Pos(*b) * Sphere(OELF_R))
    t.mat("zink", stab(tuple(b), tuple(b + d * OELF_L), OELF_R))
    t.mat("zink", stab(tuple(b + d * (OELF_L * 0.65)), tuple(b + d * (OELF_L * 0.65 + 8)), OELF_R + 3.5))   # Rollrand
    top = b + d * OELF_L
    t.mat("zink", Pos(*top) * Sphere(OELF_R))
    t.mat("blank", sechskant(tuple(top + d * (OELF_R - 3)), tuple(d), 18, 10))     # Deckelschraube


def _oelmessstab(t: Sammler) -> None:
    """Oelmessstab mit Fuehrungsrohr und Griffoese (vor dem Anlasser)."""
    xm = MESS_X
    t.mat("blank", rohr_glatt([(xm, 185, 700), (xm, 215, 740), (xm + 5, 240, 900)], 7, 30))
    t.mat("blank", stab((xm + 5, 240, 900), (xm + 6, 242, 925), 4))
    t.mat("blank", Pos(xm + 6, 242, 940) * Rot(90, 0, 0) * Torus(14, 4))


def _rohr_mit_hahn(t: Sammler) -> None:
    """Waagerechtes Rohr Ø 10 am Block (z 905) bis zum T-Stueck, von dort schwarzer Schlauch senkrecht nach unten, Hahn."""
    zr, yr, xt = 905.0, 207.0, 1000.0
    t.mat("blank", stab((740, yr, zr), (xt, yr, zr), 5))
    t.mat("blank", sechskant((740, yr, zr), (-1, 0, 0), 14, 7))
    for xc in (800, 930):                                                          # Halteclips am Block
        t.mat("blank", box(xc - 6, xc + 6, 188, yr, zr - 7, zr + 7))
    t.mat("blank", stab((xt, yr, zr), (xt, yr, zr + 22), 6))                       # T-Stueck: Stutzen nach oben
    t.mat("blank", rad_x(xt, yr, zr, 7, 24))                                       # und Rohr durchgehend
    t.mat("gummi", stab((xt, yr, zr), (xt, yr, 780), 6.5))                         # Schlauch senkrecht nach unten
    t.mat("blank", rad_y(xt, yr, 770, 10, 20))                                     # Hahn (Koerper)
    t.mat("blank", stab((xt, yr, 770), (xt - 34, yr, 770), 4))                     # Knebel
    t.mat("blank", Pos(xt - 36, yr, 770) * Sphere(6))


def _entlueftung(t: Sammler) -> None:
    """Kurbelgehaeuse-Entlueftung: Stutzen oben am Kurbelgehaeuse, Rohr nach unten."""
    xe = 745.0
    t.append(stab((xe, 183, 760), (xe, 215, 760), 22))
    t.mat("blank", rohr_glatt([(xe, 214, 760), (xe, 228, 740), (xe + 10, 228, Z_TRAEGER + 25)], 9, 30))


def _anbauteile_rechts(t: Sammler) -> None:
    """Rechte Seite (Fotos DSC04729/33/35): Oelfilter-Kanister (grau, geneigt) auf Vierschrauben-Flanschplatte,
    Oelmessstab, waagerechtes Rohr mit T-Stueck + Schlauch + Hahn, Kurbelgehaeuse-Entlueftung."""
    _oelfilter(t)
    _oelmessstab(t)
    _rohr_mit_hahn(t)
    _entlueftung(t)


def _block_rechts(t: Sammler) -> None:
    """Sichtbare Gussdetails der rechten Blockseite: roter Handlochdeckel mit 10 Schrauben (DSC04729/35),
    Kernstopfen, Lagerrippen, Wasserablasshahn."""
    # Handlochdeckel 220 x 94 (x 780..1000, z 922..1016), Aussenflaeche y 197
    dx0, dx1, dz0, dz1 = 780.0, 1000.0, 922.0, 1016.0
    dk = box(dx0, dx1, 183, 197, dz0, dz1)
    dk = fillet(dk.edges().filter_by(Axis.Y), 12)
    t.append(dk)
    for x in [dx0 + 14 + i * (dx1 - dx0 - 28) / 3 for i in range(4)]:             # 4 oben, 4 unten
        for z in (dz0 + 12, dz1 - 12):
            t.mat("blank", sechskant((x, 197, z), (0, 1, 0), 14, 6))
    for x in (dx0 + 12, dx1 - 12):                                                 # je 1 an den Seiten
        t.mat("blank", sechskant((x, 197, (dz0 + dz1) / 2), (0, 1, 0), 14, 6))
    for i in range(3):                                                 # Kernstopfen zwischen den Zylindern
        x = ZYL_X[i] + ZYL_T / 2
        if x < 640:
            continue                                                   # hinter der Lichtmaschine
        t.append(rad_y(x, Y_BLOCK + 2, 890, 28, 8))
        t.append(rad_y(x, Y_BLOCK + 5, 890, 22, 6))
    for s in (-1, 1):                                                  # Lagerrippen am Kurbelgehaeuse
        for x in [ZYL_X[0] - ZYL_T / 2 + 5, *[xz + ZYL_T / 2 for xz in ZYL_X[:-1]], ZYL_X[-1] + 70]:
            t.append(box(x - 7, x + 7, s * 183, s * 192, Z_KURBEL_U + 5, 778))
    t.mat("blank", sechskant((ZYL_X[2], Y_BLOCK, 800), (0, 1, 0), 20, 10))       # Wasserablasshahn
    t.mat("blank", stab((ZYL_X[2], Y_BLOCK + 10, 800), (ZYL_X[2], Y_BLOCK + 10, 780), 3))


# ======================================================================================
# Auspuff und Ansaugung
# ======================================================================================
def _auspuff(t: Sammler) -> None:
    """Abgaskruemmer (Sammelrohr mit 4 Stutzen) und Auspuffrohr mit S-Kroepfung durch die Haube."""
    ax, ay = AUSPUFF_XY
    r_rohr = AUSPUFF_D / 2 - 5                         # 5 mm Luft im Haubendurchbruch
    yk, zk, rk = YK_KRUEMMER, Z_KRUEMMER, RK_KRUEMMER                # Sammelrohr (ueber der Lichtmaschine)
    # Sammelrohr mit runden Enden, 4 Stutzen mit Flanschen
    t.mat("schwarz", stab((ZYL_X[0] - 40, yk, zk), (ZYL_X[-1] + 40, yk, zk), rk))
    for x in (ZYL_X[0] - 40, ZYL_X[-1] + 40):
        t.mat("schwarz", Pos(x, yk, zk) * Sphere(rk))
    for x in ZYL_X:
        t.mat("schwarz", stab((x, 196, zk), (x, yk, zk), 30))
        t.mat("schwarz", kasten_rund(x - 42, x + 42, 185, 197, zk - 42, zk + 42, 12, Axis.Y))
        for dx, dz in ((-31, -31), (31, 31)):
            t.mat("blank", sechskant((x + dx, 197, zk + dz), (0, 1, 0), 18, 9))
        t.mat("schwarz", box(x - 8, x + 8, 205, yk, zk - rk - 2, zk - rk + 14))    # Gussrippe
    # Auslassflansch oben, Rohr mit S-Kroepfung durch die Haube
    zf = zk + math.sqrt(rk ** 2 - 5 ** 2)
    t.mat("schwarz", kasten_rund(ax - 45, ax + 45, yk - 45, yk + 45, zf - 3, zf + 10, 10))
    for dx in (-33, 33):
        for dy in (-33, 33):
            t.mat("blank", sechskant((ax + dx, yk + dy, zf + 10), (0, 0, 1), 16, 8))
    t.append(rohr_glatt([(ax, yk - 5, zf), (ax, yk - 5, zf + 50), (ax, ay, zf + 160), (ax, ay, AUSPUFF_Z_TOP)],
                        r_rohr, 80))


def _luftfilter_topf(t: Sammler) -> None:
    """Oelbadluftfilter: Topf mit Spannring, 2 Buegelverschluessen, Deckel; sitzt mit Aussparungen auf
    Kopf/Kruemmer/Steigflansch."""
    ix, iy = ANSAUG_XY
    zp0, zp1, r_topf = ANSAUG_ZP0, ANSAUG_ZP1, ANSAUG_R_TOPF
    t.mat("schwarz", stab((ix, iy, Z_KOPF1 + 10), (ix, iy, 1060), 30))   # Steigrohr vom Kruemmerflansch (im Topf)
    wanne = Pos(ix, iy, zp0) * Cylinder(r_topf, zp1 - zp0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    wanne = fillet(wanne.edges().group_by(Axis.Z)[0], 28)
    # Aussparungen: Topf sitzt auf Zylinderkopf/Ventildeckelflansch, Ansaugkruemmer und Steigflansch (keine Durchdringung)
    wanne = (wanne - box(400, X_HINTEN, -190, 0, 1000, 1045)
             - box(ZYL_X[0] - 45, ZYL_X[-1] + 50, -236, -185, 1000, 1035)
             - box(ix - 50, ix + 50, -265, -180, 1000, 1053))
    t.mat("zink", wanne)                                               # Oelwanne (grau, DSC04742)
    t.mat("blank", Pos(ix, iy, 1190) * Cylinder(r_topf + 0.8, 14, align=(Align.CENTER, Align.CENTER, Align.MIN)))   # Spannring
    for sx in (-1, 1):                                                 # 2 Buegelverschluesse vorn / hinten
        t.mat("blank", Pos(ix + sx * (r_topf + 2), iy, 1188) * Box(8, 18, 36))
        t.mat("blank", Pos(ix + sx * (r_topf + 4), iy, 1216) * Box(6, 12, 20))
    deckel = Pos(ix, iy, 1204) * Cylinder(r_topf - 4, 40, align=(Align.CENTER, Align.CENTER, Align.MIN))
    deckel = fillet(deckel.edges().group_by(Axis.Z)[-1], 16)
    t.mat("zink", deckel)
    t.mat("zink", Pos(ix, iy, 1240) * Cylinder(44, 10, align=(Align.CENTER, Align.CENTER, Align.MIN)))


def _ansaugrohr(t: Sammler) -> None:
    """Ansaugrohr durch das Haubendach: Manschette auf dem Kragen, zwei Spannringe mit Ohren (z 1478..1540)."""
    ix, iy = ANSAUG_XY
    r_rohr, zs = ANSAUG_R_ROHR, ANSAUG_ZS
    t.mat("schwarz", stab((ix, iy, 1244), (ix, iy, ANSAUG_KAPPE_Z0 + 12), r_rohr))
    t.mat("gummi", Pos(ix, iy, zs) * Cylinder(r_rohr + 10, 22, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("blank", Pos(ix, iy, zs + 14) * (Cylinder(r_rohr + 13, 8) - Cylinder(r_rohr + 5, 10)))
    # Kragen: zwei Spannringe mit Ohren (z 1478..1540)
    for z0, z1 in ((1478.0, 1508.0), (1512.0, 1540.0)):
        t.mat("schwarz", Pos(ix, iy, z0) * Cylinder(r_rohr + 8, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        t.mat("schwarz", Pos(ix, iy + r_rohr + 14, (z0 + z1) / 2) * Box(16, 22, z1 - z0 - 6))


def _ansaugkappe(t: Sammler) -> None:
    """Ansaugkappe (Nordhorn 0:10 / 2:46, Massstab Deckel Ø 140): glatter Becher Ø 92 auf dem Rohr, flacher Deckel Ø 140
    mit gerundeter Kante, Oberkante ANSAUG_Z_TOP."""
    ix, iy = ANSAUG_XY
    t.mat("schwarz", Pos(ix, iy, ANSAUG_KAPPE_Z0) * Cylinder(
        46, ANSAUG_KAPPE_BECHER_H + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    deckel = Pos(ix, iy, ANSAUG_Z_TOP - ANSAUG_KAPPE_DECKEL_H) * Cylinder(
        70, ANSAUG_KAPPE_DECKEL_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    deckel = fillet(deckel.edges().group_by(Axis.Z)[-1], 12)
    t.mat("schwarz", deckel)


def _arbeitsleuchte(t: Sammler) -> None:
    """Arbeitsleuchte an Konsole am Rohr, ~72 hinter der Rohrachse (Nordhorn 0:10 / 2:46): Gehaeuse Ø 60, Metallring,
    Glasdom Ø 66 / ~78 hoch, Oberkante Gehaeuse ~1609; Kabel am Rohr entlang in die Manschette."""
    ix, iy = ANSAUG_XY
    r_rohr, zs = ANSAUG_R_ROHR, ANSAUG_ZS
    lx, zr = ix + 72, 1571.0
    t.mat("schwarz", stab((ix + r_rohr - 4, iy, 1592), (lx, iy, 1592), 5))
    t.mat("schwarz", Pos(lx, iy, zr) * Cylinder(30, 38, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("chrom", Pos(lx, iy, zr - 6) * (Cylinder(34, 8, align=(Align.CENTER, Align.CENTER, Align.MIN))
                                        - Cylinder(28, 8, align=(Align.CENTER, Align.CENTER, Align.MIN))))
    dom = scale(Sphere(33), by=(1, 1, 2.4)) & box(-60, 60, -60, 60, -100, 0)
    t.mat("glas", Pos(lx, iy, zr - 2) * dom)
    t.mat("gummi", rohr_glatt([(lx - 30, iy, 1580), (ix + r_rohr + 4, iy, 1560), (ix + r_rohr + 4, iy, zs + 10)], 3.5, 15))


def _ansaugung(t: Sammler) -> None:
    """Oelbadluftfilter: Topf Ø 190 (Unterkante z 1020, Oberkante 1194; Nordhorn 1:34: ~Ø 200..215, durch die
    Haubenwand innen y 332 begrenzt) mit Spannring und 2 Buegelverschluessen, sitzt mit Aussparungen auf
    Kopf/Kruemmer/Steigflansch; Rohr Ø 66 durch das Dach (Manschette), Kragen mit 2 Ohren, glatte Kappe (Becher Ø 92,
    Deckel Ø 140, Oberkante 1740; Nordhorn 0:10/2:46), Arbeitsleuchte mit Glasdom am Rohr (DSC04729)."""
    _luftfilter_topf(t)
    _ansaugrohr(t)
    _ansaugkappe(t)
    _arbeitsleuchte(t)


# ======================================================================================
# Fassade (wird von modell.py aufgerufen)
# ======================================================================================
def motor() -> Sammler:
    """Motor D57 mit Kuehler, Riementrieb, Einspritzanlage, Anlasser und Anbauteilen."""
    t = Sammler("motor")
    _block(t)
    _kopf(t)
    _seitendeckel(t)
    _links_zusatz(t)
    _einspritzanlage(t)
    _riementrieb(t)
    _lichtmaschine(t)
    _kuehler(t)
    _schwungradgehaeuse(t)
    _anlasser(t)
    _anbauteile_rechts(t)
    _block_rechts(t)
    return t


def auspuff() -> Sammler:
    """Abgaskruemmer rechts -> offenes glattes Auspuffrohr Ø 48 (ohne Klappe, Gewicht, Schelle; DSC04729/30);
    Ansaugrohr links: Oelbadtopf mit Spannring unter der Haube, Rohr Ø 66 durch das Dach, Kragen, Kappe, Leuchte."""
    t = Sammler("auspuff")
    _auspuff(t)
    _ansaugung(t)
    return t
