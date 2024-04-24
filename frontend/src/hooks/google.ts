import { paths } from "src/routes/paths";

export const useGoogleAuth = () => {
  const googleUrl = "https://accounts.google.com/o/oauth2/v2/auth";

  const scope = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
  ].join(" ");

  const params = new URLSearchParams({
    response_type: "code",
    client_id: process.env.GOOGLE_CLIENT_ID ?? "",
    redirect_uri: `${process.env.BASE_URL ?? ""}${paths.login}/?type=google`,
    prompt: "select_account",
    access_type: "offline",
    scope,
  });

  return { authUrl: `${googleUrl}?${params}` };
};
