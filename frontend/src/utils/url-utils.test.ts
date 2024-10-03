import { decodeUrl, encodeUrl } from "./url-utils";

describe("encodeUrl", () => {
  // Encodes a simple alphanumeric string correctly
  it("should encode alphanumeric string with hyphens instead of spaces", () => {
    const input = "hello world";
    const expectedOutput = "hello-world";
    const result = encodeUrl(input);
    expect(result).toBe(expectedOutput);
  });

  // Encodes an empty string without errors
  it("should return an empty string when input is empty", () => {
    const input = "";
    const expectedOutput = "";
    const result = encodeUrl(input);
    expect(result).toBe(expectedOutput);
  });
});

describe("decodeUrl", () => {
  // Decodes a standard URL-encoded string correctly
  it("should decode a standard URL-encoded string correctly", () => {
    const encodedString = "Hello%20World%21";
    const expectedDecodedString = "Hello World!";
    const result = decodeUrl(encodedString);
    expect(result).toBe(expectedDecodedString);
  });

  // Handles empty strings without errors
  it("should return an empty string when input is an empty string", () => {
    const encodedString = "";
    const expectedDecodedString = "";
    const result = decodeUrl(encodedString);
    expect(result).toBe(expectedDecodedString);
  });
});
