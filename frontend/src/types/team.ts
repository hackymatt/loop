import { IGender } from "./testimonial";
import { ISocialLinks } from "./socials";
import { ICourseLessonProp } from "./course";

// ----------------------------------------------------------------------

export type ITeamMemberProps = {
  id: string;
  name: string;
  description?: string;
  linkedinUrl?: string;
  email?: string;
  role?: string;
  linkedin_url?: string;
  avatarUrl: string;
  socialLinks?: ISocialLinks;
  gender?: IGender;
  ratingNumber?: number;
  totalReviews?: number;
  totalHours?: number;
  totalLessons?: number;
  lessons?: ICourseLessonProp[];
  lessonsPrice?: number;
  lessonsPreviousPrice?: number;
  lessonsLowest30DaysPrice?: number;
  totalStudents?: number;
};
