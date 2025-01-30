import { Metadata } from "next";

import { paths } from "src/routes/paths";

import { decodeUrl } from "src/utils/url-utils";
import { createMetadata } from "src/utils/create-metadata";

import { postQuery } from "src/api/posts/post";

import { PostView } from "src/sections/view/post-view";

// ----------------------------------------------------------------------

export default function PostPage({ params }: { params: { id: string } }) {
  return <PostView id={params.id} />;
}

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const decodedId = decodeUrl(params.id);
  const recordId = decodedId.slice(decodedId.lastIndexOf("-") + 1);

  const { queryFn } = postQuery(recordId);

  const { results: post } = await queryFn();

  const postTitle =
    post?.title ?? decodedId.slice(0, decodedId.lastIndexOf("-")).replace(/-/g, " ");
  const postDescription = post?.description
    ? post.description
    : `Przeczytaj nasz artykuł pod tytułem ${postTitle}. Odkryj praktyczne porady i najlepsze praktyki, które pomogą Ci w rozwoju umiejętności programistycznych.`;

  return createMetadata(
    `${postTitle} - przeczytaj artykuł już teraz`,
    postDescription,
    [
      postTitle,
      "programowanie",
      "nauka programowania",
      "najlepsze praktyki",
      "porady programistyczne",
      "szkoła programowania",
      "loop",
    ],
    `${paths.post}/${params.id}`,
    post?.coverUrl,
  );
}
