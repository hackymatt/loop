"use client";

import { _members, _coursePosts, _brandsColor, _testimonials } from "src/_mock";

import TeamAbout from "../team/team-about";
import ElearningNewsletter from "../newsletter";
import Testimonial from "../testimonial/testimonial";
import ElearningAbout from "../about/elearning-about";
import ElearningOurClients from "../elearning-our-clients";
import ElearningAboutHero from "../about/elearning-about-hero";
import ElearningAboutCoreValues from "../about/elearning-about-core-values";
import ElearningLatestPosts from "../../blog/elearning/elearning-latest-posts";

// ----------------------------------------------------------------------

export default function AboutView() {
  return (
    <>
      <ElearningAboutHero />

      <ElearningAbout />

      <ElearningAboutCoreValues />

      <TeamAbout members={_members} />

      <ElearningOurClients brands={_brandsColor} />

      <Testimonial testimonials={_testimonials} />

      <ElearningLatestPosts posts={_coursePosts.slice(0, 4)} />

      <ElearningNewsletter />
    </>
  );
}
