"use client";

import Certificate from "../certificate/certificate";

// ----------------------------------------------------------------------

export default function CertificateView({ id }: { id: string }) {
  return <Certificate id={id} />;
}
