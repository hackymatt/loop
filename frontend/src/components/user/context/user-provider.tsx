"use client";

import { AxiosError } from "axios";
import { useMemo, useState, useEffect } from "react";

import { useVerify } from "src/api/auth/verify";
import { useLogout } from "src/api/auth/logout";
import { useRegister } from "src/api/auth/register";
import { useUnregister } from "src/api/auth/unregister";
import { useVerifyCode } from "src/api/auth/resend-code";
import { useLoginGoogle } from "src/api/auth/login-google";
import { useLogin, ILoginReturn } from "src/api/auth/login";
import { useLoginFacebook } from "src/api/auth/login-facebook";
import { usePasswordReset } from "src/api/auth/password-reset";

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
    isSuccess: isSuccessLogin,
    isError: isErrorLogin,
    error: loginError,
    isLoading: isLoadingLogin,
  } = useLogin();
  const {
    mutateAsync: loginGoogle,
    isSuccess: isSuccessLoginGoogle,
    isError: isErrorLoginGoogle,
    error: loginGoogleError,
    isLoading: isLoadingLoginGoogle,
  } = useLoginGoogle();
  const {
    mutateAsync: loginFacebook,
    isSuccess: isSuccessLoginFacebook,
    isError: isErrorLoginFacebook,
    error: loginFacebookError,
    isLoading: isLoadingLoginFacebook,
  } = useLoginFacebook();
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
    if (isSuccessLogin || isSuccessLoginGoogle || isSuccessLoginFacebook) {
      setIsLoggedIn(true);
    }
  }, [isSuccessLogin, isSuccessLoginGoogle, isSuccessLoginFacebook]);

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
    if (isErrorLogin || isErrorLoginGoogle || isErrorLoginFacebook) {
      if (loginError || loginGoogleError || loginFacebookError) {
        if (((loginError || loginGoogleError) as AxiosError).response?.status === 403) {
          setEmail(((loginError as AxiosError).response?.data as ILoginReturn).email);
          setIsRegistered(true);
          setIsUnverified(true);
        }
      }
    }
  }, [
    isErrorLogin,
    isErrorLoginFacebook,
    isErrorLoginGoogle,
    loginError,
    loginFacebookError,
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
      registerUser: register,
      unregisterUser: unregister,
      verifyUser: verify,
      loginUser: login,
      loginGoogleUser: loginGoogle,
      loginFacebookUser: loginFacebook,
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
      register,
      unregister,
      verify,
      login,
      loginGoogle,
      loginFacebook,
      logout,
      verifyCode,
      resetPassword,
    ],
  );

  return <UserContext.Provider value={memoizedValue}>{children}</UserContext.Provider>;
}
