"use client";

import { _members, _coursePosts, _brandsColor, _testimonials } from "src/_mock";

import Testimonial from "../testimonial/testimonial";
import ElearningAbout from "../about/elearning-about";
import ElearningNewsletter from "../elearning-newsletter";
import ElearningOurClients from "../elearning-our-clients";
import TeamElearningAbout from "../team/elearning-team-about";
import ElearningAboutHero from "../about/elearning-about-hero";
import ElearningAboutCoreValues from "../about/elearning-about-core-values";
import ElearningLatestPosts from "../../blog/elearning/elearning-latest-posts";

// ----------------------------------------------------------------------

export default function ElearningAboutView() {
  return (
    <>
      <ElearningAboutHero />

      <ElearningAbout />

      <ElearningAboutCoreValues />

      <TeamElearningAbout members={_members} />

      <ElearningOurClients brands={_brandsColor} />

      <Testimonial testimonials={_testimonials} />

      <ElearningLatestPosts posts={_coursePosts.slice(0, 4)} />

      <ElearningNewsletter />
    </>
  );
}
