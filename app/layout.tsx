import type { Metadata } from "next";
import "./globals.css";
import StudentThemeManager from "@/components/StudentThemeManager";

export const metadata: Metadata = {
 title: "Paper Tree CBT | Online Testing for Institutes",
  description: "A modern online testing platform for NEET, JEE Main and MHT-CET coaching institutes.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}<StudentThemeManager /></body>
    </html>
  );
}