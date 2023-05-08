const R = 20;
const COLS = 20;
const ROWS = 200/COLS;
const WIDTH = (COLS+0.5) * R * Math.sqrt(3);
const HEIGHT = ((ROWS + 0.5) * R * 3) / 2;

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

function draw(data) {
  const svg = d3
    .select("#host")
    .append("svg")
    .attr("width", WIDTH)
    .attr("height", HEIGHT);

  svg
    .selectAll("polygon")
    .data(data)
    .join("polygon")
    .attr("points", hexPoints(20))
    .attr("fill", "blue")
    .attr("opacity", (d, i) => i / 200)
    .attr("transform", (d, i) => {
      const row = Math.floor(i / (COLS * 2 - 1));
      // 0 if top row, 1 if bottom row
      const subRow = Math.floor((i % (COLS * 2 - 1)) / COLS);
      const y = ((Math.floor(i / COLS) + 0.75) * R * 3) / 2;

      const x =
        (((i % COLS) + (Math.floor(i / COLS) % 2 === 0 ? 0.5 : 1)) * COLS * R * Math.sqrt(3)) /
        COLS;

      return `translate(${x},${y})`;
    });
}

async function initialize() {
  const data = await d3.csv("all_matches.csv");
  draw(data);
}

initialize();
