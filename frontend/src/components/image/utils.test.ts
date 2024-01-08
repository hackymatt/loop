import { getRatio } from "./utils";

describe("getRatio", () => {
  // Returns the correct ratio value for valid input.
  it("should return the correct ratio value for valid input", () => {
    expect(getRatio("4/3")).toBe("calc(100% / 4 * 3)");
    expect(getRatio("3/4")).toBe("calc(100% / 3 * 4)");
    expect(getRatio("6/4")).toBe("calc(100% / 6 * 4)");
    expect(getRatio("4/6")).toBe("calc(100% / 4 * 6)");
    expect(getRatio("16/9")).toBe("calc(100% / 16 * 9)");
    expect(getRatio("9/16")).toBe("calc(100% / 9 * 16)");
    expect(getRatio("21/9")).toBe("calc(100% / 21 * 9)");
    expect(getRatio("9/21")).toBe("calc(100% / 9 * 21)");
  });

  // Returns "100%" for input "1/1".
  it('should return "100%" for input "1/1"', () => {
    expect(getRatio("1/1")).toBe("100%");
  });

  // Returns "calc(100% / 16 * 9)" for input "16/9".
  it('should return "calc(100% / 16 * 9)" for input "16/9"', () => {
    expect(getRatio("16/9")).toBe("calc(100% / 16 * 9)");
  });

  // Returns undefined for invalid input.
  it("should return undefined for invalid input", () => {
    expect(getRatio("invalid")).toBeUndefined();
    expect(getRatio("0/0")).toBeUndefined();
    expect(getRatio("1/0")).toBeUndefined();
  });

  // Returns undefined for input "0/0".
  it('should return undefined for input "0/0"', () => {
    expect(getRatio("0/0")).toBeUndefined();
  });

  // Returns undefined for input "1/0".
  it('should return undefined for input "1/0"', () => {
    expect(getRatio("1/0")).toBeUndefined();
  });
});
