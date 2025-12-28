/**
 * FILE: route.ts
 * LAYER: 0 (Foundation)
 * PURPOSE: API endpoint for chat interactions with AI support agent
 *
 * CONCEPTS DEMONSTRATED:
 * - Next.js App Router API routes
 * - Request validation with Zod
 * - Error handling middleware pattern
 * - Structured API responses
 *
 * CHECKPOINT: L0-api-route
 *
 * DATA FLOW:
 * [POST /api/chat] → [Validate] → [Generate AI Response] → [Return Structured Data]
 *
 * LEARN MORE:
 * - https://nextjs.org/docs/app/building-your-application/routing/route-handlers
 */

import { NextRequest } from 'next/server';
import { ChatRequestSchema } from '@/lib/schemas';
import { generateSupportResponse } from '@/lib/ai/client';
import { handleAPIError } from '@/lib/utils/error-handling';
import { logger } from '@/lib/utils/logging';
import { nanoid } from 'nanoid';

/**
 * POST /api/chat
 *
 * Main endpoint for chat interactions
 *
 * REQUEST BODY:
 * {
 *   "message": "user question here",
 *   "debug": false // optional
 * }
 *
 * RESPONSE (Success):
 * {
 *   "success": true,
 *   "data": { ...SupportAnswer },
 *   "metadata": { request_id, timestamp, processing_time_ms }
 * }
 *
 * RESPONSE (Error):
 * {
 *   "error": {
 *     "code": "ERROR_CODE",
 *     "message": "User-friendly message",
 *     "details": {...}, // only in development
 *     "timestamp": "ISO-8601",
 *     "request_id": "unique-id"
 *   }
 * }
 */
export async function POST(request: NextRequest) {
  const requestId = nanoid(12);
  const startTime = performance.now();

  logger.info('Chat request received', { request_id: requestId });

  try {
    // Parse request body
    const body = await request.json();

    // Validate request against schema
    const validation = ChatRequestSchema.safeParse(body);

    if (!validation.success) {
      logger.warn('Invalid request body', {
        request_id: requestId,
        errors: validation.error.issues,
      });

      return Response.json(
        {
          error: {
            code: 'VALIDATION_ERROR',
            message: 'Invalid request format',
            details: process.env.NODE_ENV === 'development'
              ? validation.error.issues
              : undefined,
            timestamp: new Date().toISOString(),
            request_id: requestId,
          },
        },
        { status: 400 }
      );
    }

    const { message, debug } = validation.data;

    logger.debug('Request validated', {
      request_id: requestId,
      message_length: message.length,
      debug,
    });

    // Generate AI response
    const supportAnswer = await generateSupportResponse(message);

    // Calculate total processing time
    const processingTime = Math.round(performance.now() - startTime);

    // Build response
    const response = {
      success: true,
      data: supportAnswer,
      metadata: {
        request_id: requestId,
        timestamp: new Date().toISOString(),
        processing_time_ms: processingTime,
      },
      // Include debug info if requested
      ...(debug && {
        debug: {
          schema_version: '1.0',
          model: supportAnswer.metadata?.model_used,
          prompt_version: supportAnswer.metadata?.prompt_version,
        },
      }),
    };

    logger.info('Chat request completed', {
      request_id: requestId,
      processing_time_ms: processingTime,
      confidence: supportAnswer.confidence,
      category: supportAnswer.category,
    });

    return Response.json(response);
  } catch (error) {
    logger.error('Chat request failed', {
      request_id: requestId,
      error: error instanceof Error ? error.message : String(error),
    });

    return handleAPIError(error);
  }
}

/**
 * OPTIONS /api/chat
 *
 * CORS preflight handler
 */
export async function OPTIONS() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}

/**
 * LEARNING NOTES:
 * ===============
 *
 * This API route demonstrates the complete request/response cycle:
 *
 * 1. REQUEST VALIDATION
 *    - Parse JSON body
 *    - Validate against ChatRequestSchema
 *    - Return 400 if invalid
 *
 * 2. BUSINESS LOGIC
 *    - Call generateSupportResponse()
 *    - This returns a validated SupportAnswer
 *
 * 3. RESPONSE FORMATTING
 *    - Wrap in standard envelope
 *    - Add metadata (request_id, timestamp, etc.)
 *    - Include debug info if requested
 *
 * 4. ERROR HANDLING
 *    - Catch any errors
 *    - Use handleAPIError() for consistent format
 *    - Log everything for debugging
 *
 * The result is a robust, production-ready API endpoint
 * with proper validation, error handling, and observability.
 */
