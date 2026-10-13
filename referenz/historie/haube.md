# Historie cad/haube.py

Umbau-Notizen, die beim Refactoring aus dem Modul-Docstring und den Parameterkommentaren entfernt wurden
(Stand 2026-10-13). Die Geometrie ist unveraendert; hier steht nur, was frueher anders war.

## Maske und Kuehlerfenster
- Ein frueherer Kommentar beschrieb ein Grillfenster mit breitem Querband oben, breitem Abschlusswulst unten,
  3 flachen Querbaendern (je zwei Wulste) und schmalem Mittelsteg. Das gilt nicht mehr; heute: durchgehendes
  Fenster mit drei senkrechten Staeben (siehe Modul-Docstring).
- Maske x 0..210, z 450..1410, h/b 1,35: Review 2026-10-12 (Video 165/167, Flickr, DSC04737).
- Kuehlerverschluss: gehoert zur Maske, nicht zur Haube (Beleg BS, x ~100..180).

## Haube und Motorausschnitt
- Schriftband: heute 1090..1410, Bogenfuss z 890 (Review 2026-10-12/13). Die Oberkante des Motorausschnitts
  (HAUBE_BAND_Z) lag frueher bei 1125.
- "K55": Mitte x ~300, z 960..1000, Versalhoehe ~40 (Review 2026-10-12). Das E im Typschild entfiel nach den
  Fotos DSC04729/42; der Rahmen (TYP_RAHMEN) und das Typfeld (TYP_FELD_B, PRAEGE_H) sind entfallen, uebrig
  blieb TYP_FELD_H als Platzhalterhoehe fuer die Nietreihe.
- Seitenblech unter dem Motorausschnitt (Review 2026-10-13, Nordhorn-Video 2:44 s164, mit
  Bildneigungs-Korrektur und Ausrichtung an 6 Laufrollen + Triebradnabe, Video 2:53/2:58): Oberkante bei
  z ~805..810, Unterkante 695. Vorher stand das Blech bei z 805..895 und liess ~70..90 mm offen.
- Scheinwerfer-Position SCHEINWERFER: Review 2026-10-12 (Video 165/172/196, Flickr 40431489714).

## Entfernte, ungenutzte Namen
Im Refactoring geloescht, weil nirgends in cad/ oder tools/ verwendet: `plane_front`, `stab_x`, `stab_y`,
`stab_z`, `wulst_pfad`, Konstanten `PRAEGE_H`, `TYP_FELD_B`, `TYP_RAHMEN`.
`SCHRIFT_FONT` entfiel zugunsten von `common.FONT` (gleicher Pfad).
