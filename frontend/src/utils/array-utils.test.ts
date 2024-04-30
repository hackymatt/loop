import { haveCommonItems } from "./array-utils";

describe("haveCommonItems", () => {
  // Returns true when both arrays have at least one common item
  it("should return true when both arrays have at least one common item", () => {
    const arr1 = ["apple", "banana", "orange"];
    const arr2 = ["banana", "grapefruit", "kiwi"];
    const result = haveCommonItems(arr1, arr2);
    expect(result).toBe(true);
  });

  // Returns false when both arrays are empty
  it("should return false when both arrays are empty", () => {
    const arr1: string[] = [];
    const arr2: string[] = [];
    const result = haveCommonItems(arr1, arr2);
    expect(result).toBe(false);
  });
});
