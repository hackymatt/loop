import packageInfo from "package.json";

// ----------------------------------------------------------------------

export const createMetadata = (title?: string, description?: string, keywords?: string[]) => {
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
    ],
  };

  return {
    title: `${title ?? defaultMetadata.title} • ${packageInfo.name}`,
    description: description ?? defaultMetadata.description,
    keywords: (keywords ?? defaultMetadata.keywords).join(","),
  };
};
