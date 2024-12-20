"use client";

import { usePosts } from "src/api/posts/posts";
import { useBestCourses } from "src/api/courses/best-courses";
import { useBestReviews } from "src/api/reviews/best-reviews";
import { useBestLecturers } from "src/api/lecturers/best-lecturers";
import { useBestTechnologies } from "src/api/technologies/best-technologies";

import Team from "../team/team";
import Newsletter from "../newsletter/newsletter";
import LandingHero from "../landing/landing-hero";
import { LatestPosts } from "../posts/latest-posts";
import Testimonial from "../testimonial/testimonial";
import LandingServices from "../landing/landing-services";
import LandingIntroduce from "../landing/landing-introduce";
import LandingTechnologies from "../landing/landing-technologies";
import LandingFeaturedCourses from "../landing/landing-featured-courses";

// ----------------------------------------------------------------------

export default function HomeView() {
  const { data: bestReviews } = useBestReviews();
  const { data: bestCourses } = useBestCourses();
  const { data: technologies } = useBestTechnologies({
    courses_count_from: 1,
    sort_by: "-courses_count",
  });
  const { data: bestLecturers } = useBestLecturers();
  const { data: recentPosts } = usePosts({
    sort_by: "-publication_date",
    page_size: 3,
  });

  return (
    <>
      <LandingHero />

      <LandingIntroduce />

      <LandingServices />

      {bestCourses?.length >= 4 && <LandingFeaturedCourses courses={bestCourses} />}

      {technologies?.length >= 1 && <LandingTechnologies technologies={technologies} />}

      {bestLecturers?.length >= 4 && <Team members={bestLecturers} />}

      {bestReviews?.length >= 5 && <Testimonial testimonials={bestReviews} />}

      {recentPosts?.length === 3 && <LatestPosts posts={recentPosts} />}

      <Newsletter />
    </>
  );
}
