"use client";

import { differenceInMinutes } from "date-fns";

import { ENV } from "src/config-global";
import MainLayout from "src/layouts/main";
import CompactLayout from "src/layouts/compact";

// ----------------------------------------------------------------------

type Props = {
  children: React.ReactNode;
};

export default function Layout({ children }: Props) {
  const startDate = new Date("10/01/2024 00:00");
  const diff = differenceInMinutes(startDate, new Date());
  const showComingSoon = ENV === "PROD" && diff > 0;
  return showComingSoon ? (
    <CompactLayout>{children}</CompactLayout>
  ) : (
    <MainLayout disabledSpacing>{children}</MainLayout>
  );
}
