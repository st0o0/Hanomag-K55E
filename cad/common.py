"""Gemeinsame Konstanten und Geometrie-Helfer fuer das K 55 E Modell.

Konvention fuer alle Baugruppen ausser haube.py:
  Original-mm, X von Vorderkante Kuehlermaske nach hinten,
  Y nach rechts (in Fahrtrichtung), Z ab Boden.
zu_modell() rechnet in das Modellsystem (1:8, z=0 = Maskenunterkante) um,
in dem auch haube.py arbeitet.
"""
import math
from build123d import *

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
X_LEIT, Z_LEIT, R_LEIT = 450.0, 392.0, 330.0      # Leitrad (Teilkreis); Foto BS: Maske steht ~100 mm vor der Kettennase
X_TRIEB, Z_TRIEB, R_TRIEB = 2250.0, 402.0, 340.0  # Triebrad (Teilkreis)
Z_PIN = 62.0                  # Kettenbolzen im unteren Trum
RAHMEN_Z0, RAHMEN_Z1 = 327.0, 467.0               # Kettenrahmen-Kasten
Y_TRAEGER = 240.0             # Laengstraeger-Mitte
TRAEGER_Z0, TRAEGER_Z1 = 380.0, 520.0
DECK_Z = 840.0                # Plattform / Kotfluegel-Oberkante (Kette oben bis z~804 am Triebrad)
DECK_X0, DECK_X1, DECK_B = 1430.0, 2780.0, 1800.0
MASKE_UK = 450.0              # Unterkante Kuehlermaske (Foto BV: Maske 897 hoch, h/b = 1,26)
HAUBE_X0, HAUBE_X1, HAUBE_B = 210.0, 1080.0, 690.0   # Foto BS: Haube endet ~1080, dahinter Tank
HAUBE_DACH_Z = 392.0 + 955.0  # 1347
HAUBE_UNTEN_Z = 620.0         # Unterkante vorderes Haubenseitensegment (auf Hoehe Kettenoberkante)
HAUBE_BAND_Z = 1125.0         # Oberkante Motorausschnitt = Unterkante Schriftband (Band 1125..Dach)
SEG_X1 = 310.0                # vorderes Seitensegment x 210..310 (Foto BS), dann Bogen R ~220 in die Bandkante
TANK_X0, TANK_X1, TANK_B = 1085.0, 1455.0, 620.0   # direkt hinter der Haube, Oberkante in der Dachflucht
TANK_Z0, TANK_Z1 = 1000.0, 1335.0
Y_SCHUB = 975.0               # Schubbalken-Mitte (aussen an der Kette)
Z_SCHUB = 400.0
TRAVERSE_X, TRAVERSE_Z = 2520.0, 1080.0           # Zylinder-Mittelzapfen (Foto BS: Deckel am Endkasten bei x ~2520), Achshoehe
ABOCK_SCHEITEL = (1270.0, 1080.0)                 # x, z des A-Bock-Scheitels (Foto BS, senkrecht von der Seite)
ABOCK_FUESSE = (920.0, 1650.0)                    # vorderer / hinterer Fuss auf dem Schubbalken, fast symmetrisch

# Motor / Anbauten (Foto BS, BV)
FLANSCH_GLOCKE_X = 1090.0     # Schwungradgehaeuse -> Kupplungsglocke (motor.py endet hier, rumpf.py beginnt hier)
AUSPUFF_XY = (640.0, 220.0)   # Durchbruch Auspuff im Haubendach
ANSAUG_XY = (900.0, -220.0)   # Durchbruch Ansaugrohr Luftfilter im Haubendach
SCHEINWERFER = (110.0, 430.0, 1190.0)             # Lampenmitte x, |y|, z: oben an den Maskenseiten
PUMPE = (-70.0, 0.0, 530.0)   # Hydraulikpumpe vor dem Maskensockel, Antrieb von der Kurbelwelle
Y_LTG = 380.0                 # Hydraulikleitungen aussen an der Haubenseite (|y| der Rohrmitte)
LENKRAD = (1830.0, 200.0, 1470.0)                 # Lenkradmitte
SITZ_X = 2150.0               # Mitte Sitzschale
GESAMT_HOEHE = 1840.0


def m(v):
    """Original-mm -> Modell-mm"""
    return v / MASSSTAB


def box(x0, x1, y0, y1, z0, z1):
    """Quader aus Grenzen."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def stab(p1, p2, r):
    """Zylinder von p1 nach p2."""
    p1, p2 = Vector(*p1), Vector(*p2)
    d = p2 - p1
    return extrude(Plane(origin=p1, z_dir=d) * Circle(r), amount=d.length)


def rohr(punkte, r):
    """Rohr entlang eines Polygonzugs (Segmente + Kugeln in den Knicken)."""
    teile = []
    for a, b in zip(punkte, punkte[1:]):
        teile.append(stab(a, b, r))
    for p in punkte[1:-1]:
        teile.append(Pos(*p) * Sphere(r))
    return teile


def rohr_glatt(punkte, r, rb=None):
    """Glattes Rohr entlang eines Polygonzugs; Knicke mit Biegeradius rb (Standard 2.5 r) verrundet.
    Liefert einen einzelnen Solid (Sweep), besser als rohr() fuer sichtbare Leitungen."""
    rb = rb or 2.5 * r
    P = [Vector(*p) for p in punkte]
    edges, cur = [], P[0]
    for i in range(1, len(P) - 1):
        a, b, c = P[i - 1], P[i], P[i + 1]
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
    edges.append(Line(cur, P[-1]))
    return sweep(Plane(origin=P[0], z_dir=(P[1] - P[0])) * Circle(r), path=Wire(edges),
                 transition=Transition.ROUND)


def kasten_rund(x0, x1, y0, y1, z0, z1, r, achse=Axis.Z):
    """Quader mit verrundeten Kanten parallel zu `achse`."""
    b = box(x0, x1, y0, y1, z0, z1)
    return fillet(b.edges().filter_by(achse), r)


def schraube(p, normal, sw=24, hoehe=14, scheibe=True):
    """Sechskantkopf mit Unterlegscheibe (realistischer als sechskant())."""
    out = [sechskant(p, normal, sw, hoehe)]
    if scheibe:
        pl = Plane(origin=Vector(*p), z_dir=Vector(*normal))
        out.append(extrude(pl * Circle(sw * 0.95), amount=max(hoehe * 0.2, 5.0)))   # >= 0.6 mm im Modell
    return out


def ring_y(x, y, z, r_aussen, r_innen, b):
    """Ring (Hohlzylinder) mit Querachse Y."""
    return rad_y(x, y, z, r_aussen, b) - rad_y(x, y, z, r_innen, b + 2)


def ring_x(x, y, z, r_aussen, r_innen, b):
    return rad_x(x, y, z, r_aussen, b) - rad_x(x, y, z, r_innen, b + 2)


def pruefen(name, obj):
    """Gueltigkeits- und Volumenpruefung eines Solids/Compounds; wirft bei Fehlern."""
    if not obj.is_valid:
        raise ValueError(f"{name}: ungueltige Geometrie")
    if obj.volume < 1e-6:
        raise ValueError(f"{name}: Volumen null")
    return obj


def balken(p1, p2, b, hh):
    """Rechteckbalken von p1 nach p2 (b quer, hh hoch)."""
    p1, p2 = Vector(*p1), Vector(*p2)
    d = p2 - p1
    x_dir = Vector(0, 0, 1).cross(d)
    if x_dir.length < 1e-6:
        x_dir = Vector(1, 0, 0)
    return extrude(Plane(origin=p1, x_dir=x_dir, z_dir=d) * Rectangle(b, hh), amount=d.length)


def rad_y(x, y, z, r, b):
    """Zylinder mit Querachse (Y), mittig bei y."""
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, b)


def rad_x(x, y, z, r, b):
    """Zylinder mit Laengsachse (X), mittig bei x."""
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, b)


def sechskant(p, normal, sw=24, hoehe=14):
    """Sechskant-Schraubenkopf auf einer Flaeche (normal zeigt nach aussen)."""
    return extrude(Plane(origin=Vector(*p), z_dir=Vector(*normal)) * RegularPolygon(sw / math.sqrt(3), 6), amount=hoehe)


def schraubenkreis(mitte, normal, r, n, sw=22, hoehe=12, start=0.0):
    """n Sechskantkoepfe auf einem Kreis in der Ebene senkrecht zu normal."""
    pl = Plane(origin=Vector(*mitte), z_dir=Vector(*normal))
    out = []
    for i in range(n):
        a = math.radians(start + i * 360 / n)
        p = pl.from_local_coords((r * math.cos(a), r * math.sin(a)))
        out.append(sechskant(p, normal, sw, hoehe))
    return out


def schraubenreihe(p0, p1, n, normal, sw=20, hoehe=10):
    p0, p1 = Vector(*p0), Vector(*p1)
    return [sechskant(p0 + (p1 - p0) * (i / (n - 1)), normal, sw, hoehe) for i in range(n)]


def text_auf(pl: Plane, txt, groesse, hoehe):
    return extrude(pl * Text(txt, font_size=groesse, font_path=FONT, align=(Align.CENTER, Align.CENTER)), amount=hoehe)


class Sammler(list):
    """Liste von Solids mit Materialzuordnung.

    append / += landen im Standardmaterial, t.mat("chrom", obj) in einem
    anderen. += mit einem anderen Sammler uebernimmt dessen Materialien.
    """

    def __init__(self, standard="lack"):
        super().__init__()
        self.standard = standard
        self.extra = {}

    def mat(self, name, obj):
        if name == self.standard:
            self.extend(obj) if isinstance(obj, (list, tuple)) else self.append(obj)
        else:
            lst = self.extra.setdefault(name, [])
            lst.extend(obj) if isinstance(obj, (list, tuple)) else lst.append(obj)
        return obj

    def __iadd__(self, other):
        if isinstance(other, Sammler):
            self.mat(other.standard, list(other))
            for k, v in other.extra.items():
                self.mat(k, v)
            return self
        return super().__iadd__(other)

    def schichten(self):
        d = {self.standard: list(self)} if len(self) else {}
        for k, v in self.extra.items():
            if v:
                d.setdefault(k, []).extend(v)
        return d


def zu_modell(teile, standard="lack"):
    """Original-mm (Z ab Boden) -> Modell-mm im System von haube.py.
    Liefert {material: Compound}."""
    if not isinstance(teile, Sammler):
        s = Sammler(standard)
        s += list(teile)
        teile = s
    out = {}
    for mat, lst in teile.schichten().items():
        c = Compound(children=lst)
        out[mat] = Pos(0, 0, BODEN_Z_MODELL) * scale(c, by=1 / MASSSTAB)
    return out
