const R = 30;
const STROKE_W = 3;
const GAP = 5;
const COLS = 20;
const ROWS = Math.ceil(230 / COLS);
const WIDTH = (COLS + 0.5) * R * Math.sqrt(3);
const HEIGHT = ((ROWS + 0.5) * R * 3) / 2;

const FILTER_N = 20;

const BLUE = "#002f87";
const RED = "#e62929";
const GOLD = "#be892c";
const GREY = "#D3D3D3";

const SHIELD = `
m 0 18 
q -6.3 -1.575 -10.35 -7.312
t -4.05 -12.577
v -10.71
l 14.4 -5.4
l 14.4 5.4
v 10.71
q 0 6.84 -4.05 12.577
t -10.35 7.313
z
m 0 -2.79 
q 5.175 -1.71 8.438 -6.458
t 3.263 -10.642
v -8.82
l -11.7 -4.41
l -11.7 4.41
v 8.82
q 0 5.895 3.263 10.643
t 8.438 6.458 
z
m 0 -15.165 
z
`;

const SHIELD_SEASONS = ["2014", "2015", "2022"];

const COLORS = {
  W: BLUE,
  L: RED,
  D: GOLD,
};

const STEPS = {
  INIT: 0,
  GAMES: 1,
  RESULT: 2,
  SHIELD: 3,
  GOAL_DIFF: 4,
  POSITION: 5,
  ASSISTS: 6,
  GOALS: 7,
};

function hexPoints(r) {
  const halfWidth = (r * Math.sqrt(3)) / 2;
  return [
    [0, -r],
    [halfWidth, -r / 2],
    [halfWidth, r / 2],
    [0, r],
    [-halfWidth, r / 2],
    [-halfWidth, -r / 2],
  ];
}

function hexPointsString(r) {
  return hexPoints(r)
    .map((x) => x.join(","))
    .join(" ");
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

function indexTransform(d) {
  const i = d["index"];
  const y = ((Math.floor(i / COLS) + 0.75) * R * 3) / 2;
  const x =
    (((i % COLS) + (Math.floor(i / COLS) % 2 === 0 ? 0.5 : 1)) *
      COLS *
      R *
      Math.sqrt(3)) /
    COLS;

  return `translate(${x},${y})`;
}

function arcPath(a, b) {
  const hex = hexPoints(R - STROKE_W - GAP);
  return [
    "M",
    hex[a][0],
    hex[a][1],
    "A",
    R - STROKE_W - GAP,
    R - STROKE_W - GAP,
    -120,
    0,
    1,
    hex[b][0],
    ",",
    hex[b][1],
  ].join(" ");
}

function draw(data, step) {
  const svg = d3.select("#host svg");

  // Step 0: All Reign games
  const games = svg
    .selectAll("g")
    .data(data)
    .enter()
    .append("g")
    .attr("transform", indexTransform);

  games
    .append("polygon")
    .attr("points", hexPointsString(R - GAP))
    .attr("fill", "none")
    .attr("stroke-width", "3")
    .attr("stroke", GREY);
  games
    .append("text")
    .text((d) => d["label"]?.replace("20", ""))
    .style("text-anchor", "middle")
    .style("dominant-baseline", "middle")
    .style("font-size", "10pt")
    .style("font-family", "'Open Sans', sans-serif");
  if (step === STEPS.INIT) {
    return;
  }

  // Step 1: Games played
  data = data.filter((g) => g["minutes"] > 0);
  const strokePolygons = svg
    .append("g")
    .selectAll("polygon")
    .data(data)
    .join("polygon")
    .attr("points", hexPointsString(R - GAP))
    .attr("transform", indexTransform);
  strokePolygons
    .attr("fill", "none")
    .attr("stroke-width", "3")
    .attr("stroke", BLUE);
  if (step === STEPS.GAMES) {
    return;
  }

  // Step 2: Win/loss/tie record
  strokePolygons.attr("stroke", (d) =>
    d["minutes"] > 0 ? COLORS[getResult(d)] : GREY
  );
  if (step === STEPS.RESULT) {
    return;
  }

  // Step 3: Shield wins
  games
    .append("path")
    .filter((d) => SHIELD_SEASONS.includes(d["label"]))
    .attr("fill", BLUE)
    .attr("d", SHIELD);
  if (step === STEPS.SHIELD) {
    return;
  }

  // Step 4: Goal differential
  strokePolygons.attr("stroke-dasharray", (d) => {
    if (d["goals_against"] === 0 || d["minutes"] <= 0) {
      return "none";
    } else {
      return d["goals_for"] * 4 + "," + d["goals_against"] * 4;
    }
  });
  if (step === STEPS.GOAL_DIFF) {
    return;
  }

  // Step 5: Position
  const polygons = svg
    .append("g")
    .selectAll("polygon")
    .data(data)
    .join("polygon")
    .attr("points", hexPointsString(R))
    .attr("clip-path", "url(#hex-clip)")
    .attr("transform", indexTransform);
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

  // Step 6: Assists
  const assists = data.filter((row) => row["assists"] > 0);
  svg
    .append("g")
    .selectAll("path")
    .data(assists)
    .join("path")
    .attr("transform", indexTransform)
    .attr("d", () => {
      return arcPath(3, 1) + " " + arcPath(5, 3) + " " + arcPath(1, 5);
    })
    .attr("stroke", "white")
    .attr("opacity", 0.5)
    .attr("stroke-width", 2)
    .attr("fill", "none");
  if (step === STEPS.ASSISTS) {
    return;
  }

  // Step 7: Goals
  const goals = data.filter((row) => row["goals"] > 0);
  svg
    .append("g")
    .selectAll("path")
    .data(goals)
    .join("path")
    .attr("transform", indexTransform)
    .attr("d", () => {
      return (
        arcPath(3, 1) +
        " " +
        arcPath(5, 3) +
        " " +
        arcPath(1, 5) +
        " " +
        arcPath(4, 2) +
        " " +
        arcPath(2, 0) +
        " " +
        arcPath(0, 4)
      );
    })
    .attr("stroke", "white")
    .attr("opacity", 0.5)
    .attr("stroke-width", 2)
    .attr("fill", "none");
  if (step === STEPS.GOALS) {
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
  // Add placeholders for season labels
  const seasons = [...new Set(data.map((d) => d["season"]))];
  for (const season of seasons) {
    const index = data.findIndex((d) => d["season"] === season);
    data.splice(index, 0, { label: season });
  }
  // Add indices
  for (let i = 0; i < data.length; i++) {
    data[i]["index"] = i;
  }
  setupSvg();
  draw(data, STEPS.GOALS);
}

initialize();
