import { Gender } from "src/consts/gender";

export enum UserType {
  ADMIN = "Admin",
  TEACHER = "Wykładowca",
  STUDENT = "Student",
  OTHER = "Inny",
}

export type IUserType = `${UserType}`;

export type IUserDetailsProps = {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  active: boolean;
  phone_number: string;
  dob: string | null;
  gender: IGender;
  street_address: string;
  zip_code: string;
  city: string;
  country: string;
  image: string;
  user_type?: IUserType;
  rate?: number;
  commission?: number;
  created_at?: string;
};

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
