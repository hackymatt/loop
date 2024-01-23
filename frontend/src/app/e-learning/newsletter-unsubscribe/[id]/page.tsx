import packageInfo from "package.json";

import NewsletterUnsubscribeView from "src/sections/_elearning/view/newsletter-unsubscribe-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Anulowanie subskrypcji`,
};

export default function NewsletterUnsubscribePage({ params }: { params: { id: string } }) {
  return <NewsletterUnsubscribeView id={params.id} />;
}
