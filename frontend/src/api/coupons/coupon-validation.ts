import { ICouponProps } from "src/types/coupon";

import { Api } from "../service";

const endpoint = "/coupon-validate" as const;

export const validateCoupon = async (code: string, total: number) => {
  const url = endpoint;
  const queryUrl = `${url}/${code}/${total}`;

  let response;
  try {
    response = await Api.get<ICouponProps>(queryUrl);
  } catch (error) {
    if (error.response && (error.response.status === 400 || error.response.status === 404)) {
      response = { status: error.response.status, data: error.response.data };
    }
  }

  return response as { status: number; data: ICouponProps };
};
