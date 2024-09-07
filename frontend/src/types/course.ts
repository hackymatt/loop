import { IGender } from "./testimonial";
import { ISocialLinks } from "./socials";

// ----------------------------------------------------------------------

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

export type ITeachingProp = {
  id: string;
  title: string;
  duration: number;
  price: number;
  githubUrl: string;
  active: boolean;
  teaching: boolean;
  teachingId?: string;
};

export type ICourseLessonProp = {
  id: string;
  title: string;
  duration: number;
  category: string[];
  videoPath?: string;
  unLocked?: boolean;
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
  progress?: number | null;
};

export type ICourseModuleProp = {
  id: string;
  title: string;
  price?: number;
  priceSale?: number;
  lowest30DaysPrice?: number;
  lessons?: ICourseLessonProp[];
  lessonsCount?: number;
  progress?: number | null;
};

export type IScheduleProp = {
  id: string;
  startTime: string;
  endTime: string;
  lesson: Pick<ICourseLessonProp, "id" | "title">;
  studentsRequired: number;
};

export type ICourseLessonPriceHistoryProp = {
  id: string;
  lesson: ICourseLessonProp;
  price: number;
  createdAt: Date;
};

export type ICourseByCategoryProps = {
  id: string;
  name: string;
  totalStudents?: number;
  createdAt: Date;
};

export type ICourseByTopicProps = {
  id: string;
  name: string;
  createdAt: Date;
};

export type ICourseBySkillProps = {
  id: string;
  name: string;
  createdAt: Date;
};

export type ILevel = "P" | "Ś" | "Z" | "E";

export type ICourseProps = {
  id: string;
  slug: string;
  price: number;
  level: ILevel;
  createdAt?: Date;
  coverUrl: string;
  video?: string;
  category: string[];
  skills: string[];
  priceSale: number;
  lowest30DaysPrice?: number;
  resources?: number;
  totalHours: number;
  description?: string;
  languages?: string[];
  learnList: string[];
  ratingNumber: number;
  totalQuizzes?: number;
  totalReviews: number;
  totalStudents: number;
  shareLinks?: ISocialLinks;
  modules: ICourseModuleProp[];
  teachers: ICourseTeacherProp[];
  active: boolean;
  progress?: number | null;
};
