/**
 * @file This file contains the `cleanInput` function and the `startREPL` function.
 * The `cleanInput` function processes raw string input, while `startREPL`
 * implements a Read-Eval-Print Loop (REPL) using Node.js's `readline` module.
 */

// Import the `readline` module for creating an interactive command-line interface.
import * as readline from "readline";

/**
 * Cleans the input string by trimming leading/trailing whitespace and splitting
 * it into an array of strings. Multiple spaces between words are treated as a single delimiter.
 * Empty strings resulting from the split are filtered out.
 *
 * @param {string} input The raw input string to be cleaned.
 * @returns {string[]} An array of strings, where each element is a cleaned word from the input.
 */
export function cleanInput(input: string): string[] {
  // Trim leading and trailing whitespace from the input string.
  // Then, split the string by one or more whitespace characters (regex /\s+/).
  // Finally, filter out any empty strings that might result from multiple spaces
  // or leading/trailing spaces in the original input before trimming.
  return input.trim().split(/\s+/).filter(s => s != '');
}

/**
 * Starts the Read-Eval-Print Loop (REPL) for the Pokedex CLI.
 * This function initializes the readline interface, sets up the prompt,
 * and handles user input by cleaning it and providing feedback.
 */
export function startREPL(): void {
  /**
   * Creates a readline interface. This object facilitates reading data from a Readable stream
   * (like `process.stdin`) one line at a time and writing prompts to a Writable stream
   * (like `process.stdout`).
   *
   * @param {object} options Configuration options for the readline interface.
   * @param {NodeJS.ReadableStream} options.input The readable stream to listen to (e.g., standard input).
   * @param {NodeJS.WritableStream} options.output The writable stream to write output to (e.g., standard output).
   * @param {string} options.prompt The string to be displayed as a prompt when `rl.prompt()` is called.
   */
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: "Pokedex > ", // The prompt string as specified in the requirements.
  });

  // Display the initial prompt to the user when the application starts.
  // This gives the user an immediate indication that the CLI is ready for input.
  rl.prompt();

  /**
   * Event listener for the 'line' event. This event is emitted whenever the `input` stream
   * receives a `<return>` or `<enter>` keypress, signifying that the user has finished typing a line.
   *
   * @param {string} line The line of text entered by the user, without the trailing newline character.
   */
  rl.on("line", (line) => {
    // Use the `cleanInput` function to process the raw line entered by the user.
    // This will trim whitespace and split the input into an array of individual words.
    const cleanedWords = cleanInput(line.toLowerCase());

    // Check if the `cleanedWords` array is empty. This can happen if the user
    // just pressed Enter, or if their input consisted solely of whitespace.
    if (cleanedWords.length === 0) {
      // If the input was empty, simply call `rl.prompt()` again to display the prompt
      // and allow the user to enter another command. No further processing is needed for empty input.
      rl.prompt();
      return; // Exit the callback to prevent further execution for this empty line.
    }

    // If the input is not empty, extract the first word from the `cleanedWords` array.
    const firstWord = cleanedWords[0];

    // Print a message back to the user, confirming the command they entered.
    // The format "Your command was: <first word>" is specified in the requirements.
    console.log(`Your command was: ${firstWord}`);

    // After processing the command (or indicating an empty command), call `rl.prompt()` again.
    // This readies the interface for the next user input, displaying the prompt once more.
    rl.prompt();
  });

  /**
   * Event listener for the 'close' event. This event is emitted when the `input` stream
   * receives an 'end' event (e.g., `Ctrl+D` on Unix) or when the `rl.close()` method is called.
   * It's a good practice to handle this event to perform any necessary cleanup or exit gracefully.
   */
  rl.on("close", () => {
    // Log a friendly message to the console indicating that the CLI is shutting down.
    console.log("Exiting Pokedex CLI. Goodbye!");
    // Explicitly exit the Node.js process with a success code.
    process.exit(0);
  });
}

