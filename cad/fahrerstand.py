"""Tank und Fahrerstand (Original-mm, X nach hinten, Y nach rechts, Z ab Boden).

Fotobefund (eigene Fotos t39/t42/t46 des Nutzers, K 55; dazu fz_05/10/11, fz_01):
  * Tank: verzinkter Blechtank IN HAUBENFORM (keine liegende Trommel). Seitenprofil: Stirn senkrecht
    direkt hinter der Haube (x 1085), Oberseite fast in der Flucht des Haubendachs (z 1335), Unterseite
    waagerecht auf dem Unterbauflansch (z 1125). Hinten ist die Oberseite laenger als die Unterseite:
    Oberkante bis x ~1545, Unterkante bis 1455, dazwischen schraege Rueckwand, oben mit grossem Radius
    (100) in die Oberseite uebergehend. Unter dem Ueberhang sitzt das Armaturenbrett.
    Querschnitt fast haubenbreit (680, leicht bombierte Oberseite), Seiten senkrecht, obere Laengskanten R 115, Unterseite flach.
    Stirn mit umlaufender gerollter Falz/Sicke, hinten unten waagerechte Abkantung mit Schraubenreihe.
    Zwei Spannbaender quer ueber Oberseite und Seiten (bei ~14 % und ~72 % der Laenge), unten mit
    Gewindestangen/Muttern durch Knotenbleche am Auflageflansch des Unterbaus gespannt.
    Seitlich zwischen den Baendern zwei runde gewoelbte Schraubenkoepfe, oben Einfuellstutzen mit
    Fluegelmutter-Deckel, kleine Kanne, Kraftstoffhahn (Messing) unten aussen am Unterbau.
  * Tankunterbau: Blechkasten von der Plattform bis unter den Tank (Oberkante 1116), oben umlaufender,
    seitlich ueberstehender Auflageflansch (Winkelblech) auf dem der Tank nur aufliegt (abnehmbar, Tank
    gehoert zu haube_tank), Seitenwaende mit Schrauben.
  * Rote Armaturenkonsole = Rueckseite des Unterbaus UNTER dem Tankueberhang: ovale Instrumententafel
    links (Chromrand, zwei Zifferblaetter, Gluehueberwacher, Lichtschalter, Zuendschloss), rechts
    Oeldruckmesser (schwarz) ueber Thermometer (weiss), daneben Abstell-Zuggriff.
  * Lenksaeule steil (~50 Grad) aus dem Unterbau unter dem Tankueberhang, Vierspeichen-Lenkrad mit
    Hupenknopf; Handgashebel neben der Saeule.
  * Schalthebel mit Gummimanschette aus dem Bodenblech, Gruppenhebel,
    Kupplungs- und Bremspedal mit Riffel-Trittflaechen, verschraubte Bodenbleche.
Prospekt K 55 E (PK, PH = prospekt_heck):
  * Einteilige tiefe Sitzschale mit hochgezogenem Ruecken (keine getrennte Lehne),
    Lederpolster in der Schale, auf einem Mittelsockel mit Blattfeder-Arm, Mitte SITZ_X.
  * Werkzeugkaesten auf den Kotfluegeln, Batteriekasten rechts vor dem Sitz.
Ruecklicht: hinten links an der Rueckwand des schlanken Traversen-Quertraegers
  (x 2810, y -770, z 1150; Lage mit planierschild.py abgestimmt).
"""
import math
from build123d import *
from .common import (DECK_Z, TANK_X0, TANK_X1, TANK_B, TANK_Z0, TANK_Z1,
                     LENKRAD, SITZ_X, Y_TRAEGER, TRAEGER_Z1,
                     box, stab, rohr_glatt, rad_x, rad_y, ring_x,
                     schraubenreihe, kasten_rund, sechskant, Sammler)

# ---------------- Parameter ----------------
# Freiraum fuer die Kupplungsglocke des Rumpfs unter Tank und Konsole: |y| < 300, z <= 950
GLOCKE_Y, GLOCKE_Z1 = 300.0, 950.0

# Tankunterbau (Blechkasten unter dem Tank, x TANK_X0..XW0)
UNTERBAU_Y = 330.0           # Aussenkante Seitenwaende y = +-330
UNTERBAU_S = 22.0            # Wandstaerke Seitenwand (Innenseite 308 > GLOCKE_Y)
UB_Z0 = DECK_Z - 2           # Unterkante Seitenwaende (ueber dem Deck 2 mm eingesenkt)
UB_PLATTE_Z0 = GLOCKE_Z1 + 12   # Unterkante Kastenblock 962 (frei ueber der Glocke)
STUETZEN_X = (TANK_X0 + 70, TANK_X1 - 90)   # Stuetzen auf den Laengstraegern
FL_Y = 355.0                 # Auflageflansch: seitlicher Ueberstand bis |y| 355 (Hydraulikleitungen laufen ab |y| 375, alles am Tank innerhalb |y| 360)
FL_DICKE = 9.0               # Flanschblech
FL_Z0 = TANK_Z0 - FL_DICKE   # Unterkante Flansch 1116 (= Oberkante Kastenblock und Konsole)
FL_X1 = 1488.0               # Flansch endet hinten buendig mit der Konsolenrueckseite

# Armaturenkonsole: Rueckseite des Unterbaus, unter dem Tankueberhang
XW0 = TANK_X1                # Vorderseite Konsolenwand = Rueckseite Kastenblock
XK = TANK_X1 + 25            # Rueckseite = Instrumentenflaeche 1480
KONS_Z0, KONS_Z1 = UB_PLATTE_Z0, FL_Z0   # Wand 962..1116 ueber der Glocke; Beine bei |y| >= 300 bis aufs Deck
KONS_Y = UNTERBAU_Y
ZT = 1040.0                  # Mitte der Instrumententafel

# Tank in Haubenform (Seitenprofil X-Z, Querschnitt Y-Z)
TANK_XT = 1605.0             # virtuelle Ecke hinten oben; nach der Verrundung reicht die Oberseite bis x ~1535
R_T_OBEN_H, R_T_OBEN_V = 75.0, 40.0   # Radius hintere / vordere Oberkante (Seitenprofil)
R_T_UNTEN_H = 30.0           # Radius hintere Unterkante
R_QUER = 115.0               # Radius der oberen Laengskanten (Querschnitt)
Y_TANK = TANK_B / 2          # Tankseite y = +-325
X_BAND = (1150.0, 1400.0)    # Spannbaender bei ~14 % und ~72 % der Tanklaenge (hinten auf der ebenen Oberseite)
BAND_B, BAND_S = 40.0, 8.0   # Breite in x, Blechstaerke
BAND_ZE = TANK_Z0 + 42.0     # Bandende unten (Lasche)
Y_ROD = Y_TANK + 10.0        # Gewindestangen aussen neben dem Tank |y| 350 (im Flansch, FL_Y 355)
BOMB = 13.0                  # Bombierung der Oberseite (quer, Mitte gegen Seiten)
X_STUTZEN, Y_STUTZEN = 1275.0, -140.0
X_KANNE, Y_KANNE = 1275.0, 140.0
LTG_Y = UNTERBAU_Y + 15      # Kraftstoffleitung aussen an der Unterbau-Wand (|y| 345), laeuft frei durch die Flanschbohrung
X_HAHN = TANK_X1 - 150.0     # Kraftstoffhahn (zwischen den Baendern)

# Lenkung
LENK_MITTE = Vector(*LENKRAD)                  # Lenkradmitte (common.py)
LENK_FUSS = Vector(XK + 30.0, LENKRAD[1], 1062.0)   # Austritt aus dem Unterbau unter dem Tankueberhang; Saeule steigt unter ~50 Grad
R_KRANZ, R_KRANZ_Q = 207.0, 17.0      # Kranz Mitte / Querschnitt (aussen 448)
Y_HANDGAS = 120.0
Z_HANDGAS = ZT + 15                   # Drehpunkt Handgashebel
Y_GAUGE = 45.0                        # Oeldruck / Thermometer rechts neben der Ovaltafel

# Fussraum (Pedale und Hebel relativ zur Konsolenrueckseite)
PED_X0 = XK + 80             # Durchtritt der Pedalhebel im Bodenblech 1560
PED_X1 = XK + 215            # Trittflaechen 1695
SCHALT = (XK + 320, -100.0)  # Fuss Schalthebel 1800
GRUPPE = (XK + 300, 60.0)    # Fuss Gruppenhebel 1780
BODEN_X1 = 2330.0            # Ende Bodenblech (hinter dem Sitzsockel)

# Sitz: einteilige Schale (Ellipsoid, oben schraeg abgeschnitten, Ruecken hochgezogen)
SITZ_A, SITZ_C = 225.0, 305.0         # Halbachsen aussen: x/y, z
SITZ_WAND = 12.0
SITZ_ZB = DECK_Z + 190                # Unterkante Schale (aussen) 1030
SITZ_LIPPE = 95.0                     # Vorderkante ueber Schalenboden
SITZ_RUECKEN = SITZ_C + 10            # Rueckenoberkante ueber Schalenboden
SITZ_MULDE_DX = 150.0                 # tiefster Punkt der Randlinie vor der Sitzmitte
SITZ_NEIG = 6.0                       # Schale nach hinten geneigt (Grad, um den Boden)
POLSTER = 28.0                        # Polsterdicke
SOCKEL_X = SITZ_X + 100               # Mittelsockel hinter dem Getriebedeckel 2250
SOCKEL_Z1 = 972.0                     # Oberkante Sockel (Federeinspannung)

# Kaesten
WK_X0, WK_X1 = 2360.0, 2618.0         # Werkzeugkaesten hinten (vor den Traversen-Endkaesten ab 2395)
WK_Y0, WK_Y1 = 580.0, 845.0         # inkl. Deckel/Scharniere |y| < 875 (Traversen-Endkaesten ab |y| 880)
WK_Z1 = DECK_Z + 175
BAT = (1620.0, 1890.0, 585.0, 860.0)  # Batteriekasten rechts / Werkzeugkasten links vor dem Sitz: x0, x1, y0, y1
BAT_Z1 = DECK_Z + 170
GETR_DECKEL = (1960.0, 2180.0, 170.0, 845.0, 850.0)  # Rumpf: x0, x1, y+-, Oberkante, Schraubenkoepfe

# Ruecklicht an der Rueckwand der Traverse (planierschild.py: Rueckwand buendig mit den Endkaesten bei x 2830)
TRAV_HINTEN = 2830.0
RL_Y, RL_Z = -770.0, 1150.0
# Hydraulikleitungen der Planiereinrichtung: neben dem Tank |y| ~357..403 auf z ~1085, dann schraeg nach aussen zu den Zylinderkoepfen (x ~1825); nichts auf der Plattform



def _ellipsoid(c, a, b, cc):
    return Pos(*c) * scale(Sphere(1.0), by=(a, b, cc))


def _instrument(t, x, y, z, r, blatt="zifferblatt", winkel=35):
    """Rundinstrument auf einer Flaeche bei x (Blick +X): Chromring, Zifferblatt, Zeiger."""
    t.mat("chrom", ring_x(x + 6, y, z, r, r - 6, 12))
    t.mat(blatt, rad_x(x + 3, y, z, r - 5, 6))
    zeiger = "schwarz" if blatt != "schwarz" else "zifferblatt"
    t.mat(zeiger, Pos(x + 7, y, z) * Rot(winkel, 0, 0) * box(-2, 2, -3, 3, -4, r * 0.72))
    t.mat(zeiger, rad_x(x + 7, y, z, 5, 4))
    # Skalenstriche (5 Stueck, >= 4 mm)
    for k in range(5):
        a = math.radians(-60 + k * 30)
        rr = r - 12
        t.mat(zeiger, Pos(x + 7, y + rr * math.sin(a), z + rr * math.cos(a)) * Rot(-math.degrees(a), 0, 0)
              * box(-2, 2, -2.5, 2.5, -6, 6))


def _oben_rund(b, r):
    """Quader mit verrundeten oberen Laengskanten (parallel X)."""
    return fillet(b.edges().filter_by(Axis.X).group_by(Axis.Z)[-1], r)


# ---------------- Tank ----------------
def _ecke(f, x, z, r):
    """2D-Ecke bei (x, z) des in der XY-Ebene gebauten Profils verrunden."""
    return fillet([v for v in f.vertices() if abs(v.X - x) < 1e-3 and abs(v.Y - z) < 1e-3], r)


def _profil_face(g=0.0):
    """Seitenprofil des Tanks (X-Z), um g aufgedickt. Rueckwand schraeg, Oberseite laenger als Unterseite."""
    f = make_face(Polyline((TANK_X0, TANK_Z0), (TANK_X1, TANK_Z0), (TANK_XT, TANK_Z1),
                           (TANK_X0, TANK_Z1), close=True))
    f = _ecke(f, TANK_XT, TANK_Z1, R_T_OBEN_H)
    f = _ecke(f, TANK_X0, TANK_Z1, R_T_OBEN_V)
    f = _ecke(f, TANK_X1, TANK_Z0, R_T_UNTEN_H)
    face = f.faces()[0]
    if g:
        face = make_face(face.outer_wire().offset_2d(g))
    return face


def _quer_face(g=0.0):
    """Querschnitt des Tanks (Y-Z): Seiten senkrecht, obere Kanten gross verrundet, Unterseite flach.
    Unten um g NICHT aufgedickt (Schnitt mit z >= TANK_Z0 erfolgt im Aufrufer)."""
    y, zs = Y_TANK + g, TANK_Z1 - BOMB + g
    w = Wire([Edge.make_line((-y, TANK_Z0 - 20, 0), (y, TANK_Z0 - 20, 0)),
              Edge.make_line((y, TANK_Z0 - 20, 0), (y, zs, 0)),
              Edge.make_three_point_arc((y, zs, 0), (0, TANK_Z1 + g, 0), (-y, zs, 0)),
              Edge.make_line((-y, zs, 0), (-y, TANK_Z0 - 20, 0))])
    f = make_face(w)
    f = fillet([v for v in f.vertices() if v.Y > TANK_Z0 + 50], R_QUER + g)
    return f.faces()[0]


def _koerper(g, xa, xb):
    """Tankkoerper (Profilprisma geschnitten mit Querschnittsprisma), um g aufgedickt, nur x xa..xb, z >= TANK_Z0."""
    seite = extrude(Plane.XZ * _profil_face(g), amount=Y_TANK + g + 5, both=True)
    quer = extrude(Plane.YZ.offset(xa) * _quer_face(g), amount=xb - xa)
    return seite & quer & box(xa - 1, xb + 1, -Y_TANK - 20, Y_TANK + 20, TANK_Z0, TANK_Z1 + 50)


def tank():
    t = Sammler("zink")
    X0, X1, Z0, Z1 = TANK_X0, TANK_X1, TANK_Z0, TANK_Z1
    t.append(_koerper(0.0, X0, TANK_XT + 2))
    # gerollte Falz an der Stirn (breiter Wulst, endet bei x 1092 an der Rueckseite der Stirnwand: kein Keil davor) und eine zweite Sicke dahinter, umlaufend
    for xa, xb, g in ((X0, X0 + 7, 5.0), (X0 + 34, X0 + 48, 3.5), (X0 + 62, X0 + 70, 2.5)):
        # Innenflaeche 1,5 mm in den Tank gesenkt: Ueberlappung statt Beruehrung, sonst bleibt beim Triangulieren ein Haarspalt
        t.append(_koerper(g, xa, xb) - _koerper(-1.5, xa - 1, xb + 1))
    # zwei runde gewoelbte Schraubenkoepfe seitlich zwischen den Baendern (Foto t39)
    for s in (-1, 1):
        for x in (1235.0, 1315.0):
            t.mat("blank", Pos(x, s * (Y_TANK - 1.5), Z0 + 105) * Sphere(13))
    # hintere Abkantung unten (waagerechte Lippe) mit Schraubenreihe ueber dem Armaturenbrett (Foto t46)
    lip = box(X1 - 4, X1 + 22, -Y_TANK + 25, Y_TANK - 25, Z0, Z0 + 6)
    t.append(lip)
    t += schraubenreihe((X1 + 14, -Y_TANK + 55, Z0 + 5), (X1 + 14, Y_TANK - 55, Z0 + 5), 6, (0, 0, 1), 15, 5)

    # Spannbaender (lackiert) ueber Oberseite und Seiten; unten Laschen, Gewindestangen nach unten in den Flansch
    for xb in X_BAND:
        band = _koerper(BAND_S, xb - BAND_B / 2, xb + BAND_B / 2) - _koerper(-1.5, xb - BAND_B / 2 - 1, xb + BAND_B / 2 + 1)
        band = band & box(xb - 30, xb + 30, -400, 400, BAND_ZE, Z1 + 40)
        t.mat("lack", band)
        for s in (-1, 1):
            ya, yb = sorted((s * (Y_TANK + BAND_S - 2), s * (FL_Y + 4)))
            t.mat("lack", box(xb - BAND_B / 2, xb + BAND_B / 2, ya, yb, BAND_ZE - 8, BAND_ZE))     # Lasche
            t.mat("blank", Pos(xb, s * Y_ROD, Z0) * Cylinder(6, BAND_ZE + 14 - Z0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
            t.mat("blank", sechskant((xb, s * Y_ROD, BAND_ZE), (0, 0, 1), 17, 8))

    # Einfuellstutzen mit Fluegelmutter-Deckel oben
    zm1 = Z1
    zs = zm1 - 30
    t.append(Pos(X_STUTZEN, Y_STUTZEN, zs) * Cylinder(42, 62, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.append(Pos(X_STUTZEN, Y_STUTZEN, zm1 - 9) * Cylinder(56, 12, align=(Align.CENTER, Align.CENTER, Align.MIN)))  # Schweisskragen (reicht in die Bombierung)
    zd = zs + 62
    deckel = Pos(X_STUTZEN, Y_STUTZEN, zd) * Cylinder(54, 16, align=(Align.CENTER, Align.CENTER, Align.MIN))
    deckel = fillet(deckel.edges().group_by(Axis.Z)[-1], 5)
    t.append(deckel)
    t.mat("blank", Pos(X_STUTZEN, Y_STUTZEN, zd + 16) * Cylinder(16, 26, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    for s in (-1, 1):                                          # Fluegel
        fl = Pos(X_STUTZEN, Y_STUTZEN + s * 30, zd + 22) * Rot(s * -15, 0, 0) * box(-6, 6, -22, 22, -6, 22)
        t.mat("blank", fillet(fl.edges().filter_by(Axis.X).group_by(Axis.Z)[-1], 5))
    # Haltekette Deckel
    t.mat("blank", stab((X_STUTZEN + 50, Y_STUTZEN, zd + 4), (X_STUTZEN + 75, Y_STUTZEN + 20, zm1 - 15), 3))

    # kleine Kanne rechts oben (gerippter Deckel, Buegel)
    zk = zm1 - 25
    kanne = Pos(X_KANNE, Y_KANNE, zk) * Cylinder(55, 95, align=(Align.CENTER, Align.CENTER, Align.MIN))
    kanne = fillet(kanne.edges().group_by(Axis.Z)[-1], 6)
    t.append(kanne)
    for i in range(3):                                         # Rippen am Mantel
        t.append(Pos(X_KANNE, Y_KANNE, zk + 40 + i * 18) * Torus(55, 3))
    t.append(Pos(X_KANNE, Y_KANNE, zk + 95) * Cylinder(40, 14, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("blank", Pos(X_KANNE, Y_KANNE, zk + 109) * Sphere(12))
    t.mat("blank", Pos(X_KANNE, Y_KANNE, zk + 80) * Rot(90, 0, 0) * (Torus(52, 4) - box(-80, 80, -80, 0, -10, 10)))

    # Kraftstoffhahn (Messing -> blank) unten rechts am Tank, kompakt innerhalb |y| < 355
    # (aussen daneben laufen die Hydraulikleitungen), Leitung hinab durch eine Bohrung im Flansch
    xh, yh, zh = X_HAHN, Y_TANK - 6, Z0 + 42
    t.mat("blank", rad_y(xh, yh + 8, zh, 10, 16))              # Anschlussstutzen
    t.mat("blank", box(xh - 14, xh + 14, yh + 12, yh + 24, zh - 14, zh + 14))  # Hahnkoerper
    t.mat("blank", Pos(xh, yh + 18, zh + 14) * Cylinder(5, 12, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("lack", Pos(xh, yh + 18, zh + 26) * box(-30, 30, -5, 5, 0, 8))   # Knebel
    # Leitung bis auf den Flansch (Tankteil); unterhalb der Flanschbohrung geht sie im Unterbau weiter (_unterbau)
    yl = LTG_Y
    t.mat("blank", rohr_glatt([(xh, yh + 18, zh - 8), (xh, yl, zh - 20), (xh, yl, TANK_Z0 + 0.5)], 6))
    return t


# ---------------- Tankunterbau und Konsole ----------------
def _unterbau(t):
    """Blechkasten unter dem Tank: Kastenblock (frei ueber der Kupplungsglocke) mit Auflageflansch
    (Winkelblech, seitlich ueberstehend, Knotenbleche) oben, Seitenwaende bei |y| 308..330,
    je zwei Stuetzen auf die Laengstraeger. Der Tank liegt nur auf dem Flansch (abnehmbar)."""
    x0, x1 = TANK_X0, XW0
    yi = UNTERBAU_Y - UNTERBAU_S
    # Kastenblock bis unter den Flansch
    t.append(box(x0, x1, -UNTERBAU_Y, UNTERBAU_Y, UB_PLATTE_Z0, FL_Z0 + 1))
    # Kraftstoffleitung unter der Flanschbohrung aussen an der Seitenwand hinab (oberes Stueck gehoert zum Tank)
    t.mat("blank", rohr_glatt([(X_HAHN, LTG_Y, FL_Z0 - 0.5), (X_HAHN, LTG_Y, UB_PLATTE_Z0 - 12)], 6))
    t.mat("blank", box(X_HAHN - 10, X_HAHN + 10, UNTERBAU_Y - 1, LTG_Y + 6, UB_PLATTE_Z0 - 22, UB_PLATTE_Z0 - 2))
    # Auflageflansch mit Bohrungen fuer die Kraftstoffleitung (Tank-Leitung laeuft frei hindurch)
    fl = box(x0, FL_X1, -FL_Y, FL_Y, FL_Z0, TANK_Z0)
    for s in (-1, 1):
        fl = fl - Pos(X_HAHN, s * LTG_Y, FL_Z0 - 1) * Cylinder(8.5, FL_DICKE + 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
    t.append(fl)
    for s in (-1, 1):
        y0, y1 = sorted((s * yi, s * UNTERBAU_Y))
        t.append(box(x0, x1, y0, y1, UB_Z0, UB_PLATTE_Z0 + 1))
        # untere Abkantung nach aussen und Sicke (Versteifung) in der Seitenwand
        ya0, ya1 = sorted((s * (UNTERBAU_Y - 2), s * (UNTERBAU_Y + 6)))
        t.append(box(x0, x1, ya0, ya1, UB_Z0, UB_Z0 + 12))
        ys0, ys1 = sorted((s * (UNTERBAU_Y - 2), s * (UNTERBAU_Y + 4)))
        t.append(box(x0 + 60, x1 - 60, ys0, ys1, UB_Z0 + 45, UB_Z0 + 70))
        ys0, ys1 = sorted((s * (UNTERBAU_Y - 3.5), s * (UNTERBAU_Y + 1)))   # obere Sicke flach (Leitung laeuft daneben)
        t.append(box(x0 + 60, x1 - 60, ys0, ys1, UB_PLATTE_Z0 + 55, UB_PLATTE_Z0 + 80))
        # Schraubenreihen auf der Seitenwand (Aussenflaeche y = UNTERBAU_Y), 2,4 mm eingesenkt
        t += schraubenreihe((x0 + 40, s * (UNTERBAU_Y - 2.4), UB_PLATTE_Z0 + 20),
                            (x1 - 40, s * (UNTERBAU_Y - 2.4), UB_PLATTE_Z0 + 20), 5, (0, s, 0), 18, 9.4)
        t += schraubenreihe((x0 + 40, s * (UNTERBAU_Y - 2.4), UB_Z0 + 28),
                            (x1 - 40, s * (UNTERBAU_Y - 2.4), UB_Z0 + 28), 5, (0, s, 0), 18, 9.4)
        # Knotenbleche unter dem Flansch (je zwei pro Spannband) und Gewindestangen mit Muttern darunter
        for xb in X_BAND:
            for dx in (-16, 16):
                kn = Polyline((s * (UNTERBAU_Y - 1), FL_Z0 + 1), (s * (FL_Y - 3), FL_Z0 + 1),
                              (s * (UNTERBAU_Y - 1), FL_Z0 - 34), close=True)
                t.append(extrude(Plane.YZ.offset(xb + dx - 3) * make_face(kn), amount=6))
            t.mat("blank", Pos(xb, s * Y_ROD, FL_Z0 - 30) * Cylinder(6, 32, align=(Align.CENTER, Align.CENTER, Align.MIN)))
            t.mat("blank", sechskant((xb, s * Y_ROD, FL_Z0), (0, 0, -1), 17, 8))
            t.mat("blank", sechskant((xb, s * Y_ROD, FL_Z0 - 8), (0, 0, -1), 17, 8))
        # Stuetzen: Flachstahl aussen neben der Glocke, Fussplatte auf dem Laengstraeger-Obergurt
        yf0, yf1 = sorted((s * GLOCKE_Y, s * (GLOCKE_Y + 22)))
        yp0, yp1 = sorted((s * (Y_TRAEGER + 22), s * (UNTERBAU_Y)))
        for xs in STUETZEN_X:
            t.append(box(xs - 30, xs + 30, yf0, yf1, TRAEGER_Z1 - 2, UB_Z0 + 14))
            t.append(box(xs - 45, xs + 45, yp0, yp1, TRAEGER_Z1 - 2, TRAEGER_Z1 + 12))
            # Knotenblech Stuetze -> Fussplatte (aussen)
            kn = Polyline((s * (GLOCKE_Y + 20), TRAEGER_Z1 + 10), (s * (UNTERBAU_Y - 2), TRAEGER_Z1 + 10),
                          (s * (GLOCKE_Y + 20), TRAEGER_Z1 + 90), close=True)
            t.append(extrude(Plane.YZ.offset(xs - 6) * make_face(kn), amount=12))
            ysc = s * (Y_TRAEGER + 40)
            t += [sechskant((xs + dx, ysc, TRAEGER_Z1 + 12), (0, 0, 1), 16, 7) for dx in (-28, 28)]


def _konsole(t):
    # Armaturenwand = Rueckseite des Unterbaus unter dem Tankueberhang (oben am Flansch), unten ueber
    # der Glocke offen, seitlich Beine bei |y| >= GLOCKE_Y bis aufs Deck
    t.append(box(XW0 - 1, XK, -KONS_Y, KONS_Y, KONS_Z0, KONS_Z1 + 1))
    for s in (-1, 1):
        y0, y1 = sorted((s * GLOCKE_Y, s * KONS_Y))
        t.append(box(XW0, XK, y0, y1, UB_Z0, KONS_Z0 + 1))
        y0, y1 = sorted((s * (GLOCKE_Y - 0), s * (KONS_Y + 6)))
        t.append(box(XW0 - 10, XK + 30, y0, y1, DECK_Z - 2, DECK_Z + 10))    # Fusswinkel auf dem Deck
        t += [sechskant((XK + 15, s * (GLOCKE_Y + 15), DECK_Z + 10), (0, 0, 1), 14, 6)]
    # umlaufender Rahmen auf der Rueckseite
    aussen = box(XK - 1, XK + 8, -KONS_Y, KONS_Y, KONS_Z0, KONS_Z1)
    innen = fillet(box(XK - 2, XK + 9, -KONS_Y + 20, KONS_Y - 20, KONS_Z0 + 12, KONS_Z1 - 10).edges().filter_by(Axis.X), 18)
    t.append(aussen - innen)
    for y in (-KONS_Y + 10, KONS_Y - 10):
        t.mat("blank", sechskant((XK + 8, y, KONS_Z0 + 10), (1, 0, 0), 14, 5))
    for y in (-KONS_Y + 45, KONS_Y - 45):
        t.mat("blank", sechskant((XK + 8, y, KONS_Z1 - 5), (1, 0, 0), 14, 5))

    # ovale Instrumententafel links
    yo, zo, ay, az = -170.0, ZT, 125.0, 52.0
    ov = Plane.YZ.offset(XK)
    t.mat("blank", extrude(ov * Pos(yo, zo) * Ellipse(ay, az), amount=6))
    t.mat("chrom", extrude(ov * Pos(yo, zo) * Ellipse(ay + 8, az + 8), amount=10)
          - extrude(ov * Pos(yo, zo) * Ellipse(ay - 4, az - 4), amount=12))
    for k in range(8):                                         # Befestigungsschrauben im Rand
        a = math.radians(k * 45 + 22.5)
        t.mat("blank", rad_x(XK + 11, yo + (ay + 2) * math.cos(a), zo + (az + 2) * math.sin(a), 4, 4))
    xi = XK + 6
    _instrument(t, xi, -228, ZT - 4, 30)                       # Amperemeter
    _instrument(t, xi, -165, ZT - 20, 24, winkel=-20)          # Betriebsstundenzaehler
    t.mat("chrom", ring_x(xi + 5, -165, ZT + 30, 14, 8, 10))   # Gluehueberwacher
    t.mat("ruecklicht", Pos(xi + 2, -165, ZT + 30) * Sphere(9))
    t.mat("chrom", rad_x(xi + 8, -100, ZT + 26, 12, 16))        # Lichtschalter
    t.mat("schwarz", rad_x(xi + 26, -100, ZT + 30, 9, 20))
    t.mat("schwarz", Pos(xi + 36, -100, ZT + 26) * box(-4, 4, -4, 4, -14, 14))
    t.mat("chrom", ring_x(xi + 6, -100, ZT - 16, 17, 6, 12))    # Zuendschloss
    t.mat("schwarz", rad_x(xi + 3, -100, ZT - 16, 11, 6))
    t.mat("blank", Pos(xi + 12, -100, ZT - 16) * box(0, 8, -2.5, 2.5, -8, 8))
    t.mat("blank", Pos(xi + 17.6, -100, ZT - 16) * box(0, 6, -12, 12, -10, 10))   # Schluesselbart, ueberlappt den Schaft
    # rechts unter der Lenksaeule: Oeldruck (schwarz) ueber Thermometer (weiss)
    yr = Y_GAUGE
    _instrument(t, XK + 8, yr, ZT + 30, 24, "schwarz", winkel=10)
    _instrument(t, XK + 8, yr, ZT - 36, 27, winkel=-40)
    # Abstell-Zuggriff zwischen den Tafeln
    za = ZT + 8
    t.mat("chrom", rad_x(XK + 14, -10, za, 9, 12))             # Fuehrung
    t.mat("chrom", stab((XK + 8, -10, za), (XK + 70, -10, za), 5))
    t.mat("chrom", stab((XK + 70, -35, za), (XK + 70, 15, za), 7))

    # Handgashebel mit Rastsegment links neben der Lenksaeule
    yh, zh = Y_HANDGAS, Z_HANDGAS
    t.append(box(XK - 2, XK + 10, yh - 10, yh + 10, zh - 50, zh + 40))
    seg = Plane.XZ.offset(-yh) * Pos(XK + 5, zh - 10) * (Circle(80) - Circle(55))
    seg = extrude(seg, amount=5, both=True) & box(XK, XK + 90, yh - 10, yh + 10, zh - 10, zh + 60)
    t.append(seg)
    t.append(stab((XK + 15, yh, zh), (XK + 95, yh, zh + 140), 7))
    t.mat("schwarz", Pos(XK + 95, yh, zh + 140) * Sphere(16))
    t.mat("blank", rad_x(XK + 15, yh, zh, 12, 12))


def _lenkung(t):
    a, b = LENK_FUSS, LENK_MITTE
    d = (b - a).normalized()
    # Lagerbock: Flanschplatte mit 4 Schrauben, Lagergehaeuse
    zo = min(a.Z + 55, KONS_Z1 - 6)                            # Flansch bleibt unter dem Tankflansch
    t.append(box(XK + 6, XK + 22, a.Y - 55, a.Y + 55, zo - 110, zo))
    t.append(stab((XK + 20, a.Y, a.Z), (a.X + 16, a.Y, a.Z), 38))    # Lagerstutzen durch den Flansch
    for dy in (-42, 42):
        for dz in (zo - a.Z - 100, zo - a.Z - 12):
            t.mat("blank", sechskant((XK + 22, a.Y + dy, a.Z + dz), (1, 0, 0), 16, 7))
    t.append(stab(a + Vector(15, 0, 0), a + d * 110, 46))      # Lagergehaeuse
    t.append(stab(a + d * 102, a + d * 118, 52))               # Bund
    # Mantelrohr und Lenkspindel
    t.append(stab(a + d * 110, b - d * 140, 30))
    t.append(stab(b - d * 146, b - d * 132, 36))               # oberes Lager
    t.mat("blank", stab(b - d * 140, b - d * 40, 17))
    # Lenkrad im lokalen System (z = Saeulenachse)
    xd = (Vector(0, 1, 0) - d * d.Y).normalized()
    loc = Location(Plane(origin=b, x_dir=xd, z_dir=d))
    rad = Sammler("schwarz")
    rad.append(Torus(R_KRANZ, R_KRANZ_Q))
    rad.append(Pos(0, 0, -40) * Cylinder(32, 72, align=(Align.CENTER, Align.CENTER, Align.MIN)))  # Nabe
    for k in range(4):                                         # Speichen (Rundstahl, gekroepft)
        w = math.radians(45 + k * 90)
        cw, sw = math.cos(w), math.sin(w)
        rad.mat("blank", stab((28 * cw, 28 * sw, 20), (120 * cw, 120 * sw, 4), 8))
        rad.mat("blank", stab((120 * cw, 120 * sw, 4), ((R_KRANZ - 4) * cw, (R_KRANZ - 4) * sw, 0), 8))
        rad.mat("blank", Pos(120 * cw, 120 * sw, 4) * Sphere(8))
    rad.mat("chrom", Pos(0, 0, 18) * Cylinder(44, 16, align=(Align.CENTER, Align.CENTER, Align.MIN)))  # Nabenstern
    rad.mat("chrom", Pos(0, 0, 34) * (Cylinder(36, 8, align=(Align.CENTER, Align.CENTER, Align.MIN))
                                      - Cylinder(28, 20, align=(Align.CENTER, Align.CENTER, Align.MIN))))
    knopf = Pos(0, 0, 34) * Cylinder(28, 14, align=(Align.CENTER, Align.CENTER, Align.MIN))
    rad.mat("schwarz", fillet(knopf.edges().group_by(Axis.Z)[-1], 8))   # Hupenknopf
    for mat, lst in rad.schichten().items():
        t.mat(mat, [loc * s for s in lst])


def _hebel_pedale(t):
    zb = DECK_Z + 6                                            # Oberkante Bodenblech
    # Bodenblech Fussraum mit Ausschnitt fuer den Getriebedeckel des Rumpfs, Schraubenreihen
    gx0, gx1, gy = GETR_DECKEL[0] - 5, GETR_DECKEL[1] + 5, GETR_DECKEL[2] + 5
    xb0, xb1 = XK + 5, BODEN_X1
    t.append(box(xb0, xb1, -330, 330, DECK_Z, zb) - box(gx0, gx1, -gy, gy, DECK_Z - 1, zb + 1))
    for s in (-1, 1):
        t += schraubenreihe((xb0 + 25, s * 310, zb), (xb1 - 25, s * 310, zb), 9, (0, 0, 1), 18, 6)
    t += schraubenreihe((xb1 - 25, -230, zb), (xb1 - 25, -90, zb), 2, (0, 0, 1), 18, 6)
    t += schraubenreihe((xb1 - 25, 90, zb), (xb1 - 25, 230, zb), 2, (0, 0, 1), 18, 6)
    t += schraubenreihe((xb0 + 25, -230, zb), (xb0 + 25, 230, zb), 5, (0, 0, 1), 18, 6)
    # Riffelung des Bodenblechs (Rippen quer) unter den Pedalen
    for i in range(3):
        x = PED_X0 + 60 + i * 36
        t.append(box(x, x + 8, -280, 60, zb, zb + 4))
    for sg in (-1, 1):                                         # Riffel neben dem Deckel
        for i in range(6):
            x = gx0 + 15 + i * 36
            y0, y1 = sorted((sg * (gy + 15), sg * 290))
            t.append(box(x, x + 8, y0, y1, zb, zb + 4))

    # Schalthebel: Gummimanschette, Hebel nach vorn gekroepft, Knauf
    fx, fy = SCHALT
    t.append(Pos(fx, fy, zb) * Cylinder(62, 10, align=(Align.CENTER, Align.CENTER, Align.MIN)))   # Abdeckplatte
    t += schraubenreihe((fx - 42, fy - 42, zb + 10), (fx + 42, fy + 42, zb + 10), 2, (0, 0, 1), 14, 5)
    t += schraubenreihe((fx - 42, fy + 42, zb + 10), (fx + 42, fy - 42, zb + 10), 2, (0, 0, 1), 14, 5)
    manschette = Solid.make_cone(50, 20, 85, Plane.XY.offset(zb + 10).move(Location((fx, fy, 0))))
    t.mat("gummi", manschette)
    for i in range(3):
        t.mat("gummi", Pos(fx, fy, zb + 26 + i * 22) * Torus(44 - i * 9, 6))
    knauf = (fx - 120, fy - 5, 1085)
    t.append(rohr_glatt([(fx, fy, zb + 60), (fx - 10, fy, 1000), knauf], 13))
    t.mat("schwarz", Pos(knauf[0] - 2, knauf[1], knauf[2] + 15) * Sphere(34))

    # Gruppenhebel (kuerzer) rechts daneben
    gx, gy2 = GRUPPE
    t.mat("gummi", Solid.make_cone(36, 16, 50, Plane.XY.offset(zb).move(Location((gx, gy2, 0)))))
    knauf = (gx - 50, gy2 + 5, 1010)
    t.append(rohr_glatt([(gx, gy2, zb + 30), (gx - 15, gy2, 930), knauf], 11))
    t.mat("schwarz", Pos(knauf[0] - 2, knauf[1], knauf[2] + 12) * Sphere(26))

    # Pedale: Kupplung (Mitte), Bremse (rechts) mit Riffel-Trittflaeche
    for y, br in ((-20, 100), (230, 80)):
        t.mat("gummi", box(PED_X0 - 30, PED_X0 + 30, y - 40, y + 40, zb, zb + 8))   # Durchfuehrungsmanschette
        p0, p1 = Vector(PED_X0, y, zb + 8), Vector(PED_X1, y, DECK_Z + 125)
        t.append(stab(p0, p1, 15))
        pl = Plane(origin=p1, x_dir=(0, 1, 0), z_dir=(0.5, 0, 0.866))
        t.append(pl * Pos(0, 0, -6) * Box(br, 85, 14))
        for k in range(5):                                     # Riffel
            t.append(pl * Pos(0, -32 + k * 16, 3) * Box(br - 16, 6, 6))
        t.append(pl * Pos(0, 0, -16) * Box(30, 50, 12))        # Pedalnabe


def _sitz(t):
    """Einteilige Schalensitz (Prospekt K 55 E, PH): tiefe gepresste Schale (Ellipsoid),
    oben von einem Kreisbogen abgeschnitten -> vorn flache Lippe, hinten hochgezogener Ruecken, Randwulst,
    Lederpolster als Auskleidung mit dickerem Sitzkissen. Getragen von einer Sitzkonsole
    auf einem Blattfeder-Arm, der hinter dem Getriebedeckel in einem Mittelsockel eingespannt ist."""
    A, C, w, zb = SITZ_A, SITZ_C, SITZ_WAND, SITZ_ZB
    m = (SITZ_X, 0, zb + C)                                   # Ellipsoid-Mitte
    aussen = _ellipsoid(m, A, A, C)
    innen = _ellipsoid(m, A - w, A - w, C - w)
    # Schnittflaeche: Kreisbogen (Zylinder quer) - vorn flache Lippe SITZ_LIPPE ueber dem Boden,
    # tiefster Punkt bei SITZ_X - SITZ_MULDE_DX, hinten steil hoch auf SITZ_RUECKEN
    xc, z_tief = SITZ_X - SITZ_MULDE_DX, zb + SITZ_LIPPE - 8
    dx, dz = SITZ_X + A - xc, SITZ_RUECKEN - (SITZ_LIPPE - 8)
    rb = (dx * dx + dz * dz) / (2 * dz)
    zcb = z_tief + rb

    def ueber(off):
        """Bereich ueber der Schnittflaeche, um off nach innen (negativ: nach unten) verschoben."""
        return Pos(xc, 0, zcb) * Rot(90, 0, 0) * Cylinder(rb - off, 1400)

    schale = aussen - innen - ueber(0)
    # Randwulst: aussen aufgedickter Streifen unter der Schnittkante
    wulst = ((_ellipsoid(m, A + 9, A + 9, C + 9) - innen) & ueber(-24)) - ueber(0)
    # Polster: Auskleidung bis 40 unter die Kante, dazu Sitzkissen (in der Mitte gemuldet)
    innen2 = _ellipsoid(m, A - w - POLSTER, A - w - POLSTER, C - w - POLSTER)
    auskleidung = (innen - innen2) - ueber(-40)
    kissen = (innen & box(SITZ_X - 400, SITZ_X + 400, -400, 400, zb, zb + 80)) - Pos(0, 0, 50) * innen
    polster = auskleidung + kissen

    neig = Pos(SITZ_X, 0, zb) * Rot(0, SITZ_NEIG, 0) * Pos(-SITZ_X, 0, -zb)
    aussen_n = neig * aussen
    t.append(neig * schale)
    t.append(neig * wulst)
    t.mat("leder", neig * polster)

    # Sitzkonsole unter der Schale (an die Schale angepasst)
    kz0 = zb - 25
    t.append(box(SITZ_X - 80, SITZ_X + 80, -60, 60, kz0, zb + 45) - aussen_n)
    t += [sechskant((SITZ_X + dx, dy, kz0), (0, 0, -1), 14, 6) for dx in (-60, 60) for dy in (-40, 40)]

    # Mittelsockel hinter dem Getriebedeckel: gepresster Kasten mit Fussplatte
    zb_s = DECK_Z + 6                                         # auf dem Bodenblech
    sx = SOCKEL_X
    t.append(kasten_rund(sx - 40, sx + 40, -55, 55, zb_s - 2, SOCKEL_Z1, 15))
    t.append(kasten_rund(sx - 60, sx + 60, -75, 75, zb_s - 2, zb_s + 10, 12))
    for dx in (-48, 48):
        for dy in (-62, 62):
            t.mat("blank", sechskant((sx + dx, dy, zb_s + 10), (0, 0, 1), 14, 6))
    # Blattfeder-Arm: hinten im Sockel eingespannt, nach vorn unter die Sitzkonsole (zwei Lagen)
    p0 = Vector(sx + 30, 0, SOCKEL_Z1 + 5)
    p1 = Vector(SITZ_X - 65, 0, kz0 - 5)
    pm = (p0 + p1) * 0.5 + Vector(0, 0, -5)
    arc = ThreePointArc(p0, pm, p1)
    for l, dz in ((1.0, 0.0), (0.55, -14.0)):
        q = [arc.position_at(u * l) + Vector(0, 0, dz) for u in (0, 0.5, 1)]
        path = Wire([ThreePointArc(*q)])
        prof = Plane(origin=path.position_at(0), x_dir=(0, 1, 0), z_dir=path.tangent_at(0)) * Rectangle(70, 14)
        t.mat("schwarz", sweep(prof, path=path))
    # Klemmplatte mit Buegelschrauben auf dem Sockel
    zk = SOCKEL_Z1 + 12
    t.append(box(sx - 25, sx + 25, -48, 48, zk, zk + 12))
    for dy in (-42, 42):
        t.mat("blank", Pos(sx, dy, SOCKEL_Z1 - 30) * Cylinder(6, zk + 12 - SOCKEL_Z1 + 30,
                                                            align=(Align.CENTER, Align.CENTER, Align.MIN)))
        t.mat("blank", sechskant((sx, dy, zk + 12), (0, 0, 1), 14, 8))


def _kasten(t, x0, x1, y0, y1, z1, scharnier_y, griff=True):
    """Blechkasten mit uebergreifendem Deckel, Scharnieren an scharnier_y, Ueberwurf vorn."""
    t.append(kasten_rund(x0, x1, y0, y1, DECK_Z, z1 - 2, 8))
    # Versteifungssicke rundum
    t.append(kasten_rund(x0 - 4, x1 + 4, y0 - 4, y1 + 4, DECK_Z + 95, DECK_Z + 110, 10))
    t.append(kasten_rund(x0 - 4, x1 + 4, y0 - 4, y1 + 4, DECK_Z, DECK_Z + 10, 10))   # Fussleiste
    deckel = kasten_rund(x0 - 10, x1 + 10, y0 - 10, y1 + 10, z1 - 30, z1 + 12, 12)
    deckel = deckel - kasten_rund(x0, x1, y0, y1, z1 - 31, z1 - 2, 8)
    t.append(deckel)
    s = 1 if scharnier_y > (y0 + y1) / 2 else -1
    ys = y1 + 10 if s > 0 else y0 - 10
    for xs in (x0 + 0.2 * (x1 - x0), x1 - 0.2 * (x1 - x0)):
        t.mat("blank", rad_x(xs, ys + s * 8, z1 - 4, 10, 70))
        t.mat("blank", box(xs - 35, xs + 35, ys, ys + s * 4, z1 - 40, z1 - 4) if s > 0
              else box(xs - 35, xs + 35, ys - 4, ys, z1 - 40, z1 - 4))
    # Ueberwurf mit Oese (Vorhaengeschloss) auf der Gegenseite
    yv = y0 - 10 if s > 0 else y1 + 10
    xm = (x0 + x1) / 2
    t.mat("blank", box(xm - 20, xm + 20, yv - s * 6, yv, z1 - 75, z1 + 6) if s > 0
          else box(xm - 20, xm + 20, yv, yv - s * 6, z1 - 75, z1 + 6))
    oese = rad_y(xm, yv - s * 16, z1 - 60, 13, 8) - rad_y(xm, yv - s * 16, z1 - 60, 6, 12)
    t.mat("blank", oese)
    if griff:
        t.mat("blank", stab((xm - 70, (y0 + y1) / 2, z1 + 12), (xm - 70, (y0 + y1) / 2, z1 + 32), 6))
        t.mat("blank", stab((xm + 70, (y0 + y1) / 2, z1 + 12), (xm + 70, (y0 + y1) / 2, z1 + 32), 6))
        t.mat("blank", stab((xm - 76, (y0 + y1) / 2, z1 + 32), (xm + 76, (y0 + y1) / 2, z1 + 32), 7))


def _kaesten(t):
    # Werkzeugkaesten hinten auf beiden Kotfluegeln, Scharniere aussen
    for s in (-1, 1):
        y0, y1 = sorted((s * WK_Y0, s * WK_Y1))
        _kasten(t, WK_X0, WK_X1, y0, y1, WK_Z1, s * WK_Y1)
    # Werkzeugkasten vorn links (Prospekt)
    x0, x1, y0, y1 = BAT
    _kasten(t, x0, x1, -y1, -y0, BAT_Z1 + 20, -y1, griff=False)

    # Batteriekasten rechts vor dem Sitz: Kasten, Deckel, Spannbuegel mit Fluegelmuttern
    t.append(kasten_rund(x0, x1, y0, y1, DECK_Z, BAT_Z1, 8))
    t.append(kasten_rund(x0 - 4, x1 + 4, y0 - 4, y1 + 4, DECK_Z, DECK_Z + 10, 10))
    deckel = kasten_rund(x0 - 10, x1 + 10, y0 - 10, y1 + 10, BAT_Z1 - 25, BAT_Z1 + 12, 12)
    t.append(deckel - kasten_rund(x0, x1, y0, y1, BAT_Z1 - 26, BAT_Z1, 8))
    xm = (x0 + x1) / 2
    for dx in (-60, 60):
        t.append(box(xm + dx - 6, xm + dx + 6, y0 + 30, y1 - 30, BAT_Z1 + 12, BAT_Z1 + 17))   # Sicke im Deckel
    t.mat("schwarz", box(xm - 20, xm + 20, y0 - 22, y1 + 22, BAT_Z1 + 12, BAT_Z1 + 24))     # Spannbuegel
    for yb, sg in ((y0, -1), (y1, 1)):
        yy = yb + sg * 16
        t.mat("blank", box(xm - 20, xm + 20, yb + (sg * 0 if sg > 0 else -22), yb + (22 if sg > 0 else 0), BAT_Z1 - 90, BAT_Z1 - 78))  # Lasche
        t.mat("blank", Pos(xm, yy, BAT_Z1 - 78) * Cylinder(6, 118, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        t.mat("blank", Pos(xm, yy, BAT_Z1 + 24) * Cylinder(10, 12, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        t.mat("blank", Pos(xm, yy, BAT_Z1 + 34) * box(-24, 24, -5, 5, 0, 16))     # Fluegel
    # Batteriekabel: aus der Kastenwand zum Rumpf (unter das Bodenblech)
    # Batteriekabel: aus der Stirnwand nach vorn und durch das Kotfluegelblech zum Rumpf
    # (Kabel unter dem Kotfluegelblech)
    yk = y0 + 50
    t.mat("gummi", rohr_glatt([(x0, yk, BAT_Z1 - 80), (x0 - 60, yk, BAT_Z1 - 80), (x0 - 60, yk, DECK_Z + 2)], 11))
    t.mat("blank", rad_x(x0 - 6, yk, BAT_Z1 - 80, 16, 12))             # Kabeltuelle
    t.mat("gummi", Pos(x0 - 60, yk, DECK_Z - 2) * Cylinder(20, 10, align=(Align.CENTER, Align.CENTER, Align.MIN)))


def _ruecklicht(t):
    """Rechteckiges Ruecklicht mit runder Scheibe hinten links an der Rueckwand des
    Traversen-Quertraegers (planierschild.py: Rueckwand x = TRAV_HINTEN, z 1060..1240)."""
    y, zl = RL_Y, RL_Z
    xe = TRAV_HINTEN - 2                    # Anlage an der Rueckwand (2 mm eingesenkt)
    # Flanschplatte mit 2 Schrauben, Ausleger, Gehaeuse
    t.append(box(xe, xe + 12, y - 30, y + 30, zl - 70, zl - 10))
    t += [sechskant((xe + 12, y + dy, zl - 40), (1, 0, 0), 12, 5) for dy in (-18, 18)]
    t.append(box(xe + 10, xe + 32, y - 18, y + 18, zl - 58, zl - 44))
    t.append(kasten_rund(xe + 30, xe + 75, y - 55, y + 55, zl - 50, zl + 50, 10, Axis.X))
    t.mat("chrom", ring_x(xe + 78, y, zl, 42, 34, 8))
    t.mat("ruecklicht", rad_x(xe + 77, y, zl, 36, 6))
    t.mat("ruecklicht", Pos(xe + 80, y, zl) * scale(Sphere(1), by=(8, 34, 34)))
    # Kabel in die Traverse
    t.mat("gummi", rohr_glatt([(xe + 45, y + 45, zl - 49), (xe + 45, y + 45, zl - 62), (xe + 1, y + 45, zl - 62)], 5))


def fahrerstand():
    t = Sammler("lack")
    _unterbau(t)
    _konsole(t)
    _lenkung(t)
    _hebel_pedale(t)
    _sitz(t)
    _kaesten(t)
    _ruecklicht(t)
    return t
