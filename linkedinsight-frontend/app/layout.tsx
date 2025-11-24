import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";
import { Sidebar } from "./components/sidebar";
import { MobileNav } from "./components/mobile-nav";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "LinkedInsight - AI-powered career & skills navigator",
  description: "Discover your ideal career path, identify skill gaps, and get personalized learning roadmaps powered by AI.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Providers>
          <div className="flex h-screen bg-gray-50">
            <Sidebar />
            <div className="flex flex-col flex-1 md:pl-64">
              <main className="flex-1 overflow-y-auto pb-16 md:pb-0">
                {children}
              </main>
              <MobileNav />
            </div>
          </div>
        </Providers>
      </body>
    </html>
  );
}
