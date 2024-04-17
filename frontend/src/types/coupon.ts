import { IUserDetailsProps } from "./user";

export type ICouponProps = {
  id: string;
  code: string;
  discount: number;
  is_percentage: boolean;
  users: IUserDetailsProps[];
  all_users: boolean;
  max_uses: number;
  is_infinite: boolean;
  uses_per_user: number;
  expiration_date: Date;
  active: boolean;
  min_total: number;
};
