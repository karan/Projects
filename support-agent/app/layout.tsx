/**
 * FILE: layout.tsx
 * LAYER: 0 (Foundation)
 * PURPOSE: Root layout with global styles and metadata
 *
 * CONCEPTS DEMONSTRATED:
 * - Next.js App Router layout system
 * - Global CSS imports
 * - Metadata configuration for SEO
 *
 * CHECKPOINT: L0-root-layout
 *
 * LEARN MORE:
 * - https://nextjs.org/docs/app/building-your-application/routing/pages-and-layouts
 */

import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Support Agent - Layer 0',
  description: 'AI-powered support agent with structured outputs (Learning Project)',
  keywords: ['AI', 'support', 'chatbot', 'structured outputs', 'LLM'],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
          {children}
        </div>
      </body>
    </html>
  );
}
