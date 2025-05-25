export const MAP_CONFIG = {
  defaultCenter: [20.5937, 78.9629] as [number, number], // Center of India
  defaultZoom: 5,
  minZoom: 4,
  maxZoom: 18,
  stateZoom: 8,
  locationZoom: 12,
  tileLayer: {
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  },
  markerIconSize: [32, 32] as [number, number],
  markerIconAnchor: [16, 16] as [number, number],
};

export const CATEGORY_COLORS = {
  'Wildlife Sanctuary': '#4CAF50',
  'Forest Reserve': '#2E7D32',
  'National Park': '#1B5E20',
  'Botanical Garden': '#81C784',
  'Scenic Place': '#2196F3',
  'Temple': '#FF9800',
} as const; 