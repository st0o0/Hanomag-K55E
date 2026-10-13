"""Tank und Fahrerstand (Original-mm, X nach hinten, Y nach rechts, Z ab Boden).

WAS: Alles, was hinter der Haube auf der Plattform steht: der Kraftstofftank in Haubenform mit seinem Unterbau,
dem Armaturenkasten, der Lenkung, den Pedalen, dem Schalthebel, dem Bodenblech und dem Fahrersitz.

Aufbau und Technik (Fotos t39/t42/t46 des Nutzers, K 55; dazu fz_05/10/11, fz_01):
  * Tank: verzinkter Blechtank in Haubenform (keine liegende Trommel). Seitenprofil: Stirn senkrecht direkt
    hinter der Haube (x 1085), Oberseite fast in der Flucht des Haubendachs (z 1335), Unterseite waagerecht auf
    dem Unterbauflansch (z 1125). Hinten ist die Oberseite laenger als die Unterseite: Oberkante bis x ~1545,
    Unterkante bis 1455, dazwischen schraege Rueckwand, oben mit grossem Radius (100) in die Oberseite
    uebergehend. Unter dem Ueberhang sitzt das Armaturenbrett. Querschnitt fast haubenbreit (680): Dachbogen und
    Kantenradius (R 70) kommen aus haube.py (der Tank setzt den Haubenquerschnitt buendig fort), Seiten
    senkrecht, Unterseite flach. Stirn mit umlaufender gerollter Falz/Sicke, hinten unten waagerechte Abkantung
    mit Schraubenreihe. Zwei Spannbaender quer ueber Oberseite und Seiten (bei ~14 % und ~72 % der Laenge),
    unten mit Gewindestangen/Muttern durch Knotenbleche am Auflageflansch des Unterbaus gespannt. Seitlich
    zwischen den Baendern zwei runde gewoelbte Schraubenkoepfe, oben Einfuellstutzen mit Fluegelmutter-Deckel,
    kleine Kanne, Kraftstoffhahn (Messing) unten aussen am Unterbau.
  * Tankunterbau: Mittelblock von der Plattform bis unter den Tank (Oberkante 1116) mit seitlich ueberstehendem
    Auflageflansch (Winkelblech), auf dem der Tank nur aufliegt (abnehmbar, der Tank gehoert zu haube_tank).
    Seitlich daneben je ein flacher Werkzeugkasten auf einem Konsolenblech (Video 054-066, 137, 158), darunter
    offen; Stuetzen auf den Laengstraegern.
  * Armaturenkasten (tuerkis): Rueckseite des Unterbaus unter dem Tankueberhang, schraege Front mit grossem
    Rundinstrument links, drei kleinen Knoepfen, Zuendschloss mit Hebel und rechts zwei Instrumenten
    uebereinander (Video 121-126, 128, 131, 137, 138, 2:09).
  * Lenksaeule steil (~50 Grad) aus dem Unterbau unter dem Tankueberhang, Vierspeichen-Lenkrad mit Hupenknopf;
    Handgashebel neben der Saeule.
  * Fussraum: Schalthebel mit Gummimanschette aus dem Bodenblech, drei Pendelpedale unter dem Lenkrad
    (Kupplung links neben der Saeule, zwei Bremspedale rechts) mit Riffel-Trittflaechen, verschraubte
    Bodenbleche (Anordnung nach Traktorenlexikon Hanomag K 55).
Prospekt K 55 E (PK, PH = prospekt_heck):
  * Sitz: laut Fotos (DSC04745, c_sl_box) und Video 128-140 tiefe Blechschale mit Kunstlederpolster auf
    Sitztraeger und Blattfeder-Arm im Mittelsockel hinter dem Getriebedeckel, Mitte SITZ_X.
Werkzeugkaesten gibt es nur neben dem Tank; hinten auf den Kotfluegeln ist die Plattform frei (Video 116/130/137/157).
"""

from __future__ import annotations

import contextlib
import math

from build123d import (
    Align,
    Axis,
    Box,
    Circle,
    Cone,
    Cylinder,
    Edge,
    Location,
    Plane,
    Polyline,
    Pos,
    Rectangle,
    RectangleRounded,
    Rot,
    Solid,
    Sphere,
    ThreePointArc,
    Torus,
    Vector,
    Wire,
    extrude,
    fillet,
    make_face,
    scale,
    sweep,
)

from .common import (
    DACH_R_KANTE,
    DECK_X0,
    DECK_Z,
    FW_X0,
    FW_X1,
    FW_Y0,
    FW_Y1,
    FW_Z0,
    FW_Z1,
    LENKRAD,
    SITZ_X,
    SITZ_Y,
    TANK_B,
    TANK_X0,
    TANK_X1,
    TANK_Z0,
    TRAEGER_Z1,
    X_BREMSE,
    Y_TRAEGER,
    Sammler,
    box,
    kasten_rund,
    rad_x,
    rad_y,
    rohr_glatt,
    schraube,
    schraubenkreis,
    schraubenreihe,
    sechskant,
    stab,
    z_dach_orig,
)


def _zq(y: float) -> float:
    """Hoehe des Haubendachs (Original-mm ab Boden) bei Querlage y (Original-mm), aus haube.z_dach (Modell-mm)."""
    return z_dach_orig(abs(y))


# ---------------- Parameter ----------------

# --- Freiraum Kupplungsglocke ---
# Freiraum fuer die Kupplungsglocke des Rumpfs unter Tank und Konsole: |y| < 300, z <= 950
GLOCKE_Y, GLOCKE_Z1 = 300.0, 950.0

# --- Tankunterbau: Mittelblock, Auflageflansch, Stuetzen ---
# Mittelblock (|y| < KB_Y) unter dem Tank, seitlich je ein flacher Werkzeugkasten auf einer Konsole, darunter offen
UNTERBAU_Y = 335.0           # Aussenkante der Werkzeugkaesten y = +-335
KB_Y = 200.0                 # Mittelblock |y| < 200, Werkzeugkaesten y 200..335
UB_PLATTE_Z0 = GLOCKE_Z1 + 12   # Unterkante Mittelblock 962 (frei ueber der Glocke)
# Auflageflansch: seitlicher Ueberstand bis |y| 355 (Hydraulikleitungen laufen ab |y| 375, alles am Tank innerhalb |y| 360)
FL_Y = 355.0
FL_DICKE = 9.0               # Flanschblech
FL_ZT = TANK_Z0 - 0.6        # Oberkante Flansch: 0,6 unter dem Tank (haube.stirnwand reicht 0,5 unter die Tankunterkante)
FL_Z0 = FL_ZT - FL_DICKE     # Unterkante Flansch 1080 (= Oberkante Mittelblock)
FL_X1 = 1488.0               # Flansch endet hinten buendig mit der Konsolenrueckseite
XW0 = TANK_X1                # Vorderseite Konsolenwand = Rueckseite Kastenblock
XK = TANK_X1 + 25            # Bezugsmass Fussraum / Lenkung (1480)
LTG_Y = UNTERBAU_Y + 15      # Kraftstoffleitung aussen an der Unterbau-Wand (|y| 345), laeuft frei durch die Flanschbohrung
X_HAHN = TANK_X1 - 150.0     # Kraftstoffhahn (zwischen den Baendern), Leitung bis zum Werkzeugkasten

# --- Werkzeugkaesten neben dem Tank und Stuetzen ---
TK_X0, TK_X1 = 1100.0, 1450.0   # Werkzeugkasten neben dem Tank: 350 lang (Video: 330..400)
# Kastenkoerper 915..1030 (steht hinten auf der Plattformkante, Video 137/158); Deckel bis 1040 (unter den Spannband-Knotenblechen
# z 1047)
TK_Z0, TK_Z1 = DECK_Z, 1030.0
# Konsolenblech unter dem Kasten (z 907..915, endet vor der Plattform DECK_X0), ueber der Glocke (Oberkante bei y 200: 863)
TK_SHELF = 8.0
STUETZEN_X = (TANK_X0 + 95, TANK_X1 - 90)   # Stuetzen auf den Laengstraegern (Fussplatte hinter dem Glockenflansch bis x 1116)

# --- Tank in Haubenform (Seitenprofil X-Z, Querschnitt Y-Z) ---
TANK_Z1 = _zq(0.0)           # Oberkante Tankmitte = Haubendach (folgt haube.py)
TANK_XT = 1605.0             # virtuelle Ecke hinten oben; nach der Verrundung reicht die Oberseite bis x ~1535
R_T_OBEN_H, R_T_OBEN_V = 75.0, 40.0   # Radius hintere / vordere Oberkante (Seitenprofil)
R_T_UNTEN_H = 30.0           # Radius hintere Unterkante
R_QUER = DACH_R_KANTE   # Radius der oberen Laengskanten = Kantenradius der Haube (R 70)
Y_TANK = TANK_B / 2          # Tankseite y = +-325
BOMB = TANK_Z1 - _zq(Y_TANK)   # Bombierung der Oberseite (Pfeilhoehe bis zur Tankseite, aus dem Haubendach)
X_BAND = (1150.0, 1400.0)    # Spannbaender bei ~14 % und ~72 % der Tanklaenge (hinten auf der ebenen Oberseite)
BAND_B, BAND_S = 40.0, 8.0   # Breite in x, Blechstaerke
BAND_ZE = TANK_Z0 + 42.0     # Bandende unten (Lasche)
Y_ROD = Y_TANK + 10.0        # Gewindestangen aussen neben dem Tank |y| 350 (im Flansch, FL_Y 355)
X_STUTZEN, Y_STUTZEN = 1275.0, -140.0   # Einfuellstutzen mit Fluegelmutter-Deckel
X_KANNE, Y_KANNE = 1275.0, 140.0        # kleine Kanne rechts oben

# --- Armaturenkasten (tuerkis), haengt an der Rueckseite des Mittelblocks unter dem Tankueberhang ---
# y von / bis: 375 breit (Review Fussraum: Kamera-Fit Video 2:09, Frontbreite 350 px = 372 mm statt 436; Lenkgetriebe-Winkel
# rechts daneben ab y 150)
DASH_Y0, DASH_Y1 = -290.0, 85.0
DASH_X0 = XW0                          # Rueckwand am Mittelblock
DASH_ZU, DASH_ZO = 925.0, 1078.0       # Unterkante / Oberkante (Tankflansch beginnt bei 1081)
DASH_XU, DASH_XO = 1510.0, 1472.0      # Frontflaeche: unten / oben (schraege Front, kippt nach hinten oben)

# --- Lenkung und Handgas ---
LENK_MITTE = Vector(*LENKRAD)                       # Lenkradmitte (common.py)
# Schneckengetriebe-Gehaeuse rechts neben dem Armaturenkasten; Saeule steigt unter ~50 Grad
LENK_FUSS = Vector(XK + 30.0, LENKRAD[1], 1062.0)
R_KRANZ, R_KRANZ_Q = 207.0, 17.0      # Kranz Mitte / Querschnitt (aussen 448)
Y_HANDGAS = 118.0                     # Handgashebel neben der Saeule
HANDGAS_FUSS = (1486.0, 1030.0)       # Drehpunkt Handgashebel (x, z), am Lenksaeulenwinkel
HANDGAS_OBEN = (1556.0, 1236.0)       # Kopf der Handgasstange (x, z): ueber der Armaturenkasten-OK, hinter der Tankrueckwand

# --- Pedale (Fussraum, relativ zur Konsolenrueckseite) ---
# Review 2 (Nutzer: "Unter dem Lenkrad befinden sich die Pedale"): drei Pendelpedale unter dem Lenkrad (Saeule y 200), Hebel durch
# Schlitze
# im Bodenblech, Trittplatten schraeg zum Fahrer. Anordnung nach Traktorenlexikon Hanomag K 55 (Wikibooks: Kupplungspedal +
# Bremspedale;
# gelenkt wird ueber das Lenkrad auf die Lenkbremsen) und Konvention: Kupplung links neben der Saeule, Bremsen rechts / unter dem
# Rad.
PED_X0 = 1640.0              # Durchtritt der Bremspedalhebel im Bodenblech
PED_DX, PED_DZ = 105.0, 112.0   # Hebel: Schlitz -> Trittplatte (nach hinten oben)
PED_B = 74.0                 # Breite der Trittplatten (y)
PED_X1 = PED_X0 + PED_DX     # Trittflaechen 1745
# Kupplungspedal (x, y): Gabelkopf des Gestaenges Video 2:09 (Kamera-Fit t020: Boden x ~1665..1720, y ~10..105)
PED_KUPPLUNG = (1665.0, 112.0)
PED_KUPPLUNG_DURCHTRITT = (1722.0, 52.0)   # Durchtritt der Kupplungs-Zugstange im Blech (x, y)
PED_BREMSE = ((1640.0, 218.0), (1640.0, 298.0))   # zwei Bremspedale (links/rechts Lenkbremse), unter dem Lenkrad
PED_KLINKE_Y = 258.0         # Verbindungsklinke zwischen den Bremspedalplatten

# --- Schalthebel ---
# Fuss Schalthebel (Gummibalg). Kamera-Fit Video 2:09: Strahl durch den Balg trifft den Boden (z 745) bei x 1561..1596, y -14;
SCHALT = (1600.0, -15.0)
                              # vorher (1800, -100) lag der Balg im Fit 200 mm zu weit hinten und links, unter dem Sitz
SCHALT_KNAUF = (1580.0, -138.0, 1095.0)   # schwarze Kugel knapp hinter und ueber dem unteren Kastenrand (Short 0:45..0:50)

# --- Bodenblech, Fugen und Oel-Stutzen ---
BODEN_Z = DECK_Z + 6.0       # Oberkante Bodenblech auf den Plattformen
BODEN_X1 = 2520.0            # Ende Bodenblech (hinter dem Sitzsockel)
FUGE_B, FUGE_T = 6.0, 4.0    # Fugenbreite / -tiefe im Fussraumboden (0,75 / 0,5 mm im Modell)
FUGE_Y = (-174.0, -104.0)    # Laengsfugen (Video 2:09, Frame 129)
FUGE_X = 1557.0              # Querfuge im schmalen Streifen an der Wand
# Sechskant-Stutzen im Boden (Oel-Einfuell-/Entlueftung Getriebe), Video 2:09: Fuss bei x 1894, y -118 (Strahl auf z 740)
STUTZEN = (1894.0, -118.0)
STUTZEN_H = 200.0            # Hoehe ueber dem Boden (Kopf z ~940, 25 ueber der Plattform)
# Klinke/Zahnstange am Boden vor dem Sitz (Short 0:17/0:18.5), Lage nur grob aus dem Frame: x ~2090..2130, y ~ -25..215
KLINKE_BODEN = (2108.0, 95.0)

# --- Sitz: tiefe Blechschale mit Polster ---
# Randellipse x/y, Mulde als Ausschnitt eines Ellipsoids, umgebordelter Rand, Sitztraeger unter der Mitte, Blattfeder-Arm
SITZ_A, SITZ_B = 178.0, 225.0        # Halbachsen der Randellipse (Tiefe x 356, Breite y 450, Video 128: breiter als lang)
# Review 2 (Nutzer: "Der Sitz muss viel weiter nach hinten"): unter dem Lenkrad ausgerichtet (Lenkrad y 200); die Kamera-Fits y
# 170/195 hatten +-100 mm Tiefenunsicherheit
                                      # Seitenrand y -25..425, Sitz bleibt zwischen Fussraum (Wand y 345) und der Innenwange des
                                      # Kotfluegels (y 430)
# Mitte der Sitzschale, Review 2: Seitenansicht Video 2:44 (s164, Schale px ~365..555) -> x = 1031 + 1168*f, Perspektivfaktor f
# 1.10..1.13 (Sitz ~800 mm hinter der Spurebene) = 2316..2351; vordere Kante 2162, hinterer Rand 2518 (Querrohre der Traverse ab x
# 2519, z >= 1209 weit ueber der Schale)
SITZ_T = 6.0                          # Blechstaerke
SITZ_TIEFE = 100.0                    # tiefe Mulde: Rand liegt so viel ueber dem Schalenboden (Video 128-140)
SITZ_EA, SITZ_EB = 270.0, 341.0       # Halbachsen des Muldenellipsoids x/y
SITZ_ZB = 1005.0                      # Unterkante Schale in der Mitte (absolut, Polster ~1105 nach Video)
SITZ_NEIG = 3.0                       # Schale nach hinten geneigt (Grad, um den Boden)
SITZ_RAND_H = 14.0                    # umgebordelter Rand nach unten
SITZ_TRAEGER = (-45.0, 50.0, 45.0)    # Sitztraeger-Block unter der Mitte: x von/bis (rel. SITZ_X), halbe Breite y
SITZ_TRAEGER_UNTEN = 50.0             # Sitztraeger reicht so weit unter die Schalenunterseite
SOCKEL_X = SITZ_X + 100               # Mittelsockel hinter dem Getriebedeckel 2440 (Fussplatte auf dem Hinterachs-/Heckkasten)
SOCKEL_Z1 = 972.0                     # Oberkante Sockel (Federeinspannung)


# ---------------- Allgemeine Helfer ----------------
def _zyl(r: float, h: float) -> Solid:
    """Zylinder ab z = 0 nach oben."""
    return Cylinder(r, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def _ellipsoid(c: tuple[float, float, float], a: float, b: float, cc: float) -> Solid:
    return Pos(*c) * scale(Sphere(1.0), by=(a, b, cc))


def _ecke(f, x: float, z: float, r: float):
    """2D-Ecke bei (x, z) des in der XY-Ebene gebauten Profils verrunden."""
    return fillet([v for v in f.vertices() if abs(v.X - x) < 1e-3 and abs(v.Y - z) < 1e-3], r)


def _trittplatte(t: Sammler, p0: Vector, p1: Vector) -> None:
    """Pedalhebel von p0 nach p1 mit geneigter, geriffelter Trittplatte (Normale zum Fahrer) und Pedalnabe."""
    t.append(stab(p0, p1, 15))
    pl = Plane(origin=p1, x_dir=(0, 1, 0), z_dir=(0.5, 0, 0.866))
    t.append(pl * Pos(0, 0, -6) * Box(PED_B, 90, 14))                      # Trittplatte
    for k in range(5):                                                      # Riffel (nur auf den Trittflaechen)
        t.append(pl * Pos(0, -32 + k * 16, 3) * Box(PED_B - 16, 6, 6))
    t.append(pl * Pos(0, 0, -16) * Box(30, 50, 12))                         # Pedalnabe


# ---------------- Tank ----------------
def _profil_face(g: float = 0.0):
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


def _quer_face(g: float = 0.0):
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


def _koerper(g: float, xa: float, xb: float) -> Solid:
    """Tankkoerper (Profilprisma geschnitten mit Querschnittsprisma), um g aufgedickt, nur x xa..xb, z >= TANK_Z0."""
    seite = extrude(Plane.XZ * _profil_face(g), amount=Y_TANK + g + 5, both=True)
    quer = extrude(Plane.YZ.offset(xa) * _quer_face(g), amount=xb - xa)
    return seite & quer & box(xa - 1, xb + 1, -Y_TANK - 20, Y_TANK + 20, TANK_Z0, TANK_Z1 + 50)


def _tank_blech(t: Sammler) -> None:
    """Tankkoerper mit gerollter Falz an der Stirn, Schraubenkoepfen seitlich und hinterer Abkantung."""
    t.append(_koerper(0.0, TANK_X0, TANK_XT + 2))
    # gerollte Falz an der Stirn (breiter Wulst, endet bei x 1092 an der Rueckseite der Stirnwand: kein Keil davor) und eine
    # zweite Sicke dahinter, umlaufend
    for xa, xb, g in ((TANK_X0, TANK_X0 + 7, 5.0), (TANK_X0 + 34, TANK_X0 + 48, 3.5), (TANK_X0 + 62, TANK_X0 + 70, 2.5)):
        # Innenflaeche 1,5 mm in den Tank gesenkt: Ueberlappung statt Beruehrung, sonst bleibt beim Triangulieren ein Haarspalt
        falz = _koerper(g, xa, xb) - _koerper(-1.5, xa - 1, xb + 1)
        # Kanten der Rueckseite (x = xb) oben verrunden: nimmt dem Falzende an der verrundeten Stirnkante den spitzen Keil (Wand <
        # 0,5 mm)
        falz = fillet([e for e in falz.edges() if abs(e.center().X - xb) < 1e-3 and e.center().Z > 1200], 1.5)
        t.append(falz)
    # zwei runde gewoelbte Schraubenkoepfe seitlich zwischen den Baendern (Foto t39)
    for s in (-1, 1):
        for x in (1235.0, 1315.0):
            t.mat("blank", Pos(x, s * (Y_TANK - 1.5), TANK_Z0 + 105) * Sphere(13))
    # hintere Abkantung unten (waagerechte Lippe) mit Schraubenreihe ueber dem Armaturenbrett (Foto t46)
    lip = box(TANK_X1 - 4, TANK_X1 + 22, -Y_TANK + 25, Y_TANK - 25, TANK_Z0, TANK_Z0 + 6)
    t.append(lip)
    t += schraubenreihe((TANK_X1 + 14, -Y_TANK + 55, TANK_Z0 + 5), (TANK_X1 + 14, Y_TANK - 55, TANK_Z0 + 5), 6, (0, 0, 1), 15, 5)


def _tank_baender(t: Sammler) -> None:
    """Spannbaender (lackiert) ueber Oberseite und Seiten; unten Laschen, Gewindestangen nach unten in den Flansch."""
    for xb in X_BAND:
        band = _koerper(BAND_S, xb - BAND_B / 2, xb + BAND_B / 2) - _koerper(-1.5, xb - BAND_B / 2 - 1, xb + BAND_B / 2 + 1)
        band = band & box(xb - 30, xb + 30, -400, 400, BAND_ZE, TANK_Z1 + 40)
        t.mat("lack", band)
        for s in (-1, 1):
            ya, yb = sorted((s * (Y_TANK + BAND_S - 2), s * (FL_Y + 4)))
            t.mat("lack", box(xb - BAND_B / 2, xb + BAND_B / 2, ya, yb, BAND_ZE - 8, BAND_ZE))     # Lasche
            t.mat("blank", Pos(xb, s * Y_ROD, TANK_Z0) * _zyl(6, BAND_ZE + 14 - TANK_Z0))
            t.mat("blank", sechskant((xb, s * Y_ROD, BAND_ZE), (0, 0, 1), 17, 8))


def _tank_stutzen(t: Sammler) -> None:
    """Einfuellstutzen mit Fluegelmutter-Deckel oben und Haltekette."""
    zm1 = _zq(Y_STUTZEN)                                        # Dachhoehe an der Stutzenachse (Haubenbogen)
    zs = zm1 - 30
    t.append(Pos(X_STUTZEN, Y_STUTZEN, zs) * _zyl(42, 62))
    t.append(Pos(X_STUTZEN, Y_STUTZEN, zm1 - 9) * _zyl(56, 12))  # Schweisskragen (reicht in die Bombierung)
    zd = zs + 62
    deckel = Pos(X_STUTZEN, Y_STUTZEN, zd) * _zyl(54, 16)
    deckel = fillet(deckel.edges().group_by(Axis.Z)[-1], 5)
    t.append(deckel)
    t.mat("blank", Pos(X_STUTZEN, Y_STUTZEN, zd + 16) * _zyl(16, 26))
    for s in (-1, 1):                                          # Fluegel
        fl = Pos(X_STUTZEN, Y_STUTZEN + s * 30, zd + 22) * Rot(s * -15, 0, 0) * box(-6, 6, -22, 22, -6, 22)
        t.mat("blank", fillet(fl.edges().filter_by(Axis.X).group_by(Axis.Z)[-1], 5))
    # Haltekette Deckel
    t.mat("blank", stab((X_STUTZEN + 50, Y_STUTZEN, zd + 4), (X_STUTZEN + 75, Y_STUTZEN + 20, zm1 - 15), 3))


def _tank_kanne(t: Sammler) -> None:
    """Kleine Kanne rechts oben (gerippter Deckel, Buegel)."""
    zk = _zq(Y_STUTZEN) - 25
    kanne = Pos(X_KANNE, Y_KANNE, zk) * _zyl(55, 95)
    kanne = fillet(kanne.edges().group_by(Axis.Z)[-1], 6)
    t.append(kanne)
    for i in range(3):                                         # Rippen am Mantel
        t.append(Pos(X_KANNE, Y_KANNE, zk + 40 + i * 18) * Torus(55, 3))
    t.append(Pos(X_KANNE, Y_KANNE, zk + 95) * _zyl(40, 14))
    t.mat("blank", Pos(X_KANNE, Y_KANNE, zk + 109) * Sphere(12))
    t.mat("blank", Pos(X_KANNE, Y_KANNE, zk + 80) * Rot(90, 0, 0) * (Torus(52, 4) - box(-80, 80, -80, 0, -10, 10)))


def _tank_hahn(t: Sammler) -> None:
    """Kraftstoffhahn (Messing -> blank) unten rechts am Tank, kompakt innerhalb |y| < 355 (aussen daneben laufen
    die Hydraulikleitungen), Leitung hinab durch eine Bohrung im Flansch."""
    xh, yh, zh = X_HAHN, Y_TANK - 6, TANK_Z0 + 42
    t.mat("blank", rad_y(xh, yh + 8, zh, 10, 16))              # Anschlussstutzen
    t.mat("blank", box(xh - 14, xh + 14, yh + 12, yh + 24, zh - 14, zh + 14))  # Hahnkoerper
    t.mat("blank", Pos(xh, yh + 18, zh + 14) * _zyl(5, 12))
    t.mat("lack", Pos(xh, yh + 18, zh + 26) * box(-30, 30, -5, 5, 0, 8))   # Knebel
    # Leitung bis auf den Flansch (Tankteil); unterhalb der Flanschbohrung geht sie im Unterbau weiter (_unterbau)
    t.mat("blank", rohr_glatt([(xh, yh + 18, zh - 8), (xh, LTG_Y, zh - 20), (xh, LTG_Y, FL_Z0)], 6))


def tank() -> Sammler:
    """Tank in Haubenform mit Falz, Spannbaendern, Einfuellstutzen, Kanne und Kraftstoffhahn."""
    t = Sammler("zink")
    _tank_blech(t)
    _tank_baender(t)
    _tank_stutzen(t)
    _tank_kanne(t)
    _tank_hahn(t)
    return t


# ---------------- Tankunterbau und Werkzeugkaesten ----------------
def _unterbau_flansch(t: Sammler) -> None:
    """Auflageflansch (Winkelblech, seitlich ueberstehend) mit Bohrungen fuer die Kraftstoffleitung (die Leitung
    des Tanks laeuft frei hindurch)."""
    fl = box(TANK_X0, FL_X1, -FL_Y, FL_Y, FL_Z0, FL_ZT)
    for s in (-1, 1):
        fl = fl - Pos(X_HAHN, s * LTG_Y, FL_Z0 - 1) * _zyl(8.5, FL_DICKE + 2)
    t.append(fl)


def _unterbau_baender(t: Sammler, s: int) -> None:
    """Knotenbleche unter dem Flansch (je zwei pro Spannband) und Gewindestangen mit Muttern darunter."""
    for xb in X_BAND:
        for dx in (-16, 16):
            kn = Polyline((s * (UNTERBAU_Y - 1), FL_Z0 + 1), (s * (FL_Y - 3), FL_Z0 + 1),
                          (s * (UNTERBAU_Y - 1), FL_Z0 - 34), close=True)
            t.append(extrude(Plane.YZ.offset(xb + dx - 3) * make_face(kn), amount=6))
        t.mat("blank", Pos(xb, s * Y_ROD, FL_Z0 - 30) * _zyl(6, 32))
        t.mat("blank", sechskant((xb, s * Y_ROD, FL_Z0), (0, 0, -1), 17, 8))
        t.mat("blank", sechskant((xb, s * Y_ROD, FL_Z0 - 8), (0, 0, -1), 17, 8))


def _unterbau_stuetzen(t: Sammler, s: int) -> None:
    """Stuetzen einer Seite: Flachstahl aussen neben der Glocke bis unter das Konsolenblech, Fussplatte auf dem
    Laengstraeger-Obergurt, Knotenblech und Schrauben."""
    yf0, yf1 = sorted((s * GLOCKE_Y, s * (GLOCKE_Y + 22)))
    yp0, yp1 = sorted((s * (Y_TRAEGER + 22), s * (UNTERBAU_Y)))
    for xs in STUETZEN_X:
        t.append(box(xs - 30, xs + 30, yf0, yf1, TRAEGER_Z1, TK_Z0 - TK_SHELF + 1))
        t.append(box(xs - 45, xs + 45, yp0, yp1, TRAEGER_Z1, TRAEGER_Z1 + 12))
        # Knotenblech Stuetze -> Fussplatte (aussen)
        kn = Polyline((s * (GLOCKE_Y + 20), TRAEGER_Z1 + 10), (s * (UNTERBAU_Y - 2), TRAEGER_Z1 + 10),
                      (s * (GLOCKE_Y + 20), TRAEGER_Z1 + 90), close=True)
        t.append(extrude(Plane.YZ.offset(xs - 6) * make_face(kn), amount=12))
        ysc = s * (Y_TRAEGER + 40)
        t += [sechskant((xs + dx, ysc, TRAEGER_Z1 + 12), (0, 0, 1), 16, 7) for dx in (-28, 28)]


def _unterbau(t: Sammler) -> None:
    """Mittelblock unter dem Tank (frei ueber der Kupplungsglocke) mit Auflageflansch (Winkelblech, seitlich
    ueberstehend, Knotenbleche) oben; je zwei Stuetzen pro Seite auf die Laengstraeger. Der Tank liegt nur auf
    dem Flansch."""
    # Mittelblock bis unter den Flansch
    t.append(box(TANK_X0, XW0, -KB_Y, KB_Y, UB_PLATTE_Z0, FL_Z0 + 1))
    # Kraftstoffleitung unter der Flanschbohrung aussen neben dem Werkzeugkasten hinab (oberes Stueck gehoert zum Tank)
    z_end = TK_Z0 + 85
    t.mat("blank", rohr_glatt([(X_HAHN, LTG_Y, FL_Z0), (X_HAHN, LTG_Y, z_end)], 6))
    t.mat("blank", box(X_HAHN - 10, X_HAHN + 10, UNTERBAU_Y - 1, LTG_Y + 6, z_end - 10, z_end + 10))   # Halter an der Kastenwand
    _unterbau_flansch(t)
    for s in (-1, 1):
        _unterbau_baender(t, s)
        _unterbau_stuetzen(t, s)


def _tankkasten(t: Sammler, s: int) -> None:
    """Ein flacher Werkzeugkasten neben dem Tank (Video 054-066 links, 137/158 rechts): Kasten mit uebergreifendem
    Deckel, Ueberwurf mit Fluegelmutter, Scharniere innen, auf einem Konsolenblech (Lack), darunter offen."""
    xm = (TK_X0 + TK_X1) / 2
    yi = s * (KB_Y + 5)                                   # innere (Scharnier-) Seite
    yo = s * UNTERBAU_Y                                   # aussen
    ya, yb = sorted((yi, yo))
    t.append(kasten_rund(TK_X0, TK_X1, ya, yb, TK_Z0, TK_Z1, 6))
    # Deckel: Platte + umlaufender Rand (Lippe) ueber dem Koerper, aussen und vorn/hinten ueberstehend
    d0, d1 = sorted((yi, yo + s * 4))
    t.append(kasten_rund(TK_X0 - 4, TK_X1 + 4, d0, d1, TK_Z1, TK_Z1 + 10, 6))
    lip = (kasten_rund(TK_X0 - 4, TK_X1 + 4, d0, d1, TK_Z1 - 14, TK_Z1, 6)
           - kasten_rund(TK_X0, TK_X1, ya, yb, TK_Z1 - 15, TK_Z1 + 1, 6))
    t.append(lip)
    # Versteifungssicke in der Deckelflaeche
    t.append(kasten_rund(TK_X0 + 40, TK_X1 - 40, ya + 20, yb - 20, TK_Z1 + 10, TK_Z1 + 14, 10))
    # Ueberwurf (Haken) aussen mit Fluegelmutter
    yh0, yh1 = sorted((yo + s * 4, yo + s * 8))
    t.mat("blank", box(xm - 22, xm + 22, yh0, yh1, TK_Z1 - 60, TK_Z1 + 6))                  # Laschenblech
    t.mat("blank", rad_y(xm, yo + s * 14, TK_Z1 - 52, 6, 12))                               # Bolzen
    t.mat("blank", rad_y(xm, yo + s * 20, TK_Z1 - 52, 10, 8))                               # Mutterkoerper
    t.mat("blank", Pos(xm, yo + s * 20, TK_Z1 - 52) * box(-5, 5, -7, 7, -22, 22))           # Fluegel
    # Scharniere innen (zwei Stueck) und Nietreihe an der Aussenwand
    for xs in (TK_X0 + 70, TK_X1 - 70):
        t.mat("blank", rad_x(xs, yi, TK_Z1 + 4, 7, 60))
    t += schraubenreihe((TK_X0 + 35, yo, TK_Z0 + 22), (TK_X1 - 35, yo, TK_Z0 + 22), 5, (0, s, 0), 14, 5)
    # Konsolenblech (Lack) unter dem Kasten und seitlicher Bord, vorn und hinten ueberstehend
    c0, c1 = sorted((s * KB_Y, s * (UNTERBAU_Y + 10)))
    # endet vor der Plattform (DECK_X0): der Kasten steht hinten mit ~20 mm auf der Plattformkante
    t.append(box(TK_X0 - 15, DECK_X0, c0, c1, TK_Z0 - TK_SHELF, TK_Z0))
    b0, b1 = sorted((s * (UNTERBAU_Y + 10), s * (UNTERBAU_Y + 16)))
    t.append(box(TK_X0 - 15, DECK_X0, b0, b1, TK_Z0 - TK_SHELF - 30, TK_Z0))
    # Knotenbleche zwischen Konsolenblech und Stuetze
    for xs in STUETZEN_X:
        kn = Polyline((s * (GLOCKE_Y + 22), TK_Z0 - TK_SHELF), (s * (GLOCKE_Y + 22), TK_Z0 - TK_SHELF - 90),
                      (s * (GLOCKE_Y + 120), TK_Z0 - TK_SHELF), close=True)
        t.append(extrude(Plane.YZ.offset(xs - 5) * make_face(kn), amount=10))


def _tankkaesten(t: Sammler) -> None:
    """Flache Werkzeugkaesten links und rechts neben dem Tank."""
    for s in (-1, 1):
        _tankkasten(t, s)


# ---------------- Armaturenkasten ----------------
def _dash_ebene() -> Plane:
    """Ebene der schraegen Front des Armaturenkastens: lokal x = y global, lokal y = nach oben entlang der Front,
    z = Flaechennormale (nach hinten oben, zum Fahrer)."""
    zm = (DASH_ZU + DASH_ZO) / 2
    xm = (DASH_XU + DASH_XO) / 2
    n = Vector(DASH_ZO - DASH_ZU, 0, DASH_XU - DASH_XO).normalized()
    return Plane(origin=(xm, 0, zm), x_dir=(0, 1, 0), z_dir=n)


def _instrument(t: Sammler, loc: Location, u: float, v: float, r: float, blatt: str = "zifferblatt",
                winkel: float = 35, marke: bool = False) -> None:
    """Rundinstrument auf der Front (lokale Koordinaten u, v): Chromring, Zifferblatt, Zeiger, Skalenstriche."""
    t.mat("chrom", loc * (Pos(u, v, -1) * (_zyl(r, 8) - _zyl(r - 6, 10))))
    t.mat(blatt, loc * (Pos(u, v, -1) * _zyl(r - 5, 5)))
    zeiger = "schwarz" if blatt != "schwarz" else "zifferblatt"
    t.mat(zeiger, loc * (Pos(u, v, 4) * Rot(0, 0, winkel) * box(-2.2, 2.2, -2, r * 0.7, 0, 2.5)))
    t.mat(zeiger, loc * (Pos(u, v, 4) * _zyl(4.5, 4)))
    for k in range(5):
        a = math.radians(-60 + k * 30)
        rr = r - 10
        t.mat(zeiger, loc * (Pos(u + rr * math.sin(a), v + rr * math.cos(a), 3.5) * Rot(0, 0, -math.degrees(a))
                             * box(-2.2, 2.2, -4, 4, 0, 2)))
    if marke:                                             # rote Marke im Zifferblatt (Kontrolle)
        t.mat("ruecklicht", loc * (Pos(u, v - r * 0.38, 4) * box(-8, 8, -5, 5, 0, 2.5)))


def _dash_kasten(t: Sammler) -> None:
    """Kastenkoerper mit schraeger Front, Bodenwinkel (Abdeckleiste) unten und Schrauben."""
    yc = (DASH_Y0 + DASH_Y1) / 2
    w2 = (DASH_Y1 - DASH_Y0) / 2
    prof = make_face(Polyline((DASH_X0, DASH_ZU), (DASH_XU, DASH_ZU), (DASH_XO, DASH_ZO), (DASH_X0, DASH_ZO), close=True))
    t.mat("tuerkis", Pos(0, yc, 0) * extrude(Plane.XZ * prof, amount=w2, both=True))
    t.mat("tuerkis", Pos(0, yc, 0) * box(DASH_XU - 8, DASH_XU + 3, -w2 - 4, w2 + 4, DASH_ZU, DASH_ZU + 14))
    for y in (DASH_Y0 + 25, DASH_Y1 - 25):
        t.mat("blank", sechskant((DASH_XU - 12, y, DASH_ZU), (0, 0, -1), 14, 5))


def _zuendschloss(t: Sammler, loc: Location) -> None:
    """Zuendschloss mit Hebel mittig rechts; der Schluessel steckt und haengt nach unten (Short 0:45..0:50)."""
    uz, vz = -26.0, -4.0
    t.mat("chrom", loc * (Pos(uz, vz, 0) * (_zyl(19, 6) - _zyl(12, 8))))
    t.mat("schwarz", loc * (Pos(uz, vz, 1) * _zyl(12, 6)))
    t.mat("blank", loc * (Pos(uz, vz, 6) * box(-3, 3, -9, 9, 0, 8)))                        # Schluesselbart
    t.mat("blank", loc * (Pos(uz, vz - 8, 11) * box(-3.5, 3.5, -34, 0, -1.5, 1.5)))                # Schaft/Reide
    t.mat("blank", loc * (Pos(uz + 5, vz - 30, 11) * box(-2, 2, -4, 4, -1.5, 1.5)))                # Bart
    t.mat("blank", loc * (Pos(uz, vz - 50, 11) * (_zyl(9, 3) - _zyl(5, 4))))                         # Griff-Ring
    # Hebel nach rechts unten bis zum Instrument (Video 2:09)
    t.mat("chrom", loc * stab((uz, vz, 8), (uz + 64, vz - 10, 12), 3.6))
    t.mat("chrom", loc * (Pos(uz + 64, vz - 10, 12) * Sphere(6)))


def _dash_front(t: Sammler) -> None:
    """Frontplatte mit Rundinstrument links, drei kleinen Knoepfen, Zuendschloss und zwei Instrumenten rechts."""
    yc = (DASH_Y0 + DASH_Y1) / 2
    w2 = (DASH_Y1 - DASH_Y0) / 2
    loc = Location(_dash_ebene())
    # Frontplatte mit Rundkanten (leicht erhoben)
    plat = extrude(Pos(yc, 0) * RectangleRounded(2 * w2 - 24, 128, 20), amount=3)
    t.mat("tuerkis", loc * (Pos(0, 0, -1) * plat))
    _instrument(t, loc, -236, -4, 38, marke=True, winkel=20)          # grosses Rundinstrument links unten (Video 128)
    # kleine Knoepfe oben
    for u, r in ((-186, 10), (-148, 11), (-112, 13), (-74, 14)):
        t.mat("chrom", loc * (Pos(u, 40, 2) * _zyl(r, 5)))
        t.mat("schwarz", loc * (Pos(u, 40, 6) * _zyl(r - 5, 7)))
    _zuendschloss(t, loc)
    # rechts zwei Instrumente uebereinander
    _instrument(t, loc, 47, 38, 25, winkel=-25)          # Messung Video 2:09: Instrumente bei y ~ +47 (nicht +106)
    _instrument(t, loc, 47, -24, 25, winkel=30)


def _handgas(t: Sammler) -> None:
    """Handgashebel mit Rastsegment rechts neben dem Armaturenkasten (am Lenksaeulenwinkel, siehe _lenkung)."""
    yh = Y_HANDGAS
    xh, zh = HANDGAS_FUSS
    seg = Plane.XZ.offset(-yh) * Pos(xh, zh - 10) * (Circle(62) - Circle(45))
    seg = extrude(seg, amount=4, both=True) & box(xh - 4, xh + 80, yh - 10, yh + 10, zh - 10, zh + 45)
    t.append(seg)
    # lange duenne Stange (Video 122/128), reicht ueber den Kastenrand
    gx, gz = HANDGAS_OBEN
    t.mat("blank", stab((xh + 6, yh, zh), (gx, yh, gz), 4))
    t.mat("schwarz", Pos(gx, yh, gz) * Sphere(10))               # kleiner Knopf oben
    t.mat("blank", rad_y(xh + 6, yh, zh, 10, 12))


def _konsole(t: Sammler) -> None:
    """Armaturenkasten (tuerkisgruen) unter dem Tankueberhang mit Instrumenten, Zuendschloss und Handgashebel."""
    _dash_kasten(t)
    _dash_front(t)
    _handgas(t)


# ---------------- Lenkung ----------------
def _lenkrad(t: Sammler, b: Vector, d: Vector) -> None:
    """Vierspeichen-Lenkrad mit Hupenknopf im lokalen System (z = Saeulenachse d, Mitte b)."""
    xd = (Vector(0, 1, 0) - d * d.Y).normalized()
    loc = Location(Plane(origin=b, x_dir=xd, z_dir=d))
    rad = Sammler("schwarz")
    rad.append(Torus(R_KRANZ, R_KRANZ_Q))
    rad.append(Pos(0, 0, -40) * _zyl(32, 72))  # Nabe
    for k in range(4):                                         # Speichen (Rundstahl, gekroepft)
        w = math.radians(45 + k * 90)
        cw, sw = math.cos(w), math.sin(w)
        rad.mat("blank", stab((28 * cw, 28 * sw, 20), (120 * cw, 120 * sw, 4), 8))
        rad.mat("blank", stab((120 * cw, 120 * sw, 4), ((R_KRANZ - 4) * cw, (R_KRANZ - 4) * sw, 0), 8))
        rad.mat("blank", Pos(120 * cw, 120 * sw, 4) * Sphere(8))
    rad.mat("chrom", Pos(0, 0, 18) * _zyl(44, 16))  # Nabenstern
    rad.mat("chrom", Pos(0, 0, 34) * (_zyl(36, 8) - _zyl(28, 20)))
    knopf = Pos(0, 0, 34) * _zyl(28, 14)
    rad.mat("schwarz", fillet(knopf.edges().group_by(Axis.Z)[-1], 8))   # Hupenknopf
    for mat, lst in rad.schichten().items():
        t.mat(mat, [loc * s for s in lst])


def _lenkung(t: Sammler) -> None:
    """Winkelblech mit Schneckengetriebe-Gehaeuse, duenne Saeule (Mantelrohr Ø 35), Lenkspindel und Lenkrad."""
    a, b = LENK_FUSS, LENK_MITTE
    d = (b - a).normalized()
    # Winkelblech am Mittelblock rechts neben dem Armaturenkasten, Schneckengetriebe-Gehaeuse
    px = XW0 + 16
    t.append(box(XW0, px, 150.0, 255.0, 985.0, DASH_ZO))
    for dy in (-42, 42):
        for zz in (1005.0, 1060.0):
            t.mat("blank", sechskant((px, a.Y + dy, zz), (1, 0, 0), 16, 7))
    t.append(stab((px - 1, a.Y, a.Z), a + d * 30, 24))        # Lagerstutzen / Gehaeuse (unter der Tankkante 1090)
    t.append(stab(a + d * 24, a + d * 52, 36))                 # Gehaeuseabschluss
    t.append(stab(a + d * 50, b - d * 70, 17.5))               # Mantelrohr
    t.mat("blank", stab(b - d * 72, b - d * 40, 8))            # Lenkspindel
    _lenkrad(t, b, d)


# ---------------- Bodenblech, Fussraumboden, Oel-Stutzen ----------------
def _bodenblech(t: Sammler) -> None:
    """Bodenblech auf der Plattform: hinter dem Fussraum bis zum Sitzsockel und seitlich neben dem Fussraum;
    der Fussraum selbst ist ausgeschnitten (Seitenwaende und Inspektionsdeckel in rumpf.py). Glatt (Video 130/137);
    Riffel nur auf den Pedal-Trittflaechen."""
    xb0, xb1 = XK + 5, BODEN_X1
    fw = box(FW_X0 - 1, FW_X1, FW_Y0 - 10 - 1, FW_Y1 + 10 + 1, DECK_Z - 1, BODEN_Z + 1)
    # links Streifen -355..-311, hinter dem Fussraum voll
    t.append(box(xb0, xb1, -(FW_Y1 + 10), FW_Y1 + 10, DECK_Z, BODEN_Z) - fw)


def _fussraumboden(t: Sammler) -> None:
    """Fussraumboden: Blech auf dem Getriebe aus mehreren Bodenplatten mit Stossfugen (Video 2:09, Frame 129): zwei
    Laengsfugen (y -174, y -104) laufen von vorn bis zum Stutzen, links davon eine Querfuge bei x 1557 (nur im
    schmalen Streifen an der Wand); Sechskantschrauben mit Scheibe (rostig, ~18 SW) sitzen in Reihen beidseits der
    Laengsfuge. Darunter ein durchgehendes Blech."""
    zf = FW_Z1                                                 # Oberkante Fussraumboden (abgesenkt, Video 121-140)
    t.append(box(FW_X0, FW_X1, FW_Y0, FW_Y1, FW_Z0, zf - FUGE_T))
    ygr = [FW_Y0]
    for fy in FUGE_Y:
        ygr += [fy - FUGE_B / 2, fy + FUGE_B / 2]
    ygr.append(FW_Y1)
    for i in range(0, len(ygr), 2):
        y0, y1 = ygr[i], ygr[i + 1]
        if i == 0:                                              # Wandstreifen: Querfuge
            t.append(box(FW_X0, FUGE_X - FUGE_B / 2, y0, y1, zf - FUGE_T - 1, zf))
            t.append(box(FUGE_X + FUGE_B / 2, FW_X1, y0, y1, zf - FUGE_T - 1, zf))
        else:
            t.append(box(FW_X0, FW_X1, y0, y1, zf - FUGE_T - 1, zf))


def _bodenschrauben(t: Sammler) -> None:
    """Schraubenreihen im Fussraumboden und auf dem Bodenblech."""
    zf = FW_Z1
    xb0, xb1 = XK + 5, BODEN_X1
    for yb, x0b, dx in ((-190.0, 1561.0, 140.0), (-160.0, 1540.0, 78.0), (-98.0, 1552.0, 140.0), (FW_Y1 - 22, FW_X0 + 30, 62.0)):
        x = x0b
        while x < (1955.0 if yb < 100 else FW_X1 - 20):      # links endet die Reihe vor dem Getriebedeckel (rumpf.py, x ab 1975)
            if not (yb > 100 and 1590.0 < x < 1800.0):       # rechts Luecke fuer Bremspedale (Manschette / Trittplatte)
                t += schraube((x, yb, zf), (0, 0, 1), 18, 6)
            x += dx
    zb = BODEN_Z
    t += schraubenreihe((xb0 + 25, -335, zb), (xb1 - 25, -335, zb), 9, (0, 0, 1), 18, 6)       # links neben dem Fussraum
    t += schraubenreihe((FW_X1 + 25, 335, zb), (xb1 - 25, 335, zb), 3, (0, 0, 1), 18, 6)       # rechts nur hinter dem Fussraum
    t += schraubenreihe((xb1 - 25, -230, zb), (xb1 - 25, -90, zb), 2, (0, 0, 1), 18, 6)
    t += schraubenreihe((xb1 - 25, 90, zb), (xb1 - 25, 230, zb), 2, (0, 0, 1), 18, 6)


def _oel_stutzen(t: Sammler) -> None:
    """Sechskant-Stutzen im Boden (Video 2:09: blaugrauer Zylinder mit grosser Sechskantmutter, Kopf mit Bohrung):
    Oel-Einfuell-/Entlueftungsstutzen des Getriebes, steht auf einem Flansch im Bodenblech."""
    zf = FW_Z1
    sx_, sy_ = STUTZEN
    t.append(Pos(sx_, sy_, zf) * _zyl(58, 8))          # Flanschplatte
    t += schraubenkreis((sx_, sy_, zf + 8), (0, 0, 1), 46, 4, 14, 5, 45)
    zk_ = zf + STUTZEN_H - 50                                   # Oberkante Koerper
    t.mat("zink", Pos(sx_, sy_, zf + 8) * _zyl(40, zk_ - zf - 8))
    t.mat("zink", Pos(sx_, sy_, zk_) * Cone(40, 28, 12, align=(Align.CENTER, Align.CENTER, Align.MIN)))      # Schulter
    # grosse Sechskantmutter
    t.mat("blank", sechskant((sx_, sy_, zk_ + 12), (0, 0, 1), 54, 24))
    kopf = sechskant((sx_, sy_, zk_ + 36), (0, 0, 1), 38, 14)                                                # Verschlussschraube
    t.mat("blank", kopf - Pos(sx_, sy_, zk_ + 40) * _zyl(8, 20))


# ---------------- Schalthebel ----------------
def _schalthebel(t: Sammler) -> None:
    """Schalthebel (Video 2:09/131/137/138): schwarzer flacher Gummibalg im Boden, duenner Hebel schwingt nach
    links-vorn zum Armaturenkasten, schwarze Kugel knapp hinter und ueber dem unteren Kastenrand."""
    zf = FW_Z1
    fx, fy = SCHALT
    t.append(Pos(fx, fy, zf) * _zyl(64, 6))     # Abdeckplatte unter dem Balg
    t.mat("gummi", Pos(fx, fy, zf + 6 + 16) * Torus(44, 16))                                       # Wulst (flacher Balg)
    t.mat("gummi", Pos(fx, fy, zf + 6 + 16) * Cone(46, 22, 40, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("gummi", Pos(fx, fy, zf + 6 + 54) * Torus(22, 6))                                        # Spannring oben
    knauf = SCHALT_KNAUF
    # Review 3 (Short 0:45..0:50): duenne Stange Ø ~13, kleine Kugel
    t.append(rohr_glatt([(fx, fy, zf + 56), (fx + 6, fy - 55, 930.0), knauf], 6.5, 160))
    t.mat("schwarz", Pos(knauf[0] - 3, knauf[1], knauf[2] + 12) * Sphere(23))


# ---------------- Pedale ----------------
def _pedal(t: Sammler, x: float, y: float) -> None:
    """Pendelpedal: runder Hebel (Ø 30) steigt aus einem Schlitz mit Gummimanschette im Fussraumboden schraeg nach
    hinten oben zu einer geneigten, geriffelten Trittplatte (Normale zum Fahrer)."""
    zf = FW_Z1
    t.mat("gummi", box(x - 30, x + 30, y - 38, y + 38, zf, zf + 8))               # Durchfuehrungsmanschette
    _trittplatte(t, Vector(x, y, zf + 8), Vector(x + PED_DX, y, zf + 8 + PED_DZ))


def _bremspedale(t: Sammler) -> None:
    """Bremspedale (links / rechts Lenkbremse) unter dem Lenkrad; Verbindungsklinke (Sperrstange) zwischen den
    Platten. Darunter (nur dort, wo unter dem Blech Luft ist, also |y| > 255 neben dem Getriebegehaeuse) laufen
    Hebel und Zugstange zum Lenkbremsgehaeuse; ueber dem Getriebe sind sie verdeckt."""
    zf = FW_Z1
    for xb_, yb_ in PED_BREMSE:
        _pedal(t, xb_, yb_)
    pl_k = Plane(origin=Vector(PED_X1, PED_KLINKE_Y, zf + 8 + PED_DZ), x_dir=(0, 1, 0), z_dir=(0.5, 0, 0.866))
    # Klinke zwischen den Platten (Luecke 255..261 -> Bolzen)
    t.mat("blank", pl_k * Pos(0, 0, 4) * Box(30, 8, 8))
    # rechtes Bremspedal (y 298): Hebel durch das Blech nach unten, Gabelkopf, Zugstange z 676 nach hinten zum Hebel am
    # Lenkbremsgehaeuse
    xr, yr = PED_BREMSE[1]
    # Achse der Zugstange 676 (Gehaeuse oben 628, Blech unten 716)
    zr = FW_Z0 - 40.0
    t.append(stab((xr, yr, zr), (xr, yr, zf + 8), 12))
    t.mat("blank", Pos(xr, yr, zr) * box(-16, 16, -14, 14, -14, 14))                     # Gabelkopf
    t.mat("blank", rad_y(xr, yr, zr, 5, 40))                                             # Gabelbolzen
    t.mat("blank", stab((xr + 12, yr, zr), (X_BREMSE - 8, yr, zr), 7))                   # Zugstange
    # Hebel auf dem Lenkbremsgehaeuse (Rippe bis 630)
    t.mat("blank", box(X_BREMSE - 14, X_BREMSE + 14, yr - 9, yr + 9, 631.0, zr + 16))
    t.mat("blank", rad_y(X_BREMSE, yr, zr, 5, 36))                                       # Bolzen Hebel


def _klinke_boden(t: Sammler) -> None:
    """Klinke / Zahnstange am Boden vor dem Sitz (Short 0:17/0:18.5): flache, laengs geschlitzte Stange mit Auge,
    quer vor der Sitzschale auf dem Bodenblech, leicht schraeg."""
    w = math.radians(10)
    pl_b = Plane(origin=(*KLINKE_BODEN, BODEN_Z), x_dir=(math.sin(w), math.cos(w), 0), z_dir=(0, 0, 1))
    bar = Pos(0, 0, 4) * Box(250, 38, 6)
    for dx in (-70, 0, 70):
        bar = bar - Pos(dx, 0, 4) * Box(48, 12, 10)
    t.mat("blank", pl_b * bar)
    t.mat("blank", pl_b * (Pos(-125, 0, 7) * (_zyl(20, 6) - _zyl(8, 8))))                    # Auge am Ende (Bolzenloch)
    t.mat("blank", pl_b * (Pos(105, 0, 4) * box(-14, 14, -26, 26, -4, 10)))                  # Lagerblock / Klemme


def _kupplungspedal(t: Sammler) -> None:
    """Kupplungspedal: Gabelkopf mit Bolzen auf dem Boden (Video 2:09, Kamera-Fit t020: Gabelkopf x ~1665, y ~100;
    waagerechte Zugstange auf dem Blech nach hinten-links zum Durchtritt bei x ~1720, y ~50), Zunge in der Gabel
    und Pedalhebel mit Trittplatte (Lenkrad ueber dem Pedal)."""
    zf = FW_Z1
    kx, ky = PED_KUPPLUNG
    za = zf + 28.0                                                                        # Achse des Gestaenges ueber dem Boden
    A = Vector(kx, ky, za)
    B = Vector(*PED_KUPPLUNG_DURCHTRITT, za)
    u = (B - A).normalized()
    pl_g = Plane(origin=A, x_dir=u, z_dir=(0, 0, 1))
    t.mat("zink", pl_g * (Pos(6, 0, 0) * Box(52, 36, 30) - Pos(-8, 0, 0) * Box(44, 18, 32)))   # Gabelkopf mit Schlitz
    t.mat("blank", pl_g * (Pos(-8, 0, 0) * Rot(90, 0, 0) * Cylinder(5, 46)))               # Gabelbolzen quer
    t.mat("zink", stab(A + u * 30, B, 8))                                                   # Zugstange
    t.mat("gummi", box(B.X - 26, B.X + 26, B.Y - 26, B.Y + 26, zf, zf + 8))                 # Durchtritt Zugstange
    # Gegenmutter
    t.mat("blank", Pos(*(A + u * 44)) * Rot(0, 0, math.degrees(math.atan2(u.Y, u.X))) * box(-5, 5, -10, 10, -10, 10))
    # Kupplungshebel: Zunge in der Gabel -> Pedalhebel
    t.append(box(kx - 17, kx + 1, ky - 4.5, ky + 4.5, za - 12, za + 40))                    # Zunge in der Gabel
    _trittplatte(t, Vector(kx - 8, ky, za + 34), Vector(kx + PED_DX, ky, zf + 8 + PED_DZ + 20))


def _fussraum(t: Sammler) -> None:
    """Bodenblech, Fussraumboden, Oel-Stutzen, Schalthebel und Pedale."""
    _bodenblech(t)
    _fussraumboden(t)
    _bodenschrauben(t)
    _oel_stutzen(t)
    _schalthebel(t)
    _bremspedale(t)
    _klinke_boden(t)
    _kupplungspedal(t)


# ---------------- Sitz ----------------
def _sitz_schale(t: Sammler) -> None:
    """Tiefe Blechschale mit schwarzem Kunstlederpolster (Video 128-140): Ellipsenrand, tiefe Mulde ohne Loecher,
    umgebordelter Rand, Polster mit weisser Biese und hochgezogenem Rueckenwulst hinten, Sitztraeger unter der
    Mitte. Rechts neben dem Sitz (y 225..305) bleibt ein Streifen fuer den Steuerblock mit Hebel (planierschild.py)
    frei."""
    A, B, tt, zb = SITZ_A, SITZ_B, SITZ_T, SITZ_ZB
    ea, eb = SITZ_EA, SITZ_EB
    ec = SITZ_TIEFE / (1 - math.sqrt(1 - (A / ea) ** 2))          # Muldentiefe am Rand der x-Achse
    zc = zb + ec

    def ell(dz: float = 0.0) -> Solid:
        """Muldenellipsoid, um dz nach oben verschoben; der Boden der Schale liegt auf seiner Unterseite."""
        return _ellipsoid((SITZ_X, 0, zc + dz), ea, eb, ec)

    def prisma(ra: float, rb: float, z0: float, z1: float) -> Solid:
        return Pos(SITZ_X, 0, (z0 + z1) / 2) * scale(Cylinder(1, z1 - z0), by=(ra, rb, 1))

    ze = zb + SITZ_TIEFE + tt                                      # Oberkante Blechrand
    schale = (ell() - ell(tt)) & prisma(A, B, zb - 1, ze + 4)
    # umgebordelter Rand: Schuerze nach unten (folgt der Mulde) und gerollter Wulst oben (Short 0:17/0:18: dicker, rundum
    # gerollter Rand, Ø ~18)
    ring = prisma(A, B, zb - 30, ze + 4) - prisma(A - tt, B - tt, zb - 31, ze + 5)
    schuerze = ring & (ell(-SITZ_RAND_H) - ell(tt))
    zw = ze - 0.5
    wulst_pfad = Wire([Pos(SITZ_X, 0, zw) * Edge.make_ellipse(A - 5, B - 5)])
    wulst = sweep(Plane(origin=(SITZ_X + A - 5, 0, zw), z_dir=(0, 1, 0)) * Circle(9.0), path=wulst_pfad)
    # Polster (Kunstleder): fuellt die Mulde bis zu einer flacheren Oberflaeche, Rand 8 ueber dem Blechrand
    za = ze + 8
    dish = 25.0                                                    # Muldentiefe der Polsteroberflaeche
    ea2 = 520.0
    eb2 = ea2 * B / A
    ec2 = dish / (1 - math.sqrt(1 - (A / ea2) ** 2))
    top = _ellipsoid((SITZ_X, 0, za - dish + ec2), ea2, eb2, ec2)
    polster = (ell(tt) & prisma(A - tt - 1, B - tt - 1, zb, za)) - top
    # Rueckenwulst: hochgezogener Polsterrand hinten (Sichel)
    sichel = (prisma(A - tt - 1, B - tt - 1, za - 12, za + 58)
              - Pos(-62, 0, 0) * prisma(A - tt - 1, B - tt - 1, za - 13, za + 59))
    sichel = sichel & box(SITZ_X + 15, SITZ_X + A + 5, -B, B, za - 12, za + 59)
    with contextlib.suppress(Exception):
        sichel = fillet(sichel.edges().group_by(Axis.Z)[-1], 10)
    biese_pfad = Wire([Pos(SITZ_X, 0, za - 3) * Edge.make_ellipse(A - 12, B - 12)])
    biese = sweep(Plane(origin=(SITZ_X + A - 12, 0, za - 3), z_dir=(0, 1, 0)) * Circle(4.0), path=biese_pfad)
    # Sitztraeger: Block unter der Mitte (an die Schalenunterseite angepasst), seitlich Schrauben
    tx0, tx1, ty = SITZ_TRAEGER
    kz0 = zb - SITZ_TRAEGER_UNTEN
    traeger = box(SITZ_X + tx0, SITZ_X + tx1, -ty, ty, kz0, zb + 8) - ell(1)
    schrauben = [sechskant((SITZ_X + dx, s_ * ty, zb - 25), (0, s_, 0), 14, 6) for dx in (-25, 25) for s_ in (-1, 1)]

    neig = Pos(0, SITZ_Y, 0) * Pos(SITZ_X, 0, zb) * Rot(0, SITZ_NEIG, 0) * Pos(-SITZ_X, 0, -zb)
    for k in [schale, schuerze, wulst, traeger, *schrauben]:
        t.append(neig * k)
    t.mat("leder", neig * polster)
    t.mat("leder", neig * sichel)
    t.mat("zifferblatt", neig * biese)


def _sitz_sockel(t: Sammler) -> None:
    """Mittelsockel hinter dem Getriebedeckel (gepresster Kasten mit Fussplatte, unter der Sitzachse y = SITZ_Y) und
    Blattfeder-Arm: hinten im Sockel eingespannt, nach vorn unter die Sitzkonsole (zwei Lagen), Klemmplatte mit
    Buegelschrauben."""
    zb_s = BODEN_Z                                            # auf dem Bodenblech
    sx = SOCKEL_X
    ys = SITZ_Y
    t.append(kasten_rund(sx - 40, sx + 40, ys - 55, ys + 55, zb_s - 2, SOCKEL_Z1, 15))
    t.append(kasten_rund(sx - 60, sx + 60, ys - 75, ys + 75, zb_s - 2, zb_s + 10, 12))
    for dx in (-48, 48):
        for dy in (-62, 62):
            t.mat("blank", sechskant((sx + dx, ys + dy, zb_s + 10), (0, 0, 1), 14, 6))
    # Blattfeder-Arm: hinten im Sockel eingespannt, nach vorn unter die Sitzkonsole (zwei Lagen)
    kz0 = SITZ_ZB - SITZ_TRAEGER_UNTEN
    p0 = Vector(sx + 30, ys, SOCKEL_Z1 + 5)
    p1 = Vector(SITZ_X - 40, ys, kz0 + 4)
    pm = (p0 + p1) * 0.5 + Vector(0, 0, -5)
    arc = ThreePointArc(p0, pm, p1)
    for fl, dz in ((1.0, 0.0), (0.55, -14.0)):
        q = [arc.position_at(u * fl) + Vector(0, 0, dz) for u in (0, 0.5, 1)]
        path = Wire([ThreePointArc(*q)])
        prof = Plane(origin=path.position_at(0), x_dir=(0, 1, 0), z_dir=path.tangent_at(0)) * Rectangle(70, 14)
        t.mat("schwarz", sweep(prof, path=path))
    # Klemmplatte mit Buegelschrauben auf dem Sockel
    zk = SOCKEL_Z1 + 12
    t.append(box(sx - 25, sx + 25, ys - 48, ys + 48, zk, zk + 12))
    for dy in (-42, 42):
        t.mat("blank", Pos(sx, ys + dy, SOCKEL_Z1 - 30) * _zyl(6, zk + 12 - SOCKEL_Z1 + 30))
        t.mat("blank", sechskant((sx, ys + dy, zk + 12), (0, 0, 1), 14, 8))


def _sitz(t: Sammler) -> None:
    """Sitzschale mit Polster und Mittelsockel mit Blattfeder-Arm."""
    _sitz_schale(t)
    _sitz_sockel(t)


# ---------------- Fassade ----------------
def fahrerstand() -> Sammler:
    """Unterbau, Werkzeugkaesten, Armaturenkasten, Lenkung, Fussraum und Sitz (ohne Tank)."""
    t = Sammler("lack")
    _unterbau(t)
    _tankkaesten(t)
    _konsole(t)
    _lenkung(t)
    _fussraum(t)
    _sitz(t)
    return t
