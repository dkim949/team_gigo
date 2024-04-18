export const probabilityLayer = {
  id: "probability",
  type: "fill",
  paint: {
    "fill-color": [
      "interpolate",
      ["linear"],
      ["get", "probability"],
      0.3,
      "#fff",
      0.6,
      "#2196f3",
    ],
    "fill-opacity": 0.3,
    "fill-outline-color": "#212121",
  },
};

export const accessibilityLayer = {
  id: "Distance to Subway",
  type: "fill",
  paint: {
    "fill-color": [
      "interpolate",
      ["linear"],
      ["get", "distance_from_station(ft)"],
      0,
      "#fff",
      2000,
      "#006064",
    ],
    "fill-opacity": 0.3,
    "fill-outline-color": "#212121",
  },
};

export const ridershipLayer = {
  id: "Riderships_evening",
  type: "fill",
  paint: {
    "fill-color": [
      "interpolate",
      ["linear"],
      ["get", "ridership_evening"],
      0,
      "#fff",
      2000,
      "#f44336",
    ],
    "fill-opacity": 0.3,
    "fill-outline-color": "#212121",
  },
};

export const ridershipLayerTwo = {
  id: "Riderships_midday",
  type: "fill",
  paint: {
    "fill-color": [
      "interpolate",
      ["linear"],
      ["get", "ridership_midday"],
      0,
      "#fff",
      2000,
      "#f44336",
    ],
    "fill-opacity": 0.3,
    "fill-outline-color": "#212121",
  },
};

export const estimatedVehicleLayer = {
  id: "estimatedVehicle",
  type: "fill",
  paint: {
    "fill-color": [
      "interpolate",
      ["linear"],
      ["get", "idw_aadt_mean"],
      0,
      "#fff",
      18000,
      "#FF9800",
    ],
    "fill-opacity": 0.3,
    "fill-outline-color": "#212121",
  },
};

export const food400Layer = {
  id: "food400",
  type: "fill",
  paint: {
    "fill-color": [
      "interpolate",
      ["linear"],
      ["get", "food_400"],
      0,
      "#fff",
      150,
      "#F44336",
    ],
    "fill-opacity": 0.3,
    "fill-outline-color": "#212121",
  },
};

export const food800Layer = {
  id: "food800",
  type: "fill",
  paint: {
    "fill-color": [
      "interpolate",
      ["linear"],
      ["get", "food_800"],
      0,
      "#fff",
      150,
      "#F44336",
    ],
    "fill-opacity": 0.3,
    "fill-outline-color": "#212121",
  },
};

export const parkAccessibilityLayer = {
  id: "park_accessibility",
  type: "fill",
  paint: {
    "fill-color": [
      "interpolate",
      ["linear"],
      ["get", "distance_to_park"],
      0,
      "#fff",
      900,
      "#4caf50",
    ],
    "fill-opacity": 0.3,
    "fill-outline-color": "#212121",
  },
};

export const highlightLayer = {
  id: "building-highlighted",
  type: "line",
  paint: {
    "line-color": "#fff",
    "line-width": 3,
  },
};
