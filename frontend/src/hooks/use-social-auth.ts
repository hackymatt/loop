import { paths } from "src/routes/paths";

import { generateCode } from "src/utils/generateCode";

import {
  BASE_URL,
  GOOGLE_CLIENT_ID,
  GITHUB_CLIENT_ID,
  FACEBOOK_CLIENT_ID,
} from "src/config-global";

export const useGoogleAuth = () => {
  const googleUrl = "https://accounts.google.com/o/oauth2/v2/auth";

  const scope = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
  ].join(" ");

  const state = generateCode(18);

  const params = new URLSearchParams({
    client_id: GOOGLE_CLIENT_ID,
    redirect_uri: `${BASE_URL}${paths.login}/?type=google`,
    response_type: "code",
    scope,
    access_type: "offline",
    state,
    prompt: "select_account",
  });

  return { authUrl: `${googleUrl}?${params}`, state };
};

export const useFacebookAuth = () => {
  const facebookUrl = "https://www.facebook.com/v19.0/dialog/oauth";

  const scope = ["email", "user_gender", "public_profile"].join(",");

  const state = generateCode(18);

  const params = new URLSearchParams({
    client_id: FACEBOOK_CLIENT_ID,
    redirect_uri: `${BASE_URL}${paths.login}/?type=facebook`,
    state,
    response_type: "code",
    scope,
  });

  return { authUrl: `${facebookUrl}?${params}`, state };
};

export const useGithubAuth = () => {
  const githubUrl = "https://github.com/login/oauth/authorize";

  const scope = ["user:email", "read:user"].join(" ");

  const state = generateCode(18);

  const params = new URLSearchParams({
    client_id: GITHUB_CLIENT_ID,
    redirect_uri: `${BASE_URL}${paths.login}/?type=github`,
    scope,
    state,
  });

  return { authUrl: `${githubUrl}?${params}`, state };
};
