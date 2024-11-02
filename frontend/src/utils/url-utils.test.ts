import { decodeUrl, encodeUrl } from "./url-utils";

describe("encodeUrl", () => {
  // Converts Polish characters to their mapped equivalents
  it("should convert Polish characters to their mapped equivalents", () => {
    const input = "Zażółć gęślą jaźń";
    const expectedOutput = "Zazolc-gesla-jazn";
    expect(encodeUrl(input)).toBe(expectedOutput);
  });

  // Handles empty string input
  it("should return an empty string when input is empty", () => {
    const input = "";
    const expectedOutput = "";
    expect(encodeUrl(input)).toBe(expectedOutput);
  });
});

describe("decodeUrl", () => {
  // Decode a simple encoded URL string
  it("should return the original string when given a simple encoded URL", () => {
    const encodedUrl = "https://example.com/path";
    const result = decodeUrl(encodedUrl);
    expect(result).toBe(encodedUrl);
  });

  // Handle an empty string input
  it("should return an empty string when input is an empty string", () => {
    const result = decodeUrl("");
    expect(result).toBe("");
  });
});
