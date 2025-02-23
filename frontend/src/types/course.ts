import { Level } from "src/consts/level";

import { IUserProps } from "./user";
import { IGender } from "./testimonial";
import { ITechnologyProps } from "./technology";

// ----------------------------------------------------------------------

export type ILevel = (typeof Level)[keyof typeof Level];

export type ICourseTeacherProp = {
  id: string;
  name: string;
  role?: string;
  avatarUrl?: string;
  ratingNumber?: number;
  totalLessons?: number;
  totalReviews?: number;
  totalStudents?: number;
  gender?: IGender;
};

export type ICourseLessonProp = {
  id: string;
  title: string;
  duration: number;
  technologies: ICourseByTechnologyProps[];
  videoPath?: string;
  description: string;
  price: number;
  priceSale?: number;
  lowest30DaysPrice?: number;
  ratingNumber?: number;
  totalReviews?: number;
  totalStudents?: number;
  teachers?: ICourseTeacherProp[];
  githubUrl: string;
  active?: boolean;
  progress?: number;
};

export type ICourseModuleProp = {
  id: string;
  title: string;
  price?: number;
  totalHours?: number;
  priceSale?: number;
  lowest30DaysPrice?: number;
  lessons?: ICourseLessonProp[];
  lessonsCount?: number;
  progress?: number;
};

export type IScheduleStudentProp = { id: string; name: string; gender: IGender; image: string };

export type IScheduleProp = {
  id: string;
  startTime: string;
  endTime: string;
  lesson: Pick<ICourseLessonProp, "id" | "title">;
  meetingUrl?: string;
  students: IScheduleStudentProp[];
  studentsRequired: number;
};

export type ICourseByTechnologyProps = {
  id: string;
  name: string;
  description?: string;
  totalStudents?: number;
  createdAt?: Date;
};

// export type ICourseProps = {
//   createdAt?: Date;
//   video?: string;
//   tags: string[];
//   overview?: string;
//   learnList: string[];
//   candidateList: string[];
//   modules: ICourseModuleProp[];
// };

export type ICourseTechnologyProps = Pick<ITechnologyProps, "id" | "name">;

export type ICourseTeacherProps = Pick<IUserProps, "id" | "gender" | "image"> & { name: string };

export type ICourseProps = {
  id: string;
  price: number;
  priceSale: number | null;
  lowest30DaysPrice: number | null;
  totalHours: number;
  technologies: ICourseTechnologyProps[];
  teachers: ICourseTeacherProps[];
  totalStudents: number;
  ratingNumber: number;
  totalReviews: number;
  image: string;
  level: ILevel;
  title: string;
  description: string;
  active: boolean;
  progress: number | null;
};
