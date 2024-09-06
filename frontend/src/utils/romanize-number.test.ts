import { romanize } from "./romanize-number";

describe("romanize", () => {
  // converts single-digit numbers to Roman numerals correctly
  it("should convert single-digit numbers to Roman numerals correctly", () => {
    expect(romanize(1)).toBe("I");
    expect(romanize(2)).toBe("II");
    expect(romanize(3)).toBe("III");
    expect(romanize(4)).toBe("IV");
    expect(romanize(5)).toBe("V");
    expect(romanize(6)).toBe("VI");
    expect(romanize(7)).toBe("VII");
    expect(romanize(8)).toBe("VIII");
    expect(romanize(9)).toBe("IX");
  });

  // handles the smallest number (1) correctly
  it('should return "I" when the input is 1', () => {
    expect(romanize(1)).toBe("I");
  });
});
