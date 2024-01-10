// ----------------------------------------------------------------------

export type ITestimonialProps = {
  id: string;
  name: string;
  gender?: IGender | null;
  review?: string;
  avatarUrl?: string;
  createdAt?: Date;
  ratingNumber?: number;
};

export type IGender = "Mężczyzna" | "Kobieta" | "Inne";
