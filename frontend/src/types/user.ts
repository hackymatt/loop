import { Gender } from "src/consts/gender";
import { UserType } from "src/consts/user-type";

export type IUserType = (typeof UserType)[keyof typeof UserType];

export type IGender = (typeof Gender)[keyof typeof Gender];

export type IUserProps = {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  phoneNumber: string | null;
  dob: string | null;
  gender: IGender;
  streetAddress: string | null;
  zipCode: string | null;
  city: string | null;
  country: string | null;
  image: string | null;
};

export type IUserDetailsProps = IUserProps & {
  active: boolean;
  userType: IUserType;
  createdAt: string;
};

export type IUserFinanceProps = {
  account: string | null;
  commission: number | null;
  rate: number | null;
};
