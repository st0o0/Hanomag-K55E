# Maßkonzept Hanomag K 55 E (Modell 1:8)

Verbindliche Schnittstellen für alle Baugruppen. Alle Maße in **Original-mm**.
Koordinaten: X = 0 an der Vorderkante der Kühlermaske, nach hinten positiv.
Y = 0 Fahrzeugmitte, +Y = rechts in Fahrtrichtung. Z = 0 Boden (Greiferspitze der Kette).
`haube.py` arbeitet im Modellsystem (1:8, z = 0 Maskenunterkante), alle anderen in Original-mm
und werden mit `zu_modell()` umgerechnet.

Toleranz der Quellen: ±5 %. Was hier steht, ist der **gemeinsame Stand** — wer davon abweichen muss,
ändert zuerst `cad/common.py` (Abschnitt HAUPTMASSE) und dieses Dokument.

## Gesamtfahrzeug

| | Wert |
|---|---|
| Länge über Zugpendel | 2880 (Maske x=0 … Zugpendel x≈2880) |
| Breite über Plattform | 1800 |
| Höhe über Luftfilter | 1840 |
| Spur (Kettenmitte zu Kettenmitte) | 1270 → Kettenmitte y = ±635 |
| Kettenbreite | 400 → Kette außen y = ±835 |
| Bodenfreiheit Rahmen | ≈ 330 |

## Laufwerk (laufwerk.py)

| | Wert |
|---|---|
| Leitrad vorn: Mitte | Nennlage x = 450 (X_LEIT), Ist-Lage 456,6 in der Spannführung, z = 392 (Teilkreis-Radius 330). Foto BS: Maske steht ≈ 75 … 100 vor der Kettennase |
| Triebrad hinten: Mitte | x = 2250, z = 402 (Teilkreis-Radius 340), 13 Zähne |
| Bodenplatten-Oberkante unterer Trum | z = 62 (Platte 22 dick darunter, Greifer 40 → Boden z = 0); Bolzen bei z = 79 |
| Kettenteilung | 154,6 (36 Glieder, passend zu 13 Zähnen und Radstand 1800) |
| Triebrad-Innennabe / Endantriebsflansch | Nabe bis y = ±425 (Flansch r 155), Schwinglagerring des Rahmens y = ±(440…510), r 205 |
| Laufrollen | 6 Stück, x = 885 / 1088 / 1291 / 1494 / 1697 / 1900 (Teilung 203), R 90, Spurkranz R+10 |
| Stützrolle | 1 Stück, x = 1360, oben (im Fenster des A-Bocks) |
| Kettenrahmen (Kasten) | z = 327 … 467, Breite 230 um y = ±635 |
| Spannfeder | in geschlossenem Rohr Ø 150 am Kettenrahmen, x = 910 … 1258 (Widerlager 1255 … 1290 ersetzt die Kastenstirn bei x 1270), Federteller und Stange vorn sichtbar |

Fotobefund: offener Kettenrahmen (die Spannfeder ist von der Seite sichtbar), Leitrad mit 5 gekrümmten gegossenen Speichen (Nabe R 128) und
breitem Laufkranz, Triebrad als geschlossene Scheibe mit Schraubenkranz am Nabendeckel, Laufrollen mit
Spurkränzen in Lagerböcken, die unter dem Rahmen hängen. Bodenplatten mit **einem** hohen Greifer an
der Hinterkante, je 2 Schrauben pro Kettenglied-Seite, Kettenglieder mit Bolzen/Buchse.

## Rumpf (rumpf.py)

| | Wert |
|---|---|
| Längsträger (U-Profil) | y = ±240, z = 380 … 520, x = 100 … 1500 |
| Querblattfeder vorn | x ≈ 560, trägt das Leitrad-Joch |
| Kupplungsglocke | Flansch am Motor x = 1090 (FLANSCH_GLOCKE_X), Achse z = 640, r 300 (Oberkante 940), Kegel und Schaft bis 1400, Kupplungsgehäuse 1426 … 1640 |
| Getriebe/Lenkbremsen | x = 1640 … 2380, Lenkbremstrommeln außen bei y = ±365, z = 600 |
| Endantriebsgehäuse | um Triebradachse (x = 2250, z = 402), Flansch bei y = ±330 |
| Plattform / Kotflügel | **DECK_Z = 840**, x = 1430 … 2780, Breite 1800 (Kante y = ±900); vorn nur schmale Abkantung y ±900, z 766 … 838, obere Kette über die ganze Länge sichtbar; Kette oben reicht bis z ≈ 804 |
| Zugpendel | hinten mittig, z ≈ 465 |

Fotobefund: hinten ein hochkant stehender Getriebekasten mit Zugpendel darunter, seitlich eckige
Endantriebsgehäuse. Plattform = ebene Trittbleche links/rechts auf Höhe DECK_Z, mit Konsolen abgestützt.

## Motor (motor.py)

Motor D57 (4 Zyl., Bohrung ≈ 110, Hub ≈ 150): Zylinderabstand 155, Zylindermitten x = 480 / 635 / 790 / 945,
Block x = 400 … 1030, y = ±190, Zylinderkopf bis z ≈ 1110, Ventildeckel bis 1180.
Kühler (Block rotbraun) x = 225 … 335, y = ±320, z = 480 … 1333 (Kastenende; Netzende 1243; innerhalb der Maske), Einfüllrohr nach vorn zum Verschluss
auf der Maskenkappe (x = 140). Kurbelwelle z = 600.
Schwungradgehäuse x = 1030 … 1090, r 300 um z = 640, oben bei 950 beschnitten (unter dem Tank). Alles muss **innerhalb der Haube** bleiben: Haubenwand innen y = ±(345−13).
Sichtbar durch den Motorausschnitt: Einspritzpumpe mit Förderpumpe, zwei Kraftstofffilter mit Glasbirnen (links), Düsenhalter mit Druckleitungen,
Kastendeckel „HANOMAG DIESEL“, Lichtmaschine, Ölbad-Luftfilter.

Kastendeckel „HANOMAG DIESEL“ links (Nutzerfotos DSC04644–49, DSC04742, DSC04735/36; cad/motor.py `_seitendeckel`). Auf den Fotos ist es ein Gussgehäuse mit Deckel am hinteren Block, ohne sichtbare Pumpenanbauten außer Hebeln:

| Teil | Maße / Lage (Original-mm, y links negativ) |
|---|---|
| Gussgehäuse | 360 × 185 (x 665 … 1025, z 740 … 925, y −184 … −220), obere Gussleiste mit 2 Stehbolzen (x 715, 835) |
| Deckel | 320 × 165, Rand mit Kuppenschrauben, erhabene Fläche 285 × 130 mit „HANOMAG / DIESEL“ (Versalhöhe 42), 8 Schrauben, Ablassschraube SW 32 unten links, Rohrschelle oben mittig |
| Lageransatz links | Gussbuckel x 627 … 667, Lagernabe oben, senkrechter Hebel Ø 14 mit Kugelknopf, Rippenleiste, Stutzen unten |
| Reglerwelle rechts | Lagerhals am Gehäuse, Welle Ø 16 bei z 880 bis x 1050, Hebel nach unten mit Kugelknopf (x 1020, z 824) |
| Gusslaschen unten | zwei Laschen unter dem Gehäuse (x 887, 970) mit Drahtbügel |

Nicht umgesetzt: eingegossene Motornummer „503801“ unter dem Kasten (Strich < 0,5 mm im Druck). Der Motorraum ist sonst auf dem Stand vor Commit 9f865b6 (Einspritzleitungen, Düsenhalter, Bosch-Pumpe, Filter).

Motor-Fotoreview 2026-10 (Fotos DSC04729–44; Einspritzpumpe, Kasten HANOMAG DIESEL, Druckleitungen, Düsenhalter, Förderpumpe unverändert):
- Auspuff: Durchbruch bei x = 700, y = +220, Ø 58 (AUSPUFF_XY/AUSPUFF_D); offenes glattes Rohr Ø 48 bis z 1985 = 575 über Dach (keine Regenklappe/Schelle); Abgassammelrohr schwarz, Ø 72 auf z 1064 (über der Lichtmaschine).
- Ansaugung: Ölbadtopf Ø 184, z 1054 … 1244 UNTER der Haube (x 950, y −236; Spannring + 2 Bügelverschlüsse, grau), Rohr Ø 66 durch das Dach (ANSAUG_XY/ANSAUG_D, Durchbruch Ø 76), Kragen (2 Ringe, z 1478 … 1540), Luftfilterkappe gerippt Ø 130 mit flachem Deckel Ø 136, Oberkante z 1840 = 430 über Dach (Nordhorn/rote K 55; der breite Teller nur an der orangen Maschine), Leuchte mit Glasdom Ø 80 / 85 hoch 90 vor der Rohrachse (DSC04729).
- Kraftstofffilter: zwei getrennte Glasbirnen Ø 100 bei x 525 / 756, y −270, Mitte z 1095, Köpfe z 1138 … 1168, Konsolen auf dem Zylinderkopf. Gusszylinder links Ø 90, z 838 … 1000 bei x 416, y −262 mit Flansch und Gestänge (z 905); Ölschild rot 150 × 70 an der Kopfwand.
- Rechts: Anlasser tuerkis Ø 115, Achse y 272, z 830, x 813 … 1030 (rotes Antriebsteil, grauer Magnetschalter, Panzerkabel Ø 32); Ölfilter Kanister Ø 55 × 130, 32° nach vorn, auf 4-Schrauben-Platte x 720, z 840; Lichtmaschine 190 lang, Mitte z 960; roter Handlochdeckel 220 × 94 (x 780 … 1000, z 922 … 1016, 10 Schrauben); Rohr Ø 10 (z 905) mit T-Stück bei x 1000, Schlauch und Hahn; Öldruckleitung entfernt.

## Haube & Maske (haube.py, Modellsystem 1:8)

| | Original-mm |
|---|---|
| Maske | 710 breit, **960 hoch** (z 450 … 1410, h/b 1,35, wie DSC04737), 210 tief, Unterkante z = 450 (MASKE_UK); glatte Kappe 115 (Vorderfläche senkrecht, vorn oben R 35, Oberkante quer als Bogen, Pfeilhöhe 42, Mitte z 1410, Übergang in die Seiten R 85, gleicher Querschnitt wie die Haube) mit Flügellogo; Grillfenster 620 breit × 640 hoch (Rand 45, Sockel 205) mit Kurbelloch Ø 54 (z 530, Pumpenachse) |
| Haube | x = 210 … 1080 (Foto BS), 690 breit, Dach HAUBE_DACH_Z = **1410**, quer gewölbt wie die Maske (gleicher Kreisbogen, Pfeilhöhe 42, Ecken R 85; Längsrichtung eben) mit zwei Längssicken bei y = ±150 |
| Motorausschnitt | vorderes Seitensegment x = 210 … 370 (SEG_X1) bis z = 620 herunter, dann Ausschnitt bis hinten offen, Oberkante z = 1125, Ausschnittbogen flach elliptisch 340 × 200 (weich auslaufend, Foto DSC04742), gebordelter Rand folgt Bogen und läuft unter dem Schriftband waagerecht nach hinten; darüber nur das Schriftband |
| Schriftzug HANOMAG | Mitte x = 630, z = 1190, Teilung 78; Sicken bei z = 1145 und 1240 |
| Typfeld „K55“ | freie Schrift ohne Rahmen, Versalhöhe 38, Mitte x = 298, z = 980 (Foto: „K55“ ohne E) |
| Fensterblech | Kantenblech am Unterrand beider Motorfenster, x 305 … 1080, y 332 … 345 (bündig), z 737 … 772, Oberkante mit schräger Lippe bis 780 |
| Scheinwerfer | x = 230, |y| = 430, z = 1290 (SCHEINWERFER), Ø 150, Halter an der Haubenvorderkante |
| Grill | durchgehendes Fenster mit 3 senkrechten Stäben (18 breit, 4 Felder); keine Querbänder, kein Mittelsteg; dahinter senkrechte Lamellen; keine Eckzwickel, kein Rollwulst um das Fenster (Foto) |

Fotobefund (BS, BV): Maske mit durchgehendem Grillfenster, senkrechten Stäben und Lamellen dahinter, Flügellogo und Kühlerverschluss auf der Kappe,
Kurbelloch im Sockel auf der Pumpenachse. Haubenseite nur als Schriftband, Motor von der Seite sichtbar.

## Fahrerstand (fahrerstand.py)

| | Wert |
|---|---|
| Tank (verzinkt, Haubenform) | Seitenprofil: Stirn senkrecht bei x = 1085, Unterkante z = 1125 bis x = 1455, Oberkante = Haubendach (Mitte TANK_Z1 = 1398, Querschnitt aus haube.z_dach) bis x ≈ 1535, schräge Rückwand mit R 75 oben (Überhang über dem Armaturenbrett), 680 breit (Seiten ±340), Oberseite quer gewölbt wie das Haubendach (Pfeilhöhe/Kantenradius werden aus haube.py übernommen, z. Zt. R 85); umlaufende Falz an der Stirn, zwei Spannbänder bei x = 1150 und 1400 mit Gewindestangen durch den Auflageflansch, hinten unten Lippe mit Schraubenreihe |
| Tankunterbau | Blechkasten x = 1085 … 1455, y = ±330, von der Plattform bis z = 1116, frei über der Kupplungsglocke (z > 962); oben Auflageflansch z = 1116 … 1125, x bis 1488, y = ±355 mit Knotenblechen; der Tank liegt nur auf (Haube + Tank = ein abnehmbares Teil) |
| Armaturenkonsole (rot) | Rückseite des Unterbaus x = 1455 … 1480, z = 962 … 1116, unter dem Tanküberhang; ovale Tafel links, Oeldruck/Thermometer bei y = 45, Instrumente an der Rückseite |
| Lenksäule | aus dem Unterbau bei (1510, 200, 1062) unter ≈ 51° nach hinten oben, auf ganzer Länge ≥ 34 mm vom Tank; Lenkrad Ø 450 bei (1830, 200, 1470) |
| Sitz | flache gelochte Blechschale OHNE Rücken/Polster (Fotos DSC04745, c_sl_box): Randellipse 380 × 430 (x 1960 … 2340), 30 mm gemuldet, Blech 6, 3° nach hinten geneigt, 18 Löcher Ø 26 (Ring 6 + Ring 12), umgebördelter Rand (Wulst + Schürze 14), zwei Quersteifen, Sitzträger-Block mit Nieten unter der Mitte, Unterkante Mitte z = 1030, auf Blattfeder-Arm im Mittelsockel (x 2250) |
| Werkzeugkästen | hinten auf den Kotflügeln x = 2360 … 2618, |y| ≤ 873; vorn links Werkzeugkasten x = 1620 … 1890 |
| Batteriekasten | rechts vor dem Sitz, x = 1620 … 1890 |

## Planiereinrichtung FRISCH 55 FH2 (planierschild.py)

Aus Prospekt K 55 E und Einsatzfoto:

| | Wert |
|---|---|
| Schild | 2200 × 760, Blech gewölbt (Stich 135), Oberkante flach umgekantet, Front blank/verzinkt grau mit Bohrungsreihe, Schneide blank, leicht nach vorn, mit Senkschrauben im ~190-mm-Raster, keine Eckmesser; schmale sichelförmige Endbleche. Dahinter waagerechter Querträger (z 590 … 746) und EINE stehende Platte ≈ 900 × 280 (y −675 … 225, Oberkante z 1040, 2 Löcher, Knotenbleche). Kein Schrägdeck, keine U-Gabeln, keine D-Platten |
| Schubbalken | vorn an Zahnsegment (Neigungsverstellung) bei x −575, Spitzbleche x −160 … 260, hinten schräg mit runder Nabe; hinten (x ≥ 700) hoher flacher Kasten 120 × 250 (z 275 … 525), nach vorn auf 130 verjüngt; **außen** an den Ketten bei y = ±975; hinten Lagerblock 190 × 190 (4 Sechskantschrauben, Fettkappe, 50 außen überstehend) |
| Hinteres Gelenk | Video t=164/158 + Foto 40431489714: Lagerkappe ≈ 390 VOR der Triebradachse, x ≈ 1860, z ≈ 400 (vorher 2250); Schubbalken hinten (x > 560) 170 hoch, vorn 230 hoch mit Schrägübergang, Balkenende vorn bei x −850 an der Schildfront (Maßstab ±10 %: Rollenabstand/Kettenteilung widersprüchlich 2,2…2,9 mm/px) |
| Rahmenanbindung | Gelenkböcke y ±780, z 380; Diagonalarm zum Balken (x 60), Strebe zu Knoten unter der Pumpe (x −110); Kinematik offen |
| A-Bock | je Seite auf dem Schubbalken: Füße x = 920 / 1650, Scheitel x = 1270, z = 1080; Streben nach oben verjüngt (150 → 110, 70 tief), Stegblech mit dreieckigem Ausschnitt, flacher Kastenkopf am Scheitel (180 × 170), Knotenblech vor dem vorderen Fuß auf dem Balken |
| Ölpumpe | runder Körper Ø 150 (x −225 … −60) vor dem Maskensockel bei (−70, 0, 530) auf einer Frontplatte, seitlich je ein Anschluss; je Seite EINE Leitung (Ø 36): von der Maskenecke schräg bis x 470, dann waagerecht z 1040, |y| 392 durch den Motorausschnitt, hinter der Haube zum Zylinderkopf innen (z 1100); T-Abzweig bei x 1405 zum Bodenrohr (Deutung). Nutzerhinweis: keine hohen Bögen |
| Hubzylinder | liegend bei y = ±975, Achse z = 1080, Mittelzapfen x = 2520 im Endkasten, Rohr Ø 100 (Rohrboden x 2640), Kolbenstange Ø 48 blank zum Scheitel bei 1270, runder Kopf Ø 120, zwei dünne Rohre (z ± 62) über die Zylinderlänge in den Endkasten (unteres Rohr bei z 955, biegt am Kopf nach unten); |SZ| 1250 (Arbeitsstellung), Hub 315 |
| Traverse | zwei Endkästen außen (x = 2395 … 2830, z = 900 … 1170, |y| 880 … 1070) mit beidseitig abgeschrägter hinterer Außenecke (Δx 120 / Δy 190, ganze Kastenhöhe, Rückwand gerade bis |y| 880) und Stützschräge darunter, dazwischen Querträger als Öltank (x = 2630 … 2830, z = 900 … 1170, Rückwand bündig) mit umlaufendem Bodenflansch 35 × 45; Schild „Frisch“ mittig dunkelblau mit weißem Rand und weißer Schrift (410 × 215), Langloch 200 × 110 in der Schrägecke BEIDER Endkästen, Einfüllstutzen Ø 136 bei y −170 mit flacher rotbrauner Kappe; niedriges Geländer (3 Doppelschellen): zwei parallele Rohre Ø 30 (z 1240 / 1295, Abstand 55) dicht über der Traverse, links Haarnadelbogen bei y −680, rechts Schlaufe über dem Steuerblock; Arbeitsscheinwerfer Ø 150 hinten links auf dem Endkasten (Nordhorn und Denkmal, Nutzer bestätigt) |
| Steuerblock | kompakter Gusskörper ≈ 140 × 140 × 170 (olivgrün/Anbaulack) auf Grundplatte direkt auf dem rechten Endkasten über dem Zylindereintritt (x 2464 … 2604, y 905 … 1045, z 1184 … 1320), Gussabsätze, seitliche runde Kappe mit Handrad innen, Anschlussstutzen; kurzer Hebel (170) mit Kugel Ø 40 und dünne Stange Ø 20 (450, 28° nach vorn); zwei Rohre vorn senkrecht auf den Kasten, hoher runder Bügel (z 1450) darüber, zwei schwarze Schläuche von innen, zwei Leitungen nach hinten (Foto 40431489714; 7826381704 ist ein anderes FRISCH-Exemplar mit großer Kugel, Einzelanfertigung, Details abweichend); Maße geschätzt |

Wirkprinzip: der Zylinder schiebt den A-Bock-Scheitel vor/zurück, der Schubbalken dreht um das hintere
Gelenk, das Schild hebt/senkt (Hub 1120 über / 200 unter Fahrebene).

## Referenzfotos (Session-Ordner, nicht im Repo)

`C:\Users\st0o0\AppData\Local\Temp\claude\D--GIT\27bc3557-26fc-41dd-8d50-3587ce6b3daa\scratchpad\ref\`

- `fz_01m.jpg` Seite links, komplett (Laufwerk, Haube, Fahrerstand)
- `fz_02m.jpg`, `fz_07m.jpg` Front (Maske, Scheinwerfer, Ketten)
- `fz_04m.jpg`, `fz_08m.jpg` Heck (Getriebekasten, Zugpendel, Kotflügel, Werkzeugkästen)
- `fz_05m.jpg`, `fz_10m.jpg`, `fz_11m.jpg` Fahrerstand (Tank, Konsole, Lenkrad, Hebel, Pedale)
- `fz_06m.jpg` Motorausschnitt (Einspritzpumpe, Filter, Deckel „HANOMAG DIESEL“)
- `fz_09m.jpg` Schräg vorn links (Leitrad, Scheinwerferhalter)
- `mv_*.jpg` Wiking-Modell 1:25 (Laufwerk, Chassis, Motor, Sitzbank)
- `prospekt_oben.png`, `prospekt_unten.png` Prospekt K 55 E mit FRISCH-Schild (A-Bock, Schubbalken, Traverse)
- `alamy_zoom.png` Einsatzfoto K 55 E mit Schild (A-Bock, liegender Zylinder, Schubbalken)
