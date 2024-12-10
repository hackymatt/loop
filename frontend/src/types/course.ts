import { IGender } from "./testimonial";

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
  technologies: ICourseByTechnologyProps[];
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

export type ICourseLessonPriceHistoryProp = {
  id: string;
  lesson: ICourseLessonProp;
  price: number;
  createdAt: Date;
};

export type ICourseByTechnologyProps = {
  id: string;
  name: string;
  description?: string;
  totalStudents?: number;
  createdAt: Date;
};

export type ICourseByTopicProps = {
  id: string;
  name: string;
  createdAt: Date;
};

export type ICourseByCandidateProps = {
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
  technologies: ICourseByTechnologyProps[];
  tags: string[];
  priceSale: number;
  lowest30DaysPrice?: number;
  totalHours: number;
  description?: string;
  overview?: string;
  learnList: string[];
  candidateList: string[];
  ratingNumber: number;
  totalReviews: number;
  totalStudents: number;
  modules: ICourseModuleProp[];
  teachers: ICourseTeacherProp[];
  active: boolean;
  progress?: number;
};
