import { IGender } from "./testimonial";

export type IUserType = "Admin" | "Wykładowca" | "Student";

export type IUserDetailsProps = {
  firstName: string;
  lastName: string;
  emailAddress: string;
  phoneNumber: string;
  birthday: string;
  gender: IGender;
  streetAddress: string;
  zipCode: string;
  city: string;
  country: string;
  photo: string;
  userType?: IUserType;
  userTitle?: string;
};
