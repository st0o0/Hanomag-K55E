"""Planiereinrichtung FRISCH 55 FH2 (Frontschild, 2-Kolben-Hydraulik).

Wirkprinzip (Prospekt K 55 E, Einsatzfoto):
  Je Seite ein Schubbalken (Kastenprofil) aussen neben der Kette, hinten im Gelenkbock am Kettenrahmen gelagert
  (x = X_GELENK, z = Z_SCHUB), vorn ueber ein Zahnsegment (Neigungsverstellung) am Schild angelenkt. Die Schubbalken sind hinter
  dem Schild durch einen C-Rahmen verbunden. Auf dem Schubbalken sitzt der A-Bock (zwei Kastenstreben + Stegblech) mit dem
  Lagerauge im Scheitel. Der Hubzylinder liegt mit Mittelzapfen im Endkasten der Traverse; seine Kolbenstange greift nach vorn
  am A-Bock-Scheitel an. Einfahren zieht den Scheitel nach hinten -> Schubbalken dreht um das hintere Gelenk -> Schild hebt.
  Die Hydraulik (Pumpe, Steuerblock, Leitungen) steht in hydraulik.py, die gemeinsamen Traversen-/Zylindermasse in
  planiermasse.py.
  Hubhoehe 1120 mm ueber / 200 mm unter Fahrebene. Gezeichnet ist die Arbeitsstellung (Schneide auf der Fahrebene).

Bauteile:
  * Schild: gewoelbtes Blech mit flach umgekanteter Oberkante, Schneidleiste, Quertraeger und Rippen am Blechruecken,
    sichelfoermige Endbleche (Video 008/010/047/165/196).
  * Schubbalken: Kastenprofil, hinten 170 / vorn 230 hoch, aussen aufgeschweisste Spitzplatten, runde Lagernabe (Video 022/165).
  * A-Bock: Fuesse ABOCK_FUESSE auf dem Schubbalken, Scheitel ABOCK_SCHEITEL, Stegblech mit Dreieckausschnitt (Foto BS).
  * Hubzylinder: waagerecht auf z = TRAVERSE_Z bei y = +-Y_SCHUB, Kopf bei x ~ 1770, Rohr im Endkasten (Video 079..088, 116).
  * Traverse: zwei Endkaesten aussen (x 2395..2830) und dazwischen der Quertraeger, zugleich Oeltank, mit Schild "Frisch"
    auf der Rueckwand (Flickr 26271221407); der Mittelzapfen des Zylinders sitzt bei x 2520 (Foto BS).

Hubkinematik (Arbeitsstellung, Schubbalken waagerecht): Gelenk G = (1860, 400), Scheitel S = (1270, 1080),
  Zapfen Z = (2520, 1080), |SZ| = 1250. Schild 1120 hoch: Balken dreht um 24,1 Grad,
  |S'Z| = 939; Schild 200 tief: 4,3 Grad, |S''Z| = 1301 -> Hub 362 mm.
  Hubwerte sind nicht gegen das Original geprueft (im Video wird nicht gehoben). Herleitung: referenz/historie/planierschild.md.

Belege: Video Nordhorn (v.mp4 t=164/166, Frames 008-012, 047, 165, 193-200), Video zLWVF2nmQDY,
  Fotos 40431489714 (Balken, Zylinder, Fuehrungsplatte), 26271221407 (Traverse, Schild "Frisch"),
  Foto BS (blaue K55 senkrecht von rechts).

Alle Masse Original-mm, X nach hinten, Y nach rechts, Z ab Boden. Die Umbau-Historie steht in referenz/historie/planierschild.md.
"""
from __future__ import annotations

import math
from itertools import pairwise

from build123d import (
    Align,
    Axis,
    Cylinder,
    FontStyle,
    GeomType,
    Part,
    Plane,
    Polygon,
    Pos,
    Rot,
    SlotOverall,
    Sphere,
    Text,
    Vector,
    extrude,
    fillet,
    offset,
)

from .common import (
    ABOCK_FUESSE,
    ABOCK_SCHEITEL,
    DECK_X1,
    DECK_Z,
    X_LEIT,
    Y_SCHUB,
    Z_SCHUB,
    Sammler,
    balken,
    box,
    kasten_rund,
    rad_x,
    rad_y,
    ring_x,
    ring_y,
    schraubenkreis,
    schraubenreihe,
    sechskant,
    stab,
)
from .hydraulik import Rohrzug, durchfuehrungen, hydraulik
from .planiermasse import (
    EK_DY,
    EK_SCHR_DX,
    EK_SCHR_DY,
    EK_T,
    EK_X0,
    EK_X1,
    EK_YI,
    EK_Z0,
    EK_Z1,
    GABEL_L,
    LL_H,
    LL_L,
    QT_X0,
    QT_X1,
    QT_Z0,
    QT_Z1,
    R_KOPF,
    R_STANGE,
    R_ZYL,
    X_BODEN,
    X_KOPF,
    X_ZAPFEN,
    Y_FRISCH,
    Z_AUSS,
    Z_AUSS_O,
    Z_ZYL,
    Z_ZYL_U,
)

Kontur = list[tuple[float, float]]    # Polygonzug (x, z) bzw. (y, z)

# ---------------------------------------------------------------------------------------------------------------
# Parameter
# ---------------------------------------------------------------------------------------------------------------
# --- Schild ---
SCHILD_B, SCHILD_H = 2200.0, 760.0     # Breite 2150..2200 (Fotos 7826381704/39333958410: Balken buendig am Seitenblech)
X_SCHNEIDE = -800.0           # Vorderkante Schneide (Video v.mp4 t=166 und 196/047: Schildfront ~ 800 vor der Maske)
T_BLECH = 16.0                # Schildblech (2 mm im Modell)
T_RIPPE = 16.0                # Endblech
Y_WANGE = SCHILD_B / 2 - T_RIPPE       # Innenseite Endblech
Z_SCHN = 165.0                # Hoehe der Schneidleiste
X_ENDBL = -525.0              # Hinterkante der Endbleche (Video 165: ~ 250 hinter der Lippe)
QT_SZ0, QT_SX1 = 590.0, -560.0         # Quertraeger hinter der Oberkante: Unterkante z, Rueckwand x (Video 165)

# --- Schubrahmen (C-Rahmen hinter dem Schild, Video 008/169-173) ---
Z_RAHMEN = 400.0              # Mitte der Rahmentraeger (= Z_SCHUB)
RA_H, RA_B = 150.0, 110.0     # Kastenprofil Hoehe / Breite
X_RA_SB = -130.0              # Diagonale trifft den Schubbalken innen (vorderes Ende der Spitzplatten, Video 171/173)
X_RA_Q, Y_RA_Q = -555.0, 640.0   # Ecke Diagonale / Quertraeger (Mitte), Quertraeger liegt am Blechruecken an

# --- Schubbalken ---
SB_B, SB_H = 120.0, 170.0     # Video t=164/158: hinterer Balkenteil niedrig (~150..180), vorn hoeher (~230) mit Schraegubergang
SB_Z0, SB_Z1 = Z_SCHUB - SB_H / 2, Z_SCHUB + SB_H / 2       # hinten 315 / 485
SB_XV = 560.0                 # ab hier nach hinten volle Hoehe, davor Verjuengung
SB_H_VORN = 230.0             # Hoehe am vorderen Teil (x < SB_XV - 110)
X_GELENK = 1860.0             # hinteres Gelenk: Video t=164/158, Foto 40431489714: Lagerkappe ~ 390 VOR der Triebradachse
X_SCHILDBOLZEN = -575.0       # Balkenende vorn am Zahnsegment (Video 008/165: Balken endet direkt hinter dem Endblech)
X_STUFE0, X_STUFE1 = -160.0, 260.0      # aufgeschweisste Spitzplatten aussen am Balken (Video 022/165)

# --- A-Bock ---
XA_VORN, XA_HINTEN = ABOCK_FUESSE
XS, ZS = ABOCK_SCHEITEL
A_TIEFE, A_BREITE = 70.0, 110.0        # Kastenstrebe: quer (y); Breite in der Ebene oben 110
A_BREITE_UNTEN = 144.0                 # ... unten 144
AUS_B, AUS_Z0, AUS_Z1 = 290.0, SB_Z1 + 45, SB_Z1 + 265   # dreieckiger Ausschnitt im Stegblech (BS): Basis / Hoehe unten / Spitze

# --- Gelenkbock am hinteren Kettenrahmen (Original-mm) ---
GB_YI, GB_YA = 848.0, 880.0            # Bockplatte innen / aussen (|y|)
GB_Y_RAHMEN = 757.0                    # Arm beginnt am Kettenrahmen (Aussenseite |y| 745 + Flansch)
GB_Y_FLANSCH = 769.0                   # Anschraubflansch aussen (|y|)
GB_Z0, GB_Z1 = 352.0, 455.0            # Arm / Flansch von unten bis oben (zwischen Ober- und Untertrum)
GB_ARM_X0, GB_ARM_X1 = 1832.0, 1864.0  # Arm in x (Flansch zwischen den Deckelschrauben des Kettenrahmens bei x 1797 / 1889)
GB_FL_X0, GB_FL_X1 = 1822.0, 1874.0    # Anschraubflansch in x
GB_FL_SCHR_X = (1828.0, 1868.0)        # Schrauben im Flansch, x
GB_FL_SCHR_Z = (365.0, 442.0)          # Schrauben im Flansch, z
GB_PL_X0, GB_PL_X1 = 1770.0, 1960.0    # Bockplatte in x
GB_PL_Z0_V, GB_PL_Z0_H, GB_PL_Z1 = 335.0, 330.0, 470.0   # Bockplatte Unterkante vorn / hinten, Oberkante
GB_AUGE_R, GB_AUGE_T = 85.0, 32.0      # Auge um das Gelenk: Radius / Dicke
GB_RIPPE_X0, GB_RIPPE_X1 = 1790.0, 1940.0   # Versteifungsrippe oben, x
GB_RIPPE_Y0 = 830.0                    # Rippe von |y| 830 bis GB_YI
GB_RIPPE_Z1 = 480.0                    # Oberkante Rippe
GB_NABE_Y, GB_NABE_R, GB_NABE_T = 900.0, 70.0, 40.0    # Nabe aussen: |y|, Radius, Dicke
GB_BOLZEN_R = 40.0                     # Gelenkbolzen
GB_NIPPEL_DZ = 68.0                    # Schmiernippel ueber der Gelenkachse

# --- Balkenklammer (Schweisslaschen) ---
KL_X = 520.0                           # Klammer um den Balken
KL_T = 14.0                            # halbe Klammerbreite in x und Blechstaerke
KL_QUERSCHOTTE_X = (450.0, 1100.0, 1750.0)   # Querschotte, aussen als Laschen sichtbar

# --- Fuehrungsplatte mit Steckbolzen (kurz hinter dem Leitrad) ---
FP_X0, FP_X1 = X_LEIT + 110.0, X_LEIT + 250.0   # stehende Platte 140 lang (Foto 40431489714), etwa 320 vor dem A-Bock-Fuss
X_STECK = X_LEIT + 280.0

# --- Hubzylinder (Hauptmasse in planiermasse.py) ---
R_ZYLLTG = 11.0              # duenne Zylinderrohre Ø 22 (Kopf -> Endkasten)

# --- Arbeitsscheinwerfer hinten links auf dem Endkasten (Video 145/116/158) ---
SW_XY = (2790.0, -935.0)
SW_R = 75.0

# --- Konsole auf der Kotfluegelkante ---
KONSOLE_X0 = 2712.0           # hinter der Deckschraubenreihe des Rumpfs (x 2698)


# ---------------------------------------------------------------------------------------------------------------
# Helfer
# ---------------------------------------------------------------------------------------------------------------
def _platte_xz(pts: Kontur, y0: float, y1: float) -> Part:
    """Polygon in der XZ-Ebene (Punkte (x, z)), extrudiert von y0 bis y1 (unabhaengig vom Umlaufsinn)."""
    ya, yb = sorted((y0, y1))
    p = extrude(Plane.XZ * Polygon(*pts, align=None), amount=yb - ya)
    return Pos(0, ya - p.bounding_box().min.Y, 0) * p




def _scheibe_z(x: float, y: float, z0: float, r: float, h: float) -> Part:
    """Stehender Zylinder (Achse Z) mit Fuss bei z0."""
    return Pos(x, y, z0) * Cylinder(r, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def _bolzen_y(t: Sammler, x: float, y0: float, y1: float, z: float, r: float, kopf: bool = True) -> None:
    """Gelenkbolzen (blank) laengs Y von y0 nach y1, Kopf bei y0, Scheibe + Splint bei y1."""
    s = 1 if y1 > y0 else -1
    t.mat("blank", stab((x, y0, z), (x, y1, z), r))
    if kopf:
        t.mat("blank", stab((x, y0, z), (x, y0 - s * 14, z), r * 1.45))
    t.mat("blank", stab((x, y1 - s * 22, z), (x, y1 - s * 10, z), r * 1.5))       # Scheibe
    t.mat("schwarz", stab((x, y1 - s * 6, z - r - 4), (x, y1 - s * 6, z + r + 4), 4.5))  # Splint


def _schmiernippel(t: Sammler, x: float, y: float, z: float) -> None:
    """Kegelschmiernippel senkrecht nach oben auf (x, y, z)."""
    t.mat("blank", sechskant((x, y, z), (0, 0, 1), 14, 7))
    t.mat("blank", Pos(x, y, z + 9) * Cylinder(4, 8))
    t.mat("blank", Pos(x, y, z + 15) * Sphere(6))


# ---------------------------------------------------------------------------------------------------------------
# Schild
# ---------------------------------------------------------------------------------------------------------------
def _profil() -> tuple[Kontur, Kontur]:
    """Vorderkontur F und Rueckkontur B des Schildblechs als (x, z)-Listen (unten -> oben).

    Nach Video 165 (senkrecht von rechts, Endblech) und 193-196 (vorn rechts): unten die schraeg nach vorn stehende Schneide,
    tiefste Stelle der Mulde ~ 185 hinter der Schneide auf z ~ 430, oben stark nach vorn ausgerollte Lippe (Oberkante ~ 30 hinter
    der Schneidenspitze). Glatter Zug (Catmull-Rom) durch die Stuetzpunkte."""
    X = X_SCHNEIDE
    S = [(X + 18, 0.0), (X + 58, Z_SCHN), (X + 140, 300.0), (X + 182, 430.0), (X + 172, 560.0), (X + 120, 670.0),
         (X + 30, SCHILD_H - 16)]
    F = [S[0]]
    for i in range(1, len(S)):
        p0, p1, p2, p3 = S[max(i - 2, 0)], S[i - 1], S[i], S[min(i + 1, len(S) - 1)]
        n = 2 if i == 1 else 6
        for k in range(1, n + 1):
            u = k / n
            F.append(tuple(0.5 * (2 * p1[c] + (-p0[c] + p2[c]) * u + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * u * u
                                  + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * u ** 3) for c in (0, 1)))
    B = []
    for i, (x, z) in enumerate(F):
        a = F[max(i - 1, 0)]
        b = F[min(i + 1, len(F) - 1)]
        tx, tz = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, tz)
        nx, nz = tz / L, -tx / L                       # Normale nach hinten
        if nx < 0:
            nx, nz = -nx, -nz
        B.append((x + T_BLECH * nx, z + T_BLECH * nz))
    B[0] = (B[0][0], 0.0)
    return F, B


def _x_auf(P: Kontur, z: float) -> float:
    """x einer Kontur (Liste (x, z), z steigend) auf Hoehe z."""
    for (x0, z0), (x1, z1) in pairwise(P):
        if min(z0, z1) <= z <= max(z0, z1) and abs(z1 - z0) > 1e-9:
            return x0 + (x1 - x0) * (z - z0) / (z1 - z0)
    return P[-1][0] if z > P[-1][1] else P[0][0]


def _zug(B: Kontur, za: float, zb: float, n: int = 8) -> Kontur:
    """Rueckkontur zwischen za und zb als Punktliste."""
    return [(_x_auf(B, za + (zb - za) * i / n), za + (zb - za) * i / n) for i in range(n + 1)]


def _schildblech(t: Sammler, F: Kontur, B: Kontur) -> None:
    """Gewoelbtes Blech (Ruecken lackiert wie der Anbau, Front blank mit eigener 5-mm-Haut, Video 047/165/196) und die flach
    nach hinten umgekantete Oberkante, die den Quertraeger abdeckt."""
    F5 = [(x + (bx - x) * 5.0 / T_BLECH, z + (bz - z) * 5.0 / T_BLECH) for (x, z), (bx, bz) in zip(F, B, strict=True)]
    t.append(_platte_xz(F5 + B[::-1], -Y_WANGE, Y_WANGE))
    t.mat("zink", _platte_xz(F + F5[::-1], -Y_WANGE, Y_WANGE))
    xo = F[-1][0]
    t.append(_platte_xz([(xo - 6, SCHILD_H - 16), (xo - 6, SCHILD_H), (QT_SX1, SCHILD_H), (QT_SX1, SCHILD_H - 14)],
                        -Y_WANGE, Y_WANGE))


def _schneide(t: Sammler) -> None:
    """Eine durchgehende Leiste zwischen den Endblechen, leicht nach vorn gestellt (Video 047/048/196: blank wie das Blech,
    keine abgesetzte Lackleiste; Senkschrauben buendig, nur angedeutet)."""
    t.mat("zink", _platte_xz([(X_SCHNEIDE, 0.0), (X_SCHNEIDE + 19, 0.0), (X_SCHNEIDE + 59, Z_SCHN), (X_SCHNEIDE + 40, Z_SCHN)],
                             -Y_WANGE, Y_WANGE))
    winkel = math.degrees(math.atan2(40.0, Z_SCHN))
    n = 11
    for i in range(n):
        y = -SCHILD_B / 2 + 60 + (SCHILD_B - 120) * (i + 0.5) / n
        t.mat("blank", Pos(X_SCHNEIDE + 20, y, 85) * Rot(0, 90 - winkel, 0) * Cylinder(11, 6))


def _quertraeger_rippen(t: Sammler, B: Kontur) -> None:
    """Waagerechter Quertraeger hinter der Oberkante (Video 165: gewoelbter Blechruecken, oben ein Kastentraeger) und fuenf
    flache Rippen am Blechruecken darunter."""
    qz = _zug(B, QT_SZ0, SCHILD_H - 14, 8)
    t.append(_platte_xz([*qz, (QT_SX1, SCHILD_H - 14), (QT_SX1, QT_SZ0 + 30), (QT_SX1 - 30, QT_SZ0)], -Y_WANGE, Y_WANGE))
    for y in (-760.0, -380.0, 0.0, 380.0, 760.0):
        rp = _zug(B, 120.0, QT_SZ0, 8)
        t.append(_platte_xz(rp + [(x + 30 + 30 * (z - 120.0) / (QT_SZ0 - 120.0), z) for x, z in rp[::-1]], y - 7, y + 7))


def _endbleche(t: Sammler, F: Kontur, B: Kontur) -> None:
    """Endbleche (Video 165 senkrecht von rechts, 193-196): vorn konkav entlang der Blechkruemmung mit spitzer unterer Vorderecke
    an der Schneide, hinten eine gerade senkrechte Kante ~ 250 hinter der Lippe, unten schraeg ansteigend."""
    xo = F[-1][0]
    vorn = [(x - 6, z) for x, z in F]
    vorn[0] = (X_SCHNEIDE - 4, 0.0)
    xr = X_ENDBL
    hinten = [(xr - 30, 70.0), (xr, 125.0), (xr, SCHILD_H - 20), (xr - 20, SCHILD_H + 8), (xo + 20, SCHILD_H + 12)]
    sichel = vorn + hinten[::-1]
    for s in (-1, 1):
        t.append(_platte_xz(sichel, s * Y_WANGE, s * (SCHILD_B / 2)))
        for z in (180.0, 340.0, 500.0, 660.0):           # einzelne Schrauben entlang der Endkante (in den Blechruecken)
            xm = (_x_auf(B, z) + xr) / 2
            t.mat("blank", sechskant((xm, s * SCHILD_B / 2, z), (0, s, 0), 26, 9))


def _balkenanschluss(t: Sammler, B: Kontur) -> None:
    """Anschluss der Schubbalken (Video 008/165/196): innen ein Anschlussbock am Blechruecken vor dem Balkenende, aussen zwischen
    Balken und Endblech das senkrechte Zahnsegment (Neigungsverstellung) mit Zaehnen nach hinten, mittig die Gelenkzunge."""
    for s in (-1, 1):
        y = s * Y_SCHUB
        zs0, zs1 = Z_SCHUB - 175, Z_SCHUB + 175
        t.append(_platte_xz([*_zug(B, Z_SCHUB - 130, Z_SCHUB + 130, 6), (X_SCHILDBOLZEN - 2, Z_SCHUB + 100),
                             (X_SCHILDBOLZEN - 2, Z_SCHUB - 100)], y - 45, y + 45))
        ya, yb = s * (Y_SCHUB + SB_B / 2 + 1), s * (Y_WANGE + 1)
        xz = X_SCHILDBOLZEN + 4                               # Zahngrund
        seg = [*_zug(B, zs0, zs1, 8), (xz, zs1), (xz, Z_SCHUB + 62), (X_SCHILDBOLZEN + 80, Z_SCHUB + 45),
               (X_SCHILDBOLZEN + 80, Z_SCHUB - 45), (xz, Z_SCHUB - 62), (xz, zs0)]
        t.append(_platte_xz(seg, ya, yb))
        for zc in [zs0 + 16 + i * 32 for i in range(4)] + [zs1 - 16 - i * 32 for i in range(4)]:   # Zaehne
            t.append(_platte_xz([(xz - 1, zc - 14), (xz + 22, zc - 6), (xz + 22, zc + 6), (xz - 1, zc + 14)], ya, yb))
        _bolzen_y(t, X_SCHILDBOLZEN + 45, s * (Y_WANGE + 2), s * (Y_SCHUB - SB_B / 2 - 6), Z_SCHUB, 20, kopf=False)
        t.mat("blank", sechskant((X_SCHILDBOLZEN + 45, s * (Y_WANGE + 1), Z_SCHUB), (0, s, 0), 46, 14))
        # Klinke am Balkenende greift in das Segment
        t.append(box(X_SCHILDBOLZEN + 20, X_SCHILDBOLZEN + 85,
                     *sorted((s * (Y_SCHUB + SB_B / 2 - 2), s * (Y_SCHUB + SB_B / 2 + 16))), Z_SCHUB + 70, Z_SCHUB + 120))


def schubrahmen(t: Sammler, B: Kontur) -> None:
    """C-Rahmen hinter dem Schild (Video 008, 169-173): Quertraeger aus Kastenprofil direkt am Blechruecken in Hoehe der
    Schubbalken, an beiden Enden ein Diagonaltraeger schraeg nach hinten-aussen an die Innenseite des Schubbalkens
    (vorderes Ende der Spitzplatten). Haelt den Abstand der Schubbalken und steift das Schild aus; der ganze Rahmen
    liegt vor der Pumpe (x < -440) und bleibt beim Heben um X_GELENK frei."""
    zr0, zr1 = Z_RAHMEN - RA_H / 2, Z_RAHMEN + RA_H / 2
    xq0 = max(_x_auf(B, zr0), _x_auf(B, zr1))
    xq1 = X_RA_Q + RA_B / 2
    # Quertraeger mit Gurtblechen oben/unten (Kastenprofil), Vorderseite folgt dem Blechruecken (6 mm eingesenkt = verschweisst)
    t.append(_platte_xz([(x - 6, z) for x, z in _zug(B, zr0, zr1, 6)] + [(xq1, zr1), (xq1, zr0)],
                        -Y_RA_Q - RA_B / 2, Y_RA_Q + RA_B / 2))
    for z0, z1 in ((zr1 - 1, zr1 + 10), (zr0 - 10, zr0 + 1)):
        t.append(box(xq0 + 20, xq1 + 8, -Y_RA_Q - RA_B / 2 - 8, Y_RA_Q + RA_B / 2 + 8, z0, z1))
    for s in (-1, 1):
        # Diagonale: von der Rahmenecke zur Innenseite des Schubbalkens, Ende schraeg am Balken angeschweisst
        p0 = Vector(X_RA_Q, s * Y_RA_Q, Z_RAHMEN)
        p1 = Vector(X_RA_SB, s * (Y_SCHUB - SB_B / 2 + 30), Z_RAHMEN)
        t.append(balken((p0.X, p0.Y, p0.Z), (p1.X, p1.Y, p1.Z), RA_B, RA_H))
        # Eckknoten oben und unten (dreieckige Knotenbleche) und Anschlussblech am Schubbalken
        d = (p1 - p0).normalized()
        for zz in (zr1 + 1, zr0 - 13):
            kn = [(xq0 - 2, s * (Y_RA_Q - 140)), (xq0 - 2, s * (Y_RA_Q + RA_B / 2 + 10)),
                  (p0.X + d.X * 260, p0.Y + d.Y * 260 + s * 50), (xq1 + 10, s * (Y_RA_Q - 140))]
            if s > 0:
                kn = kn[::-1]                                  # gegen den Uhrzeigersinn -> Extrusion nach +z
            t.append(extrude(Plane.XY.offset(zz) * Polygon(*kn, align=None), amount=12))
        yi = s * (Y_SCHUB - SB_B / 2)
        t.append(box(X_RA_SB - 150, X_RA_SB + 90, *sorted((yi, yi - s * 12)), Z_RAHMEN - 95, Z_RAHMEN + 95))
        t += [sechskant((X_RA_SB + dx, yi - s * 12, Z_RAHMEN + dz), (0, -s, 0), 20, 7) for dx in (-120, 60) for dz in (-65, 65)]


def schild(t: Sammler) -> None:
    """Schild mit Blech, Schneide, Quertraeger, Endblechen, Anschluss der Schubbalken und C-Rahmen."""
    F, B = _profil()
    _schildblech(t, F, B)
    _schneide(t)
    _quertraeger_rippen(t, B)
    _endbleche(t, F, B)
    _balkenanschluss(t, B)
    schubrahmen(t, B)


# ---------------------------------------------------------------------------------------------------------------
# Schubbalken, Gelenkbock, Fuehrungsplatte
# ---------------------------------------------------------------------------------------------------------------
def _sb_h(x: float) -> float:
    """Balkenhoehe bei x: ab SB_XV nach hinten voll (SB_H), davor linear auf SB_H_VORN am vorderen Auge."""
    if x >= SB_XV:
        return SB_H
    return SB_H_VORN + (SB_H - SB_H_VORN) * max(0.0, (x - (SB_XV - 110.0)) / 110.0)


def _sb_top(x: float) -> float:
    return Z_SCHUB + _sb_h(x) / 2


def _sb_bot(x: float) -> float:
    return Z_SCHUB - _sb_h(x) / 2


def _balkenkasten(t: Sammler, s: int) -> None:
    """Kastenprofil: vorn hoeher, Schraegubergang, hinten niedrig und schraeg abgeschnitten (Video 010/022), mit Gurtblechen
    oben/unten und Stirnplatte vor dem Zahnsegment."""
    y = s * Y_SCHUB
    yi, ya = y - SB_B / 2, y + SB_B / 2
    xa = X_SCHILDBOLZEN
    xe_o, xe_u = X_GELENK + 85.0, X_GELENK - 15.0
    xs = [xa, SB_XV - 110.0, SB_XV]
    t.append(_platte_xz([(x, _sb_top(x)) for x in xs] + [(xe_o, _sb_top(xe_o)), (xe_u, _sb_bot(xe_u))]
                        + [(x, _sb_bot(x)) for x in xs[::-1]], yi, ya))
    xg = [X_SCHILDBOLZEN + 40, SB_XV - 110.0, SB_XV]
    t.append(_platte_xz([(x, _sb_top(x)) for x in xg] + [(xe_o - 10, _sb_top(xe_o)), (xe_o - 14, _sb_top(xe_o) - 14)]
                        + [(x, _sb_top(x) - 14) for x in xg[::-1]], yi - 6, ya + 6))
    t.append(_platte_xz([(x, _sb_bot(x)) for x in xg] + [(xe_u - 10, _sb_bot(xe_u)), (xe_u - 6, _sb_bot(xe_u) + 14)]
                        + [(x, _sb_bot(x) + 14) for x in xg[::-1]], yi - 6, ya + 6))
    t.append(box(xa - 4, xa + 12, yi - 6, ya + 6, _sb_bot(xa) - 4, _sb_top(xa) + 4))


def _spitzplatten(t: Sammler, s: int) -> None:
    """Aufgeschweisste Spitzplatten im vorderen Drittel (Video 022/165): aussen zwei Platten mit spitzen Enden uebereinander,
    oben eine Deckplatte mit schraegen Enden -> Stufe im Balken."""
    y = s * Y_SCHUB
    yi, ya = y - SB_B / 2, y + SB_B / 2
    yo = y + s * SB_B / 2
    zm = Z_SCHUB
    for z0, z1 in ((zm + 8, zm + 100), (zm - 100, zm - 8)):
        zc = (z0 + z1) / 2
        t.append(_platte_xz([(X_STUFE0, zc), (X_STUFE0 + 70, z0), (X_STUFE1 - 70, z0), (X_STUFE1, zc), (X_STUFE1 - 70, z1),
                             (X_STUFE0 + 70, z1)], yo - s * 1, yo + s * 16))
    zt = _sb_top(X_STUFE0)
    t.append(_platte_xz([(X_STUFE0 + 20, zt - 1), (X_STUFE1 - 20, zt - 1), (X_STUFE1 - 60, zt + 16), (X_STUFE0 + 60, zt + 16)],
                        yi - 6, ya + 6 + s * 10))


def _lagernabe(t: Sammler, s: int) -> None:
    """Hinten: runde Lagernabe aussen am Balken mit Fettkappe (Video 165: kleine runde Kappe, kein Vierkantblock)."""
    yo = s * Y_SCHUB + s * SB_B / 2
    t.append(rad_y(X_GELENK, yo + s * 12, Z_SCHUB, 72, 24))
    for a in (45, 135, 225, 315):
        w = math.radians(a)
        t.append(sechskant((X_GELENK + 50 * math.cos(w), yo + s * 24, Z_SCHUB + 50 * math.sin(w)), (0, s, 0), 18, 7))
    t.mat("blank", rad_y(X_GELENK, yo + s * 34, Z_SCHUB, 24, 20))                     # Fettkappe
    t.mat("blank", rad_y(X_GELENK, yo + s * 48, Z_SCHUB, 10, 10))


def _balkenklammer(t: Sammler, s: int) -> None:
    """Umlaufende Klammer um den Balken bei x 520 und Querschotte, aussen als Schweisslaschen sichtbar."""
    y = s * Y_SCHUB
    yo = y + s * SB_B / 2
    xk = KL_X
    t.append(box(xk - KL_T, xk + KL_T, y - SB_B / 2 - KL_T, y + SB_B / 2 + KL_T, _sb_bot(xk) - KL_T, _sb_bot(xk)))
    t.append(box(xk - KL_T, xk + KL_T, y - SB_B / 2 - KL_T, y - SB_B / 2, _sb_bot(xk), _sb_top(xk)))
    t.append(box(xk - KL_T, xk + KL_T, y + SB_B / 2, y + SB_B / 2 + KL_T, _sb_bot(xk), _sb_top(xk)))
    t.append(box(xk - KL_T, xk + KL_T, y - SB_B / 2 - KL_T, y + SB_B / 2 + KL_T, _sb_top(xk), _sb_top(xk) + KL_T))
    t += [sechskant((xk, yo + s * 14, _sb_bot(xk) + 40), (0, s, 0), 22, 8),
          sechskant((xk, yo + s * 14, _sb_top(xk) - 40), (0, s, 0), 22, 8)]
    for x in KL_QUERSCHOTTE_X:
        t.append(box(x - 8, x + 8, yo, yo + s * 6, _sb_bot(x) + 14, _sb_top(x) - 14))


def schubbalken(t: Sammler, s: int) -> None:
    """Schubbalken der Seite ``s`` (-1 links, +1 rechts) vom Zahnsegment bis zur Lagernabe am Gelenk."""
    _balkenkasten(t, s)
    _spitzplatten(t, s)
    _lagernabe(t, s)
    _balkenklammer(t, s)


def gelenkbock(t: Sammler, s: int) -> None:
    """Gelenkbock am hinteren Kettenrahmen: Arm durch die Kettenschleife, Bockplatte aussen, Bolzen."""
    yi = s * GB_YI
    ya = s * GB_YA
    # Arm vom Kettenrahmen (Aussenseite y = +-745) durch den Raum zwischen Ober- und Untertrum
    # (Flansch zwischen den Deckelschrauben des Kettenrahmens bei x 1797 / 1889)
    t.append(box(GB_ARM_X0, GB_ARM_X1, s * GB_Y_RAHMEN, ya, GB_Z0, GB_Z1))
    t.append(box(GB_FL_X0, GB_FL_X1, s * GB_Y_RAHMEN, s * GB_Y_FLANSCH, GB_Z0, GB_Z1))      # Anschraubflansch
    t += [sechskant((x, s * GB_Y_FLANSCH, z), (0, s, 0), 10, 6) for x in GB_FL_SCHR_X for z in GB_FL_SCHR_Z]
    # Bockplatte mit Auge
    pl = _platte_xz([(GB_PL_X0, GB_PL_Z0_V), (GB_PL_X1, GB_PL_Z0_H), (GB_PL_X1, GB_PL_Z1), (GB_PL_X0, GB_PL_Z1)], yi, ya)
    pl += Pos(X_GELENK, (yi + ya) / 2, Z_SCHUB) * Rot(90, 0, 0) * Cylinder(GB_AUGE_R, GB_AUGE_T)
    t.append(pl)
    # Versteifungsrippe oben und Nabe
    t.append(box(GB_RIPPE_X0, GB_RIPPE_X1, s * GB_RIPPE_Y0, s * GB_YI, GB_Z1, GB_RIPPE_Z1))
    t.append(rad_y(X_GELENK, s * GB_NABE_Y, Z_SCHUB, GB_NABE_R, GB_NABE_T))
    _bolzen_y(t, X_GELENK, s * GB_RIPPE_Y0, s * (Y_SCHUB + 20), Z_SCHUB, GB_BOLZEN_R)  # endet im Lagerblock des Schubbalkens
    _schmiernippel(t, X_GELENK, s * GB_NABE_Y, Z_SCHUB + GB_NIPPEL_DZ)


def fuehrungsplatte(t: Sammler, s: int) -> None:
    """Fuehrungsplatte (innen am Schubbalken, stehend ~ 240 hoch x 140 lang, 2 Sechskantschrauben oben) und Steckbolzen in einer
    Aufschweisshuelse auf dem Obergurt, kurz hinter der Platte (Foto 40431489714; Lage des Bolzens unsicher)."""
    y = s * Y_SCHUB
    yi = y - s * SB_B / 2                     # Innenseite Schubbalken
    za, zb = _sb_top(FP_X0), _sb_top(FP_X1)
    pts = [(FP_X0, _sb_bot(FP_X0) + 12), (FP_X1, _sb_bot(FP_X1) + 12), (FP_X1, zb + 160), (FP_X1 - 25, zb + 190),
           (FP_X0 + 25, za + 190), (FP_X0, za + 160)]
    t.append(_platte_xz(pts, yi + s * 3, yi - s * 16))
    t += [sechskant((x, yi - s * 16, za + 140), (0, -s, 0), 18, 7) for x in (FP_X0 + 40, FP_X1 - 40)]
    # Steckbolzen: Huelse, Bolzen mit Bund, Ziehring
    zt = _sb_top(X_STECK)
    t.append(_scheibe_z(X_STECK, y, zt - 3, 24, 43))
    t.mat("blank", _scheibe_z(X_STECK, y, zt + 40, 13, 30))
    t.mat("blank", _scheibe_z(X_STECK, y, zt + 70, 20, 10))
    t.mat("blank", ring_y(X_STECK, y, zt + 100, 24, 15, 9))
    # Haltekette des Bolzens (Oese an der Huelse)
    t.append(ring_x(X_STECK, y + s * 26, zt + 20, 10, 5, 6))


# ---------------------------------------------------------------------------------------------------------------
# A-Bock
# ---------------------------------------------------------------------------------------------------------------
def _bein(xf: float, y: float) -> Part:
    """Kastenstrebe von Fuss xf zum Scheitel, nach oben verjuengt (unten 144, oben 110 in der Ebene), 70 tief."""
    F = Vector(xf, 0, SB_Z1 - 20)
    P = Vector(XS, 0, ZS)
    d = (P - F).normalized()
    p = Vector(-d.Z, 0, d.X)
    pts = [(F + p * (A_BREITE_UNTEN / 2)), (F - p * (A_BREITE_UNTEN / 2)), (P - p * (A_BREITE / 2)), (P + p * (A_BREITE / 2))]
    return _platte_xz([(q.X, q.Z) for q in pts], y - A_TIEFE / 2, y + A_TIEFE / 2)


def _stegblech(t: Sammler, y: float) -> None:
    """Stegblech zwischen den Streben mit dreieckigem Ausschnitt unten in der Mitte (BS) und Randleiste um den Ausschnitt
    (Flachstahl, beidseitig 6 mm aufgesetzt)."""
    xm = (XA_VORN + XA_HINTEN) / 2
    aussen = Polygon((XA_VORN + 40, SB_Z1 - 3), (XA_HINTEN - 40, SB_Z1 - 3), (XS, ZS - 70), align=None)
    innen = Polygon((xm - AUS_B / 2, AUS_Z0), (xm + AUS_B / 2, AUS_Z0), (XS, AUS_Z1), align=None)
    innen = fillet(innen.vertices(), 25)
    blech = extrude(Plane.XZ * (aussen - innen), amount=44)
    t.append(Pos(0, y - 22 - blech.bounding_box().min.Y, 0) * blech)
    rand = extrude(Plane.XZ * (offset(innen, 22) - innen), amount=48)
    t.append(Pos(0, y - 24 - rand.bounding_box().min.Y, 0) * rand)


def abock(t: Sammler, s: int) -> None:
    """A-Bock: zwei Kastenstreben (nach oben verjuengt) von ABOCK_FUESSE zum Scheitel, Stegblech mit Dreieckausschnitt,
    flacher Kastenkopf am Scheitel, schraeges Knotenblech vor dem vorderen Fuss auf dem Balken (c_sr_beam)."""
    y = s * Y_SCHUB
    yi, ya = y - A_TIEFE / 2, y + A_TIEFE / 2
    for xf in (XA_VORN, XA_HINTEN):
        t.append(_bein(xf, y))
        t.append(box(xf - 90, xf + 90, y - 55, y + 55, SB_Z1 - 3, SB_Z1 + 16))       # Fussplatte
        t += schraubenreihe((xf - 65, y + s * 55, SB_Z1 + 8), (xf + 65, y + s * 55, SB_Z1 + 8), 2, (0, s, 0), 18, 6)
    # Knotenblech (~ 240 lang) vom vorderen Fuss nach vorn abfallend bis hinter den Steckbolzen, 2 Schrauben
    t.append(_platte_xz([(X_STECK + 40, SB_Z1), (X_STECK + 40, SB_Z1 + 45), (XA_VORN + 90, SB_Z1 + 200), (XA_VORN + 60, SB_Z1)],
                        y - 10, y + 10))
    t += [sechskant((x, y + s * 10, SB_Z1 + 22 + (x - X_STECK - 40) * 0.2), (0, s, 0), 16, 6)
          for x in (X_STECK + 80, X_STECK + 140)]
    _stegblech(t, y)
    # Scheitel: flacher Kastenkopf (~ 180 x 170) mit Lagerauge und Buchse
    t.append(kasten_rund(XS - 110, XS + 70, yi, ya, ZS - 85, ZS + 85, 22, Axis.Y))
    t.append(rad_y(XS, y, ZS, 78, A_TIEFE))
    t.mat("blank", rad_y(XS, y, ZS, 44, A_TIEFE + 6))
    _schmiernippel(t, XS, y, ZS + 85)


# ---------------------------------------------------------------------------------------------------------------
# Hubzylinder
# ---------------------------------------------------------------------------------------------------------------
def _gabelkopf(t: Sammler, s: int) -> None:
    """Gabelkopf an der Kolbenstange mit Kontermutter, Bolzen durch das Scheitelauge."""
    y = s * Y_SCHUB
    z = Z_ZYL
    for yc in (y - 60, y + 40):
        wange = _platte_xz([(XS, z - 60), (XS + 85, z - 45), (XS + 85, z + 45), (XS, z + 60)], yc, yc + 20)
        wange += Pos(XS, yc + 10, z) * Rot(90, 0, 0) * Cylinder(60, 20)
        t.append(wange)
    t.append(box(XS + 75, XS + GABEL_L - 16, y - 60, y + 60, z - 48, z + 48))
    t.mat("schwarz", sechskant((XS + GABEL_L - 16, y, z), (1, 0, 0), 70, 16))     # Kontermutter
    _bolzen_y(t, XS, s * (Y_SCHUB - 70), s * (Y_SCHUB + 75), z, 32)


def _zylinderrohr(t: Sammler, s: int) -> None:
    """Kolbenstange (matt braun-blank, Foto 40431489714), Stopfbuchse, runder Kopf (Video 079..088, 116: nur ~ 1,2 x Rohr-Ø),
    Rohr bis in den Endkasten, Zapfenring mit Querzapfen (lagert in beiden Kastenwaenden) und Bodenflansch."""
    y = s * Y_SCHUB
    z = Z_ZYL
    x0 = XS + GABEL_L - 4
    t.mat("blank", rad_x((x0 + X_KOPF - 30) / 2, y, z, R_STANGE, X_KOPF - 30 - x0))
    t.append(rad_x(X_KOPF - 18, y, z, 34, 36))
    t.mat("schwarz", rad_x(X_KOPF - 40, y, z, 29, 10))           # Abstreifer
    kopf = rad_x(X_KOPF + 30, y, z, R_KOPF, 68)
    kopf = fillet(kopf.edges().filter_by(GeomType.CIRCLE), 12)
    t.append(kopf)
    t += schraubenkreis((X_KOPF - 4, y, z), (-1, 0, 0), R_KOPF - 16, 4, 16, 7, start=45)
    t.append(rad_x((X_KOPF + 60 + X_BODEN) / 2, y, z, R_ZYL, X_BODEN - X_KOPF - 60))      # Zylinderrohr Ø100
    t.append(rad_x(X_ZAPFEN, y, z, R_ZYL + 10, 90))
    t.mat("blank", rad_y(X_ZAPFEN, y, z, 28, 2 * EK_DY - 2 * EK_T + 6))
    # Bodenflansch, Boden mit Schrauben (bleibt im Endkasten hinter dem Langloch der Schraege)
    t.append(rad_x(X_BODEN + 8, y, z, R_ZYL + 14, 16))
    t.append(rad_x(X_BODEN + 31, y, z, R_ZYL + 7, 30))
    t += schraubenkreis((X_BODEN + 46, y, z), (1, 0, 0), 36, 6, 14, 8, start=30)


def _zylinderleitungen(t: Sammler, s: int) -> None:
    """Zwei duenne Rohre: oben (z + 62) ueber die Zylinderlaenge in den Kasten; unten biegt das Rohr am Kopf nach unten ab und
    laeuft tief unter dem Zylinder nach hinten (Video 087, 116) in die Vorderwand des Endkastens. Dazu Sattelschellen."""
    y = s * Y_SCHUB
    z = Z_ZYL
    dz = 62.0
    t.append(box(X_KOPF + 15, X_KOPF + 45, y - 16, y + 16, z + R_KOPF - 8, z + dz + 8))
    Rohrzug(((X_KOPF + 30, y, z + dz), (EK_X0 + 60, y, z + dz)), R_ZYLLTG - 2).einfuegen(t)
    t.append(box(X_KOPF + 5, X_KOPF + 35, y - 16, y + 16, z - R_KOPF - 14, z - R_KOPF + 8))
    t.mat("blank", sechskant((X_KOPF + 20, y, z - R_KOPF - 14), (0, 0, -1), 26, 10))
    z_ab = z - R_KOPF - 20
    # Biegeradius knapp die Haelfte des kurzen senkrechten Stuecks, damit sich die beiden Bogentangenten nicht ueberschneiden
    Rohrzug(((X_KOPF + 20, y, z_ab), (X_KOPF + 20, y, Z_ZYL_U), (EK_X0 - 6, y, Z_ZYL_U)), R_ZYLLTG - 2,
            0.49 * (z_ab - Z_ZYL_U)).einfuegen(t)
    t.mat("blank", sechskant((EK_X0 - 2, y, Z_ZYL_U), (-1, 0, 0), 26, 12))          # Schottverschraubung
    for x in (2110.0, 2200.0):                                    # Sattelschellen
        t.append(box(x - 12, x + 12, y - 16, y + 16, z + R_ZYL - 6, z + dz))
        t.append(box(x - 12, x + 12, y - 16, y + 16, Z_ZYL_U, z - R_ZYL + 6))


def hubzylinder(t: Sammler, s: int) -> None:
    """Hubzylinder in Arbeitsstellung (waagerecht), Gabelkopf am Scheitel, Rohr im Endkasten."""
    _gabelkopf(t, s)
    _zylinderrohr(t, s)
    _zylinderleitungen(t, s)


# ---------------------------------------------------------------------------------------------------------------
# Traverse (Endkaesten + Quertraeger/Oeltank)
# ---------------------------------------------------------------------------------------------------------------
def _schraegen_geometrie(s: int, y: float) -> tuple[Vector, Vector, Vector, Vector]:
    """Endpunkte p1, p2 der Schraegflaeche an der hinteren Aussenecke des Endkastens in der XY-Ebene, ihre Richtung d und die
    Normale n (zeigt zur abgeschnittenen Ecke)."""
    ya = y + s * EK_DY
    p1 = Vector(EK_X1 - EK_SCHR_DX, ya, 0)
    p2 = Vector(EK_X1, ya - s * EK_SCHR_DY, 0)
    d = (p2 - p1).normalized()
    n = Vector(EK_SCHR_DY, s * EK_SCHR_DX, 0).normalized()
    return p1, p2, d, n


def _ecke_prisma(s: int, y: float, grow: float) -> Part:
    """Prisma (z-Extrusion) ueber der hinteren Aussenecke des Endkastens: Region hinter der Schraege
    (Dx = EK_SCHR_DX, Dy = EK_SCHR_DY, links und rechts gleich). grow > 0 verschiebt die Schraegflaeche um grow nach innen
    (fuer den Innenraum)."""
    p1, p2, d, n = _schraegen_geometrie(s, y)
    a, b = p1 - n * grow - d * 60, p2 - n * grow + d * 60
    pts = [(a.X, a.Y), (b.X, b.Y), (b.X + n.X * 200, b.Y + n.Y * 200), (a.X + n.X * 200, a.Y + n.Y * 200)]
    if sum(pts[i][0] * pts[(i + 1) % 4][1] - pts[(i + 1) % 4][0] * pts[i][1] for i in range(4)) < 0:
        pts = pts[::-1]                                              # immer gegen den Uhrzeigersinn (Extrusion nach +z)
    return extrude(Plane.XY.offset(EK_Z0 - 5) * Polygon(*pts, align=None), amount=EK_Z1 - EK_Z0 + 10)


def _langloch_schraege(s: int, y: float) -> Part:
    """Obround-Durchbruch (LL_L x LL_H, Halbkreis-Enden) mittig in der Schraegflaeche der hinteren Aussenecke."""
    p1, p2, d, n = _schraegen_geometrie(s, y)
    m = (p1 + p2) * 0.5
    pl = Plane(origin=(m.X, m.Y, (EK_Z0 + EK_Z1) / 2), x_dir=d, z_dir=n)
    return extrude(pl * SlotOverall(LL_L, LL_H), amount=60, both=True)


def _endkasten_hohlkoerper(t: Sammler, s: int) -> None:
    """Hohler Blechkasten mit abgeschraegter hinterer Aussenecke, Ausschnitt vorn fuer Zylinder und Leitungen (nach oben bis
    fast zur Decke: Schwenkfreiheit beim Heben), Langloch in der Schraege (Video 090/116/145/150/158, Flickr 26271221407),
    Leitungsdurchfuehrungen in der Innenwand (hydraulik.py) und Kantenschutz um den Ausschnitt."""
    y = s * Y_SCHUB
    k = kasten_rund(EK_X0, EK_X1, y - EK_DY, y + EK_DY, EK_Z0, EK_Z1, 14, Axis.Y)
    k -= _ecke_prisma(s, y, 0.0)
    ki = kasten_rund(EK_X0 + EK_T, EK_X1 - EK_T, y - EK_DY + EK_T, y + EK_DY - EK_T, EK_Z0 + EK_T, EK_Z1 - EK_T, 6, Axis.Y)
    ki -= _ecke_prisma(s, y, EK_T)
    k -= ki
    k -= box(EK_X0 - 5, EK_X0 + EK_T + 5, y - R_ZYL - 12, y + R_ZYL + 12, Z_AUSS, Z_AUSS_O)
    k -= _langloch_schraege(s, y)
    for d in durchfuehrungen(s):                                     # Leitungsdurchfuehrungen (hydraulik.py)
        a = Vector(*d.ort)
        n = Vector(*d.achse)
        k -= stab(tuple(a - n * (EK_T + 6) / 2), tuple(a + n * (EK_T + 6) / 2), d.radius)
    t.append(k)
    t.append(box(EK_X0 - 8, EK_X0 + 2, y - R_ZYL - 24, y - R_ZYL - 12, Z_AUSS - 12, Z_AUSS_O))
    t.append(box(EK_X0 - 8, EK_X0 + 2, y + R_ZYL + 12, y + R_ZYL + 24, Z_AUSS - 12, Z_AUSS_O))
    t.append(box(EK_X0 - 8, EK_X0 + 2, y - R_ZYL - 24, y + R_ZYL + 24, Z_AUSS - 12, Z_AUSS))


def _zapfenlager(t: Sammler, s: int) -> None:
    """Zapfenlager: Deckel Ø100 aussen vorn (1-2 Schrauben + Fettloch), Nabe innen, Falzleiste aussen."""
    y = s * Y_SCHUB
    ya = y + s * EK_DY
    t.append(rad_y(X_ZAPFEN, ya + s * 6, Z_ZYL, 50, 14))
    t += [sechskant((X_ZAPFEN + dx, ya + s * 13, Z_ZYL + 26), (0, s, 0), 14, 6) for dx in (-26, 26)]
    t.mat("schwarz", rad_y(X_ZAPFEN, ya + s * 13, Z_ZYL - 14, 7, 4))                # Fettloch
    yi = y - s * EK_DY
    t.append(rad_y(X_ZAPFEN, yi - s * 8, Z_ZYL, 44, 19))
    t.append(box(EK_X0 + 30, EK_X1 - EK_SCHR_DX - 40, ya - s * 3, ya + s * 6, EK_Z0 + 22, EK_Z0 + 34))


def _konsole(t: Sammler, s: int) -> None:
    """Konsole auf der Kotfluegelkante (Randwulst y = +-900), verschraubt."""
    yk0, yk1 = sorted((s * (EK_YI - 28), s * (EK_YI + 3)))
    xk0 = KONSOLE_X0
    t.append(box(xk0, DECK_X1 - 5, yk0, yk1, DECK_Z, EK_Z0 + 3))
    t.append(box(xk0, DECK_X1 - 5, *sorted((s * (EK_YI - 60), s * (EK_YI - 28))), DECK_Z, DECK_Z + 12))
    for x in (xk0 + 22, DECK_X1 - 27):
        t.mat("schwarz", sechskant((x, s * (EK_YI - 44), DECK_Z + 12), (0, 0, 1), 16, 7))


def endkasten(t: Sammler, s: int) -> None:
    """Rechteckiger Endkasten der Seite ``s`` (Blechkasten, hohl) mit abgeschraegter hinterer Aussenecke; der Zylinder ragt vorn
    durch einen Ausschnitt hinein, Konsole unten, Langloch in der Schraege."""
    _endkasten_hohlkoerper(t, s)
    _zapfenlager(t, s)
    _konsole(t, s)


def _oeltank(t: Sammler) -> None:
    """Quertraeger = Oeltank, hinten oben zwischen den Endkaesten (Enden 3 mm in die Kastenwand), mit umlaufendem
    Bodenflansch nach hinten (~ 35 vor, ~ 45 hoch, je 2 Sechskantschrauben, c_links), Reinigungsdeckel vorn und Ablassschraube."""
    qt = kasten_rund(QT_X0, QT_X1, -EK_YI - 3, EK_YI + 3, QT_Z0, QT_Z1, 14, Axis.Y)
    for s in (-1, 1):
        qt -= _ecke_prisma(s, s * Y_SCHUB, 0.0)          # Quertraeger endet buendig an der Schraegflaeche
    t.append(qt)
    yfl = EK_YI - 2        # endet an der Schraege (nichts steht ueber die Schraegflaeche)
    t.append(box(QT_X1 - 2, QT_X1 + 35, -yfl, yfl, QT_Z0, QT_Z0 + 45))
    for yc in (-340.0, 440.0):
        for dy in (-35, 35):
            t.mat("schwarz", sechskant((QT_X1 + 35, yc + dy, QT_Z0 + 22), (1, 0, 0), 22, 8))
    # Reinigungsdeckel vorn mit Schrauben
    t.append(box(QT_X0 - 8, QT_X0 + 2, -380, 380, QT_Z0 + 30, QT_Z1 - 30))
    t += schraubenreihe((QT_X0 - 8, -350, QT_Z1 - 48), (QT_X0 - 8, 350, QT_Z1 - 48), 7, (-1, 0, 0), 14, 6)
    t += schraubenreihe((QT_X0 - 8, -350, QT_Z0 + 48), (QT_X0 - 8, 350, QT_Z0 + 48), 7, (-1, 0, 0), 14, 6)
    # kein Einfuellstutzen (im Video nicht vorhanden, t020/t050); Entlueftung = Rundpfosten in hydraulik.py
    # Ablassschraube unten, hinter der Plattformkante (DECK_X1 2780) frei haengend
    t.mat("schwarz", sechskant((2805, 520, QT_Z0), (0, 0, -1), 30, 14))


def _firmenschild(t: Sammler) -> None:
    """Firmenschild "Frisch": Messing-/Emailleschild (26271221407), 410 x 215 mittig in der
    Rueckwand des Quertraegers."""
    zm = (QT_Z0 + QT_Z1) / 2
    zs0, zs1 = zm - 90, zm + 125
    ys0, ys1 = Y_FRISCH - 205, Y_FRISCH + 205
    t.mat("schild", box(QT_X1, QT_X1 + 6, ys0, ys1, zs0, zs1))
    rahmen = ((ys0, ys1, zs0, zs0 + 12), (ys0, ys1, zs1 - 12, zs1), (ys0, ys0 + 12, zs0, zs1), (ys1 - 12, ys1, zs0, zs1))
    for a, b, c, d in rahmen:
        t.mat("schild", box(QT_X1 + 6, QT_X1 + 10, a, b, c, d))
    try:
        # Blick von hinten: rechts = +y
        pl = Plane(origin=(QT_X1 + 6, Y_FRISCH, (zs0 + zs1) / 2), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
        tx = extrude(pl * Text("Frisch", 95, font_style=FontStyle.BOLD, align=(Align.CENTER, Align.CENTER)), amount=4)
        t.mat("schild", tx)
    except Exception as e:                                          # Schriftart nicht verfuegbar
        print("Frisch-Schrift entfaellt:", e)


def traverse(t: Sammler) -> None:
    """Traverse: beide Endkaesten, Quertraeger/Oeltank und Firmenschild."""
    for s in (-1, 1):
        endkasten(t, s)
    _oeltank(t)
    _firmenschild(t)


# ---------------------------------------------------------------------------------------------------------------
# Arbeitsscheinwerfer hinten links
# ---------------------------------------------------------------------------------------------------------------
def heckscheinwerfer(t: Sammler) -> None:
    """Scheinwerfer Ø ~ 150 auf kurzem Stiel oben auf dem linken Endkasten, Glas nach hinten, Schutzgitter
    (Video 145, 116, 158)."""
    x, y = SW_XY
    z0 = EK_Z1
    t.append(box(x - 40, x + 40, y - 35, y + 35, z0 - 1, z0 + 10))                      # Fussplatte
    t += [sechskant((x + dx, y, z0 + 10), (0, 0, 1), 14, 6) for dx in (-26, 26)]
    t.mat("schwarz", _scheibe_z(x, y, z0 + 10, 12, 50))                                   # Stiel
    zc = z0 + 60 + SW_R
    for dy in (-SW_R - 8, SW_R + 2):                                                     # Buegel seitlich
        t.mat("schwarz", box(x - 12, x + 12, y + dy, y + dy + 6, z0 + 52, zc + 8))
    t.mat("schwarz", box(x - 12, x + 12, y - SW_R - 8, y + SW_R + 8, z0 + 52, z0 + 60))
    t.mat("schwarz", Pos(x, y, zc) * Rot(90, 0, 0) * Cylinder(10, 2 * SW_R + 24))        # Klemmschraube quer
    geh = Pos(x - 20, y, zc) * Rot(0, 90, 0) * Cylinder(SW_R, 70)                         # Gehaeuse (Topf), Glas nach hinten (+x)
    geh = fillet(geh.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.X)[0:1], 22)
    t.mat("schwarz", geh)
    t.mat("chrom", rad_x(x + 19, y, zc, SW_R + 3, 8))                                     # Ring
    t.mat("glas", rad_x(x + 22, y, zc, SW_R - 8, 6))
    for dz in (-35, 0, 35):                                                               # Schutzgitter
        halb = math.sqrt(max(0.0, (SW_R - 6) ** 2 - dz * dz))
        t.mat("schwarz", box(x + 26, x + 32, y - halb, y + halb, zc + dz - 3, zc + dz + 3))
    t.mat("schwarz", box(x + 26, x + 32, y - 3, y + 3, zc - SW_R + 6, zc + SW_R - 6))


# ---------------------------------------------------------------------------------------------------------------
# Fassade
# ---------------------------------------------------------------------------------------------------------------
def planierschild() -> Sammler:
    """Gesamte Planiereinrichtung (Schild, Schubbalken, A-Boecke, Hubzylinder, Traverse, Hydraulik)."""
    t = Sammler("anbau")
    schild(t)
    for s in (-1, 1):
        schubbalken(t, s)
        fuehrungsplatte(t, s)
        gelenkbock(t, s)
        abock(t, s)
        hubzylinder(t, s)
    traverse(t)
    heckscheinwerfer(t)
    hydraulik(t)
    return t
