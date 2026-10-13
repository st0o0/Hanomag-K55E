"""Gemeinsame Masse von Planiertraverse (Endkaesten, Oeltank) und Hubzylindern.

Die Masse werden von ``planierschild`` (Bauteile) und ``hydraulik`` (Leitungen, die durch Endkasten-Waende
zu den Zylindern fuehren) benutzt und liegen deshalb in einem eigenen Modul, damit beide ohne Zirkularimport darauf
zugreifen koennen. Original-mm, X von der Maskenfront nach hinten, Y nach rechts, Z ab Boden.
"""
from __future__ import annotations

from .common import DECK_Z, TRAVERSE_X, TRAVERSE_Z, Y_SCHUB

# ---------------- Hubzylinder ----------------
# Mittelzapfen im Endkasten der Traverse (Foto BS: Deckel am Endkasten bei x ~ 2520), Achshoehe TRAVERSE_Z.
X_ZAPFEN, Z_ZYL = TRAVERSE_X, TRAVERSE_Z
R_ZYL, R_STANGE = 50.0, 24.0   # Rohr Ø 100, Stange Ø 48 (Foto 40431489714)
X_KOPF = 1770.0                # Zylinderkopf-Flansch (Vorderseite)
X_BODEN = 2640.0               # Zylinderboden-Flansch, im Endkasten vor dem Langloch der Schraege
R_KOPF = 60.0                  # runder Zylinderkopf ~ 1,2 x Rohr-Ø (Video 079..088)
Z_ZYL_U = Z_ZYL - 125.0        # unteres Zylinderrohr laeuft tief unter dem Zylinder (Video 087)
GABEL_L = 124.0                # Gabelkopf ab Scheitelauge bis Kontermutter

# ---------------- Traverse: Endkaesten aussen, Quertraeger = Oeltank hinten oben ----------------
EK_X0, EK_X1 = 2395.0, 2830.0
EK_Z0, EK_Z1 = DECK_Z + 12.0, 1170.0   # 243 hoch (Seitenfotos 240..290), steht auf der Konsole ueber der Plattform
Z_AUSS_O = EK_Z1 - 18.0        # Oberkante des Kastenausschnitts (Rest oben 18 mm, Verrundung 14)
Z_AUSS = 995.0                 # Unterkante des Kastenausschnitts (Zylinder + untere Leitung)
EK_SCHR_DX, EK_SCHR_DY = 120.0, 190.0   # abgeschraegte hintere Aussenecke, ganze Kastenhoehe (c_ende_l)
LL_L, LL_H = 200.0, 110.0      # Langloch in der Schraegflaeche beider Endkaesten
Y_FRISCH = 0.0                 # Schild "Frisch" mittig in der Rueckwand
EK_DY, EK_T = 95.0, 12.0       # halbe Breite (y), Wandstaerke
EK_YI = Y_SCHUB - EK_DY        # Innenseite des Endkastens zur Fahrzeugmitte hin (880)
QT_X0, QT_X1 = 2530.0, EK_X1   # Oeltank 300 tief, Vorderwand direkt hinter dem Sitz (Nordhorn 2:09), Rueckwand buendig
QT_Z0, QT_Z1 = EK_Z0, EK_Z1    # so hoch wie die Endkaesten (zoom_heck_l)
