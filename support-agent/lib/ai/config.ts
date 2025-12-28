/**
 * FILE: config.ts
 * LAYER: 0 (Foundation)
 * PURPOSE: AI model configuration and provider setup
 *
 * CONCEPTS DEMONSTRATED:
 * - Multi-provider AI configuration
 * - Environment-based model selection
 * - Type-safe model settings
 * - Graceful fallbacks
 *
 * CHECKPOINT: L0-ai-config
 *
 * DATA FLOW:
 * [Environment Variables] → [getModel()] → [Configured AI Client]
 *
 * LEARN MORE:
 * - https://sdk.vercel.ai/docs/ai-sdk-core/providers
 */

import { anthropic } from '@ai-sdk/anthropic';
import { openai } from '@ai-sdk/openai';

/**
 * Supported AI providers
 */
export type AIProvider = 'anthropic' | 'openai';

/**
 * Model configurations for each provider
 *
 * WHY THESE MODELS:
 * -----------------
 * - Claude 3.5 Sonnet: Best for complex reasoning, excellent structured output
 * - GPT-4 Turbo: Alternative option, good for general tasks
 */
export const MODEL_CONFIGS = {
  anthropic: {
    model: 'claude-3-5-sonnet-20241022',
    displayName: 'Claude 3.5 Sonnet',
    maxTokens: 4096,
    temperature: 0.7,
  },
  openai: {
    model: 'gpt-4-turbo-preview',
    displayName: 'GPT-4 Turbo',
    maxTokens: 4096,
    temperature: 0.7,
  },
} as const;

/**
 * Get the configured AI model
 *
 * CONFIGURATION PRECEDENCE:
 * 1. AI_MODEL environment variable (specific model ID)
 * 2. Provider-based selection (ANTHROPIC_API_KEY or OPENAI_API_KEY)
 * 3. Default to Claude 3.5 Sonnet
 *
 * @throws Error if no API key is configured
 */
export function getModel() {
  // Check for provider API keys
  const hasAnthropic = !!process.env.ANTHROPIC_API_KEY;
  const hasOpenAI = !!process.env.OPENAI_API_KEY;

  if (!hasAnthropic && !hasOpenAI) {
    throw new Error(
      'No AI provider configured. Set ANTHROPIC_API_KEY or OPENAI_API_KEY in .env'
    );
  }

  // Allow explicit model selection via environment variable
  const explicitModel = process.env.AI_MODEL;

  // Determine provider
  let provider: AIProvider;
  if (explicitModel?.startsWith('claude')) {
    provider = 'anthropic';
  } else if (explicitModel?.startsWith('gpt')) {
    provider = 'openai';
  } else {
    // Default to Anthropic if available, otherwise OpenAI
    provider = hasAnthropic ? 'anthropic' : 'openai';
  }

  // Get provider config
  const config = MODEL_CONFIGS[provider];

  // Return configured model
  if (provider === 'anthropic') {
    return {
      model: anthropic(explicitModel || config.model),
      config,
      provider,
    };
  } else {
    return {
      model: openai(explicitModel || config.model),
      config,
      provider,
    };
  }
}

/**
 * Generation settings for structured outputs
 *
 * THESE SETTINGS ARE CRITICAL:
 * ----------------------------
 * - temperature: Lower = more deterministic, Higher = more creative
 * - maxTokens: Limits response length (cost control)
 * - topP: Nucleus sampling for diversity
 *
 * Layer 0 uses conservative settings for reliability.
 */
export const GENERATION_SETTINGS = {
  /**
   * Temperature: 0.7 balances consistency with natural language
   *
   * EXPERIMENT: Try 0.3 for more factual responses,
   * or 0.9 for more creative/varied responses
   */
  temperature: 0.7,

  /**
   * Max tokens: Generous limit for detailed answers
   *
   * NOTE: This is OUTPUT tokens. Input tokens are separate.
   */
  maxTokens: 2048,

  /**
   * Top P: Nucleus sampling
   *
   * 1.0 = consider all tokens
   * 0.9 = consider top 90% probability mass
   */
  topP: 1.0,
} as const;

/**
 * Get model display name for UI
 */
export function getModelDisplayName(): string {
  const { provider } = getModel();
  return MODEL_CONFIGS[provider].displayName;
}

/**
 * Get current model ID
 */
export function getModelId(): string {
  const explicitModel = process.env.AI_MODEL;
  if (explicitModel) {
    return explicitModel;
  }

  const { provider } = getModel();
  return MODEL_CONFIGS[provider].model;
}
