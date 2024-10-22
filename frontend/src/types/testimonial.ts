// ----------------------------------------------------------------------

export type ITestimonialProps = {
  id: string;
  name: string;
  gender?: IGender;
  review?: string;
  avatarUrl?: string;
  createdAt?: Date;
  ratingNumber?: number;
};

export enum Gender {
  MALE = "Mężczyzna",
  FEMALE = "Kobieta",
  OTHER = "Inne",
}

export type IGender = `${Gender}`;
