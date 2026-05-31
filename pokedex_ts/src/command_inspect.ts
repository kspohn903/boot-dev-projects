import type { State } from "./state.js";

export async function commandInspect(state: State, ...args: string[]): Promise<void> {
  const pokemonName = args[0];

  if (!pokemonName) {
    console.log("Please provide a Pokemon name. Usage: inspect <pokemon-name>");
    return;
  }

  // Check our local state map
  const pokemon = state.pokedex[pokemonName.toLowerCase()];

  if (!pokemon) {
    console.log("you have not caught that pokemon");
    return;
  }

  console.log(`Name: ${pokemon.name}`);
  console.log(`Height: ${pokemon.height}`);
  console.log(`Weight: ${pokemon.weight}`);
  
  console.log("Stats:");
  for (const s of pokemon.stats) {
    console.log(`  -${s.stat.name}: ${s.base_stat}`);
  }

  console.log("Types:");
  for (const t of pokemon.types) {
    console.log(`  - ${t.type.name}`);
  }
}
