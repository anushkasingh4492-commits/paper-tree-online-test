import type { Metadata } from "next";
import "./globals.css";

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
      <body>{children}</body>
    </html>
  );
}