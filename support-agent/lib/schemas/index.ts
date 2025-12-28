/**
 * FILE: index.ts
 * LAYER: 0 (Foundation)
 * PURPOSE: Central export point for all schemas and validation utilities
 *
 * CONCEPTS DEMONSTRATED:
 * - Barrel export pattern
 * - Centralized schema management
 * - Clean import paths
 *
 * CHECKPOINT: L0-schema-exports
 *
 * DATA FLOW:
 * [This module] → [Consumers import from @/lib/schemas]
 *
 * USAGE:
 * import { SupportAnswerSchema, UserQuerySchema } from '@/lib/schemas';
 */

// Core output schema
export {
  SupportAnswerSchema,
  SUPPORT_CATEGORIES,
  type SupportAnswer,
  type SupportCategory,
} from './support-answer';

// Input validation schemas
export {
  UserQuerySchema,
  ChatRequestSchema,
  ChatResponseSchema,
  type UserQuery,
  type ChatRequest,
  type ChatResponse,
  safeValidate,
  formatValidationError,
} from './validation';
