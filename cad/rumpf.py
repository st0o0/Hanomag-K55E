"""Rumpf der K 55 E: Rahmen, Querblattfeder, Getriebeblock, Endantriebe, Plattform, Zugmaul.

Original-mm, X ab Maskenfront nach hinten, Y nach rechts, Z ab Boden.
Schnittstellen siehe referenz/MASSKONZEPT.md und cad/common.py (HAUPTMASSE).

Aufbau (Fotobefund fz_01/04/08, Wiking-Chassis, Prospekt; Fussraum Video 121-140):
  * zwei U-Profil-Laengstraeger (offen nach innen) mit Nietreihen, vorn ein
    Quertraeger unter der Maske mit Zugoese,
  * Querblattfeder unter der Oelwanne (x = 560), Federbuegel in der Mitte,
    die Federaugen haengen in Jochen, die auf den Kettenrahmen aufliegen,
  * Getriebeblock: runde Kupplungsglocke (Flansch bei FLANSCH_GLOCKE_X 1090, r 300
    wie das Schwungradgehaeuse des Motors, verjuengt sich kegelig) - Zwischenflansch -
    Kupplungsgehaeuse (Kasten unter dem Trittblech) - Wechselgetriebe -
    Hinterachsgehaeuse mit runden Lenkbremsdeckeln - hochkant stehender Heckkasten,
  * eckige Endantriebsgehaeuse um die Triebradachse, Flansch bei y = +-330,
  * Plattform auf DECK_Z (glattes Blech) mit abgekanteten Aussenkanten, Heckschuerzen,
    Innenwangen und Konsolen (nur innerhalb y = +-430, die Kette laeuft ab y = 435),
    dazwischen der abgesenkte Fussraum (Boden und Seitenwaende, Blech baut fahrerstand.py),
  * Zugmaul: gruener Kasten mit Deckplatte, waagerechter Bolzen mit Buegelschaekel.

Die rechte Seite (y > 0) wird gebaut und an der XZ-Ebene gespiegelt.
"""

from __future__ import annotations

import math
from functools import lru_cache

from build123d import (
    Align,
    Axis,
    Box,
    Circle,
    Cone,
    Cylinder,
    Edge,
    Part,
    Plane,
    Polyline,
    Pos,
    Rectangle,
    RectangleRounded,
    Rot,
    Shape,
    Sphere,
    Vector,
    Wire,
    extrude,
    fillet,
    make_face,
    mirror,
    sweep,
)

from .common import (
    DECK_B,
    DECK_X0,
    DECK_X1,
    DECK_Z,
    FLANSCH_GLOCKE_X,
    FW_X0,
    FW_X1,
    FW_Y0,
    FW_Y1,
    FW_Z0,
    FW_Z1,
    KETTE_B,
    MASKE_UK,
    RAHMEN_Z1,
    TRAEGER_Z0,
    TRAEGER_Z1,
    X_BREMSE,
    X_TRIEB,
    Y_KETTE,
    Y_TRAEGER,
    Z_TRIEB,
    Sammler,
    box,
    kasten_rund,
    rad_x,
    rad_y,
    ring_x,
    schraubenkreis,
    schraubenreihe,
    sechskant,
    stab,
)

# DECK_* werden von fahrerstand.py ueber dieses Modul importiert -> hier bewusst re-exportiert.
__all__ = ["DECK_B", "DECK_X0", "DECK_X1", "DECK_Z", "rumpf"]

Teile = list[Shape]

# =====================================================================================================
# Parameter (Original-mm), nach Bauteil gegliedert
# =====================================================================================================

# --- Laengstraeger ---
TR_X0, TR_X1 = 100.0, 1500.0               # Laenge des U-Profils
TR_B, TR_S = 80.0, 12.0                    # Flanschbreite, Blechstaerke
TR_YI = Y_TRAEGER - TR_B / 2               # Innenkante (Flanschende) 200
TR_YA = Y_TRAEGER + TR_B / 2               # Aussenkante Steg 280

# --- Plattform / Kotfluegel ---
BLECH = 10.0                               # Trittblech (>= 1,2 mm Modell)
RIFFEL_H = 4.0                             # Plattformblech: Blech + Riffelhoehe = Gesamtdicke 14 (Riffel nur auf Pedalen)
DECK_UK = DECK_Z - RIFFEL_H - BLECH        # Unterkante Trittblech 901
Y_KETTE_INNEN = Y_KETTE - KETTE_B / 2      # 435: hier beginnt die Kette
Y_WANGE = Y_KETTE_INNEN - 5                # Aussenseite der Kotfluegel-Innenwange 430
X_KETTE_HINTEN = X_TRIEB + 402.0           # hinterster Punkt der Greifer am Triebrad
KOT_YA = DECK_B / 2                        # Aussenkante der Plattform
KOT_X0 = 1090.0                            # Kotfluegelstreifen ab Haubenende (Nordhorn 2:44, 0:08: Schuerze unterm Tank zu)
KOT_XQ0 = X_KETTE_HINTEN + 40              # Querkonsole hinten: Vorderkante
KOT_XQ1 = DECK_X1 - BLECH                  # Querkonsole hinten: Hinterkante (vor der Heckschuerze)

# --- Querblattfeder ---
X_FEDER = 560.0
FEDER_B = 90.0                             # Lagenbreite (in x)
FEDER_D = 13.0                             # Lagendicke
FEDER_N = 5                                # Anzahl Lagen
FEDER_OK = 285.0                           # Oberkante Mitte (unter der Oelwanne, z = 320)
FEDER_YE = 455.0                           # Ende Hauptlage (Federauge dahinter)
FEDER_HUB = 215.0                          # Anstieg bis zum Ende
Y_JOCH = 508.0                             # Joch nur ueber der inneren Leitradgabel-Wange (y 485..510)
Z_GABEL = RAHMEN_Z1 + 3                    # Oberkante Gabelwange
FEDER_R = (FEDER_YE**2 + FEDER_HUB**2) / (2 * FEDER_HUB)
FEDER_ZC = FEDER_OK + FEDER_R              # Kreismittelpunkt (Feder "laechelt")

# --- Fussraum (Masse FW_*, X_BREMSE in common.py) ---
FW_WAND = 10.0                             # Blechstaerke der Seitenwaende
KG_Z1 = FW_Z0                              # Oberkante Kupplungsgehaeuse / Wechselgetriebe (unter dem Fussraum)

# --- Getriebeblock: Kupplungsglocke ---
GLOCKE_X0 = FLANSCH_GLOCKE_X               # Anschlussflansch Motor / Kupplungsglocke 1090
GLOCKE_X1 = 1640.0                         # Ende Kupplungsgehaeuse = Beginn Wechselgetriebe
GLOCKE_XM = 1400.0                         # Zwischenflansch Glocke -> Kupplungsgehaeuse (vor DECK_X0 1430)
GLOCKE_ZM = 640.0                          # Achshoehe der Glocke = SG_Z in motor.py (Schwungradgehaeuse)
GLOCKE_R0 = 300.0                          # Flanschradius vorn = Schwungradgehaeuse r 300 (Oberkante 940 <= 950)
GLOCKE_R1 = 205.0                          # Radius des Glockenschafts (Oberkante 845, Tankauflage ab 962)
GLOCKE_R2 = 212.0                          # Radius Zwischenflansch (Oberkante 852, vor DECK_X0)
GLOCKE_XK = 1250.0                         # Ende des Kegels
GLOCKE_FLANSCH_D = 26.0                    # Dicke des Motorflansches und des Zwischenflansches

# --- Getriebeblock: Wechselgetriebe, Hinterachse, Heckkasten ---
GETR_X1 = 2080.0                           # Ende Wechselgetriebe / Beginn Hinterachse
ACHS_X1 = 2380.0                           # Ende Hinterachsgehaeuse
HECK_X1 = 2735.0                           # Rueckwand Heckkasten
GETR_Z0, GETR_Z1 = 360.0, DECK_UK          # Gehaeuse traegt das Mittelblech

# --- Lenkbremse / Endantrieb ---
# Oberkante 640 = Fussraumboden (Gehaeuse tief, damit der Fussraum bis y -300 reicht)
Z_BREMSE, R_BREMSE = 480.0, 160.0
Y_BREMSE_AUSSEN = 365.0
Y_FLANSCH = 330.0                          # Flansch Hinterachsgehaeuse / Endantrieb
Y_LAGER = 425.0                            # Triebrad-Innennabe endet hier (Flansch r 155)
Y_ENDANTRIEB = 400.0                       # Aussenwand Endantriebsgehaeuse (Schwinglager ab y 440)
R_LAGERROHR = 165.0

# --- Zugmaul ---
ZM_X0, ZM_X1 = 2540.0, 2800.0              # Kasten unter dem Heckkasten (Oberkante = Heckkasten-Unterseite 500)
ZM_YB = 130.0                              # halbe Kastenbreite
ZM_Z0, ZM_Z1 = 365.0, 492.0                # Unter-/Oberkante Kasten
ZM_ZB = 428.0                              # Bolzenhoehe
ZM_XB1 = 2880.0                            # Bolzenende
ZM_YL = 40.0                               # halbe Schaekelweite


# =====================================================================================================
# Private Helfer
# =====================================================================================================
@lru_cache(maxsize=1)
def _niet_form() -> Part:
    """Halbrundniet (r 9): flacher Zylinder mit verrundeter Kuppe, einmal gebaut."""
    c = Cylinder(9.0, 6, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return fillet(c.edges().sort_by(Axis.Z)[-1], 4.0)


@lru_cache(maxsize=1)
def _riffel_form() -> Part:
    """Eine Riffelrippe fuer das Traenenblech."""
    return Box(28, 9, RIFFEL_H, align=(Align.CENTER, Align.CENTER, Align.MIN))


def niet(p: tuple[float, float, float], normal: tuple[float, float, float]) -> Part:
    """Halbrundniet (r 9) an Punkt p, Kuppe in Richtung normal."""
    return Plane(origin=Vector(*p), z_dir=Vector(*normal)) * _niet_form()


def schrauben_rechteck(pl: Plane, w: float, h: float, teil: float = 110.0, sw: float = 20, hoehe: float = 10,
                       r_ecke: float = 0.0) -> Teile:
    """Sechskantkoepfe auf einem Rechteck (Breite w, Hoehe h) in der Ebene pl, normal = pl.z_dir.
    r_ecke > 0: die Eckschrauben sitzen auf dem Eckbogen (fuer verrundete Flansche)."""
    pts = []
    nx, ny = max(2, round(w / teil) + 1), max(2, round(h / teil) + 1)
    if r_ecke:
        k = r_ecke * (1 - math.sqrt(0.5))
        for sx in (-1, 1):
            for sy in (-1, 1):
                pts.append((sx * (w / 2 - k), sy * (h / 2 - k)))
    for i in range(1 if r_ecke else 0, nx - 1 if r_ecke else nx):
        x = -w / 2 + w * i / (nx - 1)
        pts += [(x, -h / 2), (x, h / 2)]
    for j in range(1, ny - 1):
        y = -h / 2 + h * j / (ny - 1)
        pts += [(-w / 2, y), (w / 2, y)]
    n = pl.z_dir
    return [sechskant(pl.from_local_coords(p), (n.X, n.Y, n.Z), sw, hoehe) for p in pts]


def deckel(pl: Plane, w: float, h: float, d: float = 10.0, r: float = 20.0, teil: float = 110.0, sw: float = 18) -> Teile:
    """Rechteckiger Gehaeusedeckel mit Schraubenkranz auf der Ebene pl (nach aussen = z_dir)."""
    platte = extrude(pl * RectangleRounded(w, h, r), amount=d)
    vorne = Plane(origin=pl.from_local_coords((0, 0, d)), x_dir=pl.x_dir, z_dir=pl.z_dir)
    return [platte, *schrauben_rechteck(vorne, w - 2.2 * sw, h - 2.2 * sw, teil, sw, 8)]


def _rippen_paar(x0: float, x1: float, y_in: float, y_aus: float, z0: float, z1: float) -> Teile:
    """Je eine Rippe (Quader) links und rechts der Mittelebene, y_in..y_aus als Betrag."""
    t = []
    for s in (-1, 1):
        y0, y1 = sorted((s * y_in, s * y_aus))
        t.append(box(x0, x1, y0, y1, z0, z1))
    return t


def _spiegeln(teile: Teile) -> Teile:
    return [mirror(s, about=Plane.XZ) for s in teile]


# =====================================================================================================
# Rahmen
# =====================================================================================================
def laengstraeger() -> Teile:
    """Rechter U-Profil-Laengstraeger, Steg aussen, Oeffnung nach innen, mit Nieten."""
    t = []
    prof = Polyline((TR_YI, TRAEGER_Z0), (TR_YA, TRAEGER_Z0), (TR_YA, TRAEGER_Z1), (TR_YI, TRAEGER_Z1),
                    (TR_YI, TRAEGER_Z1 - TR_S), (TR_YA - TR_S, TRAEGER_Z1 - TR_S),
                    (TR_YA - TR_S, TRAEGER_Z0 + TR_S), (TR_YI, TRAEGER_Z0 + TR_S), close=True)
    t.append(extrude(Plane.YZ.offset(TR_X0) * make_face(prof), amount=TR_X1 - TR_X0))
    # Nietreihen am Steg (zwei Reihen) und auf dem Obergurt
    for x in range(int(TR_X0) + 60, int(TR_X1) - 20, 95):
        for z in (TRAEGER_Z0 + 28, TRAEGER_Z1 - 28):
            t.append(niet((x, TR_YA, z), (0, 1, 0)))
    for x in range(int(TR_X0) + 110, int(TR_X1) - 60, 190):
        t.append(niet((x, Y_TRAEGER + 8, TRAEGER_Z1), (0, 0, 1)))
    t += _verstaerkungslaschen()
    t += _glockenanschluss()
    return t


def _verstaerkungslaschen() -> Teile:
    """Verstaerkungsbleche (Laschen) an den Motorbock-Stellen, je 2 x 2 Schrauben."""
    t = []
    for xm in (560, 1260):
        t.append(box(xm - 70, xm + 70, TR_YA, TR_YA + 8, TRAEGER_Z0 + 10, TRAEGER_Z1 - 10))
        for z in (TRAEGER_Z0 + 40, TRAEGER_Z1 - 40):
            t += schraubenreihe((xm - 45, TR_YA + 8, z), (xm + 45, TR_YA + 8, z), 2, (0, 1, 0), 22, 10)
    return t


def _glockenanschluss() -> Teile:
    """Anschluss an die Kupplungsglocke: Winkel mit 4 Schrauben und Unterlegscheiben."""
    t = [box(TR_X1 - 90, TR_X1, TR_YA, TR_YA + 10, TRAEGER_Z0, TRAEGER_Z1)]
    for x in (TR_X1 - 65, TR_X1 - 25):
        for z in (TRAEGER_Z0 + 35, TRAEGER_Z1 - 35):
            t.append(rad_y(x, TR_YA + 13, z, 20, 6))                      # Unterlegscheibe 6 mm
            t.append(sechskant((x, TR_YA + 16, z), (0, 1, 0), 22, 10))
    return t


def quertraeger_vorn() -> Teile:
    """Quertraeger unter der Maske (Oberkante 15 mm unter MASKE_UK) mit Zugoese; nichts vor x 10."""
    t = []
    z0, z1 = 280.0, MASKE_UK - 15.0       # Oberkante 510: unter der Maskenunterkante 525, Pumpe davor frei
    x0, x1 = 110.0, 205.0
    # liegendes U, Steg vorn
    t.append(box(x0, x0 + 14, -330, 330, z0, z1))
    t.append(box(x0, x1, -330, 330, z1 - 14, z1))
    t.append(box(x0, x1, -330, 330, z0, z0 + 14))
    # Kopfbleche, Verbindung zu den Laengstraegern
    for s in (-1, 1):
        y0, y1 = sorted((s * (TR_YI - 4), s * (TR_YA + 4)))
        t.append(box(x0, x1 + 40, y0, y1, z1 - 14, z1 + 2))
        y0, y1 = sorted((s * 316, s * 330))
        t.append(box(x0, x1, y0, y1, z0, z1))                 # Stirnblech seitlich
        t += schraubenreihe((x0, s * 300, z0 + 30), (x0, s * 300, z1 - 30), 2, (-1, 0, 0), 22, 10)
        t += schraubenreihe((x0, s * 160, z0 + 30), (x0, s * 160, z1 - 30), 2, (-1, 0, 0), 22, 10)
    # Zugoese vorn mittig
    t.append(box(60, x0, -45, 45, 300, 372))
    oese = Pos(55, 0, 336) * Cylinder(45, 72)
    t.append(oese - (Pos(55, 0, 336) * Cylinder(24, 80)))
    t.append(box(80, 110, -60, 60, 290, 382))                # Oesenbock
    return t


# =====================================================================================================
# Querblattfeder
# =====================================================================================================
def _federlagen() -> Teile:
    """Die gebogenen Federlagen (Kreisbogen um FEDER_ZC), von der Hauptlage nach innen kuerzer."""
    lagen = []
    for i in range(FEDER_N):
        ri = FEDER_R + i * FEDER_D
        laenge = 2 * (FEDER_YE - i * 85.0)
        ring = ring_x(X_FEDER, 0, FEDER_ZC, ri + FEDER_D, ri, FEDER_B - i * 2)
        lagen.append(ring & box(X_FEDER - 60, X_FEDER + 60, -laenge / 2, laenge / 2, FEDER_ZC - ri - 10, FEDER_ZC - ri + 320))
    return lagen


def _federende(s: int, lack: Teile, schwarz: Teile) -> None:
    """Federauge, Joch auf dem Kettenrahmen und Federstuhl am Ende der Feder (s = Seite +-1)."""
    zc, R = FEDER_ZC, FEDER_R
    z_ok = zc - math.sqrt(R**2 - FEDER_YE**2)                  # Oberkante Hauptlage am Ende
    ya, za = s * (FEDER_YE + 18), z_ok + 14
    schwarz.append(ring_x(X_FEDER, ya, za, 28, 14, FEDER_B))
    # Joch: zwei Wangen, Grundplatte auf dem Kettenrahmen, Bolzen
    jy0, jy1 = sorted((s * (FEDER_YE - 15), s * Y_JOCH))
    for xw in (X_FEDER - FEDER_B / 2 - 16, X_FEDER + FEDER_B / 2 + 1):
        w = box(xw, xw + 15, jy0, jy1, Z_GABEL, za + 40)
        w = fillet(w.edges().filter_by(Axis.X).group_by(Axis.Z)[-1], 12)
        lack.append(w)
    py0, py1 = sorted((s * (Y_JOCH - 25), s * Y_JOCH))
    lack.append(box(X_FEDER - FEDER_B / 2 - 16, X_FEDER + FEDER_B / 2 + 16, py0, py1, Z_GABEL, Z_GABEL + 12))
    lack.append(rad_x(X_FEDER, ya, za, 12, FEDER_B + 50))
    for xs in (-1, 1):
        lack.append(sechskant((X_FEDER + xs * (FEDER_B / 2 + 17), ya, za), (xs, 0, 0), 26, 12))
    # Federstuhl: Laengstraeger stuetzt sich bei y = +-211 auf die Feder
    st = box(X_FEDER - 40, X_FEDER + 40, s * TR_YI - 4 * s, s * (TR_YI + 26), 250, TRAEGER_Z0 + 2)
    lack.append(st & rad_x(X_FEDER, 0, zc, R, 200))


def _federbuegel() -> Teile:
    """Federbuegel (Mitte): Klemmplatten oben/unten, 4 Stehbolzen mit Muttern, Herzbolzen."""
    t = []
    z_unten = FEDER_OK - FEDER_N * FEDER_D
    t.append(box(X_FEDER - 62, X_FEDER + 62, -90, 90, FEDER_OK, FEDER_OK + 14))
    t.append(box(X_FEDER - 62, X_FEDER + 62, -90, 90, z_unten - 16, z_unten))
    for xs in (-1, 1):
        for ys in (-1, 1):
            x, y = X_FEDER + xs * 52, ys * 62
            t.append(stab((x, y, z_unten - 30), (x, y, FEDER_OK + 20), 9))
            t.append(sechskant((x, y, FEDER_OK + 14), (0, 0, 1), 26, 6))
            t.append(sechskant((x, y, z_unten - 16), (0, 0, -1), 26, 12))
    t.append(Pos(X_FEDER, 0, FEDER_OK + 14) * Cylinder(15, 6, align=(Align.CENTER, Align.CENTER, Align.MIN)))  # Herzbolzen
    return t


def querfeder() -> tuple[Teile, Teile]:
    """Querblattfeder mit Federbuegeln, Federstuehlen und Jochen. Liefert (lack, schwarz)."""
    lack: Teile = []
    schwarz: Teile = _federlagen()
    for s in (-1, 1):
        _federende(s, lack, schwarz)
    lack += _federbuegel()
    return lack, schwarz


# =====================================================================================================
# Getriebeblock
# =====================================================================================================
def _glocke() -> Teile:
    """Kupplungsglocke: Motorflansch, Kegel mit Radialrippen, Schaft, Zwischenflansch, Ablass."""
    t = []
    zm = GLOCKE_ZM
    oben = Pos(0, (TRAEGER_Z1 + 5 + 950) / 2) * Rectangle(2 * 320, 950 - TRAEGER_Z1 - 5)
    unten = Pos(0, (320 + TRAEGER_Z1 + 5) / 2) * Rectangle(2 * 186, TRAEGER_Z1 + 5 - 320)
    prof = (Pos(0, zm) * Circle(GLOCKE_R0)) & (oben + unten)
    xk0 = GLOCKE_X0 + GLOCKE_FLANSCH_D
    t.append(extrude(Plane.YZ.offset(GLOCKE_X0) * prof, amount=GLOCKE_FLANSCH_D))                   # Flansch
    t.append(Pos(xk0 + (GLOCKE_XK - xk0) / 2, 0, zm) * Rot(0, 90, 0) * Cone(GLOCKE_R0 - 12, GLOCKE_R1, GLOCKE_XK - xk0))
    t.append(rad_x((GLOCKE_XK + GLOCKE_XM) / 2, 0, zm, GLOCKE_R1, GLOCKE_XM - GLOCKE_XK))
    # Radialrippen auf dem Kegel (Rippenkopf am Flansch 10 hoch, keine Keilspitze auf dem Kegel)
    rp = Polyline((xk0, GLOCKE_R0 - 14), (GLOCKE_XK + 30, GLOCKE_R1 - 2), (GLOCKE_XK + 30, GLOCKE_R1 + 10),
                  (xk0, GLOCKE_R0 - 2), close=True)
    rippe = extrude(Plane.XY * make_face(rp), amount=7, both=True)    # Profil in x/y, Dicke in z
    rippe = Rot(90, 0, 0) * rippe                                      # -> Profil in x/z, Dicke in y
    for w in (90, 45, -45, 135, -90):
        t.append(Pos(0, 0, zm) * Rot(w, 0, 0) * rippe)
    # Schraubenkranz am Motorflansch (Koepfe auf der Flanschrueckseite)
    for i in range(24):
        ang = math.radians(i * 15 + 7.5)
        y, z = (GLOCKE_R0 - 18) * math.cos(ang), zm + (GLOCKE_R0 - 18) * math.sin(ang)
        if z < TRAEGER_Z1 + 5 and abs(y) > 170:
            continue
        t.append(sechskant((xk0 - 0.3, y, z), (1, 0, 0), 18, 8))
    # Zwischenflansch Glocke -> Kupplungsgehaeuse mit Schraubenkranz
    t.append(rad_x(GLOCKE_XM + 13, 0, zm, GLOCKE_R2, GLOCKE_FLANSCH_D))
    t += schraubenkreis((GLOCKE_XM + GLOCKE_FLANSCH_D, 0, zm), (1, 0, 0), GLOCKE_R2 - 14, 16, 16, 8)
    t.append(sechskant((1200, 0, zm - GLOCKE_R1 - 30), (0, 0, -1), 30, 12))   # Glocken-Ablass
    return t


def _kupplungsgehaeuse() -> Teile:
    """Kasten mit runden Kanten bis zum Wechselgetriebe, Flansch hinten, Rippen und Schaudeckel."""
    t = []
    zf = GLOCKE_XM
    t.append(kasten_rund(zf + GLOCKE_FLANSCH_D, GLOCKE_X1, -255, 255, 350, KG_Z1, 70, Axis.X))
    t.append(kasten_rund(GLOCKE_X1 - 12, GLOCKE_X1 + 14, -262, 262, 345, KG_Z1, 60, Axis.X))
    pl = Plane(origin=(GLOCKE_X1 - 12, 0, (345 + KG_Z1) / 2), x_dir=(0, 1, 0), z_dir=(-1, 0, 0))
    t += schrauben_rechteck(pl, 490, KG_Z1 - 345 - 40, 100, 18, 9, r_ecke=60)
    # Laengsrippen und Kupplungs-Schaudeckel an beiden Seiten
    for s in (-1, 1):
        for z in (420, 590):
            y0, y1 = sorted((s * 250, s * 268))
            t.append(box(zf + 40, GLOCKE_X1 - 12, y0, y1, z - 9, z + 9))
        pl = Plane(origin=(1540, s * 255, 520), x_dir=(1, 0, 0), z_dir=(0, s, 0))
        t += deckel(pl, 120, 170, 8, 18, 60, 16)
    t.append(sechskant((1550, 0, 350), (0, 0, -1), 30, 12))            # Kupplungs-Ablass
    return t


def _wechselgetriebe() -> Teile:
    """Wechselgetriebe mit Rippen an Seiten und Boden."""
    t = [kasten_rund(GLOCKE_X1, GETR_X1, -230, 230, GETR_Z0, KG_Z1, 45, Axis.X)]
    for x in range(1680, int(GETR_X1) - 20, 70):
        t += _rippen_paar(x - 8, x + 8, 228, 244, GETR_Z0 + 40, KG_Z1 - 30)
        t.append(box(x - 8, x + 8, -170, 170, GETR_Z0 - 14, GETR_Z0 + 2))
    return t


def _hinterachsgehaeuse() -> Teile:
    """Hinterachsgehaeuse (breiter, nimmt Lenkbremsen und Endantriebe auf) mit Flansch und Ablassschrauben."""
    t = [kasten_rund(GETR_X1 - 10, ACHS_X1, -Y_FLANSCH + 6, Y_FLANSCH - 6, GETR_Z0 - 10, GETR_Z1, 55, Axis.X),
         kasten_rund(GETR_X1 - 24, GETR_X1 + 4, -Y_FLANSCH + 2, Y_FLANSCH - 2, GETR_Z0 - 20, GETR_Z1, 55, Axis.X)]
    pl = Plane(origin=(GETR_X1 - 24, 0, (GETR_Z0 + GETR_Z1) / 2 - 10), x_dir=(0, 1, 0), z_dir=(-1, 0, 0))
    t += schrauben_rechteck(pl, 2 * Y_FLANSCH - 50, GETR_Z1 - GETR_Z0 - 30, 105, 18, 9, r_ecke=55)
    t.append(sechskant((1860, 0, GETR_Z0 - 14), (0, 0, -1), 32, 14))
    t.append(sechskant((2230, 0, GETR_Z0 - 10), (0, 0, -1), 32, 14))
    return t


def _heckkasten() -> Teile:
    """Heckkasten: hochkant, oben breiter, Rueckwand mit Deckel und Zapfwellen-Lagerdeckel, Unterteil."""
    hk = kasten_rund(ACHS_X1 - 10, HECK_X1, -210, 210, 500, GETR_Z1, 40, Axis.X)
    t = [fillet(hk.edges().filter_by(Axis.Y).group_by(Axis.X)[-1], 30)]
    for z in (560, 650, 740):                               # Seitenrippen
        t += _rippen_paar(ACHS_X1 + 20, HECK_X1 - 40, 208, 222, z - 8, z + 8)
    pl = Plane(origin=(HECK_X1, 0, 630), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    t += deckel(pl, 330, 220, 12, 30, 80, 18)
    t.append(rad_x(HECK_X1 + 12 + 14, 0, 640, 70, 28))     # Zapfwellen-Lagerdeckel
    t += schraubenkreis((HECK_X1 + 40, 0, 640), (1, 0, 0), 55, 6, 16, 8)
    t.append(rad_x(HECK_X1 + 50, 0, 640, 26, 22))
    t.append(sechskant((HECK_X1 + 12, 120, 540), (1, 0, 0), 28, 12))   # Oelstandschraube
    # Unterteil (Kegelradgehaeuse), traegt den Zugpendel-Drehpunkt
    t.append(kasten_rund(ACHS_X1 - 10, 2520, -150, 150, GETR_Z0 - 10, 520, 35, Axis.X))
    return t


def getriebe() -> Teile:
    """Mittiger Getriebeblock (symmetrisch, ganz gebaut)."""
    return _glocke() + _kupplungsgehaeuse() + _wechselgetriebe() + _hinterachsgehaeuse() + _heckkasten()


def lenkbremse() -> Teile:
    """Rechtes Lenkbremsgehaeuse mit rundem Deckel (Trommelachse quer)."""
    t = []
    y_in = 228.0
    t.append(rad_y(X_BREMSE, (y_in + Y_BREMSE_AUSSEN - 14) / 2, Z_BREMSE, R_BREMSE - 12, Y_BREMSE_AUSSEN - 14 - y_in))
    # Deckelflansch, Deckel mit Woelbung und Schraubenkranz
    t.append(rad_y(X_BREMSE, Y_BREMSE_AUSSEN - 7, Z_BREMSE, R_BREMSE, 14))
    t += schraubenkreis((X_BREMSE, Y_BREMSE_AUSSEN, Z_BREMSE), (0, 1, 0), R_BREMSE - 17, 12, 18, 9)
    t.append(rad_y(X_BREMSE, Y_BREMSE_AUSSEN + 6, Z_BREMSE, R_BREMSE - 40, 12))
    nabe = rad_y(X_BREMSE, Y_BREMSE_AUSSEN + 22, Z_BREMSE, 55, 20)
    t.append(fillet(nabe.edges().sort_by(Axis.Y)[-1], 6))
    t.append(sechskant((X_BREMSE, Y_BREMSE_AUSSEN + 32, Z_BREMSE), (0, 1, 0), 34, 12))
    # Nachstellbock unten und Betaetigungshebel
    zb = Z_BREMSE - R_BREMSE
    t.append(box(X_BREMSE - 30, X_BREMSE + 30, y_in + 30, Y_BREMSE_AUSSEN - 20, zb - 25, zb + 20))
    t.append(sechskant((X_BREMSE, Y_BREMSE_AUSSEN - 50, Z_BREMSE - R_BREMSE - 25), (0, 0, -1), 24, 12))
    # Rippen zwischen Gehaeuse und Getriebe
    for dz in (-110, 110):
        t.append(box(X_BREMSE - 10, X_BREMSE + 10, 225, Y_BREMSE_AUSSEN - 16, Z_BREMSE + dz - 40, Z_BREMSE + dz + 40))
    return t


def endantrieb() -> Teile:
    """Rechtes eckiges Endantriebsgehaeuse um die Triebradachse."""
    t = []
    x0, x1, z0, z1 = X_TRIEB - 175, X_TRIEB + 190, Z_TRIEB - 200, Z_TRIEB + 250
    y_aus = Y_ENDANTRIEB                                    # Aussenwand, davor Lagerrohr bis y 425
    t.append(kasten_rund(x0, x1, Y_FLANSCH, y_aus, z0, z1, 70, Axis.Y))
    # Anschlussflansch zum Hinterachsgehaeuse
    t.append(kasten_rund(x0 - 32, x1 + 32, Y_FLANSCH - 4, Y_FLANSCH + 20, z0 - 32, z1 + 32, 90, Axis.Y))
    pl = Plane(origin=((x0 + x1) / 2, Y_FLANSCH + 20, (z0 + z1) / 2), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
    t += schrauben_rechteck(pl, x1 - x0 + 30, z1 - z0 + 30, 85, 20, 10, r_ecke=85)
    # Aussenwand: Versteifungsrippe oben, Lagerrohr zur Triebradnabe (Nabenflansch r 155 bei y 425)
    t.append(box(x0 + 40, x1 - 40, y_aus - 2, y_aus + 6, Z_TRIEB + 221, Z_TRIEB + 239))
    lager = rad_y(X_TRIEB, (y_aus + Y_LAGER) / 2 - 1, Z_TRIEB, R_LAGERROHR, Y_LAGER - y_aus + 2)
    t.append(fillet(lager.edges().sort_by(Axis.Y)[-1], 6))
    t += schraubenkreis((X_TRIEB, y_aus, Z_TRIEB), (0, 1, 0), R_LAGERROHR + 18, 12, 20, 9, 15)
    # Oeleinfuellschraube oben hinten, Ablass unten
    t.append(sechskant((X_TRIEB + 135, y_aus, Z_TRIEB + 200), (0, 1, 0), 30, 12))
    t.append(sechskant((X_TRIEB, (Y_FLANSCH + y_aus) / 2, z0), (0, 0, -1), 28, 12))
    # Stuetze vom Gehaeuse zum Kotfluegel
    t.append(box(X_TRIEB - 12, X_TRIEB + 12, Y_FLANSCH + 20, Y_WANGE, z1 - 40, DECK_UK))
    return t


# =====================================================================================================
# Plattform
# =====================================================================================================
def riffelblech(x0: float, x1: float, y0: float, y1: float, z: float, teilung: float = 50.0,
                oy: float | None = None, ny: int | None = None) -> Teile:
    """Traenenblech: Rauten aus kurzen Rippen, abwechselnd +-45 Grad."""
    riffel = _riffel_form()
    t = []
    nx = int((x1 - x0) / teilung)
    ny = ny or int((y1 - y0) / teilung)
    ox = x0 + ((x1 - x0) - nx * teilung) / 2
    oy = y0 + ((y1 - y0) - ny * teilung) / 2 if oy is None else oy
    for i in range(nx):
        for j in range(ny):
            w = 45 if (i + j) % 2 else -45
            t.append(Pos(ox + (i + 0.5) * teilung, oy + (j + 0.5) * teilung, z) * Rot(0, 0, w) * riffel)
    return t


def _mittelblech() -> Teile:
    """Mittelblech zwischen den Kotfluegeln: vor und hinter dem Fussraum voll, dazwischen links ein Streifen."""
    t = []
    if FW_X0 > DECK_X0:
        t.append(box(DECK_X0, FW_X0, -Y_FLANSCH, Y_FLANSCH, DECK_UK, DECK_Z))         # vor dem Fussraum
    t.append(box(FW_X1, DECK_X1, -Y_FLANSCH, Y_FLANSCH, DECK_UK, DECK_Z))             # hinter dem Fussraum
    # linker Streifen fuellt den Ausschnitt der Kotfluegelplatte (kotfluegel(): ab FW_Y1 + FW_WAND), rechts ist die Wand die Kante
    t.append(box(FW_X0, FW_X1, -(FW_Y1 + FW_WAND), FW_Y0 - FW_WAND, DECK_UK, DECK_Z))
    return t


def _fussraum_waende() -> Teile:
    """Seitenwaende des Fussraums (tuerkis), von der Plattform bis auf das Getriebe; rechts bis DECK_Z."""
    return [box(FW_X0, FW_X1, FW_Y0 - FW_WAND, FW_Y0, FW_Z0, DECK_UK + 1),
            box(FW_X0, FW_X1, FW_Y1, FW_Y1 + FW_WAND, FW_Z0, DECK_Z),
            # schmaler Streifen links neben dem Armaturenkasten (Video 128: senkrechte tuerkise Wand)
            box(1485.0, 1485.0 + FW_WAND, FW_Y0, FW_Y0 + 8, 924.0, 1078.0)]


def _spritzwand_und_boden() -> Teile:
    """Spritzwand vorn unter dem Armaturenkasten (endet 1 mm unter Werkzeugkasten/Konsolenblech) und Bodentraeger
    unter dem Fussraumblech neben dem Getriebe (das Blech ragt dort frei ueber die Rundung des Gehaeuses, |y| > 250)."""
    # nur ein niedriges Fussblech am Wannenende: darueber ist der Raum unter dem Armaturenkasten offen (Short c48/c50,
    # dahinter sieht man die Kupplungsglocke)
    t = [box(FW_X0, FW_X0 + FW_WAND, FW_Y0, FW_Y1, FW_Z1, FW_Z1 + 90.0)]
    for sx in (1500.0, 1990.0):
        t.append(box(sx - 14, sx + 14, 250.0, FW_Y1, FW_Z0 - 22.0, FW_Z0))
        t.append(box(sx - 14, sx + 14, FW_Y0, -250.0, FW_Z0 - 22.0, FW_Z0))
        t.append(box(sx - 14, sx + 14, FW_Y1 - 12, FW_Y1, FW_Z0 - 90.0, FW_Z0))     # Knotenblech an der Wand
        t.append(box(sx - 14, sx + 14, FW_Y0, FW_Y0 + 12, FW_Z0 - 90.0, FW_Z0))
    return t


def _inspektionsdeckel() -> Teile:
    """Inspektionsdeckel im Fussraumboden: dicke Platte (~18 hoch, dunkle Kante) mit grossen runden Schraubenkoepfen.
    Der Stutzen (fahrerstand.py STUTZEN) steht bei x 1894, y -118 -> Deckel dahinter (x 1975..2040)."""
    t = [kasten_rund(1975, 2040, -150, 90, FW_Z1, FW_Z1 + 18, 20)]
    for yy in (-135, -30, 75):
        t += schraubenreihe((1990, yy, FW_Z1 + 18), (2025, yy, FW_Z1 + 18), 2, (0, 0, 1), 24, 9)
    return t


def plattform_mitte() -> tuple[Teile, Teile]:
    """Mittelblech zwischen den Kotfluegeln mit abgesenktem Fussraum: vorn (Glocke offen darunter) und hinten
    (ab FW_X1, ueber dem Hinterachsgehaeuse) Plattformhoehe, dazwischen nur seitliche Streifen; der Fussraumboden
    (fahrerstand.py) liegt bei FW_Z1 auf dem Getriebe, die senkrechten Seitenwaende (tuerkis) reichen von dort bis
    zur Plattform. Liefert (lack, wand)."""
    return _mittelblech() + _spritzwand_und_boden() + _inspektionsdeckel(), _fussraum_waende()


def _kot_blech() -> Teile:
    """Glattes Trittblech bis DECK_Z (im Fussraum bis |y| FW_Y1 + FW_WAND ausgeschnitten), Abkantung mit gerolltem Rand."""
    t = []
    yi = Y_FLANSCH - 2
    yfw = FW_Y1 + FW_WAND
    for xa, xb, yy in ((KOT_X0, FW_X0, yi), (FW_X0, FW_X1, yfw), (FW_X1, DECK_X1, yi)):
        if xb > xa:
            t.append(box(xa, xb, yy, KOT_YA - BLECH, DECK_UK, DECK_Z))
    # nur eine schmale Abkantung (5 mm unter dem Trittblech), die obere Kette bleibt ueber die ganze Laenge sichtbar;
    # Unterkante Rand DECK_UK - 10 = 891, Spalt zu den Greifern 123 (ueber dem Triebrad) .. 146 (Mitte)
    t.append(box(KOT_X0, DECK_X1, KOT_YA - BLECH, KOT_YA, DECK_UK - 5, DECK_Z - 2))
    t.append(stab((KOT_X0, KOT_YA - 2, DECK_Z - 2), (DECK_X1, KOT_YA - 2, DECK_Z - 2), 8))
    t.append(stab((KOT_X0, KOT_YA - BLECH / 2, DECK_UK - 5), (DECK_X1, KOT_YA - BLECH / 2, DECK_UK - 5), 5))
    return t


def _kot_schuerze() -> Teile:
    """Heckschuerze (hinten, bis zur Ecke), unten mit Wulst."""
    ya, zs = KOT_YA, DECK_UK - 140
    xm, ym = DECK_X1 - BLECH / 2, ya - BLECH / 2
    return [box(DECK_X1 - BLECH, DECK_X1, 215, ya, zs, DECK_UK + BLECH),
            stab((xm, 215, zs), (xm, ym, zs), 9),
            Pos(xm, ym, zs) * Sphere(9),
            stab((xm, ym, zs), (xm, ym, DECK_UK - 90), 9)]


def _kot_wange_konsolen() -> Teile:
    """Kotfluegel-Innenwange (Winkel) entlang der Kette, Querkonsole hinten und dreieckige Knotenbleche."""
    ya = KOT_YA
    t = [box(KOT_X0, X_KETTE_HINTEN, Y_WANGE - 12, Y_WANGE, DECK_UK - 60, DECK_UK)]
    t += schraubenreihe((KOT_X0 + 60, Y_WANGE, DECK_UK - 30), (X_KETTE_HINTEN - 50, Y_WANGE, DECK_UK - 30),
                        12, (0, 1, 0), 18, 8)
    # Querkonsole hinten (hinter dem Triebrad), volle Breite bis zur Abkantung
    t.append(box(KOT_XQ0, KOT_XQ0 + 12, 205, ya - BLECH, DECK_UK - 70, DECK_UK))
    t.append(box(KOT_XQ0, KOT_XQ1, 205, ya - BLECH, DECK_UK - 12, DECK_UK))
    # Konsolen (dreieckige Knotenbleche) unter dem Trittblech, nur innerhalb y < 430; die vorderen beginnen
    # ausserhalb der linken Fussraumwand (gespiegelt auch rechts)
    z_tief = DECK_Z - 60    # hoechstens 60 unter dem Trittblech: darunter bleibt der Blick auf die Kette frei
    for x, y_in in ((1520, FW_Y1 + FW_WAND), (1680, FW_Y1 + FW_WAND), (2470, 210), (2600, 210)):
        prof = Polyline((y_in, DECK_UK), (Y_WANGE - 12, DECK_UK), (Y_WANGE - 12, DECK_UK - 60), (y_in, z_tief), close=True)
        t.append(extrude(Plane.YZ.offset(x - 6) * make_face(prof), amount=12))
    # Knotenbleche hinten aussen (ueber dem Triebrad-Ende frei)
    for y in (560, 760):
        prof = Polyline((KOT_XQ0, DECK_UK), (KOT_XQ0, DECK_UK - 70), (KOT_XQ1, DECK_UK - 12), (KOT_XQ1, DECK_UK), close=True)
        t.append(extrude(Plane.XZ.offset(-y + 6) * make_face(prof), amount=12))
    return t


def _kot_schrauben() -> Teile:
    """Schrauben Trittblech -> Wange / Querkonsole. Die Koepfe sind bis ins Trittblech gefuehrt (Blechoberseite
    DECK_Z - RIFFEL_H, 2,4 mm eingesenkt), sonst stehen sie nur auf den Riffelspitzen und sind im Druck lose
    Einzelteile; die sichtbare Hoehe bleibt 5 ueber DECK_Z."""
    zk, hk = DECK_Z - 2.4, 5 + 2.4
    return (schraubenreihe((DECK_X0 + 40, Y_WANGE - 6, zk), (X_KETTE_HINTEN - 40, Y_WANGE - 6, zk), 10, (0, 0, 1), 16, hk)
            + schraubenreihe((KOT_XQ0 + 6, 260, zk), (KOT_XQ0 + 6, KOT_YA - 40, zk), 7, (0, 0, 1), 16, hk))


def kotfluegel() -> Teile:
    """Rechter Kotfluegel: glattes Trittblech, Abkantung aussen, Heckschuerze, Wange, Konsolen."""
    return _kot_blech() + _kot_schuerze() + _kot_wange_konsolen() + _kot_schrauben()


# =====================================================================================================
# Zugmaul
# =====================================================================================================
def _zugkasten(tuerkis: Teile, zink: Teile, blank: Teile) -> None:
    """Gruener Kasten unter dem Heckkasten mit grauer Deckplatte, Kugelkuppe und Befestigungsschrauben."""
    tuerkis.append(kasten_rund(ZM_X0, ZM_X1, -ZM_YB, ZM_YB, ZM_Z0, ZM_Z1, 14, Axis.Z))
    tuerkis.append(box(ZM_X0 + 30, ZM_X1 - 30, -ZM_YB - 6, ZM_YB + 6, ZM_Z0 + 40, ZM_Z0 + 52))  # Sicke rundum
    zink.append(kasten_rund(ZM_X0 - 8, ZM_X1 + 8, -ZM_YB - 8, ZM_YB + 8, ZM_Z1, ZM_Z1 + 8, 10, Axis.Z))  # Deckplatte, buendig
    zink.append(Pos(ZM_X0 + 60, 0, ZM_Z1 - 12) * Sphere(20))
    for y in (-90, 90):
        blank.append(sechskant((ZM_X0 + 20, y, ZM_Z0), (0, 0, -1), 22, 8))


def _zugbolzen(blank: Teile, schwarz: Teile) -> None:
    """Waagerechter Bolzen aus der Rueckwand des Kastens, Kopf mit Querloch, Schaekel mit Bolzen und Mutter."""
    zb, yl = ZM_ZB, ZM_YL
    schwarz.append(rad_x((ZM_X1 + ZM_XB1) / 2, 0, zb, 25, ZM_XB1 - ZM_X1 + 4))
    kopf = rad_x(ZM_XB1 - 6, 0, zb, 33, 14)
    schwarz.append(fillet(kopf.edges().sort_by(Axis.X)[-1], 5))
    xs = ZM_XB1 - 28                                        # Schaekelbolzen quer (Achse y) durch den Bolzen
    blank.append(rad_y(xs, 0, zb, 9, 2 * yl + 30))
    blank.append(rad_y(xs, yl + 20, zb, 16, 10))            # Bolzenkopf
    blank.append(sechskant((xs, -yl - 15, zb), (0, -1, 0), 26, 12))   # Mutter
    pfad = Wire([Edge.make_line((xs, -yl, zb + 14), (xs, -yl, zb)),
                 Edge.make_three_point_arc((xs, -yl, zb), (xs, 0, zb - yl), (xs, yl, zb)),
                 Edge.make_line((xs, yl, zb), (xs, yl, zb + 14))])
    blank.append(sweep(Plane(origin=(xs, -yl, zb + 14), z_dir=(0, 0, -1)) * Circle(8), path=pfad))


def zugpendel() -> tuple[Teile, Teile, Teile, Teile]:
    """Zugvorrichtung unter dem Heck (Video 145-154): gruener Kasten mit grauer Deckplatte und Kugelkuppe,
    hinten ein waagerechter Bolzen (Ø 50) mit Buegelschaekel (Schaekelbolzen + Mutter).
    Liefert (tuerkis, zink, blank, schwarz)."""
    tuerkis: Teile = []
    zink: Teile = []
    blank: Teile = []
    schwarz: Teile = []
    _zugkasten(tuerkis, zink, blank)
    _zugbolzen(blank, schwarz)
    return tuerkis, zink, blank, schwarz


# =====================================================================================================
# Fassade
# =====================================================================================================
def rumpf() -> Sammler:
    """Gesamter Rumpf: rechte Seite gebaut und gespiegelt, dazu die mittigen Baugruppen."""
    t = Sammler("lack")
    rechts = laengstraeger() + lenkbremse() + endantrieb() + kotfluegel()
    t += rechts
    t += _spiegeln(rechts)
    t += quertraeger_vorn()
    lack, schwarz = querfeder()
    t += lack
    t.mat("schwarz", schwarz)
    t += getriebe()
    pm, wand = plattform_mitte()
    t += pm
    t.mat("lack", wand)
    tuerkis, zink, blank, schwarz = zugpendel()
    t.mat("lack", tuerkis)
    t.mat("zink", zink)
    t.mat("blank", blank)
    t.mat("schwarz", schwarz)
    return t
