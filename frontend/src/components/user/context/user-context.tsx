"use client";

import { useContext, createContext } from "react";

import { UserContextProps } from "../types";

// ----------------------------------------------------------------------

export const UserContext = createContext({} as UserContextProps);

export const useUserContext = () => {
  const context = useContext(UserContext);

  if (!context) throw new Error("useUserContext must be use inside UserProvider");

  return context;
};
