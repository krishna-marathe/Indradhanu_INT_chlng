import React from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import { HeatmapLayer } from 'react-leaflet-heatmap-layer-v3';

const GeoHeatmap = ({ data }) => {
  if (!data || data.length === 0) {
    return <p>No geospatial data found.</p>;
  }

  const heatmapPoints = data.map(item => [
    item.latitude,
    item.longitude,
    item.value || 1
  ]);

  return (
    <MapContainer center={[20.5937, 78.9629]} zoom={5} style={{ height: '400px', width: '100%' }}>
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
      />
      <HeatmapLayer
        fitBoundsOnLoad
        fitBoundsOnUpdate
        points={heatmapPoints}
        longitudeExtractor={m => m[1]}
        latitudeExtractor={m => m[0]}
        intensityExtractor={m => m[2]}
      />
    </MapContainer>
  );
};

export default GeoHeatmap;