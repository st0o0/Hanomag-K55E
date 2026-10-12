# Hanomag K 55 E – 1:8 Scale Model

Parametric CAD model of the **Hanomag K 55 E** crawler dozer (built 1950–1956) with the FRISCH 55 FH2 dozer blade
at 1:8 scale, plus the **Modellwerkstatt** ("model workshop"): a web app to view and measure the model and to download the print files.

**Live:** https://hanomag.st0o0.net/

The web app and the CAD sources are in German. Dimensions are in mm throughout.

## Web app (`docs/`)

- View the model from all sides, show and hide parts, explode the assembly
- **Measure:** tap two points; snaps to nearby corners. Measure direct distance or only length X, width Y, height Z (keys 1–4).
  Dimensions are drawn as in CAD, with extension lines, arrows and a dimension line offset from the object.
  Drag the label to move the dimension line, drag the end points of a selected measurement along the model, and rename it or change its type in the list.
  Measurements are stored in the browser.
- **Section** lengthwise, crosswise or horizontal
- Click a part: overall dimensions and print file
- STL download per part, STEP file of the whole model
- **Print view** (key D): shows a part's print file the way it sits on the build plate. Choose the bed size
  (220 × 220, 300 × 300, resin 218 × 123); overhangs steeper than 45° are shown in red, together with the notes from the print check
- **Sources:** all reference photos, brochures and data with links and what they were used for
  (kept in `referenz/quellen.json`, picked up by `tools/build.py`)

Run locally:

```sh
python -m http.server 8765 -d docs
# http://127.0.0.1:8765
```

GitHub Pages: the workflow `.github/workflows/pages.yml` publishes `docs/` on every push to `main` that touches it
(or manually via *Actions → Pages → Run workflow*). One-time setup: *Settings → Pages → Build and deployment → Source: GitHub Actions*.

## Layout

```
cad/            CAD sources (build123d), dimensions in full-size mm
  common.py       scale, key dimensions, helpers
  haube.py        hood, radiator mask, grille, headlights
  laufwerk.py     track frames, idler, sprocket, rollers, tracks
  rumpf.py        frame, transverse leaf spring, transmission, platform
  motor.py        Hanomag D57 engine, radiator, exhaust, air filter
  fahrerstand.py  fuel tank, instruments, steering, seat
  planierschild.py FRISCH 55 FH2 dozer blade and hydraulics
  modell.py       registry of all parts (name, material, explode direction)
tools/
  build.py        builds everything -> docs/modelle/hanomag-k55e/
  druck.py        print-ready STL files and print check
  kollision.py    collision check between parts
  render.py       preview images -> out/
docs/           web app (GitHub Pages)
  modelle/index.json           list of all models
  modelle/hanomag-k55e/        modell.json, ansicht/*.stl (display), druck/*.stl (print), STEP
referenz/       sources and how the dimensions were derived
```

## Building

```sh
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt     # Windows
.venv/Scripts/python tools/build.py                # everything, including STEP
.venv/Scripts/python tools/build.py haube motor    # selected parts only
.venv/Scripts/python tools/render.py --vorschau    # preview images
```

To change a dimension, edit the relevant file in `cad/` (full-size mm), then run `tools/build.py`.

## Adding models

Create a new model as its own package, export it with a build script to `docs/modelle/<id>/`
(`modell.json` like the K 55 E) and add it to `docs/modelle/index.json`. The app then lists it in the model picker.

## 3D printing

The files in `docs/modelle/hanomag-k55e/druck/` are prepared for printing (`tools/druck.py`, run as part of `tools/build.py`):

- all solids of a part merged with boolean unions (manifold3d): closed, manifold, no self-intersections
- where two parts overlap, the smaller piece is trimmed flush so the parts fit together after printing
- enclosed voids filled, slivers from the union removed
- split into connected print pieces, each with its underside on z = 0, laid out side by side on the bed
- check report `out/druckpruefung.md`: watertightness, wall thickness (sampled), smallest pieces, overhangs

Intended for resin or FDM with a 0.4 mm nozzle and fine layers. The finest details are 0.5 mm at model scale.
Large parts (frame, dozer blade) need a large bed or have to be split in the slicer.

```sh
.venv/Scripts/python.exe tools/druck.py            # print files only
.venv/Scripts/python.exe tools/druck.py haube      # a single part
```

## Accuracy

Dimensions are derived from photos, brochures and measurements on a real machine, roughly ±5 %.
See `referenz/MASSKONZEPT.md` for how they were derived. Check the mating dimensions on your own model before printing.

## License

Apache License 2.0, see `LICENSE`. The reference photos belong to their owners and are not part of the repository
(links in the app's Sources tab).
