import React from "react";
import styled from "styled-components";

const PopoverContainer = styled.div`
  color: #212121;
`;

const BoldText = styled.span`
  font-weight: bold;
`;

const Popover = ({ properties }) => {
  const stopPropagation = (e) => {
    e.stopPropagation();
  };
  return (
    <PopoverContainer onClick={stopPropagation}>
      <div>
        <BoldText>One year survival probability:</BoldText>{" "}
        {Math.round(properties.probability * 100)}%
      </div>
      <div>
        <BoldText>Height:</BoldText> {Math.round(properties.height * 100) / 100}
      </div>
      <div>
        <BoldText>Age:</BoldText>{" "}
        {Math.round((2024 - properties.cnstrct_yr) * 100) / 100}
      </div>
      <div>
        <BoldText>Retail area:</BoldText>{" "}
        {Math.round(properties.retail_area * 100) / 100}
      </div>
      <div>
        <BoldText>Office area:</BoldText>{" "}
        {Math.round(properties.office_area * 100) / 100}
      </div>
      <div>
        <BoldText>Residential area:</BoldText>{" "}
        {Math.round(properties.residential_area * 100) / 100}
      </div>
      <div>
        <BoldText>Estimated Vehicle Count:</BoldText>{" "}
        {Math.round(properties.idw_aadt_mean * 100) / 100}
      </div>
      <div>
        <BoldText>Distance to Subway (ft):</BoldText>{" "}
        {Math.round(properties["distance_from_station(ft)"] * 100) / 100}
      </div>
      <div>
        <BoldText>
          # of entries in the nearest subway station between 4 ~ 8PM:
        </BoldText>{" "}
        {Math.round(properties["ridership_evening"] * 100) / 100}
      </div>
    </PopoverContainer>
  );
};

export default Popover;
