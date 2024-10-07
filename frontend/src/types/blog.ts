import type { IAuthorProps } from "./author";

// ----------------------------------------------------------------------

export type IPostCategoryProps = {
  label: string;
  path: string;
};

export type IPostProps = {
  id: string;
  title: string;
  description: string;
  content: string;
  category: string;
  duration: string;
  heroUrl: string;
  coverUrl: string;
  author: IAuthorProps;
  createdAt: string;
};
