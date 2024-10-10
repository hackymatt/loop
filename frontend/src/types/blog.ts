import type { IAuthorProps } from "./author";

// ----------------------------------------------------------------------

export type IPostCategoryProps = {
  id: string;
  name: string;
  createdAt: string;
};

export type IPostNavigationProps = {
  id: string;
  title: string;
  coverUrl: string;
};

export type IPostProps = {
  id: string;
  title: string;
  description: string;
  content?: string;
  category: string;
  duration: string;
  coverUrl: string;
  authors: IAuthorProps[];
  createdAt: string;
  previousPost?: IPostNavigationProps;
  nextPost?: IPostNavigationProps;
  active: boolean;
};
