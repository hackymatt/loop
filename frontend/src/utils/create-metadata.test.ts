import packageInfo from "package.json";

import { createMetadata } from "./create-metadata";

describe("createMetadata", () => {
  // Generates metadata with a valid title, description, and keywords
  it("should generate metadata with a valid title, description, and keywords", () => {
    const title = "Test Title";
    const description = "Test Description";
    const keywords = ["keyword1", "keyword2"];

    const result = createMetadata(title, description, keywords);

    expect(result.title).toBe(`Test Title • ${packageInfo.name}`);
    expect(result.description).toBe(description);
    expect(result.keywords).toBe("keyword1,keyword2");
  });

  // Handles empty title string
  it("should handle empty title string", () => {
    const title = "";
    const description = "Test Description";
    const keywords = ["keyword1", "keyword2"];

    const result = createMetadata(title, description, keywords);

    expect(result.title).toBe(` • ${packageInfo.name}`);
    expect(result.description).toBe(description);
    expect(result.keywords).toBe("keyword1,keyword2");
  });
});
