type IConsentValuesProp = {
  analytics_storage: "granted" | "denied";
};

export const updateConsent = (consentValues: IConsentValuesProp) => {
  if (window) {
    (window as any).gtag("consent", "update", consentValues);
  }
};

export const pageView = (measurementId: string, url: string) => {
  if (window) {
    window.gtag("config", measurementId, {
      page_path: url,
    });
  }
};

export const trackEvent = (action: string, category: string, label: string, value: string) => {
  if (window) {
    window.gtag("event", action, {
      event_category: category,
      event_label: label,
      value,
    });
  }
};
