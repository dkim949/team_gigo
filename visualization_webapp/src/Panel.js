import React, { useState } from "react";
import styled from "styled-components";
import { H1Title, H3Title } from "./Components/titles";

import Overview from "./Components/Panel/Overview/Overview";
import { Navigation } from "./Components/Panel/Navigation";
import Table from "./Components/Panel/Table";
import Scatter from "./Components/Panel/Scatter/Scatter";
import { useRecoilState } from "recoil";
import { isMainPanelOpenState, layerState, subMenuState } from "./recoil/atoms";

const PanelContainer = styled.div`
  position: absolute;
  top: 10px;
  left: 10px;
  width: 400px;
  height: calc(99.5% - 10px);
  background-color: rgba(255, 255, 255, 1);
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1;
  transition: transform 0.3s ease-in-out;
  transform: ${({ $isOpen }) =>
    $isOpen ? "translateX(0)" : "translateX(-100%)"};
`;

const ToggleButton = styled.button`
  position: absolute;
  top: 10px;
  right: -30px;
  width: 30px;
  height: 30px;
  background-color: white;
  border: none;
  cursor: pointer;
`;

const Panel = () => {
  const [selectedAlgorithm, setSelectedAlgorithm] = useState("accessibility");
  const [, setLayer] = useRecoilState(layerState);
  const [subMenu, setSubMenu] = useRecoilState(subMenuState);
  const [isMainPanelOpen, setIsMainPanelOpen] =
    useRecoilState(isMainPanelOpenState);
  // const [,setIsPredictPanelOpen] = useRecoilState(isPredictPanelOpenState);

  const togglePanel = () => {
    setIsMainPanelOpen(!isMainPanelOpen);
  };

  const handleAlgorithmSelect = (e) => {
    const selectedValue = e.target.value;
    setSelectedAlgorithm(selectedValue);
    handleSelect(e);
  };

  const handleSelect = (e) => {
    e.preventDefault();
    setLayer(e.target.value);
  };

  return (
    <PanelContainer $isOpen={isMainPanelOpen}>
      <H1Title>Traffic-Driven Restaurant Success Prediction</H1Title>
      <H3Title>Layers :</H3Title>
      <select value={selectedAlgorithm} onChange={handleAlgorithmSelect}>
        <option value="rf">(Prediction) One Year Survival Probability</option>
        <option value="distance_to_subway">(Feature) Distance to Subway</option>
        <option value="ridership_evening">
          (Feature) Subway Riderships in the Evening
        </option>
        <option value="ridership_midday">
          (Feature) Subway Riderships in the Midday
        </option>
        <option value="estimatedVehicle">
          (Feature) Estimated Vehicle Count
        </option>
        <option value="food400">(Feature) # of restaurants within 400m</option>
        <option value="food800">(Feature) # of restaurants within 800m</option>
        <option value="distance_to_park">(Feature) Distance to park</option>
      </select>
      <Navigation setSubMenu={setSubMenu} subMenu={subMenu} />
      <Overview selectedAlgorithm={selectedAlgorithm} />
      <Table />
      <Scatter />
      <ToggleButton onClick={togglePanel}>
        {isMainPanelOpen ? "<" : ">"}
      </ToggleButton>
    </PanelContainer>
  );
};

export default Panel;
