import React from "react";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
// ----------------------------------------------------------------------

export type MarkdownProps = {
  content: string;
};

interface CodeProps {
  node?: any;
  inline?: boolean;
  className?: string;
  children?: React.ReactNode;
}

export function Markdown({ content }: MarkdownProps) {
  const typographicReplacements = (text: string) =>
    text
      .replace(/\(c\)/gi, "©")
      .replace(/\(r\)/gi, "®")
      .replace(/\(tm\)/gi, "™")
      .replace(/\(p\)/gi, "§")
      .replace(/\+-/g, "±");

  return (
    <ReactMarkdown
      children={typographicReplacements(content)}
      components={{
        code({ node, inline, className, children, ...props }: CodeProps) {
          const match = /language-(\w+)/.exec(className || "");
          const language = match ? match[1] : "plaintext";

          return !inline ? (
            <SyntaxHighlighter style={vscDarkPlus} language={language} PreTag="div" {...props}>
              {String(children).replace(/\n$/, "")}
            </SyntaxHighlighter>
          ) : (
            <code className={className} {...props}>
              {children} {/* Correctly display children here */}
            </code>
          );
        },
        table({ children }) {
          return <table style={{ borderCollapse: "collapse", width: "100%" }}>{children}</table>;
        },
        th({ children }) {
          return (
            <th
              style={{
                border: "1px solid black",
                padding: "8px",
                textAlign: "left",
                backgroundColor: "#f2f2f2",
              }}
            >
              {children}
            </th>
          );
        },
        td({ children }) {
          return <td style={{ border: "1px solid black", padding: "8px" }}>{children}</td>;
        },
        tr({ children }) {
          return <tr>{children}</tr>;
        },
        a({ href, children }) {
          return (
            <a
              href={href}
              style={{
                textDecoration: "none",
                fontWeight: "normal",
                color: "#018257",
              }}
            >
              {children}
            </a>
          );
        },
        blockquote({ children }) {
          return (
            <blockquote
              style={{
                borderLeft: "4px solid #ddd",
                marginLeft: 0,
                marginRight: 0,
                paddingLeft: "1em",
                color: "#555",
                fontStyle: "italic",
              }}
            >
              {children}
            </blockquote>
          );
        },
      }}
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeRaw, rehypeSanitize]}
      remarkRehypeOptions={{ passThrough: ["link"] }}
    />
  );
}
