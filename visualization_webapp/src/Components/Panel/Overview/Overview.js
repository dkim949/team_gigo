import styled from "styled-components";
import { useRecoilState } from "recoil";
import TopSuccessSpotsList from "./TopSuccessSpotsList";
import { subMenuState } from "../../../recoil/atoms";

const ChartsContainer = styled.div`
  margin-top: 20px;
  display: ${({ $isVisible }) => ($isVisible ? "flex" : "none")};
  flex-direction: column;
`;

export default function Overview({ selectedAlgorithm }) {
  const [subMenu] = useRecoilState(subMenuState);
  return (
    <ChartsContainer $isVisible={subMenu === "overview"}>
      <TopSuccessSpotsList selectedAlgorithm={selectedAlgorithm} />
    </ChartsContainer>
  );
}
