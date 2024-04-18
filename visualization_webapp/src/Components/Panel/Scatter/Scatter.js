import { useCallback, useEffect, useRef, useState } from "react";
import styled from "styled-components";
import { ScatterPlot } from "./scatterplot";
import { useRecoilState } from "recoil";
import calculateCentroid from "../../../utils/calCentroid";
import buildingJson from "../../../utils/data/building.json";
import { buildingState, subMenuState } from "../../../recoil/atoms";

const ScatterContainer = styled.div`
  width: 100%;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  min-height: 400px;
  display: ${({ $isVisible }) => ($isVisible ? "flex" : "none")};
`;

const ScatterHeader = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  justify-content: space-between;
  align-items: flex-start;

  & select {
    height: 20px;
    margin-left: 10px;
  }
`;

const ScatterLabel = styled.div`
  display: flex;
  align-items: center;
  margin-top: 15px;
`;

export default function Scatter() {
  const [building, setBuilding] = useRecoilState(buildingState);
  const [subMenu] = useRecoilState(subMenuState);
  const [chart, setChart] = useState(null);
  const [xFeature, setXFeature] = useState("office_area");
  const [yFeature, setYFeature] = useState("retail_area");

  const container = useRef(null);

  const setBuildingByBin = useCallback(
    (bin) => {
      const previousBin = building?.properties?.bin;

      if (previousBin && previousBin.toString() === bin.toString()) {
        setBuilding(null);
      }

      const buildingData = buildingJson.features.filter(
        (row) => parseInt(row.properties.bin) === bin
      )[0];

      const { properties } = buildingData;
      const coordinates = buildingData.geometry.coordinates[0][0];
      const centroid = calculateCentroid(coordinates);
      setBuilding({ properties, centroid });
    },
    [building, setBuilding]
  );

  useEffect(() => {
    if (!chart) {
      setChart(
        new ScatterPlot(
          container.current,
          building && building.properties.bin,
          setBuildingByBin
        )
      );
    } else {
      chart.update(building && building.properties.bin, xFeature, yFeature);
    }
  }, [building, xFeature, yFeature, chart, setBuildingByBin]);

  const handleXChange = (e) => {
    const selectedValue = e.target.value;
    setXFeature(selectedValue);
  };

  const handleYChange = (e) => {
    const selectedValue = e.target.value;
    setYFeature(selectedValue);
  };

  return (
    <ScatterContainer $isVisible={subMenu === "scatter"}>
      <ScatterHeader>
        <ScatterLabel>
          <label>X:</label>
          <select value={xFeature} onChange={handleXChange}>
            <option value="office_area">Office Area</option>
            <option value="retail_area">Retail Area</option>
            <option value="residential_area">Residential Area</option>
            <option value="distance_from_station(ft)">
              Distance to Subway (ft)
            </option>
            <option value="food_100"># of Restaurants within 100m</option>
            <option value="food_400"># of Restaurants within 400m</option>
          </select>
        </ScatterLabel>
        <ScatterLabel>
          <label>Y:</label>
          <select value={yFeature} onChange={handleYChange}>
            <option value="office_area">Office Area</option>
            <option value="retail_area">Retail Area</option>
            <option value="residential_area">Residential Area</option>
            <option value="distance_from_station(ft)">
              Distance to Subway (ft)
            </option>
            <option value="food_100"># of Restaurants within 100m</option>
            <option value="food_400"># of Restaurants within 400m</option>
          </select>
        </ScatterLabel>
      </ScatterHeader>
      <div className="ScatterChart" ref={container}></div>
    </ScatterContainer>
  );
}
