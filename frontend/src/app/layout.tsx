import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import React from "react";
import { Toaster } from "sonner";
import "./globals.css";

const geistSans = Geist({
    variable: "--font-geist-sans",
    subsets: ["latin"],
    display: "swap",
});

const geistMono = Geist_Mono({
    variable: "--font-geist-mono",
    subsets: ["latin"],
    display: "swap",
});

export const metadata: Metadata = {
    title: "Leet-Search",
    description: "Search LeetCode problems using natural language. AI-powered semantic matching to help you find the right problem faster.",
    icons: {
        icon: "/icon.svg"
    },
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en" className="dark">
            <body
                className={`min-h-screen bg-background font-sans antialiased ${geistSans.variable} ${geistMono.variable}`}
            >
                {children}
                <Toaster position="top-right" richColors />
            </body>
        </html>
    );
}
