import { createAxiosInstance } from "./service";

describe("createAxiosInstance", () => {
  // Returns an axios instance with the provided endpoint as baseURL if the endpoint does not start with "https"
  it('should return an axios instance with the provided endpoint as baseURL if the endpoint does not start with "https"', () => {
    const endpoint = "http://example.com";
    const axiosInstance = createAxiosInstance(endpoint);
    expect(axiosInstance.defaults.baseURL).toBe(endpoint);
  });

  // Returns an axios instance with the provided endpoint as baseURL and a httpsAgent with rejectUnauthorized set to false if the endpoint starts with "https"
  it('should return an axios instance with the provided endpoint as baseURL and a httpsAgent with rejectUnauthorized set to false if the endpoint starts with "https"', () => {
    const endpoint = "https://example.com";
    const axiosInstance = createAxiosInstance(endpoint);
    expect(axiosInstance.defaults.baseURL).toBe(endpoint);
    expect(axiosInstance.defaults.httpsAgent).toBeDefined();
  });

  // Returns an axios instance with the provided endpoint as baseURL even if the endpoint is an empty string
  it("should return an axios instance with the provided endpoint as baseURL even if the endpoint is an empty string", () => {
    const endpoint = "";
    const axiosInstance = createAxiosInstance(endpoint);
    expect(axiosInstance.defaults.baseURL).toBe(endpoint);
  });

  // The returned axios instance has default timeout of 0
  it("should return an axios instance with default timeout of 0", () => {
    const endpoint = "http://example.com";
    const axiosInstance = createAxiosInstance(endpoint);
    expect(axiosInstance.defaults.timeout).toBe(0);
  });
});
