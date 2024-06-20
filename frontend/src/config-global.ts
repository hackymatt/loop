import { env } from "../next.config";

export const ENV = env.ENV ?? "LOCAL";

export const API_URL = env.API_URL ?? "";
export const BASE_URL = env.BASE_URL ?? "";

export const GOOGLE_CLIENT_ID = env.GOOGLE_CLIENT_ID ?? "";
export const FACEBOOK_CLIENT_ID = env.FACEBOOK_CLIENT_ID ?? "";
export const GITHUB_CLIENT_ID = env.GITHUB_CLIENT_ID ?? "";

export const GITHUB_REPO = env.GITHUB_REPO ?? "";
