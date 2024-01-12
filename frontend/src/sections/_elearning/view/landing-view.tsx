"use client";

import { _members } from "src/_mock";
import { useBestCourses } from "src/api/courses/best-courses";
import { useBestReviews } from "src/api/reviews/best-reviews";
import { useTechnologies } from "src/api/technologies/technologies";
import { useBestLecturers } from "src/api/lecturers/best-lecturers";

import Team from "../team/team";
import LandingHero from "../landing/landing-hero";
import Testimonial from "../testimonial/testimonial";
import ElearningNewsletter from "../elearning-newsletter";
import LandingServices from "../landing/landing-services";
import LandingIntroduce from "../landing/landing-introduce";
import LandingCategories from "../landing/landing-categories";
import LandingFeaturedCourses from "../landing/landing-featured-courses";

// ----------------------------------------------------------------------

export default function LandingView() {
  const { data: bestReviews } = useBestReviews();
  const { data: bestCourses } = useBestCourses();
  const { data: technologies } = useTechnologies();
  const { data: bestLecturers } = useBestLecturers();

  return (
    <>
      <LandingHero />

      <LandingIntroduce />

      <LandingServices />

      {bestCourses?.length >= 4 && <LandingFeaturedCourses courses={bestCourses} />}

      {technologies?.length >= 1 && <LandingCategories categories={technologies} />}

      {bestLecturers?.length >= 4 && <Team members={bestLecturers} />}

      {bestReviews?.length >= 5 && <Testimonial testimonials={bestReviews} />}

      <ElearningNewsletter />
    </>
  );
}
