import { Level } from "src/consts/level";

import { ITagProps } from "./tags";
import { ITopicProps } from "./topic";
import { IGender } from "./testimonial";
import { IModuleProps } from "./module";
import { ILessonProps } from "./lesson";
import { ITeacherProps } from "./teacher";
import { ICandidateProps } from "./candidate";
import { ITechnologyProps } from "./technology";

// ----------------------------------------------------------------------

export type ILevel = (typeof Level)[keyof typeof Level];

export type IScheduleStudentProp = { id: string; name: string; gender: IGender; image: string };

export type IScheduleProp = {
  id: string;
  startTime: string;
  endTime: string;
  lesson: Pick<ILessonProps, "id" | "title">;
  meetingUrl?: string;
  students: IScheduleStudentProp[];
  studentsRequired: number;
};

export type ICourseTechnologyProps = Pick<ITechnologyProps, "id" | "name">;

export type ICourseTechnologyDetailsProps = Pick<ITechnologyProps, "id" | "name" | "description">;

export type ICourseTeacherProps = Pick<ITeacherProps, "id" | "name" | "gender" | "image">;

export type ICourseTeacherDetailsProps = ITeacherProps;

export type ICourseModuleLessonProps = Pick<ILessonProps, "id" | "title" | "price"> & {
  progress: number | null;
};

export type ICourseModuleProps = Omit<IModuleProps, "totalHours" | "lessons"> & {
  lessons: ICourseModuleLessonProps[];
  priceSale: number | null;
  lowest30DaysPrice: number | null;
  progress: number | null;
};

export type ICourseTagProps = Omit<ITagProps, "createdAt">;
export type ICourseTopicProps = Omit<ITopicProps, "createdAt">;
export type ICourseCandidateProps = Omit<ICandidateProps, "createdAt">;

export type ICourseProps = {
  id: string;
  price: number;
  priceSale: number | null;
  lowest30DaysPrice: number | null;
  totalHours: number;
  technologies: ICourseTechnologyProps[];
  teachers: ICourseTeacherProps[];
  totalStudents: number;
  ratingNumber: number | null;
  totalReviews: number;
  image: string;
  level: ILevel;
  title: string;
  description: string;
  active: boolean;
  progress: number | null;
};

export type ICourseDetailsProps = Omit<ICourseProps, "technologies" | "teachers"> & {
  modules: ICourseModuleProps[];
  tags: ICourseTagProps[];
  topics: ICourseTopicProps[];
  candidates: ICourseCandidateProps[];
  teachers: ICourseTeacherDetailsProps[];
  technologies: ICourseTechnologyDetailsProps[];
  video: string | null;
  overview: string;
};
