const R = 30;
const COLS = 20;
const ROWS = Math.ceil(210 / COLS);
const WIDTH = (COLS + 0.5) * R * Math.sqrt(3);
const HEIGHT = ((ROWS + 0.5) * R * 3) / 2;

const FILTER_N = 20;

const BLUE = "#002f87";
const RED = "#e62929";
const GOLD = "#be892c";
const GREY = "#D3D3D3";

const COLORS = {
  W: BLUE,
  L: RED,
  D: GOLD,
};

const STEPS = {
  GAMES: 1,
  RESULT: 2,
  POSITION: 3,
};

function hexPoints(r) {
  const halfWidth = (r * Math.sqrt(3)) / 2;
  return `
      0,${-r}
      ${halfWidth},${-r / 2}
      ${halfWidth},${r / 2}
      0,${r}
      ${-halfWidth},${r / 2}
      ${-halfWidth},${-r / 2}`;
}

function getResult(d) {
  if (d["goals_for"] > d["goals_against"]) {
    return "W";
  } else if (d["goals_for"] < d["goals_against"]) {
    return "L";
  } else {
    return "D";
  }
}

function draw(data, step) {
  const svg = d3.select("#host svg");

  const strokePolygons = svg
    .append("g")
    .selectAll("polygon")
    .data(data)
    .join("polygon")
    .attr("points", hexPoints(R - 5))
    .attr("transform", (d, i) => {
      const y = ((Math.floor(i / COLS) + 0.75) * R * 3) / 2;
      const x =
        (((i % COLS) + (Math.floor(i / COLS) % 2 === 0 ? 0.5 : 1)) *
          COLS *
          R *
          Math.sqrt(3)) /
        COLS;

      return `translate(${x},${y})`;
    });

  strokePolygons
    .attr("fill", "none")
    .attr("stroke-width", "3")
    .attr("stroke", (d) => (d["minutes"] > 0 ? BLUE : GREY));
  if (step === STEPS.GAMES) {
    return;
  }

  strokePolygons.attr("stroke", (d) =>
    d["minutes"] > 0 ? COLORS[getResult(d)] : GREY
  );
  if (step === STEPS.RESULT) {
    return;
  }

  const polygons = svg
    .append("g")
    .selectAll("polygon")
    .data(data)
    .join("polygon")
    .attr("points", hexPoints(R))
    .attr("clip-path", "url(#hex-clip)")
    .attr("transform", (d, i) => {
      const y = ((Math.floor(i / COLS) + 0.75) * R * 3) / 2;
      const x =
        (((i % COLS) + (Math.floor(i / COLS) % 2 === 0 ? 0.5 : 1)) *
          COLS *
          R *
          Math.sqrt(3)) /
        COLS;

      return `translate(${x},${y})`;
    });
  strokePolygons.raise();

  polygons
    .attr("fill", (d) => {
      if (d["minutes"] > 0) {
        return `url(#${d["position"] || "LB"}-${getResult(d)})`;
      } else {
        return "none";
      }
    })
    .attr(
      "filter",
      () => `url(#waterColor${Math.floor(Math.random() * FILTER_N)})`
    );
  if (step === STEPS.POSITION) {
    return;
  }
}

function addGradient(defs, name, percent, result) {
  const color = COLORS[result];
  const gradient = defs
    .append("linearGradient")
    .attr("id", name + "-" + result)
    .attr("x1", "0%")
    .attr("x2", "100%")
    .attr("y1", "50%")
    .attr("y2", "50%");

  gradient
    .append("stop")
    .attr("offset", "0%")
    .attr("stop-color", color)
    .attr("stop-opacity", 0.4);

  gradient
    .append("stop")
    .attr("offset", `${percent}%`)
    .attr("stop-color", color)
    .attr("stop-opacity", 1);

  gradient
    .append("stop")
    .attr("offset", "100%")
    .attr("stop-color", color)
    .attr("stop-opacity", 0.4);
}

function addFilters(defs) {
  for (const i in [...Array(FILTER_N).keys()]) {
    const filter = defs.append("filter").attr("id", `waterColor${i}`);
    filter
      .append("feTurbulence")
      .attr("type", "turbulence")
      .attr("baseFrequency", "0.1")
      .attr("numOctaves", "2")
      .attr("seed", `${Math.floor(Math.random() * 1000)}`)
      .attr("result", "turbulence");
    filter
      .append("feDisplacementMap")
      .attr("in", "SourceGraphic")
      .attr("in2", "turbulence")
      .attr("result", "displacement")
      .attr("scale", "10")
      .attr("xChannelSelector", "R")
      .attr("yChannelSelector", "G");
    filter
      .append("feGaussianBlur")
      .attr("in", "displacement")
      .attr("stdDeviation", "0.75");
  }
}

function setupSvg() {
  const svg = d3
    .select("#host svg")
    .attr("width", WIDTH)
    .attr("height", HEIGHT);

  const defs = svg.select("defs");

  for (const result of ["W", "L", "D"]) {
    addGradient(defs, "LB", 0, result);
    addGradient(defs, "LCB", 40, result);
    addGradient(defs, "CB", 50, result);
    addGradient(defs, "RCB", 60, result);
    addGradient(defs, "RB", 100, result);
  }

  addFilters(defs);
}

async function initialize() {
  const data = await d3.csv("all_matches.csv");
  setupSvg();
  draw(data, STEPS.POSITION);
}

initialize();
