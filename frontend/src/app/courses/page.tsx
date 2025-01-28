import { Metadata } from "next";

import { paths } from "src/routes/paths";

import { createMetadata } from "src/utils/create-metadata";

import CoursesView from "src/sections/view/courses-view";

// ----------------------------------------------------------------------

export default function CoursesPage() {
  return <CoursesView />;
}

export function generateMetadata({
  searchParams,
}: {
  searchParams: { technology_in?: string };
}): Metadata {
  const technology = searchParams.technology_in;

  const technologies = technology ? technology.split(",") : [];

  const title =
    technologies.length === 1
      ? `Kursy ${technologies[0]} - sprawdź ofertę`
      : "Kursy programowania online - sprawdź ofertę";

  const description =
    technologies.length === 1
      ? `Odkryj ofertę kursów programowania w loop. Nauka ${technologies[0]} oraz innych od podstaw z certyfikatem. Zajęcia prowadzone online przez doświadczonych instruktorów.`
      : "Odkryj ofertę kursów programowania w loop. Nauka Python, JavaScript, C++ oraz innych od podstaw z certyfikatem. Zajęcia prowadzone online przez doświadczonych instruktorów.";

  const path =
    technologies.length === 1 ? `${paths.courses}?technology_in=${technologies[0]}` : paths.courses;

  return createMetadata(
    title,
    description,
    [
      "oferta kursów programowania",
      "kursy Python",
      "kursy JavaScript",
      "kursy C++",
      "programowanie dla początkujących",
      "kursy programistyczne",
      "certyfikat programowania",
      "nauka kodowania",
      "nauka programowania",
      "lekcje programowania online",
      "loop kursy programowania",
    ],
    path,
  );
}
