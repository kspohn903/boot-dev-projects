import { Cache } from "./pokecache.js";

export type ShallowLocations = {
  count: number;
  next: string | null;
  previous: string | null;
  results: { name: string; url: string }[];
};

export type LocationData = {
  id: number;
  name: string;
  pokemon_encounters: {
    pokemon: { name: string; url: string };
  }[];
};

// Define the blueprint of the data structure we want to capture
export type Pokemon = {
  id: number;
  name: string;
  base_experience: number;
  height: number;
  weight: number;
  stats: {
    base_stat: number;
    stat: {
      name: string;
    };
  }[];
  types: {
    type: {
      name: string;
    };
  }[];
};


export class PokeAPI {
  private static readonly baseURL = "https://pokeapi.co/api/v2";
  #cache: Cache;

  constructor() {
    this.#cache = new Cache(5 * 60 * 1000);
  }

  async fetchLocations(pageURL?: string): Promise<ShallowLocations> {
    const targetURL = pageURL || `${PokeAPI.baseURL}/location-area`;
    const cachedData = this.#cache.get<ShallowLocations>(targetURL);
    if (cachedData) return cachedData;

    const response = await fetch(targetURL);
    if (!response.ok) throw new Error(`Failed to fetch locations: ${response.statusText}`);

    const data = (await response.json()) as ShallowLocations;
    this.#cache.add(targetURL, data);
    return data;
  }

  async fetchLocation(locationName: string): Promise<LocationData> {
    const targetURL = `${PokeAPI.baseURL}/location-area/${locationName}`;
    const cachedData = this.#cache.get<LocationData>(targetURL);
    if (cachedData) return cachedData;

    const response = await fetch(targetURL);
    if (!response.ok) throw new Error(`Failed to fetch location: ${response.statusText}`);

    const data = (await response.json()) as LocationData;
    this.#cache.add(targetURL, data);
    return data;
  }

  // Fetch individual Pokemon data by name
  async fetchPokemon(pokemonName: string): Promise<Pokemon> {
    const targetURL = `${PokeAPI.baseURL}/pokemon/${pokemonName}`;
    const cachedData = this.#cache.get<Pokemon>(targetURL);
    if (cachedData) return cachedData;

    const response = await fetch(targetURL);
    if (!response.ok) throw new Error(`Failed to fetch pokemon: ${response.statusText}`);

    const data = (await response.json()) as Pokemon;
    this.#cache.add(targetURL, data);
    return data;
  }
}
