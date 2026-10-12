"""Rumpf der K 55 E: Rahmen, Querblattfeder, Getriebeblock, Endantriebe, Plattform, Zugpendel.

Original-mm, X ab Maskenfront nach hinten, Y nach rechts, Z ab Boden.
Schnittstellen siehe referenz/MASSKONZEPT.md und cad/common.py (HAUPTMASSE).

Aufbau (Fotobefund fz_01/04/08, Wiking-Chassis, Prospekt):
  * zwei U-Profil-Laengstraeger (offen nach innen) mit Nietreihen, vorn ein
    Quertraeger unter der Maske mit Zugoese,
  * Querblattfeder unter der Oelwanne (x = 560), Federbuegel in der Mitte,
    die Federaugen haengen in Jochen, die auf den Kettenrahmen aufliegen,
  * Getriebeblock: runde Kupplungsglocke (Flansch bei FLANSCH_GLOCKE_X 1090, r 300
    wie das Schwungradgehaeuse des Motors, verjuengt sich kegelig) - Zwischenflansch -
    Kupplungsgehaeuse (Kasten unter dem Trittblech) - Wechselgetriebe -
    Hinterachsgehaeuse mit runden Lenkbremsdeckeln - hochkant stehender Heckkasten,
  * eckige Endantriebsgehaeuse um die Triebradachse, Flansch bei y = +-330,
  * Plattform auf DECK_Z mit Riffelblech, abgekanteten Aussenkanten, Heckschuerzen,
    Innenwangen und Konsolen (nur innerhalb y = +-430, die Kette laeuft ab y = 435),
  * Zugpendel auf einer Pendelschiene, Maul mit Steckbolzen.

Die rechte Seite (y > 0) wird gebaut und an der XZ-Ebene gespiegelt.
"""
import math
from build123d import *
from .common import (box, stab, rad_x, rad_y, ring_x, sechskant, schraube, schraubenkreis,
                     schraubenreihe, kasten_rund, Sammler,
                     Y_TRAEGER, TRAEGER_Z0, TRAEGER_Z1, DECK_Z, DECK_X0, DECK_X1, DECK_B,
                     X_TRIEB, Z_TRIEB, Y_KETTE, KETTE_B, MASKE_UK, FLANSCH_GLOCKE_X, RAHMEN_Z0, RAHMEN_Z1)

# DECK_Z wird von fahrerstand.py ueber dieses Modul importiert -> hier bewusst re-exportiert.
__all__ = ["rumpf", "DECK_Z", "DECK_X0", "DECK_X1", "DECK_B"]

# ---------------- Eigene Masse (Original-mm) ----------------
# Laengstraeger
TR_X0, TR_X1 = 100.0, 1500.0
TR_B, TR_S = 80.0, 12.0                    # Flanschbreite, Blechstaerke
TR_YI = Y_TRAEGER - TR_B / 2               # Innenkante (Flanschende) 200
TR_YA = Y_TRAEGER + TR_B / 2               # Aussenkante Steg 280

# Plattform
BLECH = 10.0                               # Trittblech (>= 1,2 mm Modell)
RIFFEL_H = 4.0                             # Riffelhoehe
DECK_UK = DECK_Z - RIFFEL_H - BLECH        # Unterkante Trittblech 776
Y_KETTE_INNEN = Y_KETTE - KETTE_B / 2      # 435: hier beginnt die Kette
Y_WANGE = Y_KETTE_INNEN - 5                # Aussenseite der Kotfluegel-Innenwange 430
X_KETTE_HINTEN = X_TRIEB + 402.0           # hinterster Punkt der Greifer am Triebrad

# Querblattfeder
X_FEDER = 560.0
FEDER_B = 90.0                             # Lagenbreite (in x)
FEDER_D = 13.0                             # Lagendicke
FEDER_N = 5
FEDER_OK = 285.0                           # Oberkante Mitte (unter der Oelwanne, z = 320)
FEDER_YE = 455.0                           # Ende Hauptlage (Federauge dahinter)
FEDER_HUB = 215.0                          # Anstieg bis zum Ende
Y_JOCH = 508.0                             # Joch nur ueber der inneren Leitradgabel-Wange (y 485..510)
Z_GABEL = RAHMEN_Z1 + 3                    # Oberkante Gabelwange
FEDER_R = (FEDER_YE ** 2 + FEDER_HUB ** 2) / (2 * FEDER_HUB)
FEDER_ZC = FEDER_OK + FEDER_R              # Kreismittelpunkt (Feder "laechelt")

# Getriebeblock
GLOCKE_X0 = FLANSCH_GLOCKE_X               # Anschlussflansch Motor / Kupplungsglocke 1090
GLOCKE_X1 = 1640.0                         # Ende Kupplungsgehaeuse = Beginn Wechselgetriebe
GLOCKE_XM = 1400.0                         # Zwischenflansch Glocke -> Kupplungsgehaeuse (vor DECK_X0 1430)
GLOCKE_ZM = 640.0                          # Achshoehe der Glocke = SG_Z in motor.py (Schwungradgehaeuse)
GLOCKE_R0 = 300.0                          # Flanschradius vorn = Schwungradgehaeuse r 300 (Oberkante 940 <= 950)
GLOCKE_R1 = 205.0                          # Radius des Glockenschafts (Oberkante 845, Tankauflage ab 962)
GLOCKE_R2 = 212.0                          # Radius Zwischenflansch (Oberkante 852, vor DECK_X0)
GLOCKE_XK = 1250.0                         # Ende des Kegels
GETR_X1 = 2080.0                           # Ende Wechselgetriebe / Beginn Hinterachse
ACHS_X1 = 2380.0                           # Ende Hinterachsgehaeuse
HECK_X1 = 2735.0                           # Rueckwand Heckkasten
GETR_Z0, GETR_Z1 = 360.0, DECK_UK          # Gehaeuse traegt das Mittelblech
X_BREMSE, Z_BREMSE, R_BREMSE = 1870.0, 600.0, 172.0
Y_BREMSE_AUSSEN = 365.0
Y_FLANSCH = 330.0
Y_LAGER = 425.0                            # Triebrad-Innennabe endet hier (Flansch r 155)
Y_ENDANTRIEB = 400.0                       # Aussenwand Endantriebsgehaeuse (Schwinglager ab y 440)
R_LAGERROHR = 165.0
Z_PENDEL = 465.0

# Lochbild-Schablonen (einmal bauen, dann nur verschieben)
_NIET = None


def niet(p, normal, r=9.0):
    """Halbrundniet: flacher Zylinder mit verrundeter Kuppe."""
    global _NIET
    if _NIET is None:
        c = Cylinder(r, 6, align=(Align.CENTER, Align.CENTER, Align.MIN))
        _NIET = fillet(c.edges().sort_by(Axis.Z)[-1], 4.0)
    return Plane(origin=Vector(*p), z_dir=Vector(*normal)) * _NIET


def schrauben_rechteck(pl: Plane, w, h, teil=110.0, sw=20, hoehe=10, r_ecke=0.0):
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


def deckel(pl: Plane, w, h, d=10.0, r=20.0, teil=110.0, sw=18):
    """Rechteckiger Gehaeusedeckel mit Schraubenkranz auf der Ebene pl (nach aussen = z_dir)."""
    platte = extrude(pl * RectangleRounded(w, h, r), amount=d)
    vorne = Plane(origin=pl.from_local_coords((0, 0, d)), x_dir=pl.x_dir, z_dir=pl.z_dir)
    return [platte] + schrauben_rechteck(vorne, w - 2.2 * sw, h - 2.2 * sw, teil, sw, 8)


# ---------------- Rahmen ----------------
def laengstraeger():
    """Rechter U-Profil-Laengstraeger, Steg aussen, Oeffnung nach innen, mit Nieten."""
    t = []
    prof = Polyline((TR_YI, TRAEGER_Z0), (TR_YA, TRAEGER_Z0), (TR_YA, TRAEGER_Z1), (TR_YI, TRAEGER_Z1),
                    (TR_YI, TRAEGER_Z1 - TR_S), (TR_YA - TR_S, TRAEGER_Z1 - TR_S),
                    (TR_YA - TR_S, TRAEGER_Z0 + TR_S), (TR_YI, TRAEGER_Z0 + TR_S), close=True)
    u = extrude(Plane.YZ.offset(TR_X0) * make_face(prof), amount=TR_X1 - TR_X0)
    t.append(u)
    # Nietreihen am Steg (zwei Reihen) und auf dem Obergurt
    for x in range(int(TR_X0) + 60, int(TR_X1) - 20, 95):
        for z in (TRAEGER_Z0 + 28, TRAEGER_Z1 - 28):
            t.append(niet((x, TR_YA, z), (0, 1, 0)))
    for x in range(int(TR_X0) + 110, int(TR_X1) - 60, 190):
        t.append(niet((x, Y_TRAEGER + 8, TRAEGER_Z1), (0, 0, 1), 8))
    # Verstaerkungsbleche (Laschen) an Motorbock-Stellen
    for xm in (560, 1260):
        t.append(box(xm - 70, xm + 70, TR_YA, TR_YA + 8, TRAEGER_Z0 + 10, TRAEGER_Z1 - 10))
        t += schraubenreihe((xm - 45, TR_YA + 8, TRAEGER_Z0 + 40), (xm + 45, TR_YA + 8, TRAEGER_Z0 + 40), 2, (0, 1, 0), 22, 10)
        t += schraubenreihe((xm - 45, TR_YA + 8, TRAEGER_Z1 - 40), (xm + 45, TR_YA + 8, TRAEGER_Z1 - 40), 2, (0, 1, 0), 22, 10)
    # Anschluss an die Kupplungsglocke: Winkel mit 4 Schrauben
    t.append(box(TR_X1 - 90, TR_X1, TR_YA, TR_YA + 10, TRAEGER_Z0, TRAEGER_Z1))
    for x in (TR_X1 - 65, TR_X1 - 25):
        for z in (TRAEGER_Z0 + 35, TRAEGER_Z1 - 35):
            t.append(rad_y(x, TR_YA + 13, z, 20, 6))                      # Unterlegscheibe 6 mm
            t.append(sechskant((x, TR_YA + 16, z), (0, 1, 0), 22, 10))
    return t


def quertraeger_vorn():
    """Quertraeger unter der Maske (Oberkante 15 mm unter MASKE_UK) mit Zugoese; nichts vor x 10."""
    t = []
    z0, z1 = 280.0, MASKE_UK - 15.0       # Oberkante 435: unter der Maskenunterkante 450, Pumpe davor frei
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


def querfeder():
    """Querblattfeder mit Federbuegeln, Federstuehlen und Jochen. Liefert (lack, schwarz)."""
    lack, schwarz = [], []
    zc, R = FEDER_ZC, FEDER_R
    for i in range(FEDER_N):
        ri = R + i * FEDER_D
        L = 2 * (FEDER_YE - i * 85.0)
        ring = ring_x(X_FEDER, 0, zc, ri + FEDER_D, ri, FEDER_B - i * 2)
        lage = ring & box(X_FEDER - 60, X_FEDER + 60, -L / 2, L / 2, zc - ri - 10, zc - ri + 320)
        schwarz.append(lage)
    # Federaugen (nach oben gerollt) und Joch auf dem Kettenrahmen
    for s in (-1, 1):
        ye = s * FEDER_YE
        z_ok = zc - math.sqrt(R ** 2 - FEDER_YE ** 2)          # Oberkante Hauptlage am Ende
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
        st = st & rad_x(X_FEDER, 0, zc, R, 200)
        lack.append(st)
    # Federbuegel (Mitte): Klemmplatten oben/unten, 4 Stehbolzen mit Muttern
    z_unten = FEDER_OK - FEDER_N * FEDER_D
    lack.append(box(X_FEDER - 62, X_FEDER + 62, -90, 90, FEDER_OK, FEDER_OK + 14))
    lack.append(box(X_FEDER - 62, X_FEDER + 62, -90, 90, z_unten - 16, z_unten))
    for xs in (-1, 1):
        for ys in (-1, 1):
            x, y = X_FEDER + xs * 52, ys * 62
            lack.append(stab((x, y, z_unten - 30), (x, y, FEDER_OK + 20), 9))
            lack.append(sechskant((x, y, FEDER_OK + 14), (0, 0, 1), 26, 6))
            lack.append(sechskant((x, y, z_unten - 16), (0, 0, -1), 26, 12))
    lack.append(Pos(X_FEDER, 0, FEDER_OK + 14) * Cylinder(15, 6, align=(Align.CENTER, Align.CENTER, Align.MIN)))  # Herzbolzen
    return lack, schwarz


# ---------------- Getriebeblock ----------------
def getriebe():
    """Mittiger Getriebeblock (symmetrisch, ganz gebaut)."""
    t = []
    # Kupplungsglocke: Flansch am Motor (Profil wie Schwungradgehaeuse), Kegel, Schaft, Zwischenflansch
    zm = GLOCKE_ZM
    oben = Pos(0, (TRAEGER_Z1 + 5 + 950) / 2) * Rectangle(2 * 320, 950 - TRAEGER_Z1 - 5)
    unten = Pos(0, (320 + TRAEGER_Z1 + 5) / 2) * Rectangle(2 * 186, TRAEGER_Z1 + 5 - 320)
    prof = (Pos(0, zm) * Circle(GLOCKE_R0)) & (oben + unten)
    xk0 = GLOCKE_X0 + 26
    t.append(extrude(Plane.YZ.offset(GLOCKE_X0) * prof, amount=26))                   # Flansch
    kegel = Pos(xk0 + (GLOCKE_XK - xk0) / 2, 0, zm) * Rot(0, 90, 0) * Cone(GLOCKE_R0 - 12, GLOCKE_R1, GLOCKE_XK - xk0)
    t.append(kegel)
    t.append(rad_x((GLOCKE_XK + GLOCKE_XM) / 2, 0, zm, GLOCKE_R1, GLOCKE_XM - GLOCKE_XK))
    # Radialrippen auf dem Kegel
    rp = Polyline((xk0, GLOCKE_R0 - 14), (GLOCKE_XK + 30, GLOCKE_R1 - 2), (GLOCKE_XK + 30, GLOCKE_R1 + 10),
                  (xk0, GLOCKE_R0 - 2), close=True)     # Rippenkopf am Flansch 10 hoch (keine Keilspitze auf dem Kegel)
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
    zf = GLOCKE_XM
    t.append(rad_x(zf + 13, 0, zm, GLOCKE_R2, 26))
    t += schraubenkreis((zf + 26, 0, zm), (1, 0, 0), GLOCKE_R2 - 14, 16, 16, 8)
    # Kupplungsgehaeuse: Kasten mit runden Kanten bis zum Wechselgetriebe, Flansch hinten
    t.append(kasten_rund(zf + 26, GLOCKE_X1, -255, 255, 350, GETR_Z1, 70, Axis.X))
    t.append(kasten_rund(GLOCKE_X1 - 12, GLOCKE_X1 + 14, -262, 262, 345, GETR_Z1, 60, Axis.X))
    pl = Plane(origin=(GLOCKE_X1 - 12, 0, (345 + GETR_Z1) / 2), x_dir=(0, 1, 0), z_dir=(-1, 0, 0))
    t += schrauben_rechteck(pl, 490, GETR_Z1 - 345 - 40, 100, 18, 9, r_ecke=60)
    # Kupplungsgehaeuse: Laengsrippen und Kupplungs-Schaudeckel an beiden Seiten
    for s in (-1, 1):
        for z in (420, 700):
            y0, y1 = sorted((s * 250, s * 268))
            t.append(box(zf + 40, GLOCKE_X1 - 12, y0, y1, z - 9, z + 9))
        pl = Plane(origin=(1540, s * 255, 560), x_dir=(1, 0, 0), z_dir=(0, s, 0))
        t += deckel(pl, 120, 170, 8, 18, 60, 16)
    t.append(sechskant((1550, 0, 350), (0, 0, -1), 30, 12))            # Kupplungs-Ablass
    t.append(sechskant((1200, 0, zm - GLOCKE_R1 - 30), (0, 0, -1), 30, 12))   # Glocken-Ablass
    # Wechselgetriebe
    t.append(kasten_rund(GLOCKE_X1, GETR_X1, -230, 230, GETR_Z0, GETR_Z1, 45, Axis.X))
    for x in range(1680, int(GETR_X1) - 20, 70):          # Rippen an Seiten und Boden
        for s in (-1, 1):
            y0, y1 = sorted((s * 228, s * 244))
            t.append(box(x - 8, x + 8, y0, y1, GETR_Z0 + 40, GETR_Z1 - 30))
        t.append(box(x - 8, x + 8, -170, 170, GETR_Z0 - 14, GETR_Z0 + 2))
    # Hinterachsgehaeuse (breiter, nimmt Lenkbremsen und Endantriebe auf)
    t.append(kasten_rund(GETR_X1 - 10, ACHS_X1, -Y_FLANSCH + 6, Y_FLANSCH - 6, GETR_Z0 - 10, GETR_Z1, 55, Axis.X))
    t.append(kasten_rund(GETR_X1 - 24, GETR_X1 + 4, -Y_FLANSCH + 2, Y_FLANSCH - 2, GETR_Z0 - 20, GETR_Z1, 55, Axis.X))
    pl = Plane(origin=(GETR_X1 - 24, 0, (GETR_Z0 + GETR_Z1) / 2 - 10), x_dir=(0, 1, 0), z_dir=(-1, 0, 0))
    t += schrauben_rechteck(pl, 2 * Y_FLANSCH - 50, GETR_Z1 - GETR_Z0 - 30, 105, 18, 9, r_ecke=55)
    # Ablassschrauben
    t.append(sechskant((1860, 0, GETR_Z0 - 14), (0, 0, -1), 32, 14))
    t.append(sechskant((2230, 0, GETR_Z0 - 10), (0, 0, -1), 32, 14))
    # Heckkasten: hochkant, oben breiter, Rueckwand mit Deckel und Zapfwellen-Lagerdeckel
    hk = kasten_rund(ACHS_X1 - 10, HECK_X1, -210, 210, 500, GETR_Z1, 40, Axis.X)
    hk = fillet(hk.edges().filter_by(Axis.Y).group_by(Axis.X)[-1], 30)
    t.append(hk)
    for z in (560, 650, 740):                               # Seitenrippen
        for s in (-1, 1):
            y0, y1 = sorted((s * 208, s * 222))
            t.append(box(ACHS_X1 + 20, HECK_X1 - 40, y0, y1, z - 8, z + 8))
    pl = Plane(origin=(HECK_X1, 0, 630), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    t += deckel(pl, 330, 220, 12, 30, 80, 18)
    t.append(rad_x(HECK_X1 + 12 + 14, 0, 640, 70, 28))     # Zapfwellen-Lagerdeckel
    t += schraubenkreis((HECK_X1 + 40, 0, 640), (1, 0, 0), 55, 6, 16, 8)
    t.append(rad_x(HECK_X1 + 50, 0, 640, 26, 22))
    t.append(sechskant((HECK_X1 + 12, 120, 540), (1, 0, 0), 28, 12))   # Oelstandschraube
    # Unterteil des Heckkastens (Kegelradgehaeuse), traegt den Zugpendel-Drehpunkt
    t.append(kasten_rund(ACHS_X1 - 10, 2520, -150, 150, GETR_Z0 - 10, 520, 35, Axis.X))
    return t


def lenkbremse():
    """Rechtes Lenkbremsgehaeuse mit rundem Deckel (Trommelachse quer)."""
    t = []
    y_in = 228.0
    t.append(rad_y(X_BREMSE, (y_in + Y_BREMSE_AUSSEN - 14) / 2, Z_BREMSE, R_BREMSE - 12, Y_BREMSE_AUSSEN - 14 - y_in))
    # Deckelflansch, Deckel mit Wölbung und Schraubenkranz
    t.append(rad_y(X_BREMSE, Y_BREMSE_AUSSEN - 7, Z_BREMSE, R_BREMSE, 14))
    t += schraubenkreis((X_BREMSE, Y_BREMSE_AUSSEN, Z_BREMSE), (0, 1, 0), R_BREMSE - 17, 12, 18, 9)
    t.append(rad_y(X_BREMSE, Y_BREMSE_AUSSEN + 6, Z_BREMSE, R_BREMSE - 40, 12))
    nabe = rad_y(X_BREMSE, Y_BREMSE_AUSSEN + 22, Z_BREMSE, 55, 20)
    t.append(fillet(nabe.edges().sort_by(Axis.Y)[-1], 6))
    t.append(sechskant((X_BREMSE, Y_BREMSE_AUSSEN + 32, Z_BREMSE), (0, 1, 0), 34, 12))
    # Nachstellbock unten und Betaetigungshebel
    t.append(box(X_BREMSE - 30, X_BREMSE + 30, y_in + 30, Y_BREMSE_AUSSEN - 20, Z_BREMSE - R_BREMSE - 25, Z_BREMSE - R_BREMSE + 20))
    t.append(sechskant((X_BREMSE, Y_BREMSE_AUSSEN - 50, Z_BREMSE - R_BREMSE - 25), (0, 0, -1), 24, 12))
    # Rippen zwischen Gehaeuse und Getriebe
    for dz in (-110, 110):
        t.append(box(X_BREMSE - 10, X_BREMSE + 10, 225, Y_BREMSE_AUSSEN - 16, Z_BREMSE + dz - 40, Z_BREMSE + dz + 40))
    return t


def endantrieb():
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


# ---------------- Plattform ----------------
_RIFFEL = None


def riffelblech(x0, x1, y0, y1, z, teilung=50.0, oy=None, ny=None):
    """Traenenblech: Rauten aus kurzen Rippen, abwechselnd +-45 Grad."""
    global _RIFFEL
    if _RIFFEL is None:
        _RIFFEL = Box(28, 9, RIFFEL_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
    t = []
    nx = int((x1 - x0) / teilung)
    ny = ny or int((y1 - y0) / teilung)
    ox = x0 + ((x1 - x0) - nx * teilung) / 2
    oy = y0 + ((y1 - y0) - ny * teilung) / 2 if oy is None else oy
    for i in range(nx):
        for j in range(ny):
            w = 45 if (i + j) % 2 else -45
            t.append(Pos(ox + (i + 0.5) * teilung, oy + (j + 0.5) * teilung, z) * Rot(0, 0, w) * _RIFFEL)
    return t


def plattform_mitte():
    """Geschlossenes Mittelblech zwischen den Kotfluegeln mit Inspektionsdeckel."""
    t = []
    x0 = DECK_X0                                            # davor: Glocke offen unter dem Tankunterbau
    t.append(box(x0, DECK_X1, -Y_FLANSCH, Y_FLANSCH, DECK_UK, DECK_Z))
    # Deckel ueber dem Getriebe
    t.append(kasten_rund(1960, 2180, -170, 170, DECK_Z, DECK_Z + 5, 25))
    t += schraubenreihe((1975, -150, DECK_Z + 5), (2165, -150, DECK_Z + 5), 4, (0, 0, 1), 16, 5)
    t += schraubenreihe((1975, 150, DECK_Z + 5), (2165, 150, DECK_Z + 5), 4, (0, 0, 1), 16, 5)
    return t


def kotfluegel():
    """Rechter Kotfluegel: Trittblech mit Riffelung, Abkantung aussen, Heckschuerze, Wange, Konsolen."""
    t = []
    ya = DECK_B / 2
    yi = Y_FLANSCH - 2
    t.append(box(DECK_X0, DECK_X1, yi, ya - BLECH, DECK_UK, DECK_UK + BLECH))
    t += riffelblech(DECK_X0 + 10, DECK_X1 - 20, Y_FLANSCH + 15, ya - 25, DECK_UK + BLECH,
                     oy=327.0, ny=11)   # Raster so, dass die Druck-Trennebene y 377 zwischen zwei Rippenreihen liegt
    # Abkantung aussen mit gerolltem Rand
    t.append(box(DECK_X0, DECK_X1, ya - BLECH, ya, DECK_UK - 90, DECK_Z - 2))
    t.append(stab((DECK_X0, ya - 2, DECK_Z - 2), (DECK_X1, ya - 2, DECK_Z - 2), 8))
    t.append(stab((DECK_X0, ya - BLECH / 2, DECK_UK - 90), (DECK_X1, ya - BLECH / 2, DECK_UK - 90), 9))
    # Heckschuerze (hinten, bis zur Ecke), unten mit Wulst
    zs = DECK_UK - 140
    t.append(box(DECK_X1 - BLECH, DECK_X1, 215, ya, zs, DECK_UK + BLECH))
    t.append(stab((DECK_X1 - BLECH / 2, 215, zs), (DECK_X1 - BLECH / 2, ya - BLECH / 2, zs), 9))
    t.append(Pos(DECK_X1 - BLECH / 2, ya - BLECH / 2, zs) * Sphere(9))
    t.append(stab((DECK_X1 - BLECH / 2, ya - BLECH / 2, zs), (DECK_X1 - BLECH / 2, ya - BLECH / 2, DECK_UK - 90), 9))
    # Kotfluegel-Innenwange (Winkel) entlang der Kette
    t.append(box(DECK_X0, X_KETTE_HINTEN, Y_WANGE - 12, Y_WANGE, DECK_UK - 60, DECK_UK))
    t += schraubenreihe((DECK_X0 + 60, Y_WANGE, DECK_UK - 30), (X_KETTE_HINTEN - 50, Y_WANGE, DECK_UK - 30),
                        12, (0, 1, 0), 18, 8)
    # Querkonsole hinten (hinter dem Triebrad), volle Breite bis zur Abkantung
    xq0, xq1 = X_KETTE_HINTEN + 40, DECK_X1 - BLECH
    t.append(box(xq0, xq0 + 12, 205, ya - BLECH, DECK_UK - 70, DECK_UK))
    t.append(box(xq0, xq1, 205, ya - BLECH, DECK_UK - 12, DECK_UK))
    # Konsolen (dreieckige Knotenbleche) unter dem Trittblech, nur innerhalb y < 430
    for x, y_in, z_tief in ((1520, 255, 560), (1680, 232, 590), (2470, 210, 560), (2600, 210, 560)):
        prof = Polyline((y_in, DECK_UK), (Y_WANGE - 12, DECK_UK), (Y_WANGE - 12, DECK_UK - 60),
                        (y_in, z_tief), close=True)
        k = extrude(Plane.YZ.offset(x - 6) * make_face(prof), amount=12)
        t.append(k)
    # Knotenbleche hinten aussen (ueber dem Triebrad-Ende frei)
    for y in (560, 760):
        prof = Polyline((xq0, DECK_UK), (xq0, DECK_UK - 70), (xq1, DECK_UK - 12), (xq1, DECK_UK), close=True)
        t.append(extrude(Plane.XZ.offset(-y + 6) * make_face(prof), amount=12))
    # Schrauben Trittblech -> Wange / Querkonsole
    # Schraubenkoepfe bis ins Trittblech gefuehrt (Blechoberseite DECK_Z - RIFFEL_H, 2,4 mm eingesenkt), sonst
    # stehen sie nur auf den Riffelspitzen und sind im Druck lose Einzelteile; sichtbare Hoehe bleibt 5 ueber DECK_Z
    zk, hk = DECK_Z - RIFFEL_H - 2.4, 5 + RIFFEL_H + 2.4
    t += schraubenreihe((DECK_X0 + 40, Y_WANGE - 6, zk), (X_KETTE_HINTEN - 40, Y_WANGE - 6, zk), 10, (0, 0, 1), 16, hk)
    t += schraubenreihe((xq0 + 6, 260, zk), (xq0 + 6, ya - 40, zk), 7, (0, 0, 1), 16, hk)
    return t


# ---------------- Zugpendel ----------------
def zugpendel():
    """Zugpendel mit Pendelschiene, Drehbolzen vorn und Maul mit Steckbolzen."""
    lack, blank = [], []
    zp = Z_PENDEL
    d = 50.0                                               # Pendeldicke
    # Pendelschiene (Querbalken) an zwei Haengeblechen unter dem Heckkasten
    xs0, xs1 = HECK_X1 - 65, HECK_X1
    lack.append(kasten_rund(xs0, xs1, -270, 270, zp - d / 2 - 44, zp - d / 2 - 2, 10, Axis.Y))
    for s in (-1, 1):
        prof = Polyline((2540, 520), (HECK_X1, 520), (HECK_X1, zp - d / 2 - 44), (xs0, zp - d / 2 - 44), close=True)
        y = s * 225
        lack.append(extrude(Plane.XZ.offset(-y + 7) * make_face(prof), amount=14))
        lack += schraubenreihe((HECK_X1 - 110, y + s * 7, 500), (HECK_X1 - 30, y + s * 7, 500), 2, (0, s, 0), 20, 8)
        lack.append(sechskant((xs0 + 30, y + s * 7, zp - d / 2 - 23), (0, s, 0), 20, 8))
    # Steckloecher (Pendelstellungen) und Steckbolzen in der Mitte
    for y in (-180, -90, 90, 180):
        lack.append(sechskant((xs0 + 30, y, zp - d / 2 - 2), (0, 0, 1), 18, 4))
    blank.append(Pos(xs0 + 30, 0, zp - 70) * Cylinder(14, 140, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    blank.append(Pos(xs0 + 30, 0, zp + 70) * Cylinder(22, 10, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # Pendel selbst
    p = kasten_rund(2440, 2830, -50, 50, zp - d / 2, zp + d / 2, 16, Axis.Z)
    lack.append(p)
    # vorderer Drehbolzen im Kegelradgehaeuse-Unterteil
    lack.append(box(2420, 2510, -80, 80, zp + d / 2, 520))
    blank.append(Pos(2460, 0, zp - d / 2 - 20) * Cylinder(20, d + 70, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    lack.append(sechskant((2460, 0, zp - d / 2 - 20), (0, 0, -1), 40, 16))
    # Maul: Ober- und Unterbacke, Rueckenstueck, senkrechter Steckbolzen mit Kette
    xm0, xm1 = 2790.0, 2880.0
    for z0, z1 in ((zp + d / 2, zp + d / 2 + 22), (zp - d / 2 - 22, zp - d / 2 - 0)):
        b = kasten_rund(xm0, xm1, -65, 65, z0, z1, 30, Axis.Z)
        lack.append(b)
    lack.append(box(xm0, xm0 + 30, -65, 65, zp - d / 2 - 22, zp + d / 2 + 22))
    for z in (zp + d / 2 + 22, zp - d / 2 - 22):
        n = 1 if z > zp else -1
        lack += [sechskant((xm0 + 15, y, z), (0, 0, n), 22, 10) for y in (-40, 40)]
    xb = 2850.0
    blank.append(Pos(xb, 0, zp - d / 2 - 50) * Cylinder(19, d + 130, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    kopf = Pos(xb, 0, zp + d / 2 + 22) * Cylinder(32, 14, align=(Align.CENTER, Align.CENTER, Align.MIN))
    blank.append(fillet(kopf.edges().sort_by(Axis.Z)[-1], 5))
    blank.append(Pos(xb, 0, zp + d / 2 + 50) * Rot(90, 0, 0) * Torus(18, 5))     # Griffring
    blank.append(rad_x(xb, 0, zp - d / 2 - 40, 5, 60))                          # Splint
    return lack, blank


# ---------------- Zusammenbau ----------------
def _spiegeln(teile):
    return [mirror(s, about=Plane.XZ) for s in teile]


def rumpf():
    t = Sammler("lack")
    rechts = []
    rechts += laengstraeger()
    rechts += lenkbremse()
    rechts += endantrieb()
    rechts += kotfluegel()
    t += rechts
    t += _spiegeln(rechts)
    t += quertraeger_vorn()
    lack, schwarz = querfeder()
    t += lack
    t.mat("schwarz", schwarz)
    t += getriebe()
    t += plattform_mitte()
    lack, blank = zugpendel()
    t += lack
    t.mat("blank", blank)
    return t
