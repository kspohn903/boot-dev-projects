import type { State } from "./state.js";

export async function commandPokedex(state: State): Promise<void> {
  const caughtPokemonNames = Object.keys(state.pokedex);

  if (caughtPokemonNames.length === 0) {
    console.log("Your Pokedex is empty. Go catch some Pokémon!");
    return;
  }

  console.log("Your Pokedex:");
  for (const name of caughtPokemonNames) {
    console.log(` - ${name}`);
  }
}
