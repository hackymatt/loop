import {
  UndoRedo,
  Separator,
  CodeToggle,
  CreateLink,
  ListsToggle,
  InsertImage,
  InsertTable,
  EditorInFocus,
  DirectiveNode,
  BlockTypeSelect,
  InsertCodeBlock,
  ShowSandpackInfo,
  InsertAdmonition,
  ConditionalContents,
  InsertThematicBreak,
  ChangeAdmonitionType,
  ChangeCodeMirrorLanguage,
  BoldItalicUnderlineToggles,
} from "@mdxeditor/editor";

function whenInAdmonition(editorInFocus: EditorInFocus | null) {
  const node = editorInFocus?.rootNode;
  if (!node || node.getType() !== "directive") {
    return false;
  }

  return ["note", "tip", "danger", "info", "caution"].includes(
    (node as DirectiveNode).getMdastNode().name,
  );
}

export const Toolbar = () => (
  <ConditionalContents
    options={[
      {
        when: (editor) => editor?.editorType === "codeblock",
        contents: () => <ChangeCodeMirrorLanguage />,
      },
      {
        when: (editor) => editor?.editorType === "sandpack",
        contents: () => <ShowSandpackInfo />,
      },
      {
        fallback: () => (
          <>
            <UndoRedo />
            <Separator />
            <BoldItalicUnderlineToggles />
            <CodeToggle />
            <Separator />
            <ListsToggle />
            <Separator />

            <ConditionalContents
              options={[
                {
                  when: whenInAdmonition,
                  contents: () => <ChangeAdmonitionType />,
                },
                { fallback: () => <BlockTypeSelect /> },
              ]}
            />

            <Separator />

            <CreateLink />
            <InsertImage />

            <Separator />

            <InsertTable />
            <InsertThematicBreak />

            <Separator />
            <InsertCodeBlock />

            <ConditionalContents
              options={[
                {
                  when: (editorInFocus) => !whenInAdmonition(editorInFocus),
                  contents: () => (
                    <>
                      <Separator />
                      <InsertAdmonition />
                    </>
                  ),
                },
              ]}
            />
          </>
        ),
      },
    ]}
  />
);
