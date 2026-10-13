"""Hydraulikanlage der Planiereinrichtung: Pumpe, Steuerblock, Pumpenleitungen und Zylinderleitungen.

Doppeltwirkender 2-Zylinder-Kreis (Belege: Video Nordhorn 2:09..2:53 und YouTube-Short IApSZg9dphk 0:12..1:02):

* Die Zahnradpumpe sitzt vor dem Maskensockel; je Seite fuehrt EINE Leitung nach hinten.
  Links ist es die Saugleitung zum Oeltank, rechts die Druckleitung zum Anschluss P des Steuerblocks.
* Der Steuerblock steht rechts hinter dem Sitz auf dem Plattformblech, innen neben dem rechten Endkasten.
  Seine Anschluesse A und B liegen an der Aussenseite zur Endkastenwand; von dort gehen zwei dicke Rohre
  senkrecht nach oben (Short 0:16), quer ueber die Traverse nebeneinander auf gleicher Hoehe, und am linken
  Ende dicht vor der Endkasten-Innenwand wieder nach unten (Short 1:00) und durch die Wand zum linken Zylinder.
* Der rechte Zylinder wird vom Block aus durch zwei kurze Rohre direkt versorgt (durch die rechte Innenwand).
* Ein Ruecklauf zum Oeltank ist nicht modelliert (technisch waere einer von T/Block zum Tank noetig).

Alle Rohrleitungen sind Instanzen von :class:`Rohrzug` (Polylinie mit echten Kreisboegen an den Ecken).
Original-mm, X von der Maskenfront nach hinten, Y nach rechts, Z ab Boden.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from build123d import (
    Align,
    Axis,
    Circle,
    Cylinder,
    Line,
    Plane,
    Pos,
    Solid,
    Sphere,
    ThreePointArc,
    Transition,
    Vector,
    Wire,
    sweep,
)

from .common import (
    DECK_Z,
    MASKE_UK,
    PUMPE,
    Y_LTG,
    Y_SCHUB,
    Sammler,
    box,
    kasten_rund,
    rad_x,
    rad_y,
    ring_x,
    ring_y,
    schraubenkreis,
    sechskant,
    stab,
)
from .planiermasse import EK_T, EK_YI, QT_X0, QT_Z1, R_ZYL, X_ZAPFEN, Z_ZYL

Punkt = tuple[float, float, float]


# ---------------------------------------------------------------------------------------------------------------
# Bausteine
# ---------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Rohrzug:
    """Rohr entlang einer Polylinie; die Ecken sind mit Kreisboegen des Mittellinienradius ``biegung`` verrundet.

    ``biegung`` ist ein Radius fuer alle Ecken oder je ein Radius pro Innenpunkt. Ist ein Segment zu kurz fuer die
    beiden anliegenden Bogentangenten, wird ``ValueError`` ausgeloest (statt still einen kleineren Radius zu nehmen).
    """

    punkte: tuple[Punkt, ...]
    radius: float
    biegung: float | tuple[float, ...] = 0.0
    material: str | None = None
    name: str = ""

    def __post_init__(self) -> None:
        if len(self.punkte) < 2:
            raise ValueError(f"Rohrzug {self.name!r}: mindestens zwei Punkte noetig")

    def _radien(self) -> list[float]:
        innen = len(self.punkte) - 2
        if isinstance(self.biegung, tuple):
            if len(self.biegung) != innen:
                raise ValueError(f"Rohrzug {self.name!r}: {innen} Biegeradien erwartet, {len(self.biegung)} angegeben")
            return list(self.biegung)
        return [self.biegung or 2.5 * self.radius] * innen

    def kanten(self) -> list[Line | ThreePointArc]:
        """Linien und Kreisboegen der Mittellinie."""
        p = [Vector(*q) for q in self.punkte]
        radien = self._radien()
        winkel = [0.0] * len(p)
        tangente = [0.0] * len(p)
        for i in range(1, len(p) - 1):
            d1, d2 = (p[i] - p[i - 1]).normalized(), (p[i + 1] - p[i]).normalized()
            winkel[i] = math.acos(max(-1.0, min(1.0, d1.dot(d2))))
            if winkel[i] > 1e-3:
                tangente[i] = radien[i - 1] * math.tan(winkel[i] / 2)
        for i in range(len(p) - 1):
            laenge = (p[i + 1] - p[i]).length
            if tangente[i] + tangente[i + 1] > laenge + 1e-6:
                raise ValueError(f"Rohrzug {self.name!r}: Segment {i} ({laenge:.0f} mm) zu kurz fuer die Bogentangenten "
                                 f"({tangente[i]:.0f} + {tangente[i + 1]:.0f} mm)")
        kanten, aktuell = [], p[0]
        for i in range(1, len(p) - 1):
            if tangente[i] == 0.0:
                continue
            d1, d2 = (p[i] - p[i - 1]).normalized(), (p[i + 1] - p[i]).normalized()
            a, e = p[i] - d1 * tangente[i], p[i] + d2 * tangente[i]
            if (a - aktuell).length > 1e-6:
                kanten.append(Line(aktuell, a))
            bis = (d2 - d1).normalized()
            r = radien[i - 1]
            mittelpunkt = p[i] + bis * (r / math.cos(winkel[i] / 2))
            kanten.append(ThreePointArc(a, mittelpunkt - bis * r, e))
            aktuell = e
        kanten.append(Line(aktuell, p[-1]))
        return kanten

    def koerper(self) -> Solid:
        p0, p1 = Vector(*self.punkte[0]), Vector(*self.punkte[1])
        return sweep(Plane(origin=p0, z_dir=p1 - p0) * Circle(self.radius), path=Wire(self.kanten()),
                     transition=Transition.ROUND)

    def einfuegen(self, t: Sammler) -> None:
        _ablegen(t, self.material, self.koerper())


@dataclass(frozen=True)
class Verschraubung:
    """Sechskant-Verschraubung (Ueberwurf, Hohlschraube, Schott) mit Fuss in ``ort`` und Achse ``achse``."""

    ort: Punkt
    achse: Punkt
    schluessel: float = 40.0
    hoehe: float = 14.0
    material: str = "blank"

    def koerper(self) -> Solid:
        return sechskant(self.ort, self.achse, self.schluessel, self.hoehe)

    def einfuegen(self, t: Sammler) -> None:
        _ablegen(t, self.material, self.koerper())


@dataclass(frozen=True)
class Schelle:
    """Kurzer Schellenbock fuer ein Rohr laengs X: Fussplatte auf dem Blech (2 Schrauben), Sattel, Rohrschelle mit Ohren."""

    x: float
    y: float
    z: float
    rohr_radius: float
    z_fuss: float = DECK_Z

    def einfuegen(self, t: Sammler) -> None:
        x, y, z, r, zf = self.x, self.y, self.z, self.rohr_radius, self.z_fuss
        t.append(box(x - 26, x + 26, y - r - 8, y + r + 8, zf, zf + 5))                          # Fussplatte
        t += [sechskant((x, y + dy, zf + 5), (0, 0, 1), 12, 5) for dy in (-r - 4, r + 4)]       # Fussschrauben
        t.append(box(x - 14, x + 14, y - r + 4, y + r - 4, zf + 5, z - r + 3))                  # Sattel
        t.append(ring_x(x, y, z, r + 8, r - 0.5, 28))                                           # Schelle
        for dy in (-r - 8, r + 8):                                                              # Spannschrauben
            t.append(box(x - 14, x + 14, y + dy - 6, y + dy + 6, z - 6, z + 6))
            t.mat("schwarz", sechskant((x, y + dy, z + 6), (0, 0, 1), 12, 6))


def _ablegen(t: Sammler, material: str | None, koerper: Solid) -> None:
    if material is None:
        t.append(koerper)
    else:
        t.mat(material, koerper)


def _scheibe_z(x: float, y: float, z0: float, r: float, h: float) -> Solid:
    return Pos(x, y, z0) * Cylinder(r, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


# ---------------------------------------------------------------------------------------------------------------
# Masse
# ---------------------------------------------------------------------------------------------------------------
# Rohrradien
R_QUER = 21.0        # Zylinderleitungen Ø 42 (Video: 40..45)
R_PUMPE = 18.0       # Pumpenleitungen Ø 36
R_ANSCHL = 14.0      # kurze Rohre Block -> rechter Zylinder Ø 28
R_SCHLAUCH = 11.0    # Schlauchstuecke im Endkasten

# Pumpe (Fotos 26271249857 / 40431531504 / 40431489714)
PU_Z = PUMPE[2]
PU_R = 75.0                              # Gehaeuse Ø 150
PU_PL = 2.4                              # Frontplatte 2,4 mm in den Maskensockel (x = 0) eingesenkt
PU_XV, PU_XH = -225.0, -60.0             # Gehaeuse vorn / hinten
PU_XPORT, PU_ZPORT = -105.0, PU_Z - 40.0   # Anschluss seitlich, etwas unter der Achse

# Pumpenleitungen: um die Maskenecke, EINE Biegung hoch auf Z_PL, dann gerade durch den Motorausschnitt (Oberkante 1090)
LTG_X0, LTG_Z0 = -10.0, 580.0
X_LTG_KNICK = 470.0
Z_PL = DECK_Z + 45.0                     # Rohrmitte auf der Plattform, 27 ueber dem Blech (kurze Schellen)
X_SCHELLE0, DX_SCHELLE = 1500.0, 160.0   # Schellenraster ab DECK_X0, links wie rechts gleich
BIEGUNG_PUMPE = 60.0
BIEGUNG_P = 30.0                         # Bogen zum Anschluss P
X_P_BOGEN = 2440.0                       # rechts: Abbiegen nach aussen zur Vorderseite des Blocks

# Steuerblock hinter dem Sitz (Sitz x 2340, y 200, Rand y 425), vor der Tank-Vorderwand 2630
VB_X0, VB_X1 = 2480.0, 2620.0
VB_Y0, VB_Y1 = 650.0, 780.0              # innen neben den Schenkeln der Querrohre (Short 0:16)
VB_Z0, VB_Z1 = DECK_Z + 20.0, DECK_Z + 150.0
VB_PL_X = (2510.0, 2590.0)               # Fussplatte
HEBEL_FUSS = (2498.0, 668.0, VB_Z1)      # Hebelfuss auf der Deckelkante
HEBEL_KUGEL = (2390.0, 485.0, 1190.0)    # Kugel neben dem hinteren Sitzrand, ueber dem Polster (1105)
R_KUGEL = 25.0
P_ANSCHLUSS = (VB_X0, 735.0, Z_PL)       # Druckanschluss P an der Vorderseite des Blocks

# Zylinderleitungen
X_QUER = (2538.0, 2600.0)                # beide Rohre nebeneinander auf gleicher Hoehe (Short 0:16 / 1:00), Oeltank ab 2630
Z_QUER = 1230.0                          # Nordhorn-Seitenansicht 2:44: untere Rohrlinie ~ 1230
BIEGUNG_QUER = 63.0                      # 1,5 x Ø
Y_SCHENKEL_R = 850.0                     # senkrechte Schenkel dicht vor der rechten Endkasten-Innenwand (880)
Y_SCHENKEL_L = -800.0                    # links: der Bogen zur Wand braucht 63 mm Tangente vor der Innenwand
Z_BLOCK_AB = (1022.0, 1022.0)            # A/B an der +y-Seite des Blocks
Z_ZYL_LTG = 965.0                        # Hoehe der Rohre durch die Endkastenwand (unter dem Mittelzapfen, ueber dem Kastenboden)
R_RING = R_ZYL + 10.0                    # Zapfenring um das Zylinderrohr
RING_X = (X_ZAPFEN - 45.0, X_ZAPFEN + 45.0)

# Pfosten auf dem Oeltank (Frame 144 / Short): Flachstahlbuegel links-mittig, Rundpfosten (Entlueftung) rechts-mittig
Y_PFOSTEN = (-345.0, 250.0)


# ---------------------------------------------------------------------------------------------------------------
# Wanddurchfuehrungen (fuer endkasten() in planierschild)
# ---------------------------------------------------------------------------------------------------------------
def wanddurchfuehrungen(seite: int) -> list[tuple[float, float, float, float]]:
    """Loecher in der Innenwand des Endkastens der Seite ``seite`` (-1 links, +1 rechts): (x, y, z, Radius)."""
    return [(x, seite * (EK_YI + EK_T / 2), Z_ZYL_LTG, 27.0) for x in X_QUER]


# ---------------------------------------------------------------------------------------------------------------
# Pumpe
# ---------------------------------------------------------------------------------------------------------------
def oelpumpe(t: Sammler) -> None:
    """Runde Zahnradpumpe vor dem Maskensockel auf einer Frontplatte: Gehaeuse Ø 150 mit Frontdeckel, hinten
    Kupplungsglocke (Antrieb von der Kurbelwelle), je Seite ein Anschlussflansch mit einer Leitung."""
    xm = (PU_XV + PU_XH) / 2
    t.append(rad_x(xm, 0, PU_Z, PU_R, PU_XH - PU_XV))
    t.append(rad_x(PU_XV - 6, 0, PU_Z, PU_R - 7, 14))
    t += schraubenkreis((PU_XV - 13, 0, PU_Z), (-1, 0, 0), 56, 6, 14, 7, start=30)
    t.mat("blank", rad_x(PU_XV - 18, 0, PU_Z, 22, 10))
    t.append(rad_x(PU_XH + 6, 0, PU_Z, PU_R + 6, 12))
    t.append(rad_x((PU_XH + 6 - 14) / 2, 0, PU_Z, 52, -14 - (PU_XH + 6)))
    t.append(box(-14, PU_PL, -140, 140, MASKE_UK + 2, MASKE_UK + 162))
    for dy in (-118, 118):
        for z in (MASKE_UK + 22, MASKE_UK + 142):
            t.mat("schwarz", sechskant((-14, dy, z), (-1, 0, 0), 16, 7))
    for s in (-1, 1):
        t.append(stab((PU_XPORT, s * 50, PU_ZPORT), (PU_XPORT, s * 98, PU_ZPORT), R_PUMPE + 12))
        t.append(rad_y(PU_XPORT, s * 96, PU_ZPORT, R_PUMPE + 12, 24))
        t += [sechskant((PU_XPORT + dx, s * 104, PU_ZPORT), (0, s, 0), 12, 6) for dx in (-R_PUMPE - 7, R_PUMPE + 7)]


# ---------------------------------------------------------------------------------------------------------------
# Steuerblock
# ---------------------------------------------------------------------------------------------------------------
def steuerblock(t: Sammler) -> None:
    """Dunkler Sektions-Steuerblock mit quer gestapelten Rippen (Short 0:15..0:17) auf einer Fussplatte, Handhebel mit
    Kugel schraeg nach vorn-innen zum Fahrer. Anschluesse: A/B und die Ausgaenge zum rechten Zylinder an der +y-Seite,
    P (Druck von der Pumpe) an der Vorderseite."""
    x0, x1, y0, y1, z0, z1 = VB_X0, VB_X1, VB_Y0, VB_Y1, VB_Z0, VB_Z1
    t.append(box(VB_PL_X[0], VB_PL_X[1], y0, y1, DECK_Z, z0 + 1))
    t += [sechskant((x, y, z0 - 13), (0, 0, 1), 14, 6) for x in (VB_PL_X[0] + 12, VB_PL_X[1] - 12) for y in (y0 + 14, y1 - 14)]
    t.mat("schwarz", kasten_rund(x0, x1, y0, y1, z0, z1 - 22, 12, Axis.Z))
    for i in range(6):
        xr = x0 + 14 + i * (x1 - x0 - 28) / 5
        t.mat("schwarz", kasten_rund(xr - 7, xr + 7, y0 - 2, y1 + 2, z0 + 12, z1 - 30, 5, Axis.Z))
    t.append(kasten_rund(x0 + 10, x1 - 10, y0 + 10, y1 - 10, z1 - 23, z1, 10, Axis.Z))
    t += [sechskant((x, y, z1), (0, 0, 1), 14, 6) for x in (x0 + 16, x1 - 16) for y in (y0 + 16, y1 - 16)]
    # Handhebel: Sockel auf dem Deckel, Gelenkkugel, Stange Ø 20, schwarze Kugel Ø 50
    xf, yf, zf = HEBEL_FUSS
    t.append(Pos(xf, yf, zf) * Cylinder(26, 14, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    t.mat("blank", Pos(xf, yf, zf + 16) * Sphere(16))
    xk, yk, zk = HEBEL_KUGEL
    richtung = (Vector(xk, yk, zk) - Vector(xf, yf, zf + 16)).normalized()
    t.mat("blank", stab((xf, yf, zf + 16), tuple(Vector(xk, yk, zk) - richtung * (R_KUGEL - 6)), 10))
    t.mat("schwarz", Pos(xk, yk, zk) * Sphere(R_KUGEL))
    # Anschluesse
    for x, z in zip(X_QUER, Z_BLOCK_AB, strict=True):
        Verschraubung((x, y1, z), (0, 1, 0), 44, 12).einfuegen(t)                                 # A / B
    for x in X_QUER:
        Verschraubung((x, y1, Z_ZYL_LTG), (0, 1, 0), 32, 10).einfuegen(t)                         # Ausgaenge zum rechten Zylinder
    px, py, pz = P_ANSCHLUSS
    Verschraubung((px, py, pz), (-1, 0, 0), 40, 14).einfuegen(t)                                  # P


# ---------------------------------------------------------------------------------------------------------------
# Pumpenleitungen
# ---------------------------------------------------------------------------------------------------------------
def _pumpenzug(seite: int) -> Rohrzug:
    """Pumpe -> Maskenecke -> EIN Bogen hoch auf Z_PL -> gerade bei |y| Y_LTG nach hinten.
    Links bis zur Vorderwand des Oeltanks, rechts mit Bogen nach aussen bis zur Vorderseite des Blocks (P)."""
    s = seite
    punkte: list[Punkt] = [(PU_XPORT, s * 104, PU_ZPORT), (PU_XPORT, s * 250, PU_ZPORT), (LTG_X0 - 40, s * Y_LTG, LTG_Z0 - 40),
                           (LTG_X0, s * Y_LTG, LTG_Z0), (X_LTG_KNICK, s * Y_LTG, Z_PL)]
    px, py, pz = P_ANSCHLUSS
    if s == -1:
        punkte.append((QT_X0 - 8, -Y_LTG, Z_PL))
        biegung = (BIEGUNG_PUMPE,) * 4
    else:
        punkte += [(X_P_BOGEN, Y_LTG, Z_PL), (X_P_BOGEN, py, pz), (px - 4, py, pz)]
        biegung = (BIEGUNG_PUMPE,) * 4 + (BIEGUNG_P, BIEGUNG_P)
    return Rohrzug(tuple(punkte), R_PUMPE, biegung, name="Saugleitung" if s == -1 else "Druckleitung")


def pumpenleitungen(t: Sammler) -> None:
    """Saugleitung (links) und Druckleitung (rechts), spiegelgleich gefuehrt, gehalten von kurzen Schellenboecken."""
    for s in (-1, 1):
        zug = _pumpenzug(s)
        zug.einfuegen(t)
        x_ende = QT_X0 - 8 if s == -1 else X_P_BOGEN
        if s == -1:
            t.mat("raeder", rad_x(QT_X0 - 14, -Y_LTG, Z_PL, R_PUMPE + 6, 12))             # rote Verschraubung am Tank (Video 132)
            Verschraubung((QT_X0 - 20, -Y_LTG, Z_PL), (-1, 0, 0), 46, 22).einfuegen(t)
        x = X_SCHELLE0
        while x <= x_ende - 70:
            Schelle(x, s * Y_LTG, Z_PL, R_PUMPE).einfuegen(t)
            x += DX_SCHELLE


# ---------------------------------------------------------------------------------------------------------------
# Zylinderleitungen
# ---------------------------------------------------------------------------------------------------------------
def _zylinderanschluss(t: Sammler, x: float, seite: int) -> None:
    """Verdeckter Teil im Endkasten: Schlauch von der Wanddurchfuehrung unter den Zylinder und senkrecht hoch zur Hohlschraube
    an der Unterseite von Zapfenring (x im Ring) bzw. Zylinderrohr (nahe Boden)."""
    s = seite
    y_wand = s * (EK_YI + EK_T)
    unten = Z_ZYL - (R_RING if RING_X[0] <= x <= RING_X[1] else R_ZYL)
    zf = unten - 12.0
    Rohrzug(((x, y_wand + s * 5, Z_ZYL_LTG), (x, s * Y_SCHUB, Z_ZYL_LTG), (x, s * Y_SCHUB, zf + 1)), R_SCHLAUCH,
            (R_SCHLAUCH * 1.5,), material="gummi", name="Schlauch im Endkasten").einfuegen(t)
    Verschraubung((x, s * Y_SCHUB, zf), (0, 0, 1), 40, 16).einfuegen(t)


def traversenleitungen(t: Sammler) -> None:
    """Die beiden Zylinderleitungen (Short 0:16 / 1:00): vom Block (A/B) auf der +y-Seite quer nach aussen zum Schenkel
    dicht vor der rechten Endkasten-Innenwand, senkrecht hoch auf Z_QUER, quer ueber die ganze Traverse nebeneinander, am
    linken Ende senkrecht nach unten und durch die linke Innenwand zum linken Zylinder. Rechts: zwei kurze Rohre vom Block
    durch die rechte Innenwand zum rechten Zylinder. Dazu Schottverschraubungen und Pfosten."""
    y_aus = EK_YI + EK_T + 6.0
    for i, x in enumerate(X_QUER):
        zug = Rohrzug(((x, VB_Y1 + 2, Z_BLOCK_AB[i]), (x, Y_SCHENKEL_R, Z_BLOCK_AB[i]), (x, Y_SCHENKEL_R, Z_QUER),
                       (x, Y_SCHENKEL_L, Z_QUER), (x, Y_SCHENKEL_L, Z_ZYL_LTG), (x, -y_aus, Z_ZYL_LTG)),
                      R_QUER, BIEGUNG_QUER, name=f"Querrohr {i + 1}")
        zug.einfuegen(t)
        Verschraubung((x, -(EK_YI - 14), Z_ZYL_LTG), (0, -1, 0), 50, 14).einfuegen(t)          # Schott links (aussen an der Wand)
        _zylinderanschluss(t, x, -1)
        # rechts: kurzes Rohr vom Block durch die Wand
        Rohrzug(((x, VB_Y1 + 2, Z_ZYL_LTG), (x, y_aus, Z_ZYL_LTG)), R_ANSCHL, name=f"Anschlussrohr {i + 1}").einfuegen(t)
        Verschraubung((x, EK_YI - 14, Z_ZYL_LTG), (0, 1, 0), 36, 14).einfuegen(t)                 # Schott rechts
        _zylinderanschluss(t, x, +1)
    _pfosten(t)


def _pfosten(t: Sammler) -> None:
    """Pfosten auf dem Oeltank, die beide Querrohre halten: links Flachstahlbuegel (zwei Flachstaehle), rechts-mittig Rundpfosten
    mit Kappe Ø 70 auf verschraubter Platte (Entlueftung des Oeltanks). Rohrschellen um beide Rohre, Querarm ueber den Rohren."""
    xb = QT_X0 + 8
    z_oben = Z_QUER + R_QUER
    for k, yp in enumerate(Y_PFOSTEN):
        t.append(box(QT_X0 + 2, QT_X0 + 60, yp - 35, yp + 35, QT_Z1 - 1, QT_Z1 + 10))
        t += [sechskant((QT_X0 + 40, yp + dy, QT_Z1 + 10), (0, 0, 1), 14, 6) for dy in (-22, 22)]
        if k == 0:
            for dy in (-22, 14):
                t.append(box(xb - 5, xb + 45, yp + dy, yp + dy + 8, QT_Z1 + 10, z_oben + 25))
        else:
            t.append(_scheibe_z(xb + 20, yp, QT_Z1 + 10, 22, Z_QUER - 28 - QT_Z1 - 10))
            t.append(_scheibe_z(xb + 20, yp, Z_QUER - 28, 35, 62))
        for x in X_QUER:
            t.append(ring_y(x, yp, Z_QUER, R_QUER + 6, R_QUER - 0.5, 30))
        t.append(box(X_QUER[0], xb + 2, yp - 12, yp + 12, z_oben + 3, z_oben + 13))


# ---------------------------------------------------------------------------------------------------------------
# Fassade
# ---------------------------------------------------------------------------------------------------------------
def hydraulik(t: Sammler) -> None:
    """Gesamte Hydraulikanlage in den Sammler ``t`` bauen."""
    oelpumpe(t)
    steuerblock(t)
    pumpenleitungen(t)
    traversenleitungen(t)
