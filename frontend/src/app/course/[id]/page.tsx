import { Metadata } from "next";

import { paths } from "src/routes/paths";

import { decodeUrl } from "src/utils/url-utils";
import { createMetadata } from "src/utils/create-metadata";

import { courseQuery } from "src/api/courses/course";

import CourseView from "src/sections/view/course-view";

import { ICourseByTechnologyProps } from "src/types/course";

// ----------------------------------------------------------------------

export default function CoursePage({ params }: { params: { id: string } }) {
  return <CourseView id={params.id} />;
}

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const decodedId = decodeUrl(params.id);
  const recordId = decodedId.slice(decodedId.lastIndexOf("-") + 1);

  const { queryFn } = courseQuery(recordId);

  const { results: course } = await queryFn();

  const courseTitle =
    course?.slug ?? decodedId.slice(0, decodedId.lastIndexOf("-")).replace(/-/g, " ");
  const courseDescription = course?.description ? `${course.description} ` : "";

  const technologyKeywords = (course?.technologies ?? [])
    .map((technology: ICourseByTechnologyProps) => [
      `${technology.name} online`,
      `nauka ${technology.name}`,
      `programowanie ${technology.name}`,
      `${technology.name} od podstaw`,
      `certyfikat ${technology.name}`,
      `zajęcia z ${technology.name}`,
    ])
    .flat();

  return createMetadata(
    `Kurs ${courseTitle} - sprawdź program nauczania`,
    `Zapisz się na kurs ${courseTitle} w loop i naucz się programować. ${courseDescription}Oferujemy praktyczne lekcje online z certyfikatem ukończenia oraz wsparcie doświadczonych instruktorów.`,
    [
      `kurs ${courseTitle}`,
      "kursy programowania",
      "szkoła programowania loop",
      "kurs programowania",
      ...(technologyKeywords ?? []),
    ],
    `${paths.course}/${params.id}`,
    course?.coverUrl,
  );
}
