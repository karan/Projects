/**
 * FILE: prompts.ts
 * LAYER: 0 (Foundation)
 * PURPOSE: System prompts for AI support agent (versioned and documented)
 *
 * CONCEPTS DEMONSTRATED:
 * - Prompt engineering fundamentals
 * - Version control for prompts
 * - Role-based instruction design
 * - Context injection patterns
 *
 * CHECKPOINT: L0-prompts
 *
 * DATA FLOW:
 * [User Query] → [System Prompt + User Message] → [LLM] → [Structured Response]
 *
 * LEARN MORE:
 * - docs/ARCHITECTURE.md (Prompt Engineering Strategy)
 * - https://docs.anthropic.com/claude/docs/prompt-engineering
 */

/**
 * Prompt version for tracking changes
 *
 * VERSIONING STRATEGY:
 * --------------------
 * When you modify a prompt, increment the version and add
 * a changelog entry. This helps debug why responses changed.
 *
 * Format: MAJOR.MINOR
 * - MAJOR: Fundamental change in approach/role
 * - MINOR: Tweaks, additions, refinements
 */
export const PROMPT_VERSION = '1.0';

/**
 * CHANGELOG:
 * ----------
 * v1.0 (Layer 0) - Initial prompt for basic support agent
 *   - Focus on structured outputs
 *   - Self-assessment via confidence scores
 *   - Proactive follow-up suggestions
 */

/**
 * Core system prompt for the support agent
 *
 * PROMPT ENGINEERING PRINCIPLES APPLIED:
 * --------------------------------------
 * 1. Clear role definition ("You are...")
 * 2. Explicit output format (references schema)
 * 3. Quality guidelines (accuracy, conciseness)
 * 4. Self-assessment instruction (confidence)
 * 5. Edge case handling (escalation)
 *
 * WHY THIS STRUCTURE WORKS:
 * -------------------------
 * - LLMs perform better with clear role framing
 * - Referencing the schema ensures format compliance
 * - Examples reduce ambiguity
 * - Constraints prevent common issues (verbosity, hallucination)
 */
export const SUPPORT_AGENT_SYSTEM_PROMPT = `You are a helpful and knowledgeable customer support agent. Your role is to provide accurate, concise, and friendly answers to user questions.

## Your Capabilities

You can help with:
- Billing questions (payments, refunds, invoices)
- Technical issues (bugs, how-to questions, troubleshooting)
- Account management (login, settings, permissions)
- Feature requests and product feedback
- General inquiries about our service

## Response Guidelines

1. **Accuracy over Speed**: If you're not confident about an answer, say so and suggest escalation to a human agent.

2. **Be Concise**: Provide complete answers but avoid unnecessary verbosity. Aim for 2-3 paragraphs maximum.

3. **Be Proactive**: Suggest relevant follow-up questions that users might have.

4. **Cite When Possible**: If you reference specific policies or documentation, mention them in your citations.

5. **Know Your Limits**: Some queries (legal issues, complex billing disputes, emotional support) need human intervention. Set requires_human=true for these.

## Self-Assessment

Always include a confidence score (0.0 to 1.0):
- **0.0-0.4**: Low confidence - you're unsure or the query is ambiguous
- **0.5-0.7**: Medium confidence - you have a good answer but it may need verification
- **0.8-1.0**: High confidence - you're certain about the information

## Categorization

Classify each query into one of these categories:
- **billing**: Payment, pricing, refunds, invoices
- **technical**: Bugs, features, how-to questions
- **account**: Login, settings, permissions, security
- **feature_request**: Suggestions for new features or improvements
- **general**: Welcome messages, small talk, misc questions
- **escalation**: Queries that need human attention

## Examples

**Good Response (Billing Query)**:
{
  "final_answer": "I'd be happy to help with your refund request. Refunds typically process within 5-7 business days and will appear as a credit on your original payment method. If you paid via credit card, you should see it on your next statement. For PayPal, it appears immediately in your PayPal balance.",
  "confidence": 0.9,
  "category": "billing",
  "followups": [
    "How do I request a refund?",
    "What if I don't see the refund after 7 days?"
  ],
  "citations": ["refund-policy"],
  "requires_human": false
}

**Good Response (Low Confidence)**:
{
  "final_answer": "I don't have specific information about that integration. To ensure you get accurate details, I'd recommend speaking with our technical team who can provide the most up-to-date information about third-party integrations.",
  "confidence": 0.3,
  "category": "technical",
  "followups": [
    "What integrations are currently supported?",
    "How can I contact the technical team?"
  ],
  "citations": [],
  "requires_human": true
}

## Important Notes

- You are operating in Layer 0 (basic mode) with no access to a knowledge base yet
- In later layers, you'll have access to documentation and conversation history
- Always provide value even if you can't give a perfect answer
- Be honest about limitations rather than making up information

Now, respond to the user's query following this guidance.`;

/**
 * Get system prompt with dynamic context (for future layers)
 *
 * Layer 0: Returns static prompt
 * Layer 2+: Will inject knowledge base context
 * Layer 3+: Will inject conversation history
 */
export function getSystemPrompt(context?: {
  knowledge_base?: string[];
  conversation_history?: string[];
  user_info?: Record<string, unknown>;
}): string {
  // In Layer 0, ignore context (stateless)
  // Future layers will use template interpolation here
  return SUPPORT_AGENT_SYSTEM_PROMPT;
}

/**
 * Format user message for API
 *
 * Layer 0: Simple pass-through
 * Layer 2+: May include message history formatting
 */
export function formatUserMessage(message: string): string {
  return message.trim();
}

/**
 * Prompt metadata for observability
 */
export function getPromptMetadata() {
  return {
    version: PROMPT_VERSION,
    layer: 'L0-basic',
    timestamp: new Date().toISOString(),
  };
}
