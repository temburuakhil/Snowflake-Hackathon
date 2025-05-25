import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import { Icon } from 'leaflet';
import { Box, Paper } from '@mui/material';
import { styled } from '@mui/material/styles';
import { Location, LocationCategory, MapViewState } from '../types';

// Custom icons for different location categories
const categoryIcons: Record<LocationCategory, string> = {
  'Wildlife Sanctuary': '/icons/paw.png',
  'Forest Reserve': '/icons/tree.png',
  'National Park': '/icons/mountain.png',
  'Botanical Garden': '/icons/flower.png',
  'Scenic Place': '/icons/camera.png',
  'Temple': '/icons/temple.png',
};

const MapWrapper = styled(Paper)(({ theme }) => ({
  width: '100%',
  height: 'calc(100vh - 64px)', // Adjust based on header height
  position: 'relative',
  overflow: 'hidden',
  borderRadius: theme.shape.borderRadius,
  boxShadow: theme.shadows[3],
}));

interface MapProps {
  viewState: MapViewState;
  onViewStateChange: (newState: Partial<MapViewState>) => void;
  locations: Location[];
}

const MapComponent: React.FC<MapProps> = ({ viewState, onViewStateChange, locations }) => {
  const [map, setMap] = useState<L.Map | null>(null);

  // Custom hook to handle map view changes
  const MapController = () => {
    const map = useMap();
    
    useEffect(() => {
      if (viewState.center && viewState.zoom) {
        map.setView(viewState.center, viewState.zoom);
      }
    }, [viewState.center, viewState.zoom]);

    return null;
  };

  // Filter locations based on visible categories
  const visibleLocations = locations.filter(location => 
    viewState.visibleCategories.includes(location.category)
  );

  return (
    <MapWrapper>
      <MapContainer
        center={viewState.center}
        zoom={viewState.zoom}
        style={{ height: '100%', width: '100%' }}
        whenCreated={setMap}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        <MapController />
        
        {visibleLocations.map((location) => (
          <Marker
            key={location.id}
            position={[location.coordinates.lat, location.coordinates.lng]}
            icon={new Icon({
              iconUrl: categoryIcons[location.category],
              iconSize: [32, 32],
              iconAnchor: [16, 16],
            })}
            eventHandlers={{
              click: () => {
                onViewStateChange({ selectedLocation: location });
              },
            }}
          >
            <Popup>
              <Box sx={{ p: 1 }}>
                <h3>{location.name}</h3>
                <p>{location.category}</p>
              </Box>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </MapWrapper>
  );
};

export default MapComponent; 