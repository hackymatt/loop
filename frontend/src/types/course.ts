import { IGender } from "./testimonial";
import { ISocialLinks } from "./socials";

// ----------------------------------------------------------------------

export type ICourseTeacherProp = {
  id: string;
  name: string;
  role?: string;
  avatarUrl?: string;
  ratingNumber?: number;
  totalCourses?: number;
  totalReviews?: number;
  totalStudents?: number;
  gender?: IGender;
};

export type ICourseLessonProp = {
  id: string;
  title: string;
  duration: number;
  category: string[];
  videoPath?: string;
  unLocked?: boolean;
  description: string;
  price?: number;
  priceSale?: number;
  lowest30DaysPrice?: number;
  ratingNumber?: number;
  totalReviews?: number;
  totalStudents?: number;
  teachers?: ICourseTeacherProp[];
  githubUrl?: string;
  active?: boolean;
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

export type ICourseProps = {
  id: string;
  slug: string;
  price: number;
  level: string;
  createdAt?: Date;
  coverUrl: string;
  bestSeller: boolean;
  video?: string;
  category: string[];
  skills?: string[];
  priceSale: number;
  lowest30DaysPrice?: number;
  resources?: number;
  totalHours: number;
  description?: string;
  languages?: string[];
  learnList?: string[];
  ratingNumber: number;
  totalQuizzes?: number;
  totalReviews: number;
  totalStudents: number;
  shareLinks?: ISocialLinks;
  lessons?: ICourseLessonProp[];
  teachers: ICourseTeacherProp[];
};
