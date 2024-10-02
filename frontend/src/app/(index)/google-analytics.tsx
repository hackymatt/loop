"use client";

import Script from "next/script";
import { useEffect } from "react";

import { usePathname, useSearchParams } from "src/routes/hooks";

import { useCookies } from "src/hooks/use-cookies";
import { useLocalStorage } from "src/hooks/use-local-storage";

import { pageView, updateConsent } from "src/utils/google-analytics";

import { ENV } from "src/config-global";

export default function GoogleAnalytics({ measurementId }: { measurementId: string }) {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const { defaultCookies } = useCookies();
  const { state } = useLocalStorage("cookies", { ...defaultCookies, consent: false });

  useEffect(() => {
    const url = `${pathname}${searchParams}`;

    pageView(measurementId, url);
  }, [measurementId, pathname, searchParams]);

  useEffect(() => {
    updateConsent({
      analytics_storage: state.analytics && ENV === "PROD" ? "granted" : "denied",
    });
  }, [state.analytics]);

  return (
    <>
      <Script
        strategy="afterInteractive"
        src={`https://www.googletagmanager.com/gtag/js?id=${measurementId}`}
      />
      <Script
        id="google-analytics"
        strategy="afterInteractive"
        dangerouslySetInnerHTML={{
          __html: `
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());

                gtag('consent', 'default', {
                    'analytics_storage': 'denied'
                });

                gtag('config', '${measurementId}', {
                    page_path: window.location.pathname,
                });
                `,
        }}
      />
    </>
  );
}
