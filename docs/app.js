import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { STLLoader } from "three/addons/loaders/STLLoader.js";

/* ------------------------------------------------------------------ *
 * Modellwerkstatt – 3D-Modelle ansehen, messen, Druckdateien laden.
 * Modellsystem (CAD): x nach hinten, y nach rechts, z nach oben, mm 1:n.
 * three.js: y oben -> Wurzelgruppe um -90° um X gedreht.
 * ------------------------------------------------------------------ */

const $ = (s) => document.querySelector(s);
const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const fmt = (v, d = 1) => v.toLocaleString("de-DE", { minimumFractionDigits: d, maximumFractionDigits: d });

// Lackierungen ab Werk (siehe Info-Hinweis in index.html); Raeder je Lackierung
const LACK = { gruen: 0x3b5a55, blau: 0x2b4a6b, rot: 0xa72920, grau: 0x9aa1a6, gelb: 0xd8ae1f };
const RAEDER = { gruen: 0x9b2321, blau: 0x9b2321, rot: 0x9b2321, grau: 0x8a9196 };
const STANDARD = { farbe: "#a8262b", rauheit: 0.55, metall: 0.15 };
let PALETTE = {};
function material(name) {
  const m = PALETTE[name] || STANDARD;
  const mat = new THREE.MeshStandardMaterial({
    color: new THREE.Color(m.farbe), roughness: m.rauheit, metalness: m.metall,
  });
  if (m.deckkraft !== undefined) { mat.transparent = true; mat.opacity = m.deckkraft; mat.depthWrite = false; }
  if (m.leuchten) { mat.emissive = new THREE.Color(m.farbe); mat.emissiveIntensity = m.leuchten; }
  mat.userData = { name, emissive: mat.emissive.clone() };
  return mat;
}

/* ---------------- Grundgeruest ---------------- */
const stage = $("#stage");
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.localClippingEnabled = true;
stage.prepend(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(32, 1, 1, 20000);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.09;

scene.add(new THREE.HemisphereLight(0xffffff, 0x80868b, 1.1));
const sonne = new THREE.DirectionalLight(0xffffff, 1.6);
sonne.position.set(-400, 700, 500);
scene.add(sonne);
const gegen = new THREE.DirectionalLight(0xffffff, 0.5);
gegen.position.set(600, 300, -500);
scene.add(gegen);

import("three/addons/environments/RoomEnvironment.js").then(({ RoomEnvironment }) => {
  const pm = new THREE.PMREMGenerator(renderer);
  scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.4;
});

const wurzel = new THREE.Group();
wurzel.rotation.x = -Math.PI / 2;
scene.add(wurzel);

const state = {
  info: null, basis: "", teile: new Map(), box: new THREE.Box3(),
  messen: false, schnitt: false, achse: "x", flip: false,
  messungen: [], offen: null, hover: null, auswahl: null, explode: 0,
};

/* ---------------- Laden ---------------- */
async function start() {
  let liste = [];
  try { liste = await (await fetch("modelle/index.json")).json(); } catch { /* leer */ }
  const sel = $("#modell-wahl");
  liste.forEach((m) => sel.add(new Option(m.name, m.id)));
  const id = (location.hash || "").slice(1) || (liste[0] && liste[0].id);
  if (!id) { $("#loading span").textContent = "Keine Modelle gefunden."; return; }
  sel.value = id;
  sel.addEventListener("change", () => { location.hash = sel.value; location.reload(); });
  await ladeModell(id);
}

async function ladeModell(id) {
  state.basis = `modelle/${id}/`;
  const info = await (await fetch(state.basis + "modell.json", { cache: "no-cache" })).json();
  const v = info.build ? `?v=${info.build}` : "";            // neue Dateien nach jedem Build, sonst Browser-Cache
  state.info = info;
  document.title = `${info.name} · Modellwerkstatt`;
  $("#modell-name").textContent = info.name;
  $("#modell-unter").textContent = info.untertitel || "";
  $("#massstab").textContent = `M 1:${info.massstab}`;
  $("#raster-note").textContent = `Raster 10 mm = ${10 * info.massstab} mm Original`;

  const loader = new STLLoader();
  let fertig = 0;
  const bar = $("#loading-bar");
  PALETTE = info.materialien || {};
  const schichten = info.teile.flatMap((t) => (t.schichten || [{ material: t.material, ansicht: t.ansicht }]).map((s) => ({ t, s })));
  info.teile.forEach((t) => {
    const gruppe = new THREE.Group();
    gruppe.userData.teil = t;
    wurzel.add(gruppe);
    state.teile.set(t.id, { teil: t, gruppe, meshes: [], sichtbar: true });
  });
  await Promise.all(schichten.map(async ({ t, s }) => {
    const geo = await loader.loadAsync(state.basis + s.ansicht + v);
    if (!geo.getAttribute("normal")) geo.computeVertexNormals();
    const mesh = new THREE.Mesh(geo, material(s.material));
    mesh.userData.teil = t;
    mesh.renderOrder = PALETTE[s.material]?.deckkraft !== undefined ? 2 : 0;
    const e = state.teile.get(t.id);
    e.gruppe.add(mesh); e.meshes.push(mesh);
    fertig++;
    bar.style.setProperty("--p", `${Math.round((fertig / schichten.length) * 100)}%`);
  }));
  wurzel.updateMatrixWorld(true);
  state.box.setFromObject(wurzel);
  baueRaster();
  baueTeileListe();
  baueDateien();
  baueInfo();
  messungenLaden();
  $("#loading").hidden = true;
  ansicht("iso", true);
}

/* ---------------- Raster (Boden) ---------------- */
let raster = null;
function baueRaster() {
  if (raster) { scene.remove(raster); raster.geometry.dispose(); raster.material.dispose(); }
  const c = state.box.getCenter(new THREE.Vector3());
  const groesse = Math.ceil(Math.max(state.box.max.x - state.box.min.x, state.box.max.z - state.box.min.z) * 1.6 / 10) * 10;
  raster = new THREE.GridHelper(groesse, groesse / 10, new THREE.Color(css("--grid-major")), new THREE.Color(css("--grid-minor")));
  raster.position.set(Math.round(c.x / 10) * 10, (state.info?.boden_z ?? state.box.min.y) - 0.05, Math.round(c.z / 10) * 10);
  raster.visible = $("#t-raster").getAttribute("aria-pressed") === "true";
  scene.add(raster);
}
window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => state.info && baueRaster());
$("#t-raster").addEventListener("click", (e) => {
  const an = e.currentTarget.getAttribute("aria-pressed") !== "true";
  e.currentTarget.setAttribute("aria-pressed", String(an));
  if (raster) raster.visible = an;
});

/* ---------------- Ansichten ---------------- */
const RICHTUNG = {
  iso: [-1, 0.62, 0.95], front: [-1, 0.04, 0], rear: [1, 0.04, 0],
  left: [0, 0.04, 1], right: [0, 0.04, -1], top: [-0.0001, 1, 0.0001],
};
let flug = null;
function ansicht(name, sofort = false) {
  const ziel = state.box.getCenter(new THREE.Vector3());
  const r = state.box.getSize(new THREE.Vector3()).length() / 2;
  const abstand = r / Math.sin(THREE.MathUtils.degToRad(camera.fov / 2)) * (camera.aspect < 1 ? 1.35 : 0.95);
  const pos = ziel.clone().add(new THREE.Vector3(...RICHTUNG[name]).normalize().multiplyScalar(abstand));
  if (sofort || matchMedia("(prefers-reduced-motion: reduce)").matches) {
    camera.position.copy(pos); controls.target.copy(ziel); controls.update(); return;
  }
  const p0 = camera.position.clone(), t0 = controls.target.clone(), s = performance.now();
  flug = (now) => {
    const k = Math.min(1, (now - s) / 600), e = 1 - Math.pow(1 - k, 3);
    camera.position.lerpVectors(p0, pos, e); controls.target.lerpVectors(t0, ziel, e);
    if (k >= 1) flug = null;
  };
}
document.querySelector(".views").addEventListener("click", (e) => {
  const b = e.target.closest("button[data-view]"); if (b) ansicht(b.dataset.view);
});

/* ---------------- Auseinanderziehen ---------------- */
$("#explode").addEventListener("input", (e) => {
  state.explode = +e.target.value;
  state.teile.forEach(({ teil, gruppe }) => {
    const [x, y, z] = teil.explode || [0, 0, 0];
    gruppe.position.set(x * state.explode, y * state.explode, z * state.explode);
  });
});

/* ---------------- Lackierung ---------------- */
function faerben(namen, farbe, faktor = 1) {
  state.teile.forEach(({ meshes }) => meshes.forEach((m) => {
    if (namen.includes(m.material.userData.name)) m.material.color.copy(farbe).multiplyScalar(faktor);
  }));
}
let anbauWieLack = true;
$("#farben").addEventListener("click", (e) => {
  const b = e.target.closest("button[data-farbe]"); if (!b) return;
  const c = new THREE.Color(LACK[b.dataset.farbe]);
  faerben(["lack"], c); faerben(["motor"], c, 0.82);
  faerben(["raeder"], new THREE.Color(RAEDER[b.dataset.farbe]));
  if (anbauWieLack) faerben(["anbau"], c);
  document.querySelectorAll("#farben button").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
});
$("#farben-anbau").addEventListener("click", (e) => {
  const b = e.target.closest("button[data-farbe]"); if (!b) return;
  anbauWieLack = b.dataset.farbe === "lack";
  const lack = document.querySelector('#farben [aria-pressed="true"]').dataset.farbe;
  faerben(["anbau"], new THREE.Color(LACK[anbauWieLack ? lack : b.dataset.farbe]));
  document.querySelectorAll("#farben-anbau button").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
});

/* ---------------- Teileliste und Auswahl ---------------- */
function baueTeileListe() {
  const box = $("#teile-liste");
  box.innerHTML = "";
  const gruppen = new Map();
  state.info.teile.forEach((t) => {
    if (!gruppen.has(t.gruppe)) gruppen.set(t.gruppe, []);
    gruppen.get(t.gruppe).push(t);
  });
  gruppen.forEach((teile, name) => {
    const g = document.createElement("div");
    g.className = "gruppe";
    g.innerHTML = `<h3>${name}</h3>`;
    teile.forEach((t) => {
      const row = document.createElement("div");
      row.className = "teil";
      row.dataset.id = t.id;
      const farbe = (PALETTE[t.material] || STANDARD).farbe;
      row.innerHTML = `<input type="checkbox" id="v-${t.id}" checked aria-label="${t.name} anzeigen">
        <button type="button">${t.name}</button><span class="farbpunkt" style="background:${farbe}"></span>`;
      row.querySelector("input").addEventListener("change", (e) => zeige(t.id, e.target.checked));
      row.querySelector("button").addEventListener("click", () => waehle(t.id));
      g.appendChild(row);
    });
    box.appendChild(g);
  });
}

function zeige(id, an) {
  const e = state.teile.get(id);
  e.sichtbar = an; e.gruppe.visible = an;
  const cb = document.getElementById(`v-${id}`); if (cb) cb.checked = an;
}

function waehle(id) {
  if (state.auswahl) state.teile.get(state.auswahl).meshes.forEach((m) => m.material.emissive.copy(m.material.userData.emissive));
  document.querySelectorAll(".teil.aktiv").forEach((r) => r.classList.remove("aktiv"));
  state.auswahl = id;
  const panel = $("#auswahl");
  if (!id) { panel.hidden = true; return; }
  const { teil, meshes } = state.teile.get(id);
  meshes.forEach((m) => m.material.emissive.setHex(0x3a2a00));
  document.querySelector(`.teil[data-id="${id}"]`)?.classList.add("aktiv");
  const n = state.info.massstab;
  const [l, b, h] = teil.masse_mm;
  panel.innerHTML = `
    <h3>${teil.name}</h3>
    ${teil.hinweis ? `<p>${teil.hinweis}</p>` : ""}
    <table class="masstab">
      <thead><tr><th>Außenmaß</th><th class="n">Modell</th><th class="n">Original</th></tr></thead>
      <tbody>
        <tr><td>Länge</td><td class="n">${fmt(l)} mm</td><td class="n">${fmt(l * n, 0)} mm</td></tr>
        <tr><td>Breite</td><td class="n">${fmt(b)} mm</td><td class="n">${fmt(b * n, 0)} mm</td></tr>
        <tr><td>Höhe</td><td class="n">${fmt(h)} mm</td><td class="n">${fmt(h * n, 0)} mm</td></tr>
      </tbody>
    </table>
    <div class="seg">
      ${teil.druck ? `<a class="btn" href="${state.basis + teil.druck}" download>Druckdatei · ${fmt(teil.druck_mb)} MB</a>
        <button type="button" class="btn leise" data-a="druck">Druckansicht</button>` : ""}
      <button type="button" class="btn leise" data-a="nur">Nur dieses zeigen</button>
      <button type="button" class="btn leise" data-a="alle">Alle zeigen</button>
      <button type="button" class="btn leise" data-a="weg">Ausblenden</button>
    </div>`;
  panel.hidden = false;
  panel.querySelector('[data-a="nur"]').onclick = () => state.teile.forEach((_, k) => zeige(k, k === id));
  panel.querySelector('[data-a="alle"]').onclick = () => state.teile.forEach((_, k) => zeige(k, true));
  panel.querySelector('[data-a="weg"]').onclick = () => { zeige(id, false); waehle(null); };
  const dk = panel.querySelector('[data-a="druck"]'); if (dk) dk.onclick = () => druckAn(true, id);
  zeigeTab("teile");
}

/* ---------------- Dateien und Info ---------------- */
function baueDateien() {
  const ul = $("#dateien");
  ul.innerHTML = "";
  state.info.teile.filter((t) => t.druck).forEach((t) => {
    const li = document.createElement("li");
    const n = t.druck_koerper, bett = t.druck_bett_mm;
    li.innerHTML = `<a href="${state.basis + t.druck}" download>${t.name}</a><span>${fmt(t.druck_mb)} MB</span>
      ${n ? `<small>${n === 1 ? "1 Druckteil" : `${n} Druckteile`}${bett ? ` · Bett ${bett.map((v) => fmt(v, 0)).join(" × ")} mm` : ""}</small>` : ""}
      <button type="button" class="link ansehen">Ansehen</button>`;
    li.querySelector(".ansehen").addEventListener("click", () => druckAn(true, t.id));
    ul.appendChild(li);
  });
  $("#step-zeile").innerHTML = state.info.step
    ? `Gesamtmodell für Fusion 360 / FreeCAD: <a href="${state.basis + state.info.step}" download>STEP-Datei (zip)</a>`
    : "";
}

function baueInfo() {
  const o = state.info.original || {};
  const zeilen = [
    ["Länge", o.laenge && `${o.laenge} mm`], ["Breite", o.breite && `${o.breite} mm`],
    ["Höhe", o.hoehe && `${o.hoehe} mm`], ["Spur", o.spur && `${o.spur} mm`],
    ["Kettenbreite", o.kette && `${o.kette} mm`], ["Leergewicht", o.gewicht && `${o.gewicht} kg`],
    ["Motor", o.motor], ["Baujahre", o.baujahre], ["Maßstab", `1:${state.info.massstab}`], ["Stand", state.info.stand],
  ].filter(([, v]) => v);
  $("#daten").innerHTML = zeilen.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join("");
  $("#genauigkeit").textContent = state.info.genauigkeit || "";
  const benutzt = new Set(state.info.teile.flatMap((t) => (t.schichten || []).map((s) => s.material)));
  $("#legende").innerHTML = [...benutzt].map((k) => {
    const m = PALETTE[k] || STANDARD;
    return `<li><i style="background:${m.farbe}"></i>${m.name || k}</li>`;
  }).join("");
  baueQuellen();
}

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
function baueQuellen() {
  const q = state.info.quellen;
  $("#tab-quellen").hidden = !q;
  if (!q) return;
  $("#quellen").innerHTML = (q.gruppen || []).map((g) => `
    <h2>${esc(g.titel)}</h2>
    <ul class="quellen">${(g.eintraege || []).map((e) => `
      <li>
        ${e.url ? `<a href="${esc(e.url)}" target="_blank" rel="noopener noreferrer">${esc(e.titel)}</a>` : `<b>${esc(e.titel)}</b>`}
        ${e.zeigt ? `<span class="zeigt">${esc(e.zeigt)}</span>` : ""}
        ${e.benutzt ? `<span class="benutzt">Benutzt für: ${esc(e.benutzt)}</span>` : ""}
      </li>`).join("")}
    </ul>`).join("");
  $("#quellen-hinweis").textContent = q.hinweis || "";
}

/* ---------------- Tabs ---------------- */
function zeigeTab(name) {
  document.querySelectorAll(".tabs [role=tab]").forEach((t) => {
    const an = t.id === `tab-${name}`;
    t.setAttribute("aria-selected", String(an));
    document.getElementById(t.getAttribute("aria-controls")).hidden = !an;
  });
}
document.querySelector(".tabs").addEventListener("click", (e) => {
  const t = e.target.closest("[role=tab]"); if (t) zeigeTab(t.id.replace("tab-", ""));
});

/* ---------------- Schnitt ---------------- */
const schnittEbene = new THREE.Plane(new THREE.Vector3(-1, 0, 0), 0);
const ACHSE_WELT = { x: new THREE.Vector3(1, 0, 0), y: new THREE.Vector3(0, 0, -1), z: new THREE.Vector3(0, 1, 0) };

function setzeSchnitt() {
  const a = ACHSE_WELT[state.achse];
  const k = +$("#schnitt-pos").value;
  const lo = Math.min(a.dot(state.box.min), a.dot(state.box.max));
  const hi = Math.max(a.dot(state.box.min), a.dot(state.box.max));
  const v = lo + (hi - lo) * k;
  if (state.flip) schnittEbene.set(a.clone(), -v); else schnittEbene.set(a.clone().negate(), v);
  const n = state.info.massstab;
  let text;
  if (state.achse === "x") text = `${fmt(v)} mm ab Maskenfront · ${fmt(v * n, 0)} mm Original`;
  else if (state.achse === "y") text = `${fmt(v)} mm von Mitte · ${fmt(v * n, 0)} mm Original`;
  else { const zb = v - (state.info.boden_z ?? 0); text = `${fmt(zb)} mm über Boden · ${fmt(zb * n, 0)} mm Original`; }
  $("#schnitt-out").textContent = text;
}
function schnittAn(an) {
  state.schnitt = an;
  $("#t-schnitt").setAttribute("aria-pressed", String(an));
  $("#schnitt-panel").hidden = !an;
  state.teile.forEach(({ meshes }) => meshes.forEach((mesh) => {
    mesh.material.clippingPlanes = an ? [schnittEbene] : [];
    mesh.material.side = an ? THREE.DoubleSide : THREE.FrontSide;
    mesh.material.needsUpdate = true;
  }));
  if (an) setzeSchnitt();
}
$("#t-schnitt").addEventListener("click", () => schnittAn(!state.schnitt));
$("#schnitt-pos").addEventListener("input", setzeSchnitt);
$("#schnitt-flip").addEventListener("click", () => { state.flip = !state.flip; setzeSchnitt(); });
document.querySelector("#schnitt-panel .seg").addEventListener("click", (e) => {
  const b = e.target.closest("button[data-achse]"); if (!b) return;
  state.achse = b.dataset.achse;
  document.querySelectorAll("#schnitt-panel .seg button").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
  setzeSchnitt();
});

/* ---------------- Messen ----------------
 * Bemaßung wie im CAD: Hilfslinien vom Objekt weg, Maßlinie mit Pfeilen im Abstand, Beschriftung in der Mitte.
 * Alle Bemaßungsgeometrie liegt in `bem` (Kind von `wurzel`), also im CAD-System: x hinten, y rechts, z oben.
 * Gemessen wird immer am zusammengebauten Modell (lokale Punkte), angezeigt am ggf. auseinandergezogenen.
 */
const MESSFARBE = () => new THREE.Color(css("--mess"));
const AKTIVFARBE = () => new THREE.Color(css("--mess-aktiv") || "#d9771f");
const ACHSE_CAD = { x: new THREE.Vector3(1, 0, 0), y: new THREE.Vector3(0, 1, 0), z: new THREE.Vector3(0, 0, 1) };
const TYPEN = {
  direkt: { kurz: "", name: "Abstand", taste: "1" },
  x: { kurz: "ΔX", name: "Länge X", taste: "2" },
  y: { kurz: "ΔY", name: "Breite Y", taste: "3" },
  z: { kurz: "ΔZ", name: "Höhe Z", taste: "4" },
};
const bem = new THREE.Group();
wurzel.add(bem);

const markerGeo = new THREE.SphereGeometry(1, 16, 12);
const pfeilGeo = new THREE.ConeGeometry(1, 1, 16);
pfeilGeo.translate(0, -0.5, 0);            // Spitze im Ursprung, Kegel zeigt nach +Y
function ueberAllem(mat, ordnung, obj) { mat.depthTest = false; mat.transparent = true; obj.renderOrder = ordnung; return obj; }
function marker(eltern = scene) {
  const mat = new THREE.MeshBasicMaterial({ color: MESSFARBE() });
  const m = ueberAllem(mat, 12, new THREE.Mesh(markerGeo, mat));
  eltern.add(m);
  return m;
}
function linie(eltern = scene, deckkraft = 1) {
  const g = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
  const mat = new THREE.LineBasicMaterial({ color: MESSFARBE(), opacity: deckkraft });
  const l = ueberAllem(mat, 11, new THREE.Line(g, mat));
  eltern.add(l);
  return l;
}
function pfeil(eltern) {
  const mat = new THREE.MeshBasicMaterial({ color: MESSFARBE() });
  const p = ueberAllem(mat, 12, new THREE.Mesh(pfeilGeo, mat));
  eltern.add(p);
  return p;
}
const hoverMarker = marker();
hoverMarker.visible = false;
const gummiband = linie();
gummiband.visible = false;

state.neuTyp = "direkt";
state.messAuswahl = null;
state.ziehen = null;

function weltPunkt(p) { return p.mesh.localToWorld(p.lokal.clone()); }
function cadPunkt(p) { return wurzel.worldToLocal(weltPunkt(p)); }
function zuWelt(v) { return wurzel.localToWorld(v.clone()); }
function skala(cad) { return camera.position.distanceTo(zuWelt(cad)) * 0.0065; }

/* Messwert: immer aus den zusammengebauten Punkten */
function messDelta(m) { return m.b.lokal.clone().sub(m.a.lokal); }
function messWert(m) {
  const d = messDelta(m);
  return m.typ === "direkt" ? d.length() : Math.abs(d.dot(ACHSE_CAD[m.typ]));
}
function richtung(m, A, B) {
  if (m.typ !== "direkt") return ACHSE_CAD[m.typ].clone();
  const d = B.clone().sub(A);
  return d.lengthSq() > 1e-12 ? d.normalize() : new THREE.Vector3(1, 0, 0);
}

/* Automatischer Abstand der Maßlinie: vom Modell weg, bei Achsmaßen so weit, dass beide Punkte frei liegen. */
function cadMitte() { return wurzel.worldToLocal(state.box.getCenter(new THREE.Vector3())); }
function autoAbstand(m) {
  const A = cadPunkt(m.a), B = cadPunkt(m.b), u = richtung(m, A, B);
  const diag = state.box.getSize(new THREE.Vector3()).length();
  const k = Math.max(diag * 0.045, A.distanceTo(B) * 0.12);
  const M = A.clone().add(B).multiplyScalar(0.5), weg = M.clone().sub(cadMitte());
  if (m.typ === "direkt") {
    let n = weg.clone().sub(u.clone().multiplyScalar(weg.dot(u)));
    if (n.lengthSq() < 1e-6) n = new THREE.Vector3(0, 0, 1).sub(u.clone().multiplyScalar(u.z));
    if (n.lengthSq() < 1e-6) n = new THREE.Vector3(0, 1, 0).sub(u.clone().multiplyScalar(u.y));
    return n.normalize().multiplyScalar(k);
  }
  const andere = ["x", "y", "z"].filter((a) => a !== m.typ).flatMap((a) => [ACHSE_CAD[a].clone(), ACHSE_CAD[a].clone().negate()]);
  const e = andere.reduce((best, c) => (c.dot(weg) > best.dot(weg) ? c : best));
  return e.multiplyScalar(Math.max(e.dot(A), e.dot(B)) - e.dot(A) + k);
}

function messenAn(an) {
  state.messen = an;
  $("#t-messen").setAttribute("aria-pressed", String(an));
  stage.classList.toggle("messen", an);
  $("#hint").hidden = !an;
  $("#mess-typ").hidden = !an;
  hinweis();
  if (!an) { abbrechen(); hoverMarker.visible = false; }
  else zeigeTab("messen");
}
function hinweis(text) {
  if (!state.messen) return;
  $("#hint").textContent = text || (state.offen ? "Zweiten Punkt antippen" : "Ersten Punkt antippen");
}
function abbrechen() {
  if (state.offen) { scene.remove(state.offen.m); state.offen = null; }
  gummiband.visible = false;
  hinweis();
}
$("#t-messen").addEventListener("click", () => messenAn(!state.messen));
function setzeNeuTyp(typ) {
  state.neuTyp = typ;
  document.querySelectorAll("#mess-typ button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.typ === typ)));
}
$("#mess-typ").addEventListener("click", (e) => { const b = e.target.closest("button[data-typ]"); if (b) setzeNeuTyp(b.dataset.typ); });

function punktSetzen(p) {
  if (!state.offen) {
    state.offen = { p, m: marker() };
    hinweis();
    return;
  }
  const m = neueMessung({ a: state.offen.p, b: p, typ: state.neuTyp });
  scene.remove(state.offen.m);
  state.offen = null;
  gummiband.visible = false;
  hinweis();
  waehleMessung(m);
  speichern();
}

function neueMessung({ a, b, typ = "direkt", name = "", off = null, nr = null }) {
  const g = new THREE.Group();
  bem.add(g);
  const label = document.createElement("div");
  label.className = "mlabel";
  label.tabIndex = 0;
  $("#labels").appendChild(label);
  const m = {
    nr: nr ?? (Math.max(0, ...state.messungen.map((x) => x.nr)) + 1), name, typ, a, b, g, label,
    off: off ? new THREE.Vector3(...off) : null, offAuto: !off,
    ma: marker(g), mb: marker(g), haupt: linie(g), h1: linie(g, 0.55), h2: linie(g, 0.55), p1: pfeil(g), p2: pfeil(g),
  };
  if (m.offAuto) m.off = autoAbstand(m);
  label.addEventListener("pointerdown", (e) => labelZiehenStart(e, m));
  label.addEventListener("dblclick", () => { waehleMessung(m); zeigeTab("messen"); document.querySelector(`#messungen li[data-nr="${m.nr}"] .name`)?.focus(); });
  label.addEventListener("keydown", (e) => { if (e.key === "Enter") waehleMessung(m); });
  state.messungen.push(m);
  messListe();
  return m;
}

function faerbeMessung(m) {
  const c = m === state.messAuswahl ? AKTIVFARBE() : MESSFARBE();
  [m.ma, m.mb, m.haupt, m.h1, m.h2, m.p1, m.p2].forEach((o) => o.material.color.copy(c));
  m.label.classList.toggle("aktiv", m === state.messAuswahl);
}
function waehleMessung(m) {
  state.messAuswahl = m;
  state.messungen.forEach(faerbeMessung);
  document.querySelectorAll("#messungen li").forEach((li) => li.classList.toggle("aktiv", m && li.dataset.nr === String(m.nr)));
}

function messText(m) {
  const n = state.info.massstab, L = messWert(m);
  return { modell: `${fmt(L)} mm`, original: `${fmt(L * n, 0)} mm Original` };
}
function labelText(m) {
  const t = messText(m), kurz = TYPEN[m.typ].kurz;
  m.label.innerHTML = `${m.name ? `<em>${esc(m.name)}</em>` : ""}${kurz ? `<b>${kurz}</b> ` : ""}${t.modell}<small>${t.original}</small>`;
  m.label.setAttribute("aria-label", `${m.name || `Messung ${m.nr}`}: ${TYPEN[m.typ].name} ${t.modell}, ${t.original}`);
}

function messListe() {
  const ol = $("#messungen");
  ol.innerHTML = "";
  const n = state.info.massstab;
  state.messungen.forEach((m) => {
    labelText(m);
    const t = messText(m), d = messDelta(m);
    const li = document.createElement("li");
    li.dataset.nr = m.nr;
    li.classList.toggle("aktiv", m === state.messAuswahl);
    li.innerHTML = `
      <div class="kopf"><span class="nr">${m.nr}</span><input class="name" type="text" value="${esc(m.name)}" placeholder="Messung ${m.nr}" aria-label="Name der Messung ${m.nr}"></div>
      <button type="button" class="weg" aria-label="Messung ${m.nr} löschen">Löschen</button>
      <div class="werte"><span class="wert">${t.modell}</span> <span class="orig">${t.original}</span></div>
      <div class="seg typ" role="group" aria-label="Messart">${Object.entries(TYPEN).map(([k, v]) =>
        `<button type="button" data-typ="${k}" aria-pressed="${k === m.typ}">${v.name}</button>`).join("")}</div>
      <div class="achsen">ΔX ${fmt(Math.abs(d.x))} · ΔY ${fmt(Math.abs(d.y))} · ΔZ ${fmt(Math.abs(d.z))} · direkt ${fmt(d.length())} mm<br>
        Original ΔX ${fmt(Math.abs(d.x) * n, 0)} · ΔY ${fmt(Math.abs(d.y) * n, 0)} · ΔZ ${fmt(Math.abs(d.z) * n, 0)} · direkt ${fmt(d.length() * n, 0)} mm</div>
      <div class="aktionen">
        <button type="button" class="link" data-a="seite">Maßlinie auf andere Seite</button>
        <button type="button" class="link" data-a="auto">Abstand zurücksetzen</button>
      </div>`;
    li.addEventListener("click", (e) => { if (!e.target.closest("input")) waehleMessung(m); });
    li.querySelector(".weg").addEventListener("click", (e) => { e.stopPropagation(); loeschen(m); });
    const inp = li.querySelector(".name");
    inp.addEventListener("focus", () => waehleMessung(m));
    inp.addEventListener("input", () => { m.name = inp.value.trim(); labelText(m); speichern(); });
    inp.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === "Escape") inp.blur(); });
    li.querySelector(".typ").addEventListener("click", (e) => {
      const b = e.target.closest("button[data-typ]"); if (b) setzeTyp(m, b.dataset.typ);
    });
    li.querySelector('[data-a="seite"]').addEventListener("click", () => { m.off.negate(); m.offAuto = false; speichern(); });
    li.querySelector('[data-a="auto"]').addEventListener("click", () => { m.offAuto = true; m.off = autoAbstand(m); speichern(); });
    ol.appendChild(li);
  });
  $("#mess-zahl").textContent = state.messungen.length;
  $("#mess-leer").hidden = state.messungen.length > 0;
  $("#mess-loeschen").hidden = state.messungen.length === 0;
}
function setzeTyp(m, typ) {
  m.typ = typ;
  if (m.offAuto) m.off = autoAbstand(m);
  messListe();
  waehleMessung(m);
  speichern();
}
function loeschen(m) {
  bem.remove(m.g);
  m.label.remove();
  state.messungen = state.messungen.filter((x) => x !== m);
  if (state.messAuswahl === m) state.messAuswahl = null;
  messListe();
  speichern();
}
$("#mess-loeschen").addEventListener("click", () => [...state.messungen].forEach(loeschen));

/* Speichern im Browser (nur Komfort, darf fehlen) */
const speicherSchluessel = () => `modellwerkstatt:messungen:${state.info?.id || state.basis}`;
function punktDaten(p) { return { teil: p.mesh.userData.teil.id, mat: p.mesh.material.userData.name, lokal: p.lokal.toArray() }; }
function speichern() {
  try {
    localStorage.setItem(speicherSchluessel(), JSON.stringify(state.messungen.map((m) => ({
      nr: m.nr, name: m.name, typ: m.typ, a: punktDaten(m.a), b: punktDaten(m.b), off: m.offAuto ? null : m.off.toArray(),
    }))));
  } catch { /* privates Fenster o. ä. */ }
}
function punktAus(d) {
  const mesh = state.teile.get(d.teil)?.meshes.find((x) => x.material.userData.name === d.mat);
  return mesh ? { mesh, lokal: new THREE.Vector3(...d.lokal), rast: true } : null;
}
function messungenLaden() {
  let liste = [];
  try { liste = JSON.parse(localStorage.getItem(speicherSchluessel()) || "[]"); } catch { liste = []; }
  for (const d of Array.isArray(liste) ? liste : []) {
    const a = punktAus(d.a || {}), b = punktAus(d.b || {});
    if (a && b && TYPEN[d.typ]) neueMessung({ a, b, typ: d.typ, name: d.name || "", off: d.off, nr: d.nr });
  }
}

/* ---------------- Picking ---------------- */
const ray = new THREE.Raycaster();
const maus = new THREE.Vector2();
function strahl(ev) {
  const r = renderer.domElement.getBoundingClientRect();
  maus.set(((ev.clientX - r.left) / r.width) * 2 - 1, -((ev.clientY - r.top) / r.height) * 2 + 1);
  ray.setFromCamera(maus, camera);
}
function treffer(ev) {
  strahl(ev);
  const sichtbar = [...state.teile.values()].filter((e) => e.gruppe.visible).flatMap((e) => e.meshes)
    .filter((m) => m.material.userData.name !== "glas");
  const hits = ray.intersectObjects(sichtbar, false);
  return hits.find((h) => !state.schnitt || schnittEbene.distanceToPoint(h.point) >= 0) || null;
}
function aufBildschirm(v) {
  const r = renderer.domElement.getBoundingClientRect();
  const p = v.clone().project(camera);
  return new THREE.Vector2((p.x + 1) / 2 * r.width + r.left, (1 - p.y) / 2 * r.height + r.top);
}
/** Messpunkt aus Treffer; rastet auf Eckpunkte ein (12 px). */
function messPunkt(ev, hit) {
  const mesh = hit.object, pos = mesh.geometry.getAttribute("position");
  let best = null, bestD = 12;
  const maus2 = new THREE.Vector2(ev.clientX, ev.clientY);
  for (const i of [hit.face.a, hit.face.b, hit.face.c]) {
    const lokal = new THREE.Vector3().fromBufferAttribute(pos, i);
    const d = aufBildschirm(mesh.localToWorld(lokal.clone())).distanceTo(maus2);
    if (d < bestD) { bestD = d; best = lokal; }
  }
  const lokal = best || mesh.worldToLocal(hit.point.clone());
  return { mesh, lokal, rast: !!best };
}

/* Ziehen: Endpunkt einer gewählten Messung (auf dem Modell neu setzen) oder Beschriftung (Abstand der Maßlinie). */
function griffUnterMaus(ev) {
  const m = state.messAuswahl;
  if (!m) return null;
  const p = new THREE.Vector2(ev.clientX, ev.clientY);
  let best = null, bestD = 14;
  for (const k of ["a", "b"]) {
    const d = aufBildschirm(weltPunkt(m[k])).distanceTo(p);
    if (d < bestD) { bestD = d; best = k; }
  }
  return best ? { m, k: best } : null;
}
stage.addEventListener("pointerdown", (e) => {
  if (e.button !== 0 || e.target !== renderer.domElement || !state.info) return;
  const g = griffUnterMaus(e);
  if (!g) return;
  controls.enabled = false;                       // laeuft in der Capture-Phase vor OrbitControls
  state.ziehen = { art: "punkt", ...g, alt: g.m[g.k] };
  renderer.domElement.setPointerCapture(e.pointerId);
  stage.classList.add("zieht");
}, { capture: true });

function labelZiehenStart(e, m) {
  if (e.button !== 0) return;
  e.preventDefault();
  waehleMessung(m);
  const r = m.label.getBoundingClientRect();
  state.ziehen = { art: "label", m, dx: e.clientX - (r.left + r.width / 2), dy: e.clientY - (r.top + r.height / 2), x0: e.clientX, y0: e.clientY, bewegt: false };
  m.label.setPointerCapture(e.pointerId);
  controls.enabled = false;
  stage.classList.add("zieht");
  const move = (ev) => {
    const z = state.ziehen; if (!z) return;
    if (Math.hypot(ev.clientX - z.x0, ev.clientY - z.y0) > 3) z.bewegt = true;
    if (z.bewegt) labelZiehen(ev, z);
  };
  const up = () => {
    m.label.removeEventListener("pointermove", move);
    m.label.removeEventListener("pointerup", up);
    m.label.removeEventListener("pointercancel", up);
    if (state.ziehen?.bewegt) speichern();
    state.ziehen = null; controls.enabled = true; stage.classList.remove("zieht");
  };
  m.label.addEventListener("pointermove", move);
  m.label.addEventListener("pointerup", up);
  m.label.addEventListener("pointercancel", up);
}
function labelZiehen(ev, z) {
  const m = z.m, A = cadPunkt(m.a), B = cadPunkt(m.b), u = richtung(m, A, B);
  const mitte = A.clone().add(m.off).add(u.clone().multiplyScalar(B.clone().sub(A).dot(u) / 2));
  strahl({ clientX: ev.clientX - z.dx, clientY: ev.clientY - z.dy });
  const n = camera.getWorldDirection(new THREE.Vector3());
  const ebene = new THREE.Plane().setFromNormalAndCoplanarPoint(n, zuWelt(mitte));
  const hw = ray.ray.intersectPlane(ebene, new THREE.Vector3());
  if (!hw) return;
  const o = wurzel.worldToLocal(hw).sub(A);
  o.sub(u.clone().multiplyScalar(o.dot(u)));
  m.off.copy(o);
  m.offAuto = false;
}

let down = null;
renderer.domElement.addEventListener("pointerdown", (e) => { down = { x: e.clientX, y: e.clientY }; });
renderer.domElement.addEventListener("pointermove", (e) => {
  if (!state.info || druck.an) return;
  const z = state.ziehen;
  if (z?.art === "punkt") {
    const hit = treffer(e);
    if (hit) {
      z.m[z.k] = messPunkt(e, hit);
      if (z.m.offAuto) z.m.off = autoAbstand(z.m);
      labelText(z.m);
      state.hover = z.m[z.k];
    }
    return;
  }
  if (state.messen) {
    const hit = treffer(e);
    state.hover = hit ? messPunkt(e, hit) : null;
    if (state.offen && state.hover) {
      const L = state.hover.lokal.clone().sub(state.offen.p.lokal).length(), n = state.info.massstab;
      hinweis(`Zweiten Punkt antippen · ${fmt(L)} mm · ${fmt(L * n, 0)} mm Original`);
    }
  } else {
    stage.classList.toggle("griff", !!griffUnterMaus(e));
  }
});
renderer.domElement.addEventListener("pointerup", (e) => {
  const z = state.ziehen;
  if (z?.art === "punkt") {
    state.ziehen = null; controls.enabled = true; stage.classList.remove("zieht");
    state.hover = null;
    messListe(); waehleMessung(z.m); speichern();
    return;
  }
  if (!down || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 5 || !state.info || druck.an) return;
  const hit = treffer(e);
  if (state.messen) {
    if (hit) punktSetzen(messPunkt(e, hit));
  } else {
    if (state.messAuswahl) waehleMessung(null);
    waehle(hit ? hit.object.userData.teil.id : null);
  }
});
window.addEventListener("keydown", (e) => {
  if (e.target.closest("input, select, textarea")) return;
  const typ = Object.keys(TYPEN).find((k) => TYPEN[k].taste === e.key);
  if (typ) {
    if (state.messen && !state.messAuswahl) setzeNeuTyp(typ);
    else if (state.messAuswahl) setzeTyp(state.messAuswahl, typ);
    else if (state.messen) setzeNeuTyp(typ);
    return;
  }
  if (e.key === "d" || e.key === "D") druckAn(!druck.an);
  else if (druck.an) { if (e.key === "Escape") druckAn(false); }
  else if (e.key === "m" || e.key === "M") messenAn(!state.messen);
  else if (e.key === "s" || e.key === "S") schnittAn(!state.schnitt);
  else if (e.key === "Escape") {
    if (state.ziehen?.art === "punkt") { const z = state.ziehen; z.m[z.k] = z.alt; state.ziehen = null; controls.enabled = true; stage.classList.remove("zieht"); messListe(); }
    else if (state.offen) abbrechen();
    else if (state.messAuswahl) waehleMessung(null);
    else if (state.messen) messenAn(false);
    else waehle(null);
  }
  else if ((e.key === "Delete" || e.key === "Backspace") && state.messungen.length) loeschen(state.messAuswahl || state.messungen.at(-1));
});

/* ---------------- Druckansicht ----------------
 * Zeigt die Druckdatei eines Teils so, wie sie aufs Bett kommt: Unterseite auf z = 0, Einzelteile nebeneinander.
 * Eigene Gruppe im CAD-System (z oben), das Modell ist solange ausgeblendet. Überhänge > 45° werden rot eingefärbt.
 */
const BETTEN = { fdm: { x: 220, y: 220 }, gross: { x: 300, y: 300 }, resin: { x: 218, y: 123 } };
const UEBERHANG_COS = Math.cos(THREE.MathUtils.degToRad(45));
const druck = {
  an: false, teil: null, bett: "fdm", ueberhang: true, cache: new Map(), mesh: null, bettObj: null,
  modellBox: null, rasterWar: true, gruppe: new THREE.Group(), laden: 0,
};
druck.gruppe.rotation.x = -Math.PI / 2;
druck.gruppe.visible = false;
scene.add(druck.gruppe);

/* Farben je Dreieck: Überhang, wenn die Normale steiler als 45° nach unten zeigt und das Dreieck nicht auf dem Bett liegt */
function druckFarben(geo) {
  const pos = geo.getAttribute("position"), n = pos.count;
  const basis = new THREE.Color(css("--druck")), rot = new THREE.Color(css("--ueberhang"));
  const farben = new Float32Array(n * 3);
  const a = new THREE.Vector3(), b = new THREE.Vector3(), c = new THREE.Vector3();
  const ab = new THREE.Vector3(), ac = new THREE.Vector3(), nrm = new THREE.Vector3();
  let flaecheU = 0, flaeche = 0;
  for (let i = 0; i + 2 < n; i += 3) {
    a.fromBufferAttribute(pos, i); b.fromBufferAttribute(pos, i + 1); c.fromBufferAttribute(pos, i + 2);
    nrm.crossVectors(ab.subVectors(b, a), ac.subVectors(c, a));
    const f = nrm.length() / 2;
    if (f > 0) nrm.divideScalar(f * 2);
    const ueber = nrm.z < -UEBERHANG_COS && Math.min(a.z, b.z, c.z) > 0.2;
    flaeche += f; if (ueber) flaecheU += f;
    const col = ueber ? rot : basis;
    for (let k = 0; k < 3; k++) { farben[(i + k) * 3] = col.r; farben[(i + k) * 3 + 1] = col.g; farben[(i + k) * 3 + 2] = col.b; }
  }
  geo.setAttribute("color", new THREE.BufferAttribute(farben, 3));
  return flaeche ? flaecheU / flaeche : 0;
}

function druckMaterial() {
  return new THREE.MeshStandardMaterial({
    color: druck.ueberhang ? 0xffffff : new THREE.Color(css("--druck")),
    vertexColors: druck.ueberhang, roughness: 0.7, metalness: 0.0,
    emissive: 0x2a2a2a,                               // Unterseiten nicht ganz schwarz
  });
}

/* Druckbett: Platte, 10-mm-Raster und Rand, mittig unter dem Belegungsfeld */
function baueBett(mitte) {
  if (druck.bettObj) {
    druck.gruppe.remove(druck.bettObj);
    druck.bettObj.traverse((o) => { o.geometry?.dispose(); o.material?.dispose(); });
  }
  const { x: bx, y: by } = BETTEN[druck.bett];
  const g = new THREE.Group();
  const x0 = Math.round(mitte.x - bx / 2), y0 = Math.round(mitte.y - by / 2);
  // nur von oben sichtbar, damit man von unten die Ueberhaenge sieht
  const platte = new THREE.Mesh(new THREE.PlaneGeometry(bx, by),
    new THREE.MeshStandardMaterial({ color: new THREE.Color(css("--bett")), roughness: 0.9 }));
  platte.position.set(x0 + bx / 2, y0 + by / 2, -0.05);
  g.add(platte);
  const pkt = [];
  for (let x = 0; x <= bx; x += 10) pkt.push(x0 + x, y0, 0, x0 + x, y0 + by, 0);
  for (let y = 0; y <= by; y += 10) pkt.push(x0, y0 + y, 0, x0 + bx, y0 + y, 0);
  const lg = new THREE.BufferGeometry();
  lg.setAttribute("position", new THREE.Float32BufferAttribute(pkt, 3));
  g.add(new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: new THREE.Color(css("--bett-linie")) })));
  const rand = new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(x0, y0, 0.05), new THREE.Vector3(x0 + bx, y0, 0.05),
    new THREE.Vector3(x0 + bx, y0 + by, 0.05), new THREE.Vector3(x0, y0 + by, 0.05)]);
  g.add(new THREE.LineLoop(rand, new THREE.LineBasicMaterial({ color: new THREE.Color(css("--accent")) })));
  druck.gruppe.add(g);
  druck.bettObj = g;
}

async function ladeDruck(id) {
  if (druck.cache.has(id)) return druck.cache.get(id);
  const t = state.teile.get(id).teil;
  const v = state.info.build ? `?v=${state.info.build}` : "";
  const geo = await new STLLoader().loadAsync(state.basis + t.druck + v);
  geo.computeVertexNormals();
  geo.computeBoundingBox();
  const eintrag = { geo, anteil: druckFarben(geo) };
  druck.cache.set(id, eintrag);
  return eintrag;
}

function passt(m, bett) {
  const [a, b] = m;
  return (a <= bett.x && b <= bett.y) || (a <= bett.y && b <= bett.x);
}

function druckInfo(teil, eintrag) {
  const bett = BETTEN[druck.bett];
  const bb = eintrag.geo.boundingBox, feld = [bb.max.x - bb.min.x, bb.max.y - bb.min.y, bb.max.z - bb.min.z];
  const pr = teil.druck_pruefung || {};
  const koerper = pr.koerper || [];
  const zuGross = koerper.filter((k) => !passt(k.masse_mm, bett));
  const groesst = koerper.reduce((m, k) => (!m || k.volumen_mm3 > m.volumen_mm3 ? k : m), null);
  const wand = koerper.map((k) => k.wand_min).filter((w) => w != null);
  const n = teil.druck_koerper || koerper.length || 1;
  let status, warn = false;
  if (zuGross.length) {
    warn = true;
    status = `${zuGross.length === 1 ? "Ein Druckteil ist" : `${zuGross.length} Druckteile sind`} größer als das Bett. Im Slicer teilen oder ein größeres Bett wählen.`;
  } else if (passt(feld, bett)) status = n === 1 ? "Passt aufs Bett." : `Alle ${n} Druckteile passen zusammen aufs Bett.`;
  else status = "Jedes Druckteil passt aufs Bett, alle zusammen nicht: im Slicer auf mehrere Drucke verteilen.";
  if (pr.dicht === false) { warn = true; status += " Achtung: Datei nicht dicht."; }
  const hinweise = (pr.hinweise || []).filter((h) => !/^Passung|eingeschlossene|Splitter/.test(h));
  const passung = (pr.hinweise || []).filter((h) => /^Passung/.test(h)).length;
  $("#druck-info").innerHTML = `
    <p class="status${warn ? " warn" : ""}">${status}</p>
    <dl>
      <dt>Druckteile</dt><dd>${n}</dd>
      <dt>Belegt</dt><dd>${feld.slice(0, 2).map((v) => fmt(v, 0)).join(" × ")} mm, Höhe ${fmt(feld[2], 0)} mm</dd>
      ${groesst ? `<dt>Größtes Teil</dt><dd>${groesst.masse_mm.map((v) => fmt(v, 0)).join(" × ")} mm</dd>` : ""}
      ${koerper.length ? `<dt>Volumen</dt><dd>${fmt(koerper.reduce((s, k) => s + k.volumen_mm3, 0) / 1000, 1)} cm³</dd>` : ""}
      ${wand.length ? `<dt>Dünnste Wand</dt><dd>${fmt(Math.min(...wand), 2)} mm (Stichprobe)</dd>` : ""}
      <dt>Überhang</dt><dd>${fmt(eintrag.anteil * 100, 0)} % der Fläche</dd>
    </dl>
    ${hinweise.length ? `<h4>Hinweise</h4><ul>${hinweise.slice(0, 6).map((h) => `<li>${esc(h)}</li>`).join("")}${hinweise.length > 6 ? `<li>… ${hinweise.length - 6} weitere im Prüfbericht</li>` : ""}</ul>` : ""}
    ${passung ? `<p class="note">Zu ${passung === 1 ? "einem Nachbarteil" : `${passung} Nachbarteilen`} ist das Teil bündig gekürzt, damit beide sauber aneinander liegen.</p>` : ""}
    <a class="btn" href="${state.basis + teil.druck}" download>Druckdatei · ${fmt(teil.druck_mb)} MB</a>`;
}

function druckRahmen() {
  druck.gruppe.updateMatrixWorld(true);
  state.box.setFromObject(druck.gruppe);
}

async function zeigeDruck(id) {
  const teil = state.teile.get(id)?.teil;
  if (!teil?.druck) return;
  druck.teil = id;
  $("#druck-teil").value = id;
  const nr = ++druck.laden;
  $("#druck-info").innerHTML = `<p class="note">Lade Druckdatei · ${fmt(teil.druck_mb)} MB …</p>`;
  let eintrag;
  try { eintrag = await ladeDruck(id); } catch (err) {
    console.error(err);
    $("#druck-info").innerHTML = `<p class="status warn">Druckdatei konnte nicht geladen werden.</p>`;
    return;
  }
  if (nr !== druck.laden || !druck.an) return;
  if (druck.mesh) { druck.gruppe.remove(druck.mesh); druck.mesh.material.dispose(); }
  druck.mesh = new THREE.Mesh(eintrag.geo, druckMaterial());
  druck.gruppe.add(druck.mesh);
  baueBett(eintrag.geo.boundingBox.getCenter(new THREE.Vector3()));
  druckRahmen();
  druckInfo(teil, eintrag);
  ansicht("iso");
}

function druckAn(an, id) {
  if (an === druck.an) { if (an && id) zeigeDruck(id); return; }
  druck.an = an;
  $("#t-druck").setAttribute("aria-pressed", String(an));
  $("#druck-panel").hidden = !an;
  stage.classList.toggle("druck", an);
  $("#raster-note").textContent = an ? "Bettraster 10 mm · Maße in Modell-mm"
    : `Raster 10 mm = ${10 * state.info.massstab} mm Original`;
  if (an) {
    if (state.messen) messenAn(false);
    if (state.schnitt) schnittAn(false);
    druck.modellBox = state.box.clone();
    druck.rasterWar = raster ? raster.visible : true;
    if (raster) raster.visible = false;
    wurzel.visible = false;
    druck.gruppe.visible = true;
    const sel = $("#druck-teil");
    if (!sel.options.length) state.info.teile.filter((t) => t.druck).forEach((t) => sel.add(new Option(t.name, t.id)));
    const gewaehlt = state.auswahl && state.teile.get(state.auswahl).teil.druck ? state.auswahl : null;
    zeigeDruck(id || gewaehlt || druck.teil || sel.options[0].value);
  } else {
    druck.laden++;
    wurzel.visible = true;
    druck.gruppe.visible = false;
    if (raster) raster.visible = druck.rasterWar;
    if (druck.modellBox) state.box.copy(druck.modellBox);
    ansicht("iso");
  }
}
$("#t-druck").addEventListener("click", () => druckAn(!druck.an));
$("#druck-teil").addEventListener("change", (e) => zeigeDruck(e.target.value));
$("#druck-bett").addEventListener("click", (e) => {
  const b = e.target.closest("button[data-bett]"); if (!b) return;
  druck.bett = b.dataset.bett;
  document.querySelectorAll("#druck-bett button").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
  const eintrag = druck.teil && druck.cache.get(druck.teil);
  if (eintrag && druck.mesh) {
    baueBett(eintrag.geo.boundingBox.getCenter(new THREE.Vector3()));
    druckRahmen();
    druckInfo(state.teile.get(druck.teil).teil, eintrag);
  }
});
$("#druck-ueber").addEventListener("change", (e) => {
  druck.ueberhang = e.target.checked;
  if (druck.mesh) { druck.mesh.material.dispose(); druck.mesh.material = druckMaterial(); }
});
window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
  druck.cache.forEach((e) => { e.anteil = druckFarben(e.geo); });
  if (druck.an && druck.teil) zeigeDruck(druck.teil);
});

/* ---------------- Schleife ---------------- */
function groesse(m, weltPos, f = 1) {
  m.scale.setScalar(camera.position.distanceTo(weltPos) * 0.0065 * f);
}
function setzeLinie(l, a, b) {
  const p = l.geometry.getAttribute("position");
  p.setXYZ(0, a.x, a.y, a.z); p.setXYZ(1, b.x, b.y, b.z); p.needsUpdate = true;
  l.geometry.computeBoundingSphere();
}
const Y_ACHSE = new THREE.Vector3(0, 1, 0);
function setzePfeil(p, spitze, dir, s) {
  p.position.copy(spitze);
  p.quaternion.setFromUnitVectors(Y_ACHSE, dir);   // Kegel zeigt in Richtung dir, Spitze auf `spitze`
  p.scale.set(s * 1.0, s * 3.4, s * 1.0);
}
function resize() {
  const w = stage.clientWidth, h = stage.clientHeight;
  renderer.setSize(w, h, false);
  camera.aspect = w / h; camera.updateProjectionMatrix();
}
new ResizeObserver(resize).observe(stage);

function zeichneMessung(m, r, sr) {
  const A = cadPunkt(m.a), B = cadPunkt(m.b), u = richtung(m, A, B);
  const s = B.clone().sub(A).dot(u);
  const o = m.off.clone().sub(u.clone().multiplyScalar(m.off.dot(u)));   // immer senkrecht zur Messrichtung
  const P1 = A.clone().add(o), P2 = P1.clone().add(u.clone().multiplyScalar(s));
  const mitte = P1.clone().add(P2).multiplyScalar(0.5);
  const g = skala(mitte), aktiv = m === state.messAuswahl;
  m.ma.position.copy(A); m.ma.scale.setScalar(skala(A) * (aktiv ? 1.5 : 0.8));
  m.mb.position.copy(B); m.mb.scale.setScalar(skala(B) * (aktiv ? 1.5 : 0.8));
  setzeLinie(m.haupt, P1, P2);
  for (const [l, von, bis] of [[m.h1, A, P1], [m.h2, B, P2]]) {
    const v = bis.clone().sub(von), len = v.length();
    l.visible = len > g * 2;
    if (!l.visible) continue;
    v.divideScalar(len);
    setzeLinie(l, von.clone().add(v.clone().multiplyScalar(g * 1.2)), bis.clone().add(v.clone().multiplyScalar(g * 2.2)));
  }
  // Pfeile: innen, oder bei kurzer Maßlinie von außen
  const kurz = aufBildschirm(zuWelt(P1)).distanceTo(aufBildschirm(zuWelt(P2))) < 34;
  const d12 = P2.clone().sub(P1);
  const dir = d12.lengthSq() > 1e-12 ? d12.normalize() : u.clone();
  setzePfeil(m.p1, P1, kurz ? dir : dir.clone().negate(), g);
  setzePfeil(m.p2, P2, kurz ? dir.clone().negate() : dir, g);
  const p = zuWelt(mitte).project(camera);
  const sichtbar = p.z < 1 && Math.abs(p.x) < 1.1 && Math.abs(p.y) < 1.1;
  m.label.style.display = sichtbar ? "" : "none";
  m.label.style.left = `${(p.x + 1) / 2 * r.width + r.left - sr.left}px`;
  m.label.style.top = `${(1 - p.y) / 2 * r.height + r.top - sr.top}px`;
}

function schleife(now) {
  requestAnimationFrame(schleife);
  if (flug) flug(now);
  controls.update();
  wurzel.updateMatrixWorld(true);
  // Hover und Gummiband
  if ((state.messen || state.ziehen?.art === "punkt") && state.hover) {
    const w = weltPunkt(state.hover);
    hoverMarker.position.copy(w); groesse(hoverMarker, w); hoverMarker.visible = true;
    hoverMarker.material.opacity = state.hover.rast ? 1 : 0.55;
    if (state.offen) { setzeLinie(gummiband, weltPunkt(state.offen.p), w); gummiband.visible = true; }
  } else { hoverMarker.visible = false; gummiband.visible = false; }
  if (state.offen) { const w = weltPunkt(state.offen.p); state.offen.m.position.copy(w); groesse(state.offen.m, w); }
  const r = renderer.domElement.getBoundingClientRect(), sr = stage.getBoundingClientRect();
  for (const m of state.messungen) zeichneMessung(m, r, sr);
  renderer.render(scene, camera);
}

resize();
requestAnimationFrame(schleife);
start().catch((err) => {
  console.error(err);
  $("#loading span").textContent = "Modell konnte nicht geladen werden.";
});
