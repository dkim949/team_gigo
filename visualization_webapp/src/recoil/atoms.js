import { atom } from "recoil";

export const buildingState = atom({
  key: "building",
  default: null,
});

export const layerState = atom({
  key: "layer",
  default: "rf",
});

export const subMenuState = atom({
  key: "subMenu",
  default: "overview",
});

export const isMainPanelOpenState = atom({
  key: "isMainPanelOpen",
  default: false,
});

export const isPredictPanelOpenState = atom({
  key: "isPredictPanelOpen",
  default: false,
});
