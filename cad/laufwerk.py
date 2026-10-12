"""Laufwerk und Ketten der K 55 E (Original-mm, Z ab Boden).

Aufbau je Seite (Fotobefund fz_01m, fz_09m, FL2, BS, Wiking-Modell, Prospekt):
  - offener Kettenrahmen: breiter Untergurt, hinten geschlossener Kasten, vorn nur
    Innensteg + Obergurt innen, damit das Spannfeder-Rohr von aussen sichtbar ist
  - Leitradgabel vorn (nach vorn offene Gleitfuehrung, Nennlage X_LEIT), Lagerschlitten mit Joch;
    das Leitrad steht in der Ist-Lage leitrad_x() (Kettenschluss, 6,6 mm hinter X_LEIT).
    Die innere Gabelwange traegt bei x 560 das Joch der Querblattfeder (rumpf.py)
  - Spannfeder in einem geschlossenen Rohrgehaeuse (FL2, fz_01m: dickes Rohr zwischen Leitrad und
    Stuetzrollenbock), vorn Federteller + Stellmutter auf der Spannstange, hinten Widerlager (Sackloch); Rohr mit zwei Schellen auf dem Untergurt
  - 6 Laufrollen mit Spurkraenzen in Lagerboecken unter dem Untergurt, Teilung ~205
    (Video 165/167 und Flickr 40431489714: Mitten x ~885 / 1080 / 1290 / 1500 / 1710 / 1910)
  - Stuetzrolle auf einem Bock mit Gabel (Foto BS: im A-Bock-Fenster bei x ~1365)
  - Leitrad mit 5 gekruemmten, breit gegossenen Speichen, grosser Nabe, Laufkranz und Fuehrungsbund
  - Triebrad: 13 Zaehne, geschlossene Scheibe, Nabendeckel mit Schraubenkranz
  - Schwinglager hinten um die Triebradnabe (Anschluss an das Endantriebsgehaeuse)
Kette: Bodenplatte mit einem Greifer an der Hinterkante, gekroepfte Laschen (innen/aussen),
Buchse, Bolzenkoepfe, Klemmleisten mit 2 Muttern je Plattenseite. Die Kettenteilung folgt
aus dem Triebrad (13 Zaehne), die Glieder werden als Polygon um die Raeder gelegt,
der obere Trum haengt zwischen Leitrad, Stuetzrolle und Triebrad leicht durch (36 Glieder).

Lokales Querkoordinatensystem: u = Abstand von der Kettenmitte, positiv nach aussen.
Gebaut wird fuer die rechte Seite (u = +Y), die linke wird gespiegelt.
"""
import math
from functools import lru_cache
from build123d import *
from .common import (SPUR, KETTE_B, Y_KETTE, X_LEIT, Z_LEIT, R_LEIT, X_TRIEB, Z_TRIEB, R_TRIEB,
                     Z_PIN, RAHMEN_Z0, RAHMEN_Z1, box, rad_y, rad_x, ring_x, sechskant, Sammler)

YT = Y_KETTE                     # Alias (rumpf.py importiert SPUR, YT, X_TRIEB, Z_TRIEB)

# ---------------- Kette ----------------
PLATTE_D, GREIFER_H = 22.0, 40.0
HP = 17.0                        # Bolzenmitte ueber Plattenoberseite (Plattenoberseite = Z_PIN)
H_SCHIENE = 28.0                 # Laufflaeche der Laschen ueber Bolzenmitte
N_ZAEHNE = 13
RP_TRIEB = R_TRIEB - HP          # Bolzenkreis am Triebrad
RP_LEIT = R_LEIT - HP            # Bolzenkreis am Leitrad
TEILUNG = 2 * RP_TRIEB * math.sin(math.pi / N_ZAEHNE)   # 2 * 323 * sin(180/13) = 154,6
# Kettenschluss (Radstand X_TRIEB - X_LEIT = 1800, vorher 1870):
#   Bolzenbahn = 2 * 1800 (Trume) + pi * (313 + 323) (Umschlingung je 180 Grad) = 5598 (+1 Durchhang)
#   Sehnen statt Bogen: am Triebrad 6,5 Teilungen = 1005 statt 1015, am Leitrad ~10 weniger -> ~ 5579
#   36 Glieder = 36 * 154,6 = 5566, 37 Glieder = 5720 (141 mm zu lang -> ~150 mm Durchhang, unbrauchbar;
#   oder Leitrad 60 mm weiter vorn -> passt nicht zum Foto)
#   -> 36 Glieder; die ~13 mm zu viel Bahn nimmt die Spannvorrichtung auf: das Leitrad steht in der
#   Gleitfuehrung 6,6 mm hinter seiner Nennlage X_LEIT (beide Trume je 6,6 mm kuerzer), x = 456,6.
#   Genau geloest in leitrad_x() (Bisektion auf die Leitradlage bei festem Durchhang SAG).
N_GLIEDER = 36
SAG = 10.0                       # Durchhang je Feld des oberen Trums (Leitrad-Stuetzrolle-Triebrad)
Z_BOLZEN = Z_PIN + HP            # Bolzen im unteren Trum
Z_SCHIENE = Z_BOLZEN + H_SCHIENE # Laufflaeche unterer Trum
U_I0, U_I1, U_A1 = 57.0, 85.0, 113.0   # Lasche innen u 57..85, aussen 85..113
R_BUCHSE = 15.0
PLATTE_L = TEILUNG - 7.0

# ---------------- Raeder / Rahmen ----------------
R_ROLLE = 90.0                   # Review: bei Teilung ~203 muessen die Spurkraenze (R_ROLLE + 10) freibleiben (vorher R 100 / Kranz 118)
Z_ROLLE = Z_SCHIENE + R_ROLLE
R_LEIT_KRANZ = 273.0             # Laufkranz (Polygoneffekt der Glieder beruecksichtigt)
R_KOPF = 328.0                   # Zahnkopf Triebrad
# Laufrollen (Review 2026-10-12: Video 165/167 + Flickr 40431489714 zeigen SECHS Rollen, Mittenabstand
# 200..215, Mitten x ~885 / 1080 / 1290 / 1500 / 1710 / 1910, +-25; Teilung 203). Erste Rolle: Abstand zum Leitrad
# (Ist-Lage 456,6) ~ 430 > R_LEIT_KRANZ + R_ROLLE = 363. Letzte Rolle: Mitte nur 350 vor der Triebradnabe,
# Abstand sqrt(350^2 + 205^2) = 406 > Zahnkopf 328 + Mittelnut 74 = 402 (Spurkraenze liegen bei u 128+, ausserhalb des Rades).
LAUFROLLEN_X = [885.0, 1088.0, 1291.0, 1494.0, 1697.0, 1900.0]
X_ROLLE0, X_ROLLE1 = LAUFROLLEN_X[0], LAUFROLLEN_X[-1]
# Stuetzrolle: Foto BS zeigt sie im A-Bock-Fenster bei x ~1365, Mitte z ~600
X_STUETZ, R_STUETZ = X_TRIEB - 890.0, 75.0   # 1360
Z_STUETZ_BOLZEN = 717.0          # Bolzenhoehe des oberen Trums ueber der Stuetzrolle
Z0, Z1 = RAHMEN_Z0, RAHMEN_Z1    # Kettenrahmen 327..467
GURT_D = 20.0                    # Untergurt
GURT_B = 175.0                   # Untergurt halbe Breite
KASTEN_B = 115.0                 # Kasten halbe Breite (230)
X_KASTEN0 = X_STUETZ - 90.0      # 1270: Kasten traegt den Stuetzrollenbock
X_KASTEN1 = X_TRIEB - 360.0      # 1890: endet vor dem Triebrad (Zahnkopf x = 1922)
X_GURT0 = X_LEIT + 310.0         # 760: 13 mm hinter dem Leitradbund (R 290, Ist-Lage 456,6)
# Leitradgabel (fest am Rahmen, Nennlage X_LEIT) und Stirnriegel
GABEL_U0, GABEL_U1 = 125.0, 150.0  # Leitradgabel-Wangen
GABEL_X0, GABEL_X1 = X_LEIT - 80.0, X_LEIT + 380.0   # 370..830 (Joch der Querfeder bei x 499..621 liegt auf)
X_RIEGEL = X_LEIT + 375.0        # Stirnriegel-Mitte 825
# Spannfeder im geschlossenen Rohrgehaeuse (Foto FL2, fz_01m: Rohr ~160 dick, zwischen Leitrad und
# Stuetzrollenbock, Stange vorn zum Lagerschlitten, hinten Widerlager an der Kastenstirn)
FEDER_U, FEDER_Z = 30.0, 425.0   # Achse Rohr/Stange
R_ROHR = 75.0
X_ROHR0 = X_LEIT + 460.0         # 910
X_ROHR1 = X_KASTEN0 - 15.0       # 1255 (Foto fz_01m: Rohr reicht bis knapp vor den Kasten/Stuetzrollenbock)
X_WL1 = X_ROHR1 + 35.0           # Widerlager X_ROHR1..X_WL1 (ersetzt die Kastenstirn, 1290)


def _fil(obj, kanten, r):
    """Verrundung, die bei Problemen das Original zurueckgibt."""
    try:
        k = list(kanten)
        if not k:
            return obj
        neu = fillet(k, r)
        return neu if neu.is_valid else obj
    except Exception:
        return obj


def _fas(obj, kanten, r):
    try:
        k = list(kanten)
        if not k:
            return obj
        neu = chamfer(k, r)
        return neu if neu.is_valid else obj
    except Exception:
        return obj


def _xz_poly(pts, u0, u1):
    """Polygon in der XZ-Ebene (x, z), extrudiert von u0 bis u1 (Y)."""
    f = Plane.XZ * Polygon(*pts, align=None)
    return Pos(0, (u0 + u1) / 2, 0) * extrude(f, amount=abs(u1 - u0) / 2, both=True)


# ======================= Kettenbahn =======================
def _fuehrung(xl, sag=SAG, ds=2.0):
    """Leitkurve der Bolzenmitten (Leitrad bei xl): unten vor, um das Leitrad, oberer Trum mit
    Durchhang, um das Triebrad."""
    pts = []
    zb = Z_TRIEB - RP_TRIEB
    n = int((X_TRIEB - xl) / ds)
    pts += [(X_TRIEB - (X_TRIEB - xl) * i / n, zb) for i in range(n)]
    n = int(math.pi * RP_LEIT / ds)
    for i in range(n):
        a = math.radians(270 - 180 * i / n)
        pts.append((xl + RP_LEIT * math.cos(a), Z_LEIT + RP_LEIT * math.sin(a)))

    def feld(x0, z0, x1, z1, d):
        n = int((x1 - x0) / ds)
        for i in range(n):
            t = i / n
            pts.append((x0 + (x1 - x0) * t, z0 + (z1 - z0) * t - 4 * d * t * (1 - t)))
    feld(xl, Z_LEIT + RP_LEIT, X_STUETZ, Z_STUETZ_BOLZEN, sag)
    feld(X_STUETZ, Z_STUETZ_BOLZEN, X_TRIEB, Z_TRIEB + RP_TRIEB, sag)
    n = int(math.pi * RP_TRIEB / ds)
    for i in range(n + 1):
        a = math.radians(90 - 180 * i / n)
        pts.append((X_TRIEB + RP_TRIEB * math.cos(a), Z_TRIEB + RP_TRIEB * math.sin(a)))
    return pts


def _laufen(G, n, p):
    """n Glieder der Teilung p entlang der Leitkurve G abtragen; liefert Bolzenpunkte."""
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


def _rest(xl):
    """Schlussfehler: Abstand letzter -> erster Bolzen minus Teilung (> 0: Bahn zu lang)."""
    pins, ok = _laufen(_fuehrung(xl), N_GLIEDER - 1, TEILUNG)
    return (math.dist(pins[-1], pins[0]) - TEILUNG) if ok else -1e9


@lru_cache(maxsize=1)
def leitrad_x():
    """Ist-Lage des Leitrads in der Gleitfuehrung: Versatz vor X_LEIT, bei dem N_GLIEDER bei festem
    Durchhang SAG genau schliessen (Bahn waechst, wenn das Leitrad nach vorn geht)."""
    lo, hi = X_LEIT - 60.0, X_LEIT + 60.0     # Spannweite der Gleitfuehrung +-60
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
def bolzenpunkte():
    """Bolzenmitten (x, z) der geschlossenen Kette."""
    pins, _ = _laufen(_fuehrung(leitrad_x()), N_GLIEDER - 1, TEILUNG)
    return tuple(pins)


def _glied_lagen():
    """(Mitte x, z, Richtung dx, dz) je Glied."""
    pins = bolzenpunkte()
    out = []
    for i in range(len(pins)):
        a, b = pins[i], pins[(i + 1) % len(pins)]
        L = math.dist(a, b)
        out.append(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (b[0] - a[0]) / L, (b[1] - a[1]) / L))
    return out


# ======================= Kettenglied =======================
def _lasche(vorn, u0, u1):
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


@lru_cache(maxsize=1)
def kettenglied():
    """Ein Glied lokal: x Laufrichtung, z zur Kettenmitte (zu den Raedern), Bolzenlinie z=0,
    Bolzen bei x = +-TEILUNG/2, Plattenoberseite bei z = -HP."""
    p, L = TEILUNG, PLATTE_L
    zp0, zp1 = -HP - PLATTE_D, -HP
    t = []
    platte = box(-L / 2, L / 2, -KETTE_B / 2, KETTE_B / 2, zp0, zp1)
    platte = _fas(platte, platte.edges().filter_by(Axis.Y), 4)
    t.append(platte)
    # Greifer an der Hinterkante (keilfoermig), Enden schraeg
    g = _xz_poly([(-L / 2, zp0 + 1), (-L / 2 + 30, zp0 + 1), (-L / 2 + 20, zp0 - GREIFER_H),
                  (-L / 2 + 4, zp0 - GREIFER_H)], -KETTE_B / 2, KETTE_B / 2)
    for s in (-1, 1):   # Greiferenden abgeschraegt (Draufsicht von vorn)
        cut = Pos(0, s * KETTE_B / 2, zp0) * Rot(s * 45, 0, 0) * Box(2 * L, 40, 40)
        g = g - Pos(0, 0, -GREIFER_H) * cut
    t.append(g)
    for s in (-1, 1):
        # Laschen: hinten innen, vorn aussen (gekroepft)
        for vorn, (a, b) in ((False, (U_I0, U_I1)), (True, (U_I1, U_A1))):
            las = _lasche(vorn, a, b)
            t.append(las if s > 0 else mirror(las, Plane.XZ))
        # Bolzenkopf vorn aussen
        t.append(rad_y(p / 2, s * (U_A1 + 3), 0, 14, 6))
        # Klemmleiste mit 2 Muttern je Plattenseite
        t.append(box(-52, 52, s * (U_A1 - 1), s * 152, -HP, -HP + 10))
        for x in (-32, 32):
            t.append(sechskant((x, s * 134, -HP + 10), (0, 0, 1), 24, 11))
    t.append(rad_y(-p / 2, 0, 0, R_BUCHSE, 2 * U_I0 + 6))          # Buchse
    teil = t[0]
    for x in t[1:]:
        teil = teil + x
    return teil


def kette(seite):
    y = seite * Y_KETTE
    glied = kettenglied()
    out = []
    for x, z, dx, dz in _glied_lagen():
        pl = Plane(origin=(x, y, z), x_dir=(dx, 0, dz), z_dir=(dz, 0, -dx))
        out.append(pl.location * glied)
    return out


# ======================= Raeder (lokal, Achse = Y, Mitte im Ursprung) =======================
def leitrad():
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
    r0, r1 = 110.0, R_LEIT_KRANZ - 24
    sweep = math.radians(27)                  # Schwung der Speichenmitte zwischen Nabe und Kranz
    n = 10
    pm, pl, pr = [], [], []
    for k in range(n + 1):
        f = k / n
        r = r0 + (r1 - r0) * f
        th = sweep * f ** 1.3
        hw = 60 - 22 * f                      # halbe Breite: 60 an der Nabe, 38 am Kranz
        c, sn = math.cos(th), math.sin(th)
        tx, tz = (-sn, c)                     # Quervektor
        pm.append((r * c, r * sn))
        pl.append((r * c + hw * tx, r * sn + hw * tz))
        pr.append((r * c - hw * tx, r * sn - hw * tz))
    kontur = pl + pr[::-1]
    steg = _xz_poly(kontur, -14, 14)
    rippen = None
    for pk, sg in ((pl, 1), (pr, -1)):
        # Randrippe: schmaler Streifen entlang der Kante, nach innen versetzt
        rand = [(p[0] + (q[0] - p[0]) * 0.22, p[1] + (q[1] - p[1]) * 0.22) for p, q in zip(pk, pm)]
        rp = _xz_poly(pk + rand[::-1], -34, 34)
        rippen = rp if rippen is None else rippen + rp
    speiche = steg + rippen
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


def _zahnkranz():
    rp, n = RP_TRIEB, N_ZAEHNE
    with BuildSketch(Plane.XZ) as sk:
        Circle(R_KOPF)
        Circle(RP_TRIEB - 48, mode=Mode.SUBTRACT)
        for k in range(n):
            a = math.radians(-90 + k * 360 / n)
            e, tt = (math.cos(a), math.sin(a)), (-math.sin(a), math.cos(a))

            def P(r, w):
                return (r * e[0] + w * tt[0], r * e[1] + w * tt[1])
            with Locations(P(rp, 0)):
                Circle(R_BUCHSE + 1.5, mode=Mode.SUBTRACT)
            Polygon(P(rp - 6, -(R_BUCHSE + 1.3)), P(rp - 6, R_BUCHSE + 1.3), P(rp + 1, 24), P(rp + 12, 52),
                    P(rp + 30, 60), P(rp + 30, -60), P(rp + 12, -52), P(rp + 1, -24),
                    align=None, mode=Mode.SUBTRACT)
    z = extrude(sk.sketch, amount=30, both=True)
    # Zahnkoepfe seitlich angefast
    return _fas(z, z.edges().filter_by(Axis.Y, reverse=True).filter_by_position(Axis.Y, 29, 31)
                + z.edges().filter_by(Axis.Y, reverse=True).filter_by_position(Axis.Y, -31, -29), 3)


def triebrad():
    t = Sammler("lack")
    t.append(_zahnkranz())
    scheibe = rad_y(0, 0, 0, RP_TRIEB - 40, 30)                             # geschlossene Scheibe
    for i in range(N_ZAEHNE):                                                 # Zahnkranzschrauben
        w = math.radians(i * 360 / N_ZAEHNE + 180 / N_ZAEHNE - 90)
        t.mat("blank", sechskant((262 * math.cos(w), 30, 262 * math.sin(w)), (0, 1, 0), 18, 8))
    t.append(scheibe)
    t.append(rad_y(0, 0, 0, RP_TRIEB - 46, 44) - rad_y(0, 0, 0, RP_TRIEB - 70, 50))   # Randwulst
    # Nabenflansch aussen mit Schraubenkranz
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
    # Rippen auf der Innenseite der Scheibe
    for i in range(N_ZAEHNE):
        rp = Rot(0, i * 360 / N_ZAEHNE, 0) * box(120, RP_TRIEB - 60, -40, -15, -9, 9)
        t.append(rp)
    # Nabe innen bis zum Endantriebsgehaeuse (u = -210)
    t.append(rad_y(0, -107.5, 0, 120, 185))
    t.append(rad_y(0, -204, 0, 155, 12))
    return t


def laufrolle():
    """Doppelte Laufbahn auf den Laschen, Spurkraenze aussen, Lagerboecke mit Achsdeckeln."""
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
    # Lagerboecke
    hz = Z0 - zr
    for s in (-1, 1):
        ua, ub = sorted((s * 142, s * 162))
        wange = _xz_poly([(-56, -10), (56, -10), (72, hz - 12), (-72, hz - 12)], ua, ub)
        wange = wange + Pos(0, s * 152, 0) * Rot(90, 0, 0) * Cylinder(56, 20)
        wange = wange + _xz_poly([(-9, 48), (9, 48), (9, hz - 12), (-9, hz - 12)], *sorted((s * 160, s * 172)))
        t.append(wange)
        fuss = box(-78, 78, s * 136, s * 182, hz - 12, hz)
        t.append(_fas(fuss, fuss.edges().filter_by(Axis.Y).group_by(Axis.Z)[0], 4))
        for x in (-60, 60):
            t.mat("blank", sechskant((x, s * 172, hz - 12), (0, 0, -1), 20, 9))
        t.append(rad_y(0, s * 166, 0, 42, 8))                                 # Achsdeckel
        for x in (-25, 25):
            t.mat("blank", sechskant((x, s * 170, 0), (0, s, 0), 16, 7))
    return t, zr


def stuetzrolle(zc):
    """Stuetzrolle mit Gabelbock auf dem Kasten; zc = Rollenmitte."""
    t = Sammler("lack")
    rolle = rad_y(0, 0, 0, R_STUETZ, 236) - rad_y(0, 0, 0, R_STUETZ + 5, 2 * (U_I0 - 6))
    rolle = rolle + rad_y(0, 0, 0, R_STUETZ - 14, 2 * U_I0)
    t.append(_fas(rolle, rolle.edges().filter_by(GeomType.CIRCLE).group_by(SortBy.RADIUS)[-1], 4))
    t.mat("blank", rad_y(0, 0, 0, 25, 2 * 152))
    oben = 40.0
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
    saeule = box(-35, 35, -70, 70, Z1 - zc, zkopf0)
    t.append(saeule)
    for s in (-1, 1):                                                         # Knotenbleche
        t.append(_xz_poly([(35, Z1 - zc), (75, Z1 - zc), (35, zkopf0)], -8, 8) if s > 0 else
                 _xz_poly([(-35, Z1 - zc), (-35, zkopf0), (-75, Z1 - zc)], -8, 8))
    return t


# ======================= Kettenrahmen =======================
def _stuetz_z():
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


def _rahmen_rechts():
    """Kettenrahmen rechte Seite, Kettenmitte bei y=0, u = +Y nach aussen."""
    t = Sammler("lack")
    # --- Untergurt (breit, traegt die Lagerboecke) ---
    gurt = box(X_GURT0, X_KASTEN1, -GURT_B, GURT_B, Z0, Z0 + GURT_D)
    t.append(_fil(gurt, gurt.edges().filter_by(Axis.Z), 20))
    # Verlaengerung nur aussen (u 100..175), damit der Lagerbock der sechsten Laufrolle (x 1885 +-78) aufliegt;
    # weiter innen steht das Triebrad (Zahnkopf x = 1922)
    ext = box(X_KASTEN1 - 20, LAUFROLLEN_X[-1] + 95.0, 100.0, GURT_B, Z0, Z0 + GURT_D)
    t.append(_fil(ext, ext.edges().filter_by(Axis.Z).group_by(Axis.X)[-1], 15))
    # --- Kasten hinten ---
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
    # Kasten innen: Deckel + Rippen
    t.append(box(X_KASTEN0 + 60, X_KASTEN1 - 60, -KASTEN_B - 6, -KASTEN_B + 1, Z0 + 40, Z1 - 30))
    # --- vorderer, offener Teil: Innensteg + innerer Obergurt + Rippen ---
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
    # --- Stirnriegel hinter dem Leitrad (oben/unten, Joch und Spannstange laufen dazwischen) ---
    t.append(box(X_RIEGEL - 10, X_RIEGEL + 10, -GABEL_U1, GABEL_U1, Z0, Z0 + 23))
    t.append(box(X_RIEGEL - 10, X_RIEGEL + 10, -GABEL_U1, GABEL_U1, Z1 - 17, Z1 + 3))
    # --- Leitradgabel: nach vorn offene Gleitfuehrung (Ober- und Unterschiene je Seite) ---
    # Oberkante der inneren Wange (u -150..-125, z = Z1 + 3) traegt bei x 499..621 das Joch der Querfeder
    zs0, zs1 = Z_LEIT - 43, Z_LEIT + 43        # Schlitz
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
    # --- Lagerschlitten (in der Gabel, Ist-Lage des Leitrads) mit Joch hinter dem Leitrad ---
    xl = leitrad_x()
    for s in (-1, 1):
        u0, u1 = (127, 148) if s > 0 else (-148, -127)
        t.append(box(xl - 60, xl + 345, u0, u1, zs0 + 3, zs1 - 3))
        t.append(rad_y(xl, s * 156, Z_LEIT, 32, 16))                          # Lagerdeckel
        t.mat("blank", sechskant((xl, s * 164, Z_LEIT), (0, s, 0), 30, 12))
    xj = xl + 310.0                                                           # Joch 20 hinter dem Leitradbund
    joch = box(xj, xj + 40, -127, 127, zs0 + 8, zs1 - 8)
    t.append(_fas(joch, joch.edges().filter_by(Axis.Y), 6))
    t.append(rad_x(xj + 52, FEDER_U, FEDER_Z, 22, 24))                       # Stangenkopf (zwischen den Riegeln)
    # --- Spannfeder im geschlossenen Rohrgehaeuse (Feder selbst unsichtbar) ---
    # Stange vom Stangenkopf durch Federteller und Rohr bis hinter das Widerlager
    x_st1 = X_ROHR1 + 15                                                      # endet im Sackloch des Widerlagers
    t.mat("blank", rad_x((xj + 64 + x_st1) / 2, FEDER_U, FEDER_Z, 20, x_st1 - xj - 64))
    tel = rad_x(X_ROHR0 - 9, FEDER_U, FEDER_Z, 62, 24)                        # vorderer Federteller (sichtbar)
    t.append(_fas(tel, tel.edges(), 4))
    t.mat("blank", Pos(X_ROHR0 - 21 - 20, FEDER_U, FEDER_Z) * Rot(0, 90, 0)
          * extrude(RegularPolygon(30, 6), amount=20))                       # Stellmutter vor dem Teller
    rohr_ = rad_x((X_ROHR0 + X_ROHR1 + 3) / 2, FEDER_U, FEDER_Z, R_ROHR, X_ROHR1 + 3 - X_ROHR0)
    t.append(_fas(rohr_, rohr_.edges(), 6))
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
    wl = box(X_ROHR1, X_WL1, -KASTEN_B, KASTEN_B, Z0 + GURT_D - 1, FEDER_Z + R_ROHR + 5)         - rad_x(X_ROHR1 + 10, FEDER_U, FEDER_Z, 22, 22)
    wl = _fil(wl, wl.edges().filter_by(Axis.X).group_by(Axis.Z)[-1], 15)
    t.append(wl)
    # --- Schwinglager hinten um die Triebradnabe (Endantrieb) ---
    arm = box(X_KASTEN1 - 40, X_TRIEB, -195, -60, Z_TRIEB - 60, Z_TRIEB + 60) + rad_y(X_TRIEB, -160, Z_TRIEB, 205, 70)
    arm = arm - rad_y(X_TRIEB, -125, Z_TRIEB, 126, 170)
    t.append(arm)
    for i in range(4):
        a = math.radians(45 + 90 * i)
        t.mat("blank", sechskant((X_TRIEB + 182 * math.cos(a), -195, Z_TRIEB + 182 * math.sin(a)), (0, -1, 0), 24, 11))
    # --- Laufrollen ---
    rolle, zr = laufrolle()
    for x in LAUFROLLEN_X:
        for mat, lst in rolle.schichten().items():
            t.mat(_rad_mat(mat), [Pos(x, 0, zr) * s for s in lst])
    # --- Stuetzrolle ---
    zc = _stuetz_z()
    st = stuetzrolle(zc)
    for mat, lst in st.schichten().items():
        t.mat(_rad_mat(mat), [Pos(X_STUETZ, 0, zc) * s for s in lst])
    # --- Leitrad und Triebrad ---
    for rad, (x, z) in ((leitrad(), (xl, Z_LEIT)), (triebrad(), (X_TRIEB, Z_TRIEB))):
        for mat, lst in rad.schichten().items():
            t.mat(_rad_mat(mat), [Pos(x, 0, z) * s for s in lst])
    return t


def _rad_mat(mat):
    """Laufraeder (Leitrad, Triebrad, Lauf- und Stuetzrollen) bekommen ein eigenes Material: ab Werk
    waren die Raeder rot abgesetzt (Hanomag ab 1953: Aufbau gruen bzw. blau, Raeder rot)."""
    return "raeder" if mat == "lack" else mat


def kettenrahmen(seite):
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
