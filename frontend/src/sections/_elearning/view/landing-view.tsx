"use client";

import { useBestReviews } from "src/api/reviews/best-reviews";
import { useBestCourses } from "src/api/courses/best-courses";
import { _members, _coursePosts, _coursesByCategories } from "src/_mock";

import LandingHero from "../landing/landing-hero";
import ElearningTeam from "../team/elearning-team";
import Testimonial from "../testimonial/testimonial";
import ElearningNewsletter from "../elearning-newsletter";
import LandingServices from "../landing/landing-services";
import LandingIntroduce from "../landing/landing-introduce";
import ElearningDownloadApp from "../elearning-download-app";
import LandingFeaturedCourses from "../landing/landing-featured-courses";
import ElearningLatestPosts from "../../blog/elearning/elearning-latest-posts";
import ElearningLandingCategories from "../landing/elearning-landing-categories";

// ----------------------------------------------------------------------

export default function LandingView() {
  const { data: bestReviews } = useBestReviews();
  const { data: bestCourses } = useBestCourses();

  return (
    <>
      <LandingHero />

      <LandingIntroduce />

      <LandingServices />

      {bestCourses?.length >= 4 && <LandingFeaturedCourses courses={bestCourses} />}

      <ElearningLandingCategories categories={_coursesByCategories} />

      <ElearningTeam members={_members.slice(0, 4)} />

      {bestReviews?.length >= 5 && <Testimonial testimonials={bestReviews} />}

      <ElearningLatestPosts posts={_coursePosts.slice(0, 4)} />

      <ElearningDownloadApp />

      <ElearningNewsletter />
    </>
  );
}
