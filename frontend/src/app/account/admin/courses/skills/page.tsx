import { createMetadata } from "src/utils/create-metadata";

import AccountCoursesSkillsView from "src/sections/view/account/admin/skills/account-courses-skills-view";

// ----------------------------------------------------------------------

export const metadata = createMetadata("Konto - Umiejętności");

export default function AccountCoursesSkillsPage() {
  return <AccountCoursesSkillsView />;
}
