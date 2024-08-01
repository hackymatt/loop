import { createMetadata } from "src/utils/create-metadata";

import CertificateView from "src/sections/view/certificate-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Certyfikat ukończenia");

export default function CertificatePage({ params }: { params: { id: string } }) {
  return <CertificateView id={params.id} />;
}
