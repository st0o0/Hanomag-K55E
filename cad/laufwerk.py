"""Laufwerk und Ketten der K 55 E (Original-mm, Z ab Boden).

Aufbau je Seite (Fotobefund fz_01m, fz_09m, FL2, BS, Wiking-Modell, Prospekt):
  - offener Kettenrahmen: breiter Untergurt, hinten geschlossener Kasten, vorn nur
    Innensteg + Obergurt innen, damit das Spannfeder-Rohr von aussen sichtbar ist
  - Leitradgabel vorn (nach vorn offene Gleitfuehrung, Nennlage X_LEIT), Lagerschlitten mit Joch;
    das Leitrad steht in der Ist-Lage leitrad_x() (Kettenschluss, ~57 mm vor X_LEIT, Bezug X_IST).
    Die innere Gabelwange traegt bei x 560 das Joch der Querblattfeder (rumpf.py)
  - Spannfeder in einem geschlossenen Rohrgehaeuse (FL2, fz_01m: dickes Rohr zwischen Leitrad und
    Stuetzrollenbock), vorn Federteller + Stellmutter auf der Spannstange, hinten Widerlager (Sackloch);
    Rohr mit zwei Schellen auf dem Untergurt
  - 6 Laufrollen mit Spurkraenzen in Lagerboecken unter dem Untergurt, Teilung ~205
    (Video 165/167 und Flickr 40431489714: Mitten x ~885 / 1080 / 1290 / 1500 / 1710 / 1910)
  - Stuetzrolle auf einem Bock mit Gabel (Foto BS: im A-Bock-Fenster bei x ~1365)
  - Leitrad mit 5 gekruemmten, breit gegossenen Speichen, grosser Nabe, Laufkranz und Fuehrungsbund
  - Triebrad: 12 Zaehne, geschlossene Scheibe, Nabendeckel mit Schraubenkranz
  - Schwinglager hinten um die Triebradnabe (Anschluss an das Endantriebsgehaeuse)
Kette: Bodenplatte mit einem Greifer an der Hinterkante, gekroepfte Laschen (innen/aussen),
Buchse, Bolzenkoepfe, Klemmleisten mit 2 Muttern je Plattenseite. Die Kettenteilung folgt
aus dem Triebrad (12 Zaehne), die Glieder werden als Polygon um die Raeder gelegt,
der obere Trum haengt zwischen Leitrad, Stuetzrolle und Triebrad leicht durch (36 Glieder).

Lokales Querkoordinatensystem: u = Abstand von der Kettenmitte, positiv nach aussen.
Gebaut wird fuer die rechte Seite (u = +Y), die linke wird gespiegelt.
"""

from __future__ import annotations

import math
from functools import lru_cache

from build123d import (
    Axis,
    Box,
    BuildSketch,
    Circle,
    Cylinder,
    GeomType,
    Locations,
    Mode,
    Plane,
    Polygon,
    Pos,
    Rectangle,
    RegularPolygon,
    Rot,
    Shape,
    SortBy,
    chamfer,
    extrude,
    fillet,
    mirror,
)

from .common import (
    KETTE_B,
    R_TRIEB,
    RAHMEN_Z0,
    RAHMEN_Z1,
    X_LEIT,
    X_TRIEB,
    Y_KETTE,
    Z_LEIT,
    Z_PIN,
    Z_TRIEB,
    Sammler,
    box,
    rad_x,
    rad_y,
    ring_x,
    sechskant,
)

Teile = list[Shape]
Punkt = tuple[float, float]
GliedLage = tuple[float, float, float, float]    # Mitte x, z, Richtung dx, dz

# =====================================================================================================
# Parameter (Original-mm), nach Bauteil gegliedert
# =====================================================================================================

# --- Kettenglied ---
PLATTE_D, GREIFER_H = 22.0, 28.0   # flache breite Greiferrippen (Video 165/174)
HP = 17.0                          # Bolzenmitte ueber Plattenoberseite (Plattenoberseite = Z_PIN)
H_SCHIENE = 28.0                   # Laufflaeche der Laschen ueber Bolzenmitte
U_I0, U_I1, U_A1 = 57.0, 85.0, 113.0   # Lasche innen u 57..85, aussen 85..113
R_BUCHSE = 15.0
Z_BOLZEN = Z_PIN + HP              # Bolzen im unteren Trum
Z_SCHIENE = Z_BOLZEN + H_SCHIENE  # Laufflaeche unterer Trum

# --- Triebrad (Bolzenkreis, Zahnkranz) ---
N_ZAEHNE = 12
RP_TRIEB = R_TRIEB - HP            # Bolzenkreis am Triebrad
R_KOPF = 305.0                     # Zahnkopf Triebrad
TEILUNG = 2 * RP_TRIEB * math.sin(math.pi / N_ZAEHNE)   # 2 * 298,7 * sin(180/12) = 154,6
PLATTE_L = TEILUNG - 7.0

# --- Leitrad ---
# Die Leitradnabe liegt 30 tiefer als die Triebradnabe: der untere Trum bleibt horizontal auf Z_PIN + HP
# (Laufrollen), der Bolzenkreis des Leitrads folgt aus der Nabenhoehe (293, Kettenaussenradius ~330 wie im
# Flickr-Foto); das Triebrad (Bolzenkreis 299) liegt hoeher, der Trum steigt zum Triebrad an.
RP_LEIT = Z_LEIT - (Z_PIN + HP)    # Bolzenkreis am Leitrad
R_LEIT_KRANZ = 257.0               # Laufkranz (Polygoneffekt der Glieder beruecksichtigt)
# Nennlage des Leitrads in Gabel/Gleitfuehrung (Kettenschluss, 36 Glieder -> Rad ~ 393, 57 vor X_LEIT);
# Gabel, Joch, Federrohr und Untergurt sind auf diese Lage bezogen, leitrad_x() liefert die genaue Ist-Lage.
X_IST = X_LEIT - 57.0

# --- Kettenbahn ---
# Kettenschluss (Radstand X_TRIEB - X_LEIT = 1800):
#   Bolzenbahn = 2 * 1800 (Trume) + pi * (313 + 323) (Umschlingung je 180 Grad) = 5598 (+1 Durchhang)
#   Sehnen statt Bogen: am Triebrad 6,5 Teilungen = 1005 statt 1015, am Leitrad ~10 weniger -> ~ 5579
#   36 Glieder = 36 * 154,6 = 5566, 37 Glieder = 5720 (141 mm zu lang -> ~150 mm Durchhang, unbrauchbar;
#   oder Leitrad 60 mm weiter vorn -> passt nicht zum Foto)
#   -> 36 Glieder; die ~13 mm zu viel Bahn nimmt die Spannvorrichtung auf: das Leitrad steht in der
#   Gleitfuehrung 6,6 mm hinter seiner Nennlage X_LEIT (beide Trume je 6,6 mm kuerzer), x = 456,6.
#   Genau geloest in leitrad_x() (Bisektion auf die Leitradlage bei festem Durchhang SAG).
N_GLIEDER = 36
# Durchhang je Feld des oberen Trums (Leitrad-Stuetzrolle-Triebrad); Nordhorn-Video 2:44 (s164, an 6 Laufrollen
# und Triebradnabe ausgerichtet): oberer Trum fast gerade, Greiferspitzen ~ 750..765
SAG = 5.0

# --- Laufrollen ---
# SECHS Rollen (Video 165/167 + Flickr 40431489714), Mittenabstand 200..215, Mitten x ~885 / 1080 / 1290 / 1500 /
# 1710 / 1910, +-25; Teilung 203. Erste Rolle: Abstand zum Leitrad (Ist-Lage 456,6) ~ 430 > R_LEIT_KRANZ + R_ROLLE = 363.
# Letzte Rolle: Mitte nur 350 vor der Triebradnabe, Abstand sqrt(350^2 + 205^2) = 406 > Zahnkopf 328 + Mittelnut 74 = 402
# (Spurkraenze liegen bei u 128+, ausserhalb des Rades).
LAUFROLLEN_X = [885.0, 1088.0, 1291.0, 1494.0, 1697.0, 1900.0]
R_ROLLE = 90.0                     # bei Teilung ~203 muessen die Spurkraenze (R_ROLLE + 10) freibleiben
Z_ROLLE = Z_SCHIENE + R_ROLLE

# --- Stuetzrolle ---
# Foto BS zeigt sie im A-Bock-Fenster bei x ~1365, Mitte z ~600
X_STUETZ, R_STUETZ = X_TRIEB - 890.0, 75.0   # 1360
# Bolzenhoehe des oberen Trums ueber der Stuetzrolle: Der Trum laeuft auf der Geraden Leitrad-Oberkante (669) ->
# Triebrad-Oberkante (701) und liegt nur leicht durchhaengend auf der Stuetzrolle (Gerade bei x 1360: 685, minus
# SAG = 680). Greiferspitzen = Bolzen + HP + PLATTE_D + GREIFER_H = Bolzen + 67 -> ~ 735..750; Nordhorn-Video 2:53/2:56
# (n173, n179, n115): Spalt Greiferoberkante -> Unterkante Seitenblech/Lippe (808) etwa eine Plattenhoehe, 60..70.
Z_STUETZ_BOLZEN = 680.0

# --- Kettenrahmen (Untergurt, Kasten) ---
Z0, Z1 = RAHMEN_Z0, RAHMEN_Z1      # Kettenrahmen 327..467
GURT_D = 20.0                      # Untergurt
GURT_B = 175.0                     # Untergurt halbe Breite
KASTEN_B = 115.0                   # Kasten halbe Breite (230)
X_KASTEN0 = X_STUETZ - 90.0        # 1270: Kasten traegt den Stuetzrollenbock
X_KASTEN1 = X_TRIEB - 360.0        # 1890: endet vor dem Triebrad (Zahnkopf x = 1922)
X_GURT0 = X_IST + 310.0            # 760: 13 mm hinter dem Leitradbund (R 290, Ist-Lage 456,6)

# --- Leitradgabel und Stirnriegel (fest am Rahmen, Nennlage X_LEIT) ---
GABEL_U0, GABEL_U1 = 125.0, 150.0  # Leitradgabel-Wangen
GABEL_X0, GABEL_X1 = X_IST - 80.0, X_LEIT + 380.0   # 370..830 (Joch der Querfeder bei x 499..621 liegt auf)
GABEL_ZS0, GABEL_ZS1 = Z_LEIT - 43, Z_LEIT + 43     # Schlitz der Gleitfuehrung
X_RIEGEL = X_LEIT + 375.0          # Stirnriegel-Mitte 825

# --- Spannfeder im geschlossenen Rohrgehaeuse ---
# Foto FL2, fz_01m: Rohr ~160 dick, zwischen Leitrad und Stuetzrollenbock, Stange vorn zum Lagerschlitten,
# hinten Widerlager an der Kastenstirn
FEDER_U, FEDER_Z = 30.0, 425.0     # Achse Rohr/Stange
R_ROHR = 75.0
X_ROHR0 = X_IST + 460.0            # 910
X_ROHR1 = X_KASTEN0 - 15.0         # 1255 (Foto fz_01m: Rohr reicht bis knapp vor den Kasten/Stuetzrollenbock)
X_WL1 = X_ROHR1 + 35.0             # Widerlager X_ROHR1..X_WL1 (ersetzt die Kastenstirn, 1290)


# =====================================================================================================
# Private Helfer
# =====================================================================================================
def _fil(obj: Shape, kanten, r: float) -> Shape:
    """Verrundung, die bei Problemen das Original zurueckgibt."""
    try:
        k = list(kanten)
        if not k:
            return obj
        neu = fillet(k, r)
        return neu if neu.is_valid else obj
    except Exception:
        return obj


def _fas(obj: Shape, kanten, r: float) -> Shape:
    """Fase, die bei Problemen das Original zurueckgibt."""
    try:
        k = list(kanten)
        if not k:
            return obj
        neu = chamfer(k, r)
        return neu if neu.is_valid else obj
    except Exception:
        return obj


def _xz_poly(pts: list[Punkt], u0: float, u1: float) -> Shape:
    """Polygon in der XZ-Ebene (x, z), extrudiert von u0 bis u1 (Y)."""
    f = Plane.XZ * Polygon(*pts, align=None)
    return Pos(0, (u0 + u1) / 2, 0) * extrude(f, amount=abs(u1 - u0) / 2, both=True)


def _rad_mat(mat: str) -> str:
    """Laufraeder (Leitrad, Triebrad, Lauf- und Stuetzrollen) bekommen ein eigenes Material: ab Werk
    waren die Raeder rot abgesetzt (Hanomag ab 1953: Aufbau gruen bzw. blau, Raeder rot)."""
    return "raeder" if mat == "lack" else mat


def _setzen(t: Sammler, rad: Sammler, pos: Pos, dreh: float = 0.0) -> None:
    """Teile eines lokal gebauten Rades (Achse = Y, Mitte im Ursprung) an pos setzen, optional um Y gedreht."""
    for mat, lst in rad.schichten().items():
        t.mat(_rad_mat(mat), [pos * Rot(0, dreh, 0) * s for s in lst])


# =====================================================================================================
# Kettenbahn
# =====================================================================================================
def _fuehrung(xl: float, sag: float = SAG, ds: float = 2.0) -> list[Punkt]:
    """Leitkurve der Bolzenmitten (Leitrad bei xl): unten vor, um das Leitrad, oberer Trum mit
    Durchhang, um das Triebrad."""
    pts: list[Punkt] = []
    zb = Z_BOLZEN
    # Rampe: ab XP steigt der untere Trum tangential zur Unterseite des Triebrads (Nabe 24 hoeher)
    xp = LAUFROLLEN_X[-1] + 100.0
    dx, dz = X_TRIEB - xp, Z_TRIEB - zb
    d = math.hypot(dx, dz)
    a_t = math.atan2(-dz, -dx) + math.acos(RP_TRIEB / d)       # Beruehrpunkt (Winkel um die Triebradnabe)
    tx, tz = X_TRIEB + RP_TRIEB * math.cos(a_t), Z_TRIEB + RP_TRIEB * math.sin(a_t)
    n = int(math.hypot(tx - xp, tz - zb) / ds)
    pts += [(tx + (xp - tx) * i / n, tz + (zb - tz) * i / n) for i in range(n)]
    n = int((xp - xl) / ds)
    pts += [(xp - (xp - xl) * i / n, zb) for i in range(n)]
    n = int(math.pi * RP_LEIT / ds)
    for i in range(n):
        a = math.radians(270 - 180 * i / n)
        pts.append((xl + RP_LEIT * math.cos(a), Z_LEIT + RP_LEIT * math.sin(a)))

    def feld(x0: float, z0: float, x1: float, z1: float, d: float) -> None:
        n = int((x1 - x0) / ds)
        for i in range(n):
            t = i / n
            pts.append((x0 + (x1 - x0) * t, z0 + (z1 - z0) * t - 4 * d * t * (1 - t)))

    feld(xl, Z_LEIT + RP_LEIT, X_STUETZ, Z_STUETZ_BOLZEN, sag)
    feld(X_STUETZ, Z_STUETZ_BOLZEN, X_TRIEB, Z_TRIEB + RP_TRIEB, sag)
    w = math.radians(90) - a_t
    n = int(w * RP_TRIEB / ds)
    for i in range(n + 1):
        a = math.radians(90) - w * i / n
        pts.append((X_TRIEB + RP_TRIEB * math.cos(a), Z_TRIEB + RP_TRIEB * math.sin(a)))
    return pts


def _laufen(G: list[Punkt], n: int, p: float) -> tuple[list[Punkt], bool]:
    """n Glieder der Teilung p entlang der Leitkurve G abtragen; liefert (Bolzenpunkte, ok)."""
    P, j, pins = G[0], 0, [G[0]]
    for _ in range(n):
        while j < len(G) - 1 and math.dist(P, G[j + 1]) < p:
            j += 1
        if j >= len(G) - 1:
            return pins, False
        (ax, az), (bx, bz) = G[j], G[j + 1]
        dx, dz, fx, fz = bx - ax, bz - az, ax - P[0], az - P[1]
        A, B, C = dx * dx + dz * dz, 2 * (fx * dx + fz * dz), fx * fx + fz * fz - p * p
        t = (-B + math.sqrt(max(0.0, B * B - 4 * A * C))) / (2 * A)
        P = (ax + t * dx, az + t * dz)
        pins.append(P)
    return pins, True


def _rest(xl: float) -> float:
    """Schlussfehler: Abstand letzter -> erster Bolzen minus Teilung (> 0: Bahn zu lang)."""
    pins, ok = _laufen(_fuehrung(xl), N_GLIEDER - 1, TEILUNG)
    return (math.dist(pins[-1], pins[0]) - TEILUNG) if ok else -1e9


@lru_cache(maxsize=1)
def leitrad_x() -> float:
    """Ist-Lage des Leitrads in der Gleitfuehrung: Versatz vor X_LEIT, bei dem N_GLIEDER bei festem
    Durchhang SAG genau schliessen (Bahn waechst, wenn das Leitrad nach vorn geht)."""
    lo, hi = X_IST - 40.0, X_IST + 40.0    # Spannweite der Gleitfuehrung (Bahn liegt hinter Nennlage)
    if _rest(lo) < 0 or _rest(hi) > 0:
        raise ValueError("Kette schliesst nicht innerhalb der Spannweite")
    for _ in range(40):
        mid = (lo + hi) / 2
        if _rest(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


@lru_cache(maxsize=1)
def bolzenpunkte() -> tuple[Punkt, ...]:
    """Bolzenmitten (x, z) der geschlossenen Kette."""
    pins, _ = _laufen(_fuehrung(leitrad_x()), N_GLIEDER - 1, TEILUNG)
    return tuple(pins)


def _glied_lagen() -> list[GliedLage]:
    """(Mitte x, z, Richtung dx, dz) je Glied."""
    pins = bolzenpunkte()
    out = []
    for i in range(len(pins)):
        a, b = pins[i], pins[(i + 1) % len(pins)]
        L = math.dist(a, b)
        out.append(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (b[0] - a[0]) / L, (b[1] - a[1]) / L))
    return out


def _phase_triebrad() -> float:
    """Drehung (Grad) des Triebrads, damit die Zahnluecken unter den Bolzen liegen: der erste bzw. letzte
    Bolzen liegt im Beruehrpunkt der Rampe (Winkel a_t um die Nabe), die Luecken unten bei -90 + k * 30."""
    p0 = bolzenpunkte()[0]
    return (math.degrees(math.atan2(p0[1] - Z_TRIEB, p0[0] - X_TRIEB)) + 90.0) % (360.0 / N_ZAEHNE)


# =====================================================================================================
# Kettenglied
# =====================================================================================================
def _lasche(vorn: bool, u0: float, u1: float) -> Shape:
    """Gekroepfte Laschenhaelfte: Auge um den Bolzen, Laufflaeche oben, Fuss auf der Platte."""
    p = TEILUNG
    xp = p / 2 if vorn else -p / 2
    xo = -10.0 if vorn else 10.0
    with BuildSketch(Plane.XZ) as sk:
        with Locations(((xp + xo) / 2, (H_SCHIENE - HP) / 2)):
            Rectangle(abs(xp - xo), H_SCHIENE + HP)
        with Locations((xp, 0)):
            Circle(H_SCHIENE)
        with Locations((xp, -HP - 30)):
            Rectangle(100, 60, mode=Mode.SUBTRACT)
        # Augenende unten abgeschraegt: Freigang zur Nachbarplatte beim Umlenken (bis ~32 Grad)
        sg = 1.0 if vorn else -1.0
        Polygon((xp - sg * 6, -HP - 1), (xp - sg * 6, -HP), (xp + sg * 46, -HP + 52 * 0.62),
                (xp + sg * 46, -HP - 1), align=None, mode=Mode.SUBTRACT)
    s = Pos(0, u1, 0) * extrude(sk.sketch, amount=u1 - u0)
    return _fas(s, s.edges().filter_by(Axis.X).group_by(Axis.Z)[-1], 3)


def _glied_platte() -> Teile:
    """Bodenplatte mit keilfoermigem Greifer an der Hinterkante (Greiferenden abgeschraegt)."""
    L = PLATTE_L
    zp0, zp1 = -HP - PLATTE_D, -HP
    platte = box(-L / 2, L / 2, -KETTE_B / 2, KETTE_B / 2, zp0, zp1)
    platte = _fas(platte, platte.edges().filter_by(Axis.Y), 4)
    g = _xz_poly([(-L / 2, zp0 + 1), (-L / 2 + 30, zp0 + 1), (-L / 2 + 20, zp0 - GREIFER_H),
                  (-L / 2 + 4, zp0 - GREIFER_H)], -KETTE_B / 2, KETTE_B / 2)
    for s in (-1, 1):
        cut = Pos(0, s * KETTE_B / 2, zp0) * Rot(s * 45, 0, 0) * Box(2 * L, 40, 40)
        g = g - Pos(0, 0, -GREIFER_H) * cut
    return [platte, g]


def _glied_seite(s: int) -> Teile:
    """Laschen, Bolzenkopf und Klemmleiste einer Plattenseite (s = +-1)."""
    t = []
    # Laschen: hinten innen, vorn aussen (gekroepft)
    for vorn, (a, b) in ((False, (U_I0, U_I1)), (True, (U_I1, U_A1))):
        las = _lasche(vorn, a, b)
        t.append(las if s > 0 else mirror(las, Plane.XZ))
    # Bolzenkopf vorn aussen
    t.append(rad_y(TEILUNG / 2, s * (U_A1 + 3), 0, 14, 6))
    # Klemmleiste mit 2 Muttern je Plattenseite
    t.append(box(-52, 52, s * (U_A1 - 1), s * 152, -HP, -HP + 10))
    for x in (-32, 32):
        t.append(sechskant((x, s * 134, -HP + 10), (0, 0, 1), 24, 11))
    return t


@lru_cache(maxsize=1)
def kettenglied() -> Shape:
    """Ein Glied lokal: x Laufrichtung, z zur Kettenmitte (zu den Raedern), Bolzenlinie z=0,
    Bolzen bei x = +-TEILUNG/2, Plattenoberseite bei z = -HP."""
    t = _glied_platte()
    for s in (-1, 1):
        t += _glied_seite(s)
    t.append(rad_y(-TEILUNG / 2, 0, 0, R_BUCHSE, 2 * U_I0 + 6))          # Buchse
    teil = t[0]
    for x in t[1:]:
        teil = teil + x
    return teil


def kette(seite: int) -> Teile:
    """Kette einer Seite (seite = +-1): alle Glieder entlang der Bolzenbahn gesetzt."""
    y = seite * Y_KETTE
    glied = kettenglied()
    out = []
    for x, z, dx, dz in _glied_lagen():
        pl = Plane(origin=(x, y, z), x_dir=(dx, 0, dz), z_dir=(dz, 0, -dx))
        out.append(pl.location * glied)
    return out


# =====================================================================================================
# Raeder (lokal, Achse = Y, Mitte im Ursprung)
# =====================================================================================================
def _leitrad_speiche() -> Shape:
    """Eine gekruemmte, breit gegossene Speiche (flacher Steg mit Randrippen) in der XZ-Ebene."""
    r0, r1 = 110.0, R_LEIT_KRANZ - 24
    schwung = math.radians(27)                # Schwung der Speichenmitte zwischen Nabe und Kranz
    n = 10
    pm, pl, pr = [], [], []
    for k in range(n + 1):
        f = k / n
        r = r0 + (r1 - r0) * f
        th = schwung * f**1.3
        hw = 60 - 22 * f                      # halbe Breite: 60 an der Nabe, 38 am Kranz
        c, sn = math.cos(th), math.sin(th)
        tx, tz = (-sn, c)                     # Quervektor
        pm.append((r * c, r * sn))
        pl.append((r * c + hw * tx, r * sn + hw * tz))
        pr.append((r * c - hw * tx, r * sn - hw * tz))
    steg = _xz_poly(pl + pr[::-1], -14, 14)
    rippen = None
    for pk in (pl, pr):
        # Randrippe: schmaler Streifen entlang der Kante, nach innen versetzt
        rand = [(p[0] + (q[0] - p[0]) * 0.22, p[1] + (q[1] - p[1]) * 0.22) for p, q in zip(pk, pm, strict=True)]
        rp = _xz_poly(pk + rand[::-1], -34, 34)
        rippen = rp if rippen is None else rippen + rp
    return steg + rippen


def leitrad() -> Sammler:
    """Leitrad: Laufkranz mit Fuehrungsbund, grosse Nabe, 5 Speichen, Nabendeckel mit Schrauben."""
    t = Sammler("lack")
    kranz = rad_y(0, 0, 0, R_LEIT_KRANZ, 2 * 118) - rad_y(0, 0, 0, R_LEIT_KRANZ - 30, 250)
    kranz = _fas(kranz, kranz.edges().filter_by(GeomType.CIRCLE).group_by(SortBy.RADIUS)[-1], 6)
    bund = rad_y(0, 0, 0, R_LEIT_KRANZ + 17, 76) - rad_y(0, 0, 0, R_LEIT_KRANZ - 10, 90)
    bund = _fas(bund, bund.edges().filter_by(GeomType.CIRCLE).group_by(SortBy.RADIUS)[-1], 5)
    t += [kranz, bund]
    # Innenwulst am Kranz
    t.append(rad_y(0, 0, 0, R_LEIT_KRANZ - 28, 60) - rad_y(0, 0, 0, R_LEIT_KRANZ - 48, 70))
    # grosse Nabe (Video 165/196, Flickr: dicke Nabenbuechse mit Flansch, deutlich groesser als die Achse)
    nabe = rad_y(0, 0, 0, 128, 210)
    t.append(_fas(nabe, nabe.edges(), 8))
    t.append(rad_y(0, 0, 0, 158, 70))                                       # Nabenring / Flansch
    # 5 gekruemmte, breit gegossene Speichen (Flickr/Video: stark geschwungen, flacher Steg mit Randrippen)
    speiche = _leitrad_speiche()
    for i in range(5):
        t.append(Rot(0, i * 72 + 18, 0) * speiche)
    # Nabendeckel aussen + innen mit Schrauben
    t.append(rad_y(0, 112, 0, 96, 14))
    t.append(rad_y(0, -112, 0, 96, 14))
    for i in range(6):
        a = math.radians(i * 60 + 30)
        t.mat("blank", sechskant((68 * math.cos(a), 119, 68 * math.sin(a)), (0, 1, 0), 18, 6))
    t.mat("blank", rad_y(0, 0, 0, 36, 2 * 127))                              # Achse
    return t


def _zahnkranz() -> Shape:
    """Zahnkranz des Triebrads (12 Zaehne, Buchsenmulden), Zahnkoepfe seitlich angefast."""
    rp, n = RP_TRIEB, N_ZAEHNE
    with BuildSketch(Plane.XZ) as sk:
        Circle(R_KOPF)
        Circle(RP_TRIEB - 48, mode=Mode.SUBTRACT)
        for k in range(n):
            a = math.radians(-90 + k * 360 / n)
            e, tt = (math.cos(a), math.sin(a)), (-math.sin(a), math.cos(a))

            def P(r: float, w: float, e: Punkt = e, tt: Punkt = tt) -> Punkt:
                return (r * e[0] + w * tt[0], r * e[1] + w * tt[1])

            with Locations(P(rp, 0)):
                Circle(R_BUCHSE + 1.5, mode=Mode.SUBTRACT)
            Polygon(P(rp - 6, -(R_BUCHSE + 1.3)), P(rp - 6, R_BUCHSE + 1.3), P(rp + 1, 24), P(rp + 12, 52),
                    P(rp + 30, 60), P(rp + 30, -60), P(rp + 12, -52), P(rp + 1, -24),
                    align=None, mode=Mode.SUBTRACT)
    z = extrude(sk.sketch, amount=30, both=True)
    kanten = z.edges().filter_by(Axis.Y, reverse=True)
    return _fas(z, kanten.filter_by_position(Axis.Y, 29, 31) + kanten.filter_by_position(Axis.Y, -31, -29), 3)


def _triebrad_aussen(t: Sammler) -> None:
    """Nabenflansch aussen mit Schraubenkranz, Nabendeckel mit Schrauben."""
    fl = rad_y(0, 45, 0, 168, 60)
    t.append(_fas(fl, fl.edges().group_by(Axis.Y)[-1], 8))
    for i in range(10):
        a = math.radians(i * 36)
        t.mat("blank", sechskant((135 * math.cos(a), 75, 135 * math.sin(a)), (0, 1, 0), 26, 13))
    deckel = rad_y(0, 90, 0, 82, 30)
    t.append(_fas(deckel, deckel.edges().group_by(Axis.Y)[-1], 6))
    for i in range(6):
        a = math.radians(i * 60)
        t.mat("blank", sechskant((56 * math.cos(a), 105, 56 * math.sin(a)), (0, 1, 0), 18, 9))


def triebrad() -> Sammler:
    """Triebrad: Zahnkranz, geschlossene Scheibe mit Randwulst und Rippen, Naben aussen und innen."""
    t = Sammler("lack")
    t.append(_zahnkranz())
    scheibe = rad_y(0, 0, 0, RP_TRIEB - 40, 30)                             # geschlossene Scheibe
    for i in range(N_ZAEHNE):                                                 # Zahnkranzschrauben
        w = math.radians(i * 360 / N_ZAEHNE + 180 / N_ZAEHNE - 90)
        t.mat("blank", sechskant((262 * math.cos(w), 30, 262 * math.sin(w)), (0, 1, 0), 18, 8))
    t.append(scheibe)
    t.append(rad_y(0, 0, 0, RP_TRIEB - 46, 44) - rad_y(0, 0, 0, RP_TRIEB - 70, 50))   # Randwulst
    _triebrad_aussen(t)
    # Rippen auf der Innenseite der Scheibe
    for i in range(N_ZAEHNE):
        t.append(Rot(0, i * 360 / N_ZAEHNE, 0) * box(120, RP_TRIEB - 60, -40, -15, -9, 9))
    # Nabe innen bis zum Endantriebsgehaeuse (u = -210)
    t.append(rad_y(0, -107.5, 0, 120, 185))
    t.append(rad_y(0, -204, 0, 155, 12))
    return t


def _lagerbock(t: Sammler, s: int, hz: float) -> None:
    """Lagerbock einer Laufrolle (Seite s = +-1): Wange, Fuss auf dem Untergurt, Schrauben, Achsdeckel."""
    ua, ub = sorted((s * 142, s * 162))
    wange = _xz_poly([(-56, -10), (56, -10), (72, hz - 12), (-72, hz - 12)], ua, ub)
    wange = wange + Pos(0, s * 152, 0) * Rot(90, 0, 0) * Cylinder(56, 20)
    wange = wange + _xz_poly([(-9, 48), (9, 48), (9, hz - 12), (-9, hz - 12)], *sorted((s * 160, s * 172)))
    t.append(wange)
    fuss = box(-78, 78, s * 136, s * 182, hz - 12, hz)
    t.append(_fas(fuss, fuss.edges().filter_by(Axis.Y).group_by(Axis.Z)[0], 4))
    for x in (-60, 60):
        t.mat("blank", sechskant((x, s * 172, hz - 12), (0, 0, -1), 20, 9))
    t.append(rad_y(0, s * 166, 0, 30, 8))                                 # Achsdeckel (Video 165: klein)
    t.mat("blank", sechskant((0, s * 170, 0), (0, s, 0), 24, 8))          # eine Achsmutter


def laufrolle() -> tuple[Sammler, float]:
    """Doppelte Laufbahn auf den Laschen, Spurkraenze aussen, Lagerboecke mit Achsdeckeln.
    Liefert (Teile lokal um die Rollenmitte, Rollenmitte z)."""
    t = Sammler("lack")
    zr = Z_ROLLE
    rolle = rad_y(0, 0, 0, R_ROLLE, 240) - rad_y(0, 0, 0, R_ROLLE + 5, 2 * (U_I0 - 6))
    rolle = rolle + rad_y(0, 0, 0, R_ROLLE - 16, 2 * U_I0)                   # Mittelnut
    t.append(rolle)
    for s in (-1, 1):
        sk = rad_y(0, s * 128, 0, R_ROLLE + 10, 16)
        t.append(_fas(sk, sk.edges().group_by(Axis.Y)[-1 if s > 0 else 0], 5))
        t.append(rad_y(0, s * 139, 0, 52, 6))                                 # Dichtring
    t.mat("blank", rad_y(0, 0, 0, 30, 2 * 163))                             # Achse
    for s in (-1, 1):
        _lagerbock(t, s, Z0 - zr)
    return t, zr


def stuetzrolle(zc: float) -> Sammler:
    """Stuetzrolle mit Gabelbock auf dem Kasten; zc = Rollenmitte."""
    t = Sammler("lack")
    rolle = rad_y(0, 0, 0, R_STUETZ, 236) - rad_y(0, 0, 0, R_STUETZ + 5, 2 * (U_I0 - 6))
    rolle = rolle + rad_y(0, 0, 0, R_STUETZ - 14, 2 * U_I0)
    t.append(_fas(rolle, rolle.edges().filter_by(GeomType.CIRCLE).group_by(SortBy.RADIUS)[-1], 4))
    t.mat("blank", rad_y(0, 0, 0, 25, 2 * 152))
    zkopf0 = 500.0 - zc
    for s in (-1, 1):
        u0, u1 = (124, 146) if s > 0 else (-146, -124)
        w = _xz_poly([(-55, zkopf0 + 25), (55, zkopf0 + 25), (42, 0), (-42, 0)], u0, u1)
        w = w + Pos(0, s * 135, 0) * Rot(90, 0, 0) * Cylinder(42, 22)
        t.append(w)
        t.append(rad_y(0, s * 150, 0, 30, 8))
        t.mat("blank", sechskant((0, s * 154, 0), (0, s, 0), 22, 9))
    kopf = box(-60, 60, -150, 150, zkopf0, zkopf0 + 25)
    t.append(_fas(kopf, kopf.edges().filter_by(Axis.Y), 6))
    t.append(box(-35, 35, -70, 70, Z1 - zc, zkopf0))                          # Saeule
    for s in (-1, 1):                                                         # Knotenbleche
        t.append(_xz_poly([(35, Z1 - zc), (75, Z1 - zc), (35, zkopf0)], -8, 8) if s > 0 else
                 _xz_poly([(-35, Z1 - zc), (-35, zkopf0), (-75, Z1 - zc)], -8, 8))
    return t


# =====================================================================================================
# Kettenrahmen
# =====================================================================================================
def _stuetz_z() -> float:
    """Hoehe der Stuetzrollenmitte aus der tatsaechlichen Lage des oberen Trums."""
    best = None
    for x, z, dx, dz in _glied_lagen():
        if z > 500 and abs(x - X_STUETZ) < TEILUNG / 2 + 1:
            n = (dz, -dx)                       # nach innen (unten)
            qx, qz = x + n[0] * H_SCHIENE, z + n[1] * H_SCHIENE
            if abs(dx) < 1e-6:
                continue
            s = (X_STUETZ - qx - R_STUETZ * n[0]) / dx
            zc = qz + s * dz + R_STUETZ * n[1]
            best = zc if best is None else min(best, zc)
    return best


def _untergurt_kasten(t: Sammler) -> None:
    """Untergurt, Kasten hinten mit Deckeln, vorderer offener Teil (Innensteg, innerer Obergurt, Rippen)."""
    # Untergurt (breit, traegt die Lagerboecke)
    gurt = box(X_GURT0, X_KASTEN1, -GURT_B, GURT_B, Z0, Z0 + GURT_D)
    t.append(_fil(gurt, gurt.edges().filter_by(Axis.Z), 20))
    # Verlaengerung nur aussen (u 100..175), damit der Lagerbock der sechsten Laufrolle (x 1885 +-78) aufliegt;
    # weiter innen steht das Triebrad (Zahnkopf x = 1922)
    ext = box(X_KASTEN1 - 20, LAUFROLLEN_X[-1] + 95.0, 100.0, GURT_B, Z0, Z0 + GURT_D)
    t.append(_fil(ext, ext.edges().filter_by(Axis.Z).group_by(Axis.X)[-1], 15))
    # Kasten hinten
    kasten = box(X_KASTEN0, X_KASTEN1, -KASTEN_B, KASTEN_B, Z0 + GURT_D - 1, Z1)
    kasten = _fil(kasten, kasten.edges().filter_by(Axis.X).group_by(Axis.Z)[-1], 25)
    kasten = _fil(kasten, kasten.edges().filter_by(Axis.Z).group_by(Axis.X)[-1], 20)
    # Stirn des Kastens fuer das Widerlager des verlaengerten Federrohrs freilegen
    kasten -= box(X_KASTEN0 - 1, X_WL1, -KASTEN_B - 1, KASTEN_B + 1, Z0, Z1 + 1)
    t.append(kasten)
    # Deckel aussen mit Schraubenreihen
    t.append(box(X_KASTEN0 + 60, X_KASTEN1 - 60, KASTEN_B - 1, KASTEN_B + 6, Z0 + 40, Z1 - 30))
    for i in range(8):
        x = X_KASTEN0 + 80 + i * (X_KASTEN1 - X_KASTEN0 - 160) / 7
        for z in (Z0 + 52, Z1 - 42):
            t.mat("blank", sechskant((x, KASTEN_B + 6, z), (0, 1, 0), 20, 8))
    # Kasten innen: Deckel
    t.append(box(X_KASTEN0 + 60, X_KASTEN1 - 60, -KASTEN_B - 6, -KASTEN_B + 1, Z0 + 40, Z1 - 30))
    # vorderer, offener Teil: Innensteg + innerer Obergurt + Rippen
    t.append(box(X_GURT0, X_KASTEN0, -KASTEN_B, -KASTEN_B + 20, Z0 + GURT_D - 1, Z1))
    t.append(box(X_GURT0, X_KASTEN0, -KASTEN_B, -48, Z1 - 20, Z1))
    for k in (0.22, 0.55, 0.85):
        x = X_GURT0 + k * (X_KASTEN0 - X_GURT0)
        t.append(_xz_poly([(x - 8, Z0 + GURT_D), (x + 8, Z0 + GURT_D), (x + 8, Z1 - 20), (x - 8, Z1 - 20)],
                          -KASTEN_B + 19, -48))
    # Rippen aussen am Untergurt, jeweils zwischen zwei Laufrollen
    for x in ((LAUFROLLEN_X[0] + LAUFROLLEN_X[1]) / 2, (LAUFROLLEN_X[1] + LAUFROLLEN_X[2]) / 2):
        t.append(_xz_poly([(x - 8, Z0 + GURT_D), (x + 8, Z0 + GURT_D), (x + 8, Z0 + GURT_D + 25),
                           (x - 8, Z0 + GURT_D + 25)], 95, GURT_B - 5))


def _leitradgabel(t: Sammler) -> None:
    """Stirnriegel hinter dem Leitrad (oben/unten) und die nach vorn offene Gleitfuehrung mit Gleitleisten.
    Die Oberkante der inneren Wange (u -150..-125, z = Z1 + 3) traegt bei x 499..621 das Joch der Querfeder."""
    zs0, zs1 = GABEL_ZS0, GABEL_ZS1
    t.append(box(X_RIEGEL - 10, X_RIEGEL + 10, -GABEL_U1, GABEL_U1, Z0, Z0 + 23))
    t.append(box(X_RIEGEL - 10, X_RIEGEL + 10, -GABEL_U1, GABEL_U1, Z1 - 17, Z1 + 3))
    g0, g1 = GABEL_X0, GABEL_X1
    for u0, u1 in ((GABEL_U0, GABEL_U1), (-GABEL_U1, -GABEL_U0)):
        # Schraege Stirn der Schienen: Keilspitze (Messerkante) auf 8 mm Original gekappt, senkrechte Stirnkante >= 4 mm
        kz = 8.0 / 30.0
        ob = _xz_poly([(g0 + 8, zs1), (g1, zs1), (g1, Z1 + 3), (g0 + 30, Z1 + 3),
                       (g0 + 8, zs1 + kz * (Z1 + 3 - zs1))], u0, u1)
        un = _xz_poly([(g0 + 30, Z0), (g1, Z0), (g1, zs0), (g0 + 8, zs0),
                       (g0 + 8, zs0 - kz * (zs0 - Z0))], u0, u1)
        t += [ob, un]
        # Gleitleisten aussen, verschraubt
        ua, ub = (u1, u1 + 10) if u0 > 0 else (u0 - 10, u0)
        un_ = ub if u0 > 0 else ua
        for za, zb in ((zs1 - 8, zs1 + 14), (zs0 - 14, zs0 + 8)):
            t.append(box(g0 + 10, g1 - 10, ua, ub, za, zb))
            for i in range(4):
                x = g0 + 50 + i * (g1 - g0 - 100) / 3
                t.mat("blank", sechskant((x, un_, (za + zb) / 2), (0, 1 if u0 > 0 else -1, 0), 16, 7))


def _lagerschlitten(t: Sammler, xl: float) -> float:
    """Lagerschlitten in der Gabel (Ist-Lage des Leitrads xl) mit Joch hinter dem Leitrad und Stangenkopf.
    Liefert die x-Lage des Jochs."""
    zs0, zs1 = GABEL_ZS0, GABEL_ZS1
    for s in (-1, 1):
        u0, u1 = (127, 148) if s > 0 else (-148, -127)
        t.append(box(xl - 60, xl + 345, u0, u1, zs0 + 3, zs1 - 3))
        t.append(rad_y(xl, s * 156, Z_LEIT, 32, 16))                          # Lagerdeckel
        t.mat("blank", sechskant((xl, s * 164, Z_LEIT), (0, s, 0), 30, 12))
    xj = xl + 310.0                                                           # Joch 20 hinter dem Leitradbund
    joch = box(xj, xj + 40, -127, 127, zs0 + 8, zs1 - 8)
    t.append(_fas(joch, joch.edges().filter_by(Axis.Y), 6))
    t.append(rad_x(xj + 52, FEDER_U, FEDER_Z, 22, 24))                       # Stangenkopf (zwischen den Riegeln)
    return xj


def _spannfeder(t: Sammler, xj: float) -> None:
    """Spannfeder im geschlossenen Rohrgehaeuse (Feder selbst unsichtbar): Stange, Federteller, Stellmutter, Rohr mit
    Endringen und Schellen, Widerlager mit Sackloch."""
    # Stange vom Stangenkopf durch Federteller und Rohr bis hinter das Widerlager
    x_st1 = X_ROHR1 + 15                                                      # endet im Sackloch des Widerlagers
    t.mat("blank", rad_x((xj + 64 + x_st1) / 2, FEDER_U, FEDER_Z, 20, x_st1 - xj - 64))
    tel = rad_x(X_ROHR0 - 9, FEDER_U, FEDER_Z, 62, 24)                        # vorderer Federteller (sichtbar)
    t.append(_fas(tel, tel.edges(), 4))
    t.mat("blank", Pos(X_ROHR0 - 21 - 20, FEDER_U, FEDER_Z) * Rot(0, 90, 0)
          * extrude(RegularPolygon(30, 6), amount=20))                       # Stellmutter vor dem Teller
    rohr = rad_x((X_ROHR0 + X_ROHR1 + 3) / 2, FEDER_U, FEDER_Z, R_ROHR, X_ROHR1 + 3 - X_ROHR0)
    t.append(_fas(rohr, rohr.edges(), 6))
    for x in (X_ROHR0 + 14, X_ROHR1 - 14):                                    # Endringe
        t.append(rad_x(x, FEDER_U, FEDER_Z, R_ROHR + 7, 22))
    t.append(rad_x(X_ROHR0 - 2, FEDER_U, FEDER_Z, 34, 8))                    # Stopfbuchse vorn
    # Rohrschellen mit Saettel auf dem Untergurt
    for x in (X_ROHR0 + 70, X_ROHR1 - 70):
        t.append(ring_x(x, FEDER_U, FEDER_Z, R_ROHR + 8, R_ROHR - 2, 30))
        t.append(box(x - 22, x + 22, FEDER_U - 50, FEDER_U + 50, Z0 + GURT_D - 1, FEDER_Z - 45))
        for su in (-1, 1):
            t.mat("blank", sechskant((x, FEDER_U + su * 62, Z0 + GURT_D - 0.5), (0, 0, 1), 18, 8))
    # Widerlager (Rohr stuetzt sich vorn dagegen, ersetzt die Kastenstirn), Stange endet im Sackloch
    wl = (box(X_ROHR1, X_WL1, -KASTEN_B, KASTEN_B, Z0 + GURT_D - 1, FEDER_Z + R_ROHR + 5)
          - rad_x(X_ROHR1 + 10, FEDER_U, FEDER_Z, 22, 22))
    t.append(_fil(wl, wl.edges().filter_by(Axis.X).group_by(Axis.Z)[-1], 15))


def _schwinglager(t: Sammler) -> None:
    """Schwinglager hinten um die Triebradnabe (Endantrieb) mit 4 Schrauben."""
    arm = box(X_KASTEN1 - 40, X_TRIEB, -195, -60, Z_TRIEB - 60, Z_TRIEB + 60) + rad_y(X_TRIEB, -160, Z_TRIEB, 205, 70)
    t.append(arm - rad_y(X_TRIEB, -125, Z_TRIEB, 126, 170))
    for i in range(4):
        a = math.radians(45 + 90 * i)
        t.mat("blank", sechskant((X_TRIEB + 182 * math.cos(a), -195, Z_TRIEB + 182 * math.sin(a)), (0, -1, 0), 24, 11))


def _raeder_setzen(t: Sammler, xl: float) -> None:
    """Laufrollen, Stuetzrolle, Leitrad und Triebrad an ihre Lagen setzen (Raeder-Material)."""
    rolle, zr = laufrolle()
    for x in LAUFROLLEN_X:
        _setzen(t, rolle, Pos(x, 0, zr))
    zc = _stuetz_z()
    _setzen(t, stuetzrolle(zc), Pos(X_STUETZ, 0, zc))
    _setzen(t, leitrad(), Pos(xl, 0, Z_LEIT))
    _setzen(t, triebrad(), Pos(X_TRIEB, 0, Z_TRIEB), -_phase_triebrad())


def _rahmen_rechts() -> Sammler:
    """Kettenrahmen rechte Seite, Kettenmitte bei y=0, u = +Y nach aussen."""
    t = Sammler("lack")
    xl = leitrad_x()
    _untergurt_kasten(t)
    _leitradgabel(t)
    xj = _lagerschlitten(t, xl)
    _spannfeder(t, xj)
    _schwinglager(t)
    _raeder_setzen(t, xl)
    return t


def kettenrahmen(seite: int) -> Sammler:
    """Kettenrahmen mit Raedern einer Seite (seite = +-1); links wird die rechte Seite gespiegelt."""
    r = _rahmen_rechts()
    out = Sammler("lack")
    for mat, lst in r.schichten().items():
        neu = []
        for s in lst:
            if seite < 0:
                s = mirror(s, Plane.XZ)
            neu.append(Pos(0, seite * Y_KETTE, 0) * s)
        out.mat(mat, neu)
    return out
