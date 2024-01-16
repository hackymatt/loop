// ----------------------------------------------------------------------

import NewsletterUnsubscribeView from "src/sections/_elearning/view/newsletter-unsubscribe-view";

export const metadata = {
  title: "E-learning: Newsletter unsubscribe",
};

export default function NewsletterUnsubscribePage({ params }: { params: { id: string } }) {
  return <NewsletterUnsubscribeView id={params.id} />;
}
