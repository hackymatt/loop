import { trackEvent as fpTrackEvent } from "./facebook-pixel";
import { trackEvent as gaTrackEvent } from "./google-analytics";

export const trackEvents = (action: string, category: string, label: string, value: string) => {
  gaTrackEvent(action, category, label, value);
  fpTrackEvent(action, category, label, value);
};
