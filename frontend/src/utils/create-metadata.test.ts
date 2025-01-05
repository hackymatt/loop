import packageInfo from "package.json";

import { createMetadata } from "./create-metadata";

describe("createMetadata", () => {
  // Generates metadata with a valid title, description, and keywords
  it("should generate metadata with a valid title, description, and keywords", () => {
    const title = "Test Title";
    const description = "Test Description";
    const keywords = ["keyword1", "keyword2"];
    const path = "/test-path";

    const result = createMetadata(title, description, keywords, path);

    expect(result.title).toBe(`Test Title • ${packageInfo.name}`);
    expect(result.description).toBe(description);
    expect(result.keywords).toBe("keyword1,keyword2");
    expect(result.alternates.canonical).toBe(`https://loop.edu.pl${path}/`);
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

  // Handles empty path string
  it("should handle empty path string", () => {
    const title = "Test Title";
    const description = "Test Description";
    const keywords = ["keyword1", "keyword2"];
    const path = "";

    const result = createMetadata(title, description, keywords, path);

    expect(result.title).toBe(`Test Title • ${packageInfo.name}`);
    expect(result.description).toBe(description);
    expect(result.keywords).toBe("keyword1,keyword2");
    expect(result.alternates.canonical).toBe(`https://loop.edu.pl/`);
  });
});
