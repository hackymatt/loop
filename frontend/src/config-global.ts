import { env } from "../next.config";

export const ENV = env.ENV ?? "LOCAL";

export const API_URL = env.API_URL ?? "";
export const BASE_URL = env.BASE_URL ?? "";

export const GOOGLE_CLIENT_ID = env.GOOGLE_CLIENT_ID ?? "";
export const FACEBOOK_CLIENT_ID = env.FACEBOOK_CLIENT_ID ?? "";
export const GITHUB_CLIENT_ID = env.GITHUB_CLIENT_ID ?? "";

export const GITHUB_REPO = env.GITHUB_REPO ?? "";

export const GOOGLE_ANALYTICS_ID = env.GOOGLE_ANALYTICS_ID ?? "";
export const FACEBOOK_PIXEL_ID = env.FACEBOOK_PIXEL_ID ?? "";

export const MIN_PASSWORD_LENGTH = Number(env.MIN_PASSWORD_LENGTH) ?? 8;
export const LESSON_DURATION_MULTIPLIER = Number(env.LESSON_DURATION_MULTIPLIER) ?? 30;
export const CANCELLATION_TIME = Number(env.CANCELLATION_TIME) ?? 24;

export const PAYMENT_SERVER = env.PAYMENT_SERVER ?? "https://sandbox.przelewy24.pl";
