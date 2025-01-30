import { Metadata } from "next";

import { paths } from "src/routes/paths";

import { decodeUrl } from "src/utils/url-utils";
import { createMetadata } from "src/utils/create-metadata";

import { lecturerQuery } from "src/api/lecturers/lecturer";

import TeacherView from "src/sections/view/teacher-view";

// ----------------------------------------------------------------------

export default function TeacherPage({ params }: { params: { id: string } }) {
  return <TeacherView id={params.id} />;
}

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const decodedId = decodeUrl(params.id);
  const recordId = decodedId.slice(decodedId.lastIndexOf("-") + 1);

  const { queryFn } = lecturerQuery(recordId);

  const { results: teacher } = await queryFn();

  const teacherName =
    teacher?.name ?? decodedId.slice(0, decodedId.lastIndexOf("-")).replace(/-/g, " ");
  const teacherDescription = teacher?.description
    ? teacher.description
    : `Doświadczony instruktor w loop - ${teacherName}. Sprawdź profil, lekcje, które prowadzi, oraz opinie studentów. Rozpocznij naukę programowania pod okiem profesjonalisty!`;

  return createMetadata(
    `Instruktor ${teacherName} - sprawdź oferowane lekcje`,
    teacherDescription,
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
    `${paths.teacher}/${params.id}`,
    teacher?.avatarUrl ?? undefined,
  );
}
