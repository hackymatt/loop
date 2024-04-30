import * as ReactQuery from "@tanstack/react-query";

import { Api } from "../service";
import { useUserDetails, userDetailsQuery } from "./details";

describe("userDetailsQuery", () => {
  // Returns a valid query object with url, queryFn and queryKey properties
  it("should return a valid query object", () => {
    const query = userDetailsQuery();
    expect(query).toHaveProperty("url");
    expect(query).toHaveProperty("queryFn");
    expect(query).toHaveProperty("queryKey");
  });

  // Throws an error if the Api.get method returns an error
  it("should throw an error when Api.get returns an error", async () => {
    const error = new Error("API error");
    const getMock = jest.spyOn(Api, "get").mockRejectedValue(error);

    await expect(userDetailsQuery().queryFn()).rejects.toThrowError(error);

    getMock.mockRestore();
  });
});

describe("useUserDetails", () => {
  // Returns data and rest object when useQuery hook is called with queryKey and queryFn from userDetailsQuery
  it("should return data and rest object when useQuery hook is called with queryKey and queryFn from userDetailsQuery", () => {
    // Mock the userDetailsQuery function
    jest.mock("./details", () => ({
      userDetailsQuery: jest.fn(() => ({
        queryKey: "testKey",
        queryFn: jest.fn(),
      })),
    }));

    // Mock the useQuery hook
    jest.spyOn(ReactQuery, "useQuery").mockImplementation(
      jest.fn().mockReturnValue({
        data: { results: "testData" },
        isLoading: false,
        isError: false,
        error: null,
      }),
    );

    // Call the useUserDetails function
    const result = useUserDetails();

    // Assert the expected result
    expect(result).toEqual({
      data: "testData",
      isLoading: false,
      isError: false,
      error: null,
    });
  });

  // Returns undefined when data is truthy but does not have results property
  it("should return undefined when data is truthy but does not have results property", () => {
    // Mock the userDetailsQuery function
    jest.mock("./details", () => ({
      userDetailsQuery: jest.fn(() => ({
        queryKey: "testKey",
        queryFn: jest.fn(),
      })),
    }));

    // Mock the useQuery hook
    jest.spyOn(ReactQuery, "useQuery").mockImplementation(
      jest.fn().mockReturnValue({
        data: { testProperty: "testValue" },
        isLoading: false,
        isError: false,
        error: null,
      }),
    );

    // Call the useUserDetails function
    const result = useUserDetails();

    // Assert the expected result
    expect(result).toEqual({ data: undefined, error: null, isError: false, isLoading: false });
  });
});
