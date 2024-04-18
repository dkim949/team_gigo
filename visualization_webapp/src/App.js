import "mapbox-gl/dist/mapbox-gl.css";
import { useMemo, useRef, useEffect } from "react";
import Map, { Popup, Source, Layer } from "react-map-gl";

import styled from "styled-components";

import buildingJson from "./utils/data/building.json";
import calculateCentroid from "./utils/calCentroid";

import Panel from "./Panel";
import PredictPanel from "./PredictPanel";
import Popover from "./Popover";
import { GlobalStyle } from "./styles/GlobalStyle";
import {
  accessibilityLayer,
  probabilityLayer,
  highlightLayer,
  ridershipLayer,
  ridershipLayerTwo,
  estimatedVehicleLayer,
  food400Layer,
  food800Layer,
  parkAccessibilityLayer,
} from "./layers/layers";

import { useRecoilState } from "recoil";
import { buildingState, layerState } from "./recoil/atoms";

const MapContainer = styled.div`
  position: relative;
  width: 99.5vw;
  height: 99.5vh;
`;

const mapboxAccessToken =
  "pk.eyJ1Ijoic2doYW4iLCJhIjoiY2szamxqbjZnMGtmbTNjbXZzamh4cng3dSJ9.GGv4GVVoZ811d6PKi54PrA";

function App() {
  const viewport = {
    latitude: 40.746676,
    longitude: -73.9901321,
    zoom: 12,
    transitionDuration: 2000,
  };
  const mapRef = useRef();
  const [building, setBuilding] = useRecoilState(buildingState);
  const [selectedLayer] = useRecoilState(layerState);

  const handleMapClick = (e) => {
    const features = e.features;
    if (features && features.length > 0) {
      const properties = features[0].properties;
      const coordinates = features[0].geometry.coordinates[0];
      const centroid = calculateCentroid(coordinates);
      setBuilding({ properties, centroid });
    } else {
      setBuilding(null);
    }
  };

  useEffect(() => {
    if (building) {
      mapRef.current.flyTo({
        center: building.centroid,
        zoom: 15, // 선택적으로 원하는 줌 레벨로 조정할 수 있습니다.
        essential: true, // 이동이 필수 요소임을 명시합니다.
        duration: 1000,
      });
    }
  }, [building]);

  const filter = useMemo(
    () => ["in", "bin", building?.properties.bin || ""],
    [building]
  );

  return (
    <MapContainer>
      <GlobalStyle />
      <Map
        initialViewState={viewport}
        mapboxAccessToken={mapboxAccessToken}
        mapStyle="mapbox://styles/sghan/ck1ljdcmy16fc1cpg0f4qh3wu"
        onClick={handleMapClick}
        interactiveLayerIds={[
          "probability",
          "Distance to Subway",
          "Riderships_evening",
          "Riderships_midday",
          "estimatedVehicle",
          "food400",
          "food800",
          "distance_to_park",
        ]}
        ref={mapRef}
      >
        <Source type="geojson" data={buildingJson}>
          <Layer
            {...probabilityLayer}
            layout={{
              visibility: selectedLayer === "rf" ? "visible" : "none",
            }}
          />
          <Layer
            {...accessibilityLayer}
            layout={{
              visibility:
                selectedLayer === "distance_to_subway" ? "visible" : "none",
            }}
          />
          <Layer
            {...ridershipLayer}
            layout={{
              visibility:
                selectedLayer === "ridership_evening" ? "visible" : "none",
            }}
          />
          <Layer
            {...ridershipLayerTwo}
            layout={{
              visibility:
                selectedLayer === "ridership_midday" ? "visible" : "none",
            }}
          />
          <Layer
            {...estimatedVehicleLayer}
            layout={{
              visibility:
                selectedLayer === "estimatedVehicle" ? "visible" : "none",
            }}
          />
          <Layer
            {...food400Layer}
            layout={{
              visibility: selectedLayer === "food400" ? "visible" : "none",
            }}
          />
          <Layer
            {...food800Layer}
            layout={{
              visibility: selectedLayer === "food800" ? "visible" : "none",
            }}
          />
          <Layer
            {...parkAccessibilityLayer}
            layout={{
              visibility:
                selectedLayer === "distance_to_park" ? "visible" : "none",
            }}
          />
          <Layer {...highlightLayer} filter={filter} />
        </Source>
        {building && (
          <Popup
            latitude={building.centroid[1]}
            longitude={building.centroid[0]}
            offset={[0, -10]}
            closeButton={true}
            closeOnClick={false}
            onClose={() => setBuilding(null)}
            anchor="bottom"
          >
            <Popover properties={building.properties} />
          </Popup>
        )}
      </Map>
      <PredictPanel />
      <Panel />
    </MapContainer>
  );
}

export default App;
