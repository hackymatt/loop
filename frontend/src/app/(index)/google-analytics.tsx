"use client";

import Script from "next/script";
import { useEffect } from "react";

import { usePathname, useSearchParams } from "src/routes/hooks";

import { useCookies } from "src/hooks/use-cookies";
import { useLocalStorage } from "src/hooks/use-local-storage";

import { pageView, updateConsent } from "src/utils/google-analytics";

import { ENV, GOOGLE_ANALYTICS_ID } from "src/config-global";

const ClientGoogleAnalytics = () => {
  const measurementId = GOOGLE_ANALYTICS_ID;
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const { defaultCookies } = useCookies();
  const { state } = useLocalStorage("cookies", { ...defaultCookies, consent: false });

  useEffect(() => {
    const url = `${pathname}${searchParams.toString()}`;

    if (measurementId) {
      pageView(measurementId, url);
    }

    updateConsent({
      analytics_storage: state.analytics && ENV === "PROD" ? "granted" : "denied",
    });
  }, [measurementId, pathname, searchParams, state.analytics]);

  if (typeof window === "undefined") {
    return null;
  }

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
};

export default function GoogleAnalytics() {
  if (typeof window === "undefined") {
    return null;
  }

  return <ClientGoogleAnalytics />;
}
