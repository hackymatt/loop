import { IGender } from "./testimonial";

export enum UserType {
  ADMIN = "Admin",
  TEACHER = "Wykładowca",
  STUDENT = "Student",
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
