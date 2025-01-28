import { MetadataRoute } from "next";

import { paths } from "src/routes/paths";

import { encodeUrl } from "src/utils/url-utils";

import { ENV } from "src/config-global";
import { postsQuery } from "src/api/posts/posts";
import { coursesQuery } from "src/api/courses/courses";
import { lecturersQuery } from "src/api/lecturers/lecturers";
import { technologiesQuery } from "src/api/technologies/technologies";

import { IPostProps } from "src/types/blog";
import { ITeamMemberProps } from "src/types/team";
import { ICourseProps, ICourseByTechnologyProps } from "src/types/course";

async function getCourses(env: string) {
  const { queryFn } = coursesQuery({ page_size: -1 });

  const { results: courses } = await queryFn();

  return courses?.map((course: ICourseProps) => {
    const path = `${course.slug}-${course.id}`;
    return {
      url: `https://${env}loop.edu.pl${paths.course}/${encodeUrl(path)}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "monthly",
      priority: 0.8,
    };
  });
}

async function getTechnologies(env: string) {
  const { queryFn } = technologiesQuery({ page_size: -1 });

  const { results: technologies } = await queryFn();

  return technologies?.map((technology: ICourseByTechnologyProps) => ({
    url: `https://${env}loop.edu.pl${paths.courses}?technology_in=${technology.name}/`,
    lastModified: new Date().toISOString(),
    changeFrequency: "monthly",
    priority: 0.8,
  }));
}

async function getTeachers(env: string) {
  const { queryFn } = lecturersQuery({ page_size: -1 });

  const { results: teachers } = await queryFn();

  return teachers?.map((teacher: ITeamMemberProps) => {
    const path = `${teacher.name}-${teacher.id}`;
    return {
      url: `https://${env}loop.edu.pl${paths.teacher}/${encodeUrl(path)}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "monthly",
      priority: 0.8,
    };
  });
}

async function getPosts(env: string) {
  const { queryFn } = postsQuery({ page_size: -1 });

  const { results: posts } = await queryFn();

  return posts?.map((post: IPostProps) => {
    const path = `${post.title}-${post.id}`;
    return {
      url: `https://${env}loop.edu.pl${paths.post}/${encodeUrl(path)}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "monthly",
      priority: 0.8,
    };
  });
}

async function fetchData(env: string) {
  try {
    const courses = await getCourses(env);
    const technologies = await getTechnologies(env);
    const teachers = await getTeachers(env);
    const posts = await getPosts(env);

    return [...courses, ...technologies, ...teachers, ...posts];
  } catch (error) {
    return [];
  }
}

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const env = ENV === "PROD" ? "" : `${ENV.toLocaleLowerCase()}.`;

  const dynamicRoutes = await fetchData(env);

  const staticRoutes = [
    {
      url: `https://${env}loop.edu.pl/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "always",
      priority: 1,
    },
    {
      url: `https://${env}loop.edu.pl${paths.courses}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "always",
      priority: 0.9,
    },
    {
      url: `https://${env}loop.edu.pl${paths.teachers}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "monthly",
      priority: 0.5,
    },
    {
      url: `https://${env}loop.edu.pl${paths.posts}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "always",
      priority: 0.8,
    },
    {
      url: `https://${env}loop.edu.pl${paths.about}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.5,
    },
    {
      url: `https://${env}loop.edu.pl${paths.contact}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.5,
    },
    {
      url: `https://${env}loop.edu.pl${paths.wishlist}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.9,
    },
    {
      url: `https://${env}loop.edu.pl${paths.cart}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.9,
    },
    {
      url: `https://${env}loop.edu.pl${paths.login}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.9,
    },
    {
      url: `https://${env}loop.edu.pl${paths.register}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.9,
    },
    {
      url: `https://${env}loop.edu.pl${paths.forgotPassword}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.9,
    },
    {
      url: `https://${env}loop.edu.pl${paths.support}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "monthly",
      priority: 0.6,
    },
    {
      url: `https://${env}loop.edu.pl${paths.privacyPolicy}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.5,
    },
    {
      url: `https://${env}loop.edu.pl${paths.termsAndConditions}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.5,
    },
    {
      url: `https://${env}loop.edu.pl${paths.tests.predisposition}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.5,
    },
    {
      url: `https://${env}loop.edu.pl${paths.newsletter.subscribe}/`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.5,
    },
  ];

  return [...staticRoutes, ...dynamicRoutes];
}
