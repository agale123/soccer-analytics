const WIDTH = 700;
const HEIGHT = 500;
const MARGIN = {
    top: 30,
    right: 300,
    bottom: 60,
    left: 50,
};
const IMAGE_RADIUS = 24;

const COLORS = {
    'Portland Thorns': '#99242C',
    'OL Reign': '#00528C',
    'Washington Spirit': '#BF1E2E',
    'Chicago Red Stars': '#209ED4',
    'Gotham FC': '#000000',
    'Houston Dash': '#EA5003',
    'North Carolina Courage': '#013765',
    'Orlando Pride': '#611EA1',
    'Racing Louisville': '#c5b5f2',
    'Kansas City': '#23b0ad',
};

// Read rankings from csv
d3.csv('/nwsl-standings/rankings.csv').then(data => {
    drawChart(data);
});

function drawChart(data) {
    const maxWeek = Math.max(...Object.keys(data[0]).map(x => parseInt((x.match(/\d+/) || ["0"])[0]))) + 1;
    const maxRanking = data.length;

    // Draw the svg
    const svg = d3.select(document.getElementById('chart'))
        .append('svg')
        .attr('width', WIDTH + MARGIN.left + MARGIN.right)
        .attr('height', HEIGHT + MARGIN.top + MARGIN.bottom)
        .append('g')
        .attr('transform', `translate(${MARGIN.left},${MARGIN.top})`);

    // Add clip for rounded edges
    const defs = svg.append('defs');

    // Define the axes
    const x = d3.scaleLinear().range([0, WIDTH]).domain([1, maxWeek]);
    const y = d3.scaleLinear().range([HEIGHT, 0]).domain([0, maxRanking]);

    // Draw lines
    data.forEach((team, index) => {
        // Format data
        const line = Object.entries(team)
            .filter(([key, _]) => key !== 'Team')
            .map(([key, value]) => {
                return { week: parseInt(key.match(/\d+/)[0]), rank: parseInt(value) };
            });

        // Duplicate the last entry so lines won't draw over logos
        line.push({week: maxWeek, rank: line[line.length - 1].rank});

        const valueline = d3.line()
            .x(d => x(d.week))
            .y(d => y(10.5 - d.rank));

        // Draw line
        const path = svg.append('path')
            .data([line])
            .attr('class', 'line')
            .attr('id', `line-${team['Team']}`)
            .style('stroke', COLORS[team['Team']])
            .style('stroke-width', '4px')
            .style('fill', 'none')
            .attr('d', valueline);

        // Draw image
        defs.append('pattern')
            .attr('id', `avatar_${index}`)
            .attr('width', IMAGE_RADIUS * 2)
            .attr('height', IMAGE_RADIUS * 2)
            .attr('patternUnits', 'userSpaceOnUse')
            .append('svg:image')
            .attr('xlink:href', `/nwsl-standings/logos/${team['Team'].replace(/\s+/g, '')}.png`)
            .attr('width', IMAGE_RADIUS * 2)
            .attr('height', IMAGE_RADIUS * 2)
            .attr('x', 0)
            .attr('y', 0);


        const wrapper = svg.append('g');
        wrapper.transition()
            .duration(2000)
            .ease(d3.easeLinear)
            .attrTween('transform', translateAlong(path.node()))

        wrapper.append('circle')
            .attr('cx', IMAGE_RADIUS)
            .attr('cy', IMAGE_RADIUS)
            .attr('r', IMAGE_RADIUS)
            .attr('id', team['Team'])
            .style('fill', '#fff')
            .style('fill', `url(#avatar_${index})`)
            .on("mouseover", (d) => {
                const focused = d.target.id;
                document.getElementById(`line-${team['Team']}`).classList.add('focused');
                document.body.classList.add('focus-mode');
             })
             .on("mouseout", function (d) {
                const focused = d.target.id;
                document.getElementById(`line-${team['Team']}`).classList.remove('focused');
                document.body.classList.remove('focus-mode');
             });

        // Animate line
        const totalLength = path.node().getTotalLength();
        path
            .attr('stroke-dasharray', totalLength + ' ' + totalLength)
            .attr('stroke-dashoffset', totalLength)
            .transition()
            .duration(2000)
            .ease(d3.easeLinear)
            .attr('stroke-dashoffset', 0);
    });

    // Add the X axis
    let xAxis = svg.append('g')
        .attr('transform', 'translate(0,' + HEIGHT + ')')
        .call(d3.axisBottom(x)
            .ticks(Math.min(maxWeek + 1, 10))
            .tickFormat(d3.format('.0f')));

    xAxis.select(".domain").remove();

    svg.append('text')
        .attr('transform',
            'translate(' + (WIDTH / 2) + ' ,' +
            (HEIGHT + MARGIN.top + 20) + ')')
        .style('text-anchor', 'middle')
        .text('Week');

    // Add legend
    const sortedData = data.sort((a, b) => {
        const week = `Week ${maxWeek - 1}`;
        const aRank = parseInt(a[week]);
        const bRank= parseInt(b[week]);
        return aRank > bRank ? 1 : -1;
    });
    const legend = svg.selectAll('g.legend')
        .data(sortedData)
        .enter()
        .append('g')
        .attr('class', 'legend')
        .attr('transform',
            (d, i) => `translate(${WIDTH + 30},${i * 30})`);

    legend.append('rect')
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", 10)
        .attr("height", 20)
        .style("fill", (d, i) => COLORS[d['Team']])

    legend.append('text')
        .attr("x", 20)
        .attr("y", 15)
        .text((d, i) => `${d['Team']}`)
        .style("text-anchor", "start")
        .style("font-size", 15);
}

function translateAlong(path) {
    var l = path.getTotalLength();
    return (i) => {
        return (t) => {
            var p = path.getPointAtLength(t * l);
            return 'translate(' + (p.x - IMAGE_RADIUS) + ',' + (p.y - IMAGE_RADIUS) + ')';
        }
    }
}