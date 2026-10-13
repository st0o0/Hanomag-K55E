"""Hydraulikanlage der Planiereinrichtung: Pumpe, Steuerblock, Pumpenleitungen und Zylinderleitungen.

Doppeltwirkender 2-Zylinder-Kreis (Belege: Video Nordhorn 2:09..2:53 und YouTube-Short IApSZg9dphk 0:12..1:02):

* Die Zahnradpumpe sitzt vor dem Maskensockel; je Seite fuehrt EINE Leitung nach hinten.
  Links ist es die Saugleitung zum Oeltank, rechts die Druckleitung zum Anschluss P des Steuerblocks.
* Der Steuerblock steht auf einem Blechbock (Konsole) dicht hinter dem Sitz rechts der Sitzmitte (Short 0:13..0:17), Rueckwand an
  der Tank-Vorderwand; seine Oberkante liegt knapp unter dem Sitzschalenrand. Der Kugelhebel ist ein eigener Hebel auf einem
  Lagerbock vor dem Block und wirkt ueber Winkel und waagerechtes Gestaenge (Gabelkoepfe) auf die Schieberstange.
* Zwei Zylinderleitungen (Ø 30) steigen als Steiger aus der Blockdecke senkrecht auf z 1230. Oben sitzt je ein T-Stueck, aus dem
  ein Zweig nach links und rechts abgeht: quer, 90 Grad nach vorn ueber die Endkastendecke, 90 Grad nach unten vor der Vorderwand
  des Endkastens und 90 Grad nach aussen direkt in den Zylinder (Anschluesse uebereinander; Foto des Besitzers, Short 0:13..0:17).
  Die Rohrhalter auf dem Tank folgen Nordhorn 2:09 / 2:24.
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
from .planiermasse import QT_X0, QT_Z1, R_ZYL

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


def ring_z(x: float, y: float, z: float, r_aussen: float, r_innen: float, h: float) -> Solid:
    """Hohlzylinder um eine senkrechte Achse, mittig in z."""
    return Pos(x, y, z) * Cylinder(r_aussen, h) - Pos(x, y, z) * Cylinder(r_innen, h + 2)


# ---------------------------------------------------------------------------------------------------------------
# Masse
# ---------------------------------------------------------------------------------------------------------------
# Rohrradien
R_QUER = 15.0        # Zylinderleitungen Ø 30 (Foto des Besitzers: duenner als Ø 42)
R_PUMPE = 18.0       # Pumpenleitungen Ø 36

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
X_P_BOGEN = 2400.0                       # rechts: Abbiegen nach innen (vor dem Lagerbock des Hebels)
X_P_STEIGER = 2455.0                     # kurzes senkrechtes Stueck vor dem Anschluss P

# Steuerblock dicht hinter dem Sitz (Sitz x 2162..2518, y bis 425), Rueckwand an der Tank-Vorderwand 2630
VB_X0, VB_X1 = 2480.0, 2620.0
VB_Y0, VB_Y1 = 430.0, 560.0
VB_Z0, VB_Z1 = DECK_Z + 70.0, DECK_Z + 200.0   # Oberkante 1115, knapp unter dem Sitzschalenrand (1105..1130)
VB_PL_X = (2500.0, 2600.0)               # Blechbock (Konsole) unter dem Block
Y_HEBEL = 470.0                          # Ebene des Hebels und des Gestaenges
HEBEL_DREH = (2350.0, Y_HEBEL, 1000.0)   # Drehpunkt (Bolzen) im Lagerbock vor dem Block
HEBEL_KUGEL = (2390.0, Y_HEBEL, 1240.0)  # Kugel neben dem hinteren Sitzrand, ueber dem Polster
R_KUGEL = 25.0
Z_SCHIEBER = 1000.0                      # Schieberstange Ø 14 tritt hier aus der Blockfront
Z_PL_P = Z_PL + 50.0                     # Hoehe des Anschlusses P an der Blockfront
P_ANSCHLUSS = (VB_X0, 530.0, Z_PL_P)     # Druckanschluss P an der Vorderseite des Blocks

# Zylinderleitungen
X_STEIGER = (2540.0, 2600.0)             # zwei Steiger Ø 30 aus der Blockdecke (Rohr 1 / 2) ...
Y_STEIGER = 500.0                        # ... bei y 500
Y_QUER = (810.0, 860.0)                  # |y| der Querlaeufe; hinteres Rohr 2 aussen (kreuzungsfrei)
X_VOR = (2360.0, 2300.0)                 # x der senkrechten Abwaerts-Laeufe vor der Endkastenwand (2395, Kantenschutz 2387..2397)
Z_ANSCHLUSS = (1100.0, 1060.0)           # Anschlusshoehe am Zylinder: Rohr 1 oben, Rohr 2 unten
Z_QUER = 1230.0                          # beide Querrohre nebeneinander auf gleicher Hoehe (Short 0:13..0:16)
BIEGUNG_QUER = 45.0                      # 1,5 x Ø
R_T = 22.0                               # T-Stueck-Koerper Ø 44, 70 lang
SW_ANSCHLUSS = 30.0                      # Schluesselweite der Verschraubungen
H_ANSCHLUSS = 14.0                       # Hoehe der Winkel-/Stutzenverschraubung am Zylinderrohr
X_HALTER = 2640.0                        # senkrechter Buegel auf der Tankdecke, der Tragarm greift nach vorn unter die Rohre
X_PFOSTEN = 2810.0                       # Pfosten hinter den Querrohren (Kappe und Platte ragen etwas ueber die Tank-Rueckwand)

# Pfosten auf dem Oeltank (Frame 144 / Short): Flachstahlbuegel links-mittig, Rundpfosten (Entlueftung) rechts-mittig
Y_PFOSTEN = (-345.0, 250.0)


# ---------------------------------------------------------------------------------------------------------------
# Durchfuehrungen durch Endkastenwaende (fuer endkasten() in planierschild)
# ---------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Durchfuehrung:
    """Rundes Loch in einer Endkastenwand: Mittelpunkt ``ort``, Lochachse ``achse`` (Einheitsvektor), Radius ``radius``."""

    ort: Punkt
    achse: Punkt
    radius: float = 27.0


def durchfuehrungen(seite: int) -> list[Durchfuehrung]:
    """Loecher des Endkastens der Seite ``seite``: keine, die Zylinderrohre bleiben ausserhalb der Endkaesten."""
    del seite
    return []


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
    t.append(box(-14, PU_PL, -140, 140, PU_Z - 80, PU_Z + 80))
    for dy in (-118, 118):
        for z in (PU_Z - 60, PU_Z + 60):
            t.mat("schwarz", sechskant((-14, dy, z), (-1, 0, 0), 16, 7))
    for s in (-1, 1):
        t.append(stab((PU_XPORT, s * 50, PU_ZPORT), (PU_XPORT, s * 98, PU_ZPORT), R_PUMPE + 12))
        t.append(rad_y(PU_XPORT, s * 96, PU_ZPORT, R_PUMPE + 12, 24))
        t += [sechskant((PU_XPORT + dx, s * 104, PU_ZPORT), (0, s, 0), 12, 6) for dx in (-R_PUMPE - 7, R_PUMPE + 7)]


# ---------------------------------------------------------------------------------------------------------------
# Steuerblock
# ---------------------------------------------------------------------------------------------------------------
def _gabelkopf(t: Sammler, x: float, y: float, z: float, richtung: int) -> None:
    """Gabelkopf (zwei Backen, Querbolzen, Splint) am Stangenende; die Backen ragen ab ``x`` um 18 in ``richtung`` (+1/-1)."""
    x2 = x + richtung * 18.0
    for dy in (-8.0, 3.0):
        t.mat("blank", box(min(x, x2), max(x, x2), y + dy, y + dy + 5, z - 8, z + 8))
    xb = x + richtung * 9.0
    t.mat("blank", stab((xb, y - 11, z), (xb, y + 11, z), 3.5))
    t.mat("schwarz", box(xb - 1, xb + 1, y - 13, y - 11, z - 5, z + 1))                      # Splint


def hebelwerk(t: Sammler) -> None:
    """Handhebel nach dem Foto des Besitzers: Kugelhebel (Rohr Ø 16, Kugel Ø 50) auf einem Lagerbock (zwei Laschen mit Bolzen)
    vor dem Block, unten ein Winkel; von dort ein waagerechtes Gestaenge (Stange Ø 10 mit Gabelkoepfen) zur Schieberstange
    (Ø 14, Lasche mit Bolzen) an der Blockfront. Daneben ein kleiner Stellhebel (Ø 10 x 60) am linken Blockrand."""
    xq, yq, zq = HEBEL_DREH
    for dy in (-14.0, 8.0):                                                                   # Lagerbock
        t.append(box(xq - 15, xq + 15, yq + dy, yq + dy + 6, DECK_Z, zq + 14))
    t.append(box(xq - 15, xq + 15, yq - 14, yq + 14, DECK_Z, DECK_Z + 5))                      # Fussplatte
    t += [sechskant((xq + dx, yq, DECK_Z + 5), (0, 0, 1), 12, 5) for dx in (-9, 9)]
    t.mat("blank", stab((xq, yq - 17, zq), (xq, yq + 17, zq), 5))                              # Lagerbolzen
    t.mat("blank", sechskant((xq, yq + 17, zq), (0, 1, 0), 14, 5))
    xk, yk, zk = HEBEL_KUGEL
    richtung = (Vector(xk, yk, zk) - Vector(xq, yq, zq)).normalized()
    t.mat("blank", stab((xq, yq, zq), tuple(Vector(xk, yk, zk) - richtung * (R_KUGEL - 6)), 8))
    t.mat("schwarz", Pos(xk, yk, zk) * Sphere(R_KUGEL))
    t.mat("blank", box(xq - 8, xq + 18, yq - 4, yq + 4, zq - 8, zq + 8))                       # Winkel (Hebelarm nach hinten)
    x_g1, x_g2 = xq + 14.0, VB_X0 - 30.0                                                             # Gestaenge
    _gabelkopf(t, x_g1, yq, zq, +1)
    t.mat("blank", stab((x_g1 + 18, yq, zq), (x_g2, yq, zq), 5))
    _gabelkopf(t, x_g2 + 18, yq, zq, -1)
    t.mat("blank", stab((VB_X0 + 2, yq, Z_SCHIEBER), (x_g2 + 4, yq, Z_SCHIEBER), 7))           # Schieberstange
    t.mat("blank", box(x_g2 + 4, x_g2 + 16, yq - 3, yq + 3, Z_SCHIEBER - 8, Z_SCHIEBER + 8))   # Lasche
    xs = VB_X0 + 20.0
    t.mat("blank", stab((xs, VB_Y0 - 2, 1085), (xs - 4, VB_Y0 - 52, 1100), 5))                 # Stellhebel am linken Blockrand
    t.mat("schwarz", Pos(xs - 4, VB_Y0 - 52, 1100) * Sphere(8))


def steuerblock(t: Sammler) -> None:
    """Dunkler Sektions-Steuerblock mit quer gestapelten Rippen (Short 0:15..0:17) auf einem Blechbock (zwei Flanschschrauben),
    Hebelwerk davor (:func:`hebelwerk`). Anschluesse: zwei Steiger oben (:func:`zylinderrohr`), P (Druck von der Pumpe) vorn."""
    x0, x1, y0, y1, z0, z1 = VB_X0, VB_X1, VB_Y0, VB_Y1, VB_Z0, VB_Z1
    t.append(box(VB_PL_X[0], VB_PL_X[1], y0 + 12, y1 - 12, DECK_Z + 7, z0 + 1))                # Blechbock
    t.append(box(VB_PL_X[0] - 14, VB_PL_X[1] + 14, y0 + 4, y1 - 4, DECK_Z, DECK_Z + 7))        # Fussflansch
    t += [sechskant((x, (y0 + y1) / 2, DECK_Z + 7), (0, 0, 1), 16, 8) for x in (VB_PL_X[0] - 6, VB_PL_X[1] + 6)]
    t.mat("schwarz", kasten_rund(x0, x1, y0, y1, z0, z1 - 22, 12, Axis.Z))
    for i in range(6):
        xr = x0 + 14 + i * (x1 - x0 - 28) / 5
        t.mat("schwarz", kasten_rund(xr - 7, xr + 7, y0 - 2, y1 + 2, z0 + 12, z1 - 30, 5, Axis.Z))
    t.append(kasten_rund(x0 + 10, x1 - 10, y0 + 10, y1 - 10, z1 - 23, z1, 10, Axis.Z))
    t += [sechskant((x, y, z1), (0, 0, 1), 14, 6) for x in (x0 + 16, x1 - 16) for y in (y0 + 16, y1 - 16)]
    hebelwerk(t)
    px, py, pz = P_ANSCHLUSS
    Verschraubung((px, py, pz), (-1, 0, 0), 40, 14).einfuegen(t)


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
        punkte += [(X_P_BOGEN, Y_LTG, Z_PL), (X_P_BOGEN, py, Z_PL), (X_P_STEIGER, py, Z_PL), (X_P_STEIGER, py, pz),
                   (px - 4, py, pz)]
        biegung = (BIEGUNG_PUMPE,) * 4 + (BIEGUNG_P, BIEGUNG_P, 20.0, 20.0)
    return Rohrzug(tuple(punkte), R_PUMPE, biegung, name="Saugleitung" if s == -1 else "Druckleitung")


def pumpenleitungen(t: Sammler) -> None:
    """Saugleitung (links) und Druckleitung (rechts), spiegelgleich gefuehrt, gehalten von kurzen Schellenboecken."""
    for s in (-1, 1):
        zug = _pumpenzug(s)
        zug.einfuegen(t)
        x_ende = QT_X0 - 8 if s == -1 else X_P_BOGEN
        if s == -1:
            t.mat("lack", rad_x(QT_X0 - 14, -Y_LTG, Z_PL, R_PUMPE + 6, 12))             # Verschraubung am Tank
            Verschraubung((QT_X0 - 20, -Y_LTG, Z_PL), (-1, 0, 0), 46, 22).einfuegen(t)
        x = X_SCHELLE0
        while x <= x_ende - 70:
            Schelle(x, s * Y_LTG, Z_PL, R_PUMPE).einfuegen(t)
            x += DX_SCHELLE


# ---------------------------------------------------------------------------------------------------------------
# Zylinderleitungen
# ---------------------------------------------------------------------------------------------------------------
def zylinderrohr(t: Sammler, i: int) -> None:
    """Rohr ``i`` (0 = x 2540, 1 = x 2600): Steiger aus der Blockdecke senkrecht hoch auf Z_QUER, dort ein T-Stueck (Achse y), aus
    dem je ein Zweig nach links und rechts abgeht (Spiegelbild): quer bei Z_QUER, 90 Grad nach vorn (-x) ueber die Endkasten-
    decke, 90 Grad nach unten vor der Endkastenwand, 90 Grad nach aussen direkt in den Zylinder (Verschraubung an der
    Zylinder-Innenseite). Die Anschluesse liegen uebereinander. Das hintere Rohr (2) laeuft aussen (|y| 860 statt 810),
    sonst wuerde sein Weg nach vorn den Querlauf von Rohr 1 kreuzen."""
    x, yq, xv, z = X_STEIGER[i], Y_QUER[i], X_VOR[i], Z_ANSCHLUSS[i]
    y0 = Y_SCHUB - R_ZYL
    y_start = y0 - H_ANSCHLUSS + 2.0
    Verschraubung((x, Y_STEIGER, VB_Z1), (0, 0, 1), SW_ANSCHLUSS, H_ANSCHLUSS).einfuegen(t)
    Rohrzug(((x, Y_STEIGER, VB_Z1 + 2), (x, Y_STEIGER, Z_QUER)), R_QUER, name=f"Steiger {i + 1}").einfuegen(t)
    t.mat("blank", stab((x, Y_STEIGER - 35, Z_QUER), (x, Y_STEIGER + 35, Z_QUER), R_T))              # T-Stueck
    for s in (-1, 1):
        punkte = ((x, s * Y_STEIGER, Z_QUER), (x, s * yq, Z_QUER), (xv, s * yq, Z_QUER), (xv, s * yq, z), (xv, s * y_start, z))
        Rohrzug(punkte, R_QUER, BIEGUNG_QUER, name=f"Zylinderrohr {i + 1}").einfuegen(t)
        Verschraubung((xv, s * y0, z), (0, -s, 0), SW_ANSCHLUSS, 14.0).einfuegen(t)


def traversenleitungen(t: Sammler) -> None:
    """Die beiden Zylinderleitungen (siehe :func:`zylinderrohr`) und die Rohrhalter auf dem Oeltank."""
    for i in (0, 1):
        zylinderrohr(t, i)
    _pfosten(t)


def _halter(t: Sammler, yp: float) -> None:
    """Rohrhalter nach Nordhorn 2:09 / 2:24: Flachstahl-Buegel (40 x 8) auf Fussplatte (60 x 60 x 8, zwei Schrauben) auf der
    Tankdecke; ein waagerechter Tragarm greift nach vorn unter die Querrohre (sie liegen auf), je eine Halbschalen-Schelle
    mit zwei Schrauben haelt sie."""
    xb = X_HALTER
    z_arm = Z_QUER - R_QUER
    t.mat("lack", box(xb - 30, xb + 30, yp - 30, yp + 30, QT_Z1, QT_Z1 + 8))
    t += [sechskant((xb + 12, yp + dy, QT_Z1 + 8), (0, 0, 1), 12, 6) for dy in (-22, 22)]
    t.mat("lack", box(xb - 4, xb + 4, yp - 20, yp + 20, QT_Z1 + 8, z_arm))
    t.mat("lack", box(X_STEIGER[0] - 20, xb + 4, yp - 20, yp + 20, z_arm - 8, z_arm - 0.5))          # Tragarm
    for x in X_STEIGER:
        t.mat("blank", ring_y(x, yp, Z_QUER, R_QUER + 5, R_QUER - 0.5, 30))
        for dy in (-9.0, 9.0):
            t.mat("blank", sechskant((x, yp + dy, Z_QUER + R_QUER + 5), (0, 0, 1), 10, 5))


def _pfosten(t: Sammler) -> None:
    """Zwei Rohrhalter (:func:`_halter`) auf dem Oeltank bei y -345 und +250 sowie der Einfuellstutzen mit Kappe Ø 70 auf
    verschraubter Platte (rechts-mittig, neben dem rechten Halter)."""
    for yp in Y_PFOSTEN:
        _halter(t, yp)
    xp, yp = X_PFOSTEN, Y_PFOSTEN[1]
    t.append(box(xp - 30, xp + 30, yp - 35, yp + 35, QT_Z1 - 1, QT_Z1 + 10))
    t += [sechskant((xp, yp + dy, QT_Z1 + 10), (0, 0, 1), 14, 6) for dy in (-22, 22)]
    t.append(_scheibe_z(xp, yp, QT_Z1 + 10, 22, Z_QUER - 28 - QT_Z1 - 10))
    t.append(_scheibe_z(xp, yp, Z_QUER - 28, 35, 62))


# ---------------------------------------------------------------------------------------------------------------
# Fassade
# ---------------------------------------------------------------------------------------------------------------
def hydraulik(t: Sammler) -> None:
    """Gesamte Hydraulikanlage in den Sammler ``t`` bauen."""
    oelpumpe(t)
    steuerblock(t)
    pumpenleitungen(t)
    traversenleitungen(t)
