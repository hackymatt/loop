"use client";

import Script from "next/script";
import { useEffect } from "react";

import { usePathname, useSearchParams } from "src/routes/hooks";

import { pageView } from "src/utils/google-analytics";

export default function GoogleAnalytics({ measurementId }: { measurementId: string }) {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  useEffect(() => {
    const url = `${pathname}${searchParams}`;

    pageView(measurementId, url);
  }, [measurementId, pathname, searchParams]);

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
