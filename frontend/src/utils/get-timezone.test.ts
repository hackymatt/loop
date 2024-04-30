import { getTimezone } from "./get-timezone";

describe("getTimezone", () => {
  // Returns a string representing the timezone.
  it("should return a string representing the timezone", () => {
    const result = getTimezone();
    expect(typeof result).toBe("string");
  });

  // Returns 'Europe/Warsaw' if the timezone cannot be determined.
  it("should return Europe/Warsaw if the timezone cannot be determined", () => {
    const result = getTimezone();
    expect(result).toBe("Europe/Warsaw");
  });
});
