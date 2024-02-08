import { IGender } from "./testimonial";
import { ISocialLinks } from "./socials";

// ----------------------------------------------------------------------

export type ITeamMemberProps = {
  id: string;
  name: string;
  role?: string;
  email?: string;
  avatarUrl: string;
  socialLinks?: ISocialLinks;
  gender?: IGender;
  ratingNumber?: number;
  totalReviews?: number;
  totalLessons?: number;
};
