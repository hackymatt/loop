import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { IGender, ITestimonialProps } from "src/types/testimonial";

import { Api } from "../service";

const endpoint = "/best-reviews" as const;

type IStudent = {
  first_name: string;
  gender: IGender | null;
  image: string | null;
};

type IReview = {
  id: string;
  student: IStudent;
  review: string;
};

export const bestReviewsQuery = () => {
  const url = endpoint;

  const queryFn = async () => {
    const { data } = await Api.get(url);
    const { results, records_count } = data;
    const modifiedResults = results.map(({ id, student, review }: IReview) => {
      const { first_name, gender, image } = student;
      return {
        id,
        name: first_name,
        gender,
        review,
        avatarUrl: image,
      };
    });
    return { results: modifiedResults, count: records_count };
  };

  return { url, queryFn, queryKey: compact([endpoint]) };
};

export const useBestReviews = () => {
  const { queryKey, queryFn } = bestReviewsQuery();
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as ITestimonialProps[], count: data?.count, ...rest };
};
