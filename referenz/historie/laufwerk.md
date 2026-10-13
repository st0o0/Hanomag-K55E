# Historie cad/laufwerk.py

Umbau- und Review-Notizen, die frueher im Modul-Docstring und in den Parameterkommentaren standen.

- Umbau 8: flache, breite Greiferrippen am Kettenglied (PLATTE_D/GREIFER_H, Video 165/174).
- Umbau 8: Z_STUETZ_BOLZEN nach Flickr-Seitenfoto (Greifer oben 720..745); Review 2026-10-13: Video 2:44 (s164, Rollen-/
  Triebradnabe-Fit, Bildneigung 2 Grad herausgerechnet) Greiferspitzen vorn ~750..765, hinten ~760..770 -> oberer Trum auf die
  Gerade Leitrad-Oberkante (669) -> Triebrad-Oberkante (701) angehoben.
- Review 2026-10-13: SAG = 5 (vorher mehr): Nordhorn-Video 2:44, oberer Trum fast gerade.
- Review 2: Leitradnabe liegt 30 tiefer als die Triebradnabe; Kettenschluss mit 36 Gliedern bei Radstand 1800 (vorher 1870),
  Leitrad-Ist-Lage ~57 vor X_LEIT.
- Review 2: R_ROLLE 90 statt 100 (Spurkranz 118 vorher), damit bei Teilung ~203 die Spurkraenze freibleiben.
- Review 2026-10-12: SECHS Laufrollen (Video 165/167 + Flickr 40431489714), Mittenabstand 200..215.
- Refactoring r13: Stern-Importe entfernt, Typ-Hinweise, leitrad()/triebrad()/laufrolle()/_rahmen_rechts() in Helfer zerlegt,
  ungenutzter Alias YT entfernt, Parameterblock nach Bauteil gegliedert.
