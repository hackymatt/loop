import { MetadataRoute } from "next";

import { ENV } from "src/config-global";
import { getAllTechnologies } from "src/api/technologies/technologies";

import { ICourseByCategoryProps } from "src/types/course";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const technologies = await getAllTechnologies({
    courses_count_from: 1,
    sort_by: "-courses_count",
    page_size: 1000,
  });

  const env = ENV === "PROD" ? "" : `${ENV.toLocaleLowerCase()}.`;

  const coursesDetails: MetadataRoute.Sitemap = technologies?.map(
    (technology: ICourseByCategoryProps) => ({
      url: `https://www.${env}loop.edu.pl/courses/?technology_in=${technology.name}`,
      lastModified: new Date(),
      changeFrequency: "always",
      priority: 0.8,
    }),
  );

  return [
    {
      url: `https://www.${env}loop.edu.pl`,
      lastModified: new Date(),
      changeFrequency: "always",
      priority: 1,
    },
    {
      url: `https://www.${env}loop.edu.pl/courses`,
      lastModified: new Date(),
      changeFrequency: "always",
      priority: 0.9,
    },
    {
      url: `https://www.${env}loop.edu.pl/teachers`,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.5,
    },
    {
      url: `https://www.${env}loop.edu.pl/about`,
      lastModified: new Date(),
      changeFrequency: "yearly",
      priority: 0.5,
    },
    {
      url: `https://www.${env}loop.edu.pl/contact`,
      lastModified: new Date(),
      changeFrequency: "yearly",
      priority: 0.5,
    },
    {
      url: `https://www.${env}loop.edu.pl/login`,
      lastModified: new Date(),
      changeFrequency: "yearly",
      priority: 0.9,
    },
    {
      url: `https://www.${env}loop.edu.pl/support`,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.6,
    },
    {
      url: `https://www.${env}loop.edu.pl/privacy-policy`,
      lastModified: new Date(),
      changeFrequency: "yearly",
      priority: 0.5,
    },
    {
      url: `https://www.${env}loop.edu.pl/terms-and-conditions`,
      lastModified: new Date(),
      changeFrequency: "yearly",
      priority: 0.5,
    },
    ...coursesDetails,
  ];
}
