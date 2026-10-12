# Hanomag K 55 E – Modell 1:8

Parametrisches CAD-Modell der Planierraupe **Hanomag K 55 E** mit FRISCH-Planiereinrichtung 55 FH2
im Maßstab 1:8, dazu die **Modellwerkstatt**: eine Web-App zum Ansehen, Messen und Herunterladen der Druckdateien.

**Online:** https://st0o0.github.io/Hanomag-K55E/

## Web-App (`docs/`)

- Modell von allen Seiten ansehen, Teile ein- und ausblenden, auseinanderziehen
- **Messen:** zwei Punkte antippen, rastet an Ecken ein. Messart direkt oder nur Länge X, Breite Y, Höhe Z (Tasten 1–4).
  Darstellung wie im CAD mit Hilfslinien, Pfeilen und Maßlinie im Abstand zum Objekt. Beschriftung ziehen verschiebt die Maßlinie,
  Endpunkte einer gewählten Messung lassen sich auf dem Modell verschieben, Name und Messart sind in der Liste änderbar.
  Messungen bleiben im Browser gespeichert.
- **Schnitt** längs, quer oder in der Höhe
- Teil anklicken: Außenmaße und Druckdatei
- STL-Download je Teil, STEP des Gesamtmodells
- **Quellen:** alle Referenzfotos, Prospekte und Daten mit Link und Verwendungszweck (gepflegt in `referenz/quellen.json`, `tools/build.py` übernimmt sie)

Lokal starten:

```sh
python -m http.server 8765 -d docs
# http://127.0.0.1:8765
```

Auf GitHub Pages: *Settings → Pages → Build and deployment → Deploy from a branch → `main`, Ordner `/docs`*.

## Struktur

```
cad/            CAD-Quellen (build123d), Maße in Original-mm
  common.py       Maßstab, Helfer
  haube.py        Motorhaube, Kühlermaske, Gitter, Scheinwerfer
  laufwerk.py     Kettenrahmen, Leitrad, Triebrad, Rollen, Ketten
  rumpf.py        Rahmen, Querblattfeder, Getriebe, Plattform
  motor.py        Motor D57, Kühler, Auspuff, Luftfilter
  fahrerstand.py  Tank, Instrumente, Lenkung, Sitz
  planierschild.py FRISCH 55 FH2
  modell.py       Register aller Teile (Name, Material, Explosionsrichtung)
tools/
  build.py        baut alles -> docs/modelle/hanomag-k55e/
  render.py       Vorschaubilder -> out/
docs/           Web-App (GitHub Pages)
  modelle/index.json           Liste aller Modelle
  modelle/hanomag-k55e/        modell.json, ansicht/*.stl, druck/*.stl, STEP
referenz/       Quellen und Maßherleitung
```

## Bauen

```sh
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt     # Windows
.venv/Scripts/python tools/build.py                # alles inkl. STEP
.venv/Scripts/python tools/build.py haube motor    # nur einzelne Teile
.venv/Scripts/python tools/render.py --vorschau    # Vorschaubilder
```

Maße ändern: in der jeweiligen Datei unter `cad/` (Original-mm), dann `tools/build.py`.

## Weitere Modelle

Neues Modell als eigenes Paket anlegen, mit einem Build-Skript nach `docs/modelle/<id>/` exportieren
(`modell.json` wie bei der K 55 E) und in `docs/modelle/index.json` eintragen. Die App zeigt es dann in der Auswahl oben.

## 3D-Druck

Die Dateien unter `docs/modelle/hanomag-k55e/druck/` sind druckfertig aufbereitet (`tools/druck.py`, läuft in `tools/build.py` mit):

- alle Einzelsolids eines Teils boolesch vereinigt (manifold3d): geschlossen, mannigfaltig, ohne Selbstüberschneidung
- eingeschlossene Hohlräume gefüllt, Splitter aus der Vereinigung entfernt
- in zusammenhängende Druckteile zerlegt, jedes mit der Unterseite auf z = 0, nebeneinander auf dem Bett
- Prüfbericht `out/druckpruefung.md`: Dichtheit, Wandstärke (Stichprobe), kleinste Teile, Überhänge

Gedacht für Resin oder FDM mit 0,4-mm-Düse und feiner Schichthöhe. Feinste Details sind 0,5 mm (Modell).
Große Teile (Rumpf, Planierschild) brauchen ein großes Bett oder müssen im Slicer geteilt werden.

```sh
.venv/Scripts/python.exe tools/druck.py            # nur Druckdateien neu
.venv/Scripts/python.exe tools/druck.py haube      # einzelnes Teil
```

## Genauigkeit

Maße aus Fotos und Prospekten abgeleitet, ca. ±5 %. Details siehe `referenz/MASSKONZEPT.md` und `referenz/FEHLERLISTE.md`.
Vor dem Druck die Anschlussmaße am eigenen Modell prüfen.

## Lizenz

Apache License 2.0, siehe `LICENSE`. Die Referenzfotos gehören ihren Urhebern und sind nicht Teil des Repositorys (Links im Quellen-Tab der App).
