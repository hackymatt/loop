// ----------------------------------------------------------------------

import { ILogin, ILoginReturn } from "src/api/auth/login";
import { IUnregisterReturn } from "src/api/auth/unregister";
import { ILogout, ILogoutReturn } from "src/api/auth/logout";
import { IVerify, IVerifyReturn } from "src/api/auth/verify";
import { IRegister, IRegisterReturn } from "src/api/auth/register";
import { IVerifyCode, IVerifyCodeReturn } from "src/api/auth/resend-code";
import { ILoginGoogle, ILoginGoogleReturn } from "src/api/auth/login-google";
import { ILoginGithub, ILoginGithubReturn } from "src/api/auth/login-github";
import { IPasswordReset, IPasswordResetReturn } from "src/api/auth/password-reset";
import { ILoginFacebook, ILoginFacebookReturn } from "src/api/auth/login-facebook";

export type UserContextProps = {
  isLoading: boolean;
  isRegistered: boolean;
  isLoggedIn: boolean;
  isUnverified: boolean;
  isPasswordReset: boolean;
  email: string;
  userType: string;
  registerUser: (variables: IRegister) => Promise<IRegisterReturn>;
  unregisterUser: () => Promise<IUnregisterReturn>;
  verifyUser: (variables: IVerify) => Promise<IVerifyReturn>;
  loginUser: (variables: ILogin) => Promise<ILoginReturn>;
  loginGoogleUser: (variables: ILoginGoogle) => Promise<ILoginGoogleReturn>;
  loginFacebookUser: (variables: ILoginFacebook) => Promise<ILoginFacebookReturn>;
  loginGithubUser: (variables: ILoginGithub) => Promise<ILoginGithubReturn>;
  logoutUser: (variables: ILogout) => Promise<ILogoutReturn>;
  resendVerificationCode: (variables: IVerifyCode) => Promise<IVerifyCodeReturn>;
  resetUserPassword: (variables: IPasswordReset) => Promise<IPasswordResetReturn>;
};
