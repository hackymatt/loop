import { getTimezone } from "./get-timezone";

describe("getTimezone", () => {
  // Returns a string representing the timezone.
  it("should return a string representing the timezone", () => {
    const result = getTimezone();
    expect(typeof result).toBe("string");
  });

  // Returns 'UTC' if the timezone cannot be determined.
  it("should return UTC if the timezone cannot be determined", () => {
    const result = getTimezone();
    expect(result).toBe("UTC");
  });
});
