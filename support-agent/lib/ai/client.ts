/**
 * FILE: client.ts
 * LAYER: 0 (Foundation)
 * PURPOSE: AI SDK client wrapper for generating structured support responses
 *
 * CONCEPTS DEMONSTRATED:
 * - Vercel AI SDK generateObject() usage
 * - Schema-driven LLM outputs
 * - Error handling for AI calls
 * - Performance measurement
 *
 * CHECKPOINT: L0-ai-client
 *
 * DATA FLOW:
 * [User Query] → [generateSupportResponse()] → [AI SDK] → [Validated SupportAnswer]
 *
 * LEARN MORE:
 * - https://sdk.vercel.ai/docs/ai-sdk-core/generating-structured-data
 */

import { generateObject } from 'ai';
import { SupportAnswerSchema, type SupportAnswer } from '@/lib/schemas';
import { getModel, GENERATION_SETTINGS, getModelId } from './config';
import { getSystemPrompt, formatUserMessage, getPromptMetadata } from './prompts';
import { logger } from '@/lib/utils/logging';

/**
 * Generate a structured support response
 *
 * This is the CORE FUNCTION of Layer 0. Everything else exists
 * to support this operation.
 *
 * HOW IT WORKS:
 * -------------
 * 1. Takes a user query string
 * 2. Combines it with system prompt
 * 3. Calls LLM with schema constraint
 * 4. Validates response against SupportAnswerSchema
 * 5. Returns type-safe SupportAnswer object
 *
 * THE MAGIC: generateObject() ensures the LLM's output
 * conforms to our Zod schema. If it doesn't, the SDK
 * will retry or throw an error.
 *
 * @param userQuery - The user's question/message
 * @returns Promise resolving to validated SupportAnswer
 * @throws Error if generation fails or response invalid
 *
 * @example
 * const answer = await generateSupportResponse(
 *   "How do I request a refund?"
 * );
 * console.log(answer.final_answer); // Type-safe access
 * console.log(answer.confidence);   // TypeScript knows this exists
 */
export async function generateSupportResponse(
  userQuery: string
): Promise<SupportAnswer> {
  // Start performance timer
  const startTime = performance.now();

  logger.info('Generating support response', {
    query_length: userQuery.length,
    model: getModelId(),
  });

  try {
    // Get configured model
    const { model, config } = getModel();

    // Format inputs
    const systemPrompt = getSystemPrompt();
    const userMessage = formatUserMessage(userQuery);

    // Generate structured output
    // This is where the magic happens! 🪄
    const result = await generateObject({
      model,
      schema: SupportAnswerSchema,
      system: systemPrompt,
      prompt: userMessage,
      temperature: GENERATION_SETTINGS.temperature,
      maxTokens: GENERATION_SETTINGS.maxTokens,
    });

    // Calculate processing time
    const processingTime = Math.round(performance.now() - startTime);

    logger.info('Support response generated successfully', {
      processing_time_ms: processingTime,
      confidence: result.object.confidence,
      category: result.object.category,
      requires_human: result.object.requires_human,
    });

    // Enrich response with metadata
    const enrichedResponse: SupportAnswer = {
      ...result.object,
      metadata: {
        ...result.object.metadata,
        processing_time_ms: processingTime,
        model_used: getModelId(),
        layer: 'L0-basic',
        prompt_version: getPromptMetadata().version,
      },
    };

    return enrichedResponse;
  } catch (error) {
    const processingTime = Math.round(performance.now() - startTime);

    logger.error('Failed to generate support response', {
      error: error instanceof Error ? error.message : String(error),
      processing_time_ms: processingTime,
    });

    // Re-throw with context
    throw new Error(
      `AI generation failed: ${error instanceof Error ? error.message : 'Unknown error'}`
    );
  }
}

/**
 * LEARNING CHECKPOINT:
 * ====================
 *
 * This file demonstrates the core pattern for structured AI outputs:
 *
 * 1. Define schema (SupportAnswerSchema)
 * 2. Create prompt (SUPPORT_AGENT_SYSTEM_PROMPT)
 * 3. Call generateObject() with both
 * 4. Get type-safe, validated response
 *
 * Without structured outputs, you'd need to:
 * - Parse markdown/JSON from free text
 * - Handle malformed responses
 * - Write custom validation logic
 * - Deal with inconsistent formats
 *
 * The schema solves ALL of these problems.
 *
 * EXPERIMENT IDEAS:
 * -----------------
 * 1. Add console.log(result) before return to see raw AI SDK output
 * 2. Temporarily break the schema and observe validation errors
 * 3. Change temperature and observe response variety
 * 4. Add a new field to schema and see it auto-populate
 */
