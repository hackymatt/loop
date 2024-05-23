import { createMetadata } from "./create-metadata";

describe("createMetadata", () => {
  // Verify the function returns an object with a 'title' property
  it("should return an object with a title property when called", () => {
    const result = createMetadata("Test");
    expect(result).toHaveProperty("title");
    expect(typeof result.title).toBe("string");
  });

  // Test with an empty string as the title input
  it("should handle empty string input correctly", () => {
    const result = createMetadata("");
    expect(result.title).toBe(" | loop");
  });
});
