"use client";

import { AxiosError } from "axios";
import { useMemo, useState, useEffect } from "react";

import { useVerify } from "src/api/auth/verify";
import { useLogout } from "src/api/auth/logout";
import { useRegister } from "src/api/auth/register";
import { useVerifyCode } from "src/api/auth/resend-code";
import { useLogin, ILoginReturn } from "src/api/auth/login";
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
    isLoadingVerify ||
    isLoadingVerifyCode ||
    isLoadingLogin ||
    isLoadingLogout ||
    isLoadingPasswordReset;

  useEffect(() => {
    if (isSuccessRegister) {
      setIsRegistered(true);
      setEmail(registerData.email);
    }
  }, [isSuccessRegister, registerData?.email]);

  useEffect(() => {
    if (isSuccessVerify) {
      setIsUnverified(false);
    }
  }, [isSuccessVerify]);

  useEffect(() => {
    if (isSuccessLogin) {
      setIsLoggedIn(true);
    }
  }, [isSuccessLogin]);

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
    if (isErrorLogin) {
      if (loginError) {
        if ((loginError as AxiosError).response?.status === 403) {
          console.log((loginError as AxiosError).response?.data as ILoginReturn);
          setEmail(((loginError as AxiosError).response?.data as ILoginReturn).email);
          setIsUnverified(true);
        }
      }
    }
  }, [isErrorLogin, loginError]);

  const memoizedValue = useMemo(
    () => ({
      isLoading,
      isRegistered,
      isLoggedIn,
      isUnverified,
      isPasswordReset,
      email,
      registerUser: register,
      verifyUser: verify,
      loginUser: login,
      logoutUser: logout,
      resendVerificationCode: verifyCode,
      resetUserPassword: resetPassword,
    }),
    [
      email,
      isLoading,
      isLoggedIn,
      isPasswordReset,
      isRegistered,
      isUnverified,
      login,
      logout,
      register,
      resetPassword,
      verify,
      verifyCode,
    ],
  );

  return <UserContext.Provider value={memoizedValue}>{children}</UserContext.Provider>;
}
