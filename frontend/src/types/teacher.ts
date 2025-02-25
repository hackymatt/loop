import { IUserProps } from "./user";

export type ITeacherProps = Pick<IUserProps, "id" | "gender" | "image"> & {
  name: string;
  role: string;
  totalLessons: number;
  ratingNumber: number | null;
  totalReviews: number;
};
