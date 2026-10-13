# Codestil und Aufbau

Gilt für `cad/` und `tools/`. Prüfen mit `.venv/Scripts/python.exe -m ruff check cad tools` (Konfiguration in `pyproject.toml`).

## Grundregeln

- PEP 8 über ruff, Zeilenlänge 130. Jede Datei beginnt mit `from __future__ import annotations`.
- **Keine Stern-Importe.** `from build123d import Box, Cylinder, Pos, ...` und `from .common import ...` werden explizit geschrieben.
- **Typ-Hinweise** an allen Funktionen (`def kotfluegel(t: Sammler) -> None:`). Geometrie-Rückgaben werden als `Solid`, `Compound` oder `Part` annotiert.
- Die Namen bleiben deutsch wie bisher (Fachsprache des Modells). Konstanten schreiben wir `GROSS_MIT_UNTERSTRICH`, Funktionen und Variablen `klein_mit_unterstrich`.

## Aufbau eines Baugruppenmoduls

1. **Modul-Docstring:** WAS die Baugruppe ist, wie sie technisch funktioniert und welche Belege es gibt (Fotos, Video und Zeitstempel). Keine Umbau-Historie; die steht in `referenz/historie/<modul>.md`.
2. **Importe.**
3. **Parameterblock:** Konstanten nach Bauteil gruppiert, mit einer Kopfzeile pro Gruppe (`# --- Endkasten ---`). Jede Konstante bekommt einen kurzen Kommentar mit Einheit (Original-mm) und Beleg. Abgeleitete Werte werden berechnet, nicht als Zahl abgeschrieben.
4. **Private Helfer** (`_name`), danach die **öffentlichen Bauteilfunktionen** `teil(t: Sammler) -> None` und am Ende die **Fassade** der Baugruppe, die `modell.py` aufruft.
5. **Funktionen kurz halten:** Eine Funktion baut ein Bauteil. Wiederholte Muster wie Schraubenreihen, Rohrzüge oder Bleche mit Kantung gehören in Helfer.

## Schnittstellen

- Maße zwischen Baugruppen stehen nur in `cad/common.py` (HAUPTMASSE) bzw. `cad/planiermasse.py` (Planiereinrichtung). Ein Modul importiert keine Konstanten aus einem *anderen* Baugruppenmodul. Ausnahme bis zur Bereinigung: Was heute so importiert wird, wird im Bericht aufgelistet und nach `common.py` verschoben, wenn mehrere Module es brauchen.
- Allgemeine Geometrie-Helfer (`box`, `stab`, `sechskant`, `rad_x`, …) liegen nur in `common.py`. Lokale Kopien, die dasselbe tun, werden gelöscht.
- Leitungen und Rohre werden mit `hydraulik.Rohrzug` gebaut (Stützpunkte plus Biegeradius), nicht mit handgebauten Bogenketten.

## Koordinaten

Original-mm: X von der Maskenfront nach hinten, Y nach rechts, Z ab Boden. Ausnahme ist `haube.py` (Modell-mm, über `m()`/`_z()`). `zu_modell()` rechnet ins Modellsystem um.

## Refactoring-Regel

Ein Refactoring ändert keine Geometrie. Vorher und nachher wird geprüft:
`tools/vorschau.py <teile> --out out/<x>` und dann `tools/snapshot.py diff out/snapshot_r13.json --quelle out/<x>` muss „keine Abweichungen“ melden.
Gewollte Geometrieänderungen sind ein eigener Schritt.
