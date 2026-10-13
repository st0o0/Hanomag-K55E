# Planierschild: Umbau-Historie

Ausgelagert aus dem Modul-Docstring von `cad/planierschild.py`. Der Docstring beschreibt nur den Stand; hier steht, wie er entstand.

## Video-Umbau 2026-10

- Gelenk x 1860 (vorher 2250), Schildlippe -800 (vorher -700), Balken hinten 170 / vorn 230 hoch.

## Umbau 2026-10-12 nach Review (Video zLWVF2nmQDY, Frames 008-012, 019-030, 043-048, 160-176, 194-200)

- Schild neu: gewoelbtes Blech mit flach umgekanteter Oberkante (kein Rundwulst), dahinter waagerechter Quertraeger und
  EINE stehende Rechteckplatte (~1000 breit, Oberkante z 1040, 2 Loecher, Knotenbleche an den Enden) statt Kastendeck mit
  4 U-Gabeln; schmale sichelfoermige Endbleche; Schubbalken ueber ein Zahnsegment (Neigungsverstellung) angelenkt;
  offener Rahmen zum Fahrzeug (Diagonalarm vom Schubbalken + Strebe zum Knoten unter der Pumpe).
- Schubbalken: aufgeschweisste Spitzplatten im vorderen Drittel, hinteres Ende schraeg, runde Lagernabe statt Vierkantblock.
- Leitung je Seite im Bogen hoch durch das obere Drittel des Motorausschnitts zum Zylinderkopf (statt flach auf z 560).
- Zylinderkopf rund (~1,2 x Rohr-Ø), unteres Rohr tief unter dem Zylinder; Langloch in der Schraege beider Endkaesten,
  Schild "Frisch" mittig, Arbeitsscheinwerfer hinten links.

## Umbau 2 (2026-10-12 spaet, Nutzerhinweise Video 1:56, 2:09, 2:17, 2:51)

- Steuerblock mit Kugelhebel (Ø 20 / Kugel Ø 50) rechts neben dem Sitz auf dem Bodenblech, Lenker zum Bodenbock;
  Ventil auf dem rechten Endkasten entfaellt (dort ist im Video nichts).
- Leitungen: links Saugleitung Oeltank -> Pumpe, rechts Druckleitung Pumpe -> Steuerblock (beide ueber den Haubenausschnitt
  auf z 1030 = HAUBE_BAND_Z - 60, vor dem Armaturenkasten auf die Plattform), Steuerblock -> zwei Querrohre ueber der
  Traverse (die "Gelaender"-Rohre) -> beide Endkaesten/Zylinder; kein T-Abzweig, kein Anschluss mehr am Zylinderkopf.
- Schubrahmen: C-Rahmen (Quertraeger am Blechruecken + 2 Diagonalen zu den Schubbalken, Video 008/169-173) statt
  Diagonalarmen mit Strebenknoten unter der Pumpe (Knoten lief beim Heben ins Pumpengehaeuse).
- Schildbohrungen Ø 38 (Video 047).

## Umbau 3 (Nutzerwunsch, Video 3:13-3:20 = Frames 193-200 und 165)

- Schildprofil neu: tiefere Mulde, stark nach vorn ausgerollte Lippe, schraeg vorstehende Schneide.
- Endbleche mit gerader Hinterkante und spitzer unterer Vorderecke.
- Stehende Platte ueber dem Schild und die Bohrungsreihe entfernt (die Loecher der Nordhorn-Maschine werden nicht uebernommen).

## Umbau 8

- Plattform `DECK_Z` neu: Spalt Kette/Aufbau ~120..150 wie Video 165/174 + Flickr; der Oeltank steht nur noch 12 mm ueber der
  Plattform, die Ablassschraube haengt hinter der Plattformkante frei.

## Umbau 11

- Einfuellstutzen Ø 115 am Oeltank entfaellt (im Video nicht vorhanden, t020/t050); Entlueftung = Rundpfosten.

## Umbau 13 (2026-10-13)

- Pumpe, Steuerblock, Pumpenleitungen und Zylinderleitungen nach `cad/hydraulik.py` ausgelagert (Klasse `Rohrzug` mit echten
  Kreisboegen); gemeinsame Traversen-/Zylindermasse in `cad/planiermasse.py`. Die Endkaesten bekommen ihre
  Leitungsdurchfuehrungen (Innenwand) aus `hydraulik.wanddurchfuehrungen()`. Pfosten auf dem Oeltank siehe `hydraulik.py`.

## Fotobefund (BS = blaue K55 senkrecht von rechts, BV = von vorn, FL, PK)

- A-Bock fast symmetrisch: Fuesse `ABOCK_FUESSE` (920 / 1650) auf dem Schubbalken, Scheitel `ABOCK_SCHEITEL` (1270, 1080); zwei
  Kastenstreben, Stegblech dazwischen mit dreieckigem Ausschnitt unten in der Mitte (BS: x ~1130..1420, ~210 hoch). Die fruehere
  "Asymmetrie" (PK/FL) war Perspektive der Schraegfotos.
- Hubzylinder waagerecht auf z = `TRAVERSE_Z` bei y = +-`Y_SCHUB`; Kopf bei x ~1770, Rohr hinten im Endkasten, Kolbenstange nach
  vorn zum Scheitel.
- Traverse: zwei rechteckige Endkaesten aussen (x 2395..2830, z 900..1240, um y +-975), dazwischen ein Kasten-Quertraeger gleicher
  Hoehe (zoom_heck_l: Schild "Frisch" auf der Rueckwand; zugleich Oeltank, Einfuellstutzen mit roter Kappe oben links,
  Entlueftung). Oben auf dem Quertraeger die Querleitung zwischen den Endkaesten, darueber das Querrohr des Schutzbuegels
  (zwei parallele Rohre). BS zeigt den runden Deckel auf der Endkasten-Aussenseite bei x ~2520: dort sitzt der Mittelzapfen des
  Hubzylinders (`TRAVERSE_X` in common.py). Rueckwand durchgehend (Quertraeger buendig mit den Endkaesten); Querrohre ueber der
  Traverse bei z 1240/1295.
- Schutzbuegel: Rohrbuegel ueber dem Endkasten (BS: Schlaufe x ~2310..2600, Scheitel z ~1400) mit Querrohr ueber der Traverse,
  dazu eine Rohrschlaufe hinten links (PK).
- Pumpe: runder Koerper (Ø ~150, x -225..-60) auf einer Frontplatte vor dem Maskensockel (BV, 26271249857, 40431531504), seitlich
  je ein Anschluss etwas unter der Achse. JE SEITE NUR EINE LEITUNG (Ø ~36). Kein Gestaenge an der Haubenseite, kein Ventilblock
  auf der Pumpe. Steuerblock rechts neben dem Sitz (vorher auf dem rechten Endkasten, dort ist im Video nichts).
- Einfuellstutzen Ø ~115 mit roter Kappe (26271221407), spaeter entfernt (Umbau 11).
- Fuehrungsplatte mit Steckbolzen auf dem Schubbalken kurz hinter dem Leitrad (FL).

## Hubkinematik: Herleitung (Stand nach Video-Auswertung 2026-10)

Arbeitsstellung = Schneide auf dem Boden, Schubbalken waagerecht.

- Gelenk G = (1860, 400) (Lagerkappe ~390 vor der Triebradachse, Video v.mp4 t=164/166 und Foto 40431489714), Scheitel
  S = (1270, 1080), Zapfen Z = (2520, 1080), Schneide P = (-800, 0).
- Schild 1120 hoch: Schubbalken dreht um G um 24,1 Grad -> S' = (1599, 1262), |S'Z| = 939 (Zylinder 11 Grad geneigt).
  Arbeitsstellung: |SZ| = 1250. Schild 200 tief: 4,3 Grad -> S'' = (1220, 1033), |S''Z| = 1301.
- Hub 1301 - 939 = 362 mm (aus der Arbeitsstellung 311 ein / 51 aus). Der Hub am Schild (1320) ist durch den kuerzeren Hebel
  (Scheitel 900 vom Gelenk) groesser als vorher (315). Hubwerte ungeprueft gegen das Original (im Video wird nicht gehoben).
- Kopf `X_KOPF` 1770: eingefahren steht der Gabelkopf (124 lang) bei 1599 + 124 = 1723, ~47 mm vor dem Abstreifer.
- Rohrende im Endkasten `X_BODEN` 2640 (120 hinter dem Zapfen, bleibt hinter dem Langloch der Schraege im Kasten): bei +11 Grad
  senkt sich der Boden um ~23. Kolbenstangenlaenge ab Auge 570..1080 moeglich (Kolben im Rohr).
- Balken (Video, Ueberlagerung ueber Leit-/Triebradnabe, Massstab 2,29 mm/px): hinten (x > 560) 170 hoch, vorn 230,
  Schraegubergang bei x 450..560, Balkenende vorn bei x -575 am Zahnsegment.
