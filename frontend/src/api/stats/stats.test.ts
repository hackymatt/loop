import { Api } from "../service";
import { useStats, statsQuery } from "./stats";

describe("statsQuery", () => {
  // 'url' property is set to '/stats'
  it("should set the 'url' property to '/stats'", () => {
    const result = statsQuery();
    expect(result.url).toBe("/stats");
  });

  // 'queryFn' property is an async function that makes a GET request to the '/stats' endpoint of the API and returns an object with 'results' and 'count' properties
  it("should set the 'queryFn' property as an async function that makes a GET request to the '/stats' endpoint of the API and returns an object with 'results' and 'count' properties", async () => {
    const result = statsQuery();
    const data = { results: [], count: 0 };
    Api.get = jest.fn().mockResolvedValue({ data });
    const queryResult = await result.queryFn();
    expect(Api.get).toHaveBeenCalledWith("/stats");
    expect(queryResult).toEqual(data);
  });

  // Throws an error if the API call fails
  it("should throw an error if the API call fails", async () => {
    const result = statsQuery();
    Api.get = jest.fn().mockRejectedValue(new Error("API error"));
    await expect(result.queryFn()).rejects.toThrow("API error");
  });

  // 'queryKey' property is an array containing the non-null values of the 'url' property
  it("should set the 'queryKey' property as an array containing the non-null values of the 'url' property", () => {
    const result = statsQuery();
    expect(result.queryKey).toEqual(["/stats"]);
  });
});

describe("useStats", () => {
  // Returns data and rest object when useQuery returns successfully
  it("should return data and rest object when useQuery returns successfully", () => {
    // Arrange
    const queryKey = "testKey";
    const queryFn = jest.fn().mockResolvedValue({ results: [], count: 0 });
    const useQueryMock = jest
      .fn()
      .mockReturnValue({ data: { results: [], count: 0 }, isLoading: false, error: null });
    jest.mock("@tanstack/react-query", () => ({ useQuery: useQueryMock }));

    // Act
    const result = useStats();

    // Assert
    expect(useQueryMock).toHaveBeenCalledWith({ queryKey, queryFn });
    expect(result).toEqual({ data: [], isLoading: false, error: null });
  });
});
