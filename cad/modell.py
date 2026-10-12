"""Baugruppen-Register der Hanomag K 55 E (1:8).

Jedes Teil liefert {material: Compound} im Modellsystem (mm, 1:8,
x=0 Maskenfront, z=0 Maskenunterkante). tools/build.py schreibt daraus
je Material eine Ansicht-STL (Farbe in der App) und je Teil eine Druck-STL.
"""
from dataclasses import dataclass
from typing import Callable
from build123d import Compound, Plane, mirror

from . import haube as h
from . import laufwerk, rumpf, motor, fahrerstand, planierschild
from .common import zu_modell, MASSSTAB, BODEN_Z_MODELL

# Farbpalette (App und Renderer). Lack, Motor und Anbau sind in der App umschaltbar.
MATERIALIEN = {
    "lack":        {"name": "Lack",               "farbe": "#a8262b", "rauheit": 0.55, "metall": 0.15},
    "motor":       {"name": "Motorlack",          "farbe": "#8a2024", "rauheit": 0.6,  "metall": 0.2},
    "anbau":       {"name": "Planiereinrichtung", "farbe": "#a8262b", "rauheit": 0.55, "metall": 0.15},
    "stahl":       {"name": "Kettenstahl",        "farbe": "#3b3d3f", "rauheit": 0.5,  "metall": 0.6},
    "blank":       {"name": "Blanker Stahl",      "farbe": "#9ca1a5", "rauheit": 0.3,  "metall": 0.85},
    "chrom":       {"name": "Chrom",              "farbe": "#e1e5e8", "rauheit": 0.12, "metall": 1.0},
    "zink":        {"name": "Verzinkt",           "farbe": "#a9b0b5", "rauheit": 0.35, "metall": 0.7},
    "schwarz":     {"name": "Schwarz",            "farbe": "#1c1c1c", "rauheit": 0.45, "metall": 0.3},
    "gummi":       {"name": "Gummi",              "farbe": "#121212", "rauheit": 0.95, "metall": 0.0},
    "leder":       {"name": "Sitzpolster",        "farbe": "#171717", "rauheit": 0.35, "metall": 0.05},
    "glas":        {"name": "Glas",               "farbe": "#d9e8f0", "rauheit": 0.05, "metall": 0.1, "deckkraft": 0.35},
    "ruecklicht":  {"name": "Rücklicht",          "farbe": "#c0121c", "rauheit": 0.2,  "metall": 0.0, "leuchten": 0.35},
    "zifferblatt": {"name": "Zifferblatt",        "farbe": "#efeadb", "rauheit": 0.6,  "metall": 0.0},
    "bosch":       {"name": "Bosch-Blau",         "farbe": "#2f6e86", "rauheit": 0.5,  "metall": 0.3},
    "auspuff":     {"name": "Auspuff, rostig",    "farbe": "#5b3b2b", "rauheit": 0.9,  "metall": 0.4},
}


@dataclass
class Teil:
    id: str
    name: str
    gruppe: str
    material: str                     # Hauptmaterial (Farbpunkt in der Liste)
    bauen: Callable[[], dict]         # -> {material: Compound}
    explode: tuple = (0.0, 0.0, 0.0)  # Modell-mm beim Auseinanderziehen
    hinweis: str = ""
    druck: bool = True
    druck_rot: tuple = (0.0, 0.0, 0.0)  # Drehung (Grad um x, y, z) fuer die Drucklage, siehe tools/druck.py


def _d(**schichten):
    return {k: (v if isinstance(v, Compound) else Compound(children=list(v))) for k, v in schichten.items()}


_km_cache = {}


def _km():
    if not _km_cache:
        _km_cache["km"], _km_cache["g"] = h.kuehlermaske()
    return _km_cache["km"], _km_cache["g"]


def _sw(seite):
    sw = h.scheinwerfer(-1)
    if seite > 0:
        sw = {k: [mirror(s, about=Plane.XZ) for s in v] for k, v in sw.items()}
    return _d(**sw)


TEILE = [
    Teil("haube", "Motorhaube", "Haube & Maske", "lack", lambda: _d(lack=[h.haube()]), (0, 0, 45),
         "Dach mit Längssicken, Seitenwände mit großem Motorausschnitt, Schriftband HANOMAG, Typfeld K55E, Nieten. Druck stehend auf der Hinterkante.",
         druck_rot=(0.0, 90.0, 0.0)),
    Teil("kuehlermaske", "Kühlermaske", "Haube & Maske", "lack",
         lambda: _d(lack=[_km()[0]], chrom=h.maske_zier()), (-40, 0, 0),
         "Maske wie R 45: Flügellogo, drei senkrechte Grillstäbe, Kühlerverschluss auf der Kappe, Kurbelloch."),
    Teil("gitter", "Grillgitter", "Haube & Maske", "schwarz", lambda: _d(schwarz=[h.gitter(*_km()[1])]), (-22, 0, 0),
         "Einsatz hinter dem Grill, 2 mm Maschen. Für FDM besser Messinggaze verwenden."),
    Teil("scheinwerfer_links", "Scheinwerfer links", "Haube & Maske", "schwarz", lambda: _sw(-1), (-10, -30, 0),
         "Gehäuse mit Halter, Chromring, Glas."),
    Teil("scheinwerfer_rechts", "Scheinwerfer rechts", "Haube & Maske", "schwarz", lambda: _sw(1), (-10, 30, 0),
         "Gehäuse mit Halter, Chromring, Glas."),
    Teil("motor", "Motor D57 & Kühler", "Antrieb", "motor", lambda: zu_modell(motor.motor()), (0, 0, 0),
         "4-Zylinder-Diesel 5,7 l: Einspritzpumpe mit Leitungen, Kraftstofffilter mit Glasglocken, Lichtmaschine, "
         "Bosch-Anlasser, Riementrieb, Kühler mit Lüfter und Schläuchen."),
    Teil("auspuff", "Auspuff & Luftfilter", "Antrieb", "auspuff", lambda: zu_modell(motor.auspuff()), (0, 0, 60),
         "Krümmer, Auspuffrohr mit Regenklappe, Ölbadluftfilter mit Arbeitsleuchte."),
    Teil("rumpf", "Rahmen & Getriebe", "Fahrgestell", "lack", lambda: zu_modell(rumpf.rumpf()), (0, 0, -10),
         "Längsträger, Querblattfeder, Getriebe, Endantriebe, Lenkbremsen, Plattform mit Riffelblech und gerollter Kante, Zugpendel."),
    Teil("laufwerk_links", "Laufwerk links", "Fahrgestell", "lack", lambda: zu_modell(laufwerk.kettenrahmen(-1)), (0, -45, 0),
         "Kettenrahmen, Leitrad, Triebrad, 5 Laufrollen, Stützrolle, Spannfeder im Rohrgehäuse."),
    Teil("laufwerk_rechts", "Laufwerk rechts", "Fahrgestell", "lack", lambda: zu_modell(laufwerk.kettenrahmen(1)), (0, 45, 0),
         "Kettenrahmen, Leitrad, Triebrad, 5 Laufrollen, Stützrolle, Spannfeder im Rohrgehäuse."),
    Teil("kette_links", "Kette links", "Fahrgestell", "stahl", lambda: zu_modell(laufwerk.kette(-1), "stahl"), (0, -75, 0),
         "36 Bodenplatten 400 mm mit Greifer, Kettenglieder, Bolzen."),
    Teil("kette_rechts", "Kette rechts", "Fahrgestell", "stahl", lambda: zu_modell(laufwerk.kette(1), "stahl"), (0, 75, 0),
         "36 Bodenplatten 400 mm mit Greifer, Kettenglieder, Bolzen."),
    Teil("tank", "Kraftstofftank", "Fahrerstand", "zink", lambda: zu_modell(fahrerstand.tank()), (0, 0, 35),
         "Verzinkter, gewölbter Tank mit Spannbändern, Flügelmutter-Deckel, Kanne und Kraftstoffhahn."),
    Teil("fahrerstand", "Fahrerstand", "Fahrerstand", "lack", lambda: zu_modell(fahrerstand.fahrerstand()), (20, 0, 20),
         "Armaturenkonsole mit ovaler Instrumententafel, Lenkrad, Pedale, Hebel, einteilige Sitzschale auf Blattfeder, Werkzeugkästen, Batteriekasten, Rücklicht."),
    Teil("planierschild", "Planierschild FRISCH 55 FH2", "Planiereinrichtung", "anbau",
         lambda: zu_modell(planierschild.planierschild(), "anbau"), (-70, 0, 0),
         "Schild 2400 mm mit Bohrungsreihe, Schubbalken, A-Böcke, zwei Hubzylinder in den Endkästen der Traverse, Öltank, Schutzbügel, Pumpe vor der Maske mit Leitungen, Steuerschieber."),
]

INFO = {
    "id": "hanomag-k55e",
    "name": "Hanomag K 55 E",
    "untertitel": "Planierraupe mit FRISCH-Planiereinrichtung 55 FH2",
    "massstab": MASSSTAB,
    "boden_z": BODEN_Z_MODELL,
    "original": {"laenge": 2880, "breite": 1800, "hoehe": 1840, "spur": 1270, "kette": 400,
                 "gewicht": 4640, "motor": "Hanomag D57, 4 Zyl., 5702 cm³, 55 PS bei 1300/min",
                 "baujahre": "1950–1956"},
    "genauigkeit": "Maße aus Fotos und Prospekt abgeleitet, ca. ±5 %. Haube und Maske wie K 55.",
    "materialien": MATERIALIEN,
}
