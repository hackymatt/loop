import { ViewUtil } from "src/utils/page-utils";
import { createMetadata } from "src/utils/create-metadata";

import TeachersView from "src/sections/view/teachers-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata(
  "Instruktorzy - sprawdź oferowane lekcje",
  "Poznaj instruktorów loop — doświadczonych programistów, którzy poprowadzą Cię przez kursy programowania online. Sprawdź profile naszych nauczycieli i wybierz idealnego instruktora dla siebie.",
  [
    "instruktorzy",
    "nauczyciele programowania",
    "loop instruktorzy",
    "doświadczeni programiści",
    "profesjonalni instruktorzy",
    "prowadzący kursy programowania",
    "mentoring programistyczny",
    "wybór instruktora",
    "nauka z instruktorem",
    "szkoła programowania loop",
  ],
);
export default function CoursesPage() {
  return <ViewUtil defaultView={<TeachersView />} />;
}
