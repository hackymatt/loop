"use client";

import { _members } from "src/_mock";
import { useBestCourses } from "src/api/courses/best-courses";
import { useBestReviews } from "src/api/reviews/best-reviews";
import { useTechnologies } from "src/api/technologies/technologies";

import LandingHero from "../landing/landing-hero";
import ElearningTeam from "../team/elearning-team";
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

  return (
    <>
      <LandingHero />

      <LandingIntroduce />

      <LandingServices />

      {bestCourses?.length >= 4 && <LandingFeaturedCourses courses={bestCourses} />}

      {technologies?.length >= 1 && <LandingCategories categories={technologies.slice(0, 9)} />}

      <ElearningTeam members={_members.slice(0, 4)} />

      {bestReviews?.length >= 5 && <Testimonial testimonials={bestReviews} />}

      <ElearningNewsletter />
    </>
  );
}
