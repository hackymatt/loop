import { MetadataRoute } from "next";

import { ENV } from "src/config-global";

export default function robots(): MetadataRoute.Robots {
  const env = ENV === "PROD" ? "" : `${ENV.toLocaleLowerCase()}.`;

  const allRules = { userAgent: "*", allow: "/$", disallow: "/" };
  const prodRules = {
    userAgent: ["Googlebot", "Applebot", "Bingbot"],
    allow: ["/"],
    disallow: [""],
  };

  const rules = ENV === "PROD" ? [prodRules, allRules] : [allRules];

  return {
    rules,
    sitemap: `https://www.${env}loop.edu.pl/sitemap.xml`,
  };
}
