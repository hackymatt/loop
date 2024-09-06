export function romanize(num: number, result: string = ""): string {
  const romanNumerals: { [key: number]: string } = {
    1000: "M",
    900: "CM",
    500: "D",
    400: "CD",
    100: "C",
    90: "XC",
    50: "L",
    40: "XL",
    10: "X",
    9: "IX",
    5: "V",
    4: "IV",
    1: "I",
  };

  const keys = Object.keys(romanNumerals).map(Number).reverse();

  // Base case: when num is 0, return the accumulated result
  if (num === 0) {
    return result;
  }

  // Find the largest Roman numeral that fits into num
  const largestKey = keys.find((key) => num >= key)!;

  // Recur, subtracting the value of the found numeral and adding it to the result
  return romanize(num - largestKey, result + romanNumerals[largestKey]);
}
