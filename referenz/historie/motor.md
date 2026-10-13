# Historie cad/motor.py

Umbau-Notizen, die beim Refactoring aus dem Modul-Docstring und den Parameterkommentaren entfernt wurden
(Stand 2026-10-13). Die Geometrie ist unveraendert.

- Zylinderabstand ZYL_T = 155 (frueher 230): Block x 400..1030, Steuergehaeuse/Riementrieb davor.
- Raumgrenzen "Stand Umbau 2026-10": Maske x 0..210, z 450..1410; Haube x 210..1080; Motorausschnitt z 620..1090.
- DZ_OBEN = 70: Absenkung von Kopf und Aufbauten gegenueber dem alten Stand (Kopf-Unterkante damals 1000).
- Kuehler: das Netz endet bei z 1243, weil die Maske 63 hoeher ist als frueher.
- Anlasser ANL_Z (Umbau 10): Video 2:44/2:58, Unterkante ~812 direkt ueber der Fensterblech-Lippe 808;
  vorher 830.
- Oelschild links (Review 2026-10): rot (Video 095/100/108, DSC04644), ~150 x 70 statt 120 x 28.
- Luftfilter-Topf (Review 2): Unterkante ~1020, Durchmesser 190..210.
- Kuehler-Netz-Kommentar "Maske ist 63 hoeher als frueher" und der Hinweis in KD_X ("= haube.KD_X") wurden
  in neutrale Formulierungen ueberfuehrt.

## Entfernte, ungenutzte Namen
`_schrift` (alte Einzelbuchstaben-Schrift, ersetzt durch `_schrift_mass`), Konstante `Z_MOTOR_OBEN`,
ueberfluessiges `return` am Ende von `_links_zusatz`.
