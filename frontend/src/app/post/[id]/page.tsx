import { Metadata } from "next";

import { decodeUrl } from "src/utils/url-utils";
import { createMetadata } from "src/utils/create-metadata";

import { PostView } from "src/sections/view/post-view";

// ----------------------------------------------------------------------

export default function PostPage({ params }: { params: { id: string } }) {
  return <PostView id={params.id} />;
}

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const decodedId = decodeUrl(params.id);
  const postTitle = decodedId.slice(0, decodedId.lastIndexOf("-")).replace(/-/g, " ");

  const metadata = createMetadata(
    `${postTitle} - przeczytaj artykuł już teraz`,
    `Przeczytaj nasz artykuł o ${postTitle}. Odkryj praktyczne porady i najlepsze praktyki, które pomogą Ci w rozwoju umiejętności programistycznych.`,
    [
      postTitle,
      "programowanie",
      "nauka programowania",
      "najlepsze praktyki",
      "porady programistyczne",
      "szkoła programowania",
      "loop",
    ],
  );

  return {
    title: metadata.title,
    description: metadata.description,
    keywords: metadata.keywords,
  };
}
