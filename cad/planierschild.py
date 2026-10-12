"""Planiereinrichtung FRISCH 55 FH2 (Frontschild, 2-Kolben-Hydraulik).

Wirkprinzip (Prospekt K 55 E, Einsatzfoto):
  Je Seite ein Schubbalken (Kastenprofil) aussen neben der Kette, hinten im
  Gelenkbock am Kettenrahmen gelagert (x = X_TRIEB, z = Z_SCHUB), vorn am
  Schild angebolzt und ueber eine Diagonalstrebe abgestuetzt. Auf dem
  Schubbalken sitzt der A-Bock (zwei Kastenstreben + Knotenblech) mit dem
  Lagerauge im Scheitel. Der Hubzylinder liegt mit Mittelzapfen im
  Endkasten der Traverse; seine Kolbenstange greift nach vorn am
  A-Bock-Scheitel an. Einfahren zieht den Scheitel nach hinten -> Schubbalken
  dreht um das hintere Gelenk -> Schild hebt. runde Zahnrad-Oelpumpe vor dem
  Maskensockel (Antrieb von der Kurbelwelle), je Seite eine Leitung nach hinten.
  Steuerventil mit Kugelhebel und Schraegstab hinten auf der Plattform
  rechts der Mitte (x 2475..2605, y 335..485, z 840..990). Hubhoehe 1120 mm ueber / 200 mm unter Fahrebene.

Fotobefund (BS = blaue K55 senkrecht von rechts, BV = von vorn, FL, PK):
  * A-Bock fast symmetrisch: Fuesse ABOCK_FUESSE (920 / 1650) auf dem Schubbalken,
    Scheitel ABOCK_SCHEITEL (1270, 1080); zwei Kastenstreben, Stegblech dazwischen mit
    dreieckigem Ausschnitt unten in der Mitte (BS: x ~1130..1420, ~210 hoch).
    Die fruehere "Asymmetrie" (PK/FL) war Perspektive der Schraegfotos.
  * Hubzylinder waagerecht auf z = TRAVERSE_Z bei y = +-Y_SCHUB; Kopf bei x ~1770,
    Rohr hinten im Endkasten, Kolbenstange nach vorn zum Scheitel.
  * Traverse: zwei rechteckige Endkaesten aussen (x 2395..2830, z 900..1240, um
    y +-975), dazwischen ein Kasten-Quertraeger gleicher Hoehe (zoom_heck_l: Schild
    "Frisch" auf der Rueckwand; zugleich Oeltank, Einfuellstutzen mit roter Kappe oben
    links, Entluefter). Oben auf dem Quertraeger die Querleitung zwischen den Endkaesten,
    darueber das Querrohr des Schutzbuegels (zwei parallele Rohre).
    BS zeigt den runden Deckel auf der Endkasten-Aussenseite bei x ~2520: dort sitzt der
    Mittelzapfen des Hubzylinders (TRAVERSE_X in common.py).
  * Schutzbuegel: Rohrbuegel ueber dem Endkasten (BS: Schlaufe x ~2310..2600, Scheitel
    z ~1400) mit Querrohr ueber der Traverse, dazu eine Rohrschlaufe hinten links (PK).
  * Pumpe: runder Koerper (Ø ~150, x -225..-60) auf einer Frontplatte vor dem Maskensockel (BV, 26271249857,
    40431531504), seitlich je ein Anschluss etwas unter der Achse. JE SEITE NUR EINE LEITUNG (Ø ~36): um die
    Maskenecke, aussen an den Haubenseiten (|y| = Y_LTG) schraeg nach hinten oben (BS: x 0 / z 775 -> x 1050 /
    z 1060), Schellen an Maske, Haube und Schriftband. Rechts = Foerderleitung zum Steuerventil, links = Saugleitung
    aus dem Oeltank (beide Ø 36, wie im Foto); hinter dem Unterbau bei |y| 410 niedrig (z 960) mit Standschellen auf
    der Plattform. Ventil: Rueckleitung in den Tank, zwei Steigleitungen (Schwanenhals) auf die zwei parallelen
    Querrohre ueber der Traverse (z 1370 Stangenseite, z 1440 Kolbenseite/Buegel), die beide Zylinder parallel
    versorgen; die Leitungen laufen verdeckt durch die hohlen Endkaesten zu den Zylinderenden. Das untere duenne Rohr
    am Zylinder (BS, 39334013090) ist als Leckoelleitung des Kopfes gedeutet. Kein Gestaenge an der Haubenseite, kein
    Ventilblock auf der Pumpe (39333958410: linke Haubenseite nur das Rohr). Traverse: Rueckwand durchgehend (Quertraeger buendig mit
    den Endkaesten), Schild "Frisch" links der Mitte, Langloch rechts, Einfuellstutzen Ø ~115 mit roter Kappe
    (26271221407); Querrohre ueber der Traverse bei z 1370 (Leitung) und 1440 (Buegel).
  * Schild glatt (die Bohrungsreihe auf FL gehoert zu einer anderen Maschine).
  * Fuehrungsplatte mit Steckbolzen auf dem Schubbalken kurz hinter dem Leitrad (FL).

Hubkinematik (Arbeitsstellung = Schneide auf dem Boden, Schubbalken waagerecht):
  Gelenk G = (2250, 400), Scheitel S = (1270, 1080), Zapfen Z = (2520, 1080), Schneide P = (-700, 0).
  Schild 1120 hoch: Schubbalken dreht um G um 21,7 Grad -> S' = (1591, 1394), |S'Z| = 981.
  Arbeitsstellung: |SZ| = 1250.   Schild 200 tief: 3,9 Grad -> S'' = (1226, 1012), |S''Z| = 1296.
  -> Hub 1296 - 981 = 315 mm (aus der Arbeitsstellung 269 ein / 46 aus), der Zylinder schwenkt
  um den Mittelzapfen um +18,7 / -3,0 Grad. Kolbenstange frei von 1394 (Gabelkopf) bis 1740.
  Kopf X_KOPF 1770: eingefahren steht der Gabelkopf (124 lang) bei 1591 + 124 = 1715, also
  ~10 mm vor dem Abstreifer. Rohrende im Endkasten X_BODEN 2740 (220 hinter dem Zapfen): bei +18,7 Grad senkt sich der Boden um ~75 und bleibt
  in der Rueckwand frei; oben stoesst das Rohr bei vollem Hub gerade an die Kastendecke
  (= mechanischer Endanschlag). Kolbenstangenlaenge ab Auge 570..1180 moeglich (Kolben im Rohr).

Alle Masse Original-mm, X nach hinten, Y nach rechts, Z ab Boden.
Gezeichnet in Arbeitsstellung (Schneide auf der Fahrebene).
"""
import math
from build123d import *
from .common import (box, stab, rohr_glatt, balken, rad_x, rad_y, ring_x, ring_y, sechskant,
                     schraube, schraubenreihe, schraubenkreis, kasten_rund, Sammler,
                     Y_SCHUB, Z_SCHUB, DECK_X0, DECK_X1, TRAVERSE_X, TRAVERSE_Z, ABOCK_SCHEITEL,
                     ABOCK_FUESSE, X_TRIEB, X_LEIT, DECK_Z, PUMPE, Y_LTG, HAUBE_X1, HAUBE_B,
                     HAUBE_BAND_Z, TANK_X1, MASKE_UK, SCHEINWERFER, SEG_X1)

# ---------------- Parameter ----------------
# Schild
SCHILD_B, SCHILD_H = 2400.0, 850.0
X_SCHNEIDE = -700.0           # Vorderkante Schneide / Lippe
T_BLECH = 16.0                # Schildblech (2 mm im Modell)
T_RIPPE = 16.0
Y_WANGE = SCHILD_B / 2 - T_RIPPE       # Innenseite Seitenwange
X_RUECK = -470.0              # Hinterkante der Rippen
# Schubbalken (Kastenprofil 120 x 170)
SB_B, SB_H = 120.0, 170.0
SB_Z0, SB_Z1 = Z_SCHUB - SB_H / 2, Z_SCHUB + SB_H / 2
X_GELENK = X_TRIEB            # hinteres Gelenk
X_SCHILDBOLZEN = -360.0       # vorderes Gelenk am Schild
# A-Bock
XA_VORN, XA_HINTEN = ABOCK_FUESSE
XS, ZS = ABOCK_SCHEITEL
A_TIEFE, A_BREITE = 70.0, 110.0        # Kastenstrebe: quer (y) x in der Ebene
# dreieckiger Ausschnitt im Stegblech (BS): Basis ueber dem Schubbalken, Spitze unter dem Scheitel
AUS_B, AUS_Z0, AUS_Z1 = 290.0, SB_Z1 + 45, SB_Z1 + 265
# Hubzylinder (Mittelzapfen im Endkasten der Traverse), Rechnung siehe Docstring
X_ZAPFEN, Z_ZYL = TRAVERSE_X, TRAVERSE_Z   # Mittelzapfen bei x 2520 (Foto BS)
R_ZYL, R_STANGE = 65.0, 30.0
X_KOPF = 1770.0               # Zylinderkopf-Flansch (Vorderseite)
X_BODEN = 2740.0              # Zylinderboden-Flansch (im Endkasten)
GABEL_L = 124.0               # Gabelkopf ab Scheitelauge bis Kontermutter
# Traverse: Endkaesten aussen, Quertraeger (Oeltank) hinten oben
EK_X0, EK_X1 = 2395.0, 2830.0
EK_Z0, EK_Z1 = 900.0, 1240.0
Z_AUSS = 960.0               # Unterkante des Kastenausschnitts (Zylinder + Bodenleitung)
EK_DY, EK_T = 95.0, 12.0               # halbe Breite (y), Wandstaerke
EK_YI = Y_SCHUB - EK_DY                # Innenseite Endkasten (880, frei von Werkzeugkasten-Deckel/Scharnier)
QT_X0, QT_X1 = 2630.0, EK_X1           # Quertraeger = Oeltank, Rueckwand buendig mit den Endkaesten (26271221407: durchgehende Rueckwand)
QT_Z0, QT_Z1 = EK_Z0, EK_Z1           # so hoch wie die Endkaesten (zoom_heck_l)
# Schutzbuegel
R_BUEGEL = 16.0               # Ø 32 (BS ~30)
BG_X0, BG_X1, BG_Z = 2340.0, 2600.0, 1440.0
R_QL, Z_QL = 14.0, 1370.0     # Querleitung: unteres der zwei parallelen Querrohre ueber der Traverse (rr_valve)
# Oelpumpe vor dem Maskensockel (runde Zahnradpumpe, Fotos 26271249857 / 40431531504 / 40431489714)
PU_X, PU_Y, PU_Z = PUMPE
PU_R = 75.0                   # Gehaeuse Ø 150 (BS: 140 hoch, vorn: ~160)
PU_PL = 2.4                   # Frontplatte 2,4 mm in den Maskensockel (x = 0) eingesenkt
PU_XV, PU_XH = -225.0, -60.0  # Gehaeuse vorn / hinten (BS: Pumpenkoerper x -60 .. -220)
PU_XPORT, PU_ZPORT = -135.0, PU_Z - 40.0   # Anschluss seitlich, etwas unter der Achse
# Leitungen: je Seite EINE Leitung (Fotos), Ø ~ 36
R_LTG, R_ZYLLTG = 18.0, 11.0
Y_HAUBE = HAUBE_B / 2         # Haubenseite aussen (345)
LTG_VORN = (0.0, 775.0)       # (x, z) Maskenecke: Beginn des Schraegstuecks (Foto BS)
LTG_HINTEN = (HAUBE_X1 - 30.0, 1060.0)   # Ende des Schraegstuecks am Haubenende
Z_LTG = 1085.0                # waagerechter Lauf hinter der Haube: ueber Kastendeckel (1022) und
                              # Spannbuegel-Fluegel (bis 1060) der Kaesten vor dem Sitz (fahrerstand.py)
X_LTG_AUS = 1580.0           # hinter Unterbau, Tank (bis x 1535) und Konsole: hier geht die Leitung nach aussen und herunter
Y_HINT = 410.0                # |y| der Leitungen hinter dem Unterbau (zwischen Sitz |y| <= 250 und Werkzeugkasten |y| >= 580)
Z_HINT = 960.0                # Hoehe dieses Laufs (120 ueber der Plattform, unter den Kastendeckeln)
# Steuerventil (Foto 39334013090, 40431531504): Block hinten auf der Plattform, rechts der Mitte, vor der Traverse
VB_X0, VB_X1 = 2475.0, 2605.0
VB_Y0, VB_Y1 = 335.0, 485.0
VB_Z1 = 990.0                 # Oberkante Block
Y_ARM1, Y_ARM2 = 380.0, 440.0   # y der beiden Steigleitungen ("Schwanenhals") zu den Querrohren
# Fuehrungsplatte mit Steckbolzen (kurz hinter dem Leitrad)
FP_X0, FP_X1 = X_LEIT + 230.0, X_LEIT + 310.0
X_STECK = X_LEIT + 350.0


# ---------------- Helfer ----------------
def platte_xz(pts, y0, y1):
    """Polygon in der XZ-Ebene (Punkte (x, z)), extrudiert von y0 bis y1 (unabhaengig vom Umlaufsinn)."""
    ya, yb = sorted((y0, y1))
    p = extrude(Plane.XZ * Polygon(*pts, align=None), amount=yb - ya)
    return Pos(0, ya - p.bounding_box().min.Y, 0) * p


def platte_yz(pts, x0, x1):
    """Polygon in der YZ-Ebene (Punkte (y, z)), extrudiert von x0 bis x1."""
    xa, xb = sorted((x0, x1))
    p = extrude(Plane.YZ * Polygon(*pts, align=None), amount=xb - xa)
    return Pos(xa - p.bounding_box().min.X, 0, 0) * p


def ring_z(x, y, z, ra, ri, h):
    return (Pos(x, y, z) * Cylinder(ra, h)) - (Pos(x, y, z) * Cylinder(ri, h + 2))


def scheibe_z(x, y, z0, r, h):
    return Pos(x, y, z0) * Cylinder(r, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def bolzen_y(t, x, y0, y1, z, r, kopf=True):
    """Gelenkbolzen (blank) laengs Y von y0 nach y1, Kopf bei y0, Scheibe + Splint bei y1."""
    s = 1 if y1 > y0 else -1
    t.mat("blank", stab((x, y0, z), (x, y1, z), r))
    if kopf:
        t.mat("blank", stab((x, y0, z), (x, y0 - s * 14, z), r * 1.45))
    t.mat("blank", stab((x, y1 - s * 22, z), (x, y1 - s * 10, z), r * 1.5))       # Scheibe
    t.mat("schwarz", stab((x, y1 - s * 6, z - r - 4), (x, y1 - s * 6, z + r + 4), 4.5))  # Splint


def schelle_x(t, x, y, z, r, z_fuss):
    """Rohrschelle um ein Rohr laengs X mit Fuss bis z_fuss (Plattform/Konsole)."""
    t.append(ring_x(x, y, z, r + 10, r - 0.5, 26))
    t.append(box(x - 22, x + 22, y - r - 16, y + r + 16, z_fuss, z - r + 3))
    for dy in (-r - 9, r + 9):
        t.mat("schwarz", sechskant((x, y + dy, z - r + 3), (0, 0, 1), 12, 6))


def schelle_y(t, x, y, z, r, z_fuss):
    t.append(ring_y(x, y, z, r + 10, r - 0.5, 26))
    t.append(box(x - r - 16, x + r + 16, y - 22, y + 22, z_fuss, z - r + 3))


def ring_dir(p, d, ra, ri, b):
    """Ring (Rohrschelle) um die Achse d, mittig in p."""
    p, d = Vector(*p), Vector(*d).normalized()
    pl = Plane(origin=p - d * (b / 2), z_dir=d)
    return extrude(pl * (Circle(ra) - Circle(ri)), amount=b)


def schmiernippel(t, x, y, z):
    """Kegelschmiernippel senkrecht nach oben auf (x, y, z)."""
    t.mat("blank", sechskant((x, y, z), (0, 0, 1), 14, 7))
    t.mat("blank", Pos(x, y, z + 9) * Cylinder(4, 8))
    t.mat("blank", Pos(x, y, z + 15) * Sphere(6))


def nippel(t, p, d, sw=30, l=18):
    """Sechskant-Verschraubung am Leitungsende p, Achse d."""
    t.mat("blank", sechskant(p, d, sw, l))


# ---------------- Schild ----------------
def _profil():
    """Vorderkontur F und Rueckkontur B des Schildblechs als (x, z)-Listen (unten -> oben)."""
    F = [(X_SCHNEIDE + 20, 0.0), (X_SCHNEIDE + 20, 170.0)]
    n = 24
    for i in range(1, n + 1):                          # gewoelbter Teil (Kreisbogen-artig)
        u = i / n
        z = 170 + 600 * u
        F.append((X_SCHNEIDE + 20 + 95 * math.sin(math.pi * u) + 25 * u, z))
    F.append((X_SCHNEIDE - 5, SCHILD_H))               # nach vorn gekantete Lippe
    B = []
    for i, (x, z) in enumerate(F):
        a = F[max(i - 1, 0)]
        b = F[min(i + 1, len(F) - 1)]
        tx, tz = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, tz)
        nx, nz = tz / L, -tx / L                       # Normale nach hinten
        B.append((x + T_BLECH * nx, z + T_BLECH * nz))
    B[0] = (B[0][0], 0.0)
    return F, B


def _x_rueck(B, z):
    """x der Rueckseite des Schildblechs auf Hoehe z."""
    for (x0, z0), (x1, z1) in zip(B, B[1:]):
        if z0 <= z <= z1:
            return x0 + (x1 - x0) * (z - z0) / (z1 - z0)
    return B[-1][0]


def _zug(B, za, zb, n=8):
    """Rueckkontur zwischen za und zb als Punktliste."""
    return [(_x_rueck(B, za + (zb - za) * i / n), za + (zb - za) * i / n) for i in range(n + 1)]


def schild(t):
    F, B = _profil()
    # Schildblech (gewoelbt, Lippe nach vorn gekantet), glatt
    t.append(platte_xz(F + B[::-1], -Y_WANGE, Y_WANGE))
    # Wulst an der Lippe
    xl, zl = F[-1]
    t.append(stab((xl + 6, -Y_WANGE, zl - 6), (xl + 6, Y_WANGE, zl - 6), 12))
    # Seitenwangen
    wange = F + [(X_RUECK - 10, SCHILD_H - 40), (X_RUECK + 30, 140), (X_RUECK - 50, 0)]
    for s in (-1, 1):
        t.append(platte_xz(wange, s * Y_WANGE, s * SCHILD_B / 2))
        t += schraubenreihe((X_RUECK - 40, s * SCHILD_B / 2, 240), (X_RUECK - 40, s * SCHILD_B / 2, 620), 3,
                            (0, s, 0), 22, 8)
    # Rippen auf der Rueckseite
    for y in (0.0, -430.0, 430.0, -860.0, 860.0):
        rippe = _zug(B, 30, 800, 16) + [(X_RUECK, 770), (X_RUECK, 170), (X_RUECK - 70, 30)]
        t.append(platte_xz(rippe, y - T_RIPPE / 2, y + T_RIPPE / 2))
    # Querholme (Kasten unten, Winkel oben)
    t.append(platte_xz(_zug(B, 250, 430) + [(X_RUECK + 20, 430), (X_RUECK + 20, 250)], -Y_WANGE, Y_WANGE))
    t.append(platte_xz(_zug(B, 690, 780) + [(X_RUECK - 15, 780), (X_RUECK - 15, 690)], -Y_WANGE, Y_WANGE))
    # Schweissnahtartige Deckleiste auf dem unteren Holm
    t.append(box(X_RUECK + 20, X_RUECK + 32, -Y_WANGE, Y_WANGE, 262, 418))
    # Schneide (3 Segmente, blank) mit Senkschrauben
    x0 = X_SCHNEIDE
    for ya, yb in ((-900, -302), (-298, 298), (302, 900)):
        t.mat("blank", platte_yz([(ya, 0), (yb, 0), (yb, 165), (ya, 165)], x0, x0 + 20))
        n = 5
        for i in range(n):
            y = ya + (yb - ya) * (i + 0.5) / n
            t.mat("schwarz", rad_x(x0 - 2, y, 85, 14, 4))
    # Eckmesser (dicker, oben angeschraegt)
    for s in (-1, 1):
        pts = [(s * 904, 0), (s * SCHILD_B / 2, 0), (s * SCHILD_B / 2, 240), (s * 1060, 240), (s * 904, 150)]
        t.mat("blank", platte_yz(pts, x0 - 6, x0 + 20))
        for y, z in ((s * 960, 60), (s * 1120, 60), (s * 1120, 170)):
            t.mat("schwarz", rad_x(x0 - 8, y, z, 14, 4))
    # Anschlussboecke fuer die Schubbalken (Gabel aus zwei Blechen)
    for s in (-1, 1):
        for dy in (-72, 52):
            ya = s * Y_SCHUB + dy
            pl = platte_xz(_zug(B, 285, 515) + [(X_SCHILDBOLZEN, 475), (X_SCHILDBOLZEN, 325)], ya, ya + 20)
            pl += Pos(X_SCHILDBOLZEN, ya + 10, Z_SCHUB) * Rot(90, 0, 0) * Cylinder(75, 20)
            t.append(pl)
        bolzen_y(t, X_SCHILDBOLZEN, s * (Y_SCHUB - 72), s * (Y_SCHUB + 92), Z_SCHUB, 32)
        # Laschen fuer die Diagonalstrebe am oberen Holm
        for dy in (-26, 10):
            t.append(box(X_RUECK - 30, X_RUECK + 50, s * 860 + dy, s * 860 + dy + 16, 680, 760))
    return B


def diagonalstrebe(t, s):
    """Rundrohrstrebe vom oberen Schildholm zum Schubbalken (Stabilisierung)."""
    p1 = Vector(X_RUECK + 25, s * 860, 720)
    p2 = Vector(300, s * (Y_SCHUB - 30), SB_Z1 + 45)
    d = (p2 - p1).normalized()
    t.append(stab(p1 + d * 40, p2 - d * 40, 28))
    for p in (p1, p2):
        t.append(stab(p - d * 45 if p is p2 else p, p + d * 45 if p is p1 else p, 22))
        t.append(rad_y(p.X, p.Y, p.Z, 34, 20))
    bolzen_y(t, p1.X, s * 840, s * 882, p1.Z, 16)
    # Lasche auf dem Schubbalken
    t.append(platte_xz([(p2.X - 70, SB_Z1), (p2.X + 70, SB_Z1), (p2.X + 45, p2.Z + 55), (p2.X - 45, p2.Z + 55)],
                       s * (Y_SCHUB - 52), s * (Y_SCHUB - 8)) - rad_y(p2.X, s * (Y_SCHUB - 30), p2.Z, 36, 60))
    bolzen_y(t, p2.X, s * (Y_SCHUB - 60), s * (Y_SCHUB + 5), p2.Z, 16)


# ---------------- Schubbalken, Gelenkbock, A-Bock ----------------
def schubbalken(t, s):
    y = s * Y_SCHUB
    yi, ya = y - SB_B / 2, y + SB_B / 2
    # Kastenprofil mit Gurtblechen
    t.append(box(X_SCHILDBOLZEN + 60, X_GELENK, yi, ya, SB_Z0, SB_Z1))
    t.append(box(X_SCHILDBOLZEN + 120, X_GELENK - 90, yi - 6, ya + 6, SB_Z1 - 14, SB_Z1))   # Obergurt
    t.append(box(X_SCHILDBOLZEN + 120, X_GELENK - 90, yi - 6, ya + 6, SB_Z0, SB_Z0 + 14))   # Untergurt
    # vorderes Auge (geschmiedet, schmaler) mit Uebergang
    t.append(rad_y(X_SCHILDBOLZEN, y, Z_SCHUB, 68, 100))
    t.append(box(X_SCHILDBOLZEN, X_SCHILDBOLZEN + 70, y - 50, y + 50, Z_SCHUB - 68, Z_SCHUB + 68))
    schmiernippel(t, X_SCHILDBOLZEN + 30, y, Z_SCHUB + 66)
    # hinteres Gelenkauge (voll gerundet) mit Buchse
    t.append(rad_y(X_GELENK, y, Z_SCHUB, SB_H / 2, SB_B))
    t.mat("blank", rad_y(X_GELENK, y, Z_SCHUB, 50, SB_B + 8))
    # Querschotte aussen sichtbar als Schweisslaschen
    for x in (450, 1100, 1750):
        t.append(box(x - 8, x + 8, ya, ya + 6, SB_Z0 + 14, SB_Z1 - 14))


def gelenkbock(t, s):
    """Gelenkbock am hinteren Kettenrahmen: Arm durch die Kettenschleife, Bockplatte aussen, Bolzen."""
    yi = s * 848
    ya = s * 880
    # Arm vom Kettenrahmen (Aussenseite y = +-745) durch den Raum zwischen Ober- und Untertrum
    # (Flansch zwischen den Deckelschrauben des Kettenrahmens bei x 1797 / 1889)
    t.append(box(1832, 1864, s * 757, ya, 352, 455))
    t.append(box(1822, 1874, s * 757, s * 769, 352, 455))                       # Anschraubflansch
    t += [sechskant((x, s * 769, z), (0, s, 0), 10, 6) for x in (1828, 1868) for z in (365, 442)]
    # Bockplatte mit Auge
    pl = platte_xz([(1832, 352), (2150, 320), (X_GELENK, 318), (X_GELENK, 482), (2150, 480), (1832, 455)], yi, ya)
    pl += Pos(X_GELENK, (yi + ya) / 2, Z_SCHUB) * Rot(90, 0, 0) * Cylinder(85, 32)
    t.append(pl)
    # Versteifungsrippe oben und Nabe
    t.append(box(1880, 2160, s * 830, s * 848, 455, 480))
    t.append(rad_y(X_GELENK, s * 900, Z_SCHUB, 70, 40))
    bolzen_y(t, X_GELENK, s * 830, s * 1075, Z_SCHUB, 40)
    t.mat("schwarz", sechskant((X_GELENK, s * 1053, Z_SCHUB), (0, s, 0), 80, 22))   # Kronenmutter
    schmiernippel(t, X_GELENK, s * 900, Z_SCHUB + 68)


def fuehrungsplatte(t, s):
    """Fuehrungsplatte (innen am Schubbalken, hochstehend) und Steckbolzen in einer Aufschweisshuelse
    auf dem Obergurt, kurz hinter dem Leitrad (FL)."""
    y = s * Y_SCHUB
    yi = y - s * SB_B / 2                     # Innenseite Schubbalken
    pts = [(FP_X0, SB_Z0 + 12), (FP_X1, SB_Z0 + 12), (FP_X1, SB_Z1 + 160), (FP_X1 - 25, SB_Z1 + 190),
           (FP_X0 + 25, SB_Z1 + 190), (FP_X0, SB_Z1 + 160)]
    t.append(platte_xz(pts, yi + s * 3, yi - s * 16))
    t += [sechskant(((FP_X0 + FP_X1) / 2, yi - s * 16, z), (0, -s, 0), 18, 7) for z in (SB_Z0 + 50, SB_Z1 - 50)]
    # Steckbolzen: Huelse, Bolzen mit Bund, Ziehring
    t.append(scheibe_z(X_STECK, y, SB_Z1 - 3, 24, 43))
    t.mat("blank", scheibe_z(X_STECK, y, SB_Z1 + 40, 13, 30))
    t.mat("blank", scheibe_z(X_STECK, y, SB_Z1 + 70, 20, 10))
    t.mat("blank", ring_y(X_STECK, y, SB_Z1 + 100, 24, 15, 9))
    # Haltekette des Bolzens (Oese an der Huelse)
    t.append(ring_x(X_STECK, y + s * 26, SB_Z1 + 20, 10, 5, 6))


def abock(t, s):
    """A-Bock: zwei Kastenstreben von ABOCK_FUESSE zum Scheitel, Stegblech mit Dreieckausschnitt."""
    y = s * Y_SCHUB
    yi, ya = y - A_TIEFE / 2, y + A_TIEFE / 2
    for xf in (XA_VORN, XA_HINTEN):
        t.append(balken((xf, y, SB_Z1 - 20), (XS, y, ZS), A_TIEFE, A_BREITE))
        t.append(box(xf - 90, xf + 90, y - 55, y + 55, SB_Z1 - 3, SB_Z1 + 16))       # Fussplatte
        t += schraubenreihe((xf - 65, y + s * 55, SB_Z1 + 8), (xf + 65, y + s * 55, SB_Z1 + 8), 2, (0, s, 0), 18, 6)
    # Stegblech zwischen den Streben mit dreieckigem Ausschnitt unten in der Mitte (BS)
    xm = (XA_VORN + XA_HINTEN) / 2
    aussen = Polygon((XA_VORN + 40, SB_Z1 - 3), (XA_HINTEN - 40, SB_Z1 - 3), (XS, ZS - 70), align=None)
    innen = Polygon((xm - AUS_B / 2, AUS_Z0), (xm + AUS_B / 2, AUS_Z0), (XS, AUS_Z1), align=None)
    innen = fillet(innen.vertices(), 25)
    blech = extrude(Plane.XZ * (aussen - innen), amount=20)
    t.append(Pos(0, y - 10 - blech.bounding_box().min.Y, 0) * blech)
    # Randleiste um den Ausschnitt (Flachstahl, beidseitig 6 mm aufgesetzt)
    rand = extrude(Plane.XZ * (offset(innen, 22) - innen), amount=32)
    t.append(Pos(0, y - 16 - rand.bounding_box().min.Y, 0) * rand)
    # Scheitel: Lagerauge mit Buchse
    t.append(rad_y(XS, y, ZS, 78, A_TIEFE))
    t.append(box(XS - 60, XS + 60, yi, ya, ZS - 120, ZS - 40))
    t.mat("blank", rad_y(XS, y, ZS, 44, A_TIEFE + 6))
    schmiernippel(t, XS, y, ZS + 76)


# ---------------- Hubzylinder ----------------
def hubzylinder(t, s):
    """Hubzylinder in Arbeitsstellung (waagerecht), Gabelkopf am Scheitel, Rohr im Endkasten."""
    y = s * Y_SCHUB
    z = Z_ZYL
    # Gabelkopf an der Kolbenstange, Bolzen durch das Scheitelauge
    for yc in (y - 60, y + 40):
        wange = platte_xz([(XS, z - 60), (XS + 85, z - 45), (XS + 85, z + 45), (XS, z + 60)], yc, yc + 20)
        wange += Pos(XS, yc + 10, z) * Rot(90, 0, 0) * Cylinder(60, 20)
        t.append(wange)
    t.append(box(XS + 75, XS + GABEL_L - 16, y - 60, y + 60, z - 48, z + 48))
    t.mat("schwarz", sechskant((XS + GABEL_L - 16, y, z), (1, 0, 0), 70, 16))     # Kontermutter
    bolzen_y(t, XS, s * (Y_SCHUB - 70), s * (Y_SCHUB + 75), z, 32)
    # Kolbenstange (chrom)
    x0 = XS + GABEL_L - 4
    t.mat("chrom", rad_x((x0 + X_KOPF - 30) / 2, y, z, R_STANGE, X_KOPF - 30 - x0))
    # Stopfbuchse, Kopfflansch mit Schrauben, Kopfstueck
    t.append(rad_x(X_KOPF - 18, y, z, 48, 36))
    t.mat("schwarz", rad_x(X_KOPF - 40, y, z, 38, 10))           # Abstreifer
    t.append(rad_x(X_KOPF + 15, y, z, 88, 30))
    t += schraubenkreis((X_KOPF, y, z), (-1, 0, 0), 74, 8, 18, 9, start=22.5)
    t.append(rad_x(X_KOPF + 55, y, z, R_ZYL + 12, 52))
    # Zylinderrohr bis in den Endkasten
    t.append(rad_x((X_KOPF + 78 + X_BODEN) / 2, y, z, R_ZYL, X_BODEN - X_KOPF - 78))
    # Zapfenring mit Querzapfen (lagert in beiden Kastenwaenden)
    t.append(rad_x(X_ZAPFEN, y, z, R_ZYL + 10, 90))
    t.mat("blank", rad_y(X_ZAPFEN, y, z, 34, 2 * EK_DY - 2 * EK_T + 6))
    # Bodenflansch, Boden mit Schrauben
    t.append(rad_x(X_BODEN + 8, y, z, 80, 16))
    t.append(rad_x(X_BODEN + 31, y, z, 72, 30))
    t += schraubenkreis((X_BODEN + 46, y, z), (1, 0, 0), 50, 6, 16, 8, start=30)
    # Anschluss Ringseite oben am Kopfstueck, Rohr auf dem Zylinder in den Endkasten (Foto BS)
    zr = z + R_ZYL + 30
    t.append(box(X_KOPF + 40, X_KOPF + 76, y - 20, y + 20, z + R_ZYL, z + R_ZYL + 16))
    t.append(rohr_glatt([(X_KOPF + 58, y, z + R_ZYL + 4), (X_KOPF + 58, y, zr), (EK_X0 + 60, y, zr)], R_ZYLLTG - 2, 22))
    for x in (2050.0, 2300.0):                                    # Sattelschellen
        t.append(box(x - 12, x + 12, y - 16, y + 16, z + R_ZYL - 6, zr))
    # Anschluss Bodenseite unten am Kopfstueck, spiegelbildlich: Rohr unter dem Zylinder in den Endkasten (Foto BS)
    zu = z - R_ZYL - 30
    t.append(box(X_KOPF + 40, X_KOPF + 76, y - 20, y + 20, z - R_ZYL - 16, z - R_ZYL))
    t.append(rohr_glatt([(X_KOPF + 58, y, z - R_ZYL - 4), (X_KOPF + 58, y, zu), (EK_X0 + 60, y, zu)], R_ZYLLTG - 2, 22))
    for x in (2050.0, 2300.0):
        t.append(box(x - 12, x + 12, y - 16, y + 16, zu, z - R_ZYL + 6))


# ---------------- Traverse (Endkaesten + Quertraeger/Oeltank) ----------------
def endkasten(t, s):
    """Rechteckiger Endkasten (Blechkasten, hohl), Zylinder ragt vorn durch einen Ausschnitt hinein."""
    y = s * Y_SCHUB
    k = kasten_rund(EK_X0, EK_X1, y - EK_DY, y + EK_DY, EK_Z0, EK_Z1, 18, Axis.Y)
    k -= kasten_rund(EK_X0 + EK_T, EK_X1 - EK_T, y - EK_DY + EK_T, y + EK_DY - EK_T,
                     EK_Z0 + EK_T, EK_Z1 - EK_T, 6, Axis.Y)
    # Ausschnitt vorn fuer Zylinder und Leitung (nach oben bis zur Decke: Schwenkfreiheit beim Heben)
    k -= box(EK_X0 - 5, EK_X0 + EK_T + 5, y - R_ZYL - 12, y + R_ZYL + 12, Z_AUSS, EK_Z1 - EK_T - 2)
    t.append(k)
    # Kantenschutz um den Ausschnitt
    t.append(box(EK_X0 - 8, EK_X0 + 2, y - R_ZYL - 24, y - R_ZYL - 12, Z_AUSS - 12, EK_Z1 - 14))
    t.append(box(EK_X0 - 8, EK_X0 + 2, y + R_ZYL + 12, y + R_ZYL + 24, Z_AUSS - 12, EK_Z1 - 14))
    t.append(box(EK_X0 - 8, EK_X0 + 2, y - R_ZYL - 24, y + R_ZYL + 24, Z_AUSS - 12, Z_AUSS))
    # Zapfenlager: Deckel aussen mit Schrauben, Nabe innen
    ya = y + s * EK_DY
    t.append(rad_y(X_ZAPFEN, ya + s * 8, Z_ZYL, 58, 19))
    t += schraubenkreis((X_ZAPFEN, ya + s * 17, Z_ZYL), (0, s, 0), 42, 6, 14, 7, start=30)
    yi = y - s * EK_DY
    t.append(rad_y(X_ZAPFEN, yi - s * 8, Z_ZYL, 52, 19))
    schmiernippel(t, X_ZAPFEN, ya + s * 8, Z_ZYL + 56)
    # Schweissnaht-/Falzleisten aussen
    t.append(box(EK_X0 + 30, EK_X1 - 30, ya - s * 3, ya + s * 6, EK_Z0 + 22, EK_Z0 + 34))
    # Konsole auf der Kotfluegelkante (Randwulst y = +-900), verschraubt
    yk0, yk1 = sorted((s * (EK_YI - 28), s * (EK_YI + 3)))
    t.append(box(QT_X0 + 10, DECK_X1 - 5, yk0, yk1, DECK_Z, EK_Z0 + 3))
    t.append(box(QT_X0 + 10, DECK_X1 - 5, *sorted((s * (EK_YI - 60), s * (EK_YI - 28))), DECK_Z, DECK_Z + 12))
    for x in (QT_X0 + 40, DECK_X1 - 35):
        t.mat("schwarz", sechskant((x, s * (EK_YI - 44), DECK_Z + 12), (0, 0, 1), 16, 7))


def traverse(t):
    for s in (-1, 1):
        endkasten(t, s)
    # Quertraeger = Oeltank, hinten oben zwischen den Endkaesten (Enden 3 mm in die Kastenwand)
    qt = kasten_rund(QT_X0, QT_X1, -EK_YI - 3, EK_YI + 3, QT_Z0, QT_Z1, 20, Axis.Y)
    # Langloch (Griffoeffnung) in der Rueckwand rechts (26271221407: ovale Vertiefung ~240 x 125 bei y ~ +620)
    qt -= kasten_rund(QT_X1 - 14, QT_X1 + 2, 620 - 120, 620 + 120, 1010, 1134, 60, Axis.X)
    t.append(qt)
    # Firmenschild "Frisch" auf der Rueckwand links der Mitte (26271221407)
    t.mat("schwarz", box(QT_X1, QT_X1 + 8, -570, -130, 995, 1185))
    t.mat("blank", box(QT_X1 + 8, QT_X1 + 14, -570, -130, 995, 1005))
    t.mat("blank", box(QT_X1 + 8, QT_X1 + 14, -570, -130, 1175, 1185))
    t.mat("blank", box(QT_X1 + 8, QT_X1 + 14, -570, -560, 995, 1185))
    t.mat("blank", box(QT_X1 + 8, QT_X1 + 14, -140, -130, 995, 1185))
    try:
        pl = Plane(origin=(QT_X1 + 8, -350, 1090), x_dir=(0, 1, 0), z_dir=(1, 0, 0))   # Blick von hinten: rechts = +y
        tx = extrude(pl * Text("Frisch", 140, font_style=FontStyle.BOLD, align=(Align.CENTER, Align.CENTER)), amount=6)
        t.mat("blank", tx)
    except Exception as e:                                          # Schriftart nicht verfuegbar
        print("Frisch-Schrift entfaellt:", e)
    # Reinigungsdeckel vorn mit Schrauben
    t.append(box(QT_X0 - 8, QT_X0 + 2, -380, 380, QT_Z0 + 30, QT_Z1 - 30))
    t += schraubenreihe((QT_X0 - 8, -350, QT_Z1 - 48), (QT_X0 - 8, 350, QT_Z1 - 48), 7, (-1, 0, 0), 14, 6)
    t += schraubenreihe((QT_X0 - 8, -350, QT_Z0 + 48), (QT_X0 - 8, 350, QT_Z0 + 48), 7, (-1, 0, 0), 14, 6)
    # Einfuellstutzen links (26271221407): Ø ~115, ~110 hoch, rote Kappe; Entluefter/Peilstab sind nicht zu sehen
    xe = 2740.0
    t.append(scheibe_z(xe, -300, QT_Z1 - 2, 55, 112))
    t.mat("ruecklicht", scheibe_z(xe, -300, QT_Z1 + 108, 60, 18))                # rote Kappe
    # Ablassschraube unten
    t.mat("schwarz", sechskant((2720, 520, QT_Z0), (0, 0, -1), 30, 14))


# ---------------- Schutzbuegel ----------------
def schutzbuegel(t):
    """Rohrbuegel ueber den Endkaesten mit Querrohr ueber der Traverse (BS, PK, FL) und
    Rohrschlaufe hinten links am Endkasten (PK)."""
    yb = Y_SCHUB - 55
    for s in (-1, 1):
        y = s * yb
        t.append(rohr_glatt([(BG_X1, y, EK_Z1 - 3), (BG_X1, y, BG_Z), (BG_X0, y, BG_Z),
                             (EK_X0 + 30, y, EK_Z1 - 3)], R_BUEGEL, 70))
        for x in (BG_X1, EK_X0 + 30):                                # Fussplatten
            t.append(box(x - 40, x + 40, y - 36, y + 36, EK_Z1 - 3, EK_Z1 + 10))
    t.append(stab((BG_X1, -yb, BG_Z), (BG_X1, yb, BG_Z), R_BUEGEL))
    # Rohrschlaufe hinten links
    y0, y1 = -(Y_SCHUB + 60), -(Y_SCHUB - 60)
    z = 1150.0
    t.append(rohr_glatt([(EK_X1 - 3, y0, z), (EK_X1 + 140, y0, z), (EK_X1 + 140, y1, z), (EK_X1 - 3, y1, z)],
                        R_BUEGEL - 2, 50))
    for yy in (y0, y1):
        t.append(box(EK_X1 - 3, EK_X1 + 12, yy - 30, yy + 30, z - 30, z + 30))


# ---------------- Oelpumpe ----------------
def oelpumpe(t):
    """Runde Zahnradpumpe vor dem Maskensockel auf einer Frontplatte (Fotos 26271249857, 40431531504, BS):
    Gehaeuse Ø 150 mit Frontdeckel, hinten Kupplungsglocke zum Sockel (Antrieb von der Kurbelwelle),
    je Seite ein Anschlussflansch mit EINER Leitung. Kein Ventilblock/Hebel auf der Pumpe (nicht zu sehen)."""
    xm = (PU_XV + PU_XH) / 2
    t.append(rad_x(xm, 0, PU_Z, PU_R, PU_XH - PU_XV))
    t.append(rad_x(PU_XV - 6, 0, PU_Z, PU_R - 7, 14))                       # Frontdeckel
    t += schraubenkreis((PU_XV - 13, 0, PU_Z), (-1, 0, 0), 56, 6, 14, 7, start=30)
    t.mat("blank", rad_x(PU_XV - 18, 0, PU_Z, 22, 10))                      # Wellenende/Staufferdeckel
    t.append(rad_x(PU_XH + 6, 0, PU_Z, PU_R + 6, 12))                       # Flansch zur Glocke
    t.append(rad_x((PU_XH + 6 - 14) / 2, 0, PU_Z, 52, -14 - (PU_XH + 6)))  # Kupplungsglocke
    # Frontplatte am Maskensockel
    t.append(box(-14, PU_PL, -140, 140, MASKE_UK + 2, MASKE_UK + 162))
    for dy in (-118, 118):
        for z in (MASKE_UK + 22, MASKE_UK + 142):
            t.mat("schwarz", sechskant((-14, dy, z), (-1, 0, 0), 16, 7))
    # Leitungsanschluesse seitlich (unter der Achse)
    for s in (-1, 1):
        t.append(stab((PU_XPORT, s * 50, PU_ZPORT), (PU_XPORT, s * 98, PU_ZPORT), R_LTG + 12))
        t.append(rad_y(PU_XPORT, s * 98, PU_ZPORT, R_LTG + 16, 12))
        t += [sechskant((PU_XPORT + dx, s * 104, PU_ZPORT), (0, s, 0), 12, 6) for dx in (-R_LTG - 7, R_LTG + 7)]


# ---------------- Hydraulikleitungen ----------------
def _z_haube(x):
    """z der Leitung auf dem Schraegstueck an der Haubenseite."""
    (xa, za), (xb, zb) = LTG_VORN, LTG_HINTEN
    return za + (x - xa) * (zb - za) / (xb - xa)


def _schelle_haube(t, x, s, r):
    """Rohrschelle um die Leitung an der Maske/Haubenseite mit Lasche zur Wand.
    Hinter dem Seitensegment (x > SEG_X1) ist die Haube unten offen: dort haengt die Schelle am Schriftband."""
    (xa, za), (xb, zb) = LTG_VORN, LTG_HINTEN
    d = (xb - xa, 0, zb - za)
    z = _z_haube(x)
    y = s * Y_LTG
    t.append(ring_dir((x, y, z), d, r + 8, r - 0.5, 26))
    yw = 355.0 if x < 210 else Y_HAUBE                       # Maskenseite / Haubenseite aussen
    ya, yb = sorted((s * (yw - 2.4), s * (Y_LTG - r + 4)))
    if x < SEG_X1:
        t.append(box(x - 15, x + 15, ya, yb, z - 16, z + 16))
        t.mat("schwarz", sechskant((x, s * (Y_LTG - r + 4), z), (0, s, 0), 12, 5))
    else:
        t.append(box(x - 15, x + 15, ya, yb, z + r - 2, HAUBE_BAND_Z + 45))
        t.mat("schwarz", sechskant((x, s * (Y_LTG - r + 4), HAUBE_BAND_Z + 25), (0, s, 0), 12, 5))


def ventil(t):
    """Steuerventil (Fotos 39334013090, 40431531504, 26271221407): Block hinten auf der Plattform rechts der Mitte
    vor der Traverse, mit Kugelhebel und Schraegstab. Steht auf der Plattform (z 840, 0,3 mm eingesenkt)."""
    zb = DECK_Z - 0.3
    xm, ym = (VB_X0 + VB_X1) / 2, (VB_Y0 + VB_Y1) / 2
    t.append(box(VB_X0 - 10, VB_X1 + 10, VB_Y0 - 10, VB_Y1 + 10, zb, zb + 12))                 # Fussplatte
    t += [sechskant((x, y, zb + 12), (0, 0, 1), 16, 7) for x in (VB_X0, VB_X1) for y in (VB_Y0 - 3, VB_Y1 + 3)]
    t.append(kasten_rund(VB_X0 + 8, VB_X1 - 8, VB_Y0 + 8, VB_Y1 - 8, zb + 12, VB_Z1, 8, Axis.Z))   # Ventilkoerper
    for yy in (VB_Y0 + 8, VB_Y1 - 8):                                                          # Schieberdeckel quer
        t.append(rad_y(xm, yy + (-14 if yy < ym else 14) / 2, zb + 78, 34, 14))
    t.append(rad_x(xm, ym, zb + 78, 22, VB_X1 - VB_X0 + 30))                                  # Schieberbohrungen / Anschlussbalken
    for z in (zb + 112, zb + 144):
        t.append(rad_x(xm, ym, z, 16, VB_X1 - VB_X0 + 14))
    # Kugelhebel (Schaltstock) und Schraegstab
    t.mat("blank", stab((xm - 30, ym, VB_Z1 - 4), (xm - 30, ym, VB_Z1 + 150), 8))
    t.mat("schwarz", Pos(xm - 30, ym, VB_Z1 + 166) * Sphere(24))
    t.append(Pos(xm - 30, ym, VB_Z1 + 6) * Cylinder(20, 14))
    t.mat("blank", stab((VB_X0 + 25, VB_Y0 + 10, VB_Z1 - 20), (VB_X0 - 40, VB_Y0 + 10, VB_Z1 + 150), 7))
    t.append(rad_y(VB_X0 + 25, VB_Y0 + 6, VB_Z1 - 20, 15, 16))
    # Steigleitungen (Schwanenhaelse): Leitung 1 (Stangenseite) auf das Querrohr z Z_QL, Leitung 2 (Kolbenseite) auf das Buegelrohr
    xq, xb = 2655.0, BG_X1
    t.append(rohr_glatt([(xm + 30, Y_ARM1, VB_Z1 - 20), (xm + 30, Y_ARM1, Z_QL), (xq, Y_ARM1, Z_QL)], R_QL, 40))
    t.append(rohr_glatt([(xb, Y_ARM2, VB_Z1 - 20), (xb, Y_ARM2, BG_Z)], R_QL, 40))
    for (x, y, z) in ((xq, Y_ARM1, Z_QL), (xb, Y_ARM2, BG_Z)):                                  # Abzweig-Verschraubung
        t.mat("blank", sechskant((x, y, z - 28), (0, 0, 1), 24, 10))
    # Ruecklauf in den Oeltank (Querträger-Vorderwand)
    t.append(rohr_glatt([(VB_X1 - 20, ym, zb + 112), (QT_X0 + 4, ym, zb + 112)], R_QL, 20))
    t.append(rad_x(VB_X1 + 2, ym, zb + 112, 22, 12))


def leitungen(t):
    """Hydraulikkreis (Fotos 26271249857, 40431531504, 39333958410, BS, 39334013090, 26271221407; Verdecktes plausibel):
      * Pumpe -> je Seite EINE dicke Leitung (Ø 36) um die Maskenecke und schraeg an der Haubenseite nach hinten.
        Rechts: Foerderleitung zum Steuerventil; links: Saugleitung aus dem Oeltank (gleicher Durchmesser, wie im Foto).
        Hinter dem Unterbau laufen beide bei |y| = Y_HINT niedrig (Z_HINT) zum Ventil bzw. in den Tank.
      * Ventil -> Ruecklauf (kurz) in den Tank; zwei Steigleitungen auf die zwei parallelen Querrohre ueber der Traverse
        (Stangenseite z Z_QL, Kolbenseite im Buegelrohr z BG_Z). Beide Querrohre verbinden die Zylinder parallel.
      * Stangenseite je Zylinder: duenne Leitung oben vom Kopfstueck in den Endkasten (hohl, dort verdeckt hoch zum
        Querrohr). Kolbenseite: Buegelschlaufe ueber dem Endkasten in den Kasten (Boden, verdeckt).
        Das untere duenne Rohr am Zylinder (Foto) ist die Leckoelleitung des Kopfes zum Tank."""
    for s in (-1, 1):
        x_end = VB_X0 + 2 if s == 1 else QT_X0 + 4
        pts = [(PU_XPORT, s * 104, PU_ZPORT), (PU_XPORT, s * 300, PU_ZPORT), (-35.0, s * Y_LTG, 560.0),
               (LTG_VORN[0], s * Y_LTG, LTG_VORN[1]), (LTG_HINTEN[0], s * Y_LTG, LTG_HINTEN[1]),
               (LTG_HINTEN[0] + 120, s * Y_LTG, Z_LTG), (X_LTG_AUS, s * Y_LTG, Z_LTG),
               (X_LTG_AUS + 100, s * Y_HINT, Z_LTG - 60), (X_LTG_AUS + 200, s * Y_HINT, Z_HINT),
               (x_end, s * Y_HINT, Z_HINT)]
        t.append(rohr_glatt(pts, R_LTG, 70))
        for x in (100.0, 290.0, 980.0):
            _schelle_haube(t, x, s, R_LTG)
        for x in (1850.0, 2150.0, 2350.0):                               # Standschellen auf der Plattform
            schelle_x(t, x, s * Y_HINT, Z_HINT, R_LTG, DECK_Z - 0.3)
        t.append(rad_x(x_end - s * 0 + (-6 if s == 1 else 6), s * Y_HINT, Z_HINT, R_LTG + 8, 12))   # Verschraubung am Ende
    # Querleitung (Stangenseite, gemeinsam fuer beide Zylinder) oben auf dem Traversen-Quertraeger
    xa = 2655.0
    ye = EK_YI + 60
    t.append(rohr_glatt([(xa, -ye, EK_Z1 - 3), (xa, -ye, Z_QL), (xa, ye, Z_QL), (xa, ye, EK_Z1 - 3)], R_QL, 30))
    for y in (-ye, ye):                                                  # Verschraubungen auf der Decke
        t.mat("blank", sechskant((xa, y, EK_Z1), (0, 0, 1), 30, 14))
    # Doppelschellen halten beide Querrohre (Querleitung z Z_QL, Buegelrohr z BG_Z) auf dem Quertraeger
    for y in (-700, -350, 560, 700):
        t.append(box(xa - 12, xa + 12, y - 14, y + 14, QT_Z1 - 2, Z_QL - R_QL + 2))
        t.append(box(BG_X1 - 10, xa + 12, y - 8, y + 8, Z_QL - R_QL, BG_Z + R_BUEGEL))


# ---------------- Gesamt ----------------
def planierschild():
    t = Sammler("anbau")
    schild(t)
    for s in (-1, 1):
        schubbalken(t, s)
        fuehrungsplatte(t, s)
        gelenkbock(t, s)
        abock(t, s)
        diagonalstrebe(t, s)
        hubzylinder(t, s)
    traverse(t)
    schutzbuegel(t)
    oelpumpe(t)
    ventil(t)
    leitungen(t)
    return t
