import { formatQueryParams } from "./query-params";

describe("formatQueryParams", () => {
  // Should return an empty string when query is undefined
  it("should return an empty string when query is undefined", () => {
    const result = formatQueryParams(undefined);
    expect(result).toEqual("");
  });

  // Should return a formatted string with one query parameter
  it("should return a formatted string with one query parameter", () => {
    const query = { key: "value" };
    const result = formatQueryParams(query);
    expect(result).toEqual("key=value");
  });

  // Should return a formatted string with multiple query parameters
  it("should return a formatted string with multiple query parameters", () => {
    const query = { key1: "value1", key2: "value2" };
    const result = formatQueryParams(query);
    expect(result).toEqual("key1=value1&key2=value2");
  });

  // Should return an empty string when query is an empty object
  it("should return an empty string when query is an empty object", () => {
    const query = {};
    const result = formatQueryParams(query);
    expect(result).toEqual("");
  });

  // Should return a formatted string with query parameters containing empty values
  it("should return a formatted string with query parameters containing empty values", () => {
    const query = { key1: "", key2: "value2" };
    const result = formatQueryParams(query);
    expect(result).toEqual("key1=&key2=value2");
  });

  // Should return a formatted string with query parameters containing undefined values
  it("should return a formatted string with query parameters containing undefined values", () => {
    const query = { key1: undefined, key2: "value2" };
    const result = formatQueryParams(query);
    expect(result).toEqual("key1=&key2=value2");
  });
});
