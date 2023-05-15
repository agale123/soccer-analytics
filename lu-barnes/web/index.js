const N = 230;
const FILTER_N = 20;
const MAX_WIDTH = 1200;

let ROWS, COLS, R, WIDTH, HEIGHT, STROKE_W, GAP;

function calculateDimensions() {
  const height = document.body.clientHeight - 160;
  const width = Math.min(document.body.clientWidth, MAX_WIDTH);

  STROKE_W = Math.ceil((width / MAX_WIDTH) * 3);
  GAP = 2 + STROKE_W;

  ROWS = Math.ceil(Math.sqrt((N * height) / width));
  COLS = Math.ceil(N / ROWS);
  R = Math.floor(width / COLS / 2);
  WIDTH = (COLS + 0.5) * R * Math.sqrt(3);
  HEIGHT = ((ROWS + 0.5) * R * 3) / 2;
}

calculateDimensions();

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
  POSITION: 3,
  MINUTES: 4,
  GOAL_DIFF: 5,
  ASSISTS: 6,
  GOALS: 7,
  SHIELD: 8,
};

function hexPoints(r, c = [0, 0], scale = 1) {
  const halfWidth = ((r * Math.sqrt(3)) / 2) * scale;
  return [
    [c[0] + 0, c[1] + -r],
    [c[0] + halfWidth, c[1] + -r / 2],
    [c[0] + halfWidth, c[1] + r / 2],
    [c[0] + 0, c[1] + r],
    [c[0] + -halfWidth, c[1] + r / 2],
    [c[0] + -halfWidth, c[1] + -r / 2],
  ];
}

function hexPointsString(r, c = [0, 0], scale = 1) {
  return hexPoints(r, c, scale)
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

function fadeIn(els, min = 0, max = 1) {
  els.attr("opacity", min).transition().duration(500).attr("opacity", max);
}

function draw() {
  const svg = d3.select("#background svg");

  svg.selectAll("g").remove();

  // Step 0: All Reign games
  const games = svg
    .selectAll("g")
    .data(data)
    .enter()
    .append("g")
    .attr("transform", indexTransform);

  const gamePolygons = games
    .append("polygon")
    .attr("points", hexPointsString(R - GAP))
    .attr("fill", "none")
    .attr("stroke-width", STROKE_W)
    .attr("stroke", GREY);
  games
    .append("text")
    .text((d) => d["label"]?.replace("20", ""))
    .style("text-anchor", "middle")
    .style("dominant-baseline", "middle")
    .style("font-size", Math.floor(R / 2) + "pt")
    .style("font-family", "'Open Sans', sans-serif");
  if (currentStep === STEPS.INIT) {
    if (previousStep > currentStep) {
      gamePolygons
        .attr("stroke", (d) => (d["minutes"] > 0 ? BLUE : GREY))
        .transition()
        .duration(500)
        .attr("stroke", GREY);
    }
    return;
  }

  // Step 1: Games played
  const filteredData = data.filter((g) => g["minutes"] > 0);
  const strokePolygons = svg
    .append("g")
    .selectAll("polygon")
    .data(filteredData)
    .join("polygon")
    .attr("points", hexPointsString(R - GAP))
    .attr("transform", indexTransform);
  strokePolygons
    .attr("fill", "none")
    .attr("stroke-width", STROKE_W)
    .attr("stroke", BLUE);
  if (currentStep === STEPS.GAMES) {
    if (previousStep < currentStep) {
      fadeIn(strokePolygons);
    } else if (previousStep > currentStep) {
      strokePolygons
        .attr("stroke", (d) => (d["minutes"] > 0 ? COLORS[getResult(d)] : GREY))
        .transition()
        .duration(500)
        .attr("stroke", BLUE);
    }
    return;
  }

  // Step 2: Win/loss/tie record
  strokePolygons.attr("stroke", (d) =>
    d["minutes"] > 0 ? COLORS[getResult(d)] : GREY
  );

  // Create position polygons early to support fade out.
  const polygons = svg
    .append("g")
    .selectAll("polygon")
    .data(filteredData)
    .join("polygon")
    .attr("points", hexPointsString(R + STROKE_W))
    .attr("clip-path", "url(#hex-clip-9)")
    .attr("transform", indexTransform)
    .attr("opacity", 0)
    .attr("fill", (d) => {
      if (d["minutes"] > 0) {
        return `url(#${d["position"]}-${getResult(d)})`;
      } else {
        return "none";
      }
    })
    .attr("filter", (d, i) => `url(#waterColor${i % FILTER_N})`);
  gamePolygons.raise();
  strokePolygons.raise();

  if (currentStep === STEPS.RESULT) {
    if (currentStep > previousStep) {
      strokePolygons
        .attr("stroke", BLUE)
        .transition()
        .duration(500)
        .attr("stroke", (d) =>
          d["minutes"] > 0 ? COLORS[getResult(d)] : GREY
        );
    } else if (currentStep < previousStep) {
      fadeIn(polygons, 1, 0);
    }
    return;
  }

  // Step 3: Position
  polygons.attr("opacity", 1);
  if (currentStep === STEPS.POSITION) {
    if (currentStep > previousStep) {
      fadeIn(polygons);
    } else if (currentStep < previousStep) {
      polygons
        .transition()
        .duration(500)
        .attrTween("clip-path", (d, i, a) => {
          return (val) => {
            const minutes = parseInt(d["minutes"]);
            return `url(#hex-clip-${minuteBin(
              minutes + val * (90 - minutes)
            )})`;
          };
        });
    }
    return;
  }

  function minuteBin(minutes) {
    return Math.ceil(Math.max(Math.min(minutes, 90), 0) / 10);
  }

  // Step 4: Minutes
  polygons.attr(
    "clip-path",
    (d) => `url(#hex-clip-${minuteBin(parseInt(d["minutes"]))})`
  );
  if (currentStep === STEPS.MINUTES) {
    if (currentStep > previousStep) {
      polygons
        .transition()
        .duration(500)
        .attrTween("clip-path", (d, i, a) => {
          return (val) => {
            const minutes = parseInt(d["minutes"]);
            return `url(#hex-clip-${minuteBin(
              minutes + (1 - val) * (90 - minutes)
            )})`;
          };
        });
    }
    return;
  }

  // Step 5: Goal differential
  strokePolygons.attr("stroke-dasharray", (d) => {
    if (d["goals_against"] === 0 || d["minutes"] <= 0) {
      return "none";
    } else {
      return 8 + "," + d["goals_against"] * 4;
    }
  });
  if (currentStep === STEPS.GOAL_DIFF) {
    return;
  }

  // Step 6: Assists
  const assists = filteredData.filter((row) => row["assists"] > 0);
  const assistsEls = svg
    .append("g")
    .selectAll("path")
    .data(assists)
    .join("path")
    .attr("transform", indexTransform)
    .attr("d", () => {
      return arcPath(3, 1) + " " + arcPath(5, 3) + " " + arcPath(1, 5);
    })
    .attr("stroke", "white")
    .attr("stroke-width", 2)
    .attr("opacity", 0.5)
    .attr("fill", "none");
  if (currentStep === STEPS.ASSISTS) {
    if (currentStep > previousStep) {
      fadeIn(assistsEls, 0, 0.5);
    }
    return;
  }

  // Step 7: Goals
  const goals = filteredData.filter((row) => row["goals"] > 0);
  const goalsEls = svg
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
    .attr("stroke-width", 2)
    .attr("opacity", 0.5)
    .attr("fill", "none");
  if (currentStep === STEPS.GOALS) {
    if (currentStep > previousStep) {
      fadeIn(goalsEls, 0, 0.5);
    }
    return;
  }

  // Step 8: Shield wins
  const shieldEls = games
    .append("path")
    .filter((d) => SHIELD_SEASONS.includes(d["label"]))
    .attr("fill", BLUE)
    .attr("d", SHIELD)
    .attr("transform", () => `scale(${0.3 + (1 * WIDTH) / MAX_WIDTH})`);
  if (currentStep === STEPS.SHIELD) {
    if (currentStep > previousStep) {
      fadeIn(shieldEls);
    }
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
    .attr("stop-opacity", 0.2);

  gradient
    .append("stop")
    .attr("offset", `${percent}%`)
    .attr("stop-color", color)
    .attr("stop-opacity", 1);

  gradient
    .append("stop")
    .attr("offset", "100%")
    .attr("stop-color", color)
    .attr("stop-opacity", 0.2);
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

function addClipPaths(defs) {
  for (let i of [1, 2, 3, 4, 5, 6, 7, 8, 9]) {
    const points = hexPoints((Math.sqrt(i) / 3) * 0.33 + (5-STROKE_W)* 0.008, [0.5, 0.5], 1.2).map(
      (p, i) => (i === 0 ? "M " : "L ") + p.join(",")
    );

    defs
      .append("clipPath")
      .attr("clipPathUnits", "objectBoundingBox")
      .attr("id", "hex-clip-" + i)
      .append("path")
      .attr("d", points.join(" "));
  }
}

function setupSvg() {
  const svg = d3
    .select("#background svg")
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

  addClipPaths(defs);
}

let currentStep = STEPS.INIT;
let previousStep = undefined;
let data;

function addScrollListeners() {
  for (const i of Object.values(STEPS)) {
    const observer = new IntersectionObserver(
      (entry) => {
        if (entry[0].isIntersecting) {
          previousStep = currentStep;
          currentStep = i;
          draw();
        }
      },
      { root: document.querySelector(`#story`), threshold: 1 }
    );

    observer.observe(document.querySelector(`#story  div:nth-child(${i + 1})`));
  }
}

async function initialize() {
  data = await d3.csv("all_matches.csv");
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
  draw();

  addScrollListeners();

  //Resize the d3 charts on a page resize
  window.addEventListener("resize", () => {
    calculateDimensions();

    d3.select("#background svg").attr("width", WIDTH).attr("height", HEIGHT);

    draw();
  });
}

initialize();
