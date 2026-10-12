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
Sichtbar durch den Motorausschnitt: Einspritzpumpe, Kraftstofffilter mit Glasglocke (links),
Lichtmaschine, Deckel „HANOMAG DIESEL“, Ölbad-Luftfilter.

Auspuff: Durchbruch in der Haube bei x = 640, y = +220, Ø 70 (AUSPUFF_XY, Foto BS); Rohr senkrecht bis z ≈ 2000, Regenklappe.
Ansaug/Luftfilter: Durchbruch bei x = 900, y = −220, Ø 90 (ANSAUG_XY); Ölbadfilter Ø 198 bis z ≈ 1850.

## Haube & Maske (haube.py, Modellsystem 1:8)

| | Original-mm |
|---|---|
| Maske | 710 breit, 897 hoch, 210 tief, Unterkante z = 450 (MASKE_UK, Foto BV: h/b 1,26); Kappe 160 (Walze: im Seitenprofil über die ganze Höhe als Viertelkreis R ≈ 138 nach hinten gerollt, unten 6 Lippe über dem Querband; Oberkante quer als Bogen, Pfeilhöhe 22, Mitte z 1347, Übergang in die Seiten R 100; erhabenes Querband 15 hoch über dem Grill, Flügellogo auf der Wölbung), Grill 597 × 612, Sockel 125 (Foto g38, DSC04738) |
| Haube | x = 210 … 1080 (Foto BS), 690 breit, Dach quer gewölbt wie die Maske (gleicher Kreisbogen, Pfeilhöhe 22, Mitte z 1347, Ecken R 90) mit zwei Längssicken bei y = ±150; Schriftzug z 1187 zwischen den Sicken bei z 1145 und 1228 (Seitenwand eben bis ≈ 1236) |
| Motorausschnitt | vorderes Seitensegment x = 210 … 310 (SEG_X1, Foto BS) bis z = 620 herunter, dann Ausschnitt bis hinten offen, Oberkante z = 1125, Bogen R 280 (weich auslaufend, Foto DSC04742), gebordelter Rand folgt Bogen und läuft unter dem Schriftband waagerecht nach hinten; darüber nur das Schriftband |
| Schriftzug HANOMAG | Mitte x = 745, z = 1212, Teilung 88, Versalhöhe 55, zwischen den Sicken bei z = 1152 und 1272 |
| Typfeld K55E | erhaben eingerahmt, x = 215 … 305, z = 678 … 722; Schrift Versalhöhe ≈ 21 mm (2,6 mm im Modell), Strich ≈ 0,7 mm |
| Scheinwerfer | oben an den Maskenseiten, Mitte x = 110, y = ±430, z = 1190 (SCHEINWERFER; Foto BS, senkrecht und kalibriert, ist maßgeblich), Ø 150, Winkelhalter an der Maskenseite |
| Grill | breiter flacher Mittelsteg (80 breit, Mittelrippe) über die ganze Höhe vor 3 waagerechten Rundstäben (14 hoch; mit Rollwulst oben/unten 4 gleiche Felder, Teilung ≈ 155) vor dem Drahtgitter, Rollwulst und Eckzwickel |

Fotobefund (BS, BV): Maske mit breitem Mittelsteg und waagerechten Stäben (Foto g38), Drahtgitter dahinter, Flügellogo und Kühlerverschluss auf der Kappe,
Kurbelloch im Sockel auf der Pumpenachse. Haubenseite nur als Schriftband, Motor von der Seite sichtbar.

## Fahrerstand (fahrerstand.py)

| | Wert |
|---|---|
| Tank (verzinkt, Haubenform) | Seitenprofil: Stirn senkrecht bei x = 1085, Unterkante z = 1125 bis x = 1455, Oberkante z = 1335 (Dachflucht) bis x ≈ 1535, schräge Rückwand mit R 75 oben (Überhang über dem Armaturenbrett), 680 breit (Seiten ±340), Oberseite quer gewölbt (13 mm), obere Längskanten R 115; umlaufende Falz an der Stirn, zwei Spannbänder bei x = 1150 und 1400 mit Gewindestangen durch den Auflageflansch, hinten unten Lippe mit Schraubenreihe |
| Tankunterbau | Blechkasten x = 1085 … 1455, y = ±330, von der Plattform bis z = 1116, frei über der Kupplungsglocke (z > 962); oben Auflageflansch z = 1116 … 1125, x bis 1488, y = ±355 mit Knotenblechen; der Tank liegt nur auf (Haube + Tank = ein abnehmbares Teil) |
| Armaturenkonsole (rot) | Rückseite des Unterbaus x = 1455 … 1480, z = 962 … 1116, unter dem Tanküberhang; ovale Tafel links, Oeldruck/Thermometer bei y = 45, Instrumente an der Rückseite |
| Lenksäule | aus dem Unterbau bei (1510, 200, 1062) unter ≈ 51° nach hinten oben, auf ganzer Länge ≥ 34 mm vom Tank; Lenkrad Ø 450 bei (1830, 200, 1470) |
| Sitz | einteilige tiefe Schale mit hochgezogenem Rücken, Mitte x = 2150, Hülle x ≈ 1925 … 2405, Rücken bis z ≈ 1345, auf Blattfeder-Arm im Mittelsockel |
| Werkzeugkästen | hinten auf den Kotflügeln x = 2360 … 2618, |y| ≤ 873; vorn links Werkzeugkasten x = 1620 … 1890 |
| Batteriekasten | rechts vor dem Sitz, x = 1620 … 1890 |

## Planiereinrichtung FRISCH 55 FH2 (planierschild.py)

Aus Prospekt K 55 E und Einsatzfoto:

| | Wert |
|---|---|
| Schild | 2400 breit, 850 hoch, gewölbt, Oberkante nach vorn gekantet, Schneide mit Schraubenreihe, Eckmesser |
| Schubbalken | Kastenprofil ≈ 120 × 170, **außen** an den Ketten bei y = ±975, Höhe z ≈ 400 |
| Hinteres Gelenk | am Ende des Kettenrahmens, x ≈ 2250, z ≈ 400 |
| A-Bock | je Seite auf dem Schubbalken, fast symmetrisch (senkrechtes Seitenfoto BS): Füße x = 920 / 1650, Scheitel x = 1270, z = 1080; Stegblech mit dreieckigem Ausschnitt |
| Ölpumpe | runder Körper Ø 150 (x −225 … −60) vor dem Maskensockel bei (−70, 0, 530) auf einer Frontplatte, seitlich je ein Anschluss (z ≈ 490); je Seite EINE Leitung (Ø 36, Fotos 26271249857, 40431531504, 39333958410, BS) um die Maskenecke, bei |y| = 392 schräg an der Haubenseite von (0, 775) nach (1050, 1060), hinter dem Unterbau bei |y| = 410, z = 960 (Rohraußenkante ≥ 374 vom Tank) auf Standschellen zur Plattform; rechts Förderleitung ins Steuerventil, links Saugleitung in die Tankvorderwand (Deutung, nicht im Foto sichtbar) |
| Hubzylinder | liegend bei y = ±975, Achse z = 1080, Mittelzapfen x = 2520 im Endkasten (Foto BS, TRAVERSE_X), Rohr 1770 … 2740, Kolbenstange zum Scheitel bei 1270; |SZ| 1250 (Arbeitsstellung), Hub 315; doppeltwirkend: oberes dünnes Rohr (z 1175) = Stangenseite, vom Kopfstück in den hohlen Endkasten und von dort zum Querrohr z 1370; Kolbenseite über die Bügelschlaufe (z 1440) in den Endkasten; unteres Rohr (z 985) als Leckölleitung gedeutet |
| Traverse | zwei Endkästen außen (x = 2395 … 2830, z = 900 … 1240, |y| 880 … 1070) mit den Zylindern, dazwischen Querträger als Öltank (x = 2630 … 2830, Rückwand bündig mit den Endkästen, z = 900 … 1240) mit Schild „Frisch“ (y −570 … −130), Langloch rechts (y ≈ +620, ≈ 240 × 125), Einfüllstutzen Ø 115 rot gekappt bei y = −300 (26271221407); darüber zwei parallele Querrohre (z 1370 Leitung, z 1440 Bügel, Ø 28 / 32) mit Doppelschellen; Schutzbügel bis z = 1440 |
| Steuerventil | Block 130 × 150 × 150 hinten auf der Plattform (x 2475 … 2605, y 335 … 485, z 840 … 990) vor der Traverse, mit Kugelhebel (Oberkante z ≈ 1160) und Schrägstab (Fotos 39334013090, 40431531504, 26271221407); Rücklauf kurz in die Tankvorderwand, zwei Steigleitungen (Schwanenhals) auf die zwei Querrohre über der Traverse; Maße aus den Fotos geschätzt |

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
