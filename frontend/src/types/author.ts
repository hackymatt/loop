import { IGender } from "./testimonial";

export type IAuthorProps = {
  id: string;
  name: string;
  role?: string;
  description?: string;
  dateJoined?: string;
  gender: IGender;
  avatarUrl: string;
};
