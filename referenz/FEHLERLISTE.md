# Fehlerliste — Review 2026-10-12 gegen Video zLWVF2nmQDY (Nordhorn 2025), Flickr-Denkmal und Nutzerfotos

## Stand Umbau 2026-10-12 (abends)

Erledigt: A1 (6 Laufrollen), A2 (Leitung über den Haubenausschnitt), A3/A4 (Schild neu: offener Rücken, Querträger,
stehende Platte, Sichel-Endbleche, Zahnsegment, Schubbalken-Spitzbleche), A5 (Grill senkrechte Stäbe), A6 (Kotflügelschürze),
A7 (Dach 1410), A8 (Luftfilterkappe), Heck (2 Langlöcher, Lampe links, „Frisch“ mittig), Hubzylinderkopf, Schriftzug, Segment/K55,
Scheinwerfer, Leitrad-Speichen, Abgassammelrohr schwarz, Kühler rotbraun, Ölschild.

Offen:
- **Hydraulik-Steuerhebel**: Modell hat Ventilblock mit 2 Hebeln auf dem rechten Endkasten; im Video dort nichts, vermutlich
  die lange Kugelstange links vor dem Armaturenbrett (Frames 122, 131, 137, 138) → Nutzer fragen.
- Triebrad 12 statt 13 Zähne / R_TRIEB ≈ 316 (Kettenoberkante ≈ 30 zu hoch, Greifer stoßen 28 mm ins Trittblech); Kettenschluss neu.
- Leitradnabe ≈ 30 tiefer als Triebradnabe (Z_LEIT ≈ 372).
- Oberkante Motorausschnitt HAUBE_BAND_Z ≈ 1090 statt 1125 (mittel sicher; hängt an Tank und Motor).
- Schild: Knoten der Streben unter der Pumpe kollidiert beim Heben (Kinematik), Lage der stehenden Platte ±100.
- Kasten links hinten an der Haube, Armaturenbrett-Layout, Lenksäule, Sitz (Exemplar), Zugmaul-Schäkel, Ölbad-Topf, Riffelblech.
- Kollisionsprüfung: rumpf/fahrerstand 55 mm³ (Deck z 839, Träger z 519) prüfen.

Methode: Web-Viewer in Chrome mit Kamera auf die Video-Frames abgestimmt, fünf Bereichs-Reviews,
Hauptpunkte vom Koordinator selbst gegen die Frames geprüft (✔). Frame-Nr. = Sekunde im Video.
Schwere: A = Form/Proportion sofort sichtbar · B = Detail fehlt/falsch · C = Feinheit.
„Exemplar“ = Nordhorn und Denkmal unterscheiden sich, Entscheidung nötig.

## A — sofort sichtbar

| # | Teil | Befund | Beleg | Code |
|---|---|---|---|---|
| 1 ✔ | Laufrollen | **6 statt 5** Rollen, Abstand ≈ 205, Mitten x ≈ 885 / 1080 / 1290 / 1500 / 1710 / 1910 (±25) | Video 165, Flickr 40431489714 unabhängig | laufwerk.py, common.py |
| 2 ✔ | Hydraulikleitung | Rohr Ø ≈ 38 von der Pumpe an der Maskenunterkante im Bogen hoch, bei x ≈ 450–500 / z ≈ 1030 waagerecht quer durch das obere Drittel des Motorausschnitts, am A-Bock vorbei zum Zylinderkopf (z ≈ 1080–1130) — **beidseitig, fehlt im Modell** (dort nur flach auf z 560 hinter der Kette) | Video 010, 058–078, 165, 172, 196; Flickr 39333958410, 40431531504 | planierschild.py `leitungen()`, `Z_LTG` |
| 3 ✔ | Schild-Rückseite | Kein geschlossenes Schrägdeck. Real: gerundeter Schildrücken mit Querträger, darüber **eine stehende Rechteckplatte** mit Knotenblechen (statt 4 U-Gabeln), offener Rahmen zwischen Schild und Maske | Video 010, 047, 165, 196 | planierschild.py `schild()` (`ZB0/ZB1`, `XB`, `ZL`) |
| 4 ✔ | Schild-Seitenbleche | Real schmale **sichelförmige** Endbleche entlang der Blechkrümmung, nicht große Rechteckplatten mit Viertelbogen; Schubbalken-Anschluss über **Zahnsegment** (Neigungsverstellung) | Video 165, 196 | planierschild.py |
| 5 ✔ | Grill | Durchgehendes Kühlerfenster mit 3–4 senkrechten Stäben, kein 2×4-Feld mit Querbändern und Drahtgitter; Kühler dahinter rotbraun. Rote K 55 (DSC04737) hat Querbänder → Exemplar/Maskenvariante | Video 172, 196; Flickr 26271249857 | haube.py |
| 6 | Kotflügelschürze | Abkantung y ±900, z 686…838, x 1430…2780 verdeckt die hintere Hälfte der oberen Kette; real ist die obere Kette über die ganze Länge sichtbar | Video 116, 165, 167; Flickr | rumpf.py |
| 7 | Haubendach | ≈ 1410–1440 statt 1347 (Video 165: 1432, 167: 1441, Flickr: 1426; Luftfilter/Auspuff-Abstände und Maskenproportion DSC04737 stützen das) | zwei unabhängige Reviews | common.py `HAUBE_DACH_Z`, haube.py |
| 8 | Luftfilterkappe | Schlanke gerippte Kappe Ø ≈ 125–140 statt Pilzhut Ø 220/236 (breiter Teller nur an der orangen Maschine) | Video 054, 165, 172; DSC04729, 04737 | motor.py `_ansaugung` |

## B — Details

| Teil | Befund | Beleg |
|---|---|---|
| Schriftzug HANOMAG | Mitte x ≈ 615–650 statt 745, Länge ≈ 500–540 statt ≈ 580, Teilung ≈ 78 statt 88 | Video 010, 165 |
| Vorderes Haubensegment / K55 | Segment ≈ 150–200 breit (SEG_X1 ≈ 370) statt 100; K55 ≈ 40 hoch, Mitte x ≈ 300, z ≈ 960–1000 | Video 165, 172 |
| Scheinwerfer | Mitte an der Naht Maske/Haube (x ≈ 200–260), z ≈ 1250–1300; Modell x 110 / z 1190 (rote K 55 tiefer → Exemplar) | Video 172, Flickr |
| Kasten links hinten an der Haube | Eigener flacher Kasten mit Deckel, Haken, Konsole, ≈ 330–400 lang, z ≈ 930–1250, darunter offen; Modell: durchgehender Nietkasten bis Plattform | Video 054–066 |
| Kettenoberkante | über Triebradnabe ≈ 330–337 statt 362 (≈ 8 % zu hoch) | Flickr, Video 165 |
| Leitrad | Speichen gekrümmt, breit gegossen, große Nabe; Nabe ≈ 30 tiefer als Triebradnabe (Modell 10) | Video 165, Flickr |
| Abgassammelrohr | rostbraunes Rohr direkt unter dem Ausschnittbogen zu auffällig, real dunkler Spalt | Video 177–182, DSC04736 |
| Hubzylinder | Kopfblock ≈ 1,2× Rohr-Ø und gerundet (Modell 1,7×, eckig); unteres Rohr biegt am Kopf ab und läuft tief nach hinten | Video 079–088 |
| Armaturenbrett | links großes Rundinstrument, 3 Knöpfe oben, Zündschloss Mitte rechts, rechts 2 Instrumente übereinander; Kasten türkisgrün | Video 121–140 |
| Lenksäule / Hebel | Säule Ø ≈ 35 ohne dicke Hülse; langer Schalthebel am unteren Rand des Armaturenkastens | Video 128–140 |
| Schubbalken | aufgeschweißte Stufen-/Schrägplatten im vorderen Drittel, Balkenende schräg | Video 022, 165 |
| Zugmaul | waagerechter Bolzen mit Bügelschäkel | Video 145–154 |

### Heck der Traverse (Nutzer bestätigt: gilt für Nordhorn UND Denkmal)

| Teil | Befund | Code |
|---|---|---|
| Langlöcher | ≈ 200 × 110 mit Halbkreis-Enden in der **Schrägecke beider** Endkästen (links und rechts); Modell nur eins rechts in der geraden Rückwand bei y 730, auf der Schräge stattdessen runder 6-Schrauben-Deckel | planierschild.py `Y_LANGLOCH`, Z. 600/634 |
| Lampe | Scheinwerfer Ø ≈ 150 mit Glas und Gitter auf kurzem Stiel, **links** auf dem Traversenende — fehlt | planierschild.py |
| Schild „Frisch“ | **in der Mitte** der Rückwand, Modell bei y −230 (links der Mitte) | planierschild.py Z. 644 |

## Exemplar-Entscheidungen (Nordhorn ≠ Denkmal)

- Sitz: Nordhorn tiefe Schale mit schwarzem Polster; Modell flache Lochblechschale (DSC04745).
- Ölfilter rechts senkrecht (Nordhorn) vs. 32° geneigt (rote K 55, Modell).
- Farben Nordhorn: Motor blassgrün, Anlasser schwarz.

## C — Feinheiten

Ölbad-Topf links tiefer (UK ≈ 1020) und Ø ≈ 200 · Ölschild rot ≈ 150 × 80 · Schild-Oberwulst flacher ·
Schildlöcher ≈ 35–40 · Greifer niedriger/breiter · Kette am Denkmal rot lackiert · Bodenblech glatt statt Riffelblech ·
Ölpumpe an Nordhorn evtl. höher · Ausschnittbogen flacher/elliptischer.

## Bestätigt

Radstand, Maskenfront–Triebradnabe (2223 vs 2250), Maske ≈ 90 vor der Kettennase, Kettenteilung, Stützrolle im A-Bock-Fenster,
Zylinderachse, A-Bock-Form und Scheitel, Traversen-Endkästen, Tank mit zwei Bändern, Naht Maske/Haube x ≈ 210, Tankansatz ≈ 1080,
Kasten HANOMAG DIESEL, Reihenfolge rechts (Anlasser, Deckel, Ölfilter, Lichtmaschine), Auspuff x ≈ 700, Lenkradlage,
Schildbreite ≈ 2200 / Höhe ≈ 760, Schneide auf Bodenebene, Schildfront ≈ 800 vor der Maske, Schubbalken außen auf Nabenhöhe.

Einzelbefunde mit Messwegen: Session-Scratchpad `review/befund_*.md` (nicht im Repo).
