export type LocationCategory = 
  | 'Wildlife Sanctuary'
  | 'Forest Reserve'
  | 'National Park'
  | 'Botanical Garden'
  | 'Scenic Place'
  | 'Temple';

export interface Location {
  id: string;
  name: string;
  state: string;
  category: LocationCategory;
  coordinates: {
    lat: number;
    lng: number;
  };
  wikipediaUrl: string;
  summary: string;
  threeDModelUrl: string;
  imageUrl: string;
}

export interface State {
  name: string;
  coordinates: {
    lat: number;
    lng: number;
  };
  zoom: number;
  locations: Location[];
}

export interface MapViewState {
  center: [number, number];
  zoom: number;
  selectedState: string | null;
  selectedLocation: Location | null;
  visibleCategories: LocationCategory[];
} 