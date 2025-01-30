import { Metadata } from "next";

import { paths } from "src/routes/paths";

import { createMetadata } from "src/utils/create-metadata";

import { certificateQuery } from "src/api/certificates/certificate";

import CertificateView from "src/sections/view/certificate-view";

import { CertificateType } from "src/types/certificate";

// ----------------------------------------------------------------------

export default function CertificatePage({ params }: { params: { id: string } }) {
  return <CertificateView id={params.id} />;
}

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const { queryFn } = certificateQuery(params.id);

  const { results: certificate } = await queryFn();

  const getType = () => {
    switch (certificate?.type) {
      case CertificateType.LESSON:
        return "lekcji";
      case CertificateType.MODULE:
        return "modułu";
      case CertificateType.COURSE:
        return "kursu";
      default:
        return "lekcji";
    }
  };

  const type = getType();
  const title = certificate?.title ? ` ${certificate.title}` : "";
  const studentName = certificate?.studentName ? ` dla ${certificate.studentName}` : "";

  return createMetadata(
    `Certyfikat ukończenia ${type}${title}${studentName}`,
    undefined,
    undefined,
    `${paths.certificate}/${params.id}`,
  );
}
