"use client";

import { useBestReviews } from "src/api/reviews/best-reviews";
import { useBestLecturers } from "src/api/lecturers/best-lecturers";

import About from "../about/about";
import TeamAbout from "../team/team-about";
import AboutHero from "../about/about-hero";
import Newsletter from "../newsletter/newsletter";
import Testimonial from "../testimonial/testimonial";
import AboutCoreValues from "../about/about-core-values";

// ----------------------------------------------------------------------

export default function AboutView() {
  const { data: bestReviews } = useBestReviews();
  const { data: bestLecturers } = useBestLecturers();

  return (
    <>
      <AboutHero />

      <About />

      <AboutCoreValues />

      {bestLecturers?.length >= 4 && <TeamAbout members={bestLecturers} />}

      {bestReviews?.length >= 5 && <Testimonial testimonials={bestReviews} />}

      <Newsletter />
    </>
  );
}
