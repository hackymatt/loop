import { AxiosError } from "axios";
import { useState, useEffect } from "react";

import { useLogin } from "src/api/auth/login";
import { useVerify } from "src/api/auth/verify";
import { useRegister } from "src/api/auth/register";

export function useUser() {
  const [isRegistered, setIsRegistered] = useState<boolean>(false);
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [isUnverified, setIsUnverified] = useState<boolean>(false);
  const [email, setEmail] = useState<string>("");

  const { mutateAsync: register, data: registerData, isSuccess: isSuccessRegister } = useRegister();
  const { mutateAsync: verify } = useVerify();
  const {
    mutateAsync: login,
    isSuccess: isSuccessLogin,
    isError: isErrorLogin,
    error: loginError,
  } = useLogin();

  useEffect(() => {
    if (isSuccessRegister) {
      setIsRegistered(true);
      setEmail(registerData.email);
    }
  }, [isSuccessRegister, registerData?.email]);

  useEffect(() => {
    if (isSuccessLogin) {
      setIsLoggedIn(true);
    }
  }, [isSuccessLogin]);

  useEffect(() => {
    if (isErrorLogin) {
      if (loginError) {
        if ((loginError as AxiosError).response?.status === 403) {
          setIsUnverified(true);
        }
      }
    }
  }, [isErrorLogin, loginError]);

  const loginUser = async (data: { email: string; password: string }) => {
    setEmail(data.email);
    await login(data);
  };

  return {
    isRegistered,
    isLoggedIn,
    isUnverified,
    email,
    registerUser: register,
    verifyUser: verify,
    loginUser,
  };
}
