import type { State } from "./state.js";

export async function commandCatch(state: State, ...args: string[]): Promise<void> {
  const pokemonName = args[0];

  if (!pokemonName) {
    console.log("Please provide a Pokemon name. Usage: catch <pokemon-name>");
    return;
  }

  console.log(`Throwing a Pokeball at ${pokemonName}...`);

  try {
    const pokemon = await state.pokeAPI.fetchPokemon(pokemonName);

    // Calculate dynamic capture rate scale based on difficulty
    // High base experience decreases the capture probability curve
    const threshold = 40; 
    const roll = Math.random() * pokemon.base_experience;

    if (roll < threshold) {
      console.log(`${pokemon.name} was caught!`);
      // Save full species snapshot directly to our internal pokedex map
      state.pokedex[pokemon.name] = pokemon;
    } else {
      console.log(`${pokemon.name} escaped!`);
    }
  } catch (error) {
    console.log(`Failed to locate Pokemon "${pokemonName}". Check the spelling.`);
  }
}
