"use client";

import { useBestCourses } from "src/api/courses/best-courses";
import { useBestReviews } from "src/api/reviews/best-reviews";
import { useTechnologies } from "src/api/technologies/technologies";
import { useBestLecturers } from "src/api/lecturers/best-lecturers";

import Team from "../team/team";
import Newsletter from "../newsletter/newsletter";
import LandingHero from "../landing/landing-hero";
import Testimonial from "../testimonial/testimonial";
import LandingServices from "../landing/landing-services";
import LandingIntroduce from "../landing/landing-introduce";
import LandingCategories from "../landing/landing-categories";
import LandingFeaturedCourses from "../landing/landing-featured-courses";

// ----------------------------------------------------------------------

export default function HomeView() {
  const { data: bestReviews } = useBestReviews();
  const { data: bestCourses } = useBestCourses();
  const { data: technologies } = useTechnologies({ sort_by: "-courses_count" });
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

      <Newsletter />
    </>
  );
}
