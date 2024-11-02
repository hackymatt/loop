export function encodeUrl(text: string) {
  const polishCharsMap: { [key: string]: string } = {
    ą: "a",
    ć: "c",
    ę: "e",
    ł: "l",
    ń: "n",
    ó: "o",
    ś: "s",
    ź: "z",
    ż: "z",
    Ą: "A",
    Ć: "C",
    Ę: "E",
    Ł: "L",
    Ń: "N",
    Ó: "O",
    Ś: "S",
    Ź: "Z",
    Ż: "Z",
  };

  // Replace Polish characters with mapped equivalents
  text = text
    .split("")
    .map((char) => polishCharsMap[char] || char)
    .join("");

  // Allow letters (case-sensitive), numbers, spaces, periods, and hyphens only
  return text
    .replace(/[^a-zA-Z0-9\s.-]/g, "") // Keep case sensitivity
    .trim()
    .replace(/\s+/g, "-") // Convert spaces to hyphens
    .replace(/-+/g, "-"); // Remove multiple hyphens
}

export function decodeUrl(text: string) {
  return text;
}
