import type { State } from "./state.js";

export async function commandMap(state: State): Promise<void> {
  // Use nextLocationsURL if it exists (for pages 2+), otherwise fetch default page
  const url = state.nextLocationsURL || undefined;
  
  const data = await state.pokeAPI.fetchLocations(url);
  
  // Update pagination state references
  state.nextLocationsURL = data.next;
  state.prevLocationsURL = data.previous;

  // Print results
  for (const location of data.results) {
    console.log(location.name);
  }
}
