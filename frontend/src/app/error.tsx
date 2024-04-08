"use client";

import Error500View from "src/sections/error/500-view";
// ----------------------------------------------------------------------

export const metadata = {
  title: "500 Błąd serwera",
};

export default function Page500() {
  return <Error500View />;
}
