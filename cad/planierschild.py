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
  Video-Umbau 2026-10: Gelenk x 1860 (vorher 2250), Schildlippe -800 (vorher -700), Balken hinten 170 / vorn 230 hoch.

Umbau 2026-10-12 nach Review (Video zLWVF2nmQDY, Frames 008-012, 019-030, 043-048, 160-176, 194-200):
  * Schild neu: gewoelbtes Blech mit flach umgekanteter Oberkante (kein Rundwulst), dahinter waagerechter Quertraeger
    und EINE stehende Rechteckplatte (~1000 breit, Oberkante z 1040, 2 Loecher, Knotenbleche an den Enden) statt Kastendeck
    mit 4 U-Gabeln; schmale sichelfoermige Endbleche; Schubbalken ueber ein Zahnsegment (Neigungsverstellung) angelenkt;
    offener Rahmen zum Fahrzeug (Diagonalarm vom Schubbalken + Strebe zum Knoten unter der Pumpe).
  * Schubbalken: aufgeschweisste Spitzplatten im vorderen Drittel, hinteres Ende schraeg, runde Lagernabe statt Vierkantblock.
  * Leitung je Seite im Bogen hoch durch das obere Drittel des Motorausschnitts zum Zylinderkopf (statt flach auf z 560).
  * Zylinderkopf rund (~1,2 x Rohr-Ø), unteres Rohr tief unter dem Zylinder; Langloch in der Schraege beider Endkaesten,
    Schild "Frisch" mittig, Arbeitsscheinwerfer hinten links.

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
    40431531504), seitlich je ein Anschluss etwas unter der Achse. JE SEITE NUR EINE LEITUNG (Ø ~36), siehe leitungen().
    Kein Gestaenge an der Haubenseite, kein Ventilblock auf der Pumpe. Steuerblock auf dem rechten Endkasten (ventil(),
    Lage noch offen). Traverse: Rueckwand durchgehend (Quertraeger buendig mit den Endkaesten), Einfuellstutzen Ø ~115 mit
    roter Kappe (26271221407); Querrohre ueber der Traverse bei z 1240/1295.
  * Fuehrungsplatte mit Steckbolzen auf dem Schubbalken kurz hinter dem Leitrad (FL).

Hubkinematik (Arbeitsstellung = Schneide auf dem Boden, Schubbalken waagerecht), Stand nach Video-Auswertung 2026-10:
  Gelenk G = (1860, 400) (Lagerkappe ~ 390 vor der Triebradachse, Video v.mp4 t=164/166 und Foto 40431489714),
  Scheitel S = (1270, 1080), Zapfen Z = (2520, 1080), Schneide P = (-800, 0).
  Schild 1120 hoch: Schubbalken dreht um G um 24,1 Grad -> S' = (1599, 1262), |S'Z| = 939 (Zylinder 11 Grad geneigt).
  Arbeitsstellung: |SZ| = 1250.   Schild 200 tief: 4,3 Grad -> S'' = (1220, 1033), |S''Z| = 1301.
  -> Hub 1301 - 939 = 362 mm (aus der Arbeitsstellung 311 ein / 51 aus). Der Hub am Schild (1320) ist durch den kuerzeren
  Hebel (Scheitel 900 vom Gelenk) groesser als vorher (315). Hubwerte ungeprueft gegen das Original (im Video wird nicht gehoben).
  Kopf X_KOPF 1770: eingefahren steht der Gabelkopf (124 lang) bei 1599 + 124 = 1723, ~ 47 mm vor dem Abstreifer.
  Rohrende im Endkasten X_BODEN 2640 (120 hinter dem Zapfen, bleibt hinter dem Langloch der Schraege im Kasten): bei +11 Grad
  senkt sich der Boden um ~ 23. Kolbenstangenlaenge ab Auge 570..1080 moeglich (Kolben im Rohr).
  Balken (Video, Ueberlagerung ueber Leit-/Triebradnabe, Massstab 2,29 mm/px): hinten (x > 560) 170 hoch, vorn 230, Schraegubergang
  bei x 450..560, Balkenende vorn bei x -575 am Zahnsegment.

Alle Masse Original-mm, X nach hinten, Y nach rechts, Z ab Boden.
Gezeichnet in Arbeitsstellung (Schneide auf der Fahrebene).
"""
import math
from build123d import *
from .common import (box, stab, rohr_glatt, balken, rad_x, rad_y, ring_x, ring_y, sechskant,
                     schraube, schraubenreihe, schraubenkreis, kasten_rund, Sammler,
                     Y_SCHUB, Z_SCHUB, DECK_X0, DECK_X1, TRAVERSE_X, TRAVERSE_Z, ABOCK_SCHEITEL,
                     ABOCK_FUESSE, X_TRIEB, X_LEIT, DECK_Z, PUMPE, Y_LTG, HAUBE_X1, HAUBE_B,
                     HAUBE_BAND_Z, TANK_X1, MASKE_UK, SCHEINWERFER, SEG_X1, HAUBE_X0)

# ---------------- Parameter ----------------
# Schild
SCHILD_B, SCHILD_H = 2200.0, 760.0     # Breite 2150..2200 (Fotos 7826381704/39333958410: Balken buendig am Seitenblech)
X_SCHNEIDE = -800.0           # Vorderkante Schneide (Video v.mp4 t=166 und 196/047: Schildfront ~ 800 vor der Maske)
T_BLECH = 16.0                # Schildblech (2 mm im Modell)
T_RIPPE = 16.0                # Endblech
Y_WANGE = SCHILD_B / 2 - T_RIPPE       # Innenseite Endblech
Z_SCHN = 165.0                # Hoehe der Schneidleiste
Z_LOCH = 420.0                # Bohrungsreihe im Schildblech (Video 196/047)
QT_SZ0, QT_SX1 = 590.0, -560.0         # Quertraeger hinter der Oberkante: Unterkante z, Rueckwand x (Video 165)
PL_X = -650.0                 # stehende Platte (Vorderseite x), 20 dick, auf dem Quertraeger
PL_Y0, PL_Y1 = -675.0, 225.0  # ~ 900 breit, Mitte y -225 (Video 047: -594..268, Video 196: -704..132 aus Anteilen der Schildbreite; +-100)
PL_Z1 = 1040.0                # Oberkante der Platte (Video 047/048: ~ 280 ueber der Schildkante)
Y_BOCK = 780.0                # Anlenkboecke des offenen Rahmens am Blechruecken (Video 172: Ecke kurz innen vor dem Endblech)
Z_RAHMEN = 380.0              # Hoehe der Rahmenarme (unter der Pumpe, Pumpe unten z 455)
X_ARM_SB = 60.0               # Diagonalarm trifft den Schubbalken innen (vor der Kettennase)
X_KNOTEN = -110.0             # Knoten der beiden Streben unter der Pumpe (Video 008/170/172)
# Schubbalken: hinten hoher flacher Kasten 120 x 250, ab x 700 nach vorn verjuengt auf 130 (Foto 40431489714)
SB_B, SB_H = 120.0, 170.0     # Video t=164/158: hinterer Balkenteil niedrig (~150..180), vorn hoeher (~230) mit abgeschraegtem Uebergang
SB_Z0, SB_Z1 = Z_SCHUB - SB_H / 2, Z_SCHUB + SB_H / 2       # hinten 275 / 525
SB_XV = 560.0                 # ab hier nach hinten volle Hoehe, davor Verjuengung
SB_H_VORN = 230.0             # Hoehe am vorderen Teil (x < SB_XV - 110)
X_GELENK = 1860.0             # hinteres Gelenk: Video t=164/158 und Foto 40431489714: Lagerkappe ~ 390 VOR der Triebradachse (vorher 2250)
X_SCHILDBOLZEN = -575.0       # Balkenende vorn am Zahnsegment (Video 008/165: Balken endet direkt hinter dem Endblech)
X_STUFE0, X_STUFE1 = -160.0, 260.0      # aufgeschweisste Spitzplatten aussen am Balken (Video 022/165)
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
X_BODEN = 2640.0              # Zylinderboden-Flansch (im Endkasten, vor dem Langloch der Schraege; vorher 2740 = runder Deckel auf der Schraege)
R_KOPF = 60.0                 # runder Zylinderkopf ~ 1,2 x Rohr-Ø (Video 079..088)
Z_ZYL_U = Z_ZYL - 125.0       # unteres Zylinderrohr laeuft tief unter dem Zylinder (Video 087)
GABEL_L = 124.0               # Gabelkopf ab Scheitelauge bis Kontermutter
# Traverse: Endkaesten aussen, Quertraeger (Oeltank) hinten oben
EK_X0, EK_X1 = 2395.0, 2830.0
EK_Z0, EK_Z1 = 900.0, 1170.0   # 270 hoch (Seitenfotos 240..290)
Z_AUSS_O = EK_Z1 - 18.0         # Oberkante des Kastenausschnitts (Rest oben 18 mm, Verrundung 14)
Z_AUSS = 995.0               # Unterkante des Kastenausschnitts (Zylinder + untere Leitung)
EK_SCHR_DX, EK_SCHR_DY = 120.0, 190.0  # abgeschraegte hintere Aussenecke, beidseitig, ganze Kastenhoehe (Nutzerhinweis, c_ende_l; Rueckwand gerade bis |y| 880)
LL_L, LL_H = 200.0, 110.0     # Langloch in der Schraegflaeche beider Endkaesten (vorher eins rechts in der Rueckwand bei y 730)
Y_FRISCH = 0.0                # Schild "Frisch" mittig in der Rueckwand (vorher y -230)
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
# Arbeitsscheinwerfer hinten links auf dem Endkasten (Video 145/116/158)
SW_XY = (2735.0, -935.0)
SW_R = 75.0
# Oelpumpe vor dem Maskensockel (runde Zahnradpumpe, Fotos 26271249857 / 40431531504 / 40431489714)
PU_X, PU_Y, PU_Z = PUMPE
PU_R = 75.0                   # Gehaeuse Ø 150 (BS: 140 hoch, vorn: ~160)
PU_PL = 2.4                   # Frontplatte 2,4 mm in den Maskensockel (x = 0) eingesenkt
PU_XV, PU_XH = -225.0, -60.0  # Gehaeuse vorn / hinten (BS: Pumpenkoerper x -60 .. -220)
PU_XPORT, PU_ZPORT = -105.0, PU_Z - 40.0   # Anschluss seitlich, etwas unter der Achse
# Leitungen: je Seite EINE Leitung (Fotos), Ø ~ 36; schraeger Teil beginnt an der Maskenecke bei (LTG_X0, LTG_Z0)
R_LTG, R_ZYLLTG = 18.0, 11.0
LTG_X0, LTG_Z0 = -10.0, 580.0
Y_HAUBE = HAUBE_B / 2         # Haubenseite aussen (345)
# Leitung je Seite (Video 010, 043..078, 165, 172, 196; Flickr 39333958410/40431531504): von der Pumpe um die Maskenecke,
# im Bogen schraeg hoch ueber das vordere Seitensegment, ab x ~ 470 waagerecht durch das obere Drittel des Motorausschnitts
# (Oberkante 1125), hinter der Haube nach aussen zum Zylinderkopf
Z_LTG = 1040.0                # waagerechter Teil (Video 172: ~ 70 unter der Ausschnitt-Oberkante 1125)
X_LTG_KNICK = 470.0           # Uebergang schraeg -> waagerecht
X_LTG_AB = 1405.0             # T-Stueck: Abzweig hinunter auf die Plattform (Bodenleitung zum Steuerblock, Deutung)
Z_LTG_KOPF = 1100.0           # Anschluss am Zylinderkopf (innen)
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
# Neuaufbau 2026-10-12 nach Video (Frames 008/010/047/165/170/172/196): gewoelbtes Schildblech mit flach umgekanteter
# Oberkante, dahinter ein waagerechter Quertraeger mit EINER stehenden Rechteckplatte (Knotenbleche an den Enden),
# schmale sichelfoermige Endbleche, Schubbalken ueber ein Zahnsegment angelenkt, offener Rahmen zum Fahrzeug
# (je Seite Diagonalarm vom Schubbalken und Strebe zum Knoten unter der Pumpe).
def _bogen(p0, p1, sag, n):
    """Kreisbogen von p0 nach p1 (x, z) mit Pfeilhoehe sag (Bogen nach +x ausgebeult), n Teilstuecke."""
    (x0, z0), (x1, z1) = p0, p1
    c = math.hypot(x1 - x0, z1 - z0)
    R = (c * c / 4 + sag * sag) / (2 * sag)
    ux, uz = (x1 - x0) / c, (z1 - z0) / c
    nx, nz = uz, -ux                                   # Normale zur Sehne
    if nx < 0:
        nx, nz = -nx, -nz                              # zeigt nach +x (Ausbeulung nach hinten)
    mx, mz = (x0 + x1) / 2, (z0 + z1) / 2
    cx, cz = mx - nx * (R - sag), mz - nz * (R - sag)
    a0, a1 = math.atan2(z0 - cz, x0 - cx), math.atan2(z1 - cz, x1 - cx)
    if a1 - a0 > math.pi:
        a1 -= 2 * math.pi
    if a0 - a1 > math.pi:
        a1 += 2 * math.pi
    return [(cx + R * math.cos(a0 + (a1 - a0) * i / n), cz + R * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _profil():
    """Vorderkontur F und Rueckkontur B des Schildblechs als (x, z)-Listen (unten -> oben).
    Unten ein gerades, leicht nach vorn gestelltes Stueck hinter der Schneide, dann der Kreisbogen (Pfeilhoehe 135),
    oben nach vorn ausgerollt (Video 196/047: Oberkante steht vor der Schneide)."""
    F = [(X_SCHNEIDE + 18, 0.0), (X_SCHNEIDE + 38, Z_SCHN)]
    F += _bogen((X_SCHNEIDE + 38, Z_SCHN), (X_SCHNEIDE - 4, SCHILD_H - 16), 135.0, 24)[1:]
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


def _x_auf(P, z):
    """x einer Kontur (Liste (x, z), z steigend) auf Hoehe z."""
    for (x0, z0), (x1, z1) in zip(P, P[1:]):
        if min(z0, z1) <= z <= max(z0, z1) and abs(z1 - z0) > 1e-9:
            return x0 + (x1 - x0) * (z - z0) / (z1 - z0)
    return P[-1][0] if z > P[-1][1] else P[0][0]


def _zug(B, za, zb, n=8):
    """Rueckkontur zwischen za und zb als Punktliste."""
    return [(_x_auf(B, za + (zb - za) * i / n), za + (zb - za) * i / n) for i in range(n + 1)]


def schild(t):
    F, B = _profil()
    # Schildblech (gewoelbt): Ruecken lackiert wie der Anbau (Video 165), Front blank (eigene Haut 5 mm, Video 047/196)
    F5 = [(x + (bx - x) * 5.0 / T_BLECH, z + (bz - z) * 5.0 / T_BLECH) for (x, z), (bx, bz) in zip(F, B)]
    blech = platte_xz(F5 + B[::-1], -Y_WANGE, Y_WANGE)
    haut = platte_xz(F + F5[::-1], -Y_WANGE, Y_WANGE)
    # Bohrungsreihe etwa in halber Hoehe (Video 196/047: ~ 8 Loecher, Ø ~ 35)
    xl_ = _x_auf(F, Z_LOCH)
    for y in (-900.0, -640.0, -380.0, -125.0, 125.0, 380.0, 640.0, 900.0):
        loch = Pos(xl_ + 10, y, Z_LOCH) * Rot(0, 90, 0) * Cylinder(17, 90)
        blech -= loch
        haut -= loch
    t.append(blech)
    t.mat("zink", haut)
    # Oberkante: flach nach hinten umgekanteter Rand (kein Rundwulst), deckt den Quertraeger ab
    xo = F[-1][0]
    t.append(platte_xz([(xo - 6, SCHILD_H - 16), (xo - 6, SCHILD_H), (QT_SX1, SCHILD_H), (QT_SX1, SCHILD_H - 14)], -Y_WANGE, Y_WANGE))
    # Schneide: eine durchgehende Leiste zwischen den Endblechen, leicht nach vorn gestellt
    # (Video 047/048/196: blank wie das Blech, keine abgesetzte Lackleiste; Senkschrauben buendig, nur angedeutet)
    t.mat("zink", platte_xz([(X_SCHNEIDE, 0.0), (X_SCHNEIDE + 19, 0.0), (X_SCHNEIDE + 39, Z_SCHN), (X_SCHNEIDE + 20, Z_SCHN)],
                            -Y_WANGE, Y_WANGE))
    n = 11
    for i in range(n):
        y = -SCHILD_B / 2 + 60 + (SCHILD_B - 120) * (i + 0.5) / n
        t.mat("blank", Pos(X_SCHNEIDE + 9, y, 85) * Rot(0, 83, 0) * Cylinder(11, 6))
    # waagerechter Quertraeger hinter der Oberkante (Video 165: gewoelbter Blechruecken, oben ein Kastentraeger)
    qz = _zug(B, QT_SZ0, SCHILD_H - 14, 8)
    t.append(platte_xz(qz + [(QT_SX1, SCHILD_H - 14), (QT_SX1, QT_SZ0 + 30), (QT_SX1 - 30, QT_SZ0)], -Y_WANGE, Y_WANGE))
    # flache Rippen am Blechruecken unter dem Quertraeger (5 Stueck)
    for y in (-760.0, -380.0, 0.0, 380.0, 760.0):
        rp = _zug(B, 120.0, QT_SZ0, 8)
        t.append(platte_xz(rp + [(x + 30 + 30 * (z - 120.0) / (QT_SZ0 - 120.0), z) for x, z in rp[::-1]], y - 7, y + 7))
    # stehende Rechteckplatte auf dem Quertraeger (Video 047/165/196: ~ 900 breit, Oberkante ~ z 1040, zwei Loecher oben)
    xp0, xp1 = PL_X, PL_X + 20
    pl_ = box(xp0, xp1, PL_Y0, PL_Y1, SCHILD_H - 2, PL_Z1)
    for yy in (PL_Y0 + 50, PL_Y1 - 50):
        pl_ -= Pos((xp0 + xp1) / 2, yy, PL_Z1 - 50) * Rot(0, 90, 0) * Cylinder(24, 40)
    t.append(pl_)
    for yy in (PL_Y0, PL_Y1 - 16):                     # dreieckige Knotenbleche an beiden Enden, vorn und hinten
        t.append(platte_xz([(xp1 - 1, SCHILD_H - 2), (QT_SX1 - 4, SCHILD_H - 2), (xp1 - 1, SCHILD_H + 175)], yy, yy + 16))
        t.append(platte_xz([(xp0 + 1, SCHILD_H - 2), (xp0 - 75, SCHILD_H - 2), (xp0 + 1, SCHILD_H + 120)], yy, yy + 16))
    t += [sechskant((xp1, yy, SCHILD_H + 40), (1, 0, 0), 20, 7) for yy in (PL_Y0 + 200, (PL_Y0 + PL_Y1) / 2, PL_Y1 - 200)]
    # schmale sichelfoermige Endbleche: folgen der Blechkruemmung (vorn konkav), wenig hinter den Blechruecken ragend
    vorn = [(x - 6, z) for x, z in F]
    vorn[0] = (X_SCHNEIDE + 12, 0.0)
    hinten = [(_x_auf(B, z) + 32, z) for z in (0.0, 120.0, 250.0, 380.0, 470.0)]
    hinten += [(_x_auf(B, 540.0) + 75, 540.0), (QT_SX1 + 8, QT_SZ0 + 40), (QT_SX1 + 8, SCHILD_H - 40), (QT_SX1 - 20, SCHILD_H + 6),
               (xo + 30, SCHILD_H + 12)]
    sichel = vorn + hinten[::-1]
    for s in (-1, 1):
        t.append(platte_xz(sichel, s * Y_WANGE, s * (SCHILD_B / 2)))
        for z in (110.0, 300.0, 480.0, 660.0):           # einzelne Schrauben entlang der Sichel
            xm_ = (_x_auf(F, z) + _x_auf(B, z) + 32) / 2 + (60 if z > 600 else 0)
            t.mat("blank", sechskant((xm_, s * SCHILD_B / 2, z), (0, s, 0), 26, 9))
    # Anschluss Schubbalken (Video 008/165/196): innen ein Anschlussbock am Blechruecken vor dem Balkenende, aussen zwischen
    # Balken und Endblech das senkrechte Zahnsegment (Neigungsverstellung) mit Zaehnen nach hinten, mittig die Gelenkzunge
    for s in (-1, 1):
        y = s * Y_SCHUB
        zs0, zs1 = Z_SCHUB - 175, Z_SCHUB + 175
        t.append(platte_xz(_zug(B, Z_SCHUB - 130, Z_SCHUB + 130, 6) + [(X_SCHILDBOLZEN - 2, Z_SCHUB + 100), (X_SCHILDBOLZEN - 2, Z_SCHUB - 100)],
                           y - 45, y + 45))
        ya_, yb_ = s * (Y_SCHUB + SB_B / 2 + 1), s * (Y_WANGE + 1)
        xz = X_SCHILDBOLZEN + 4                               # Zahngrund
        seg = _zug(B, zs0, zs1, 8) + [(xz, zs1), (xz, Z_SCHUB + 62), (X_SCHILDBOLZEN + 80, Z_SCHUB + 45),
                                       (X_SCHILDBOLZEN + 80, Z_SCHUB - 45), (xz, Z_SCHUB - 62), (xz, zs0)]
        t.append(platte_xz(seg, ya_, yb_))
        for zc in [zs0 + 16 + i * 32 for i in range(4)] + [zs1 - 16 - i * 32 for i in range(4)]:   # Zaehne
            t.append(platte_xz([(xz - 1, zc - 14), (xz + 22, zc - 6), (xz + 22, zc + 6), (xz - 1, zc + 14)], ya_, yb_))
        bolzen_y(t, X_SCHILDBOLZEN + 45, s * (Y_WANGE + 2), s * (Y_SCHUB - SB_B / 2 - 6), Z_SCHUB, 20, kopf=False)
        t.mat("blank", sechskant((X_SCHILDBOLZEN + 45, s * (Y_WANGE + 1), Z_SCHUB), (0, s, 0), 46, 14))
        # Klinke am Balkenende greift in das Segment
        t.append(box(X_SCHILDBOLZEN + 20, X_SCHILDBOLZEN + 85, *sorted((s * (Y_SCHUB + SB_B / 2 - 2), s * (Y_SCHUB + SB_B / 2 + 16))),
                     Z_SCHUB + 70, Z_SCHUB + 120))
    # offener Rahmen zwischen Schild und Fahrzeug (Video 008/165/170/172): je Seite ein Anlenkbock am Blechruecken,
    # Diagonalarm schraeg nach hinten aussen an den Schubbalken und Strebe nach hinten innen zum Knoten unter der Pumpe
    for s in (-1, 1):
        yb = s * Y_BOCK
        xb = _x_auf(B, Z_RAHMEN)
        for dy in (-55, 55):
            t.append(platte_xz([(xb - 2, Z_RAHMEN - 85), (xb + 150, Z_RAHMEN - 70), (xb + 150, Z_RAHMEN + 70), (xb - 2, Z_RAHMEN + 85)],
                               yb + dy - 10, yb + dy + 10))
        t.mat("blank", Pos(xb + 105, yb, Z_RAHMEN) * Cylinder(20, 150))                       # senkrechter Bolzen
        t.mat("blank", Pos(xb + 105, yb, Z_RAHMEN + 77) * Cylinder(30, 8))
        t.append(balken((xb + 105, yb, Z_RAHMEN), (X_ARM_SB, s * (Y_SCHUB - SB_B / 2 + 8), Z_RAHMEN), 90, 110))
        t.append(balken((xb + 105, yb, Z_RAHMEN), (X_KNOTEN, s * 60, Z_RAHMEN), 80, 90))
    # Knoten unter der Pumpe: zwei waagerechte Knotenbleche und Nabe
    kn = [(X_KNOTEN - 110, 0.0), (X_KNOTEN + 70, -150.0), (X_KNOTEN + 70, 150.0)]
    for zz in (Z_RAHMEN + 43, Z_RAHMEN - 55):
        t.append(extrude(Plane.XY.offset(zz) * Polygon(*kn, align=None), amount=12))
    t.append(Pos(X_KNOTEN, 0, Z_RAHMEN) * Cylinder(62, 110))
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
    xa = X_SCHILDBOLZEN
    xe_o, xe_u = X_GELENK + 85.0, X_GELENK - 15.0          # hinteres Ende schraeg abgeschnitten (Video 010/022)
    xs = [xa, SB_XV - 110.0, SB_XV]
    # Kasten: vorn hoeher, Schraegubergang, hinten niedrig; Polygonplatte
    t.append(platte_xz([(x, sb_top(x)) for x in xs] + [(xe_o, sb_top(xe_o)), (xe_u, sb_bot(xe_u))] +
                       [(x, sb_bot(x)) for x in xs[::-1]], yi, ya))
    # Gurtbleche (Obergurt / Untergurt) folgen dem Profil
    xg = [X_SCHILDBOLZEN + 40, SB_XV - 110.0, SB_XV]
    t.append(platte_xz([(x, sb_top(x)) for x in xg] + [(xe_o - 10, sb_top(xe_o)), (xe_o - 14, sb_top(xe_o) - 14)] +
                       [(x, sb_top(x) - 14) for x in xg[::-1]], yi - 6, ya + 6))
    t.append(platte_xz([(x, sb_bot(x)) for x in xg] + [(xe_u - 10, sb_bot(xe_u)), (xe_u - 6, sb_bot(xe_u) + 14)] +
                       [(x, sb_bot(x) + 14) for x in xg[::-1]], yi - 6, ya + 6))
    # Stirnplatte vorn (vor dem Zahnsegment)
    t.append(box(xa - 4, xa + 12, yi - 6, ya + 6, sb_bot(xa) - 4, sb_top(xa) + 4))
    # aufgeschweisste Spitzplatten im vorderen Drittel (Video 022/165): aussen zwei Platten mit spitzen Enden uebereinander,
    # oben eine Deckplatte mit schraegen Enden -> Stufe im Balken
    zm = Z_SCHUB
    for z0, z1 in ((zm + 8, zm + 100), (zm - 100, zm - 8)):
        zc = (z0 + z1) / 2
        t.append(platte_xz([(X_STUFE0, zc), (X_STUFE0 + 70, z0), (X_STUFE1 - 70, z0), (X_STUFE1, zc), (X_STUFE1 - 70, z1), (X_STUFE0 + 70, z1)],
                           yo - s * 1, yo + s * 16))
    zt = sb_top(X_STUFE0)
    t.append(platte_xz([(X_STUFE0 + 20, zt - 1), (X_STUFE1 - 20, zt - 1), (X_STUFE1 - 60, zt + 16), (X_STUFE0 + 60, zt + 16)], yi - 6, ya + 6 + s * 10))
    # hinten: runde Lagernabe aussen am Balken mit Fettkappe (Video 165: kleine runde Kappe, kein Vierkantblock)
    t.append(rad_y(X_GELENK, yo + s * 12, Z_SCHUB, 72, 24))
    t += [sechskant((X_GELENK + 50 * math.cos(math.radians(a_)), yo + s * 24, Z_SCHUB + 50 * math.sin(math.radians(a_))), (0, s, 0), 18, 7)
          for a_ in (45, 135, 225, 315)]
    t.mat("blank", rad_y(X_GELENK, yo + s * 34, Z_SCHUB, 24, 20))                     # Fettkappe
    t.mat("blank", rad_y(X_GELENK, yo + s * 48, Z_SCHUB, 10, 10))
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
    # Stopfbuchse und runder Kopf (Video 079..088, 116: nur ~ 1,2 x Rohr-Ø, gerundet), Rohr dahinter
    t.append(rad_x(X_KOPF - 18, y, z, 34, 36))
    t.mat("schwarz", rad_x(X_KOPF - 40, y, z, 29, 10))           # Abstreifer
    kopf = rad_x(X_KOPF + 30, y, z, R_KOPF, 68)
    kopf = fillet(kopf.edges().filter_by(GeomType.CIRCLE), 12)
    t.append(kopf)
    t += schraubenkreis((X_KOPF - 4, y, z), (-1, 0, 0), R_KOPF - 16, 4, 16, 7, start=45)
    # Zylinderrohr Ø100 bis in den Endkasten
    t.append(rad_x((X_KOPF + 60 + X_BODEN) / 2, y, z, R_ZYL, X_BODEN - X_KOPF - 60))
    # Zapfenring mit Querzapfen (lagert in beiden Kastenwaenden)
    t.append(rad_x(X_ZAPFEN, y, z, R_ZYL + 10, 90))
    t.mat("blank", rad_y(X_ZAPFEN, y, z, 28, 2 * EK_DY - 2 * EK_T + 6))
    # Bodenflansch, Boden mit Schrauben (bleibt im Endkasten hinter dem Langloch der Schraege)
    t.append(rad_x(X_BODEN + 8, y, z, R_ZYL + 14, 16))
    t.append(rad_x(X_BODEN + 31, y, z, R_ZYL + 7, 30))
    t += schraubenkreis((X_BODEN + 46, y, z), (1, 0, 0), 36, 6, 14, 8, start=30)
    # zwei duenne Rohre: oben (z + 62) ueber die Zylinderlaenge in den Kasten; unten biegt das Rohr am Kopf nach unten ab
    # und laeuft tief unter dem Zylinder nach hinten (Video 087, 116) in die Vorderwand des Endkastens
    dz = 62.0
    t.append(box(X_KOPF + 15, X_KOPF + 45, y - 16, y + 16, z + R_KOPF - 8, z + dz + 8))
    t.append(rohr_glatt([(X_KOPF + 30, y, z + dz), (EK_X0 + 60, y, z + dz)], R_ZYLLTG - 2, 22))
    t.append(box(X_KOPF + 5, X_KOPF + 35, y - 16, y + 16, z - R_KOPF - 14, z - R_KOPF + 8))
    t.mat("blank", sechskant((X_KOPF + 20, y, z - R_KOPF - 14), (0, 0, -1), 26, 10))
    t.append(rohr_glatt([(X_KOPF + 20, y, z - R_KOPF - 20), (X_KOPF + 20, y, Z_ZYL_U), (EK_X0 - 6, y, Z_ZYL_U)], R_ZYLLTG - 2, 30))
    t.mat("blank", sechskant((EK_X0 - 2, y, Z_ZYL_U), (-1, 0, 0), 26, 12))          # Schottverschraubung
    for x in (2110.0, 2200.0):                                    # Sattelschellen
        t.append(box(x - 12, x + 12, y - 16, y + 16, z + R_ZYL - 6, z + dz))
        t.append(box(x - 12, x + 12, y - 16, y + 16, Z_ZYL_U, z - R_ZYL + 6))


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


def _langloch_schraege(s, y):
    """Obround-Durchbruch (LL_L x LL_H, Halbkreis-Enden) mittig in der Schraegflaeche der hinteren Aussenecke."""
    ya = y + s * EK_DY
    p1 = Vector(EK_X1 - EK_SCHR_DX, ya, 0)
    p2 = Vector(EK_X1, ya - s * EK_SCHR_DY, 0)
    d = (p2 - p1).normalized()
    n = Vector(EK_SCHR_DY, s * EK_SCHR_DX, 0).normalized()
    m = (p1 + p2) * 0.5
    pl = Plane(origin=(m.X, m.Y, (EK_Z0 + EK_Z1) / 2), x_dir=d, z_dir=n)
    return extrude(pl * SlotOverall(LL_L, LL_H), amount=60, both=True)


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
    # Langloch ~ 200 x 110 mit Halbkreis-Enden mitten in der Schraegflaeche, links und rechts (Video 090/116/145/150/158, Flickr 26271221407)
    k -= _langloch_schraege(s, y)
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
    for s_ in (-1, 1):
        qt -= _ecke_prisma(s_, s_ * Y_SCHUB, 0.0)          # Quertraeger endet buendig an der Schraegflaeche
    t.append(qt)
    # umlaufender Bodenflansch nach hinten abgekantet (~ 35 vor, ~ 45 hoch), je 2 Sechskantschrauben (c_links)
    yfl = EK_YI - 2        # endet an der Schraege (nichts steht ueber die Schraegflaeche)
    t.append(box(QT_X1 - 2, QT_X1 + 35, -yfl, yfl, QT_Z0, QT_Z0 + 45))
    for yc in (-340.0, 440.0):
        for dy in (-35, 35):
            t.mat("schwarz", sechskant((QT_X1 + 35, yc + dy, QT_Z0 + 22), (1, 0, 0), 22, 8))
    # Firmenschild "Frisch": dunkelblaue Platte, weisser Rand und weisse Blockschrift (26271221407), 410 x 215 mittig in der Rueckwand
    zs0, zs1 = zm - 90, zm + 125
    ys0, ys1 = Y_FRISCH - 205, Y_FRISCH + 205
    t.mat("bosch", box(QT_X1, QT_X1 + 6, ys0, ys1, zs0, zs1))
    for (a, b, c, d) in ((ys0, ys1, zs0, zs0 + 12), (ys0, ys1, zs1 - 12, zs1), (ys0, ys0 + 12, zs0, zs1), (ys1 - 12, ys1, zs0, zs1)):
        t.mat("zifferblatt", box(QT_X1 + 6, QT_X1 + 10, a, b, c, d))
    try:
        pl = Plane(origin=(QT_X1 + 6, Y_FRISCH, (zs0 + zs1) / 2), x_dir=(0, 1, 0), z_dir=(1, 0, 0))   # Blick von hinten: rechts = +y
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


# ---------------- Arbeitsscheinwerfer hinten links ----------------
def heckscheinwerfer(t):
    """Scheinwerfer Ø ~ 150 auf kurzem Stiel oben auf dem linken Endkasten, Glas nach hinten, Schutzgitter (Video 145, 116, 158)."""
    x, y = SW_XY
    z0 = EK_Z1
    t.append(box(x - 40, x + 40, y - 35, y + 35, z0 - 1, z0 + 10))                      # Fussplatte
    t += [sechskant((x + dx, y, z0 + 10), (0, 0, 1), 14, 6) for dx in (-26, 26)]
    t.mat("schwarz", Pos(x, y, z0 + 10) * Cylinder(12, 50, align=(Align.CENTER, Align.CENTER, Align.MIN)))   # Stiel
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
        t.mat("schwarz", box(x + 26, x + 32, y - math.sqrt(max(0.0, (SW_R - 6) ** 2 - dz * dz)), y + math.sqrt(max(0.0, (SW_R - 6) ** 2 - dz * dz)),
                             zc + dz - 3, zc + dz + 3))
    t.mat("schwarz", box(x + 26, x + 32, y - 3, y + 3, zc - SW_R + 6, zc + SW_R - 6))


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
def _ltg_z(x):
    """Hoehe der Leitungsachse auf dem schraegen / waagerechten Teil."""
    if x >= X_LTG_KNICK:
        return Z_LTG
    return LTG_Z0 + (Z_LTG - LTG_Z0) * (x - LTG_X0) / (X_LTG_KNICK - LTG_X0)


def _schelle_ltg(t, x, s, art):
    """Rohrschelle an der Leitung: 'wand' = Lasche zur Masken-/Haubenwand, 'band' = Haenger am Schriftband,
    'unterbau' = Lasche zur Tankunterbau-Wand (y 330)."""
    z = _ltg_z(x)
    y = s * Y_LTG
    d = (1.0, 0.0, 0.0) if x >= X_LTG_KNICK else (X_LTG_KNICK - LTG_X0, 0.0, Z_LTG - LTG_Z0)
    t.append(ring_dir((x, y, z), d, R_LTG + 7, R_LTG - 0.5, 22))
    if art == "wand":
        yw = 355.0 if x < HAUBE_X0 else Y_HAUBE                       # Maskenseite / Haubenseite aussen
        t.append(box(x - 14, x + 14, *sorted((s * (yw + 0.5), s * (Y_LTG - R_LTG + 2))), z - 12, z + 12))
        t.mat("schwarz", sechskant((x, s * (Y_LTG - R_LTG - 4), z + 20), (0, s, 0), 12, 5))
    elif art == "band":
        zb = HAUBE_BAND_Z + 62                                         # zwischen unterer Sicke (1145) und Dachsicke, hinter dem Schriftzug
        t.append(box(x - 14, x + 14, *sorted((s * (Y_LTG - 4), s * (Y_LTG + 4))), z + R_LTG + 5, zb + 6))
        t.append(box(x - 14, x + 14, *sorted((s * (Y_HAUBE + 0.5), s * (Y_LTG + 4))), zb - 6, zb + 6))
        t.mat("schwarz", sechskant((x, s * (Y_LTG + 4), zb), (0, s, 0), 12, 4))
    else:
        t.append(box(x - 14, x + 14, *sorted((s * 331.0, s * (Y_LTG - R_LTG + 2))), z - 12, z + 12))


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
    """Hydraulikkreis:
      * Pumpe -> je Seite EINE dicke Leitung (Ø 36), sichtbar ueber den Haubenausschnitt (Video 010, 043..078, 165, 172, 196,
        Flickr 39333958410 / 40431531504): um die Maskenecke, schraeg hoch ueber das vordere Seitensegment, ab x ~ 470 auf z 1030
        waagerecht durch das obere Drittel des Motorausschnitts, aussen an der Haubenseite (|y| 392, Haube 345), hinter der Haube
        nach aussen und leicht steigend an der Innenseite des A-Bocks vorbei zum Zylinderkopf (Anschluss innen, z 1100).
      * Abzweig (T-Stueck bei x 1405, Deutung) hinunter auf die Plattform und AM BODEN (z 885, |y| 440, Standschellen) nach hinten:
        rechts bis x 2250, dann schwarzer Schlauch zum Steuerblock auf dem rechten Endkasten (Lage des Steuerhebels wird noch
        geklaert), links in die Vorderwand des Oeltanks.
      * Zylinder: oberes duennes Rohr Kopf -> Endkasten, unteres biegt am Kopf ab und laeuft tief unter dem Zylinder nach hinten."""
    for s in (-1, 1):
        haupt = [(PU_XPORT, s * 104, PU_ZPORT), (PU_XPORT, s * 250, PU_ZPORT), (LTG_X0 - 40, s * Y_LTG, LTG_Z0 - 40),
                 (LTG_X0, s * Y_LTG, LTG_Z0), (X_LTG_KNICK, s * Y_LTG, Z_LTG), (1480.0, s * Y_LTG, Z_LTG),
                 (1630.0, s * 830, Z_LTG_KOPF), (1790.0, s * 870, Z_LTG_KOPF), (1800.0, s * 870, Z_LTG_KOPF)]
        t.append(rohr_glatt(haupt[:-1] + [(1800.0, s * (Y_SCHUB - R_KOPF + 4), Z_LTG_KOPF)], R_LTG, 75))
        nippel(t, (1800.0, s * (Y_SCHUB - R_KOPF + 4), Z_LTG_KOPF), (0, -s, 0), 34, 16)
        # T-Stueck und Abzweig auf die Plattform
        t.append(rad_x(X_LTG_AB, s * Y_LTG, Z_LTG, R_LTG + 6, 56))
        t.append(Pos(X_LTG_AB, s * Y_LTG, Z_LTG - R_LTG - 8) * Cylinder(R_LTG + 6, 24))
        ab = [(X_LTG_AB, s * Y_LTG, Z_LTG - 10), (X_LTG_AB, s * Y_LTG, Z_HINT), (X_LTG_AB + 110, s * Y_LTG, Z_HINT),
              (X_LTG_AB + 210, s * Y_HINT, Z_HINT)]
        if s == 1:
            ab += [(X_SCHLAUCH, s * Y_HINT, Z_HINT)]
        else:
            ab += [(2540.0, s * Y_HINT, Z_HINT), (2590.0, s * Y_HINT, Z_HINT + 75), (QT_X0 + 4, s * Y_HINT, Z_HINT + 75)]
        t.append(rohr_glatt(ab, R_LTG, 70))
        _schelle_ltg(t, 120.0, s, "wand")
        _schelle_ltg(t, 265.0, s, "wand")
        _schelle_ltg(t, 1010.0, s, "band")
        _schelle_ltg(t, 1250.0, s, "unterbau")
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
    heckscheinwerfer(t)
    oelpumpe(t)
    ventil(t)
    leitungen(t)
    return t
