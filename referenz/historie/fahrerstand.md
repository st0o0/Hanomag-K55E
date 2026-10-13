# Historie fahrerstand.py

Umbau-Notizen, die frueher im Modul-Docstring und in Parameterkommentaren standen.

- Fotobefund Tank (t39/t42/t46, fz_05/10/11, fz_01) und Tankunterbau/Werkzeugkaesten: Umbau 8 setzte den Kastenkoerper auf die Plattformkante (Video 137/158) und loeste den Sitz von DECK_Z (SITZ_ZB absolut 1005).
- Werkzeugkaesten hinten auf den Kotfluegeln (WK_*, `_kasten`, `_kaesten`) wurden entfernt: im Video 116/130/137/157 ist die Plattform hinten frei. Ebenso entfielen die ungenutzten Konstanten GETR_DECKEL, SITZ_LOCH_D, UB_Z0, Z_HANDGAS und die Rundinstrument-Variante `_instrument` (Blick +X) samt `_oben_rund`.
- Kein Batteriekasten / Werkzeugkasten vor dem Sitz (im Video nicht vorhanden).
- Sitz: urspruenglich flache gelochte Blechschale ohne Ruecken und ohne Polster (Fotos DSC04745, c_sl_box); Review 2 ersetzte sie durch die tiefe Mulde mit Polster (Video 128-140) und verschob sie weit nach hinten (SITZ_Y 200 unter dem Lenkrad, SITZ_X 2340 aus Video 2:44).
- Pedale: Review 2 (Nutzer: "Unter dem Lenkrad befinden sich die Pedale") - drei Pendelpedale statt der frueheren Anordnung. Schalthebel: Kamera-Fit Video 2:09 verschob den Balg von (1800, -100) nach (1600, -15); Review 3 (Short 0:45..0:50) machte die Stange duenn (Ø 13) mit kleiner Kugel.
- Armaturenkasten: Review Fussraum verkleinerte die Breite von 436 auf 375 (Kamera-Fit Video 2:09).
- Refactoring r13: explizite Importe, Typ-Hinweise, Parameterblock nach Bauteil, lange Funktionen in Helfer zerlegt (Tank, Unterbau, Armaturenkasten, Lenkrad, Fussraum, Sitz); lokales `SITZ_X = SITZ_XM` aufgeloest (Modulkonstante heisst jetzt SITZ_X, common.SITZ_X = 2150 wird hier nicht benutzt).
