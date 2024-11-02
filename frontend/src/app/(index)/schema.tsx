"use client";

import Script from "next/script";

const ClientSchema = () => {
  const schemaData = {
    "@context": "https://schema.org",
    "@type": "EducationalOrganization",
    name: "loop - szkoła programowania",
    url: "https://loop.edu.pl",
    logo: "https://loop.edu.pl/logo/logo.svg",
    description:
      "Naucz się programować w loop – oferujemy kursy Python, JavaScript, C++, oraz wiele innych. Rozwijaj swoją karierę IT z najlepszymi instruktorami, korzystając z nowoczesnych metod nauki i materiałów dostępnych 24/7.",
    foundingDate: "2024-01-01",
    address: {
      "@type": "PostalAddress",
      addressCountry: "PL",
      addressRegion: "Małopolskie",
      postalCode: "30-716",
    },
    contactPoint: {
      "@type": "ContactPoint",
      contactType: "Obsługa klienta",
      email: "info@loop.edu.pl",
      telephone: "+48-881-455-596",
      availableLanguage: ["Polish"],
    },
  };

  if (typeof window === "undefined") {
    return null;
  }

  return (
    <Script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schemaData) }}
    />
  );
};

export default function Schema() {
  if (typeof window === "undefined") {
    return null;
  }

  return <ClientSchema />;
}
