/**
 * FILE: SchemaViewer.tsx
 * LAYER: 0 (Foundation)
 * PURPOSE: Visual schema inspector for understanding structured outputs
 *
 * CONCEPTS DEMONSTRATED:
 * - Schema introspection
 * - JSON visualization
 * - Educational debugging tools
 *
 * CHECKPOINT: L0-schema-viewer
 */

'use client';

import { SupportAnswerSchema, SUPPORT_CATEGORIES } from '@/lib/schemas';

export function SchemaViewer() {
  // Generate example valid object
  const exampleValid = {
    final_answer: "Your refund has been processed and will appear in your account within 5-7 business days.",
    confidence: 0.92,
    category: "billing" as const,
    followups: [
      "When will I see the refund?",
      "Can I get a receipt?"
    ],
    citations: ["refund-policy.pdf"],
    requires_human: false,
    metadata: {
      processing_time_ms: 1250,
      model_used: "claude-3-5-sonnet-20241022",
      layer: "L0-basic",
    },
  };

  // Test validation
  const validationResult = SupportAnswerSchema.safeParse(exampleValid);

  return (
    <div className="space-y-6">
      {/* Schema Overview */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          SupportAnswer Schema
        </h2>
        <p className="text-gray-700 mb-4">
          This schema defines the structure of all AI-generated support responses.
          It ensures consistency and enables type-safe programming.
        </p>

        {/* Fields */}
        <div className="space-y-3">
          <SchemaField
            name="final_answer"
            type="string"
            required
            constraints="min: 10 chars, max: 2000 chars"
            description="The actual response shown to the user"
          />
          <SchemaField
            name="confidence"
            type="number"
            required
            constraints="0.0 to 1.0"
            description="Model's self-assessed confidence score"
          />
          <SchemaField
            name="category"
            type="enum"
            required
            constraints={SUPPORT_CATEGORIES.join(' | ')}
            description="Classification of query type"
          />
          <SchemaField
            name="followups"
            type="string[]"
            required
            constraints="max: 3 items"
            description="Suggested follow-up questions"
          />
          <SchemaField
            name="citations"
            type="string[]"
            required
            constraints="no limit (can be empty)"
            description="Source references"
          />
          <SchemaField
            name="requires_human"
            type="boolean"
            required={false}
            constraints="default: false"
            description="Whether query needs human escalation"
          />
          <SchemaField
            name="metadata"
            type="object"
            required={false}
            constraints="optional debugging info"
            description="Processing metadata"
          />
        </div>
      </div>

      {/* Example Valid Object */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-3">
          Example Valid Object
        </h3>
        <pre className="bg-gray-50 rounded-lg p-4 overflow-x-auto text-sm">
          <code>{JSON.stringify(exampleValid, null, 2)}</code>
        </pre>
        <div className="mt-3 flex items-center text-green-700">
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
          <span className="font-medium">
            Validation: {validationResult.success ? 'PASSED ✓' : 'FAILED ✗'}
          </span>
        </div>
      </div>

      {/* Try It Out */}
      <div className="bg-blue-50 rounded-lg p-6 border border-blue-200">
        <h3 className="text-lg font-bold text-blue-900 mb-2">
          Try It Out
        </h3>
        <p className="text-blue-800 mb-3">
          Open your browser's developer console and try:
        </p>
        <pre className="bg-white rounded p-3 text-sm text-gray-800 overflow-x-auto">
{`import { SupportAnswerSchema } from '@/lib/schemas';

// Valid object
SupportAnswerSchema.parse({
  final_answer: "Test answer",
  confidence: 0.8,
  category: "general",
  followups: [],
  citations: [],
});

// Invalid object (will throw)
SupportAnswerSchema.parse({
  final_answer: "Too short", // < 10 chars
  confidence: 1.5, // > 1.0
});`}
        </pre>
      </div>
    </div>
  );
}

interface SchemaFieldProps {
  name: string;
  type: string;
  required: boolean;
  constraints: string;
  description: string;
}

function SchemaField({ name, type, required, constraints, description }: SchemaFieldProps) {
  return (
    <div className="border-l-4 border-blue-500 pl-4 py-2">
      <div className="flex items-center space-x-2 mb-1">
        <code className="text-sm font-mono font-bold text-gray-900">{name}</code>
        <span className="text-sm text-gray-600">{type}</span>
        {required && (
          <span className="text-xs bg-red-100 text-red-800 px-2 py-0.5 rounded">
            required
          </span>
        )}
      </div>
      <p className="text-sm text-gray-700 mb-1">{description}</p>
      <p className="text-xs text-gray-500 font-mono">{constraints}</p>
    </div>
  );
}
