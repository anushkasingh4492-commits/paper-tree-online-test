import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Paper Tree Online Test",
  description: "Online testing platform for competitive exams",
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