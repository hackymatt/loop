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
  // Returns an object with 'data' property containing an array of 'IStats' objects when the query is successful
  it("should return an object with 'data' property containing an array of 'IStats' objects when the query is successful", () => {
    // Mock the statsQuery function
    const mockStatsQuery = jest.fn(() => ({
      queryKey: ["stats"],
      queryFn: jest.fn().mockResolvedValue({ results: [{}, {}], count: 2 }),
    }));

    // Mock the useQuery function
    const mockUseQuery = jest.fn(() => ({
      data: { results: [{}, {}] },
      isLoading: false,
      isError: false,
    }));

    // Replace the original functions with the mock functions
    jest.mock("@tanstack/react-query", () => ({
      useQuery: mockUseQuery,
    }));
    jest.mock("../service", () => ({
      statsQuery: mockStatsQuery,
    }));

    // Call the useStats function
    const result = useStats();

    // Assertions
    expect(mockStatsQuery).toHaveBeenCalled();
    expect(mockUseQuery).toHaveBeenCalledWith({
      queryKey: ["stats"],
      queryFn: expect.any(Function),
    });
    expect(result).toEqual({ data: [{}, {}], isLoading: false, isError: false });
  });

  // Returns an object with 'isLoading' property set to true when the query is in progress
  it("should return an object with 'isLoading' property set to true when the query is in progress", () => {
    // Mock the statsQuery function
    const mockStatsQuery = jest.fn(() => ({
      queryKey: ["stats"],
      queryFn: jest.fn().mockResolvedValue({ results: [], count: 0 }),
    }));

    // Mock the useQuery function
    const mockUseQuery = jest.fn(() => ({
      data: null,
      isLoading: true,
      isError: false,
    }));

    // Replace the original functions with the mock functions
    jest.mock("@tanstack/react-query", () => ({
      useQuery: mockUseQuery,
    }));
    jest.mock("../service", () => ({
      statsQuery: mockStatsQuery,
    }));

    // Call the useStats function
    const result = useStats();

    // Assertions
    expect(mockStatsQuery).toHaveBeenCalled();
    expect(mockUseQuery).toHaveBeenCalledWith({
      queryKey: ["stats"],
      queryFn: expect.any(Function),
    });
    expect(result).toEqual({ data: null, isLoading: true, isError: false });
  });

  // Returns an object with 'isError' property set to true when the query fails
  it("should return an object with 'isError' property set to true when the query fails", () => {
    // Mock the statsQuery function
    const mockStatsQuery = jest.fn(() => ({
      queryKey: ["stats"],
      queryFn: jest.fn().mockRejectedValue(new Error("Query failed")),
    }));

    // Mock the useQuery function
    const mockUseQuery = jest.fn(() => ({
      data: null,
      isLoading: false,
      isError: true,
    }));

    // Replace the original functions with the mock functions
    jest.mock("@tanstack/react-query", () => ({
      useQuery: mockUseQuery,
    }));
    jest.mock("../service", () => ({
      statsQuery: mockStatsQuery,
    }));

    // Call the useStats function
    const result = useStats();

    // Assertions
    expect(mockStatsQuery).toHaveBeenCalled();
    expect(mockUseQuery).toHaveBeenCalledWith({
      queryKey: ["stats"],
      queryFn: expect.any(Function),
    });
    expect(result).toEqual({ data: null, isLoading: false, isError: true });
  });

  // Returns an object with 'data' property set to null when the query fails
  it("should return an object with 'data' property set to null when the query fails", () => {
    // Mock the statsQuery function
    const mockStatsQuery = jest.fn(() => ({
      queryKey: ["stats"],
      queryFn: jest.fn().mockRejectedValue(new Error("Query failed")),
    }));

    // Mock the useQuery function
    const mockUseQuery = jest.fn(() => ({
      data: null,
      isLoading: false,
      isError: true,
    }));

    // Replace the original functions with the mock functions
    jest.mock("@tanstack/react-query", () => ({
      useQuery: mockUseQuery,
    }));
    jest.mock("../service", () => ({
      statsQuery: mockStatsQuery,
    }));

    // Call the useStats function
    const result = useStats();

    // Assertions
    expect(mockStatsQuery).toHaveBeenCalled();
    expect(mockUseQuery).toHaveBeenCalledWith({
      queryKey: ["stats"],
      queryFn: expect.any(Function),
    });
    expect(result).toEqual({ data: null, isLoading: false, isError: true });
  });

  // Returns an object with 'data' property set to null when the query is in progress
  it("should return an object with 'data' property set to null when the query is in progress", () => {
    // Mock the statsQuery function
    const mockStatsQuery = jest.fn(() => ({
      queryKey: ["stats"],
      queryFn: jest.fn().mockResolvedValue({ results: [], count: 0 }),
    }));

    // Mock the useQuery function
    const mockUseQuery = jest.fn(() => ({
      data: null,
      isLoading: true,
      isError: false,
    }));

    // Replace the original functions with the mock functions
    jest.mock("@tanstack/react-query", () => ({
      useQuery: mockUseQuery,
    }));
    jest.mock("../service", () => ({
      statsQuery: mockStatsQuery,
    }));

    // Call the useStats function
    const result = useStats();

    // Assertions
    expect(mockStatsQuery).toHaveBeenCalled();
    expect(mockUseQuery).toHaveBeenCalledWith({
      queryKey: ["stats"],
      queryFn: expect.any(Function),
    });
    expect(result).toEqual({ data: null, isLoading: true, isError: false });
  });

  // Returns an object with 'isLoading' property set to false when the query fails
  it("should return an object with 'isLoading' property set to false when the query fails", () => {
    // Mock the statsQuery function
    const mockStatsQuery = jest.fn(() => ({
      queryKey: ["stats"],
      queryFn: jest.fn().mockRejectedValue(new Error("Query failed")),
    }));

    // Mock the useQuery function
    const mockUseQuery = jest.fn(() => ({
      data: null,
      isLoading: false,
      isError: true,
    }));

    // Replace the original functions with the mock functions
    jest.mock("@tanstack/react-query", () => ({
      useQuery: mockUseQuery,
    }));
    jest.mock("../service", () => ({
      statsQuery: mockStatsQuery,
    }));

    // Call the useStats function
    const result = useStats();

    // Assertions
    expect(mockStatsQuery).toHaveBeenCalled();
    expect(mockUseQuery).toHaveBeenCalledWith({
      queryKey: ["stats"],
      queryFn: expect.any(Function),
    });
    expect(result).toEqual({ data: null, isLoading: false, isError: true });
  });
});
