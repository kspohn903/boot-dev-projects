// Import the cleanInput function from the module under test.
import { cleanInput } from "./repl";

// Import necessary testing utilities from Vitest.
// `describe`: Used to group related tests into a test suite.
// `expect`: Used to make assertions about values.
// `test`: Used to define individual test cases.
import { describe, expect, test } from "vitest";

/**
 * Define a test suite for the `cleanInput` function using `describe.each`.
 * This allows defining multiple test cases in a data-driven way.
 * Each object in the array represents a test case with an `input` string and an `expected` array of strings.
 */
describe.each([
  {
    input: "  hello  world  ", // Input with leading, trailing, and multiple internal spaces
    expected: ["hello", "world"],
  },
  {
    input: "singleword", // Single word with no extra spaces
    expected: ["singleword"],
  },
  {
    input: "  another   test   case   ", // Multiple words with varying spaces
    expected: ["another", "test", "case"],
  },
  {
    input: "", // Empty string input
    expected: [],
  },
  {
    input: "   ", // Input consisting only of spaces
    expected: [],
  },
  {
    input: " leading space", // Input with only leading spaces
    expected: ["leading", "space"],
  },
  {
    input: "trailing space ", // Input with only trailing spaces
    expected: ["trailing", "space"],
  },
  {
    input: " one two   three ", // Mixed spaces
    expected: ["one", "two", "three"],
  },
])(
  // The test suite name, dynamically generated using the `input` value for clarity.
  "cleanInput($input)",
  ({ input, expected }) => {
    // Define an individual test case for each data entry.
    // The test name dynamically displays the expected output.
    test(`Expected: [${expected.map((s) => `'${s}'`).join(", ")}]`, () => {
      // Call the function under test with the current input.
      const actual = cleanInput(input);

      // Assert that the length of the actual array matches the expected array's length.
      // This is a quick check to see if the number of words is correct.
      expect(actual).toHaveLength(expected.length);

      // Iterate over the expected array to compare each element.
      // Using `for...in` here to iterate over indices for direct comparison.
      for (const i in expected) {
        // Assert that each element in the actual array is strictly equal to the corresponding
        // element in the expected array. This ensures the words themselves are correct.
        expect(actual[i]).toBe(expected[i]);
      }
    });
  }
);

