import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Doctor Companion - Medical Assistant",
  description: "Your AI-powered medical companion for disease information and image analysis",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-50`}>
          <main className="min-h-screen">
            {children}
          </main>

      </body>
    </html>
  );
}
