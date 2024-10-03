export function encodeUrl(text: string) {
  return encodeURIComponent(text).replace(/%20/g, "-");
}

export function decodeUrl(text: string) {
  return decodeURIComponent(text);
}
