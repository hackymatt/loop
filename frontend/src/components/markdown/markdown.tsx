import React from "react";
import "@mdxeditor/editor/style.css";
import { MDXEditor } from "@mdxeditor/editor";

import "./styles.css";
import { plugins } from "../markdown-editor/pluggins";

// ----------------------------------------------------------------------

type MarkdownProps = {
  content: string;
};

export function Markdown({ content, ...other }: MarkdownProps) {
  return <MDXEditor className="" markdown={content} plugins={plugins} readOnly {...other} />;
}
