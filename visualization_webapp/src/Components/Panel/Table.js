import styled from "styled-components";

import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import { useRecoilState } from "recoil";
import { buildingState, subMenuState } from "../../recoil/atoms";

const keyMapping = {
  height: "Height",
  cnstrct_yr: "Construction Year",
  bin: "Building ID",
  retail_area: "Retail Area",
  office_area: "Office Area",
  residential_area: "Residential Area",
  idw_aadt_mean: "Estimated Vehicle Count-1",
  idw_atvc_mean: "Estimated Vehicle Count-2",
  "distance_from_station(ft)": "Distance to Subway (ft)",
  ridership_morning: "Riderships at the nearest subway between 6~10AM",
  ridership_midday: "Riderships at the nearest subway between 10AM~4PM",
  ridership_evening: "Riderships at the nearest subway between 4~8PM",
  ridership_night: "Riderships at the nearest subway between 8~12PM",
  ridership_late_night: "Riderships at the nearest subway between 0~6AM",
  office_within_450ft: "Office area within 450ft",
  retail_within_450ft: "Retail area within 450ft",
  residential_within_450ft: "Residential area within 450ft",
  distance_to_park: "Distance to Park",
  distance_to_school: "Distance to School",
  food_100: "# of restaurants within 100m",
  food_400: "# of restaurants within 400m",
  food_800: "# of restaurants within 800m",
  food_1000: "# of restaurants within 1000m",
};

const TableContainerDiv = styled.div`
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  min-height: 400px;
  display: ${({ $isVisible }) => ($isVisible ? "flex" : "none")};
`;

export default function TableBox() {
  const [building] = useRecoilState(buildingState);
  const [subMenu] = useRecoilState(subMenuState);
  let rows;
  if (building !== null) {
    const { properties } = building;
    rows = Object.entries(properties)
      .map(([k, v]) => {
        return {
          key: k,
          value: parseFloat(v) ? Math.round(parseFloat(v) * 100) / 100 : v,
        };
      })
      .filter((row) => row.key !== "globalid");
  }

  return (
    <TableContainerDiv $isVisible={subMenu === "table"}>
      {!building && "Please select any building"}
      {building && (
        <TableContainer component={Paper} style={{ maxHeight: 500 }}>
          <Table sx={{ maxWidth: 400 }} aria-label="simple table" stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell
                  style={{ backgroundColor: "#808080", color: "#ffffff" }}
                >
                  Attributes
                </TableCell>
                <TableCell
                  style={{ backgroundColor: "#808080", color: "#ffffff" }}
                  align="right"
                >
                  Value
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((row) => (
                <TableRow
                  key={row.key}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                >
                  <TableCell
                    sx={{ fontWeight: "bold" }}
                    component="th"
                    scope="row"
                  >
                    {keyMapping[row.key] || row.key}
                  </TableCell>
                  <TableCell align="right">{row.value}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </TableContainerDiv>
  );
}
