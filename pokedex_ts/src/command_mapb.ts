import type { State } from "./state.js";

export async function commandMapb(state: State): Promise<void> {
  if (!state.prevLocationsURL) {
    console.log("you're on the first page");
    return;
  }

  const data = await state.pokeAPI.fetchLocations(state.prevLocationsURL);
  
  // Update pagination state references
  state.nextLocationsURL = data.next;
  state.prevLocationsURL = data.previous;

  // Print results
  for (const location of data.results) {
    console.log(location.name);
  }
}
