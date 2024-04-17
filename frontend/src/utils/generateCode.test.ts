import { generateCode } from "./generateCode";

describe("generateCode", () => {
  // Should generate a random string of the specified length
  it("should generate a random string of the specified length when length is positive", () => {
    const length = 10;
    const result = generateCode(length);
    expect(result.length).toBe(length);
  });

  // Should throw an error if length is negative
  it("should throw an error if length is negative", () => {
    const length = -10;
    expect(() => generateCode(length)).toThrowError();
  });
});
