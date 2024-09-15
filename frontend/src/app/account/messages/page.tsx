import { createMetadata } from "src/utils/create-metadata";

import AccountMessagesView from "src/sections/view/account/user/messages/account-messages-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Wiadomości");

export default function AccountMessagesPage() {
  return <AccountMessagesView />;
}
