import { IGender } from "./testimonial";

export type IAuthorProps = {
  id: string;
  name: string;
  role: string;
  gender: IGender;
  avatarUrl: string;
  linkedinUrl: string;
};
