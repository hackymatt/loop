import { IGender } from "./testimonial";

export type IUserType = "Admin" | "Wykładowca" | "Student";

export type IUserDetailsProps = {
  first_name: string;
  last_name: string;
  email: string;
  phone_number: string;
  dob: string;
  gender: IGender;
  street_address: string;
  zip_code: string;
  city: string;
  country: string;
  image: string;
  user_type?: IUserType;
  user_title?: string;
};
