/**
 * FILE: types/index.ts
 * LAYER: 0 (Foundation)
 * PURPOSE: Global TypeScript type definitions and utility types
 *
 * CONCEPTS DEMONSTRATED:
 * - Type-only imports/exports
 * - Utility type patterns
 * - Domain modeling with types
 *
 * CHECKPOINT: L0-typescript-types
 *
 * LEARN MORE:
 * - https://www.typescriptlang.org/docs/handbook/utility-types.html
 */

/**
 * Re-export schema-derived types for convenience
 *
 * NOTE: All types are inferred from Zod schemas,
 * so this is mostly for organization.
 */
export type {
  SupportAnswer,
  SupportCategory,
  UserQuery,
  ChatRequest,
  ChatResponse,
} from '@/lib/schemas';

/**
 * Message types for chat interface
 */
export type MessageRole = 'user' | 'assistant' | 'system';

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
  /** For assistant messages, this contains the structured data */
  structured_data?: unknown;
}

/**
 * UI State types
 */
export interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
}

/**
 * API Error types
 */
export interface APIError {
  code: ErrorCode;
  message: string;
  details?: unknown;
  timestamp: string;
  request_id: string;
}

export type ErrorCode =
  | 'VALIDATION_ERROR'
  | 'AI_ERROR'
  | 'RATE_LIMIT'
  | 'INTERNAL_ERROR'
  | 'UNKNOWN_ERROR';

/**
 * Utility types for working with structured outputs
 */

/** Make all fields of T optional recursively */
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

/** Extract keys from T where value is of type U */
export type KeysOfType<T, U> = {
  [K in keyof T]: T[K] extends U ? K : never;
}[keyof T];

/** Make specific keys K of type T required */
export type RequireKeys<T, K extends keyof T> = T & Required<Pick<T, K>>;

/**
 * EXAMPLE USAGE:
 *
 * // Make only 'final_answer' required
 * type MinimalAnswer = RequireKeys<
 *   DeepPartial<SupportAnswer>,
 *   'final_answer'
 * >;
 *
 * // Get all string fields from SupportAnswer
 * type StringFields = KeysOfType<SupportAnswer, string>;
 * // Result: 'final_answer' | 'category'
 */
