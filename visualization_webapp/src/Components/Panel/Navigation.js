import styled from "styled-components";

const NavContainer = styled.ul`
  display: flex;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ccc;

  & li {
    cursor: pointer;
    margin-right: 20px;
    padding: 0;
    border-radius: 5px;
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    padding: 6px;
    color: #ccc;
  }

  & li.active {
    color: #fff;
    border: 1px solid #212121;
    background-color: #424242;
  }
`;

export function Navigation({ subMenu, setSubMenu }) {
  return (
    <NavContainer>
      <li
        onClick={() => setSubMenu("overview")}
        className={subMenu === "overview" ? "active" : "inActive"}
      >
        Overview
      </li>
      <li
        onClick={() => setSubMenu("scatter")}
        className={subMenu === "scatter" ? "active" : "inActive"}
      >
        Scatter
      </li>
      <li
        onClick={() => setSubMenu("table")}
        className={subMenu === "table" ? "active" : "inActive"}
      >
        Table
      </li>
    </NavContainer>
  );
}
