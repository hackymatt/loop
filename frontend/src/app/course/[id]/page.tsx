import { Metadata } from "next";

import { decodeUrl } from "src/utils/url-utils";
import { createMetadata } from "src/utils/create-metadata";

import CourseView from "src/sections/view/course-view";

// ----------------------------------------------------------------------

export default function CoursePage({ params }: { params: { id: string } }) {
  return <CourseView id={params.id} />;
}

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const decodedId = decodeUrl(params.id);

  const courseTitle = decodedId.slice(0, decodedId.lastIndexOf("-")).replace(/-/g, " ");

  const metadata = createMetadata(
    `Kurs ${courseTitle} - sprawdź program nauczania`,
    `Zapisz się na kurs ${courseTitle} w loop i naucz się programować. Oferujemy praktyczne lekcje online z certyfikatem ukończenia oraz wsparcie doświadczonych instruktorów.`,
    [
      `kurs ${courseTitle}`,
      "kursy programowania",
      "szkoła programowania loop",
      "kurs programowania",
    ],
  );

  return {
    title: metadata.title,
    description: metadata.description,
    keywords: metadata.keywords,
  };
}
