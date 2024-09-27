import { MetadataRoute } from "next";

import { ENV } from "src/config-global";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const env = ENV === "PROD" ? "" : `${ENV.toLocaleLowerCase()}.`;

  return [
    {
      url: `https://www.${env}loop.edu.pl`,
      lastModified: new Date().toISOString(),
      changeFrequency: "always",
      priority: 1,
    },
    {
      url: `https://www.${env}loop.edu.pl/courses`,
      lastModified: new Date().toISOString(),
      changeFrequency: "always",
      priority: 0.9,
    },
    {
      url: `https://www.${env}loop.edu.pl/teachers`,
      lastModified: new Date().toISOString(),
      changeFrequency: "monthly",
      priority: 0.5,
    },
    {
      url: `https://www.${env}loop.edu.pl/about`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.5,
    },
    {
      url: `https://www.${env}loop.edu.pl/contact`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.5,
    },
    {
      url: `https://www.${env}loop.edu.pl/login`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.9,
    },
    {
      url: `https://www.${env}loop.edu.pl/support`,
      lastModified: new Date().toISOString(),
      changeFrequency: "monthly",
      priority: 0.6,
    },
    {
      url: `https://www.${env}loop.edu.pl/privacy-policy`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.5,
    },
    {
      url: `https://www.${env}loop.edu.pl/terms-and-conditions`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.5,
    },
    {
      url: `https://www.${env}loop.edu.pl/tests/predisposition`,
      lastModified: new Date().toISOString(),
      changeFrequency: "yearly",
      priority: 0.5,
    },
  ];
}
