import { Location, State } from '../types';

// Mock data for development - replace with actual Snowflake queries in production
const mockLocations: Location[] = [
  {
    id: '1',
    name: 'Jim Corbett National Park',
    state: 'Uttarakhand',
    category: 'National Park',
    coordinates: {
      lat: 29.5328,
      lng: 78.9417,
    },
    wikipediaUrl: 'https://en.wikipedia.org/wiki/Jim_Corbett_National_Park',
    summary: 'India\'s oldest national park, known for its Bengal tigers and diverse wildlife.',
    threeDModelUrl: '/models/corbett.glb',
    imageUrl: '/images/corbett.jpg',
  },
  // Add more mock locations here
];

const mockStates: State[] = [
  {
    name: 'Uttarakhand',
    coordinates: {
      lat: 30.0668,
      lng: 79.0193,
    },
    zoom: 8,
    locations: mockLocations.filter(loc => loc.state === 'Uttarakhand'),
  },
  // Add more states here
];

export class DatabaseService {
  private static instance: DatabaseService;
  private locations: Location[] = [];
  private states: State[] = [];

  private constructor() {
    // Initialize with mock data
    this.locations = mockLocations;
    this.states = mockStates;
  }

  public static getInstance(): DatabaseService {
    if (!DatabaseService.instance) {
      DatabaseService.instance = new DatabaseService();
    }
    return DatabaseService.instance;
  }

  public async getLocations(): Promise<Location[]> {
    // In production, this would query Snowflake
    return this.locations;
  }

  public async getStates(): Promise<State[]> {
    // In production, this would query Snowflake
    return this.states;
  }

  public async searchLocations(query: string): Promise<Location[]> {
    // In production, this would query Snowflake with a LIKE clause
    return this.locations.filter(location =>
      location.name.toLowerCase().includes(query.toLowerCase()) ||
      location.state.toLowerCase().includes(query.toLowerCase())
    );
  }

  public async getLocationsByCategory(category: string): Promise<Location[]> {
    // In production, this would query Snowflake with a WHERE clause
    return this.locations.filter(location => location.category === category);
  }

  public async getLocationsByState(state: string): Promise<Location[]> {
    // In production, this would query Snowflake with a WHERE clause
    return this.locations.filter(location => location.state === state);
  }
}

export const databaseService = DatabaseService.getInstance(); 