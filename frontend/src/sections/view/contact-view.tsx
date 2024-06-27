"use client";

import Newsletter from "../newsletter/newsletter";
import ContactForm from "../contact/contact-form";
import ContactInfo from "../contact/contact-info";

// ----------------------------------------------------------------------

export default function ContactView() {
  return (
    <>
      <ContactInfo />
      <ContactForm />
      <Newsletter />
    </>
  );
}
