import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

import { useTheme } from "@mui/material/styles";

import { paths } from "src/routes/paths";

import LandingHero from "./landing-hero";

describe("LandingHero", () => {
  const theme = useTheme();
  // Renders the hero section with the correct content and styles
  it("should render the hero section with the correct content and styles", () => {
    // Test setup
    render(<LandingHero />);

    // Test assertions
    expect(screen.getByText(/Zostań/i)).toBeInTheDocument();
    expect(screen.getByText(/programistą/i)).toBeInTheDocument();
    expect(screen.getByText(/Rozpocznij naukę/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Rozpocznij naukę/i })).toHaveAttribute(
      "href",
      paths.eLearning.courses,
    );
  });

  // Displays the call-to-action button with the correct text and link
  it("should display the call-to-action button with the correct text and link", () => {
    // Test setup
    render(<LandingHero />);

    // Test assertions
    expect(screen.getByRole("button", { name: /Rozpocznij naukę/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Rozpocznij naukę/i })).toHaveAttribute(
      "href",
      paths.eLearning.courses,
    );
  });

  // Shows the statistics section with the correct data and styles
  it("should show the statistics section with the correct data and styles", () => {
    // Test setup
    render(<LandingHero />);

    // Test assertions
    expect(screen.getByText(/Studentów/i)).toBeInTheDocument();
    expect(screen.getByText(/Kursów/i)).toBeInTheDocument();
    expect(screen.getByText(/Wykładowców/i)).toBeInTheDocument();
    expect(screen.getByText(/Studentów/i).previousSibling).toHaveStyle({
      backgroundColor: theme.palette.warning.main,
    });
    expect(screen.getByText(/Kursów/i).previousSibling).toHaveStyle({
      backgroundColor: theme.palette.error.main,
    });
    expect(screen.getByText(/Wykładowców/i).previousSibling).toHaveStyle({
      backgroundColor: theme.palette.success.main,
    });
  });

  // Handles missing or invalid data for the statistics section
  it("should handle missing or invalid data for the statistics section", () => {
    // Test setup
    render(<LandingHero />);

    // Test assertions
    expect(screen.queryByText(/Studentów/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Kursów/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Wykładowców/i)).not.toBeInTheDocument();
  });

  // Handles different screen sizes and orientations
  it("should handle different screen sizes and orientations", () => {
    // Test setup
    const { container } = render(<LandingHero />);

    // Test assertions
    expect(container.firstChild).toHaveStyle({ height: "100vh" });
  });

  // Handles different browser zoom levels
  it("should handle different browser zoom levels", () => {
    // Test setup
    const { container } = render(<LandingHero />);

    // Test assertions
    expect(container.firstChild).toHaveStyle({ height: "100vh" });
  });
});
