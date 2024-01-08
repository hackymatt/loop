import "@testing-library/jest-dom";
import { render } from "@testing-library/react";

import HeroIllustration from "./hero-illustration";

describe("HeroIllustration", () => {
  // Renders the component with the correct dimensions and positioning
  it("should render the component with the correct dimensions and positioning", () => {
    const { container } = render(<HeroIllustration />);
    const box = container.firstChild;

    expect(box).toHaveStyle({
      width: "670px",
      height: "670px",
      display: "flex",
      alignItems: "center",
      position: "relative",
      justifyContent: "center",
    });
  });

  // Renders all images with the correct alt text and source
  it("should render all images with the correct alt text and source", () => {
    const { container } = render(<HeroIllustration />);
    const images = container.querySelectorAll("img");

    images.forEach((image) => {
      expect(image).toHaveAttribute("alt");
      expect(image).toHaveAttribute("src");
    });
  });

  // None of the images have a source or alt text
  it("should not have any images without a source or alt text", () => {
    const { container } = render(<HeroIllustration />);
    const images = container.querySelectorAll("img");

    images.forEach((image) => {
      expect(image).not.toHaveAttribute("alt", "");
      expect(image).not.toHaveAttribute("src", "");
    });
  });

  // One or more of the images have an invalid source or alt text
  it("should not have any images with an invalid source or alt text", () => {
    const { container } = render(<HeroIllustration />);
    const images = container.querySelectorAll("img");

    images.forEach((image) => {
      expect(image).not.toHaveAttribute("alt", "invalid");
      expect(image).not.toHaveAttribute("src", "invalid");
    });
  });
});
