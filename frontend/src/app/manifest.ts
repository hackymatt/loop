import { MetadataRoute } from "next";

import { ENV } from "src/config-global";

export default function manifest(): MetadataRoute.Manifest {
  const env = ENV.toLocaleLowerCase();
  return {
    theme_color: "#000000",
    background_color: "#ffffff",
    icons: [
      {
        purpose: "maskable",
        sizes: "512x512",
        src: `logo/pwa/${env}/maskable.png`,
        type: "image/png",
      },
      {
        purpose: "any",
        sizes: "512x512",
        src: `logo/pwa/${env}/rounded.png`,
        type: "image/png",
      },
    ],
    orientation: "any",
    display: "standalone",
    dir: "auto",
    lang: "pl-PL",
    name: `loop-${env}`,
    short_name: `loop-${env}`,
    start_url: "/",
  };
}
