import { test, expect } from "vitest";
import { Cache } from "./pokecache.js";

test.concurrent.each([
  {
    key: "https://example.com",
    val: "testdata",
    interval: 500, // 1/2 second
  },
  {
    key: "https://example.com/path",
    val: "moretestdata",
    interval: 1000, // 1 second
  }
])("Test Caching $interval ms", async ({ key, val, interval }) => {
  const cache = new Cache(interval);

  // Add item and check immediate retrieval
  cache.add(key, val);
  const cached = cache.get(key);
  expect(cached).toBe(val);

  // Wait long enough for the reap loop to trigger and clear stale entry
  await new Promise((resolve) => setTimeout(resolve, (interval * 2) + 50 ) );
  
  const reaped = cache.get(key);
  expect(reaped).toBe(undefined);

  cache.stopReapLoop();
});
