import React from "react";
import styled from "styled-components";
import { H4Title } from "../../titles";
import { buildingState } from "../../../recoil/atoms";
import { useRecoilState } from "recoil";
import calculateCentroid from "../../../utils/calCentroid";

import buildingJson from "../../../utils/data/building.json";

const ListContainer = styled.div`
  margin-top: 20px;

  & li {
    margin-bottom: 8px;
    font-size: 15px;
    cursor: pointer;
  }

  & li:hover {
    font-weight: bold;
  }
`;

const listData = [
  { id: 1, name: "Spot 1", probability: "70%", bin: 1063584 },
  { id: 2, name: "Spot 2", probability: "69.9%", bin: 1082666 },
  { id: 3, name: "Spot 3", probability: "69.3%", bin: 1085800 },
  { id: 4, name: "Spot 4", probability: "69.1%", bin: 1088298 },
  { id: 5, name: "Spot 5", probability: "68.8%", bin: 1020543 },
  { id: 6, name: "Spot 6", probability: "68.7%", bin: 1088320 },
  { id: 7, name: "Spot 7", probability: "68.7%", bin: 1085400 },
  { id: 8, name: "Spot 8", probability: "68.6%", bin: 1001137 },
  { id: 9, name: "Spot 9", probability: "68.5%", bin: 1087577 },
  { id: 10, name: "Spot 10", probability: "68.4%", bin: 1085799 },
];

const TopSuccessSpotsList = ({ selectedAlgorithm }) => {
  const [building, setBuilding] = useRecoilState(buildingState);
  const setBuildingByBin = (bin) => {
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
  };
  return (
    <ListContainer>
      <H4Title>Top Success Spots</H4Title>
      <ul>
        {listData.map((spot) => (
          <li key={spot.id} onClick={(e) => setBuildingByBin(spot.bin)}>
            {spot.name} - {spot.probability}
          </li>
        ))}
      </ul>
    </ListContainer>
  );
};

export default TopSuccessSpotsList;
