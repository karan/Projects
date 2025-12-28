/**
 * FILE: validation.ts
 * LAYER: 0 (Foundation)
 * PURPOSE: Input validation schemas for user queries and API requests
 *
 * CONCEPTS DEMONSTRATED:
 * - Input sanitization and validation
 * - Protection against malicious inputs
 * - Request/response type safety
 * - Zod transform methods for data normalization
 *
 * CHECKPOINT: L0-input-validation
 *
 * DATA FLOW:
 * [Raw User Input] → [Validation Schema] → [Sanitized Input] → [API Handler]
 *
 * LEARN MORE:
 * - docs/ARCHITECTURE.md (Security Considerations)
 * - https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
 */

import { z } from 'zod';

/**
 * User Query Input Schema
 *
 * WHY VALIDATE USER INPUT:
 * ------------------------
 * 1. Security: Prevent injection attacks (though LLMs handle this naturally)
 * 2. UX: Provide immediate feedback on invalid input
 * 3. Cost: Don't waste tokens on empty/malformed requests
 * 4. Debugging: Easier to trace issues with structured data
 */
export const UserQuerySchema = z.object({
  /**
   * The actual question/message from the user
   *
   * VALIDATION RULES:
   * - Trim whitespace (transform)
   * - Minimum 1 character (no empty queries)
   * - Maximum 1000 characters (prevent abuse)
   */
  message: z.string()
    .min(1, 'Message cannot be empty')
    .max(1000, 'Message too long (max 1000 characters)')
    .transform(str => str.trim())
    .describe('The user\'s support query'),

  /**
   * Optional conversation ID for multi-turn chats
   *
   * LAYER 0: Not used (stateless)
   * LAYER 2+: Used for conversation context
   */
  conversation_id: z.string()
    .optional()
    .describe('Optional conversation thread ID'),

  /**
   * Optional metadata about the request
   *
   * EXAMPLE USES:
   * - User timezone (for time-sensitive queries)
   * - User plan (for feature-specific answers)
   * - Request source (web, mobile, api)
   */
  metadata: z.object({
    user_timezone: z.string().optional(),
    user_plan: z.enum(['free', 'pro', 'enterprise']).optional(),
    source: z.enum(['web', 'mobile', 'api']).optional(),
  }).optional(),
});

export type UserQuery = z.infer<typeof UserQuerySchema>;

/**
 * Chat API Request Schema
 *
 * This is what the POST /api/chat endpoint expects
 */
export const ChatRequestSchema = z.object({
  /**
   * The message from the user
   *
   * DESIGN NOTE: We keep this simple in Layer 0.
   * In later layers, this becomes a messages array
   * for multi-turn conversations.
   */
  message: z.string()
    .min(1, 'Message is required')
    .max(1000, 'Message exceeds maximum length')
    .transform(str => str.trim()),

  /**
   * Optional debug flag
   *
   * When true, includes extra metadata in response:
   * - Raw schema
   * - Validation errors (if any)
   * - Token usage
   * - Processing time breakdown
   */
  debug: z.boolean()
    .optional()
    .default(false)
    .describe('Enable debug mode for detailed response'),
});

export type ChatRequest = z.infer<typeof ChatRequestSchema>;

/**
 * Chat API Response Schema
 *
 * WHY VALIDATE RESPONSES:
 * -----------------------
 * Even though we control the response format,
 * validating it ensures:
 * 1. We never send malformed data to clients
 * 2. Schema changes are caught early
 * 3. API contracts are self-documenting
 */
export const ChatResponseSchema = z.object({
  /**
   * Success flag
   */
  success: z.boolean(),

  /**
   * The structured answer (if successful)
   *
   * NOTE: We import SupportAnswerSchema in the implementation,
   * not here, to avoid circular dependencies.
   */
  data: z.unknown().optional(),

  /**
   * Error details (if failed)
   */
  error: z.object({
    code: z.string(),
    message: z.string(),
    details: z.unknown().optional(),
  }).optional(),

  /**
   * Request metadata
   */
  metadata: z.object({
    request_id: z.string(),
    timestamp: z.string(),
    processing_time_ms: z.number().optional(),
  }),
});

export type ChatResponse = z.infer<typeof ChatResponseSchema>;

/**
 * VALIDATION HELPERS
 * ==================
 *
 * Common validation utilities used across the app
 */

/**
 * Safely parse and validate input
 *
 * @example
 * const result = safeValidate(UserQuerySchema, untrustedInput);
 * if (result.success) {
 *   // result.data is type-safe
 * } else {
 *   // result.error contains validation errors
 * }
 */
export function safeValidate<T extends z.ZodTypeAny>(
  schema: T,
  data: unknown
): { success: true; data: z.infer<T> } | { success: false; error: z.ZodError } {
  const result = schema.safeParse(data);
  if (result.success) {
    return { success: true, data: result.data };
  }
  return { success: false, error: result.error };
}

/**
 * Format Zod validation errors for user-friendly display
 *
 * TRANSFORMS:
 * { issues: [{ path: ['message'], message: 'Required' }] }
 * INTO:
 * "message: Required"
 */
export function formatValidationError(error: z.ZodError): string {
  return error.issues
    .map(issue => `${issue.path.join('.')}: ${issue.message}`)
    .join(', ');
}
