import packageInfo from "package.json";

// ----------------------------------------------------------------------

export const createMetadata = (
  title?: string,
  description?: string,
  keywords?: string[],
  path?: string,
) => {
  const defaultMetadata = {
    title: "Szkoła programowania",
    description:
      "Platforma firmy loop oferującej kursy programowania online dla przyszłych i obecnych programistów",
    keywords: [
      "programowanie dla początkujących",
      "kursy programowania online",
      "nauka programowania",
      "szkoła programowania online",
      "certyfikat programowania",
      "kursy Python",
      "kursy JavaScript",
      "kursy TypeScript",
      "kursy C++",
      "kursy Git",
      "kursy programistyczne",
      "loop szkoła programowania",
      "loop",
    ],
  };

  const location = path ? `${path}/` : "/";

  return {
    title: `${title ?? defaultMetadata.title} • ${packageInfo.name}`,
    description: description ?? defaultMetadata.description,
    keywords: (keywords ?? defaultMetadata.keywords).join(","),
    alternates: {
      canonical: `https://loop.edu.pl${location}`,
    },
    openGraph: {
      type: "website",
      url: `https://loop.edu.pl${location}`,
      images: "https://loop.edu.pl/logo/logo.svg",
      title: `${title ?? defaultMetadata.title} • ${packageInfo.name}`,
      description: description ?? defaultMetadata.description,
    },
  };
};
