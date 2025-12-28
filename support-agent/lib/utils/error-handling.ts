/**
 * FILE: error-handling.ts
 * LAYER: 0 (Foundation)
 * PURPOSE: Standardized error handling and response formatting
 *
 * CONCEPTS DEMONSTRATED:
 * - Error type discrimination
 * - Consistent error responses
 * - Request ID generation for traceability
 * - Safe error serialization
 *
 * CHECKPOINT: L0-error-handling
 *
 * DATA FLOW:
 * [Error Occurs] → [createErrorResponse()] → [Standardized APIError] → [Client]
 *
 * LEARN MORE:
 * - docs/ARCHITECTURE.md (Error Handling Strategy)
 */

import { z } from 'zod';
import { nanoid } from 'nanoid';
import type { ErrorCode, APIError } from '@/lib/types';

/**
 * Error Response Schema
 *
 * This ensures all API errors follow a consistent structure
 */
export const ErrorResponseSchema = z.object({
  error: z.object({
    code: z.string(),           // Machine-readable error code
    message: z.string(),        // User-friendly message
    details: z.unknown().optional(), // Technical details for debugging
    timestamp: z.string(),      // ISO 8601 timestamp
    request_id: z.string(),     // Unique identifier for tracing
  }),
});

export type ErrorResponse = z.infer<typeof ErrorResponseSchema>;

/**
 * Create a standardized error response
 *
 * WHY STANDARDIZE:
 * ----------------
 * 1. Consistent client error handling
 * 2. Easier logging and monitoring
 * 3. Better debugging with request IDs
 * 4. Prevents leaking sensitive info
 *
 * @param code - Machine-readable error code
 * @param message - User-friendly error message
 * @param details - Optional technical details (only in dev mode)
 * @returns Standardized error object
 *
 * @example
 * const error = createErrorResponse(
 *   'VALIDATION_ERROR',
 *   'Invalid input provided',
 *   { field: 'message', reason: 'too short' }
 * );
 */
export function createErrorResponse(
  code: ErrorCode,
  message: string,
  details?: unknown
): APIError {
  const isDevelopment = process.env.NODE_ENV === 'development';

  return {
    code,
    message,
    // Only include details in development to avoid leaking info
    details: isDevelopment ? details : undefined,
    timestamp: new Date().toISOString(),
    request_id: nanoid(12), // Short, URL-safe unique ID
  };
}

/**
 * Map different error types to appropriate error codes
 *
 * DESIGN PATTERN: Type discrimination allows us to
 * handle different error sources appropriately.
 */
export function mapErrorToCode(error: unknown): ErrorCode {
  // Zod validation errors
  if (error instanceof z.ZodError) {
    return 'VALIDATION_ERROR';
  }

  // AI SDK errors (check error message patterns)
  if (error instanceof Error) {
    const message = error.message.toLowerCase();

    if (message.includes('rate limit') || message.includes('429')) {
      return 'RATE_LIMIT';
    }

    if (
      message.includes('api key') ||
      message.includes('authentication') ||
      message.includes('401')
    ) {
      return 'AI_ERROR';
    }

    if (
      message.includes('timeout') ||
      message.includes('network') ||
      message.includes('fetch')
    ) {
      return 'AI_ERROR';
    }
  }

  return 'INTERNAL_ERROR';
}

/**
 * Extract user-friendly message from error
 *
 * SECURITY NOTE: Never expose raw error messages to users
 * as they might contain sensitive system information.
 */
export function getErrorMessage(error: unknown): string {
  if (error instanceof z.ZodError) {
    // Format Zod errors nicely
    return error.issues
      .map(issue => issue.message)
      .join(', ');
  }

  if (error instanceof Error) {
    const message = error.message;

    // Map common errors to user-friendly messages
    if (message.includes('rate limit')) {
      return 'Too many requests. Please try again in a moment.';
    }

    if (message.includes('api key') || message.includes('authentication')) {
      return 'AI service configuration error. Please contact support.';
    }

    if (message.includes('timeout')) {
      return 'Request timed out. Please try again.';
    }

    // Generic fallback
    return 'An error occurred while processing your request.';
  }

  return 'An unexpected error occurred.';
}

/**
 * Handle errors in API routes
 *
 * This is the main error handling function used in /api/chat
 *
 * @example
 * try {
 *   // API logic
 * } catch (error) {
 *   return handleAPIError(error);
 * }
 */
export function handleAPIError(error: unknown): Response {
  const code = mapErrorToCode(error);
  const message = getErrorMessage(error);
  const details = error instanceof Error ? {
    name: error.name,
    message: error.message,
    stack: process.env.NODE_ENV === 'development' ? error.stack : undefined,
  } : error;

  const errorResponse = createErrorResponse(code, message, details);

  // Map error codes to HTTP status codes
  const statusCode = getHTTPStatusCode(code);

  return Response.json(
    { error: errorResponse },
    { status: statusCode }
  );
}

/**
 * Map error codes to HTTP status codes
 */
function getHTTPStatusCode(code: ErrorCode): number {
  switch (code) {
    case 'VALIDATION_ERROR':
      return 400; // Bad Request
    case 'RATE_LIMIT':
      return 429; // Too Many Requests
    case 'AI_ERROR':
      return 502; // Bad Gateway (upstream service error)
    case 'INTERNAL_ERROR':
    case 'UNKNOWN_ERROR':
    default:
      return 500; // Internal Server Error
  }
}

/**
 * Type guard to check if response is an error
 */
export function isErrorResponse(
  response: unknown
): response is ErrorResponse {
  const result = ErrorResponseSchema.safeParse(response);
  return result.success;
}
