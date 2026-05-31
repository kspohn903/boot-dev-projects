import type { State } from "./state.js";

export function cleanInput(input: string): string[] {
  const lowedAndTrimmed = input.trim().toLowerCase();
  if (lowedAndTrimmed === "") {
    return [];
  }
  return lowedAndTrimmed.split(/\s+/);
}

export function startREPL(state: State) {
  state.rl.prompt();

  // Changed to async (line: string) => ...
  state.rl.on("line", async (line: string) => {
    const words = cleanInput(line);

    if (words.length === 0) {
      state.rl.prompt();
      return;
    }

    const commandName = words[0];
    const args = words.slice(1);
    if (commandName in state.commands) {
      try {
        // Correctly await the execution of the command
        await state.commands[commandName].callback(state, ...args);
      } catch (err) {
        console.error(`Error running command: ${err}`);
      }
    } else {
      console.log("Unknown command");
    }

    state.rl.prompt();
  });
}
