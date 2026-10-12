"""Motor Hanomag D57 (4 Zyl.-Vorkammerdiesel, 5702 cm3, Bohrung ~110, Hub ~150) mit Kuehler,
Luefter, Riementrieb, Einspritzanlage, Lichtmaschine, Anlasser und Schwungradgehaeuse;
Auspuffanlage und Ansaugung.

Original-mm, X ab Vorderkante Kuehlermaske nach hinten, Y nach rechts, Z ab Boden.
Linke Seite (y < 0): Einspritzpumpe vorn (Antrieb aus dem Steuergehaeuse), Vorreiniger mit
Glasschale hinter der Pumpe, Kraftstoff-Doppelfilter oben, Seitendeckel "HANOMAG DIESEL" unten
hinter der Pumpe, Stoesselkammerdeckel, Anlasser am Schwungradgehaeuse, Ansaugkruemmer.
Rechte Seite (y > 0): Lichtmaschine vorn oben, Oelfilter, Oelmessstab, Abgaskruemmer.

Fotobefund: Foto BS (rechte Seite): Haube endet bei x ~1080, Auspuffrohr steht bei x ~640 aus
dem Dach; der Motor ist durch den grossen Seitenausschnitt sichtbar. fz_06m (linke Seite):
Pumpe vorn unten, Deckel "HANOMAG DIESEL" unten dahinter, Filterglocke oben.
Zylinderabstand ZYL_T = 155 (frueher 230): Block x 400..1030, Steuergehaeuse/Riementrieb davor
(x 364..402), Schwungradgehaeuse x 1030..FLANSCH_GLOCKE_X.

Raumgrenzen (common.py, Stand Umbau 2026-10): Maske x 0..210, z 450..1347; Haube x 210..1080,
Dach aussen z 1347, Wand innen y = +-332; Motorausschnitt offen x ~360..1080, z 620..1125.
Motor innerhalb y +-325, x 225 (Kuehler) .. FLANSCH_GLOCKE_X = 1090; Tank x 1085..1455 ab z 1000
(Schwungradgehaeuse bleibt darunter, Oberkante <= 950); Kupplungsglocke (rumpf.py) ab x 1090.
Laengstraeger y = +-(195..285), z = 380..520, Querblattfeder x = 505..615 bis z = 580.
Auspuff und Ansaugrohr durchs Haubendach bei AUSPUFF_XY / ANSAUG_XY.
"""
import math
from build123d import *
from .common import (box, stab, rohr_glatt, rad_x, rad_y, ring_x, sechskant,
                     schraubenkreis, schraubenreihe, kasten_rund, Sammler, FONT,
                     HAUBE_DACH_Z, FLANSCH_GLOCKE_X, AUSPUFF_XY, ANSAUG_XY, TRAEGER_Z1, TANK_Z0)

# ---------------- Hauptmasse Motor ----------------
HAUBE_TOP = HAUBE_DACH_Z                # Dach aussen (1347)
HAUBE_KRAGEN = HAUBE_TOP + 6.4          # Oberkante Kragen der Haubendurchbrueche (0,8 mm Modell)
AUSPUFF_D, ANSAUG_D = 70.0, 90.0        # Durchmesser der Dachdurchbrueche (haube.py muss gleich sein)
KD_X = 140.0                            # Muendung Kuehlerverschluss auf der Maskenkappe (lokal, = haube.KD_X;
                                        # Deckel x 108..172 gehoert zur kuehlermaske, Unterseite Maskendach)
KD_Z = HAUBE_DACH_Z - 13.0              # Unterseite Maskendach innen (~1334, Wand 1,6 mm Modell)
ZYL_T = 155.0                           # Zylinderabstand (Bohrung ~110)
ZYL_X = [480.0 + i * ZYL_T for i in range(4)]   # Zylindermitten 480, 635, 790, 945
X_VORN, X_HINTEN = 380.0, 1030.0        # Block inkl. Steuergehaeuse
Y_BLOCK = 190.0
Z_KW = 600.0                            # Kurbelwelle
Z_WANNE = 320.0                         # Unterkante Oelwanne
Z_KURBEL_U = 585.0                      # Unterkante Kurbelgehaeuse vorn (ueber der Querfeder)
DZ_OBEN = 70.0                          # Absenkung von Kopf und Aufbauten gegenueber dem alten Stand (Kopf-Unterkante 1000)
Z_KOPF0 = 1000.0 - DZ_OBEN              # Block-Oberkante / Kopf-Unterkante (930 -> hier 930)
Z_KOPF1 = Z_KOPF0 + 105.0               # Oberkante Zylinderkopf (1035)
Z_VD = Z_KOPF1 + 48.0                   # Oberkante Ventildeckel (1083); Hutmuttern bis ~1098
Z_AK0 = Z_KOPF1 - 26.0                  # Unterkante Ansaugkruemmer
Z_MOTOR_OBEN = Z_VD + 15.0              # hoechster Punkt des Motors (Hutmutter-Kuppe) ~1098
Z_TRAEGER = TRAEGER_Z1                  # Oberkante Laengstraeger (520)

# Riementrieb (Ebene x = RIEMEN_X0..X1), Kreise (y, z, Wirkradius)
RIEMEN_X0, RIEMEN_X1 = 364.0, 380.0
SCHEIBE_KW = (0.0, Z_KW, 105.0)
SCHEIBE_WP = (0.0, 860.0, 70.0)
SCHEIBE_LIMA = (255.0, 870.0, 46.0)      # (frueher z 900; 30 tiefer, damit der abgesenkte Abgaskruemmer frei bleibt)
LUEFTER_X, LUEFTER_R = 354.0, 245.0
HAUBE_BLECH = 10.0                      # Luefterhaube (>= 1,2 mm Modell)

# Kuehler (hinter der Maske, z innerhalb MASKE_UK 450 .. Dach)
K_X0, K_X1 = 225.0, 335.0
K_Y = 320.0
K_Z0, K_Z1 = 480.0, 1270.0   # Oberkante unter der gewoelbten Dachecke
K_NETZ_Z0, K_NETZ_Z1 = 580.0, 1180.0

# Einspritzanlage (linke Seite, vorn)
Y_ESP = -228.0                          # Mittelebene Einspritzpumpe und Druckleitungen
ESP_X0, ESP_X1 = 440.0, 670.0
ESP_Z0, ESP_Z1 = 640.0, 745.0
DV_X = [ESP_X0 + 30 + 50 * i for i in range(4)]   # Druckventilhalter 470..620
Z_DUESE = Z_KOPF0 + 50.0                # Duesenhalter (seitlich im Kopf)
DL_Z = [Z_DUESE - 20 - 9 * i for i in range(4)]   # Hoehe der waagerechten Leitungsabschnitte (ueber der Kastenpumpe)
DL_R = 3.5                              # Radius der Druckleitungen
FILTER_X = (528.0, 588.0)               # Kraftstoff-Doppelfilter, Glasglocken (zwischen den Leitungen)
FILTER_Y = -291.0
FILTER_Z = Z_DUESE + 5.0                # Mitte Filterkopf (vor den Duesenhaltern, ueber den Druckleitungen)
FP_DX = 121.0                           # Foerderpumpe: Mitte hinter ESP_X0
VR_X = 765.0                            # Vorreiniger mit Glasschale hinter dem Regler

# Seitendeckel (unten hinter der Pumpe, ueber dem Anlasser) und Stoesselkammerdeckel
# Kastenpumpe "HANOMAG DIESEL" (Nutzermasse nach Zollstockfotos): Gussgehaeuse 360 x 185, steht 30 vom Block ab,
# darauf Deckelplatte 320 x 165, darin erhabene Flaeche 285 x 130 mit zweizeiliger Schrift.
SD_X0, SD_X1, SD_Z0, SD_Z1 = 665.0, 1025.0, 740.0, 925.0      # Gussgehaeuse (Z0 ueber dem Reglerdeckel, hinten am Schwungradgehaeuse)
SD_Y0, SD_Y1 = -184.0, -220.0                                  # Block-Seite (leicht eingesenkt) bis Gehaeuse-Aussenflaeche
SK_X0, SK_X1, SK_Z0, SK_Z1 = 495.0, 625.0, 795.0, 865.0        # Stoesselkammerdeckel (vorn, hinter den Druckleitungen)

# Schwungradgehaeuse
SG_X0, SG_X1, SG_X2 = X_HINTEN, FLANSCH_GLOCKE_X - 12, FLANSCH_GLOCKE_X   # SG_X2 = Flansch Glocke
SG_Z, SG_R = 640.0, 300.0               # Oberkante 940 < Tank-Unterkante TANK_Z0 und <= 950
SG_OBEN = min(950.0, TANK_Z0 - 50.0)     # Schnitt oben (Kupplungsglocke <= 950, Tank darueber)

# Anlasser (links am Schwungradgehaeuse, unter dem Seitendeckel)
ANL_Y, ANL_Z = -255.0, 600.0

# Rechte Seite
OELF_X = 880.0                          # Oelfilter
MESS_X = 1010.0                         # Oelmessstab hinter dem Kruemmerende


SCHEIBE_MIN = 4.0                        # Mindestdicke Unterlegscheibe (0,5 mm Modell)


def schraube(p, normal, sw=24, hoehe=14, scheibe=True):
    """Sechskantkopf mit Unterlegscheibe; Scheibe mindestens SCHEIBE_MIN dick (druckbar),
    der Kopf sitzt auf der Scheibe."""
    pl = Plane(origin=Vector(*p), z_dir=Vector(*normal))
    if not scheibe:
        return [sechskant(p, normal, sw, hoehe)]
    d = max(SCHEIBE_MIN, hoehe * 0.2)
    kopf = Vector(*p) + Vector(*normal).normalized() * (d - 0.5)
    return [extrude(pl * Circle(sw * 0.95), amount=d), sechskant(kopf, normal, sw, hoehe)]


def _gummi_schelle(t, p, achse, r, b=10, schloss=(0, 0, 1)):
    """Schlauchschelle (blanker Ring) an Punkt p, Achse als Vektor; Schraubschloss Richtung `schloss`."""
    pl = Plane(origin=Vector(*p) - Vector(*achse).normalized() * (b / 2), z_dir=achse)
    ring = extrude(pl * Circle(r + 5), amount=b) - extrude(pl * Circle(r - 1), amount=b)
    t.mat("blank", ring)
    # Schraubschloss der Schelle
    n = Vector(*achse).normalized()
    quer = Vector(*schloss)
    quer = (quer - n * quer.dot(n)).normalized()
    t.mat("blank", Pos(*(Vector(*p) + quer * (r + 7))) * Box(12, 12, 12))


def _riemen_profil(kreise, dr):
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


def _ebene_x(x):
    """Skizzenebene senkrecht zu X, lokale Koordinaten (u, v) = (y, z)."""
    return Plane(origin=(x, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))


def _schrift(t, mitte_x, z, y_flaeche, txt, groesse, teilung=None, hoehe=5.0):
    """Erhabene Schrift auf einer Flaeche mit Normale -Y (linke Motorseite).
    Mit `teilung` werden die Buchstaben einzeln gesetzt (gesperrt)."""
    pl = Plane(origin=(0, y_flaeche + 0.5, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    if teilung is None:
        teile = [(mitte_x, txt)]
    else:
        n = len(txt)
        teile = [(mitte_x + (i - (n - 1) / 2) * teilung, c) for i, c in enumerate(txt)]
    for x, c in teile:
        sk = Text(c, font_size=groesse, font_path=FONT, align=(Align.CENTER, Align.CENTER))
        # lokale v-Achse der Ebene zeigt nach +Z
        t.append(extrude(pl * (Pos(x, z) * sk), amount=hoehe + 0.5))


# ======================================================================================
def motor():
    t = Sammler("motor")
    _block(t)
    _kopf(t)
    _seitendeckel(t)
    _einspritzanlage(t)
    _riementrieb(t)
    _lichtmaschine(t)
    _kuehler(t)
    _schwungradgehaeuse(t)
    _anlasser(t)
    _anbauteile_rechts(t)
    _block_rechts(t)
    return t


def _block(t):
    """Kurbelgehaeuse, Zylinderblock, Steuergehaeuse, Oelwanne, Motorfuesse."""
    # Kurbelgehaeuse (vorn hochgezogen ueber der Querblattfeder)
    t.append(kasten_rund(400, X_HINTEN, -185, 185, Z_KURBEL_U, 800, 15))
    # Zylinderblock (Wassermantel), leicht breiter, mit Gussleisten
    t.append(kasten_rund(400, X_HINTEN - 10, -Y_BLOCK, Y_BLOCK, 780, Z_KOPF0, 20))
    for s in (-1, 1):
        t.append(box(405, X_HINTEN - 15, s * Y_BLOCK - 4, s * Y_BLOCK + 4, 775, 790))   # Leiste unten
        t.append(box(405, X_HINTEN - 15, s * Y_BLOCK - 4, s * Y_BLOCK + 4, Z_KOPF0 - 10, Z_KOPF0))  # Leiste oben
    # Steuergehaeuse vorn mit Auge fuer den Pumpenantrieb
    t.append(kasten_rund(X_VORN, 402, -170, 170, 490, 820, 40, Axis.X))
    t.append(rad_x(391, Y_ESP, 690, 46, 22))
    t += schraubenreihe((X_VORN, -150, 510), (X_VORN, 150, 510), 5, (-1, 0, 0), 16, 6)
    # Oelwanne: tiefer Sumpf hinten, Flansch mit Schraubenreihe, Ablassschraube
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
    # Motorfuesse vorn (auf den Laengstraegern)
    for s in (-1, 1):
        t.append(box(640, 720, s * 186, s * 282, Z_TRAEGER, Z_TRAEGER + 16))
        t.append(box(672, 688, s * 182, s * 270, Z_TRAEGER + 16, 700))
        t.append(box(640, 720, s * 182, s * 196, Z_TRAEGER + 16, 700))
        for x in (655, 705):
            t += schraube((x, s * 245, Z_TRAEGER + 16), (0, 0, 1), 22, 12)


def _kopf(t):
    """Zylinderkopf, Ventildeckel, Kopfschrauben, Thermostat, Ansaugkruemmer, Duesenhalter."""
    kopf = box(400, X_HINTEN - 10, -185, 185, Z_KOPF0, Z_KOPF1)
    t.append(chamfer(kopf.edges().group_by(Axis.Z)[-1], 6))
    for s in (-1, 1):                                                # Kopfschrauben von oben
        for i in range(9):
            x = 425 + i * (X_HINTEN - 30 - 425) / 8                  # 2 je Zylinder + 1
            if s < 0 and abs(x - ANSAUG_XY[0]) < 62:
                continue                                             # unter dem Ansaugflansch
            t += schraube((x, s * 168, Z_KOPF1), (0, 0, 1), 22, 12)
    # Ventildeckel mit Fussflansch, Laengssicken, Hutmuttern, Oeleinfuellstutzen
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
    # Thermostatgehaeuse vorn auf dem Kopf, Stutzen nach vorn zum Kuehler
    z_th = Z_KOPF1 + 48.0                                             # Oberkante Thermostatgehaeuse
    t.append(kasten_rund(405, 465, -45, 45, Z_KOPF1, z_th, 12))
    t.append(rad_x(392, 0, Z_KOPF1 + 24, 24, 30))
    t += schraubenreihe((415, -35, z_th), (455, 35, z_th), 2, (0, 0, 1), 16, 7)
    # Ansaugkruemmer links mit 4 Flanschen und Steigflansch
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
    # Duesenhalter (seitlich, je Zylinder) mit Flansch, Muttern und Anschlussstutzen unten
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


def _schrift_mass(t, mitte_x, mitte_z, y_flaeche, txt, breite, hoehe, erhaben=5.0):
    """Erhabene Schrift auf einer Flaeche mit Normale -Y, auf Sollbreite und Soll-Versalhoehe gestreckt
    (Mitte mitte_x / mitte_z). Material wie die uebrige Schrift (blank)."""
    roh = extrude(Text(txt, font_size=40, font_path=FONT, align=(Align.CENTER, Align.CENTER)), amount=1.0)
    bb = roh.bounding_box()
    roh = Pos(-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, 0) * roh
    roh = scale(roh, by=(breite / bb.size.X, hoehe / bb.size.Y, 1.0))
    roh = scale(roh, by=(1.0, 1.0, (erhaben + 0.5)))               # Dicke 1 -> erhaben + 0,5 (Einsenkung)
    pl = Plane(origin=(mitte_x, y_flaeche + 0.5, mitte_z), x_dir=(1, 0, 0), z_dir=(0, -1, 0))   # lokales +Y = +Z
    t.mat("blank", Location(pl) * roh)


def _seitendeckel(t):
    """Hanomag-Kastenpumpe 'HANOMAG DIESEL' an der linken Blockseite: Gussgehaeuse 360 x 185, 30 vom Block,
    Deckelplatte 320 x 165 mit 8 Sechskantschrauben (Halteblech oben), erhabene Flaeche 285 x 130 mit
    Schrift, Ablassschraube SW 32 unten links, Abstellhebel mit Kugelknopf hinten, Typenschild."""
    xm = (SD_X0 + SD_X1) / 2                                          # 845
    zm = (SD_Z0 + SD_Z1) / 2                                          # 832,5
    # Gussgehaeuse (Kasten), Ecken gerundet, Aussenkante abgerundet
    kasten = box(SD_X0, SD_X1, SD_Y1, SD_Y0, SD_Z0, SD_Z1)
    kasten = fillet(kasten.edges().filter_by(Axis.Y), 22)
    kasten = fillet(kasten.edges().group_by(Axis.Y)[0], 5)
    t.append(kasten)
    # Deckelplatte 320 x 165
    px0, px1, pz0, pz1 = xm - 160, xm + 160, zm - 82.5, zm + 82.5
    y_pl = SD_Y1 - 8.0                                                # Plattenflaeche
    platte = box(px0, px1, SD_Y1 + 1, y_pl, pz0, pz1)
    platte = fillet(platte.edges().filter_by(Axis.Y), 12)
    platte = fillet(platte.edges().group_by(Axis.Y)[0], 2.5)
    t.append(platte)
    # Ablassschraube SW 32 unten links (Sockel + Sechskant), Freiraum in der erhabenen Flaeche
    ax, az = px0 + 26, pz0 + 26
    t.append(Pos(ax, y_pl + 0.5, az) * Rot(90, 0, 0) * Cylinder(25, 7.0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("blank", sechskant((ax, y_pl - 6.5, az), (0, -1, 0), 32, 13))
    # erhabene Flaeche 285 x 130, umlaufend abgerundet; an der Ablassschraube ausgespart
    ex0, ex1, ez0, ez1 = xm - 142.5, xm + 142.5, zm - 65, zm + 65
    y_er = y_pl - 5.0
    erh = box(ex0, ex1, y_pl + 0.5, y_er, ez0, ez1)
    erh = fillet(erh.edges().filter_by(Axis.Y), 20)
    erh = fillet(erh.edges().group_by(Axis.Y)[0], 3.5)
    erh = erh - Pos(ax, y_pl, az) * Rot(90, 0, 0) * Cylinder(32, 40)
    t.append(erh)
    # Schrift: HANOMAG (Breite 245, Versalhoehe 42), DIESEL (167, 40), Oberkante zu Oberkante 52
    z_top = zm + 46.0
    _schrift_mass(t, xm, z_top - 21, y_er, "HANOMAG", 245.0, 42.0)
    _schrift_mass(t, xm, z_top - 52 - 20, y_er, "DIESEL", 167.0, 40.0)
    # 8 Sechskantschrauben: oben links/Mitte/rechts, unten rechts + 3 gleichmaessig dazwischen (unten links = Ablassschraube)
    s_sw, s_h = 14.0, 6.0
    xs_oben = (px0 + 13, xm, px1 - 13)
    for x in xs_oben:
        t.mat("blank", sechskant((x, y_pl + 0.3, pz1 - (13 if x != xm else 9)), (0, -1, 0), s_sw, s_h))
    xr = px1 - 13
    for i in range(1, 5):
        x = ax + (xr - ax) * i / 4
        t.mat("blank", sechskant((x, y_pl + 0.3, pz0 + (13 if i == 4 else 9)), (0, -1, 0), s_sw, s_h))
    # Halteblech (Lasche) oben mittig, nach oben ueber die Platte bis zum Gehaeuserand
    lasche = box(xm - 14, xm + 14, SD_Y1 + 1, y_pl - 1.5, pz1 - 22, SD_Z1 - 3)
    lasche = fillet(lasche.edges().filter_by(Axis.Y), 6)
    t.mat("blank", lasche)
    # Abstellhebel hinten (rechts neben dem Kasten): Lagerbock, Hebel schraeg nach hinten unten, Kugelknopf
    hx, hz = SD_X1 - 12, SD_Z1 - 50
    y_h = -258.0
    t.append(stab((hx, SD_Y1 + 1, hz), (hx, y_h, hz), 11))                            # Lagerzapfen
    t.mat("blank", rad_y(hx, y_h - 3, hz, 16, 6))
    ende = (hx + 52, y_h - 3, hz - 62)
    t.mat("blank", stab((hx, y_h - 3, hz), ende, 6))
    t.mat("blank", Pos(*ende) * Sphere(13))
    # Typenschild mit Nieten (am Block, links vor den Druckleitungen)
    tx0, tx1, tz0, tz1 = 408.0, 464.0, 850.0, 890.0
    t.mat("blank", box(tx0, tx1, -194, -190, tz0, tz1))
    for x in (tx0 + 8, tx1 - 8):
        for z in (tz0 + 8, tz1 - 8):
            t.mat("blank", Pos(x, -194, z) * Sphere(4))
    # Stoesselkammer-Kontrolldeckel mit Schraubenkranz (am Block hinter den Druckleitungen)
    t.append(kasten_rund(SK_X0, SK_X1, -200, -189, SK_Z0, SK_Z1, 15, Axis.Y))
    for z in (SK_Z0 + 12, SK_Z1 - 12):
        t += schraubenreihe((SK_X0 + 15, -200, z), (SK_X1 - 15, -200, z), 4, (0, -1, 0), 16, 7)


def _einspritzpumpe(t):
    """Bosch-Reiheneinspritzpumpe mit Antrieb, Regler, Foerderpumpe."""
    y0, y1 = Y_ESP - 36, Y_ESP + 36
    # Antriebsgehaeuse vom Steuergehaeuse zur Pumpe
    t.append(rad_x((402 + ESP_X0) / 2, Y_ESP, 690, 38, ESP_X0 - 402 + 4))
    t.append(rad_x(ESP_X0 - 6, Y_ESP, 690, 50, 12))
    # Konsole am Kurbelgehaeuse
    t.append(box(ESP_X0 + 20, ESP_X1 - 20, -196, y1 + 2, ESP_Z0 - 22, ESP_Z0 + 2))
    # Pumpengehaeuse (Nockenwellenteil unten, Elementteil oben)
    t.append(kasten_rund(ESP_X0, ESP_X1, y0, y1, ESP_Z0, ESP_Z0 + 55, 10))       # im Motorlack (Foto)
    t.append(kasten_rund(ESP_X0 + 5, ESP_X1 - 5, y0 + 6, y1 - 6, ESP_Z0 + 55, ESP_Z1, 8))
    # Verschlussschrauben der Elemente (seitlich) und Druckventilhalter oben
    for x in DV_X:
        t.mat("blank", sechskant((x, y0 + 6, ESP_Z0 + 75), (0, -1, 0), 16, 6))
        t.mat("blank", sechskant((x, Y_ESP, ESP_Z1), (0, 0, 1), 26, 14))
        t.mat("blank", Pos(x, Y_ESP, ESP_Z1 + 14) * Cylinder(10, 20, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # Regler hinten mit Deckel und Stellhebel
    t.append(rad_x(ESP_X1 + 25, Y_ESP, 690, 48, 50))
    t.append(rad_x(ESP_X1 + 55, Y_ESP, 690, 40, 10))
    t += schraubenkreis((ESP_X1 + 60, Y_ESP, 690), (1, 0, 0), 32, 4, 12, 5, 45)
    t.mat("blank", stab((ESP_X1 + 30, y0 - 10, 735), (ESP_X1 + 30, Y_ESP, 735), 7))
    t.mat("blank", box(ESP_X1 + 22, ESP_X1 + 38, y0 - 14, y0 - 4, 700, 780))
    # Foerderpumpe aussen mit Handpumpe
    xf = ESP_X0 + FP_DX                                               # Mitte Foerderpumpe
    t.mat("schwarz", kasten_rund(xf - 31, xf + 31, y0 - 28, y0 + 2, 650, 705, 8))
    t.mat("schwarz", Pos(xf, y0 - 14, 705) * Cylinder(12, 40, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("blank", Pos(xf, y0 - 14, 745) * Cylinder(17, 12, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # Typschild BOSCH (gruen-blau) auf der Pumpe
    t.mat("bosch", box(ESP_X0 + 145, ESP_X0 + 195, y0 - 4, y0 + 1, ESP_Z0 + 12, ESP_Z0 + 40))


def _einspritzanlage(t):
    _einspritzpumpe(t)
    # Druckleitungen: senkrecht hoch, waagerecht gestaffelt, senkrecht zum Duesenstutzen.
    # Gestaffelte Hoehen DL_Z (hohe Leitung = vorderster Zylinder) -> keine Kreuzung.
    z_ende = Z_DUESE - 14.0                                            # Unterkante Duesenstutzen
    for xo, xt, zh in zip(DV_X, ZYL_X, DL_Z):
        if abs(xt - xo) < 40:                                          # kurzer Versatz: S-Schlag
            pts = [(xo, Y_ESP, ESP_Z1 + 28), (xo, Y_ESP, zh - 60), (xt, Y_ESP, zh), (xt, Y_ESP, z_ende)]
        else:
            pts = [(xo, Y_ESP, ESP_Z1 + 28), (xo, Y_ESP, zh), (xt, Y_ESP, zh), (xt, Y_ESP, z_ende)]
        t.mat("blank", rohr_glatt(pts, DL_R, 18))
    # Leitungsschellen am Block (zwischen Filterkonsole und Seitendeckel)
    # (liegen ueber der Kastenpumpe, halten die beiden laengsten Leitungen)
    zc = (DL_Z[2] + DL_Z[3]) / 2
    for x in (ZYL_X[2] - 30, ZYL_X[3] - 60):
        t.append(box(x - 9, x + 9, Y_ESP - 6, Y_ESP + 6, DL_Z[3] - 9, DL_Z[2] + 9))
        t.append(box(x - 5, x + 5, Y_ESP + 6, -189, zc - 6, zc + 6))
    # duenne Kraftstoffleitung (Leckoel-Ruecklauf) laengs ueber der Kastenpumpe, hinter den Druckleitungen
    zr = DL_Z[0] + 10.0
    t.mat("blank", rohr_glatt([(SD_X0 + 25, -205, zr), (SD_X1 - 25, -205, zr), (SD_X1 - 25, -192, zr + 14)], DL_R, 12))
    t.mat("blank", sechskant((SD_X0 + 25, -205, zr), (-1, 0, 0), 14, 6))
    # Kraftstoff-Doppelfilter mit Glasglocken; Konsole am Block zwischen den Druckleitungen,
    # Filterkopf unter den Duesenhaltern (FILTER_Z)
    fx0, fx1 = FILTER_X[0] - 28, FILTER_X[1] + 28
    fm = (fx0 + fx1) / 2
    zk0, zk1 = FILTER_Z - 20, FILTER_Z + 20                            # Filterkopf
    t.append(box(fm - 14, fm + 14, -196, -244, zk0 + 5, zk1 - 5))
    t.append(kasten_rund(fx0, fx1, FILTER_Y - 32, FILTER_Y + 32, zk0, zk1, 12))
    t.mat("blank", sechskant((fm, FILTER_Y, zk1), (0, 0, 1), 18, 10))           # Entlueftung
    zg = zk0 - 10                                                      # Glockenoberkante
    for x in FILTER_X:
        t.append(Pos(x, FILTER_Y, zg) * Cylinder(30, 10, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        glocke = Pos(x, FILTER_Y, zg - 85) * Cylinder(26, 86, align=(Align.CENTER, Align.CENTER, Align.MIN))
        glocke = fillet(glocke.edges().group_by(Axis.Z)[0], 12)
        t.mat("glas", glocke)
        t.mat("blank", Pos(x, FILTER_Y, zg - 97) * Cylinder(14, 14, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        # Spannbuegel
        for dy in (-30, 30):
            t.mat("blank", stab((x, FILTER_Y + dy, zg), (x, FILTER_Y + dy, zg - 92), 3.5))
        t.mat("blank", stab((x, FILTER_Y - 30, zg - 92), (x, FILTER_Y + 30, zg - 92), 4))
        t.mat("blank", sechskant((x, FILTER_Y, zg - 97), (0, 0, -1), 16, 8))
    # Kraftstoffleitungen: Vorreiniger -> Foerderpumpe -> Filter -> Pumpe (aussen bei y ~ -300)
    y0 = Y_ESP - 36
    xf = ESP_X0 + FP_DX
    xs = fx0 - 12                                                     # Steigleitung vor dem Filter
    t.mat("blank", rohr_glatt([(xf + 20, y0 - 26, 690), (xs, -308, 700), (xs, -308, FILTER_Z),
                               (fx0 + 4, -308, FILTER_Z)], 4, 14))
    # Filter -> Pumpe: zwischen den Glocken senkrecht nach unten (verdeckt den Seitendeckel nicht)
    t.mat("blank", rohr_glatt([(fm, -252, zk0 + 2), (fm, -252, 820), (ESP_X1 - 15, -252, 790),
                               (ESP_X1 - 15, -252, ESP_Z1 - 3)], 4, 14))
    t.mat("blank", sechskant((fm, -252, zk0), (0, 0, -1), 16, 8))
    t.mat("blank", sechskant((fx0, -308, FILTER_Z), (-1, 0, 0), 16, 8))
    # Vorreiniger mit Glasschale hinter dem Regler (fz_06m: Glasschale unten am Pumpenende)
    t.append(kasten_rund(VR_X - 20, VR_X + 20, -312, -262, 690, 722, 8))
    t.append(box(VR_X - 10, VR_X + 10, -262, -194, 696, 716))         # Halter zum Block
    t.mat("glas", Pos(VR_X, -290, 632) * Cylinder(19, 58, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("blank", Pos(VR_X, -290, 622) * Cylinder(10, 10, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    for dy in (-22, 22):
        t.mat("blank", stab((VR_X, -290 + dy, 690), (VR_X, -290 + dy, 627), 3))
    t.mat("blank", stab((VR_X, -312, 627), (VR_X, -268, 627), 3.5))
    t.mat("blank", rohr_glatt([(VR_X - 20, -300, 706), (ESP_X1 - 40, -312, 706), (xf + 31, -312, 690),
                               (xf + 26, y0 - 22, 680)], 4, 14))


def _riementrieb(t):
    """Keilriemen Kurbelwelle - Wasserpumpe - Lichtmaschine, Scheiben, Luefter mit Haube."""
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
    # Luefter: Nabe + 4 angestellte Fluegel, Spitzen gerundet
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


def _lichtmaschine(t):
    """Bosch-Lichtmaschine rechts oben am Block, Riemenscheibe in der Riemenebene."""
    y, z = SCHEIBE_LIMA[0], SCHEIBE_LIMA[1]
    t.mat("schwarz", rad_x(510, y, z, 60, 240))
    for x in (395, 625):                                              # Lagerschilde
        t.mat("schwarz", rad_x(x, y, z, 66, 14))
    t.mat("blank", rad_x(385, y, z, 12, 10))                          # Welle
    for a in (45, 225):                                               # Zuganker
        dy, dz = 63 * math.cos(math.radians(a)), 63 * math.sin(math.radians(a))
        t.mat("blank", stab((388, y + dy, z + dz), (632, y + dy, z + dz), 5))
    t.mat("schwarz", kasten_rund(560, 610, y - 30, y + 30, z + 56, z + 82, 8))   # Klemmenkasten
    t.mat("blank", Pos(585, y, z + 82) * Cylinder(6, 14, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("bosch", box(470, 540, y + 57, y + 63, z - 15, z + 15))                 # Typschild
    # Halter: Schwenkfuesse unten zum Block, Spannlasche vorn zur Wasserpumpe
    for x in (420, 600):
        t.append(box(x, x + 28, 185, y - 10, z - 72, z - 50))
        t.append(box(x, x + 28, y - 30, y + 10, z - 70, z - 40))
    t.append(box(386, 398, 60, y - 40, z + 5, z + 25))


def _kuehler(t):
    """Kuehler: Lamellenblock, Wasserkaesten, Seitenteile, Fuesse, Einfuellstutzen, Schlaeuche."""
    # Netz mit Lamellen vorn und hinten
    t.mat("schwarz", box(K_X0 + 10, K_X1 - 10, -300, 300, K_NETZ_Z0, K_NETZ_Z1))
    z = K_NETZ_Z0 + 12
    while z < K_NETZ_Z1 - 8:
        for x0, x1 in ((K_X0 + 6, K_X0 + 10), (K_X1 - 10, K_X1 - 6)):
            t.mat("blank", box(x0, x1, -298, 298, z, z + 5))
        z += 20
    for y in range(-270, 271, 90):                                    # senkrechte Stuetzbleche
        t.mat("schwarz", box(K_X0 + 4, K_X0 + 10, y - 3, y + 3, K_NETZ_Z0, K_NETZ_Z1))
    # Oberer Wasserkasten; Einfuellrohr vom Kasten nach vorn in die (hinten offene) Maske gekroepft,
    # Muendung unter dem Verschluss auf der Maskenkappe (KD_X), 0,5 mm Luft zum Maskendach
    t.mat("schwarz", kasten_rund(K_X0, K_X1, -K_Y, K_Y, K_NETZ_Z1, K_Z1, 25, Axis.X))
    xs, ze, zr = 280.0, KD_Z - 0.5, 1298.0                           # Abgang, Muendungsoberkante, Rohrhoehe
    t.mat("schwarz", Pos(xs, 0, K_Z1 - 5) * Cylinder(32, 12, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("schwarz", rohr_glatt([(xs, 0, K_Z1 - 5), (xs, 0, zr), (KD_X, 0, zr), (KD_X, 0, ze - 20)], 22, 40))
    t.mat("schwarz", Pos(KD_X, 0, ze - 24) * Cylinder(29, 24, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("schwarz", rad_x(K_X1 + 8, 0, 1240, 24, 16))                 # Zulaufstutzen
    # Ueberlaufrohr: vom Einfuellrohr nach rechts, hinter dem Seitenteil nach unten
    t.mat("blank", rohr_glatt([(250, 15, zr), (250, 312, zr), (K_X1 + 7, 312, zr), (K_X1 + 7, 312, 560)], 4, 15))
    # Unterer Wasserkasten: Mitte bis z = 480 zwischen den Traegern, aussen auf den Traegern
    t.mat("schwarz", kasten_rund(K_X0, K_X1, -K_Y, K_Y, Z_TRAEGER + 8, K_NETZ_Z0, 20, Axis.X))
    t.mat("schwarz", kasten_rund(K_X0 + 10, K_X1 - 10, -180, 180, K_Z0, Z_TRAEGER + 10, 20, Axis.X))
    t.mat("blank", sechskant((280, 0, K_Z0), (0, 0, -1), 22, 12))     # Ablasshahn
    t.mat("schwarz", rad_x(K_X1 + 8, -300, 552, 22, 16))               # Ablaufstutzen links
    # Seitenteile (U-Profil) und Fuesse auf den Laengstraegern
    for s in (-1, 1):
        t.mat("schwarz", box(K_X0, K_X1, s * 300, s * K_Y, Z_TRAEGER + 8, K_Z1 - 20))
        t.mat("schwarz", box(K_X0 + 15, K_X1 - 15, s * 196, s * 290, Z_TRAEGER, Z_TRAEGER + 10))
        for x in (250, 310):
            t += schraube((x, s * 245, Z_TRAEGER + 10), (0, 0, 1), 20, 10)
        # Stehbolzen der Wasserkastenverschraubung
        t.mat("schwarz", schraubenreihe((K_X0, s * 260, K_NETZ_Z1 + 10), (K_X0, s * 260, K_Z1 - 30), 2, (-1, 0, 0), 16, 6))
    # Schlaeuche mit Schellen
    oben = [(K_X1 + 14, 0, 1240), (362, 0, 1222), (378, 0, 1130), (388, 0, Z_KOPF1 + 60), (392, 0, Z_KOPF1 + 24)]
    t.mat("gummi", rohr_glatt(oben, 27, 45))
    _gummi_schelle(t, (K_X1 + 18, 0, 1240), (1, 0, 0), 27)
    _gummi_schelle(t, (390, 0, Z_KOPF1 + 40), (0.1, 0, -1), 27, schloss=(0, 1, 0))
    unten = [(K_X1 + 14, -300, 552), (395, -300, 560), (412, -300, 760), (440, -232, 800)]
    t.mat("gummi", rohr_glatt(unten, 25, 50))
    _gummi_schelle(t, (K_X1 + 20, -300, 552), (1, 0, 0), 25)
    # Wassereinlass am Block (Gusskruemmer)
    t.append(stab((440, -185, 800), (440, -236, 800), 26))
    _gummi_schelle(t, (440, -225, 800), (0, -1, 0), 25)


def _schwungradgehaeuse(t):
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
    # Schraubenkranz auf dem Flansch (nur ausserhalb des Blocks sichtbar)
    for i in range(24):
        a = math.radians(i * 15 + 7.5)
        y, z = (SG_R - 16) * math.cos(a), SG_Z + (SG_R - 16) * math.sin(a)
        im_block = abs(y) < 200 and z > Z_WANNE - 10
        im_traeger = abs(y) > 175 and z < Z_TRAEGER + 20
        if im_block or im_traeger:
            continue
        t.append(sechskant((SG_X0, y, z), (-1, 0, 0), 18, 8))
    # Schwungrad-Schauloch-Deckel unten
    t.append(box(SG_X0 + 16, SG_X1 - 4, -60, 60, 330, 352))
    # hintere Motorfuesse auf den Traegern
    for s in (-1, 1):
        t.append(box(SG_X0 + 5, SG_X1 - 3, s * 186, s * 282, Z_TRAEGER, Z_TRAEGER + 18))
        t.append(box(SG_X0 + 5, SG_X1 - 3, s * 186, s * 200, Z_TRAEGER, 620))
        t += schraube(((SG_X0 + SG_X1) / 2, s * 250, Z_TRAEGER + 18), (0, 0, 1), 22, 12)


def _anlasser(t):
    """Bosch-Anlasser links am Schwungradgehaeuse (Ritzel nach hinten), unter dem Seitendeckel,
    mit Magnetschalter und Kabel. Laengen relativ zur Flanschflaeche SG_X0."""
    y, z, x0 = ANL_Y, ANL_Z, SG_X0
    t.mat("bosch", rad_x(x0 - 115, y, z, 60, 150))                    # Motorteil
    t.mat("bosch", rad_x(x0 - 198, y, z, 50, 16))                     # Kollektordeckel
    t.mat("blank", rad_x(x0 - 212, y, z, 18, 14))
    t.mat("blank", ring_x(x0 - 115, y, z, 63, 58, 18))                # Deckband
    t.append(rad_x(x0 - 25, y, z, 66, 50))                            # Antriebslagerflansch (Motorlack)
    t += schraubenkreis((x0 - 50, y, z), (-1, 0, 0), 52, 3, 16, 7, 90)
    # Magnetschalter oben mit Klemmen
    t.mat("bosch", rad_x(x0 - 110, y, z + 82, 30, 110))
    t.mat("bosch", box(x0 - 140, x0 - 80, y - 14, y + 14, z + 50, z + 70))
    t.mat("blank", rad_x(x0 - 167, y, z + 82, 22, 6))
    for dy in (-11, 11):
        t.mat("blank", rad_x(x0 - 176, y + dy, z + 82, 6, 14))
    for x in (x0 - 130, x0 - 85):                                     # Klemmen oben
        t.mat("blank", Pos(x, y, z + 108) * Cylinder(6, 16, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        t.mat("blank", sechskant((x, y, z + 112), (0, 0, 1), 14, 5))
    # Kabel flach nach hinten (unter dem Seitendeckel, verdeckt die Schrift nicht)
    t.mat("gummi", rohr_glatt([(x0 - 85, y, z + 116), (x0 - 60, y, z + 120), (x0 + 8, -250, z + 120)], 7, 25))
    t.mat("gummi", rohr_glatt([(x0 - 130, y, z + 118), (x0 - 130, y, z + 124), (x0 - 174, y - 11, z + 124),
                               (x0 - 174, y - 11, z + 90)], 4, 10))


def _anbauteile_rechts(t):
    """Oelfilter, Oelmessstab auf der rechten Seite (unter dem Abgaskruemmer)."""
    x = OELF_X
    t.append(box(x - 50, x + 50, 185, 200, 780, 850))                 # Filterkonsole
    t.append(Pos(x, 255, 640) * Cylinder(66, 160, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.append(Pos(x, 255, 800) * Cylinder(72, 18, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.append(box(x - 15, x + 15, 195, 255, 790, 840))
    t.mat("blank", sechskant((x, 255, 818), (0, 0, 1), 24, 12))
    t.mat("blank", sechskant((x, 255, 640), (0, 0, -1), 22, 10))
    # Oelmessstab mit Fuehrungsrohr und Griffoese (hinter dem Kruemmerende, unterhalb davon)
    xm = MESS_X
    t.mat("blank", rohr_glatt([(xm, 185, 700), (xm, 215, 740), (xm + 5, 240, 900)], 7, 30))
    t.mat("blank", stab((xm + 5, 240, 900), (xm + 6, 242, 925), 4))
    t.mat("blank", Pos(xm + 6, 242, 940) * Rot(90, 0, 0) * Torus(14, 4))
    # Oeldruckleitung vom Filterkopf zum Hauptoelkanal, mit Oeldruckschalter
    t.mat("blank", rohr_glatt([(x + 20, 255, 836), (x + 20, 255, 880), (x + 60, 215, 900), (x + 60, Y_BLOCK - 2, 900)],
                              5, 18))
    t.mat("blank", sechskant((x + 60, Y_BLOCK, 900), (0, 1, 0), 18, 8))
    t.append(stab((x - 70, Y_BLOCK - 2, 930), (x - 70, 218, 930), 12))           # Oeldruckschalter
    t.mat("blank", sechskant((x - 70, 218, 930), (0, 1, 0), 22, 8))
    # Kurbelgehaeuse-Entlueftung: Stutzen oben am Kurbelgehaeuse, Rohr nach unten
    xe = 960.0
    t.append(stab((xe, 183, 760), (xe, 215, 760), 22))
    t.mat("blank", rohr_glatt([(xe, 214, 760), (xe, 228, 740), (xe + 10, 228, Z_TRAEGER + 25)], 9, 30))


def _block_rechts(t):
    """Sichtbare Gussdetails der rechten Blockseite (Motorausschnitt): Kernstopfen, Lagerrippen,
    Wasserablasshahn."""
    for i in range(3):                                                 # Kernstopfen zwischen den Zylindern
        x = ZYL_X[i] + ZYL_T / 2
        if x < 640:
            continue                                                   # hinter der Lichtmaschine
        t.append(rad_y(x, Y_BLOCK + 2, 890, 28, 8))
        t.append(rad_y(x, Y_BLOCK + 5, 890, 22, 6))
    for s in (-1, 1):                                                  # Lagerrippen am Kurbelgehaeuse
        for x in [ZYL_X[0] - ZYL_T / 2 + 5] + [xz + ZYL_T / 2 for xz in ZYL_X[:-1]] + [ZYL_X[-1] + 70]:
            t.append(box(x - 7, x + 7, s * 183, s * 192, Z_KURBEL_U + 5, 778))
    t.mat("blank", sechskant((ZYL_X[2], Y_BLOCK, 800), (0, 1, 0), 20, 10))       # Wasserablasshahn
    t.mat("blank", stab((ZYL_X[2], Y_BLOCK + 10, 800), (ZYL_X[2], Y_BLOCK + 10, 780), 3))


# ======================================================================================
def auspuff():
    """Abgaskruemmer rechts -> Auspuffrohr mit Halteschelle und Regenklappe;
    Ansaugrohr links mit Oelbadluftfilter (Topf, Spannring, Vorabscheider) und Arbeitsleuchte."""
    t = Sammler("auspuff")
    _auspuff(t)
    _ansaugung(t)
    return t


def _auspuff(t):
    ax, ay = AUSPUFF_XY
    r_rohr = AUSPUFF_D / 2 - 5                         # 5 mm Luft im Haubendurchbruch
    yk, zk, rk = 255.0, Z_KOPF1 - 25.0, 40.0                         # Sammelrohr (am abgesenkten Kopf)
    # Sammelrohr mit runden Enden, 4 Stutzen mit Flanschen
    t.append(stab((ZYL_X[0] - 40, yk, zk), (ZYL_X[-1] + 40, yk, zk), rk))
    for x in (ZYL_X[0] - 40, ZYL_X[-1] + 40):
        t.append(Pos(x, yk, zk) * Sphere(rk))
    for x in ZYL_X:
        t.append(stab((x, 196, zk), (x, yk, zk), 30))
        t.append(kasten_rund(x - 42, x + 42, 185, 197, zk - 42, zk + 42, 12, Axis.Y))
        for dx, dz in ((-31, -31), (31, 31)):
            t.mat("blank", sechskant((x + dx, 197, zk + dz), (0, 1, 0), 18, 9))
        t.append(box(x - 8, x + 8, 205, yk, zk - rk - 2, zk - rk + 14))    # Gussrippe
    # Auslassflansch oben, Rohr mit S-Kroepfung durch die Haube
    zf = zk + math.sqrt(rk ** 2 - 5 ** 2)
    t.append(kasten_rund(ax - 45, ax + 45, yk - 45, yk + 45, zf - 3, zf + 10, 10))
    for dx in (-33, 33):
        for dy in (-33, 33):
            t.mat("blank", sechskant((ax + dx, yk + dy, zf + 10), (0, 0, 1), 16, 8))
    z_top = 1985.0
    t.append(rohr_glatt([(ax, yk - 5, zf), (ax, yk - 5, zf + 50), (ax, ay, zf + 160), (ax, ay, z_top)],
                        r_rohr, 80))
    # Halteschelle auf dem Kragen der Haube (geteilt, mit Ohren und Schraube)
    zs = HAUBE_KRAGEN - 0.5
    t.mat("schwarz", Pos(ax, ay, zs) * (Cylinder(r_rohr + 10, 20, align=(Align.CENTER, Align.CENTER, Align.MIN))
                                         - Cylinder(r_rohr - 1, 20, align=(Align.CENTER, Align.CENTER, Align.MIN))))
    for s in (-1, 1):
        t.mat("schwarz", box(ax - 4 + s * 6, ax + 4 + s * 6, ay + r_rohr + 5, ay + r_rohr + 24, zs + 2, zs + 18))
    t.mat("blank", stab((ax - 16, ay + r_rohr + 16, zs + 10), (ax + 16, ay + r_rohr + 16, zs + 10), 4))
    t.mat("blank", sechskant((ax + 16, ay + r_rohr + 16, zs + 10), (1, 0, 0), 12, 6))
    # Regenklappe: Scharnier hinten, Klappe leicht geoeffnet, Gegengewicht
    xs, zsch = ax + r_rohr + 6, z_top + 6
    for dy in (-14, 14):
        t.append(box(ax + r_rohr - 6, xs + 6, ay + dy - 4, ay + dy + 4, z_top - 25, zsch + 5))
    t.mat("schwarz", rad_y(xs, ay, zsch, 5, 40))
    klappe = Pos(ax, ay, z_top + 2) * Cylinder(r_rohr + 5, 5, align=(Align.CENTER, Align.CENTER, Align.MIN))
    klappe += box(ax + r_rohr - 4, xs + 4, ay - 9, ay + 9, z_top + 2, zsch + 5)
    klappe += box(xs, xs + 30, ay - 5, ay + 5, zsch - 3, zsch + 5)                 # Gegengewichtsarm
    klappe += Pos(xs + 34, ay, zsch + 1) * Box(14, 22, 18)                         # Gewicht
    t.mat("schwarz", Pos(xs, ay, zsch) * Rot(0, 15, 0) * Pos(-xs, -ay, -zsch) * klappe)


def _ansaugung(t):
    ix, iy = ANSAUG_XY
    r_rohr = ANSAUG_D / 2 - 5
    # Ansaugrohr vom Steigflansch des Kruemmers bis in den Filtertopf
    t.mat("schwarz", stab((ix, iy, Z_KOPF1 + 10), (ix, iy, 1600), r_rohr))   # sitzt auf dem Steigflansch
    zs = HAUBE_KRAGEN - 0.5                                            # Gummimanschette auf dem Kragen
    t.mat("gummi", Pos(ix, iy, zs) * Cylinder(r_rohr + 10, 22, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("blank", Pos(ix, iy, zs + 14) * (Cylinder(r_rohr + 13, 8) - Cylinder(r_rohr + 5, 10)))
    # Oelbadluftfilter
    topf = Pos(ix, iy, 1590) * Cylinder(90, 100, align=(Align.CENTER, Align.CENTER, Align.MIN))
    topf = fillet(topf.edges().group_by(Axis.Z)[0], 18)
    t.mat("schwarz", topf)                                             # Oelwanne
    t.mat("schwarz", Pos(ix, iy, 1688) * Cylinder(96, 12, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("blank", Pos(ix, iy, 1690) * Cylinder(99, 8, align=(Align.CENTER, Align.CENTER, Align.MIN)))  # Spannring
    for a in (0, 120, 240):                                            # Spannbuegel
        t.mat("blank", Pos(ix, iy, 1694) * Rot(0, 0, a) * Pos(101, 0, 0) * Box(10, 24, 40))
    t.mat("schwarz", Pos(ix, iy, 1700) * Cylinder(92, 62, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("schwarz", Pos(ix, iy, 1762) * Cylinder(72, 18, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    for i in range(8):                                                 # Stege im Lufteinlass
        t.mat("schwarz", Pos(ix, iy, 1771) * Rot(0, 0, i * 45 + 22.5) * Pos(82, 0, 0) * Box(22, 8, 18))
    haube = Pos(ix, iy, 1780) * Cylinder(98, 44, align=(Align.CENTER, Align.CENTER, Align.MIN))
    haube = fillet(haube.edges().group_by(Axis.Z)[-1], 22)
    t.mat("schwarz", haube)                                            # Vorabscheider-Haube
    t.mat("blank", Pos(ix, iy, 1823) * Cylinder(14, 17, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("blank", Pos(ix, iy, 1834) * Box(64, 7, 12))                 # Fluegelmutter
    # Arbeitsleuchte an Schelle, nach vorn gerichtet
    zl = 1530.0
    t.mat("schwarz", Pos(ix, iy, 1500) * (Cylinder(r_rohr + 8, 20) - Cylinder(r_rohr - 1, 22)))
    t.mat("schwarz", stab((ix - r_rohr - 4, iy, 1500), (ix - 92, iy, 1500), 8))
    t.mat("schwarz", stab((ix - 92, iy, 1500), (ix - 92, iy, zl - 20), 8))
    gehaeuse = scale(Sphere(50), by=(0.7, 1, 1)) - box(-60, 0, -60, 60, -60, 60)
    lx = ix - 130
    t.mat("schwarz", Pos(lx, iy, zl) * gehaeuse)
    t.mat("chrom", Pos(lx, iy, zl) * (rad_x(-3, 0, 0, 52, 8) - rad_x(-3, 0, 0, 43, 10)))
    t.mat("glas", Pos(lx, iy, zl) * rad_x(-3, 0, 0, 44, 4))
    t.mat("schwarz", rad_y(lx + 18, iy, zl, 7, 2 * 50 + 10))           # Schwenkbolzen
    # Kabel der Leuchte am Rohr entlang in die Manschette
    t.mat("gummi", rohr_glatt([(lx + 30, iy, zl - 25), (ix - r_rohr - 4, iy, 1470),
                               (ix - r_rohr - 4, iy, zs + 10)], 4, 20))
