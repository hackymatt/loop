/* eslint-disable perfectionist/sort-imports */
import "src/global.css";

// ----------------------------------------------------------------------

import ThemeProvider from "src/theme";
import { primaryFont } from "src/theme/typography";
import { LocalizationProvider } from "src/locales";

import ProgressBar from "src/components/progress-bar";
import { MotionLazy } from "src/components/animate/motion-lazy";
import { SettingsDrawer, SettingsProvider } from "src/components/settings";
import { UserProvider } from "src/components/user";
import { ToastProvider } from "src/components/toast";
import { ReactQueryProvider } from "./(index)/react-query-provider";

// ----------------------------------------------------------------------

export const viewport = {
  themeColor: "#000000",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export const metadata = {
  title: "loop",
  description:
    "Platforma firmy loop oferującej kursy programowania online dla przyszłych i obecnych programistów",
  keywords: "loop,szkoła,kursy,programowanie,it,tanio,profesjonalnie,online,zdalne",
  manifest: "/manifest.json",
  icons: [
    { rel: "icon", url: "/favicon/favicon.ico" },
    { rel: "icon", type: "image/png", sizes: "16x16", url: "/favicon/favicon-16x16.png" },
    { rel: "icon", type: "image/png", sizes: "32x32", url: "/favicon/favicon-32x32.png" },
    { rel: "apple-touch-icon", sizes: "180x180", url: "/favicon/apple-touch-icon.png" },
  ],
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
                  themeMode: "light", // 'light' | 'dark'
                  themeDirection: "ltr", //  'rtl' | 'ltr'
                  themeColorPresets: "default", // 'default' | 'preset01' | 'preset02' | 'preset03' | 'preset04' | 'preset05'
                }}
              >
                <ThemeProvider>
                  <ToastProvider>
                    <MotionLazy>
                      <ProgressBar />
                      <SettingsDrawer />
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
