import packageInfo from "package.json";

import AccountCoursesSkillsView from "src/sections/_elearning/view/account/admin/account-courses-skills-view";

// ----------------------------------------------------------------------

export const metadata = {
  title: `${packageInfo.name}: Konto - Umiejętności`,
};

export default function AccountCoursesSkillsPage() {
  return <AccountCoursesSkillsView />;
}
