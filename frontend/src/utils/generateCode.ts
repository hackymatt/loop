export function generateCode(length: number) {
  if (length < 0) {
    throw new Error("Length cannot be negative");
  }

  const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
  const string_length = length;
  let randomString = "";
  for (let i = 0; i < string_length; i += 1) {
    const position = Math.floor(Math.random() * chars.length);
    randomString += chars[position];
  }
  return randomString;
}
