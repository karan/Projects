/**
 * FILE: MessageBubble.tsx
 * LAYER: 0 (Foundation)
 * PURPOSE: Individual message display with structured data visualization
 *
 * CONCEPTS DEMONSTRATED:
 * - Conditional rendering based on message role
 * - Displaying structured AI responses
 * - Confidence visualization
 * - Accessible UI components
 *
 * CHECKPOINT: L0-message-bubble
 */

'use client';

import type { SupportAnswer } from '@/lib/schemas';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  structured_data?: SupportAnswer;
  timestamp: Date;
}

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-3xl ${isUser ? 'w-auto' : 'w-full'}`}>
        {/* Message bubble */}
        <div
          className={`rounded-lg px-4 py-3 ${
            isUser
              ? 'bg-blue-600 text-white'
              : 'bg-white border border-gray-200 text-gray-900'
          }`}
        >
          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        </div>

        {/* Structured data (assistant only) */}
        {!isUser && message.structured_data && (
          <div className="mt-2 space-y-2">
            {/* Confidence indicator */}
            <ConfidenceIndicator confidence={message.structured_data.confidence} />

            {/* Category badge */}
            <div className="flex items-center space-x-2">
              <CategoryBadge category={message.structured_data.category} />
              {message.structured_data.requires_human && (
                <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-orange-100 text-orange-800">
                  Requires Human
                </span>
              )}
            </div>

            {/* Follow-up questions */}
            {message.structured_data.followups.length > 0 && (
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-xs font-medium text-gray-700 mb-2">
                  Related questions:
                </p>
                <ul className="space-y-1">
                  {message.structured_data.followups.map((q, i) => (
                    <li key={i} className="text-sm text-gray-600">
                      • {q}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Citations */}
            {message.structured_data.citations.length > 0 && (
              <div className="text-xs text-gray-500">
                Sources: {message.structured_data.citations.join(', ')}
              </div>
            )}
          </div>
        )}

        {/* Timestamp */}
        <div className={`text-xs text-gray-500 mt-1 ${isUser ? 'text-right' : 'text-left'}`}>
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}

/**
 * Confidence indicator component
 */
function ConfidenceIndicator({ confidence }: { confidence: number }) {
  const percentage = Math.round(confidence * 100);
  const color =
    confidence >= 0.8
      ? 'bg-green-500'
      : confidence >= 0.5
      ? 'bg-yellow-500'
      : 'bg-red-500';

  return (
    <div className="flex items-center space-x-2">
      <div className="flex-1 bg-gray-200 rounded-full h-2 max-w-[100px]">
        <div
          className={`${color} h-2 rounded-full transition-all`}
          style={{ width: `${percentage}%` }}
          role="progressbar"
          aria-valuenow={percentage}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label="Confidence level"
        />
      </div>
      <span className="text-xs text-gray-600">{percentage}% confident</span>
    </div>
  );
}

/**
 * Category badge component
 */
function CategoryBadge({ category }: { category: string }) {
  const colors: Record<string, string> = {
    billing: 'bg-blue-100 text-blue-800',
    technical: 'bg-purple-100 text-purple-800',
    account: 'bg-green-100 text-green-800',
    feature_request: 'bg-yellow-100 text-yellow-800',
    general: 'bg-gray-100 text-gray-800',
    escalation: 'bg-red-100 text-red-800',
  };

  const colorClass = colors[category] || colors.general;

  return (
    <span
      className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${colorClass}`}
    >
      {category.replace('_', ' ')}
    </span>
  );
}
