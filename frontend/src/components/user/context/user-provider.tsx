"use client";

import { AxiosError } from "axios";
import { useMemo, useState, useEffect } from "react";

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

export function UserProvider({ children }: Props) {
  const [isRegistered, setIsRegistered] = useState<boolean>(false);
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [isUnverified, setIsUnverified] = useState<boolean>(false);
  const [isPasswordReset, setIsPasswordReset] = useState<boolean>(false);
  const [email, setEmail] = useState<string>("");
  const [userType, setUserType] = useState<string>(UserType.Student);

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
  } = useLogin();
  const {
    mutateAsync: loginGoogle,
    data: loginGoogleData,
    isSuccess: isSuccessLoginGoogle,
    isError: isErrorLoginGoogle,
    error: loginGoogleError,
    isLoading: isLoadingLoginGoogle,
  } = useLoginGoogle();
  const {
    mutateAsync: loginFacebook,
    data: loginFacebookData,
    isSuccess: isSuccessLoginFacebook,
    isError: isErrorLoginFacebook,
    error: loginFacebookError,
    isLoading: isLoadingLoginFacebook,
  } = useLoginFacebook();
  const {
    mutateAsync: loginGithub,
    data: loginGithubData,
    isSuccess: isSuccessLoginGithub,
    isError: isErrorLoginGithub,
    error: loginGithubError,
    isLoading: isLoadingLoginGithub,
  } = useLoginGithub();
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
      setIsUnverified(true);
      setIsRegistered(true);
      setEmail(registerData.email);
    }
  }, [isSuccessRegister, registerData?.email]);

  useEffect(() => {
    if (isSuccessUnregister) {
      setIsUnverified(true);
      setIsRegistered(false);
      setIsLoggedIn(false);
    }
  }, [isSuccessUnregister]);

  useEffect(() => {
    if (isSuccessVerify) {
      setIsRegistered(false);
      setIsUnverified(false);
    }
  }, [isSuccessVerify]);

  useEffect(() => {
    if (isSuccessLogin || isSuccessLoginGoogle || isSuccessLoginFacebook || isSuccessLoginGithub) {
      setIsLoggedIn(true);
      setUserType(
        (loginData?.user_type ||
          loginGoogleData?.user_type ||
          loginFacebookData?.user_type ||
          loginGithubData?.user_type) ??
          UserType.Student,
      );
    }
  }, [
    isSuccessLogin,
    isSuccessLoginGoogle,
    isSuccessLoginFacebook,
    isSuccessLoginGithub,
    loginData?.user_type,
    loginGoogleData?.user_type,
    loginFacebookData?.user_type,
    loginGithubData?.user_type,
  ]);

  useEffect(() => {
    if (isSuccessLogout) {
      setIsLoggedIn(false);
    }
  }, [isSuccessLogout]);

  useEffect(() => {
    if (isSuccessPasswordReset) {
      setIsPasswordReset(true);
    }
  }, [isSuccessPasswordReset]);

  useEffect(() => {
    if (isErrorLogin || isErrorLoginGoogle || isErrorLoginFacebook || isErrorLoginGithub) {
      if (loginError || loginGoogleError || loginFacebookError || loginGithubError) {
        if (
          ((loginError || loginGoogleError || loginFacebookError || loginGithubError) as AxiosError)
            .response?.status === 403
        ) {
          setEmail(((loginError as AxiosError).response?.data as ILoginReturn).email);
          setIsRegistered(true);
          setIsUnverified(true);
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
  ]);

  const memoizedValue = useMemo(
    () => ({
      isLoading,
      isRegistered,
      isLoggedIn,
      isUnverified,
      isPasswordReset,
      email,
      userType,
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
      isRegistered,
      isLoggedIn,
      isUnverified,
      isPasswordReset,
      email,
      userType,
      register,
      unregister,
      verify,
      login,
      loginGoogle,
      loginFacebook,
      loginGithub,
      logout,
      verifyCode,
      resetPassword,
    ],
  );

  return <UserContext.Provider value={memoizedValue}>{children}</UserContext.Provider>;
}
