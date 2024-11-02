function createSEOUrl(text: string) {
  return text
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9\s-]/g, "")
    .trim()
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-");
}

export function encodeUrl(text: string) {
  return createSEOUrl(encodeURIComponent(text).replace(/%20/g, "-"));
}

export function decodeUrl(text: string) {
  return decodeURIComponent(text);
}
