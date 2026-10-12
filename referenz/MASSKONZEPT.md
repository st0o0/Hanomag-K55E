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
| Laufrollen | 5 Stück, x = 840 / 1072,5 / 1305 / 1537,5 / 1770, Radius 100 |
| Stützrolle | 1 Stück, x = 1360, oben (im Fenster des A-Bocks) |
| Kettenrahmen (Kasten) | z = 327 … 467, Breite 230 um y = ±635 |
| Spannfeder | in geschlossenem Rohr Ø 150 am Kettenrahmen, x = 910 … 1258 (Widerlager 1255 … 1290 ersetzt die Kastenstirn bei x 1270), Federteller und Stange vorn sichtbar |

Fotobefund: offener Kettenrahmen (die Spannfeder ist von der Seite sichtbar), Leitrad mit 5 Speichen und
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
| Plattform / Kotflügel | **DECK_Z = 840**, x = 1430 … 2780, Breite 1800 (Kante y = ±900); Kette oben reicht bis z ≈ 804 |
| Zugpendel | hinten mittig, z ≈ 465 |

Fotobefund: hinten ein hochkant stehender Getriebekasten mit Zugpendel darunter, seitlich eckige
Endantriebsgehäuse. Plattform = ebene Trittbleche links/rechts auf Höhe DECK_Z, mit Konsolen abgestützt.

## Motor (motor.py)

Motor D57 (4 Zyl., Bohrung ≈ 110, Hub ≈ 150): Zylinderabstand 155, Zylindermitten x = 480 / 635 / 790 / 945,
Block x = 400 … 1030, y = ±190, Zylinderkopf bis z ≈ 1110, Ventildeckel bis 1180.
Kühler x = 225 … 335, y = ±320, z = 480 … 1290 (innerhalb der Maske), Einfüllrohr nach vorn zum Verschluss
auf der Maskenkappe (x = 140). Kurbelwelle z = 600.
Schwungradgehäuse x = 1030 … 1090, r 300 um z = 640, oben bei 950 beschnitten (unter dem Tank). Alles muss **innerhalb der Haube** bleiben: Haubenwand innen y = ±(345−13).
Sichtbar durch den Motorausschnitt: Einspritzpumpe mit Förderpumpe, Kraftstofffilter mit Glasglocke (links), Düsenhalter mit Druckleitungen,
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

Auspuff: Durchbruch in der Haube bei x = 640, y = +220, Ø 70 (AUSPUFF_XY, Foto BS); Rohr senkrecht bis z ≈ 2000, Regenklappe.
Ansaug/Luftfilter: Durchbruch bei x = 900, y = −220, Ø 90 (ANSAUG_XY); Ölbadfilter Ø 198 bis z ≈ 1850.

## Haube & Maske (haube.py, Modellsystem 1:8)

| | Original-mm |
|---|---|
| Maske | 710 breit, 897 hoch, 210 tief, Unterkante z = 450 (MASKE_UK); nach eigenen Fotos DSC04737/38/42: glatte Kappe 135 (Vorderfläche senkrecht, vorn oben R 35, Oberkante quer als Bogen, Pfeilhöhe 42, Mitte z 1347, Übergang in die Seiten R 85 (Flickr-Fotos 26271249857/39333958410, 2026-10), gleicher Querschnitt wie die Haube) mit Flügellogo; Grillfenster 678 breit (Randstreifen 16) × 641 hoch, oben Querband 46, unten Abschlusswulst 48 (Mitte ≈ z 590), Sockel 116 mit Kurbelloch Ø 54 (z 530, Pumpenachse). Foto-Seitenverhältnis der Front eher h/b ≈ 1,36 (Maske dort ~8 % höher) – nicht übernommen, MASKE_UK bleibt |
| Haube | x = 210 … 1080 (Foto BS), 690 breit, Dach quer gewölbt wie die Maske (gleicher Kreisbogen, Pfeilhöhe 42, Mitte z 1347, Ecken R 85; Längsrichtung eben) mit zwei Längssicken bei y = ±150; Schriftzug z 1187 zwischen den Sicken bei z 1145 und 1228 (Seitenwand eben bis ≈ 1236) |
| Motorausschnitt | vorderes Seitensegment x = 210 … 310 (SEG_X1, Foto BS) bis z = 620 herunter, dann Ausschnitt bis hinten offen, Oberkante z = 1125, Bogen R 280 (weich auslaufend, Foto DSC04742), gebordelter Rand folgt Bogen und läuft unter dem Schriftband waagerecht nach hinten; darüber nur das Schriftband |
| Schriftzug HANOMAG | Mitte x = 745, z = 1212, Teilung 88, Versalhöhe 55, zwischen den Sicken bei z = 1152 und 1272 |
| Typfeld K55E | erhaben eingerahmt, x = 215 … 305, z = 678 … 722; Schrift Versalhöhe ≈ 21 mm (2,6 mm im Modell), Strich ≈ 0,7 mm |
| Scheinwerfer | oben an den Maskenseiten, Mitte x = 110, y = ±430, z = 1190 (SCHEINWERFER; Foto BS, senkrecht und kalibriert, ist maßgeblich), Ø 150, Winkelhalter an der Maskenseite |
| Grill | schmaler Mittelsteg (70 breit, Randwulste, flacher Kanal) über die ganze Höhe vor 3 flachen Querbändern (je 40 hoch, zwei Wülste; mit oberem Querband 46 und Abschlusswulst 48 vier gleiche Felder, Teilung ≈ 150) vor feinem Drahtgitter (Teilung 1,8 / Draht 0,6 Modell-mm); keine Eckzwickel, kein Rollwulst um das Fenster (Foto) |

Fotobefund (BS, BV): Maske mit breitem Mittelsteg und waagerechten Stäben (Foto g38), Drahtgitter dahinter, Flügellogo und Kühlerverschluss auf der Kappe,
Kurbelloch im Sockel auf der Pumpenachse. Haubenseite nur als Schriftband, Motor von der Seite sichtbar.

## Fahrerstand (fahrerstand.py)

| | Wert |
|---|---|
| Tank (verzinkt, Haubenform) | Seitenprofil: Stirn senkrecht bei x = 1085, Unterkante z = 1125 bis x = 1455, Oberkante = Haubendach (Mitte z = 1347, Querschnitt aus haube.z_dach) bis x ≈ 1535, schräge Rückwand mit R 75 oben (Überhang über dem Armaturenbrett), 680 breit (Seiten ±340), Oberseite quer gewölbt wie das Haubendach (Pfeilhöhe/Kantenradius werden aus haube.py übernommen, z. Zt. R 85); umlaufende Falz an der Stirn, zwei Spannbänder bei x = 1150 und 1400 mit Gewindestangen durch den Auflageflansch, hinten unten Lippe mit Schraubenreihe |
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
| Schild | 2200 breit, ~ 760 hoch (Seitenfoto 40431489714, Review: niedriger als zuvor 850), gewölbt, Front blank/verzinkt grau mit Bohrungsreihe (8 × Ø 28, Foto 7826381704), kräftiger Wulst oben; EINE durchgehende lackierte Schneide mit Senkschrauben im ~190-mm-Raster, keine Eckmesser; Seitenbleche D-Platten (Hinterkante x −300, nur 3 Einzelschrauben, keine Randreihe); Diagonalstrebe als Flachstahl 120 × 30 in Gabellaschen; Z-Obergurt mit 4 stehenden Laschen (das schwarze Blech oberhalb des Schilds auf 7826381704 bewusst nicht übernommen) |
| Schubbalken | hinten (x ≥ 700) hoher flacher Kasten 120 × 250 (z 275 … 525), nach vorn auf 130 verjüngt; **außen** an den Ketten bei y = ±975; hinten quadratischer Lagerblock 190 × 190 (4 Sechskantschrauben, Fettkappe, 50 außen überstehend) |
| Hinteres Gelenk | am Ende des Kettenrahmens, x ≈ 2250, z ≈ 400 |
| A-Bock | je Seite auf dem Schubbalken: Füße x = 920 / 1650, Scheitel x = 1270, z = 1080; Streben nach oben verjüngt (150 → 110, 70 tief), Stegblech mit dreieckigem Ausschnitt, flacher Kastenkopf am Scheitel (180 × 170), Knotenblech vor dem vorderen Fuß auf dem Balken |
| Ölpumpe | runder Körper Ø 150 (x −225 … −60) vor dem Maskensockel bei (−70, 0, 530) auf einer Frontplatte, seitlich je ein Anschluss; je Seite EINE Leitung (Ø 36), **flach** an der Haubenseite (|y| = 392, z 560, knapp über dem Längsträger, Konsolen auf dem Träger bzw. Wandlaschen an der Maske) bis x 1405, dort kurz senkrecht auf Plattformhöhe, am Boden (z 885, |y| 440, Standschellen) nach hinten; rechts Förderleitung bis x 2250, dann schwarzer Schlauch (knapp über Werkzeugkasten, z 1085) zum Steuerblock auf dem rechten Endkasten, links Saugleitung in die Tankvorderwand (Deutung). Nutzerhinweis: Leitungen knapp über Plattform, keine hohen Bögen |
| Hubzylinder | liegend bei y = ±975, Achse z = 1080, Mittelzapfen x = 2520 im Endkasten, Rohr Ø 100 (1770 … 2740), Kolbenstange Ø 48 blank zum Scheitel bei 1270, eckiger Kopfblock 60 × 165 × 165 mit Eckschrauben, zwei dünne Rohre (z ± 62) über die Zylinderlänge in den Endkasten (unteres biegt am Kopf nach unten); |SZ| 1250 (Arbeitsstellung), Hub 315 |
| Traverse | zwei Endkästen außen (x = 2395 … 2830, z = 900 … 1170, |y| 880 … 1070) mit beidseitig abgeschrägter hinterer Außenecke (Δx 120 / Δy 190, ganze Kastenhöhe, Rückwand gerade bis |y| 880) und Stützschräge darunter, dazwischen Querträger als Öltank (x = 2630 … 2830, z = 900 … 1170, Rückwand bündig) mit umlaufendem Bodenflansch 35 × 45; Schild „Frisch“ dunkelblau mit weißem Rand und weißer Schrift (410 × 215, y −230), Langloch 270 × 110 rechts in der Rückwand (y ≈ +730, vor der Schräge), Einfüllstutzen Ø 136 bei y −170 mit flacher rotbrauner Kappe; niedriges Geländer (3 Doppelschellen): zwei parallele Rohre Ø 30 (z 1240 / 1295, Abstand 55) dicht über der Traverse, links Haarnadelbogen bei y −680, rechts Schlaufe über dem Steuerblock; keine Schlaufe hinten links |
| Steuerblock | Ventilbatterie (3 Scheiben) auf Grundplatte am vorderen Ende des rechten Endkastens (x 2340 … 2510, y 942 … 1060, z 1170 … 1272, ragt 55 über die Kastenfront) mit Hebelbock + Kulisse hinten, kurzem Kugelhebel Ø 40 und langem schrägem Hebel (≈ 320, 15° nach vorn, Kugel Ø 30); Anschlüsse Druck/Rücklauf innen (x 2468 / 2500, z 1225), zwei schwarze Schläuche, zwei Leitungen nach hinten zu den Querrohren (Foto 40431489714; Maße geschätzt) |

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
