"use client";

import Script from "next/script";
import { useState, useEffect } from "react";

import { usePathname, useSearchParams } from "src/routes/hooks";

import { useCookies } from "src/hooks/use-cookies";
import { useLocalStorage } from "src/hooks/use-local-storage";

import { pageView, updateConsent } from "src/utils/facebook-pixel";

import { ENV, FACEBOOK_PIXEL_ID } from "src/config-global";

export default function FacebookPixel() {
  const measurementId = FACEBOOK_PIXEL_ID;
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const { defaultCookies } = useCookies();
  const { state } = useLocalStorage("cookies", { ...defaultCookies, consent: false });
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  useEffect(() => {
    if (isMounted && measurementId) {
      pageView();
      updateConsent(state.marketing && ENV === "PROD" ? "grant" : "revoke");
    }
  }, [isMounted, measurementId, pathname, searchParams, state.marketing]);

  if (!isMounted) {
    return null;
  }

  return (
    <>
      <Script id="facebook-pixel" strategy="afterInteractive">
        {`
          !function(f,b,e,v,n,t,s)
          {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
          n.callMethod.apply(n,arguments):n.queue.push(arguments)};
          if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
          n.queue=[];t=b.createElement(e);t.async=!0;
          t.src=v;s=b.getElementsByTagName(e)[0];
          s.parentNode.insertBefore(t,s)}(window, document,'script',
          'https://connect.facebook.net/en_US/fbevents.js');
          fbq('init', '${measurementId}');
          fbq('track', 'PageView');
          fbq('consent', 'revoke');
        `}
      </Script>

      <noscript>
        <img
          height="1"
          width="1"
          style={{ display: "none" }}
          src={`https://www.facebook.com/tr?id=${measurementId}&ev=PageView&noscript=1`}
          alt="facebook-pixel"
        />
      </noscript>
    </>
  );
}
