import { describe, expect, test } from "vitest";
import { cleanInput } from "./repl.js";

describe.each([
  {
    input: "  hello  world  ",
    expected: ["hello", "world"],
  },
  {
    input: "Charmander Bulbasaur PIKACHU",
    expected: ["charmander", "bulbasaur", "pikachu"],
  },
  {
    input: "   ",
    expected: [],
  },
  {
    input: "SingleWord",
    expected: ["singleword"],
  }
])("cleanInput($input)", ({ input, expected }) => {
  test(`Expected: ${JSON.stringify(expected)}`, () => {
    // Call the function to get the actual results
    const actual = cleanInput(input);

    // Verify the arrays match length
    expect(actual).toHaveLength(expected.length);
    
    // Verify each individual item matches
    for (const i in expected) {
      expect(actual[i]).toBe(expected[i]);
    }
  });
});
