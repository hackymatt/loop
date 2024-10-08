"use client";

import { useMemo } from "react";
import { polishPlurals } from "polish-plurals";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Divider from "@mui/material/Divider";
import Grid from "@mui/material/Unstable_Grid2";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import { Avatar, IconButton, AvatarGroup } from "@mui/material";

import { paths } from "src/routes/paths";

import { fDate } from "src/utils/format-time";
import { createMetadata } from "src/utils/create-metadata";

import { _coursePosts } from "src/_mock";

import Iconify from "src/components/iconify";
import { Markdown } from "src/components/markdown";
import CustomBreadcrumbs from "src/components/custom-breadcrumbs";

import { IAuthorProps } from "src/types/author";

import Newsletter from "../newsletter/newsletter";
import { PostAuthors } from "../posts/post-author";
import { LatestPosts } from "../posts/latest-posts";
import { PrevNextButton } from "../posts/post-prev-and-next";

// ----------------------------------------------------------------------

const post = _coursePosts[0];
const prevPost = _coursePosts[1];
const nextPost = _coursePosts[2];
const latestPosts = _coursePosts.slice(3, 6);

export function PostView() {
  const renderToolbar = (
    <Box
      gap={1.5}
      display="flex"
      sx={(theme) => ({
        py: 3,
        my: 5,
        borderTop: `solid 1px ${theme.palette.divider}`,
        borderBottom: `solid 1px ${theme.palette.divider}`,
      })}
    >
      <AvatarGroup total={post.authors.length} max={1}>
        {post.authors.map((author: IAuthorProps) => {
          const genderAvatarUrl =
            author?.gender === "Kobieta"
              ? "/assets/images/avatar/avatar_female.jpg"
              : "/assets/images/avatar/avatar_male.jpg";

          const avatarUrl = author?.avatarUrl || genderAvatarUrl;
          return <Avatar key={author.id} src={avatarUrl} />;
        })}
      </AvatarGroup>

      <Stack spacing={0.5} flexGrow={1} typography="subtitle2">
        <Stack direction="row" spacing={0.5}>
          {post.authors[0].name}
          {post.authors.length > 1 && (
            <Typography
              color="text.secondary"
              variant="subtitle2"
              sx={{ textDecoration: "underline" }}
            >
              + {post.authors.length - 1}{" "}
              {polishPlurals("autor", "autorów", "autorów", post.authors.length - 1)}
            </Typography>
          )}
        </Stack>
        <Typography variant="caption" sx={{ color: "text.secondary" }}>
          {fDate(post.createdAt)}
        </Typography>
      </Stack>

      <Box display="flex" alignItems="center">
        <IconButton
          onClick={() =>
            navigator.share({ url: "xxxxx", title: post.title, text: post.description })
          }
        >
          <Iconify icon="solar:share-outline" />
        </IconButton>
      </Box>
    </Box>
  );

  const markdown = `
# A demo of \`react-markdown\`

\`react-markdown\` is a markdown component for React.

👉 Changes are re-rendered as you type.

👈 Try writing some markdown on the left.

## Overview

* Follows [CommonMark](https://commonmark.org)
* Optionally follows [GitHub Flavored Markdown](https://github.github.com/gfm/)
* Renders actual React elements instead of using \`dangerouslySetInnerHTML\`
* Lets you define your own components (to render \`MyHeading\` instead of 'h1')
* Has a lot of plugins

## Contents

Here is an example of a plugin in action ([\`remark-toc\`](https://github.com/remarkjs/remark-toc)).
**This section is replaced by an actual table of contents**.

## Syntax highlighting

Here is an example of a plugin to highlight code: [\`rehype-highlight\`](https://github.com/rehypejs/rehype-highlight).

\`\`\`js
import React from 'react'
import ReactDOM from 'react-dom'
import Markdown from 'react-markdown'
import rehypeHighlight from 'rehype-highlight'

const markdown = \`
# Your markdown here
\`

ReactDOM.render(
  <Markdown rehypePlugins={[rehypeHighlight]}>{markdown}</Markdown>,
  document.querySelector('#content')
)
\`\`\`

Pretty neat, eh?

## GitHub flavored markdown (GFM)

For GFM, you can *also* use a plugin: [\`remark-gfm\`](https://github.com/remarkjs/react-markdown#use).
It adds support for GitHub-specific extensions to the language:
tables, strikethrough, tasklists, and literal URLs.

These features **do not work by default**.
👆 Use the toggle above to add the plugin.

| Feature    | Support              |
| ---------: | :------------------- |
| CommonMark | 100%                 |
| GFM        | 100% w/ \`remark-gfm\` |

~~strikethrough~~

* [ ] task list
* [x] checked item

https://example.com

## HTML in markdown

⚠️ HTML in markdown is quite unsafe, but if you want to support it, you can use [\`rehype-raw\`](https://github.com/rehypejs/rehype-raw).
You should probably combine it with [\`rehype-sanitize\`](https://github.com/rehypejs/rehype-sanitize).

<blockquote>
  👆 Use the toggle above to add the plugin.
</blockquote>

## Components

You can pass components to change things:

\`\`\`js
import React from 'react'
import ReactDOM from 'react-dom'
import Markdown from 'react-markdown'
import MyFancyRule from './components/my-fancy-rule.js'

const markdown = \`
# Your markdown here
\`

ReactDOM.render(
  <Markdown
    components={{
      // Use h2s instead of h1s
      h1: 'h2',
      // Use a component instead of hrs
      hr(props) {
        const {node, ...rest} = props
        return <MyFancyRule {...rest} />
      }
    }}
  >
    {markdown}
  </Markdown>,
  document.querySelector('#content')
)
\`\`\`

## More info?

Much more info is available in the [readme on GitHub](https://github.com/remarkjs/react-markdown)!

***

A component by [Espen Hovlandsdal](https://espen.codes/)
`;

  const metadata = useMemo(
    () =>
      createMetadata(
        `Artykuł: ${post.title}`,
        `Przeczytaj nasz artykuł o ${post.title}. Dowiedz się, jak ${post.description.toLowerCase()}. Odkryj praktyczne porady i najlepsze praktyki, które pomogą Ci w rozwoju umiejętności programistycznych.`,
        [
          post.title,
          post.description,
          "programowanie",
          "nauka programowania",
          "najlepsze praktyki",
          "porady programistyczne",
          "szkoła programowania",
          "loop",
        ],
      ),
    [],
  );

  return (
    <>
      <title>{metadata.title}</title>
      <meta name="description" content={metadata.description} />
      <meta name="keywords" content={metadata.keywords} />
      <Divider />

      <Container>
        <CustomBreadcrumbs
          links={[
            { name: "Strona główna", href: "/" },
            { name: "Blog", href: paths.posts },
            { name: post.title },
          ]}
          sx={{ my: { xs: 3, md: 5 } }}
        />

        <Box
          display="flex"
          alignItems="center"
          justifyContent="center"
          sx={(theme) => ({
            borderRadius: 2,
            overflow: "hidden",
            position: "relative",
            backgroundSize: "cover",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
            aspectRatio: { xs: "16/9", md: "21/9" },
            backgroundImage: `url(${post.coverUrl})`,
          })}
        />

        <Grid container disableEqualOverflow spacing={3} justifyContent={{ md: "center" }}>
          <Grid xs={12} md={8}>
            <Stack
              spacing={3}
              sx={{
                textAlign: "center",
                mt: { xs: 5, md: 10 },
              }}
            >
              <Typography variant="body2" sx={{ color: "text.disabled" }}>
                {post.duration}
              </Typography>

              <Typography variant="h2" component="h1">
                {post.title}
              </Typography>

              <Typography variant="h5">{post.description}</Typography>
            </Stack>

            {renderToolbar}

            <Markdown content={markdown} />

            <Divider sx={{ mt: 10 }} />

            <PostAuthors authors={post.authors} />

            <Divider />

            <Box
              gap={5}
              display="grid"
              gridTemplateColumns={{ xs: "repeat(1, 1fr)", md: "repeat(2, 1fr)" }}
              sx={{ py: 10 }}
            >
              <PrevNextButton title={prevPost?.title} coverUrl={prevPost?.coverUrl} href="#" />
              <PrevNextButton
                isNext
                title={nextPost?.title}
                coverUrl={nextPost?.coverUrl}
                href="#"
              />
            </Box>
          </Grid>
        </Grid>
      </Container>

      <Divider />

      <LatestPosts posts={latestPosts} />

      <Newsletter />
    </>
  );
}
