import React, { useRef, useEffect, useMemo } from "react";
import styled from "styled-components";
import * as d3 from "d3";

const ChartContainer = styled.div`
  width: 100%;
  height: 200px;
`;

const AlgorithmComparisonChart = ({ selectedAlgorithm }) => {
  const chartData = useMemo(() => {
    return {
      accessibility: { accuracy: 0.85 },
      algorithm2: { accuracy: 0.88 },
      algorithm3: { accuracy: 0.78 },
      algorithm4: { accuracy: 0.7 },
      algorithm5: { accuracy: 0.83 },
    };
  }, []);

  const chartRef = useRef(null);

  useEffect(() => {
    const chartContainer = d3.select(chartRef.current);
    const width = chartContainer.node().getBoundingClientRect().width;
    const height = chartContainer.node().getBoundingClientRect().height;

    // 기존 차트 삭제
    chartContainer.selectAll("*").remove();

    const margin = { top: 20, right: 20, bottom: 30, left: 40 };
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;

    const svg = chartContainer
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", `translate(${margin.left}, ${margin.top})`);

    const x = d3.scaleBand().range([0, chartWidth]).padding(0.1);
    const y = d3.scaleLinear().range([chartHeight, 0]);

    const data = Object.entries(chartData).map(([name, { accuracy }]) => ({
      name,
      accuracy,
    }));

    x.domain(data.map((d) => d.name));
    y.domain([0, 1]);

    svg
      .append("g")
      .attr("transform", `translate(0, ${chartHeight})`)
      .call(d3.axisBottom(x))
      .append("text")
      .attr("y", height - margin.bottom + 15)
      .attr("x", chartWidth / 2)
      .attr("text-anchor", "middle")
      .text("Algorithm");

    svg
      .append("g")
      .call(d3.axisLeft(y))
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x", 0 - height / 2)
      .attr("text-anchor", "middle")
      .text("Accuracy");

    svg
      .append("text")
      .attr("x", width / 2 - 30)
      .attr("y", margin.top / 2 - 10)
      .attr("text-anchor", "middle")
      .style("font-size", "16px")
      .style("font-weight", "bold")
      .text("Accuracy Comparison");

    const barGroups = svg.selectAll(".bar").data(data).enter().append("g");

    barGroups
      .append("rect")
      .attr("class", "bar")
      .attr("x", (d) => x(d.name))
      .attr("y", (d) => y(d.accuracy))
      .attr("width", x.bandwidth())
      .attr("height", (d) => chartHeight - y(d.accuracy))
      .attr("fill", (d) =>
        d.name === selectedAlgorithm ? "steelblue" : "lightgray"
      );
  }, [chartData, selectedAlgorithm]);

  return <ChartContainer ref={chartRef} />;
};

export default AlgorithmComparisonChart;
