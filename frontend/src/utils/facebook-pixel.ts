type IConsentValuesProp = "grant" | "revoke";

export const updateConsent = (consentValues: IConsentValuesProp) => {
  if (window) {
    (window as any).fbq("consent", consentValues);
  }
};

export const pageView = () => {
  if (window) {
    window.fbq("track", "PageView");
  }
};

export const trackEvent = (action: string, category: string, label: string, value: string) => {
  if (window) {
    window.fbq("track", action, {
      event_category: category,
      event_label: label,
      value,
    });
  }
};
