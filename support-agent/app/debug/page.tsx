/**
 * FILE: debug/page.tsx
 * LAYER: 0 (Foundation)
 * PURPOSE: Debug and introspection view for learning about schemas
 *
 * CONCEPTS DEMONSTRATED:
 * - Schema visualization
 * - Educational tooling
 * - Development aids
 *
 * CHECKPOINT: L0-debug-page
 */

import { SchemaViewer } from '@/components/debug/SchemaViewer';
import Link from 'next/link';
import { getModelDisplayName, GENERATION_SETTINGS } from '@/lib/ai/config';
import { PROMPT_VERSION } from '@/lib/ai/prompts';

export default function DebugPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto max-w-6xl py-8 px-6">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/"
            className="text-blue-600 hover:text-blue-800 font-medium mb-4 inline-block"
          >
            ← Back to Chat
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Debug View
          </h1>
          <p className="text-gray-600">
            Inspect schemas, configuration, and system internals
          </p>
        </div>

        {/* Configuration Panel */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Current Configuration
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <ConfigItem label="AI Model" value={getModelDisplayName()} />
            <ConfigItem label="Prompt Version" value={PROMPT_VERSION} />
            <ConfigItem label="Temperature" value={GENERATION_SETTINGS.temperature} />
            <ConfigItem label="Max Tokens" value={GENERATION_SETTINGS.maxTokens} />
            <ConfigItem label="Layer" value="L0 (Foundation)" />
            <ConfigItem
              label="Features"
              value="Structured outputs only (no RAG, no memory)"
            />
          </div>
        </div>

        {/* Schema Viewer */}
        <SchemaViewer />

        {/* Learning Resources */}
        <div className="mt-6 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-6 border border-purple-200">
          <h3 className="text-lg font-bold text-purple-900 mb-3">
            Learning Resources
          </h3>
          <ul className="space-y-2">
            <li>
              <a
                href="https://sdk.vercel.ai/docs/ai-sdk-core/generating-structured-data"
                target="_blank"
                rel="noopener noreferrer"
                className="text-purple-700 hover:text-purple-900 underline"
              >
                Vercel AI SDK: Structured Data Guide
              </a>
            </li>
            <li>
              <a
                href="https://zod.dev"
                target="_blank"
                rel="noopener noreferrer"
                className="text-purple-700 hover:text-purple-900 underline"
              >
                Zod Documentation
              </a>
            </li>
            <li>
              <a
                href="https://docs.anthropic.com/claude/docs/prompt-engineering"
                target="_blank"
                rel="noopener noreferrer"
                className="text-purple-700 hover:text-purple-900 underline"
              >
                Anthropic: Prompt Engineering Guide
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}

function ConfigItem({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="bg-gray-50 rounded-lg p-3">
      <div className="text-xs font-medium text-gray-600 mb-1">{label}</div>
      <div className="text-sm font-mono text-gray-900">{value}</div>
    </div>
  );
}
