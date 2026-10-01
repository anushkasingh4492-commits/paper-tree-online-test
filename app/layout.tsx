import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
 title: "CBT",
  description: "Competitive exam preparation and testing platform",
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