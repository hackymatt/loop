"use client";

import { useBestReviews } from "src/api/reviews/best-reviews";
import { _courses, _members, _coursePosts, _coursesByCategories } from "src/_mock";

import LandingHero from "../landing/landing-hero";
import ElearningTeam from "../team/elearning-team";
import Testimonial from "../testimonial/testimonial";
import ElearningNewsletter from "../elearning-newsletter";
import LandingServices from "../landing/landing-services";
import LandingIntroduce from "../landing/landing-introduce";
import ElearningDownloadApp from "../elearning-download-app";
import ElearningLatestPosts from "../../blog/elearning/elearning-latest-posts";
import ElearningLandingCategories from "../landing/elearning-landing-categories";
import ElearningLandingFeaturedCourses from "../landing/elearning-landing-featured-courses";

// ----------------------------------------------------------------------

export default function LandingView() {
  const { data: testimonials } = useBestReviews();
  return (
    <>
      <LandingHero />

      <LandingIntroduce />

      <LandingServices />

      <ElearningLandingFeaturedCourses courses={_courses} />

      <ElearningLandingCategories categories={_coursesByCategories} />

      <ElearningTeam members={_members.slice(0, 4)} />

      {testimonials?.length >= 5 && <Testimonial testimonials={testimonials} />}

      <ElearningLatestPosts posts={_coursePosts.slice(0, 4)} />

      <ElearningDownloadApp />

      <ElearningNewsletter />
    </>
  );
}
