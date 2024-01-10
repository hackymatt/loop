import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { IGender, ITestimonialProps } from "src/types/testimonial";

import { Api } from "../service";

const statsEndpoint = "/best-reviews" as const;

type IStudent = {
  full_name: string;
  email: string;
  gender: IGender | null;
  image: string | null;
};

type IReview = {
  id: number;
  student: IStudent;
  modified_at: string;
  created_at: string;
  review: string;
  rating: string;
};

export const bestReviewsQuery = () => {
  const url = statsEndpoint;

  const queryFn = async () => {
    const { data } = await Api.get(url);
    const { results, records_count } = data;
    const modifiedResults = results.map((review: IReview) => ({
      id: review.id,
      name: review.student.full_name,
      review: review.review,
      avatarUrl: review.student.image,
    }));
    return { results: modifiedResults, count: records_count };
  };

  return { url, queryFn, queryKey: compact([url]) };
};

export const useBestReviews = () => {
  const { queryKey, queryFn } = bestReviewsQuery();
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as ITestimonialProps[], ...rest };
};
