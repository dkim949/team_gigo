export default function calculateCentroid(coordinates) {
  let totalLat = 0;
  let totalLon = 0;

  coordinates.forEach((coordinate) => {
    totalLat += parseFloat(coordinate[1]);
    totalLon += parseFloat(coordinate[0]);
  });
  const avgLat = totalLat / coordinates.length;
  const avgLon = totalLon / coordinates.length;

  return [avgLon, avgLat];
}
