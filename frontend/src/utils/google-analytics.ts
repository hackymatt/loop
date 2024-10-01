type IConsentValuesProp = {
  analytics_storage: "granted" | "denied";
};

export const updateConsent = (consentValues: IConsentValuesProp) =>
  window.gtag("consent", "update", consentValues);

export const pageView = (measurementId: string, url: string) => {
  window.gtag("config", measurementId, {
    page_path: url,
  });
};

export const trackEvent = (action: string, category: string, label: string, value: string) => {
  window.gtag("event", action, {
    event_category: category,
    event_label: label,
    value,
  });
};
