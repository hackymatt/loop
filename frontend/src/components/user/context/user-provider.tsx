"use client";

import { AxiosError } from "axios";
import { useMemo, useState, useEffect, useCallback } from "react";

import { useLocalStorage } from "src/hooks/use-local-storage";

import { useVerify } from "src/api/auth/verify";
import { useLogout } from "src/api/auth/logout";
import { useRegister } from "src/api/auth/register";
import { useUnregister } from "src/api/auth/unregister";
import { useVerifyCode } from "src/api/auth/resend-code";
import { useLoginGoogle } from "src/api/auth/login-google";
import { useLoginGithub } from "src/api/auth/login-github";
import { useLogin, ILoginReturn } from "src/api/auth/login";
import { useLoginFacebook } from "src/api/auth/login-facebook";
import { usePasswordReset } from "src/api/auth/password-reset";

import { UserType } from "src/types/user";

import { UserContext } from "./user-context";

// ----------------------------------------------------------------------

type Props = {
  children: React.ReactNode;
};

enum LoginType {
  EMAIL = "email",
  GOOGLE = "google",
  FACEBOOK = "facebook",
  GITHUB = "github",
}

type ILoginType = `${LoginType}`;

type User = {
  isRegistered: boolean;
  isLoggedIn: boolean;
  isUnverified: boolean;
  isPasswordReset: boolean;
  email: string;
  userType: UserType;
  loginType: ILoginType;
};

const defaultSettings = {
  isRegistered: false,
  isLoggedIn: false,
  isUnverified: false,
  isPasswordReset: false,
  email: "",
  userType: UserType.STUDENT,
  loginType: LoginType.EMAIL,
};

const STORAGE_KEY = "user";

export function UserProvider({ children }: Props) {
  const { state, update } = useLocalStorage(STORAGE_KEY, defaultSettings);

  const [user, setUser] = useState<User>(state);

  const updateUser = useCallback(
    (key: keyof User, value: any) => {
      setUser((prev: User) => ({ ...prev, [key]: value }));
      update(key, value);
    },
    [update],
  );

  const {
    mutateAsync: register,
    data: registerData,
    isSuccess: isSuccessRegister,
    isLoading: isLoadingRegister,
  } = useRegister();
  const {
    mutateAsync: unregister,
    isSuccess: isSuccessUnregister,
    isLoading: isLoadingUnregister,
  } = useUnregister();
  const {
    mutateAsync: verify,
    isSuccess: isSuccessVerify,
    isLoading: isLoadingVerify,
  } = useVerify();
  const { mutateAsync: verifyCode, isLoading: isLoadingVerifyCode } = useVerifyCode();
  const {
    mutateAsync: login,
    data: loginData,
    isSuccess: isSuccessLogin,
    isError: isErrorLogin,
    error: loginError,
    isLoading: isLoadingLogin,
  } = useLogin(() => updateUser("loginType", LoginType.EMAIL));
  const {
    mutateAsync: loginGoogle,
    data: loginGoogleData,
    isSuccess: isSuccessLoginGoogle,
    isError: isErrorLoginGoogle,
    error: loginGoogleError,
    isLoading: isLoadingLoginGoogle,
  } = useLoginGoogle(() => updateUser("loginType", LoginType.GOOGLE));
  const {
    mutateAsync: loginFacebook,
    data: loginFacebookData,
    isSuccess: isSuccessLoginFacebook,
    isError: isErrorLoginFacebook,
    error: loginFacebookError,
    isLoading: isLoadingLoginFacebook,
  } = useLoginFacebook(() => updateUser("loginType", LoginType.FACEBOOK));
  const {
    mutateAsync: loginGithub,
    data: loginGithubData,
    isSuccess: isSuccessLoginGithub,
    isError: isErrorLoginGithub,
    error: loginGithubError,
    isLoading: isLoadingLoginGithub,
  } = useLoginGithub(() => updateUser("loginType", LoginType.GITHUB));
  const {
    mutateAsync: logout,
    isSuccess: isSuccessLogout,
    isLoading: isLoadingLogout,
  } = useLogout();
  const {
    mutateAsync: resetPassword,
    isSuccess: isSuccessPasswordReset,
    isLoading: isLoadingPasswordReset,
  } = usePasswordReset();

  const isLoading =
    isLoadingRegister ||
    isLoadingUnregister ||
    isLoadingVerify ||
    isLoadingVerifyCode ||
    isLoadingLogin ||
    isLoadingLoginGoogle ||
    isLoadingLoginFacebook ||
    isLoadingLoginGithub ||
    isLoadingLogout ||
    isLoadingPasswordReset;

  useEffect(() => {
    if (isSuccessRegister) {
      updateUser("isUnverified", true);
      updateUser("isRegistered", true);
      updateUser("email", registerData.email);
    }
  }, [isSuccessRegister, registerData?.email, updateUser]);

  useEffect(() => {
    if (isSuccessUnregister) {
      updateUser("isUnverified", true);
      updateUser("isRegistered", false);
      updateUser("isLoggedIn", false);
    }
  }, [isSuccessUnregister, updateUser]);

  useEffect(() => {
    if (isSuccessVerify) {
      updateUser("isRegistered", false);
      updateUser("isUnverified", false);
    }
  }, [isSuccessVerify, updateUser]);

  useEffect(() => {
    switch (user.loginType) {
      case LoginType.GOOGLE:
        if (isSuccessLoginGoogle) {
          updateUser("isLoggedIn", true);
          updateUser("userType", loginGoogleData?.user_type ?? UserType.STUDENT);
        }
        break;
      case LoginType.FACEBOOK:
        if (isSuccessLoginFacebook) {
          updateUser("isLoggedIn", true);
          updateUser("userType", loginFacebookData?.user_type ?? UserType.STUDENT);
        }
        break;
      case LoginType.GITHUB:
        if (isSuccessLoginGithub) {
          updateUser("isLoggedIn", true);
          updateUser("userType", loginGithubData?.user_type ?? UserType.STUDENT);
        }
        break;
      default:
        if (isSuccessLogin) {
          updateUser("isLoggedIn", true);
          updateUser("userType", loginData?.user_type ?? UserType.STUDENT);
        }
        break;
    }
  }, [
    isSuccessLogin,
    isSuccessLoginFacebook,
    isSuccessLoginGithub,
    isSuccessLoginGoogle,
    loginData?.user_type,
    loginFacebookData?.user_type,
    loginGithubData?.user_type,
    loginGoogleData?.user_type,
    updateUser,
    user.loginType,
  ]);

  useEffect(() => {
    if (isSuccessLogout) {
      updateUser("isLoggedIn", false);
      updateUser("userType", UserType.STUDENT);
    }
  }, [isSuccessLogout, updateUser]);

  useEffect(() => {
    if (isSuccessPasswordReset) {
      updateUser("isPasswordReset", true);
    }
  }, [isSuccessPasswordReset, updateUser]);

  useEffect(() => {
    if (isErrorLogin || isErrorLoginGoogle || isErrorLoginFacebook || isErrorLoginGithub) {
      if (loginError || loginGoogleError || loginFacebookError || loginGithubError) {
        if (
          ((loginError || loginGoogleError || loginFacebookError || loginGithubError) as AxiosError)
            .response?.status === 403
        ) {
          updateUser("email", ((loginError as AxiosError).response?.data as ILoginReturn).email);
          updateUser("isRegistered", true);
          updateUser("isUnverified", true);
        }
      }
    }
  }, [
    isErrorLogin,
    isErrorLoginFacebook,
    isErrorLoginGithub,
    isErrorLoginGoogle,
    loginError,
    loginFacebookError,
    loginGithubError,
    loginGoogleError,
    updateUser,
  ]);

  const memoizedValue = useMemo(
    () => ({
      isLoading,
      isRegistered: state.isRegistered,
      isLoggedIn: state.isLoggedIn,
      isUnverified: state.isUnverified,
      isPasswordReset: state.isPasswordReset,
      email: state.email,
      userType: state.userType,
      registerUser: register,
      unregisterUser: unregister,
      verifyUser: verify,
      loginUser: login,
      loginGoogleUser: loginGoogle,
      loginFacebookUser: loginFacebook,
      loginGithubUser: loginGithub,
      logoutUser: logout,
      resendVerificationCode: verifyCode,
      resetUserPassword: resetPassword,
    }),
    [
      isLoading,
      login,
      loginFacebook,
      loginGithub,
      loginGoogle,
      logout,
      register,
      resetPassword,
      state.email,
      state.isLoggedIn,
      state.isPasswordReset,
      state.isRegistered,
      state.isUnverified,
      state.userType,
      unregister,
      verify,
      verifyCode,
    ],
  );

  return <UserContext.Provider value={memoizedValue}>{children}</UserContext.Provider>;
}
