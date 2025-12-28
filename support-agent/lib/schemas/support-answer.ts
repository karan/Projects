/**
 * FILE: support-answer.ts
 * LAYER: 0 (Foundation)
 * PURPOSE: Define the core structured output schema for AI-generated support responses
 *
 * CONCEPTS DEMONSTRATED:
 * - Zod schema definition for runtime validation
 * - Type inference from schemas (no manual TypeScript types)
 * - Structured outputs as contracts between app and LLM
 * - Self-documenting code through inline JSDoc
 * - Enum constraints for categorical data
 *
 * CHECKPOINT: L0-core-schema
 *
 * DATA FLOW:
 * [LLM Raw Output] → [Zod Validation] → [Type-safe SupportAnswer Object] → [React UI]
 *
 * LEARN MORE:
 * - docs/ARCHITECTURE.md (Schema Design Principles)
 * - https://zod.dev (Zod documentation)
 * - https://sdk.vercel.ai/docs/ai-sdk-core/generating-structured-data
 */

import { z } from 'zod';

/**
 * SupportAnswer Schema - The Core Contract
 * =========================================
 *
 * WHY THIS EXISTS:
 * ----------------
 * LLMs naturally produce unstructured text. Without constraints,
 * responses vary wildly in format, making them hard to:
 * - Display consistently in UI
 * - Validate for quality
 * - Process programmatically
 * - Debug when things go wrong
 *
 * Structured outputs solve this by forcing the LLM to conform
 * to a predefined shape. Think of it as a "contract" between
 * your application and the model.
 *
 * HOW IT REDUCES HALLUCINATION:
 * -----------------------------
 * 1. Confidence field forces the model to self-assess
 * 2. Citations field requires source attribution
 * 3. Category enum limits response scope
 * 4. Followups encourage actionable responses
 *
 * SCHEMA FIELDS EXPLAINED:
 * ------------------------
 */

/**
 * Define allowed categories as a const for reuse
 *
 * DESIGN PATTERN: Using 'as const' creates a readonly tuple,
 * which Zod can use for enum validation while also being
 * usable in TypeScript for type narrowing.
 */
export const SUPPORT_CATEGORIES = [
  'billing',           // Payment, invoices, refunds
  'technical',         // Product bugs, how-to questions
  'account',           // Login, settings, permissions
  'feature_request',   // Enhancement suggestions
  'general',           // Catch-all for misc queries
  'escalation'         // Needs human intervention
] as const;

/**
 * Type for category - useful for type guards and UI logic
 */
export type SupportCategory = typeof SUPPORT_CATEGORIES[number];

/**
 * Main schema definition
 *
 * LEARNING NOTE: Each field demonstrates a different Zod feature:
 * - .min() / .max() = validation constraints
 * - .describe() = schema introspection (used in debug views)
 * - .default() = fallback values
 * - .optional() = nullable fields
 */
export const SupportAnswerSchema = z.object({
  /**
   * final_answer: The actual response to show the user
   *
   * DESIGN DECISION: We use a single string rather than
   * structured sections because:
   * 1. Natural language is more flexible
   * 2. Easier to render in chat UI
   * 3. Model can structure internally as needed
   *
   * VALIDATION RATIONALE:
   * - min(10): Prevents lazy/incomplete responses
   * - max(2000): Keeps responses concise and scannable
   */
  final_answer: z.string()
    .min(10, 'Answer too short - likely incomplete')
    .max(2000, 'Answer too long - consider breaking up')
    .describe('The complete answer to the user query'),

  /**
   * confidence: Model's self-assessment (0.0 to 1.0)
   *
   * WHY THIS MATTERS:
   * - Low confidence (< 0.5) → suggest escalation
   * - Medium (0.5-0.8) → provide answer but offer human help
   * - High (> 0.8) → confident response
   *
   * This creates a feedback loop for quality control.
   *
   * IMPLEMENTATION NOTE: In Layer 1+, you can use this
   * to trigger different UI states or routing logic.
   */
  confidence: z.number()
    .min(0)
    .max(1)
    .describe('Confidence score from 0.0 (no confidence) to 1.0 (certain)'),

  /**
   * category: Classification of the query type
   *
   * Using an enum (not free text) because:
   * 1. Enables routing logic (technical → dev team)
   * 2. Powers analytics dashboards
   * 3. Prevents category drift over time
   *
   * EXPERIMENT: Try adding a new category and observe
   * how the model naturally starts using it.
   */
  category: z.enum(SUPPORT_CATEGORIES)
    .describe('The primary category this query falls into'),

  /**
   * followups: Suggested next questions
   *
   * PROACTIVE SUPPORT PATTERN:
   * Instead of waiting for users to struggle,
   * suggest logical next steps. This:
   * - Reduces follow-up tickets
   * - Improves user satisfaction
   * - Demonstrates product knowledge
   *
   * MAX 3 RATIONALE: More choices = decision paralysis
   */
  followups: z.array(z.string())
    .max(3, 'Too many followups overwhelms users')
    .describe('Up to 3 suggested follow-up questions'),

  /**
   * citations: Source references
   *
   * TRUST BUILDING:
   * When answers cite sources, users can verify.
   * Empty array is valid (for general knowledge),
   * but RAG responses should always cite.
   *
   * LAYER EVOLUTION: In L2+, these become document IDs
   * that link to actual knowledge base entries.
   */
  citations: z.array(z.string())
    .describe('Source documents or URLs referenced'),

  /**
   * requires_human: Escalation flag
   *
   * SAFETY NET:
   * Some queries need human judgment:
   * - Legal matters
   * - Complex billing disputes
   * - Emotional support needs
   *
   * DEFAULT FALSE: Optimistic automation, but
   * the model can self-escalate when needed.
   */
  requires_human: z.boolean()
    .default(false)
    .describe('Whether this query needs human escalation'),

  /**
   * metadata: Debugging information
   *
   * OBSERVABILITY:
   * In production, you need to trace what happened.
   * This object can be extended per layer.
   *
   * OPTIONAL PATTERN: Using .optional() on the whole
   * object makes all fields truly optional (not required
   * even when the object is present).
   */
  metadata: z.object({
    processing_time_ms: z.number().optional(),
    model_used: z.string().optional(),
    layer: z.string().default('L0-basic'),
    prompt_version: z.string().optional(),
  }).optional(),
});

/**
 * Type inference - no manual type definition needed!
 *
 * MAGIC OF ZOD: This single line gives you full TypeScript
 * type safety based on the schema. Change the schema,
 * and the type updates automatically.
 */
export type SupportAnswer = z.infer<typeof SupportAnswerSchema>;

/**
 * EXAMPLE VALID OBJECT:
 *
 * const validAnswer: SupportAnswer = {
 *   final_answer: "Your refund has been processed...",
 *   confidence: 0.92,
 *   category: "billing",
 *   followups: [
 *     "When will I see the refund in my account?",
 *     "Can I get a receipt for this refund?"
 *   ],
 *   citations: ["refund-policy.pdf"],
 *   requires_human: false,
 *   metadata: {
 *     processing_time_ms: 1250,
 *     model_used: "claude-3-5-sonnet-20241022",
 *     layer: "L0-basic"
 *   }
 * };
 *
 * INVALID EXAMPLES (would fail validation):
 *
 * { final_answer: "OK" } // too short (< 10 chars)
 * { confidence: 1.5 } // out of range (> 1.0)
 * { category: "random" } // not in enum
 * { followups: ["q1", "q2", "q3", "q4"] } // too many (> 3)
 */
