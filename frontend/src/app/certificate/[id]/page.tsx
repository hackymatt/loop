import { Metadata } from "next";

import { paths } from "src/routes/paths";

import { createMetadata } from "src/utils/create-metadata";

import CertificateView from "src/sections/view/certificate-view";

// ----------------------------------------------------------------------

export default function CertificatePage({ params }: { params: { id: string } }) {
  return <CertificateView id={params.id} />;
}

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  return createMetadata(
    "Certyfikat ukończenia",
    undefined,
    undefined,
    `${paths.certificate}/${params.id}`,
  );
}
