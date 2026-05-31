import type { State } from "./state.js";

export async function commandExplore(state: State, ...args: string[]): Promise<void> {
  const areaName = args[0];
  
  if (!areaName) {
    console.log("Please provide a location area name. Usage: explore <area-name>");
    return;
  }

  console.log(`Exploring ${areaName}...`);

  try {
    const locationData = await state.pokeAPI.fetchLocation(areaName);
    
    console.log("Found Pokemon:");
    
    // Check if encounters exist in the payload
    if (!locationData.pokemon_encounters || locationData.pokemon_encounters.length === 0) {
      console.log(" No Pokémon found in this area.");
      return;
    }

    // Loop through the encounter array to list species names
    for (const encounter of locationData.pokemon_encounters) {
      console.log(` - ${encounter.pokemon.name}`);
    }
  } catch (error) {
    console.log(`Could not explore area "${areaName}". Make sure the name is spelled correctly.`);
  }
}
