import { useState } from "react";

export function useUser() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return {
    isLoggedIn,
    setIsLoggedIn,
  };
}
