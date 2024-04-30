import { fData, fNumber, fPercent, fCurrency, fShortenNumber } from "./format-number";

describe("fNumber", () => {
  // Returns a formatted number string for valid input values.
  it("should return a formatted number string when input value is valid", () => {
    const inputValue = 1234.5678;
    const result = fNumber(inputValue);
    expect(result).toEqual("1234,57");
  });

  // Returns NaN for invalid input values.
  it("should return NaN when input value is invalid", () => {
    const inputValue = "abc";
    const result = fNumber(inputValue);
    expect(result).toEqual("NaN");
  });
});

describe("fCurrency", () => {
  // Returns a formatted currency string when given a valid number input
  it("should return a formatted currency string when given a valid number input", () => {
    const result = fCurrency(1000);
    expect(result.replace(/\s/g, "")).toEqual("1000,00 zł".replace(/\s/g, ""));
  });

  // Returns an empty string when given a non-numeric string input
  it("should return an empty string when given a non-numeric string input", () => {
    const result = fCurrency("abc");
    expect(result.replace(/\s/g, "")).toEqual("NaN zł".replace(/\s/g, ""));
  });
});

describe("fPercent", () => {
  // Should return an empty string when inputValue is null
  it("should return an empty string when inputValue is null", () => {
    const result = fPercent(null);
    expect(result).toBe("");
  });

  // Should return an empty string when inputValue is an empty string
  it("should return an empty string when inputValue is an empty string", () => {
    const result = fPercent("");
    expect(result).toBe("");
  });
});

describe("fShortenNumber", () => {
  // Returns empty string when inputValue is null
  it("should return empty string when inputValue is null", () => {
    const result = fShortenNumber(null);
    expect(result).toBe("");
  });
});

describe("fData", () => {
  // Returns an empty string when inputValue is null or undefined
  it("should return an empty string when inputValue is null", () => {
    const inputValue = null;
    const result = fData(inputValue);
    expect(result).toBe("");
  });

  // Returns formatted string with correct unit and decimal places for very large inputValues
  it("should return formatted string with correct unit and decimal places for very large inputValues", () => {
    const inputValue = 1234567890;
    const result = fData(inputValue);
    expect(result).toBe("1.15 Gb");
  });

  // Returns formatted string with correct unit and decimal places for very large inputValues
  it("should return formatted string with correct unit and decimal places for very large inputValues", () => {
    const inputValue = 9876543210;
    const result = fData(inputValue);
    expect(result).toBe("9.2 Gb");
  });
});
