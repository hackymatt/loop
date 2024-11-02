import { Metadata } from "next";

import { ViewUtil } from "src/utils/page-utils";
import { decodeUrl } from "src/utils/url-utils";
import { createMetadata } from "src/utils/create-metadata";

import TeacherView from "src/sections/view/teacher-view";

// ----------------------------------------------------------------------

export default function TeacherPage({ params }: { params: { id: string } }) {
  return <ViewUtil defaultView={<TeacherView id={params.id} />} />;
}

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const decodedId = decodeUrl(params.id);
  const teacherName = decodedId.slice(0, decodedId.lastIndexOf("-")).replace(/-/g, " ");

  const metadata = createMetadata(
    `Instruktor: ${teacherName}`,
    `Poznaj ${teacherName} — doświadczonego instruktora w loop. Sprawdź jego profil, lekcje, które prowadzi, oraz opinie studentów. Rozpocznij naukę programowania pod okiem profesjonalisty!`,
    [
      "profil instruktora",
      "instruktor programowania",
      "loop instruktor",
      "nauczyciel programowania",
      "opinie o instruktorze",
      "kursy prowadzone przez instruktora",
      "doświadczenie instruktora",
      "specjalizacje instruktora",
      "mentor programistyczny",
      "szkoła programowania",
    ],
  );

  return {
    title: metadata.title,
    description: metadata.description,
    keywords: metadata.keywords,
  };
}
