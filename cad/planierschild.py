"""Planiereinrichtung FRISCH 55 FH2 (Frontschild, 2-Kolben-Hydraulik).

Wirkprinzip (Prospekt K 55 E, Einsatzfoto):
  Je Seite ein Schubbalken (Kastenprofil) aussen neben der Kette, hinten im
  Gelenkbock am Kettenrahmen gelagert (x = X_GELENK = 1860, z = Z_SCHUB), vorn am
  Schild angebolzt und ueber eine Diagonalstrebe abgestuetzt. Auf dem
  Schubbalken sitzt der A-Bock (zwei Kastenstreben + Knotenblech) mit dem
  Lagerauge im Scheitel. Der Hubzylinder liegt mit Mittelzapfen im
  Endkasten der Traverse; seine Kolbenstange greift nach vorn am
  A-Bock-Scheitel an. Einfahren zieht den Scheitel nach hinten -> Schubbalken
  dreht um das hintere Gelenk -> Schild hebt. runde Zahnrad-Oelpumpe vor dem
  Maskensockel (Antrieb von der Kurbelwelle), je Seite eine Leitung nach hinten.
  Steuerblock mit kleiner Kugel + Schraeghebel vorn auf dem rechten Endkasten (Foto 40431489714).
  Hubhoehe 1120 mm ueber / 200 mm unter Fahrebene.
  Video-Umbau 2026-10: Gelenk x 1860 (vorher 2250), Schildlippe -800 (vorher -700), Balken hinten 170 / vorn 230 hoch, Kastenruecken steigend.

Umbau 2026-10 nach out/frisch_analyse/fehler_frisch.md (Flickr 26271221407 ist von hinten RECHTS, nicht links);
Stand: Traverse 270 hoch, Schubbalken hinten 250 hoch + Lagerblock, Zylinder Ø100/Stange Ø48, Steuerblock vorn mit Kugel Ø40,
Leitungen flach knapp ueber dem Laengstraeger/Plattform (Nutzerhinweis). Aeltere Angaben unten, soweit nicht ueberholt.

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
    z 1060), Schellen an Maske, Haube und Schriftband; hinter dem Unterbau (Halter an der Unterbauwand) herunter auf
    Plattformhoehe und AM BODEN (z 885, |y| 440, Standschellen) nach hinten (7826381704). Rechts: Foerderleitung bis x 2250,
    dann schwarzer Schlauch ueber den Werkzeugkasten zum Steuerblock oben hinten auf dem rechten Endkasten (Kugelhebel); zweiter Schlauch (Ruecklauf) parallel zurueck, am Boden Rohr (y 500) in die Tankvorderwand;
    links: Saugleitung in die Tankvorderwand. Steuerblock -> zwei Leitungen auf die zwei parallelen Querrohre ueber der
    Traverse (z 1370 Stangenseite, z 1440 Kolbenseite/Buegel; versorgen beide Zylinder), Das
    untere duenne Rohr am Zylinder (BS, 39334013090) ist als Leckoelleitung gedeutet. Kein Gestaenge an der Haubenseite,
    kein Ventilblock auf der Pumpe (39333958410: linke Haubenseite nur das Rohr). Traverse: Rueckwand durchgehend (Quertraeger buendig mit
    den Endkaesten), Schild "Frisch" links der Mitte, Langloch rechts, Einfuellstutzen Ø ~115 mit roter Kappe
    (26271221407); Querrohre ueber der Traverse bei z 1370 (Leitung) und 1440 (Buegel).
  * Schild glatt (die Bohrungsreihe auf FL gehoert zu einer anderen Maschine).
  * Fuehrungsplatte mit Steckbolzen auf dem Schubbalken kurz hinter dem Leitrad (FL).

Hubkinematik (Arbeitsstellung = Schneide auf dem Boden, Schubbalken waagerecht), Stand nach Video-Auswertung 2026-10:
  Gelenk G = (1860, 400) (Lagerkappe ~ 390 vor der Triebradachse, Video v.mp4 t=164/166 und Foto 40431489714),
  Scheitel S = (1270, 1080), Zapfen Z = (2520, 1080), Schneide P = (-800, 0).
  Schild 1120 hoch: Schubbalken dreht um G um 24,1 Grad -> S' = (1599, 1262), |S'Z| = 939 (Zylinder 11 Grad geneigt).
  Arbeitsstellung: |SZ| = 1250.   Schild 200 tief: 4,3 Grad -> S'' = (1220, 1033), |S''Z| = 1301.
  -> Hub 1301 - 939 = 362 mm (aus der Arbeitsstellung 311 ein / 51 aus). Der Hub am Schild (1320) ist durch den kuerzeren
  Hebel (Scheitel 900 vom Gelenk) groesser als vorher (315). Hubwerte ungeprueft gegen das Original (im Video wird nicht gehoben).
  Kopf X_KOPF 1770: eingefahren steht der Gabelkopf (124 lang) bei 1599 + 124 = 1723, ~ 47 mm vor dem Abstreifer.
  Rohrende im Endkasten X_BODEN 2740 (220 hinter dem Zapfen): bei +11 Grad senkt sich der Boden um ~ 42 und bleibt in der
  Rueckwand frei. Kolbenstangenlaenge ab Auge 570..1180 moeglich (Kolben im Rohr).
  Balken (Video, Ueberlagerung ueber Leit-/Triebradnabe, Massstab 2,29 mm/px): hinten (x > 560) 170 hoch, vorn 230, Schraegubergang
  bei x 450..560, Balkenende vorn bei x -650; Kastenruecken steigt nach hinten (Lippe 760 -> Rueckwand z 900).

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
SCHILD_B, SCHILD_H = 2200.0, 760.0     # Breite 2150..2200 (Fotos 7826381704/39333958410: Balken buendig am Seitenblech)
X_SCHNEIDE = -800.0           # Vorderkante Schneide / Lippe (Video v.mp4 t=166, Ueberlagerung ueber Leit-/Triebradnabe: Lippe bei ~ -800 (+-100); vorher -700)
SH = X_SCHNEIDE + 700.0       # Vorverlegung der Schildfront gegen den Stand vor dem Video (Rueckseite/Seitenplatten-Hinterkante bleiben)
T_BLECH = 16.0                # Schildblech (2 mm im Modell)
T_RIPPE = 16.0
Y_WANGE = SCHILD_B / 2 - T_RIPPE       # Innenseite Seitenwange
X_RUECK = -470.0              # Hinterkante der Rippen
X_PL_H = -230.0              # Hinterkante der Seitenplatten (ragt ueber die Kastenrueckwand)
X_WANGE_H = -300.0            # Hinterkante der Seitenbleche (Foto 40431489714: D-Platte, Kante senkrecht am Balkenanschluss)
Z_LOCH = 450.0                # Bohrungsreihe im Schildblech (7826381704)
# Schubbalken: hinten hoher flacher Kasten 120 x 250, ab x 700 nach vorn verjuengt auf 130 (Foto 40431489714)
SB_B, SB_H = 120.0, 170.0     # Video t=164/158: hinterer Balkenteil niedrig (~150..180), vorn hoeher (~230) mit abgeschraegtem Uebergang
SB_Z0, SB_Z1 = Z_SCHUB - SB_H / 2, Z_SCHUB + SB_H / 2       # hinten 275 / 525
SB_XV = 560.0                 # ab hier nach hinten volle Hoehe, davor Verjuengung
SB_H_VORN = 230.0             # Hoehe am vorderen Teil (x < SB_XV - 110)
LB = 190.0                    # Lagerblock hinten (quadratisch)
X_GELENK = 1860.0             # hinteres Gelenk: Video t=164/158 und Foto 40431489714: Lagerkappe ~ 390 VOR der Triebradachse (vorher 2250)
X_SCHILDBOLZEN = -650.0       # Balkenende an der Schildfront (Video: Balken laeuft unter dem Kasten bis zur Zahnleiste an der Mulde)
X_BR = -150.0                 # Gelenkboecke am Kastenruecken (unveraendert)
# A-Bock
XA_VORN, XA_HINTEN = ABOCK_FUESSE
XS, ZS = ABOCK_SCHEITEL
A_TIEFE, A_BREITE = 70.0, 110.0        # Kastenstrebe: quer (y); Breite in der Ebene unten 150 -> oben 110
A_BREITE_UNTEN = 144.0
# dreieckiger Ausschnitt im Stegblech (BS): Basis ueber dem Schubbalken, Spitze unter dem Scheitel
AUS_B, AUS_Z0, AUS_Z1 = 290.0, SB_Z1 + 45, SB_Z1 + 265
# Hubzylinder (Mittelzapfen im Endkasten der Traverse), Rechnung siehe Docstring
X_ZAPFEN, Z_ZYL = TRAVERSE_X, TRAVERSE_Z   # Mittelzapfen bei x 2520 (Foto BS)
R_ZYL, R_STANGE = 50.0, 24.0        # Rohr Ø100, Stange Ø48 (Foto 40431489714)
X_KOPF = 1770.0               # Zylinderkopf-Flansch (Vorderseite)
X_BODEN = 2740.0              # Zylinderboden-Flansch (im Endkasten)
GABEL_L = 124.0               # Gabelkopf ab Scheitelauge bis Kontermutter
# Traverse: Endkaesten aussen, Quertraeger (Oeltank) hinten oben
EK_X0, EK_X1 = 2395.0, 2830.0
EK_Z0, EK_Z1 = 900.0, 1170.0   # 270 hoch (Seitenfotos 240..290)
Z_AUSS_O = EK_Z1 - 18.0         # Oberkante des Kastenausschnitts (Rest oben 18 mm, Verrundung 14)
Z_AUSS = 995.0               # Unterkante des Kastenausschnitts (Zylinder + untere Leitung)
EK_SCHR_DX, EK_SCHR_DY = 120.0, 190.0  # abgeschraegte hintere Aussenecke, beidseitig, ganze Kastenhoehe (Nutzerhinweis, c_ende_l; Rueckwand gerade bis |y| 880)
Y_LANGLOCH = 730.0            # Langloch rechts in der Rueckwand (270 x 110), vor der Schraege (gerade Rueckwand endet bei y 920)
EK_DY, EK_T = 95.0, 12.0               # halbe Breite (y), Wandstaerke
EK_YI = Y_SCHUB - EK_DY                # Innenseite Endkasten (880, frei von Werkzeugkasten-Deckel/Scharnier)
QT_X0, QT_X1 = 2630.0, EK_X1           # Quertraeger = Oeltank, Rueckwand buendig mit den Endkaesten (26271221407: durchgehende Rueckwand)
QT_Z0, QT_Z1 = EK_Z0, EK_Z1           # so hoch wie die Endkaesten (zoom_heck_l)
# Schutzbuegel
R_BUEGEL = 15.0               # Ø 30 (BS ~30)
BG_X0, BG_X1, BG_Z = 2340.0, 2640.0, EK_Z1 + 125.0
BG_HOCH = 1450.0              # hoher runder Buegel ueber dem Steuerblock (40431489714)
R_QL, Z_QL = 15.0, EK_Z1 + 70.0   # zwei parallele Querrohre dicht ueber der Traverse (c_links: 40..80 mm)
X_QL = 2655.0
Y_HAARNADEL = -680.0          # linkes Ende: enger Haarnadelbogen
# Oelpumpe vor dem Maskensockel (runde Zahnradpumpe, Fotos 26271249857 / 40431531504 / 40431489714)
PU_X, PU_Y, PU_Z = PUMPE
PU_R = 75.0                   # Gehaeuse Ø 150 (BS: 140 hoch, vorn: ~160)
PU_PL = 2.4                   # Frontplatte 2,4 mm in den Maskensockel (x = 0) eingesenkt
PU_XV, PU_XH = -225.0, -60.0  # Gehaeuse vorn / hinten (BS: Pumpenkoerper x -60 .. -220)
PU_XPORT, PU_ZPORT = -105.0, PU_Z - 40.0   # Anschluss seitlich, etwas unter der Achse
# Leitungen: je Seite EINE Leitung (Fotos), Ø ~ 36
R_LTG, R_ZYLLTG = 18.0, 11.0
Y_HAUBE = HAUBE_B / 2         # Haubenseite aussen (345)
Z_LTG = 560.0                 # Leitungen laufen flach knapp ueber dem Laengstraeger (Oberkante 520) an der Haubenseite nach hinten
LTG_VORN = (0.0, Z_LTG)       # (x, z) Maskenecke
LTG_HINTEN = (1405.0, Z_LTG)  # hier steigt die Leitung kurz senkrecht vor der Plattformkante (x 1430) auf Plattformhoehe
X_LTG_AB = LTG_HINTEN[0]
Y_HINT = 440.0                # |y| der Leitungen auf der Plattform (Gasse zwischen Sitz |y| <= 250 und Kaesten |y| >= 585)
Z_HINT = 885.0                # Rohrachse am Boden (Unterkante 867, 27 ueber der Plattform), auf Standschellen
XH_P, XH_R = 2500.0, 2550.0   # x der beiden Schlauchanschluesse am Steuerblock (Druck / Ruecklauf)
X_SCHLAUCH = 2250.0           # hier geht das Rohr rechts in den Schlauch zum Steuerblock ueber
# Steuerblock oben auf dem rechten Endkasten (Denkmal-Foto 40431489714; 7826381704 = anderes FRISCH-Exemplar, Einzelanfertigung, mit grosser Kugel hinten)
VB_X0, VB_X1 = 2464.0, 2604.0   # Steuerblock auf dem vorderen Teil des rechten Endkastens, ragt ~ 55 ueber die Kastenfront (40431489714: ~ 240 lang)
VB_Y0, VB_Y1 = 905.0, 1045.0
VB_Z0 = EK_Z1 + 14.0          # Unterkante Ventilkoerper (auf der Grundplatte)
VB_Z1 = EK_Z1 + 150.0         # Oberkante Block (1272; das Buegelrohr z 1295 liegt darueber)
Z_PORT = EK_Z1 + 55.0         # Achse der Schlauchanschluesse
# Fuehrungsplatte mit Steckbolzen (kurz hinter dem Leitrad)
FP_X0, FP_X1 = X_LEIT + 110.0, X_LEIT + 250.0   # stehende Platte 140 lang (Foto 40431489714), etwa 320 vor dem A-Bock-Fuss
X_STECK = X_LEIT + 280.0


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
    F = [(X_SCHNEIDE + 20, 0.0), (X_SCHNEIDE + 20, 150.0)]
    n = 24
    for i in range(1, n + 1):                          # gewoelbter Teil (Kreisbogen-artig)
        u = i / n
        z = 150 + 540 * u
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


def _randpunkte(poly, step, inset):
    """Punkte im Abstand `step` entlang des geschlossenen Polygons (x, z), um `inset` nach innen versetzt."""
    n = len(poly)
    area = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    sg = 1.0 if area > 0 else -1.0
    segs = []
    for i in range(n):
        (x0, z0), (x1, z1) = poly[i], poly[(i + 1) % n]
        L = math.hypot(x1 - x0, z1 - z0)
        if L > 1e-6:
            segs.append((x0, z0, x1, z1, L))
    total = sum(sg_[4] for sg_ in segs)
    k = max(1, round(total / step))
    d = total / k
    out, acc, i = [], 0.0, 0
    for j in range(k):
        pos = (j + 0.5) * d
        while i < len(segs) - 1 and acc + segs[i][4] < pos:
            acc += segs[i][4]
            i += 1
        x0, z0, x1, z1, L = segs[i]
        u = (pos - acc) / L
        nx, nz = -(z1 - z0) / L * sg, (x1 - x0) / L * sg     # Normale nach innen
        out.append((x0 + (x1 - x0) * u + nx * inset, z0 + (z1 - z0) * u + nz * inset))

    def _innen(px, pz):
        # Punkt im Polygon und mindestens 0.7 * inset von jeder Kante entfernt
        ein = False
        for (xa, za), (xb, zb) in zip(poly, poly[1:] + poly[:1]):
            if (za > pz) != (zb > pz) and px < xa + (pz - za) * (xb - xa) / (zb - za):
                ein = not ein
            dx, dz = xb - xa, zb - za
            L2 = dx * dx + dz * dz
            if L2 > 1e-9:
                q = max(0.0, min(1.0, ((px - xa) * dx + (pz - za) * dz) / L2))
                if math.hypot(px - xa - q * dx, pz - za - q * dz) < 0.7 * inset:
                    return False
        return ein
    return [p for p in out if _innen(*p)]


def schild(t):
    F, B = _profil()
    # Schildblech (gewoelbt, Lippe nach vorn gekantet), glatt; Front blank/graumetallisch (39333958410), nur die Seitenbleche lackiert
    blech = platte_xz(F + B[::-1], -Y_WANGE, Y_WANGE)
    # Bohrungsreihe (Foto 7826381704: ~ 8 kleine Loecher Ø 28 in einer Reihe etwa in halber Hoehe, zwischen den Rippen)
    for y in (-900.0, -625.0, -375.0, -125.0, 125.0, 375.0, 625.0, 900.0):
        blech -= Pos(X_SCHNEIDE + 120, y, Z_LOCH) * Rot(0, 90, 0) * Cylinder(14, 300)
    t.mat("zink", blech)
    # kraeftiger, nach vorn gerollter Wulst an der Oberkante (7826381704)
    xl, zl = F[-1]
    t.append(stab((xl + 8, -Y_WANGE, zl - 10), (xl + 8, Y_WANGE, zl - 10), 19))
    # Seitenwangen
    # Lippenspitze der Wange gekappt (keine Messerkante): Kappe 7 mm breit
    # "D"-Form (c_sr_schild): hintere Kante fast senkrecht, Oberkante steigt nach vorn, vorn grosser konvexer Radius
    # Seitenbleche (Foto 40431489714): flache D-Platten, hintere Kante senkrecht am Balkenanschluss (x -300), Oberkante steigt nach
    # vorn; nur wenige einzelne Schrauben (keine Randreihe) und ein Entlastungsloch
    # konvexe D-Platte (aeusserer Umriss, verdeckt die konkave Blechkontur): vorn gerade/leicht gebogen, oben schraeg nach hinten fallend,
    # Hinterkante senkrecht, hintere untere Ecke stark verrundet (Foto 40431489714)
    XP = X_PL_H
    wange = [(-720.0 + SH, 745.0), (-728.0 + SH, 560.0), (-726.0 + SH, 400.0)]
    cx, cz, rx, rz = -440.0 + SH, 290.0, 286.0, 290.0                     # grosser Viertelbogen vorn unten (fast halbrund)
    for k in range(0, 13):
        th = math.radians(180 + 90 * k / 12)
        wange.append((cx + rx * math.cos(th) * 1.0, cz + rz * math.sin(th)))
    wange += [(-330.0, 0.0), (XP - 60, 4.0), (XP - 12, 40.0), (XP, 100.0), (XP, 600.0), (-700.0 + SH, 745.0 + 0.0)]
    wange = wange[:-1]
    for s in (-1, 1):
        w_ = platte_xz(wange, s * Y_WANGE, s * SCHILD_B / 2)
        w_ -= Pos(-560.0 + SH, s * (Y_WANGE + 8), 70) * Rot(90, 0, 0) * Cylinder(10, 40)
        t.append(w_)
        for (px, pz) in ((-380.0, 600.0), (X_PL_H - 45, 380.0), (X_PL_H - 70, 120.0), (-640.0 + SH, 330.0), (-520.0 + SH, 150.0)):
            t.mat("blank", sechskant((px, s * SCHILD_B / 2, pz), (0, s, 0), 34, 12))
    # Winkelprofil an der Hinterkante der Seitenplatte (7826381704: blaue senkrechte Kantenschiene mit Schrauben)
    for s in (-1, 1):
        ya_, yb_ = sorted((s * (SCHILD_B / 2), s * (SCHILD_B / 2 + 14)))
        t.append(box(X_PL_H - 50, X_PL_H - 6, ya_, yb_, 100.0, 600.0))
        for zz in (160.0, 380.0, 540.0):
            t.mat("blank", sechskant((X_PL_H - 28, s * (SCHILD_B / 2 + 14), zz), (0, s, 0), 24, 8))
    # Rueckseite als hoher Kastentraeger (Foto 40431489714: tiefer Kasten ueber die ganze Breite, Oberseite schraeg nach hinten
    # abfallend, senkrechte Rueckwand, nach innen Zwischenrippen) zwischen den Seitenblechen
    XB = X_WANGE_H
    ZB0, ZB1 = 110.0, 900.0      # Video t=164: Oberseite steigt nach hinten (Lippe 770 -> Kastenruecken ~ 1000), vorher fallend (ZB1 610)
    zug = _zug(B, ZB0, 690, 16)
    kasten = platte_xz(zug + [(XB, ZB1), (XB, ZB0)], -Y_WANGE, Y_WANGE)
    innen = [(x + 10, z) for x, z in _zug(B, ZB0 + 14, 676, 12)] + [(XB - 14, ZB1 - 16), (XB - 14, ZB0 + 14)]
    kasten -= platte_xz(innen, -Y_WANGE + T_RIPPE, Y_WANGE - T_RIPPE)
    t.append(kasten)
    for y in (0.0, -430.0, 430.0, -860.0, 860.0):                               # Innenrippen
        t.append(platte_xz(innen, y - T_RIPPE / 2, y + T_RIPPE / 2))
    # abgesetzte Oberleiste (breiter Flansch nach hinten, Foto: zweite Stufe auf der Kastendecke)
    t.append(platte_xz([(XB + 20, ZB1), (XB - 150, ZB1 + 40), (XB - 150, ZB1 + 52), (XB + 20, ZB1 + 12)], -Y_WANGE, Y_WANGE))
    # Tragrippen sichtbar als Absatz an der Rueckwand (senkrechte Bleche, 3 Paare)
    for y in (-860.0, -430.0, 430.0, 860.0):
        t.append(box(XB, XB + 16, y - 25, y + 25, ZB0 + 20, ZB1 - 20))
    # Anlenkboecke in der Mitte (Foto: Gelenkbock mit uebereinander gestapelten Klotz-Laschen / Zahnleiste und Querbolzen)
    for sg in (-1, 1):
        yc = sg * 150.0
        for dy in (-52, 52):
            t.append(platte_xz([(XB, ZB0 + 20), (XB + 150, ZB0 + 20), (XB + 150, ZB1 - 60), (XB, ZB1 - 60)], yc + dy - 12, yc + dy + 12))
        for zc in (230.0, 330.0, 430.0):                                         # Klotz-Stufen zwischen den Wangen
            t.append(box(XB + 30, XB + 150, yc - 40, yc + 40, zc - 35, zc + 35))
            t.mat("blank", rad_y(XB + 110, yc, zc, 12, 150))
        t.mat("blank", rad_y(XB + 70, yc, 520.0, 24, 150))                       # grosser Querbolzen oben
        t.mat("blank", rad_y(XB + 70, yc, 520.0, 34, 10))

    # Schneide (7826381704): EINE durchgehende, lackierte Leiste ueber die ganze Breite, buendig mit den Seitenblechen,
    # blanke Senkschrauben im ~190-mm-Raster, keine Eckmesser
    x0 = X_SCHNEIDE
    t.append(platte_yz([(-SCHILD_B / 2, 0), (SCHILD_B / 2, 0), (SCHILD_B / 2, 165), (-SCHILD_B / 2, 165)], x0, x0 + 20))
    n = 11
    for i in range(n):
        y = -SCHILD_B / 2 + 60 + (SCHILD_B - 120) * (i + 0.5) / n
        t.mat("blank", rad_x(x0 - 2, y, 85, 14, 4))
    # Anschluss der Schubbalken (Foto 40431489714): Balkenende (Endblock) stoesst an die Rueckwand des Kastens, aussen eine
    # Laschenplatte mit senkrechter Reihe aus 3 Bolzenloechern (Neigungs-Verstellung), Bolzenkoepfe aussen; Beugel am Seitenblech
    for s in (-1, 1):
        yo = Y_WANGE + 18
        yi = Y_SCHUB - SB_B / 2 - 4
        # Gelenkbock: Rueckplatte am Kasten + drei uebereinander gestapelte Klotzlaschen (Leiter / Zahnleiste), grosser Bolzen oben
        ya_, yb_ = sorted((s * yi, s * (Y_WANGE - 1)))
        t.append(box(XB - 1, X_BR + 4, ya_, yb_, Z_SCHUB - 170, Z_SCHUB + 170))              # Stirnblock am Balkenende
        ya3, yb3 = sorted((s * (Y_WANGE + 1), s * yo))
        for zc in (Z_SCHUB - 110, Z_SCHUB, Z_SCHUB + 110):
            t.append(box(X_PL_H + 4, X_BR + 20, ya3, yb3, zc - 38, zc + 38))                  # Klotz hinter der Seitenplatte
            t.mat("blank", rad_y(X_PL_H + 60, s * (Y_WANGE + 10), zc, 14, 70))                           # Stufenbolzen
        t.append(box(X_PL_H + 4, X_PL_H + 30, ya3, yb3, Z_SCHUB - 160, Z_SCHUB + 160))                  # Steg
        t.mat("blank", rad_y(X_PL_H + 85, s * (Y_WANGE + 20), Z_SCHUB + 175, 40, 56))                    # grosser Bolzen oben
        t.mat("blank", rad_y(X_PL_H + 85, s * (Y_WANGE + 52), Z_SCHUB + 175, 52, 12))
    # stehende Laschen mit U-Ausschnitt auf dem Kastenflansch (Foto: einzelne hohe Platten quer zur Schildebene)
    ZL = ZB1 + 52 + 90                                                    # ~ 1/3 der Schildhoehe ueber der Oberleiste
    for y in (-860.0, -150.0, 150.0, 860.0):
        lp = platte_xz([(XB - 180, ZB1 + 36), (XB + 20, ZB1 + 10), (XB + 20, ZL - 40), (XB - 10, ZL), (XB - 140, ZL), (XB - 180, ZL - 60)],
                       y - 9, y + 9)
        lp -= Pos(XB - 90, y, ZL - 70) * Rot(90, 0, 0) * Cylinder(22, 30)
        lp -= box(XB - 130, XB - 50, y - 12, y + 12, ZL - 70, ZL + 5)
        t.append(lp)
    return B


# ---------------- Schubbalken, Gelenkbock, A-Bock ----------------
def sb_h(x):
    """Balkenhoehe bei x: ab SB_XV nach hinten voll (250), davor linear auf SB_H_VORN am vorderen Auge."""
    if x >= SB_XV:
        return SB_H
    return SB_H_VORN + (SB_H - SB_H_VORN) * max(0.0, (x - (SB_XV - 110.0)) / 110.0)


def sb_top(x):
    return Z_SCHUB + sb_h(x) / 2


def sb_bot(x):
    return Z_SCHUB - sb_h(x) / 2


def schubbalken(t, s):
    y = s * Y_SCHUB
    yi, ya = y - SB_B / 2, y + SB_B / 2        # (nur Breitenbereich; aussen ist y + s * SB_B / 2)
    yo = y + s * SB_B / 2
    xa, xe = X_SCHILDBOLZEN, X_GELENK - LB / 2 + 10
    xs = [xa, SB_XV - 110.0, SB_XV, xe]
    # Kasten: hinten hoch und flach, nach vorn verjuengt (Foto 40431489714), Polygonplatte statt Quader
    t.append(platte_xz([(x, sb_top(x)) for x in xs] + [(x, sb_bot(x)) for x in xs[::-1]], yi, ya))
    # Gurtbleche (Obergurt / Untergurt) folgen dem Profil
    xg = [X_SCHILDBOLZEN + 60, SB_XV - 110.0, SB_XV, X_GELENK - 90]
    t.append(platte_xz([(x, sb_top(x)) for x in xg] + [(x, sb_top(x) - 14) for x in xg[::-1]], yi - 6, ya + 6))
    t.append(platte_xz([(x, sb_bot(x)) for x in xg] + [(x, sb_bot(x) + 14) for x in xg[::-1]], yi - 6, ya + 6))
    # hinten quadratischer Lagerblock (~190 x 190), aussen ~50 ueberstehend, 4 Sechskantschrauben, Fettkappe (c_sr_beam)
    yb = yo + s * 50
    t.append(kasten_rund(X_GELENK - LB / 2, X_GELENK + LB / 2, y - s * SB_B / 2, yb, Z_SCHUB - LB / 2, Z_SCHUB + LB / 2, 14, Axis.Y))
    for dx in (-62, 62):
        for dz in (-62, 62):
            t.mat("blank", sechskant((X_GELENK + dx, yb, Z_SCHUB + dz), (0, s, 0), 26, 10))
    t.mat("blank", stab((X_GELENK, yb, Z_SCHUB), (X_GELENK, yb + s * 18, Z_SCHUB), 24))            # Fettkappe
    t.mat("blank", stab((X_GELENK, yb + s * 18, Z_SCHUB), (X_GELENK, yb + s * 26, Z_SCHUB), 10))
    # Foto 7826381704: schwarzes Gummi-/Trittband auf dem Obergurt kurz hinter dem Schild, Buegelschelle (U-Band) um den Balken,
    # (schraege Aussenlasche des Fotos entfaellt: Passstiftschnitt macht sie zu duenn)
    t.mat("gummi", platte_xz([(-100, sb_top(-100) - 1), (260, sb_top(260) - 1), (260, sb_top(260) + 12), (-100, sb_top(-100) + 12)], y - 40, y + 40))
    xs_ = 520.0
    t.append(box(xs_ - 14, xs_ + 14, y - SB_B / 2 - 14, y + SB_B / 2 + 14, sb_bot(xs_) - 14, sb_bot(xs_)))
    t.append(box(xs_ - 14, xs_ + 14, y - SB_B / 2 - 14, y - SB_B / 2, sb_bot(xs_), sb_top(xs_)))
    t.append(box(xs_ - 14, xs_ + 14, y + SB_B / 2, y + SB_B / 2 + 14, sb_bot(xs_), sb_top(xs_)))
    t.append(box(xs_ - 14, xs_ + 14, y - SB_B / 2 - 14, y + SB_B / 2 + 14, sb_top(xs_), sb_top(xs_) + 14))
    t += [sechskant((xs_, yo + s * 14, sb_bot(xs_) + 40), (0, s, 0), 22, 8), sechskant((xs_, yo + s * 14, sb_top(xs_) - 40), (0, s, 0), 22, 8)]
    # Querschotte aussen sichtbar als Schweisslaschen
    for x in (450, 1100, 1750):
        t.append(box(x - 8, x + 8, yo, yo + s * 6, sb_bot(x) + 14, sb_top(x) - 14))


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
    pl = platte_xz([(1770, 335), (1960, 330), (1960, 470), (1770, 470)], yi, ya)
    pl += Pos(X_GELENK, (yi + ya) / 2, Z_SCHUB) * Rot(90, 0, 0) * Cylinder(85, 32)
    t.append(pl)
    # Versteifungsrippe oben und Nabe
    t.append(box(1790, 1940, s * 830, s * 848, 455, 480))
    t.append(rad_y(X_GELENK, s * 900, Z_SCHUB, 70, 40))
    bolzen_y(t, X_GELENK, s * 830, s * (Y_SCHUB + 20), Z_SCHUB, 40)               # endet im Lagerblock des Schubbalkens
    schmiernippel(t, X_GELENK, s * 900, Z_SCHUB + 68)


def fuehrungsplatte(t, s):
    """Fuehrungsplatte (innen am Schubbalken, stehend ~ 240 hoch x 140 lang, 2 Sechskantschrauben oben) und Steckbolzen in einer
    Aufschweisshuelse auf dem Obergurt, kurz hinter der Platte (Foto 40431489714; Lage des Bolzens unsicher)."""
    y = s * Y_SCHUB
    yi = y - s * SB_B / 2                     # Innenseite Schubbalken
    za, zb = sb_top(FP_X0), sb_top(FP_X1)
    pts = [(FP_X0, sb_bot(FP_X0) + 12), (FP_X1, sb_bot(FP_X1) + 12), (FP_X1, zb + 160), (FP_X1 - 25, zb + 190),
           (FP_X0 + 25, za + 190), (FP_X0, za + 160)]
    t.append(platte_xz(pts, yi + s * 3, yi - s * 16))
    t += [sechskant((x, yi - s * 16, za + 140), (0, -s, 0), 18, 7) for x in (FP_X0 + 40, FP_X1 - 40)]
    # Steckbolzen: Huelse, Bolzen mit Bund, Ziehring
    zt = sb_top(X_STECK)
    t.append(scheibe_z(X_STECK, y, zt - 3, 24, 43))
    t.mat("blank", scheibe_z(X_STECK, y, zt + 40, 13, 30))
    t.mat("blank", scheibe_z(X_STECK, y, zt + 70, 20, 10))
    t.mat("blank", ring_y(X_STECK, y, zt + 100, 24, 15, 9))
    # Haltekette des Bolzens (Oese an der Huelse)
    t.append(ring_x(X_STECK, y + s * 26, zt + 20, 10, 5, 6))


def _bein(xf, y):
    """Kastenstrebe von Fuss xf zum Scheitel, nach oben verjuengt (unten 150, oben 110 in der Ebene), 70 tief."""
    F = Vector(xf, 0, SB_Z1 - 20)
    P = Vector(XS, 0, ZS)
    d = (P - F).normalized()
    p = Vector(-d.Z, 0, d.X)
    pts = [(F + p * (A_BREITE_UNTEN / 2)), (F - p * (A_BREITE_UNTEN / 2)), (P - p * (A_BREITE / 2)), (P + p * (A_BREITE / 2))]
    return platte_xz([(q.X, q.Z) for q in pts], y - A_TIEFE / 2, y + A_TIEFE / 2)


def abock(t, s):
    """A-Bock: zwei Kastenstrebe (nach oben verjuengt) von ABOCK_FUESSE zum Scheitel, Stegblech mit Dreieckausschnitt,
    flacher Kastenkopf am Scheitel, schraeges Knotenblech vor dem vorderen Fuss auf dem Balken (c_sr_beam)."""
    y = s * Y_SCHUB
    yi, ya = y - A_TIEFE / 2, y + A_TIEFE / 2
    for xf in (XA_VORN, XA_HINTEN):
        t.append(_bein(xf, y))
        t.append(box(xf - 90, xf + 90, y - 55, y + 55, SB_Z1 - 3, SB_Z1 + 16))       # Fussplatte
        t += schraubenreihe((xf - 65, y + s * 55, SB_Z1 + 8), (xf + 65, y + s * 55, SB_Z1 + 8), 2, (0, s, 0), 18, 6)
    # Knotenblech (~ 240 lang) vom vorderen Fuss nach vorn abfallend bis hinter den Steckbolzen, 2 Schrauben
    t.append(platte_xz([(X_STECK + 40, SB_Z1), (X_STECK + 40, SB_Z1 + 45), (XA_VORN + 90, SB_Z1 + 200), (XA_VORN + 60, SB_Z1)],
                       y - 10, y + 10))
    t += [sechskant((x, y + s * 10, SB_Z1 + 22 + (x - X_STECK - 40) * 0.2), (0, s, 0), 16, 6) for x in (X_STECK + 80, X_STECK + 140)]
    # Stegblech zwischen den Streben mit dreieckigem Ausschnitt unten in der Mitte (BS)
    xm = (XA_VORN + XA_HINTEN) / 2
    aussen = Polygon((XA_VORN + 40, SB_Z1 - 3), (XA_HINTEN - 40, SB_Z1 - 3), (XS, ZS - 70), align=None)
    innen = Polygon((xm - AUS_B / 2, AUS_Z0), (xm + AUS_B / 2, AUS_Z0), (XS, AUS_Z1), align=None)
    innen = fillet(innen.vertices(), 25)
    blech = extrude(Plane.XZ * (aussen - innen), amount=44)
    t.append(Pos(0, y - 22 - blech.bounding_box().min.Y, 0) * blech)
    # Randleiste um den Ausschnitt (Flachstahl, beidseitig 6 mm aufgesetzt)
    rand = extrude(Plane.XZ * (offset(innen, 22) - innen), amount=48)
    t.append(Pos(0, y - 24 - rand.bounding_box().min.Y, 0) * rand)
    # Scheitel: flacher Kastenkopf (~ 180 x 170) mit Lagerauge und Buchse
    t.append(kasten_rund(XS - 110, XS + 70, yi, ya, ZS - 85, ZS + 85, 22, Axis.Y))
    t.append(rad_y(XS, y, ZS, 78, A_TIEFE))
    t.mat("blank", rad_y(XS, y, ZS, 44, A_TIEFE + 6))
    schmiernippel(t, XS, y, ZS + 85)


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
    # Kolbenstange (matt braun-blank, Foto 40431489714)
    x0 = XS + GABEL_L - 4
    t.mat("blank", rad_x((x0 + X_KOPF - 30) / 2, y, z, R_STANGE, X_KOPF - 30 - x0))
    # Stopfbuchse, vierkantiger Kopfblock (~ 60 lang x 165 x 165, Eckschrauben), Rohr dahinter
    t.append(rad_x(X_KOPF - 18, y, z, 34, 36))
    t.mat("schwarz", rad_x(X_KOPF - 40, y, z, 29, 10))           # Abstreifer
    t.append(kasten_rund(X_KOPF - 4, X_KOPF + 56, y - 82, y + 82, z - 82, z + 82, 8, Axis.X))
    for dy in (-58, 58):
        for dz in (-58, 58):
            t.mat("blank", sechskant((X_KOPF - 4, y + dy, z + dz), (-1, 0, 0), 20, 8))
    # Zylinderrohr Ø100 bis in den Endkasten
    t.append(rad_x((X_KOPF + 50 + X_BODEN) / 2, y, z, R_ZYL, X_BODEN - X_KOPF - 50))
    # Zapfenring mit Querzapfen (lagert in beiden Kastenwaenden)
    t.append(rad_x(X_ZAPFEN, y, z, R_ZYL + 10, 90))
    t.mat("blank", rad_y(X_ZAPFEN, y, z, 28, 2 * EK_DY - 2 * EK_T + 6))
    # Bodenflansch, Boden mit Schrauben
    t.append(rad_x(X_BODEN + 8, y, z, R_ZYL + 14, 16))
    t.append(rad_x(X_BODEN + 31, y, z, R_ZYL + 7, 30))
    t += schraubenkreis((X_BODEN + 46, y, z), (1, 0, 0), 36, 6, 14, 8, start=30)
    # zwei duenne Rohre ueber die ganze Zylinderlaenge oben und unten (z +- 62), unteres biegt am Kopf nach unten (c_sr_box)
    dz = 62.0
    t.append(box(X_KOPF + 40, X_KOPF + 70, y - 18, y + 18, z + R_ZYL, z + dz + 8))
    t.append(rohr_glatt([(X_KOPF + 60, y, z + dz), (EK_X0 + 60, y, z + dz)], R_ZYLLTG - 2, 22))
    t.append(box(X_KOPF + 40, X_KOPF + 70, y - 18, y + 18, z - dz - 8, z - R_ZYL))
    t.append(rohr_glatt([(X_KOPF + 60, y, z - dz - 40), (X_KOPF + 60, y, z - dz), (EK_X0 + 60, y, z - dz)], R_ZYLLTG - 2, 24))
    for x in (2110.0, 2200.0):                                    # Sattelschellen
        t.append(box(x - 12, x + 12, y - 16, y + 16, z + R_ZYL - 6, z + dz))
        t.append(box(x - 12, x + 12, y - 16, y + 16, z - dz, z - R_ZYL + 6))


# ---------------- Traverse (Endkaesten + Quertraeger/Oeltank) ----------------
def _ecke_prisma(s, y, grow):
    """Prisma (z-Extrusion) ueber der hinteren Aussenecke des Endkastens: Region hinter der Schraege
    (Dx = EK_SCHR_DX, Dy = EK_SCHR_DY, links und rechts gleich). grow > 0 verschiebt die Schraegflaeche um grow nach innen (fuer den Innenraum)."""
    ya = y + s * EK_DY
    p1 = Vector(EK_X1 - EK_SCHR_DX, ya, 0)
    p2 = Vector(EK_X1, ya - s * EK_SCHR_DY, 0)
    d = (p2 - p1).normalized()
    n = Vector(EK_SCHR_DY, s * EK_SCHR_DX, 0).normalized()          # zeigt zur abgeschnittenen Ecke
    a, b = p1 - n * grow - d * 60, p2 - n * grow + d * 60
    pts = [(a.X, a.Y), (b.X, b.Y), (b.X + n.X * 200, b.Y + n.Y * 200), (a.X + n.X * 200, a.Y + n.Y * 200)]
    if sum(pts[i][0] * pts[(i + 1) % 4][1] - pts[(i + 1) % 4][0] * pts[i][1] for i in range(4)) < 0:
        pts = pts[::-1]                                              # immer gegen den Uhrzeigersinn (Extrusion nach +z)
    pr = extrude(Plane.XY.offset(EK_Z0 - 5) * Polygon(*pts, align=None), amount=EK_Z1 - EK_Z0 + 10)
    return pr


def endkasten(t, s):
    """Rechteckiger Endkasten (Blechkasten, hohl) mit abgeschraegter hinterer Aussenecke (Dx 90 / Dy 150), Zylinder ragt vorn
    durch einen Ausschnitt hinein; Stuetzschraege (Konsole) unten, Langloch in der Rueckwand (rechts)."""
    y = s * Y_SCHUB
    k = kasten_rund(EK_X0, EK_X1, y - EK_DY, y + EK_DY, EK_Z0, EK_Z1, 14, Axis.Y)
    k -= _ecke_prisma(s, y, 0.0)
    ki = kasten_rund(EK_X0 + EK_T, EK_X1 - EK_T, y - EK_DY + EK_T, y + EK_DY - EK_T, EK_Z0 + EK_T, EK_Z1 - EK_T, 6, Axis.Y)
    ki -= _ecke_prisma(s, y, EK_T)
    k -= ki
    # Ausschnitt vorn fuer Zylinder und Leitungen (nach oben bis fast zur Decke: Schwenkfreiheit beim Heben)
    k -= box(EK_X0 - 5, EK_X0 + EK_T + 5, y - R_ZYL - 12, y + R_ZYL + 12, Z_AUSS, Z_AUSS_O)
    zm = (EK_Z0 + EK_Z1) / 2
    if s > 0:
        # Langloch in der Rueckwand dicht am rechten Ende (26271221407: Obround ~ 270 x 110, vor der Schraege)
        k -= kasten_rund(EK_X1 - EK_T - 2, EK_X1 + 2, Y_LANGLOCH - 135, Y_LANGLOCH + 135, zm - 55, zm + 55, 54, Axis.X)
    t.append(k)
    # Kantenschutz um den Ausschnitt
    t.append(box(EK_X0 - 8, EK_X0 + 2, y - R_ZYL - 24, y - R_ZYL - 12, Z_AUSS - 12, Z_AUSS_O))
    t.append(box(EK_X0 - 8, EK_X0 + 2, y + R_ZYL + 12, y + R_ZYL + 24, Z_AUSS - 12, Z_AUSS_O))
    t.append(box(EK_X0 - 8, EK_X0 + 2, y - R_ZYL - 24, y + R_ZYL + 24, Z_AUSS - 12, Z_AUSS))
    # Zapfenlager: Deckel Ø100 aussen vorn (1-2 Schrauben + Fettloch), Nabe innen
    ya = y + s * EK_DY
    t.append(rad_y(X_ZAPFEN, ya + s * 6, Z_ZYL, 50, 14))
    t += [sechskant((X_ZAPFEN + dx, ya + s * 13, Z_ZYL + 26), (0, s, 0), 14, 6) for dx in (-26, 26)]
    t.mat("schwarz", rad_y(X_ZAPFEN, ya + s * 13, Z_ZYL - 14, 7, 4))                # Fettloch
    yi = y - s * EK_DY
    t.append(rad_y(X_ZAPFEN, yi - s * 8, Z_ZYL, 44, 19))
    # Schweissnaht-/Falzleisten aussen
    t.append(box(EK_X0 + 30, EK_X1 - EK_SCHR_DX - 40, ya - s * 3, ya + s * 6, EK_Z0 + 22, EK_Z0 + 34))
    # Stuetzschraege (Konsole) unter dem Kasten, nach vorn abfallend ~ 30..36 Grad (c_sr_box / c_sl_box)
    ys = s * (Y_SCHUB + 30)
    t.append(platte_xz([(EK_X1 - 100, EK_Z0 + 2), (EK_X1 - 220, EK_Z0 + 2), (EK_X1 - 370, EK_Z0 - 110), (EK_X1 - 370, EK_Z0 - 155)],
                       ys - 13, ys + 13))
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
    qt = kasten_rund(QT_X0, QT_X1, -EK_YI - 3, EK_YI + 3, QT_Z0, QT_Z1, 14, Axis.Y)
    zm = (QT_Z0 + QT_Z1) / 2
    # Langloch rechts in der Rueckwand (setzt sich im Endkasten fort, s. endkasten)
    qt -= kasten_rund(QT_X1 - 20, QT_X1 + 2, Y_LANGLOCH - 135, Y_LANGLOCH + 135, zm - 55, zm + 55, 54, Axis.X)
    for s_ in (-1, 1):
        qt -= _ecke_prisma(s_, s_ * Y_SCHUB, 0.0)          # Quertraeger endet buendig an der Schraegflaeche
    t.append(qt)
    # umlaufender Bodenflansch nach hinten abgekantet (~ 35 vor, ~ 45 hoch), je 2 Sechskantschrauben (c_links)
    yfl = EK_YI - 2        # endet an der Schraege (nichts steht ueber die Schraegflaeche)
    t.append(box(QT_X1 - 2, QT_X1 + 35, -yfl, yfl, QT_Z0, QT_Z0 + 45))
    for yc in (-340.0, 440.0):
        for dy in (-35, 35):
            t.mat("schwarz", sechskant((QT_X1 + 35, yc + dy, QT_Z0 + 22), (1, 0, 0), 22, 8))
    # Firmenschild "Frisch": dunkelblaue Platte, weisser Rand und weisse Blockschrift (26271221407), 410 x 215 bei y -230
    zs0, zs1 = zm - 90, zm + 125
    ys0, ys1 = -230 - 205, -230 + 205
    t.mat("bosch", box(QT_X1, QT_X1 + 6, ys0, ys1, zs0, zs1))
    for (a, b, c, d) in ((ys0, ys1, zs0, zs0 + 12), (ys0, ys1, zs1 - 12, zs1), (ys0, ys0 + 12, zs0, zs1), (ys1 - 12, ys1, zs0, zs1)):
        t.mat("zifferblatt", box(QT_X1 + 6, QT_X1 + 10, a, b, c, d))
    try:
        pl = Plane(origin=(QT_X1 + 6, -230, (zs0 + zs1) / 2), x_dir=(0, 1, 0), z_dir=(1, 0, 0))   # Blick von hinten: rechts = +y
        tx = extrude(pl * Text("Frisch", 95, font_style=FontStyle.BOLD, align=(Align.CENTER, Align.CENTER)), amount=4)
        t.mat("zifferblatt", tx)
    except Exception as e:                                          # Schriftart nicht verfuegbar
        print("Frisch-Schrift entfaellt:", e)
    # Reinigungsdeckel vorn mit Schrauben
    t.append(box(QT_X0 - 8, QT_X0 + 2, -380, 380, QT_Z0 + 30, QT_Z1 - 30))
    t += schraubenreihe((QT_X0 - 8, -350, QT_Z1 - 48), (QT_X0 - 8, 350, QT_Z1 - 48), 7, (-1, 0, 0), 14, 6)
    t += schraubenreihe((QT_X0 - 8, -350, QT_Z0 + 48), (QT_X0 - 8, 350, QT_Z0 + 48), 7, (-1, 0, 0), 14, 6)
    # Einfuellstutzen (26271221407): Ø ~ 136, ~ 125 hoch, flache rotbraune Kappe mit Rand, bei y -170
    xe, ye_ = 2730.0, -170.0
    t.append(scheibe_z(xe, ye_, QT_Z1 - 2, 68, 112))
    t.mat("auspuff", scheibe_z(xe, ye_, QT_Z1 + 108, 72, 16))                   # Kappe mit Rand
    t.mat("auspuff", scheibe_z(xe, ye_, QT_Z1 + 122, 54, 6))
    # Ablassschraube unten
    t.mat("schwarz", sechskant((2720, 520, QT_Z0), (0, 0, -1), 30, 14))


# ---------------- Schutzbuegel ----------------
def schutzbuegel(t):
    """Niedriges Gelaender (Foto 26271221407, c_links, c_sr_box): ein durchgehendes Rohr bildet zwei parallele Querrohre
    (Abstand 55) dicht ueber der Traverse (40..80 mm); links endet es in einem engen Haarnadelbogen (y -680), rechts
    laeuft es in einer niedrigen Schlaufe ueber dem Steuerblock auf dem rechten Endkasten aus. Nichts ragt ueber die
    Rueckwand hinaus (keine Schlaufe hinten links)."""
    y = Y_SCHUB - 55
    ya = 1018.0                                                  # Ende der Stangenseiten-Leitung (hinter dem Steuerblock)
    t.append(rohr_glatt([(EK_X0 + 30, y, EK_Z1 - 3), (EK_X0 + 30, y, BG_HOCH), (BG_X1, y, BG_HOCH), (BG_X1, y, BG_Z),
                         (BG_X1, Y_HAARNADEL, BG_Z), (X_QL, Y_HAARNADEL, Z_QL),
                         (X_QL, ya, Z_QL), (X_QL, ya, EK_Z1 - 3)], R_BUEGEL, 55))
    for x, yy in ((EK_X0 + 30, y), (X_QL, ya)):                  # Fussplatten
        t.append(box(x - 22 if x < 2500 else x - 36, x + 22 if x < 2500 else x + 36, yy - 36, yy + 36, EK_Z1 - 3, EK_Z1 + 10))
    # Haarnadelbogen links: Stuetze auf der Decke
    xh = (BG_X1 + X_QL) / 2
    t.append(box(xh - 36, xh + 36, Y_HAARNADEL - 36, Y_HAARNADEL + 36, EK_Z1 - 3, EK_Z1 + 10))
    t.append(stab((xh, Y_HAARNADEL, EK_Z1), (xh, Y_HAARNADEL, Z_QL + 6), 10))
    for yy in (-450.0, 100.0, 600.0):                            # nur drei Doppelschellen halten beide Querrohre (kein "Gitter")
        t.append(box(X_QL - 12, X_QL + 12, yy - 14, yy + 14, QT_Z1 - 2, Z_QL - R_QL + 2))
        t.append(box(BG_X1 - 12, X_QL + 12, yy - 8, yy + 8, Z_QL - R_QL, BG_Z + R_BUEGEL))


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
        t.append(rad_y(PU_XPORT, s * 96, PU_ZPORT, R_LTG + 12, 24))
        t += [sechskant((PU_XPORT + dx, s * 104, PU_ZPORT), (0, s, 0), 12, 6) for dx in (-R_LTG - 7, R_LTG + 7)]


# ---------------- Hydraulikleitungen ----------------
def _schelle_haube(t, x, s, r):
    """Rohrschelle um die flach laufende Leitung. An Maske/Haubenseite (x < SEG_X1) mit Lasche zur Wand, sonst auf einer
    Konsole, die auf dem Laengstraeger (Oberkante z 520, y 200..280) steht und nach aussen unter die Leitung greift."""
    z = Z_LTG
    y = s * Y_LTG
    t.append(ring_x(x, y, z, r + 8, r - 0.5, 26))
    if x < SEG_X1:
        yw = 355.0 if x < 210 else Y_HAUBE                       # Maskenseite / Haubenseite aussen
        ya, yb = sorted((s * (yw - 2.4), s * (Y_LTG - r + 4)))
        t.append(box(x - 15, x + 15, ya, yb, z - 16, z + 16))
        t.mat("schwarz", sechskant((x, s * (Y_LTG - r + 4), z), (0, s, 0), 12, 5))
    else:
        ya, yb = sorted((s * 262.0, s * Y_LTG))
        t.append(box(x - 18, x + 18, ya, yb, 520.0, z - r + 2))     # Konsole auf dem Obergurt des Laengstraegers (Oberkante z 520)
        t.mat("schwarz", sechskant((x, s * 330.0, z - r + 2), (0, 0, 1), 12, 5))


def ventil(t):
    """Steuerventil (Foto 40431489714, c_sr_box; 26271221407 / 39333958410 zeigen den Block nicht): kompakter, hoher Gusskoerper
    (~ 140 x 140 x 170, olivgruen = Anbaulack) auf einer Grundplatte direkt auf dem rechten Endkasten, ueber dem Zylindereintritt,
    mit Gussabsatz oben, seitlicher runder Kappe + Handrad, Anschlussstutzen. Hebel: kurzer senkrechter Hebel mit Kugel Ø 40 und
    daneben eine lange duenne Stange (Ø 20, ~ 450, 28 Grad nach vorn geneigt) mit kleinem Knopf. Zwei Rohre vorn senkrecht nach
    unten auf den Kasten (zu den Zylinder-Rohren), Schlauchanschluesse innen, zwei Leitungen nach hinten in die Querrohre."""
    zt = EK_Z1
    x0, x1, y0, y1 = VB_X0, VB_X1, VB_Y0, VB_Y1
    xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
    # Grundplatte mit 4 Schrauben
    t.append(box(x0 - 12, x1 + 12, y0 - 12, y1 + 12, zt - 1, VB_Z0))
    t += [sechskant((x, y, VB_Z0), (0, 0, 1), 16, 7) for x in (x0 - 3, x1 + 3) for y in (y0 - 3, y1 + 3)]
    # Gusskoerper mit Absaetzen
    t.append(kasten_rund(x0, x1, y0, y1, VB_Z0, VB_Z0 + 100, 14, Axis.Z))
    t.append(kasten_rund(x0 + 14, x1 - 14, y0 + 14, y1 - 14, VB_Z0 + 100, VB_Z1 - 8, 10, Axis.Z))
    t.append(kasten_rund(x0 + 30, x1 - 30, y0 + 30, y1 - 30, VB_Z1 - 8, VB_Z1, 8, Axis.Z))
    for z_ in (VB_Z0 + 100,):
        t.append(box(x0 - 3, x1 + 3, y0 - 3, y1 + 3, z_ - 6, z_ + 4))                                        # umlaufender Gussabsatz
    t += [sechskant((x, y, VB_Z1), (0, 0, 1), 14, 6) for x in (x0 + 38, x1 - 38) for y in (y0 + 38, y1 - 38)]
    # seitliche runde Kappe + Handrad innen (-y)
    zc = VB_Z0 + 55
    t.append(rad_y(xm - 10, y0 - 16, zc, 36, 32))
    t.mat("blank", rad_y(xm - 10, y0 - 40, zc, 8, 20))
    t.mat("schwarz", rad_y(xm - 10, y0 - 52, zc, 38, 6))                                                       # Handrad
    t += [sechskant((xm - 10 + dx, y0 - 30, zc + dz), (0, -1, 0), 12, 5) for dx in (-24, 24) for dz in (-24, 24)]
    # Anschlussstutzen: innen (Schlaeuche) und vorn (Rohre nach unten)
    for xx in (XH_P, XH_R):
        t.mat("blank", stab((xx, y0 + 2, Z_PORT), (xx, y0 - 14, Z_PORT), 14))
        t.mat("blank", sechskant((xx, y0 - 14, Z_PORT), (0, -1, 0), 30, 12))
    for yy in (ym - 40, ym + 40):
        t.mat("blank", stab((x0 + 2, yy, VB_Z0 + 70), (x0 - 10, yy, VB_Z0 + 70), 16))
        t.append(rohr_glatt([(x0 - 8, yy, VB_Z0 + 70), (EK_X0 + 25, yy, VB_Z0 + 70), (EK_X0 + 25, yy, EK_Z1 + 2)], 11.0, 24))
        t.append(ring_x(EK_X0 + 25, yy, EK_Z1 + 8, 20, 10, 4) if False else box(EK_X0 + 25 - 20, EK_X0 + 25 + 20, yy - 20, yy + 20, EK_Z1 - 1, EK_Z1 + 8))
    # Hebel 1: kurzer senkrechter Hebel mit Kugel Ø 40 (Foto: ~ 80..150 ueber dem Block), Lagerbock
    xk, yk = x1 - 40, y0 + 45
    t.append(Pos(xk, yk, VB_Z1 + 9) * Cylinder(20, 18))
    t.mat("blank", stab((xk, yk, VB_Z1 + 10), (xk, yk, VB_Z1 + 170), 8))
    t.mat("schwarz", Pos(xk, yk, VB_Z1 + 170 + 14) * Sphere(20))
    # Hebel 2: lange duenne Stange Ø 20, 28 Grad nach vorn (-x) geneigt, kleiner Knopf
    xl, yl = x1 - 40, y1 - 40
    a = math.radians(28)
    L = 450.0
    t.append(Pos(xl, yl, VB_Z1 + 9) * Cylinder(20, 18))
    p0 = (xl, yl, VB_Z1 + 10)
    p1 = (xl - L * math.sin(a), yl, VB_Z1 + 10 + L * math.cos(a))
    t.mat("blank", stab(p0, p1, 10))
    t.mat("schwarz", Pos(*p1) * Sphere(14))
    # Leitungen nach hinten in die Querrohre
    rr = R_QL - 3
    t.append(rohr_glatt([(x1 + 14, 1018.0, 1235.0), (X_QL - 4, 1018.0, 1235.0)], rr, 25))      # -> Querrohr (Stangenseite)
    t.append(rohr_glatt([(x1 + 14, 975.0, 1205.0), (BG_X1, 975.0, 1205.0), (BG_X1, 920.0, 1205.0),
                         (BG_X1, 920.0, BG_Z - 12)], rr, 25))                                  # -> Buegelrohr (Kolbenseite)


def leitungen(t):
    """Hydraulikkreis (Fotos Flickr 7826381704 (FRISCH-Anbau, anderes Exemplar, Details abweichend), 26271249857, 40431531504, 39333958410, 40431489714, 39334013090,
    26271221407; Verdecktes plausibel):
      * Pumpe -> je Seite EINE dicke Leitung (Ø 36): um die Maskenecke, schraeg an der Haubenseite nach hinten,
        hinter dem Unterbau herunter auf Plattformhoehe und AM BODEN (z 885, |y| 440, Standschellen) nach hinten.
      * Rechts: Foerderleitung bis x 2250, dann schwarzer Schlauch (f7826) ueber den Werkzeugkasten zum Steuerblock oben auf
        dem rechten Endkasten. Links: Saugleitung in die Vorderwand des Oeltanks (Querträger).
      * Steuerblock -> zwei Leitungen auf die zwei parallelen Querrohre ueber der Traverse (Stangenseite z Z_QL,
        Kolbenseite im Buegelrohr z BG_Z) = Querverbindung zu beiden Zylindern; Rueckleitung in den Tank.
      * Zylinder: oberes duenne Rohr = Stangenseite (Kopf -> Endkasten), Kolbenseite ueber die Buegelschlaufe in den Kasten,
        unteres Rohr = Leckoelleitung des Kopfes (gedeutet)."""
    for s in (-1, 1):
        pts = [(PU_XPORT, s * 104, PU_ZPORT), (PU_XPORT, s * 300, PU_ZPORT), (-35.0, s * Y_LTG, Z_LTG),
               (LTG_HINTEN[0], s * Y_LTG, LTG_HINTEN[1]),
               (X_LTG_AB, s * Y_LTG, Z_HINT), (X_LTG_AB + 110, s * Y_LTG, Z_HINT), (X_LTG_AB + 210, s * Y_HINT, Z_HINT)]
        if s == 1:
            pts += [(X_SCHLAUCH, s * Y_HINT, Z_HINT)]
        else:
            pts += [(2540.0, s * Y_HINT, Z_HINT), (2590.0, s * Y_HINT, Z_HINT + 75), (QT_X0 + 4, s * Y_HINT, Z_HINT + 75)]
        t.append(rohr_glatt(pts, R_LTG, 70))
        for x in (100.0, 290.0, 470.0, 815.0):
            _schelle_haube(t, x, s, R_LTG)
        for x in (1800.0, 2000.0, 2200.0) if s == 1 else (1800.0, 2000.0, 2200.0, 2450.0):
            schelle_x(t, x, s * Y_HINT, Z_HINT, R_LTG, DECK_Z - 0.3)
    # zwei schwarze Schlaeuche rechts (f7826): Druck (Plattform -> ueber die Werkzeugkaesten -> Steuerblock) und Ruecklauf
    # (Steuerblock -> Plattform -> Rohr in die Tankvorderwand); beide laufen parallel
    t.mat("gummi", rohr_glatt([(X_SCHLAUCH - 6, Y_HINT, Z_HINT), (2300.0, Y_HINT, Z_HINT), (2300.0, Y_HINT, 1085.0),
                               (2300.0, 862.0, 1085.0), (XH_P, 862.0, 1085.0), (XH_P, 862.0, Z_PORT),
                               (XH_P, VB_Y0 - 22, Z_PORT)], 13.0, 45))
    t.mat("gummi", rohr_glatt([(XH_R, VB_Y0 - 22, Z_PORT), (XH_R, 830.0, Z_PORT), (XH_R, 830.0, 1092.0),
                               (2335.0, 830.0, 1092.0), (2335.0, 500.0, 1092.0), (2335.0, 500.0, Z_HINT + 14)], 13.0, 45))
    t.append(ring_x(X_SCHLAUCH, Y_HINT, Z_HINT, R_LTG + 6, R_LTG - 0.5, 14))                  # Uebergang Rohr/Schlauch
    t.append(rad_x(X_SCHLAUCH + 12, Y_HINT, Z_HINT, R_LTG + 4, 14))
    t.append(rohr_glatt([(2335.0, 500.0, Z_HINT), (2540.0, 500.0, Z_HINT), (2590.0, 500.0, Z_HINT + 75),
                         (QT_X0 + 4, 500.0, Z_HINT + 75)], R_LTG, 70))                         # Ruecklaufrohr in den Tank
    t.append(Pos(2335.0, 500.0, Z_HINT + 22) * Cylinder(R_LTG + 5, 14))                                 # Uebergang Schlauch/Rohr
    for x in (2420.0, 2520.0):
        schelle_x(t, x, 500.0, Z_HINT, R_LTG, DECK_Z - 0.3)


# ---------------- Gesamt ----------------
def planierschild():
    t = Sammler("anbau")
    schild(t)
    for s in (-1, 1):
        schubbalken(t, s)
        fuehrungsplatte(t, s)
        gelenkbock(t, s)
        abock(t, s)
        hubzylinder(t, s)
    traverse(t)
    schutzbuegel(t)
    oelpumpe(t)
    ventil(t)
    leitungen(t)
    return t
