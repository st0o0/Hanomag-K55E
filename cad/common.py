"""Gemeinsame Konstanten und Geometrie-Helfer fuer das K 55 E Modell.

WAS: HAUPTMASSE (Schnittstellen zwischen den Baugruppen, Herleitung in referenz/MASSKONZEPT.md),
Geometrie-Helfer (Quader, Staebe, Rohre, Schrauben, Ringe), der Material-Sammler und die
Umrechnung ins Modellsystem.

Konvention fuer alle Baugruppen ausser haube.py:
  Original-mm, X von Vorderkante Kuehlermaske nach hinten,
  Y nach rechts (in Fahrtrichtung), Z ab Boden.
zu_modell() rechnet in das Modellsystem (1:8, z=0 = Nullebene MASKE_UNTEN) um,
in dem auch haube.py arbeitet.

Umbau-Historie der Masse: referenz/historie/common.md.
"""
from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from itertools import pairwise

from build123d import (
    Align,
    Axis,
    Box,
    Circle,
    Compound,
    Cylinder,
    Line,
    Plane,
    Pos,
    Rectangle,
    RegularPolygon,
    Rot,
    Solid,
    Sphere,
    Text,
    ThreePointArc,
    Transition,
    Vector,
    Wire,
    extrude,
    fillet,
    scale,
    sweep,
)

Punkt = Sequence[float]

MASSSTAB = 8.0
MASKE_UNTEN = 392.0                       # Nullebene des Modellsystems (z=0), historisch Maskenunterkante;
                                          # die echte Maskenunterkante ist jetzt MASKE_UK (HAUPTMASSE)
BODEN_Z_MODELL = -MASKE_UNTEN / MASSSTAB  # Boden im Modellsystem
FONT = r"C:\Windows\Fonts\GOTHICB.TTF"    # Century Gothic Bold

# ---------------- HAUPTMASSE (Original-mm, siehe referenz/MASSKONZEPT.md) ----------------
# Diese Werte sind die Schnittstellen zwischen den Baugruppen. Nur hier aendern.
SPUR = 1270.0                 # Kettenmitte zu Kettenmitte
KETTE_B = 400.0               # Bodenplattenbreite
Y_KETTE = SPUR / 2            # Kettenmitte
X_LEIT, Z_LEIT, R_LEIT = 450.0, 372.0, 330.0      # Leitrad (Teilkreis); Foto BS: Maske steht ~100 mm vor der Kettennase
X_TRIEB, Z_TRIEB, R_TRIEB = 2250.0, 402.0, 315.7  # Triebrad (Teilkreis)
Z_PIN = 58.0                  # Kettenbolzen im unteren Trum
RAHMEN_Z0, RAHMEN_Z1 = 327.0, 467.0               # Kettenrahmen-Kasten
Y_TRAEGER = 240.0             # Laengstraeger-Mitte
TRAEGER_Z0, TRAEGER_Z1 = 380.0, 520.0
DECK_Z = 915.0                # Plattform / Kotfluegel-Oberkante (Spalt Kette/Aufbau ~120..150 wie Video 165/174 + Flickr,
                              # Unterkante Plattformrand 891, Greifer oben 738..768; Tankkasten steht auf der Plattformkante)
DECK_X0, DECK_X1, DECK_B = 1430.0, 2780.0, 1800.0
MASKE_UK = 525.0              # Unterkante Kuehlermaske (Nordhorn-Video n160/n167, Overlay: 520..560; Maske 525..1410 = 885 hoch)
HAUBE_X0, HAUBE_X1, HAUBE_B = 210.0, 1080.0, 690.0   # Foto BS: Haube endet ~1080, dahinter Tank
HAUBE_DACH_Z = 1410.0        # Video 165/167 + Flickr 1426..1441, Maske 525..1410 = 885 hoch
HAUBE_UNTEN_Z = 620.0         # Unterkante Haubenseitenwand (Bodenstreifen unter dem Motorfenster): Nordhorn n164 (+-30)
                              # (Greifer oben 738..768)
HAUBE_BAND_Z = 1090.0         # Oberkante Motorausschnitt = Unterkante Schriftband (Video 165/173, DSC04742 1070..1095)
SEG_X1 = 370.0                # vorderes Seitensegment x 210..370 (Video 066/070/173 + DSC04742, 150..200 breit),
                              # dann flacher Ellipsenbogen in die Bandkante
TANK_X0, TANK_X1, TANK_B = 1085.0, 1455.0, 680.0   # Tank in Haubenform: Unterkante bis x 1455, Oberkante bis ~1545 (Ueberhang)
TANK_Z0, TANK_Z1 = 1090.0, 1398.0       # Unterkante = Oberkante Motorausschnitt (HAUBE_BAND_Z), Oberkante unter Haubendach 1410
Y_SCHUB = 975.0               # Schubbalken-Mitte (aussen an der Kette)
Z_SCHUB = 400.0
TRAVERSE_X, TRAVERSE_Z = 2520.0, 1080.0           # Zylinder-Mittelzapfen (Foto BS: Deckel am Endkasten bei x ~2520), Achshoehe
ABOCK_SCHEITEL = (1270.0, 1080.0)                 # x, z des A-Bock-Scheitels (Foto BS, senkrecht von der Seite)
ABOCK_FUESSE = (920.0, 1650.0)                    # vorderer / hinterer Fuss auf dem Schubbalken, fast symmetrisch

# Motor / Anbauten (Foto BS, BV)
FLANSCH_GLOCKE_X = 1090.0     # Schwungradgehaeuse -> Kupplungsglocke (motor.py endet hier, rumpf.py beginnt hier)
AUSPUFF_XY = (700.0, 220.0)   # Durchbruch Auspuff im Haubendach (Fotos DSC04729/30/42: x ~ 700)
AUSPUFF_D = 58.0              # Durchbruch Auspuff (Rohr Ø 48, 5 mm Luft rundum)
ANSAUG_XY = (950.0, -236.0)   # Durchbruch Ansaugrohr (Ölbadtopf darunter im Motorraum, Fotos DSC04742/43/44)
ANSAUG_D = 76.0               # Durchbruch Ansaugrohr (Rohr Ø 66)
SCHEINWERFER = (230.0, 430.0, 1290.0)             # Lampenmitte x, |y|, z: an der Naht Maske/Haube, knapp unter der Dachkante
                                                  # (Video 165/172/196, Flickr 40431489714)
PUMPE = (-70.0, 0.0, 530.0)   # Hydraulikpumpe vor dem Maskensockel, Antrieb von der Kurbelwelle
Y_LTG = 392.0                 # Hydraulikleitungen aussen an der Haubenseite (|y| der Rohrmitte)
LENKRAD = (1850.0, 140.0, 1440.0)   # Lenkradmitte: Saeule gerade aus der Kastenfront, ~47 Grad (Short 0:47, Nordhorn 2:15)
SITZ_X = 2180.0               # Mitte Sitzschale (Kamera-Fit n129 2:09; n164 unsicher +-100)
SITZ_Y = 125.0                # Sitzachse y (n129: linke Schalenspitze bei y ~ -100)
KD_X = 140.0                  # Kuehlerverschluss auf der Maskenkappe, Mitte x (Foto BS: x ~100..180)
GESAMT_HOEHE = 1840.0

# Fussraum (Video 121-140, 128/129/132): Boden deutlich unter den Plattformen, senkrechte Seitenwaende.
# rumpf.py baut die Waende, fahrerstand.py das Bodenblech.
# vorn hinter dem Zwischenflansch der Glocke (Flansch 1400..1426, Schraubenkoepfe bis 1434), 10 hinter DECK_X0;
# hinten stuft die Plattform wieder auf DECK_Z (Hinterachsflansch ab 2056)
FW_X0, FW_X1 = 1440.0, 2520.0
# Bodenblech y, 645 breit (>= Haubenbreite 690: |y| 345); links bis y -300 belegt, rechts Wand innen y 345
# (Aussenseite 355, die Pumpenleitung bei |y| 392 bleibt auf der Plattform)
FW_Y0, FW_Y1 = -300.0, 345.0
FW_STUFE = 225.0                # Stufe Plattform -> Fussraumboden ~ Armaturenkasten (Short c48/c50: 220..250; vorher 185)
FW_Z0 = DECK_Z - FW_STUFE - 14.0   # Unterkante Bodenblech = Oberkante Kupplungs-/Wechselgetriebe 676
FW_Z1 = FW_Z0 + 14.0            # Oberkante Bodenblech 690
X_BREMSE = 1870.0               # Bremstrommel-Achse x (rumpf.py baut die Bremse, fahrerstand.py die Pedale/Gestaenge)

# Haubendach (Original-mm): Dachbogen quer ueber die Maskenbreite, Kantenradius zur Seitenwand
MASKE_B = 710.0               # Maskenbreite
DACH_SAG = 42.0               # Pfeilhoehe des Dachbogens (Flickr-Frontfoto: Mitte zur Seite ~75 inkl. Ecke, Bogen allein ~42)
DACH_R_KANTE = 85.0           # Radius Dachbogen -> senkrechte Seiten (Flickr 26271249857/39333958410: Schulter ~85-90)


def m(v: float) -> float:
    """Original-mm -> Modell-mm."""
    return v / MASSSTAB


def z_dach_orig(y: float) -> float:
    """Haubendach-Hoehe (Original-mm ab Boden) bei Querlage y (Original-mm): Kreisbogen mit Pfeilhoehe DACH_SAG
    ueber MASKE_B, Mitte = HAUBE_DACH_Z. haube.py nutzt die Modell-mm-Fassung z_dach()."""
    hb = MASKE_B / 2
    r = (hb * hb + DACH_SAG * DACH_SAG) / (2 * DACH_SAG)
    return HAUBE_DACH_Z - (r - math.sqrt(r * r - y * y))


def box(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> Solid:
    """Quader aus Grenzen."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def stab(p1: Punkt, p2: Punkt, r: float) -> Solid:
    """Zylinder von p1 nach p2."""
    v1, v2 = Vector(*p1), Vector(*p2)
    d = v2 - v1
    return extrude(Plane(origin=v1, z_dir=d) * Circle(r), amount=d.length)


def rohr(punkte: Sequence[Punkt], r: float) -> list[Solid]:
    """Rohr entlang eines Polygonzugs (Segmente + Kugeln in den Knicken)."""
    teile = [stab(a, b, r) for a, b in pairwise(punkte)]
    teile += [Pos(*p) * Sphere(r) for p in punkte[1:-1]]
    return teile


def rohr_glatt(punkte: Sequence[Punkt], r: float, rb: float | None = None) -> Solid:
    """Glattes Rohr entlang eines Polygonzugs; Knicke mit Biegeradius rb (Standard 2.5 r) verrundet.

    Liefert einen einzelnen Solid (Sweep), besser als rohr() fuer sichtbare Leitungen.
    """
    rb = rb or 2.5 * r
    pts = [Vector(*p) for p in punkte]
    edges, cur = [], pts[0]
    for i in range(1, len(pts) - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        d1, d2 = (b - a).normalized(), (c - b).normalized()
        ang = math.acos(max(-1.0, min(1.0, d1.dot(d2))))
        if ang < 1e-3:
            continue
        t = min(rb * math.tan(ang / 2), 0.49 * (b - a).length, 0.49 * (c - b).length)
        p1, p2 = b - d1 * t, b + d2 * t
        if (p1 - cur).length > 1e-6:
            edges.append(Line(cur, p1))
        bis = (d2 - d1).normalized()
        rr = t / math.tan(ang / 2)
        center = b + bis * (rr / math.cos(ang / 2))
        edges.append(ThreePointArc(p1, center - bis * rr, p2))
        cur = p2
    edges.append(Line(cur, pts[-1]))
    return sweep(Plane(origin=pts[0], z_dir=(pts[1] - pts[0])) * Circle(r), path=Wire(edges), transition=Transition.ROUND)


def kasten_rund(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float, r: float, achse: Axis = Axis.Z) -> Solid:
    """Quader mit verrundeten Kanten parallel zu `achse`."""
    b = box(x0, x1, y0, y1, z0, z1)
    return fillet(b.edges().filter_by(achse), r)


def schraube(p: Punkt, normal: Punkt, sw: float = 24, hoehe: float = 14, scheibe: bool = True) -> list[Solid]:
    """Sechskantkopf mit Unterlegscheibe (realistischer als sechskant())."""
    out = [sechskant(p, normal, sw, hoehe)]
    if scheibe:
        pl = Plane(origin=Vector(*p), z_dir=Vector(*normal))
        out.append(extrude(pl * Circle(sw * 0.95), amount=max(hoehe * 0.2, 5.0)))  # >= 0.6 mm im Modell
    return out


def ring_y(x: float, y: float, z: float, r_aussen: float, r_innen: float, b: float) -> Solid:
    """Ring (Hohlzylinder) mit Querachse Y."""
    return rad_y(x, y, z, r_aussen, b) - rad_y(x, y, z, r_innen, b + 2)


def ring_x(x: float, y: float, z: float, r_aussen: float, r_innen: float, b: float) -> Solid:
    """Ring (Hohlzylinder) mit Laengsachse X."""
    return rad_x(x, y, z, r_aussen, b) - rad_x(x, y, z, r_innen, b + 2)


def pruefen[T: (Solid, Compound)](name: str, obj: T) -> T:
    """Gueltigkeits- und Volumenpruefung eines Solids/Compounds; wirft bei Fehlern."""
    if not obj.is_valid:
        raise ValueError(f"{name}: ungueltige Geometrie")
    if obj.volume < 1e-6:
        raise ValueError(f"{name}: Volumen null")
    return obj


def balken(p1: Punkt, p2: Punkt, b: float, hh: float) -> Solid:
    """Rechteckbalken von p1 nach p2 (b quer, hh hoch)."""
    v1, v2 = Vector(*p1), Vector(*p2)
    d = v2 - v1
    x_dir = Vector(0, 0, 1).cross(d)
    if x_dir.length < 1e-6:
        x_dir = Vector(1, 0, 0)
    return extrude(Plane(origin=v1, x_dir=x_dir, z_dir=d) * Rectangle(b, hh), amount=d.length)


def rad_y(x: float, y: float, z: float, r: float, b: float) -> Solid:
    """Zylinder mit Querachse (Y), mittig bei y."""
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, b)


def rad_x(x: float, y: float, z: float, r: float, b: float) -> Solid:
    """Zylinder mit Laengsachse (X), mittig bei x."""
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, b)


def sechskant(p: Punkt, normal: Punkt, sw: float = 24, hoehe: float = 14) -> Solid:
    """Sechskant-Schraubenkopf auf einer Flaeche (normal zeigt nach aussen)."""
    return extrude(Plane(origin=Vector(*p), z_dir=Vector(*normal)) * RegularPolygon(sw / math.sqrt(3), 6), amount=hoehe)


def schraubenkreis(
    mitte: Punkt, normal: Punkt, r: float, n: int, sw: float = 22, hoehe: float = 12, start: float = 0.0
) -> list[Solid]:
    """n Sechskantkoepfe auf einem Kreis in der Ebene senkrecht zu normal."""
    pl = Plane(origin=Vector(*mitte), z_dir=Vector(*normal))
    out = []
    for i in range(n):
        a = math.radians(start + i * 360 / n)
        p = pl.from_local_coords((r * math.cos(a), r * math.sin(a)))
        out.append(sechskant(p, normal, sw, hoehe))
    return out


def schraubenreihe(p0: Punkt, p1: Punkt, n: int, normal: Punkt, sw: float = 20, hoehe: float = 10) -> list[Solid]:
    """n Sechskantkoepfe gleichmaessig auf der Strecke p0..p1."""
    v0, v1 = Vector(*p0), Vector(*p1)
    return [sechskant(v0 + (v1 - v0) * (i / (n - 1)), normal, sw, hoehe) for i in range(n)]


def text_auf(pl: Plane, txt: str, groesse: float, hoehe: float) -> Solid:
    """Erhabener Text (FONT) mittig auf der Ebene `pl`."""
    return extrude(pl * Text(txt, font_size=groesse, font_path=FONT, align=(Align.CENTER, Align.CENTER)), amount=hoehe)


class Sammler(list):
    """Liste von Solids mit Materialzuordnung.

    append / += landen im Standardmaterial, t.mat("chrom", obj) in einem
    anderen. += mit einem anderen Sammler uebernimmt dessen Materialien.
    """

    def __init__(self, standard: str = "lack") -> None:
        super().__init__()
        self.standard = standard
        self.extra: dict[str, list] = {}

    def mat(self, name: str, obj):
        """Haengt `obj` (Teil oder Liste von Teilen) ans Material `name`; gibt `obj` zurueck."""
        ziel = self if name == self.standard else self.extra.setdefault(name, [])
        if isinstance(obj, (list, tuple)):
            ziel.extend(obj)
        else:
            ziel.append(obj)
        return obj

    def __iadd__(self, other):
        if isinstance(other, Sammler):
            self.mat(other.standard, list(other))
            for k, v in other.extra.items():
                self.mat(k, v)
            return self
        return super().__iadd__(other)

    def schichten(self) -> dict[str, list]:
        """Material -> Teileliste (Standardmaterial zuerst, leere Materialien entfallen)."""
        d = {self.standard: list(self)} if len(self) else {}
        for k, v in self.extra.items():
            if v:
                d.setdefault(k, []).extend(v)
        return d


def zu_modell(teile: Iterable | Sammler, standard: str = "lack") -> dict[str, Compound]:
    """Original-mm (Z ab Boden) -> Modell-mm im System von haube.py.

    Liefert {material: Compound}.
    """
    if not isinstance(teile, Sammler):
        s = Sammler(standard)
        s += list(teile)
        teile = s
    out = {}
    for mat, lst in teile.schichten().items():
        c = Compound(children=lst)
        out[mat] = Pos(0, 0, BODEN_Z_MODELL) * scale(c, by=1 / MASSSTAB)
    return out
