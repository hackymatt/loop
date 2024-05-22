import { createMetadata } from "src/utils/create-metadata";

import NewsletterUnsubscribeView from "src/sections/view/newsletter-unsubscribe-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Anulowanie subskrypcji");

export default function NewsletterUnsubscribePage({ params }: { params: { id: string } }) {
  return <NewsletterUnsubscribeView id={params.id} />;
}
