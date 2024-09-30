/* eslint-disable perfectionist/sort-imports */
import "src/global.css";

// ----------------------------------------------------------------------

import ThemeProvider from "src/theme";
import { primaryFont } from "src/theme/typography";
import { LocalizationProvider } from "src/locales";

import ProgressBar from "src/components/progress-bar";
import { MotionLazy } from "src/components/animate/motion-lazy";
import { SettingsProvider } from "src/components/settings";
import { UserProvider } from "src/components/user";
import { ToastProvider } from "src/components/toast";
import CookiesManager from "src/components/cookies/cookies-manager";
import { ReactQueryProvider } from "./(index)/react-query-provider";

// ----------------------------------------------------------------------

export const viewport = {
  themeColor: "#000000",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export const metadata = {
  manifest: "/manifest.json",
  icons: [{ rel: "icon", url: "/favicon/favicon.ico" }],
};

type Props = {
  children: React.ReactNode;
};

export default function RootLayout({ children }: Props) {
  return (
    <html lang="en" className={primaryFont.className}>
      <body>
        <ReactQueryProvider>
          <UserProvider>
            <LocalizationProvider>
              <SettingsProvider
                defaultSettings={{
                  themeMode: "light",
                  themeDirection: "ltr",
                  themeColorPresets: "default",
                }}
              >
                <ThemeProvider>
                  <ToastProvider>
                    <MotionLazy>
                      <ProgressBar />
                      <CookiesManager />
                      {children}
                    </MotionLazy>
                  </ToastProvider>
                </ThemeProvider>
              </SettingsProvider>
            </LocalizationProvider>
          </UserProvider>
        </ReactQueryProvider>
      </body>
    </html>
  );
}
