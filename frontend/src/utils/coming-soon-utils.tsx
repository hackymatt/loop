"use client";

import { ReactNode } from "react";
import { differenceInSeconds } from "date-fns";

import { useLocalStorage } from "src/hooks/use-local-storage";

import Layout from "src/app/coming-soon/layout";

import ComingSoonView from "src/sections/status/view/coming-soon-view";

const START_DATE: Date = new Date("10/01/2024 00:00");

const useShowComingSoon = () => {
  const { state } = useLocalStorage("admin", { admin: false });
  const diff = differenceInSeconds(START_DATE, new Date());
  return diff > 0 && (process.env.NEXT_PUBLIC_ENV ?? "LOCAL") === "PROD" && !state.admin;
};

export function ComingSoonViewUtil({ defaultView }: { defaultView: ReactNode }) {
  const showComingSoon = useShowComingSoon();
  return showComingSoon ? <ComingSoonView startDate={START_DATE} /> : defaultView;
}

export function ComingSoonLayoutUtil({
  defaultLayout,
  children,
}: {
  defaultLayout: ReactNode;
  children: ReactNode;
}) {
  const showComingSoon = useShowComingSoon();
  return showComingSoon ? <Layout>{children}</Layout> : defaultLayout;
}
