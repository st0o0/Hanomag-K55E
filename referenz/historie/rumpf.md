# Historie cad/rumpf.py

Umbau- und Review-Notizen, die frueher im Modul-Docstring und in den Parameterkommentaren standen.

- Umbau 8 (Frame 128, Kamera-Fit auf Armaturenkasten/Lenkrad/Schaltknauf): Fussraum ~150..210 unter der Plattform-Oberkante
  (Spritzwandfuss ~680..710 bei Plattform ~860..875 im Fit) -> Boden 185 unter DECK_Z.
- Umbau 8: Unterkante des Kotfluegel-Randes DECK_UK - 10 = 891 (Flickr 880..900), Spalt zu den Greifern 123 (ueber dem
  Triebrad) .. 146 (Mitte), Video 174: eine Handbreit Luft.
- Review 2026-10-12 (Video 130/137): Kotfluegel glatt, kein Riffelblech -> ein glattes Trittblech bis DECK_Z.
- Review 2026-10-12 (Video 116/165/167, Flickr 40431489714): die obere Kette ist ueber die ganze Laenge sichtbar, keine
  hohe Schuerze an der Plattformkante -> nur eine schmale Abkantung (5 mm unter dem Trittblech) mit gerolltem Rand.
- Review 2026-10-13: Lenkbremsgehaeuse tiefer (X_BREMSE/Z_BREMSE), Oberkante 640 = Fussraumboden, damit der Fussraum bis
  y -300 reicht.
- Review 2 (Fussraum): FW_X0 vorn hinter den Zwischenflansch der Glocke (Flansch 1400..1426, Schraubenkoepfe bis 1434),
  10 hinter DECK_X0; Kamera-Fit: Boden unter dem Armaturenkasten bis ~1380 sichtbar. Davor fast kein Mittelblech mehr.
- Review 2 (Nutzer): "Fussraum mindestens so breit wie der Rahmen" = Haubenbreite 690 (|y| 345); links Video 128/129/132
  bis y -300 belegt, rechts Wand innen y 345 (Aussenseite 355, die Pumpenleitung bei |y| 392 bleibt auf der Plattform).
  Die Kotfluegelplatte ist im Fussraum bis |y| FW_Y1 + FW_WAND ausgeschnitten.
- Review Fussraum: der Stutzen (fahrerstand.py STUTZEN) steht bei x 1894, y -118 -> Inspektionsdeckel dahinter (x 1975..2040).
- Review 3 (Short 0:18.5/0:47/0:50): der Inspektionsdeckel ist eine dicke Platte (~18 hoch, dunkle Kante) mit grossen runden
  Schraubenkoepfen.
- Refactoring r13: Stern-Importe und globale Formen-Caches (_NIET, _RIFFEL) durch lru_cache ersetzt, getriebe(),
  plattform_mitte(), kotfluegel(), zugpendel() in Helfer zerlegt, Parameterblock nach Bauteil gegliedert.
