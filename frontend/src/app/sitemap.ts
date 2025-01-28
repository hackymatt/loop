import { MetadataRoute } from "next";

import { paths } from "src/routes/paths";

import { ENV } from "src/config-global";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const env = ENV === "PROD" ? "" : `${ENV.toLocaleLowerCase()}.`;

  return [
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
}
