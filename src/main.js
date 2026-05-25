import * as d3 from "d3";
import scrollama from "scrollama";
import "./styles.css";

import wavesData from "../data/processed/waves_by_batch.json";
import sectorData from "../data/processed/genai_cross_sector.json";
import outcomeData from "../data/processed/outcome_proxies.json";
import metadata from "../data/processed/metadata.json";

const chartEl = document.querySelector("#chart");
const chartTitle = document.querySelector("#chart-title");
const chartEyebrow = document.querySelector("#chart-eyebrow");
const sourceNote = document.querySelector("#source-note");
const steps = Array.from(document.querySelectorAll(".step"));
const modeInputs = Array.from(document.querySelectorAll('input[name="mode"]'));

const WAVES = wavesData.waves.filter((wave) => wave !== "Other");
const COLORS = new Map([
  ["Web / Social / UGC", "#875f76"],
  ["Mobile-Enabled Commerce / Marketplaces", "#b45f3a"],
  ["Fintech", "#346da8"],
  ["Crypto / Web3", "#8b7d33"],
  ["Generative AI / Agents", "#1d6f68"],
  ["Other", "#cfc8bc"],
]);

const SCENE_COPY = {
  stacked: ["Waves have come before", "Chapter 1"],
  "stacked-ai": ["Founder attention moves in waves", "Chapter 1"],
  durable: ["Commerce and fintech set the bar", "Chapter 2"],
  "durable-outcomes": ["Durability takes time to prove", "Chapter 2"],
  crypto: ["Loud is not always broad", "Chapter 3"],
  "crypto-trust": ["The cautionary wave", "Chapter 3"],
  indexed: ["This is the shift", "Chapter 4"],
  "indexed-annotated": ["The AI / agents curve pulls away", "Chapter 4"],
  sectors: ["Category and capability layer", "Chapter 4"],
  method: ["The signal lives between the reads", "Chapter 4"],
  fork: ["The outcome fork", "Chapter 5"],
  "fork-paths": ["Three possible futures", "Chapter 5"],
  call: ["The window is open", "Chapter 6"],
  "call-final": ["You are here", "Chapter 6"],
};

let state = {
  mode: "broad",
  scene: "stacked",
  width: 800,
  height: 560,
};
let activeStep = steps[0];
let scrollFrame = 0;

sourceNote.textContent = `Source: ${metadata.source.name}, ${metadata.source.included_companies.toLocaleString()} companies, ${metadata.source.included_batch_count} batches. Snapshot: ${new Date(metadata.source.snapshot_timestamp).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}.`;

const svg = d3.select(chartEl).append("svg").attr("aria-label", "YC founder wave chart");
const root = svg.append("g");

const fmtPct = d3.format(".1%");
const fmtPct0 = d3.format(".0%");
const fmtMult = (value) => `${d3.format(".1f")(value)}x`;

const rowsByMode = d3.group(wavesData.rows, (row) => row.mode);
const batches = wavesData.batches.slice().sort((a, b) => a.batch_order - b.batch_order);

function modeRows() {
  return rowsByMode.get(state.mode) ?? [];
}

function byBatchWave(rows) {
  return d3.rollup(
    rows,
    (values) => values[0],
    (row) => row.batch_order,
    (row) => row.wave,
  );
}

function getWaveSeries(wave, mode = state.mode) {
  return wavesData.rows
    .filter((row) => row.mode === mode && row.wave === wave)
    .sort((a, b) => a.batch_order - b.batch_order);
}

function getIndexedSeries(wave, mode = state.mode) {
  const series = getWaveSeries(wave, mode);
  const firstIndex = series.findIndex((row) => row.pct >= 0.02);
  if (firstIndex < 0) return [];
  const base = series[firstIndex].pct || 1;
  return series
    .slice(firstIndex)
    .map((row) => ({ ...row, indexed: row.pct / base, firstBatch: series[firstIndex].batch_code }));
}

function clear() {
  root.selectAll("*").remove();
}

function updateHeader() {
  const [title, eyebrow] = SCENE_COPY[state.scene] ?? SCENE_COPY.stacked;
  chartTitle.textContent = title;
  chartEyebrow.textContent = eyebrow;
}

function dimensions() {
  const rect = chartEl.getBoundingClientRect();
  const width = Math.max(320, rect.width);
  const height = Math.max(320, rect.height);
  state.width = width;
  state.height = height;
  svg.attr("viewBox", `0 0 ${width} ${height}`);
  return { width, height };
}

function margins(width) {
  return width < 560
    ? { top: 42, right: 24, bottom: 46, left: 46 }
    : { top: 58, right: 76, bottom: 56, left: 62 };
}

function axes(g, x, y, innerHeight, width, tickFormat = fmtPct0) {
  const xTicks = width < 560 ? batches.filter((_, i) => i % 8 === 0) : batches.filter((_, i) => i % 5 === 0);
  g.append("g")
    .attr("class", "grid")
    .call(d3.axisLeft(y).ticks(5).tickSize(-x.range()[1]).tickFormat(""))
    .call((selection) => selection.selectAll("line").attr("stroke-dasharray", "2 5"));
  g.append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(
      d3
        .axisBottom(x)
        .tickValues(xTicks.map((batch) => batch.batch_order))
        .tickFormat((order) => batches.find((batch) => batch.batch_order === order)?.batch_code ?? ""),
    )
    .call((selection) => selection.select(".domain").remove());
  g.append("g")
    .attr("class", "axis")
    .call(d3.axisLeft(y).ticks(5).tickFormat(tickFormat))
    .call((selection) => selection.select(".domain").remove());
}

function drawLegend(g, items, x, y, mutedSet = new Set()) {
  if (state.width < 560) return;
  const legend = g.append("g").attr("class", "legend").attr("transform", `translate(${x},${y})`);
  const row = legend
    .selectAll("g")
    .data(items)
    .join("g")
    .attr("transform", (_, i) => `translate(0,${i * 21})`);
  row
    .append("line")
    .attr("x1", 0)
    .attr("x2", 22)
    .attr("y1", 0)
    .attr("y2", 0)
    .attr("stroke", (d) => COLORS.get(d))
    .attr("stroke-width", 4)
    .attr("opacity", (d) => (mutedSet.has(d) ? 0.25 : 1));
  row
    .append("text")
    .attr("x", 30)
    .attr("y", 4)
    .attr("opacity", (d) => (mutedSet.has(d) ? 0.55 : 1))
    .text((d) => d.replace("Mobile-Enabled Commerce / Marketplaces", "Commerce / Marketplaces"));
}

function drawStacked() {
  clear();
  const { width, height } = dimensions();
  const margin = margins(width);
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  const g = root.append("g").attr("transform", `translate(${margin.left},${margin.top})`);
  const rows = modeRows();
  const lookup = byBatchWave(rows);
  const stackedRows = batches.map((batch) => {
    const row = { batch_order: batch.batch_order, batch_code: batch.batch_code };
    wavesData.waves.forEach((wave) => {
      row[wave] = lookup.get(batch.batch_order)?.get(wave)?.pct ?? 0;
    });
    return row;
  });

  const x = d3.scaleLinear().domain(d3.extent(batches, (d) => d.batch_order)).range([0, innerWidth]);
  const y = d3.scaleLinear().domain([0, 1]).range([innerHeight, 0]);
  const stack = d3.stack().keys(wavesData.waves);
  const area = d3
    .area()
    .x((d) => x(d.data.batch_order))
    .y0((d) => y(d[0]))
    .y1((d) => y(d[1]))
    .curve(d3.curveMonotoneX);

  g.selectAll("path.layer")
    .data(stack(stackedRows))
    .join("path")
    .attr("class", "layer")
    .attr("d", area)
    .attr("fill", (d) => COLORS.get(d.key))
    .attr("opacity", (d) => {
      if (state.scene === "stacked-ai" && d.key !== "Generative AI / Agents") return d.key === "Other" ? 0.26 : 0.4;
      return d.key === "Other" ? 0.45 : 0.78;
    });

  axes(g, x, y, innerHeight, width);
  g.append("text")
    .attr("class", "chart-subtitle")
    .attr("x", 0)
    .attr("y", -24)
    .text(`${state.mode === "broad" ? "Broad" : "Strict"} classification, share of each YC batch`);
  drawLegend(g, wavesData.waves, Math.max(6, innerWidth - 230), 4, state.scene === "stacked-ai" ? new Set(wavesData.waves.filter((w) => w !== "Generative AI / Agents")) : new Set());
}

function drawLines({ highlight = [], ceiling = false, outcomes = false, call = false } = {}) {
  clear();
  const { width, height } = dimensions();
  const margin = margins(width);
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  const g = root.append("g").attr("transform", `translate(${margin.left},${margin.top})`);
  const x = d3.scaleLinear().domain(d3.extent(batches, (d) => d.batch_order)).range([0, innerWidth]);
  const y = d3.scaleLinear().domain([0, 0.5]).nice().range([innerHeight, 0]);
  const line = d3
    .line()
    .x((d) => x(d.batch_order))
    .y((d) => y(d.pct))
    .curve(d3.curveMonotoneX);
  const muted = new Set(WAVES.filter((wave) => highlight.length && !highlight.includes(wave)));

  axes(g, x, y, innerHeight, width);
  WAVES.forEach((wave) => {
    const series = getWaveSeries(wave);
    g.append("path")
      .datum(series)
      .attr("fill", "none")
      .attr("stroke", COLORS.get(wave))
      .attr("stroke-width", highlight.includes(wave) ? 3.8 : 2)
      .attr("opacity", muted.has(wave) ? 0.2 : 0.9)
      .attr("d", line);
  });

  if (ceiling) {
    g.append("line")
      .attr("x1", 0)
      .attr("x2", innerWidth)
      .attr("y1", y(0.1))
      .attr("y2", y(0.1))
      .attr("stroke", "#686156")
      .attr("stroke-dasharray", "4 6");
    g.append("text")
      .attr("class", "annotation-label")
      .attr("x", innerWidth - 138)
      .attr("y", y(0.1) - 8)
      .text("10% ceiling");
  }

  if (outcomes) {
    drawOutcomeInset(g, innerWidth, innerHeight);
  }

  if (call) {
    const ai = getWaveSeries("Generative AI / Agents").at(-1);
    g.append("circle").attr("cx", x(ai.batch_order)).attr("cy", y(ai.pct)).attr("r", 6).attr("fill", COLORS.get(ai.wave));
    g.append("text")
      .attr("class", "annotation-label")
      .attr("x", Math.min(x(ai.batch_order) - 112, innerWidth - 160))
      .attr("y", y(ai.pct) - 14)
      .text("You are here");
  }

  const legendItems = highlight.length ? highlight : WAVES;
  drawLegend(g, legendItems, Math.max(6, innerWidth - 230), 4);
  g.append("text")
    .attr("class", "chart-subtitle")
    .attr("x", 0)
    .attr("y", -24)
    .text("Share of each YC batch");
}

function drawOutcomeInset(g, innerWidth, innerHeight) {
  const rows = outcomeData.rows
    .filter((row) => row.mode === state.mode && row.cohort_filter === "through_2020")
    .filter((row) => ["Mobile-Enabled Commerce / Marketplaces", "Fintech"].includes(row.wave));
  const x = d3.scaleLinear().domain([0, 0.07]).range([0, Math.min(220, innerWidth * 0.36)]);
  const inset = g.append("g").attr("transform", `translate(8,${innerHeight - 86})`);
  inset.append("text").attr("class", "annotation-note").attr("x", 0).attr("y", -12).text("Mature-cohort top-company rate");
  rows.forEach((row, i) => {
    inset
      .append("rect")
      .attr("x", 0)
      .attr("y", i * 28)
      .attr("height", 12)
      .attr("width", x(row.top_company_rate))
      .attr("fill", COLORS.get(row.wave));
    inset
      .append("text")
      .attr("class", "annotation-note")
      .attr("x", x(row.top_company_rate) + 8)
      .attr("y", i * 28 + 10)
      .text(`${row.wave.startsWith("Fintech") ? "Fintech" : "Commerce"} ${fmtPct(row.top_company_rate)}`);
  });
}

function drawIndexed() {
  clear();
  const { width, height } = dimensions();
  const isMobile = width < 560;
  const margin = margins(width);
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  const g = root.append("g").attr("transform", `translate(${margin.left},${margin.top})`);
  const indexed = WAVES.flatMap((wave) => getIndexedSeries(wave).map((row) => ({ ...row, wave })));
  const x = d3.scaleLinear().domain(d3.extent(batches, (d) => d.batch_order)).range([0, innerWidth]);
  const yMax = Math.max(5, d3.max(indexed, (d) => d.indexed) ?? 1);
  const y = d3.scaleLinear().domain([0, yMax * 1.08]).range([innerHeight, 0]);
  const line = d3
    .line()
    .defined((d) => Number.isFinite(d.indexed))
    .x((d) => x(d.batch_order))
    .y((d) => y(d.indexed))
    .curve(d3.curveMonotoneX);

  axes(g, x, y, innerHeight, width, (d) => `${d}x`);
  g.append("line")
    .attr("x1", 0)
    .attr("x2", innerWidth)
    .attr("y1", y(1))
    .attr("y2", y(1))
    .attr("stroke", "#6d665d")
    .attr("stroke-dasharray", "4 6")
    .attr("opacity", 0.75);

  WAVES.forEach((wave) => {
    const series = getIndexedSeries(wave);
    const isAi = wave === "Generative AI / Agents";
    const muted = state.scene !== "indexed" && !isAi;
    g.append("path")
      .datum(series)
      .attr("fill", "none")
      .attr("stroke", COLORS.get(wave))
      .attr("stroke-width", isAi ? 4.2 : 2)
      .attr("opacity", muted ? 0.2 : 0.74)
      .attr("d", line);
    if (series.length) {
      const first = series[0];
      g.append("circle")
        .attr("cx", x(first.batch_order))
        .attr("cy", y(1))
        .attr("r", isAi ? 4.5 : 3)
        .attr("fill", COLORS.get(wave))
        .attr("opacity", muted ? 0.25 : 0.78);
    }
  });

  const aiSeries = getIndexedSeries("Generative AI / Agents");
  const aiLast = aiSeries.at(-1);
  const aiRaw = getWaveSeries("Generative AI / Agents").at(-1);
  g.append("circle")
    .attr("cx", x(aiLast.batch_order))
    .attr("cy", y(aiLast.indexed))
    .attr("r", 7)
    .attr("fill", COLORS.get("Generative AI / Agents"));
  const calloutX = isMobile ? Math.max(0, innerWidth - 260) : Math.max(0, Math.min(x(aiLast.batch_order) - 210, innerWidth - 260));
  const calloutY = Math.max(isMobile ? 34 : 22, y(aiLast.indexed) - 16);
  g.append("text")
    .attr("class", "annotation-label")
    .attr("x", calloutX)
    .attr("y", calloutY)
    .text(isMobile ? `${fmtPct(aiRaw.pct)} of ${aiRaw.batch_code} matched GenAI` : `${fmtPct(aiRaw.pct)} of ${aiRaw.batch} matched GenAI / agents`);
  g.append("text")
    .attr("class", "annotation-note")
    .attr("x", calloutX)
    .attr("y", calloutY + 20)
    .text(isMobile ? `${fmtMult(aiLast.indexed)} since first >=2% batch` : `${fmtMult(aiLast.indexed)} from the first >=2% batch in ${state.mode} mode`);

  if (state.scene === "indexed-annotated" || state.scene === "method" || state.scene === "call-final") {
    const strictPeak = d3.max(getWaveSeries("Generative AI / Agents", "strict"), (d) => d.pct);
    g.append("g")
      .attr("class", "annotation")
      .attr("transform", `translate(${Math.max(0, innerWidth - 300)},${innerHeight - 86})`)
      .call((group) => {
        group.append("rect").attr("width", 280).attr("height", 70).attr("fill", "#fffdf8").attr("stroke", "#d4cec1");
        group.append("text").attr("class", "annotation-label").attr("x", 14).attr("y", 24).text("Strict read survives the check");
        group.append("text").attr("class", "annotation-note").attr("x", 14).attr("y", 47).text(`Strict peak: ${fmtPct(strictPeak)} in Winter 2023`);
      });
  }

  g.append("text")
    .attr("class", "chart-subtitle")
    .attr("x", 0)
    .attr("y", -24)
    .text(isMobile ? `Indexed growth from first >=2% batch (${state.mode})` : `Indexed from each wave's first batch at or above 2% (${state.mode})`);
}

function drawSectors() {
  clear();
  const { width, height } = dimensions();
  const margin = margins(width);
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  const g = root.append("g").attr("transform", `translate(${margin.left},${margin.top})`);
  const rows = sectorData.rows.slice(0, width < 560 ? 6 : 9);
  const y = d3.scaleBand().domain(rows.map((d) => d.sector)).range([0, innerHeight]).padding(0.28);
  const x = d3.scaleLinear().domain([0, 0.5]).range([0, innerWidth]);

  g.append("g")
    .attr("class", "grid")
    .call(d3.axisTop(x).ticks(width < 560 ? 3 : 5).tickSize(-innerHeight).tickFormat(fmtPct0))
    .call((selection) => selection.select(".domain").remove());
  const bar = g.selectAll("g.sector").data(rows).join("g").attr("class", "sector").attr("transform", (d) => `translate(0,${y(d.sector)})`);
  bar
    .append("rect")
    .attr("height", y.bandwidth())
    .attr("width", (d) => x(d.pct_of_genai_broad))
    .attr("fill", (d, i) => (i < 5 ? "#1d6f68" : "#a9b7af"))
    .attr("opacity", (d, i) => (i < 5 ? 0.9 : 0.55));
  bar
    .append("text")
    .attr("class", "annotation-label")
    .attr("x", 0)
    .attr("y", -6)
    .text((d) => d.sector.replace(" / Infrastructure", "").replace(" / Education", ""));
  bar
    .append("text")
    .attr("class", "annotation-note")
    .attr("x", (d) => Math.min(innerWidth - 44, x(d.pct_of_genai_broad) + 8))
    .attr("y", y.bandwidth() / 2 + 4)
    .text((d) => fmtPct(d.pct_of_genai_broad));

  g.append("text")
    .attr("class", "chart-subtitle")
    .attr("x", 0)
    .attr("y", -24)
    .text(width < 560 ? "Broad-mode GenAI background sectors" : "Broad-mode background sectors among GenAI / agents-classified companies");
}

function drawFork() {
  clear();
  const { width, height } = dimensions();
  const margin = margins(width);
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  const g = root.append("g").attr("transform", `translate(${margin.left},${margin.top})`);
  const rows = outcomeData.rows
    .filter((row) => row.mode === state.mode && row.cohort_filter === "through_2020")
    .filter((row) => row.wave !== "Other")
    .sort((a, b) => d3.descending(a.public_or_acquired_rate, b.public_or_acquired_rate));
  const isMobile = width < 560;
  const y = d3
    .scaleBand()
    .domain(rows.map((d) => d.wave))
    .range([isMobile ? 18 : 0, isMobile ? innerHeight * 0.86 : innerHeight * 0.58])
    .padding(isMobile ? 0.34 : 0.22);
  const x = d3.scaleLinear().domain([0, 0.32]).range([0, innerWidth]);

  g.append("text")
    .attr("class", "chart-subtitle")
    .attr("x", 0)
    .attr("y", -24)
    .text(isMobile ? "Mature cohorts through 2020 only" : "Outcome proxies are shown only for mature cohorts through 2020");
  const row = g.selectAll("g.proxy").data(rows).join("g").attr("class", "proxy").attr("transform", (d) => `translate(0,${y(d.wave)})`);
  row
    .append("rect")
    .attr("height", y.bandwidth())
    .attr("width", (d) => x(d.public_or_acquired_rate))
    .attr("fill", (d) => COLORS.get(d.wave))
    .attr("opacity", (d) => (d.wave === "Generative AI / Agents" ? 0.42 : 0.78));
  row
    .append("text")
    .attr("class", "annotation-label")
    .attr("x", 0)
    .attr("y", isMobile ? -4 : -6)
    .text((d) => shortWave(d.wave, isMobile));
  row
    .append("text")
    .attr("class", "annotation-note")
    .attr("x", (d) => (isMobile ? Math.min(innerWidth - 38, x(d.public_or_acquired_rate) + 7) : x(d.public_or_acquired_rate) + 8))
    .attr("y", y.bandwidth() / 2 + 4)
    .text((d) => (isMobile ? fmtPct(d.public_or_acquired_rate) : `${fmtPct(d.public_or_acquired_rate)} public/acquired`));

  if (isMobile) return;
  const cards = [
    ["Path A", "Fintech / commerce", "Broad formation becomes durable companies."],
    ["Path B", "Crypto", "A loud wave stays narrower than its footprint."],
    ["Path C", "Substrate", "AI becomes too normal to remain one label."],
  ];
  const cardY = innerHeight * 0.67;
  const cardW = (innerWidth - 24) / 3;
  const card = g.selectAll("g.path-card").data(cards).join("g").attr("transform", (_, i) => `translate(${i * (cardW + 12)},${cardY})`);
  card.append("rect").attr("width", cardW).attr("height", 104).attr("fill", "#fffdf8").attr("stroke", "#d4cec1");
  card.append("text").attr("class", "annotation-note").attr("x", 12).attr("y", 24).text((d) => d[0]);
  card.append("text").attr("class", "annotation-label").attr("x", 12).attr("y", 47).text((d) => d[1]);
  card
    .append("text")
    .attr("class", "annotation-note")
    .attr("x", 12)
    .attr("y", 72)
    .text((d) => d[2].slice(0, width < 560 ? 32 : 46));
}

function shortWave(wave, compact = false) {
  const labels = new Map([
    ["Web / Social / UGC", compact ? "Web / social" : "Web / Social / UGC"],
    ["Mobile-Enabled Commerce / Marketplaces", compact ? "Commerce" : "Commerce / Marketplaces"],
    ["Fintech", "Fintech"],
    ["Crypto / Web3", "Crypto / Web3"],
    ["Generative AI / Agents", compact ? "GenAI / agents" : "Generative AI / Agents"],
  ]);
  return labels.get(wave) ?? wave;
}

function render() {
  updateHeader();
  if (state.scene.startsWith("stacked")) drawStacked();
  else if (state.scene === "durable") drawLines({ highlight: ["Mobile-Enabled Commerce / Marketplaces", "Fintech"] });
  else if (state.scene === "durable-outcomes") drawLines({ highlight: ["Mobile-Enabled Commerce / Marketplaces", "Fintech"], outcomes: true });
  else if (state.scene.startsWith("crypto")) drawLines({ highlight: ["Crypto / Web3"], ceiling: true });
  else if (state.scene.startsWith("indexed") || state.scene === "method" || state.scene.startsWith("call")) drawIndexed();
  else if (state.scene === "sectors") drawSectors();
  else if (state.scene.startsWith("fork")) drawFork();
  else drawStacked();
}

function setActiveStep(element) {
  if (!element || element === activeStep) return;
  activeStep = element;
  steps.forEach((step) => step.classList.toggle("is-active", step === element));
  state.scene = element.dataset.scene;
  render();
}

function syncActiveFromViewport() {
  scrollFrame = 0;
  const offset = window.innerHeight * (window.innerWidth < 860 ? 0.52 : 0.54);
  let candidate = steps[0];
  for (const step of steps) {
    if (step.getBoundingClientRect().top <= offset) candidate = step;
    else break;
  }
  setActiveStep(candidate);
}

function requestScrollSync() {
  if (scrollFrame) return;
  scrollFrame = window.requestAnimationFrame(syncActiveFromViewport);
}

modeInputs.forEach((input) => {
  input.addEventListener("change", (event) => {
    state.mode = event.target.value;
    render();
  });
});

const scroller = scrollama();
scroller
  .setup({
    step: ".step",
    offset: window.innerWidth < 860 ? 0.72 : 0.54,
  })
  .onStepEnter(({ element }) => setActiveStep(element));

const resizeObserver = new ResizeObserver(() => {
  render();
  scroller.resize();
});
resizeObserver.observe(chartEl);

window.addEventListener("resize", () => scroller.resize());
window.addEventListener("scroll", requestScrollSync, { passive: true });
syncActiveFromViewport();
render();
