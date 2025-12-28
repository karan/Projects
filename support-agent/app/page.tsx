/**
 * FILE: page.tsx
 * LAYER: 0 (Foundation)
 * PURPOSE: Main application page with chat interface
 *
 * CONCEPTS DEMONSTRATED:
 * - Next.js App Router pages
 * - Client component composition
 * - Layout structure
 *
 * CHECKPOINT: L0-main-page
 */

import { ChatInterface } from '@/components/chat/ChatInterface';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="container mx-auto max-w-6xl h-screen flex flex-col">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200 px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <span className="text-sm font-medium text-gray-700">
              Support Agent - Layer 0
            </span>
          </div>
          <Link
            href="/debug"
            className="text-sm text-blue-600 hover:text-blue-800 font-medium"
          >
            Debug View →
          </Link>
        </div>
      </nav>

      {/* Chat Interface */}
      <div className="flex-1 overflow-hidden">
        <ChatInterface />
      </div>
    </div>
  );
}
