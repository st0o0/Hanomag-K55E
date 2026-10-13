"""Kollisions- und Filigranpruefung aller Teile.

  python tools/kollision.py [teil_id ...]

Ausgabe: stdout und out/kollision.md. Koordinaten in Original-mm.
"""
from __future__ import annotations

import sys
import time
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build123d import Compound  # noqa: E402

from cad.modell import INFO, TEILE  # noqa: E402

TOL = 0.05          # bbox-Toleranz (Modell-mm)
V_MIN = 0.5         # Durchdringung ab diesem Volumen (Modell-mm3)
V_KLEIN = 0.05
KANTE_MIN = 0.4
S = INFO["massstab"]
BZ = INFO["boden_z"]


def orig(c) -> tuple[float, float, float]:
    """Modell-mm-Punkt -> Original-mm (x, y, z ab Boden)."""
    return (c.X * S, c.Y * S, (c.Z - BZ) * S)


def bb_hit(a, b, tol: float = TOL) -> bool:
    """Ueberlappen sich zwei Huellquader (mit Toleranz)?"""
    return (a.min.X - tol <= b.max.X and b.min.X - tol <= a.max.X and
            a.min.Y - tol <= b.max.Y and b.min.Y - tol <= a.max.Y and
            a.min.Z - tol <= b.max.Z and b.min.Z - tol <= a.max.Z)


def main() -> None:
    """Alle (oder die genannten) Teile bauen, paarweise schneiden, Bericht schreiben."""
    nur = set(sys.argv[1:])
    t0 = time.time()
    teile = []
    for t in TEILE:
        if nur and t.id not in nur:
            continue
        ts = time.time()
        d = t.bauen()
        solids = []
        for mat, comp in d.items():
            for s in comp.solids():
                solids.append((mat, s, s.bounding_box()))
        allc = Compound(children=[s for _, s, _ in solids])
        teile.append((t.id, solids, allc.bounding_box()))
        print(f"gebaut {t.id}: {len(solids)} Solids, {time.time()-ts:.1f}s", file=sys.stderr, flush=True)
    t_bau = time.time() - t0

    t1 = time.time()
    paare, fehler = [], []
    for (ia, sa, ba), (ib, sb, bb) in combinations(teile, 2):
        if not bb_hit(ba, bb):
            continue
        tp = time.time()
        vol, hits, n_pruef = 0.0, [], 0
        for ma, a, bba in sa:
            for mb, b, bbb in sb:
                if not bb_hit(bba, bbb):
                    continue
                n_pruef += 1
                try:
                    r = a.intersect(b)
                    if r is None:
                        continue
                    r = Compound(children=list(r)) if isinstance(r, (list, tuple)) else r
                    v = r.volume if len(r.solids()) else 0.0
                except Exception as e:
                    fehler.append((ia, ib, f"{type(e).__name__}: {e}"))
                    continue
                if v > V_MIN:
                    vol += v
                    c = r.bounding_box().center()
                    hits.append((v, ma, mb, orig(c)))
        print(f"paar {ia}/{ib}: {n_pruef} Booleans, {vol:.2f} mm3, {time.time()-tp:.1f}s", file=sys.stderr, flush=True)
        if hits:
            hits.sort(key=lambda h: -h[0])
            paare.append((ia, ib, vol, hits))
    t_koll = time.time() - t1

    klein = []
    for tid, solids, _ in teile:
        for mat, s, bx in solids:
            v = s.volume
            kante = min(bx.size.X, bx.size.Y, bx.size.Z)
            if v < V_KLEIN or kante < KANTE_MIN:
                klein.append((tid, mat, v, kante, orig(bx.center())))

    L = ["# Kollisionspruefung", "",
         f"Laufzeit: Bauen {t_bau:.0f} s, Kollision {t_koll:.0f} s. "
         f"Schwelle Durchdringung > {V_MIN} mm3 (Modell), bbox-Toleranz {TOL} mm. "
         "Koordinaten: Original-mm (x ab Maskenfront, y rechts, z ab Boden).", "",
         "## Durchdringungen", ""]
    if paare:
        L += ["| Teil A | Teil B | Schnittvolumen Modell-mm3 | Solidpaare |", "|---|---|---:|---:|"]
        for ia, ib, vol, hits in sorted(paare, key=lambda p: -p[2]):
            L.append(f"| {ia} | {ib} | {vol:.2f} | {len(hits)} |")
        for ia, ib, _vol, hits in sorted(paare, key=lambda p: -p[2]):
            L += ["", f"### {ia} / {ib}", "",
                  "| Volumen | Material A | Material B | Mitte x, y, z (Orig.-mm) |", "|---:|---|---|---|"]
            for v, ma, mb, c in hits[:5]:
                L.append(f"| {v:.2f} | {ma} | {mb} | {c[0]:.0f}, {c[1]:.0f}, {c[2]:.0f} |")
    else:
        L.append("Keine Durchdringungen.")
    L += ["", "## Fehler bei intersect", ""]
    if fehler:
        from collections import Counter
        L += [f"- {a} / {b}: {e} (x{n})" for (a, b, e), n in Counter(fehler).items()]
    else:
        L.append("Keine.")
    L += ["", f"## Zu filigrane Solids (Volumen < {V_KLEIN} mm3 oder Kante < {KANTE_MIN} mm)", ""]
    if klein:
        L += ["| Teil | Material | Volumen | kleinste Kante | Mitte (Orig.-mm) |", "|---|---|---:|---:|---|"]
        for tid, mat, v, k, c in klein:
            L.append(f"| {tid} | {mat} | {v:.4f} | {k:.3f} | {c[0]:.0f}, {c[1]:.0f}, {c[2]:.0f} |")
    else:
        L.append("Keine.")
    txt = "\n".join(L) + "\n"
    (ROOT / "out").mkdir(exist_ok=True)
    (ROOT / "out" / "kollision.md").write_text(txt, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(txt)


main()
