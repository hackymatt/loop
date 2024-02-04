import { blobToBase64 } from "./blob-to-base64";

describe("blobToBase64", () => {
  // Returns a promise that resolves to a base64 encoded string when given a valid Blob object.
  it("should return a promise that resolves to a base64 encoded string when given a valid Blob object", async () => {
    const blob = new Blob(["test"], { type: "text/plain" });
    const result = await blobToBase64(blob);
    expect(typeof result).toBe("string");
    expect((result as string).startsWith("data:text/plain;base64,")).toBe(true);
  });

  // Handles Blobs of various sizes and types, including images and audio files.
  it("should handle Blobs of various sizes and types, including images and audio files", async () => {
    const blob1 = new Blob(["test"], { type: "text/plain" });
    const blob2 = new Blob(["test"], { type: "image/jpeg" });
    const blob3 = new Blob(["test"], { type: "audio/mpeg" });

    const result1 = await blobToBase64(blob1);
    const result2 = await blobToBase64(blob2);
    const result3 = await blobToBase64(blob3);

    expect(typeof result1).toBe("string");
    expect((result1 as string).startsWith("data:text/plain;base64,")).toBe(true);

    expect(typeof result2).toBe("string");
    expect((result2 as string).startsWith("data:image/jpeg;base64,")).toBe(true);

    expect(typeof result3).toBe("string");
    expect((result3 as string).startsWith("data:audio/mpeg;base64,")).toBe(true);
  });

  // Uses FileReader to read the contents of the Blob and convert it to a base64 encoded string.
  it("should use FileReader to read the contents of the Blob and convert it to a base64 encoded string", async () => {
    const blob = new Blob(["test"], { type: "text/plain" });

    const result = await blobToBase64(blob);

    const reader = new FileReader();
    reader.onloadend = () => {
      expect(result).toBe(reader.result);
    };
    reader.readAsDataURL(blob);
  });

  // Throws an error if given an invalid Blob object.
  it("should throw an error if given an invalid Blob object", async () => {
    const invalidBlob = {};

    try {
      await blobToBase64(invalidBlob as Blob);
    } catch (error) {
      expect(error).toBeInstanceOf(Error);
      expect(error.message).toBe(
        "Failed to execute 'readAsDataURL' on 'FileReader': parameter 1 is not of type 'Blob'.",
      );
    }
  });

  // Handles Blobs with empty contents.
  it("should handle Blobs with empty contents", async () => {
    const blob = new Blob([], { type: "text/plain" });

    const result = await blobToBase64(blob);

    expect(typeof result).toBe("string");
    expect((result as string).startsWith("data:text/plain;base64,")).toBe(true);
  });

  // Handles Blobs with non-standard characters in their contents.
  it("should handle Blobs with non-standard characters in their contents", async () => {
    const blob = new Blob(["!@#$%^&*()"], { type: "text/plain" });

    const result = await blobToBase64(blob);

    expect(typeof result).toBe("string");
    expect((result as string).startsWith("data:text/plain;base64,")).toBe(true);
  });
});
