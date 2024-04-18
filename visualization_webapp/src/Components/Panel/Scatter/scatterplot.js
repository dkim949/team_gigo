import * as d3 from "d3";
import csvData from "../../../utils/data/building.csv";
import buildingJson from "../../../utils/data/building.json";

export function ScatterPlot(element, bin, handleBinSelect) {
  const margin = { top: 50, bottom: 50, right: 50, left: 50 };
  const height = 400 - margin.top - margin.bottom;
  const width = 400 - margin.left - margin.right;

  let data;
  const svg = d3
    .select(element)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);

  const container = svg
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

  const xAxis = container
    .append("g")
    .attr("transform", `translate(0, ${height})`);

  const yAxis = container.append("g");

  const showLoading = () => {
    container
      .append("text")
      .attr("class", "loading-text")
      .attr("x", width / 2)
      .attr("y", height / 2)
      .attr("text-anchor", "middle")
      .text("Loading...");
  };

  const hideLoading = () => {
    container.select(".loading-text").remove();
  };

  showLoading();

  d3.csv(csvData).then((d) => {
    data = d;
    const xFeature = "office_area";
    const yFeature = "retail_area";

    this.update(bin, xFeature, yFeature);
    hideLoading();
  });

  this.update = (bin, xFeature, yFeature) => {
    if (!data) return;

    const xScale = d3
      .scaleLinear()
      .domain([0, d3.max(data.map((d) => parseInt(d[xFeature])))])
      .range([0, width]);

    const yScale = d3
      .scaleLinear()
      .domain([0, d3.max(data.map((d) => parseInt(d[yFeature])))])
      .range([height, 0]);

    const xAxisCall = d3.axisBottom(xScale).tickFormat(d3.format(".2s"));
    xAxis.call(xAxisCall);

    const yAxisCall = d3.axisLeft(yScale).tickFormat(d3.format(".2s"));
    yAxis.call(yAxisCall);

    const circles = container.selectAll("circle").data(data);

    circles
      .enter()
      .append("circle")
      .attr("cx", (d) => xScale(d[xFeature]))
      .attr("cy", (d) => yScale(d[yFeature]))
      .attr("r", 5)
      .attr("fill", (d) => (bin && d.bin === bin ? "#f44336" : "#424242"))
      .attr("fill-opacity", 0.2)
      .on("mouseenter", function (e) {
        d3.select(this).attr("fill", "#f44336").attr("fill-opacity", 0.7);
      })
      .on("mouseout", function (e) {
        d3.select(this).attr("fill", "#424242").attr("fill-opacity", 0.2);
      })
      .on("click", function (event, d) {
        handleBinSelect(parseInt(d.bin));
      });

    circles
      .transition()
      .duration(500)
      .attr("cx", (d) => xScale(d[xFeature]))
      .attr("cy", (d) => yScale(d[yFeature]));

    circles.exit().remove();

    if (bin) {
      const redCircles = container
        .selectAll(".red-circle")
        .data(data.filter((d) => bin && d.bin === bin));

      redCircles
        .enter()
        .append("circle")
        .merge(redCircles)
        .attr("cx", (d) => xScale(d[xFeature]))
        .attr("cy", (d) => yScale(d[yFeature]))
        .attr("r", 5)
        .attr("fill", "#f44336")
        .attr("fill-opacity", 0.7);

      redCircles.exit().remove();
    } else {
      container.selectAll(".red-circle").remove();
    }
  };
}
