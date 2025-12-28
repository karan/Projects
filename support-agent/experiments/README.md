# Layer 0 Experiments

> **Purpose**: 12 progressive hands-on experiments to master Layer 0 concepts

## How to Use This Guide

1. **Complete in order**: Each experiment builds on previous ones
2. **Read objective first**: Understand what you'll learn
3. **Try before checking solution**: Struggle = learning
4. **Reflect after completion**: Answer "What you learned" prompts
5. **Undo changes**: Return to baseline before next experiment

---

## Experiment 1: Add a Sentiment Field

**Difficulty**: ⭐ Easy
**Time**: 10 minutes
**Concept**: Schema modification and LLM adaptation

### Objective

Add a `sentiment` field to detect user emotion (positive, neutral, negative). Observe how the LLM automatically populates new schema fields without prompt changes.

### Files to Modify

1. `lib/schemas/support-answer.ts`

### Step-by-Step Instructions

**Step 1**: Add the field to the schema

```typescript
// In lib/schemas/support-answer.ts, add after category field:

sentiment: z.enum(['positive', 'neutral', 'negative'])
  .describe('Detected sentiment of the user query'),
```

**Step 2**: Test the application

```bash
npm run dev
```

**Step 3**: Ask various questions:
- "This is amazing! How do I upgrade?" (positive)
- "How do I cancel my subscription?" (neutral/negative)
- "I'm frustrated with the billing errors" (negative)

**Step 4**: Check the response in browser DevTools

### Expected Outcome

The LLM automatically populates the `sentiment` field! You'll see:

```json
{
  "sentiment": "negative",
  "final_answer": "I understand your frustration...",
  ...
}
```

### Solution

<details>
<summary>Click to reveal full solution</summary>

```typescript
// lib/schemas/support-answer.ts

export const SupportAnswerSchema = z.object({
  final_answer: z.string()
    .min(10, 'Answer too short - likely incomplete')
    .max(2000, 'Answer too long - consider breaking up')
    .describe('The complete answer to the user query'),

  confidence: z.number()
    .min(0)
    .max(1)
    .describe('Confidence score from 0.0 (no confidence) to 1.0 (certain)'),

  category: z.enum(SUPPORT_CATEGORIES)
    .describe('The primary category this query falls into'),

  // NEW FIELD
  sentiment: z.enum(['positive', 'neutral', 'negative'])
    .describe('Detected sentiment of the user query'),

  followups: z.array(z.string())
    .max(3, 'Too many followups overwhelms users')
    .describe('Up to 3 suggested follow-up questions'),

  citations: z.array(z.string())
    .describe('Source documents or URLs referenced'),

  requires_human: z.boolean()
    .default(false)
    .describe('Whether this query needs human escalation'),

  metadata: z.object({
    processing_time_ms: z.number().optional(),
    model_used: z.string().optional(),
    layer: z.string().default('L0-basic'),
    prompt_version: z.string().optional(),
  }).optional(),
});
```

**Display in UI** (optional):

```typescript
// components/chat/MessageBubble.tsx

{message.structured_data?.sentiment && (
  <span className={`text-xs px-2 py-1 rounded ${
    message.structured_data.sentiment === 'positive' ? 'bg-green-100 text-green-800' :
    message.structured_data.sentiment === 'negative' ? 'bg-red-100 text-red-800' :
    'bg-gray-100 text-gray-800'
  }`}>
    {message.structured_data.sentiment}
  </span>
)}
```

</details>

### What You Learned

**Reflect on these questions**:

1. Did you need to modify the prompt? Why not?
2. How does the LLM know what "sentiment" means?
3. What happens if you make sentiment required but the LLM doesn't return it?
4. Could you add more granular sentiments (angry, happy, confused)?

**Key Insight**: The `.describe()` method guides the LLM. Structured outputs adapt to schema changes automatically.

---

## Experiment 2: Validation Limits Testing

**Difficulty**: ⭐ Easy
**Time**: 5 minutes
**Concept**: Schema constraints and validation errors

### Objective

Understand how Zod constraints work by intentionally breaking them.

### Files to Modify

1. `lib/schemas/support-answer.ts`

### Instructions

**Test 1**: Change `final_answer` max length

```typescript
final_answer: z.string()
  .min(10)
  .max(50) // Changed from 2000
  .describe('The complete answer to the user query'),
```

Ask: "How do I get a refund?"

**Expected**: LLM may violate this constraint, causing error or truncation.

**Test 2**: Invalid confidence range

```typescript
confidence: z.number()
  .min(0)
  .max(0.5) // Changed from 1.0
  .describe('Confidence score'),
```

**Expected**: LLM might fail validation if it returns confidence > 0.5.

**Test 3**: Zero followups allowed

```typescript
followups: z.array(z.string())
  .max(0) // Changed from 3
  .describe('Up to 0 suggested follow-up questions'),
```

**Expected**: Validation errors if LLM suggests followups.

### Solution

The point is to observe errors! Revert changes after experimenting.

### What You Learned

1. What error message appears when validation fails?
2. How does the AI SDK handle validation failures?
3. Which constraints are "hard" (cause errors) vs "soft" (cause retries)?
4. How would you debug a validation error in production?

---

## Experiment 3: Confidence Threshold UI

**Difficulty**: ⭐⭐ Medium
**Time**: 15 minutes
**Concept**: Using structured data for conditional UI

### Objective

Add a warning banner when the AI's confidence is low.

### Files to Modify

1. `components/chat/MessageBubble.tsx`

### Instructions

Add this component after the confidence indicator:

```typescript
{/* Low confidence warning */}
{message.structured_data && message.structured_data.confidence < 0.5 && (
  <div className="mt-2 bg-yellow-50 border border-yellow-200 rounded p-3">
    <div className="flex items-start">
      <svg className="w-5 h-5 text-yellow-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <div>
        <p className="text-sm font-medium text-yellow-800">Low Confidence</p>
        <p className="text-sm text-yellow-700 mt-1">
          This answer may not be accurate. Would you like to speak with a human agent?
        </p>
      </div>
    </div>
  </div>
)}
```

### Expected Outcome

When the AI returns `confidence < 0.5`, a yellow warning appears.

### Solution

See above. Test by asking ambiguous questions like:
- "What's the meaning of life?"
- "Can you help with quantum computing?"

### What You Learned

1. How can structured data drive UI decisions?
2. What confidence threshold would you use in production?
3. How would you track low-confidence responses for improvement?

---

## Experiment 4: New Category Addition

**Difficulty**: ⭐⭐ Medium
**Time**: 20 minutes
**Concept**: Enum modification and UI updates

### Objective

Add a new category and update both backend and frontend.

### Files to Modify

1. `lib/schemas/support-answer.ts`
2. `components/chat/MessageBubble.tsx`

### Instructions

**Step 1**: Add 'security' category

```typescript
// lib/schemas/support-answer.ts

export const SUPPORT_CATEGORIES = [
  'billing',
  'technical',
  'account',
  'feature_request',
  'general',
  'escalation',
  'security', // NEW
] as const;
```

**Step 2**: Add color for security category

```typescript
// components/chat/MessageBubble.tsx

const colors: Record<string, string> = {
  billing: 'bg-blue-100 text-blue-800',
  technical: 'bg-purple-100 text-purple-800',
  account: 'bg-green-100 text-green-800',
  feature_request: 'bg-yellow-100 text-yellow-800',
  general: 'bg-gray-100 text-gray-800',
  escalation: 'bg-red-100 text-red-800',
  security: 'bg-orange-100 text-orange-800', // NEW
};
```

**Step 3**: Test with security questions

- "How do I enable two-factor authentication?"
- "Is my data encrypted?"
- "I think my account was hacked"

### Solution

Above instructions are complete.

### What You Learned

1. What other parts of the system auto-updated?
2. Did you need to modify the prompt?
3. How does TypeScript help when adding enum values?
4. What categories would you add for your domain?

---

## Experiment 5: Prompt Engineering - Tone Modification

**Difficulty**: ⭐⭐ Medium
**Time**: 15 minutes
**Concept**: Prompt engineering and its effects

### Objective

Change the AI's tone and observe response differences.

### Files to Modify

1. `lib/ai/prompts.ts`

### Instructions

**Experiment A**: Formal tone

```typescript
export const SUPPORT_AGENT_SYSTEM_PROMPT = `You are a professional, formal customer support representative. Maintain a business-appropriate tone at all times. Use complete sentences and avoid contractions.

...rest of prompt...
`;
```

**Experiment B**: Casual tone

```typescript
export const SUPPORT_AGENT_SYSTEM_PROMPT = `You are a friendly, casual support buddy. Use a conversational tone, contractions, and feel free to add emoji occasionally 😊

...rest of prompt...
`;
```

**Experiment C**: Expert technical tone

```typescript
export const SUPPORT_AGENT_SYSTEM_PROMPT = `You are a senior technical support engineer. Use precise technical terminology and assume the user has advanced knowledge.

...rest of prompt...
`;
```

### Expected Outcome

Same question, different tones:

- **Formal**: "I would be pleased to assist you with your refund request. Our standard refund processing time is five to seven business days."
- **Casual**: "Hey! I can totally help with that refund 😊 It usually takes about 5-7 business days to show up."
- **Technical**: "Refund processing follows our standard ACH transfer protocol, with settlement occurring within 5-7 business days depending on your financial institution's processing schedule."

### Solution

Try all three variations and compare responses.

### What You Learned

1. How does tone affect user satisfaction?
2. Which tone works best for which categories?
3. Can you combine tones conditionally (formal for billing, casual for general)?
4. How would you A/B test different tones?

---

## Experiment 6: Error Injection

**Difficulty**: ⭐ Easy
**Time**: 10 minutes
**Concept**: Error handling and debugging

### Objective

Intentionally create errors to understand error handling.

### Instructions

**Error 1**: Remove required field

```typescript
// Comment out final_answer in schema
// final_answer: z.string()...
```

**Expected**: Zod validation error, TypeScript compilation error.

**Error 2**: Invalid API key

```bash
# In .env
ANTHROPIC_API_KEY=invalid_key
```

**Expected**: AI provider authentication error.

**Error 3**: Network timeout (simulated)

```typescript
// In lib/ai/client.ts, add:
await new Promise(resolve => setTimeout(resolve, 60000)); // 60s delay
```

**Expected**: Request timeout.

### Solution

Observe error messages and recovery mechanisms. Revert all changes.

### What You Learned

1. Where are errors caught?
2. How are errors displayed to users?
3. What debugging information is available?
4. How would you improve error messages?

---

## Experiment 7: Type Safety Test

**Difficulty**: ⭐⭐ Medium
**Time**: 10 minutes
**Concept**: TypeScript type safety

### Objective

Try to break type safety and observe compiler protection.

### Instructions

**Test 1**: Wrong type assignment

```typescript
// In app/api/chat/route.ts
const supportAnswer = await generateSupportResponse(message);

// Try this (should error):
supportAnswer.confidence = "high"; // ❌ string not assignable to number
supportAnswer.category = "invalid"; // ❌ not in enum
```

**Test 2**: Missing required field

```typescript
const manualAnswer: SupportAnswer = {
  final_answer: "test",
  // Missing other required fields
}; // ❌ TypeScript error
```

**Test 3**: Access non-existent field

```typescript
console.log(supportAnswer.nonExistentField); // ❌ Property doesn't exist
```

### Solution

TypeScript should prevent all these! That's the point.

### What You Learned

1. How does TypeScript protect you?
2. What's the difference between compile-time and runtime errors?
3. Why is type inference better than manual types?

---

## Experiment 8: Metadata Extension

**Difficulty**: ⭐⭐ Medium
**Time**: 15 minutes
**Concept**: Schema extension and data enrichment

### Objective

Add token usage tracking to metadata.

### Files to Modify

1. `lib/schemas/support-answer.ts`
2. `lib/ai/client.ts`

### Instructions

**Step 1**: Extend metadata schema

```typescript
metadata: z.object({
  processing_time_ms: z.number().optional(),
  model_used: z.string().optional(),
  layer: z.string().default('L0-basic'),
  prompt_version: z.string().optional(),
  tokens_used: z.number().optional(), // NEW
  cost_usd: z.number().optional(), // NEW
}).optional(),
```

**Step 2**: Calculate tokens (estimate)

```typescript
// In lib/ai/client.ts

const estimatedTokens = Math.ceil(
  (systemPrompt.length + userMessage.length + JSON.stringify(result.object).length) / 4
);

const costPerToken = 0.000003; // $3 per 1M tokens (example)
const estimatedCost = estimatedTokens * costPerToken;

const enrichedResponse: SupportAnswer = {
  ...result.object,
  metadata: {
    ...result.object.metadata,
    processing_time_ms: processingTime,
    model_used: getModelId(),
    tokens_used: estimatedTokens,
    cost_usd: estimatedCost,
  },
};
```

### Solution

See above. Display in `/debug` view for monitoring.

### What You Learned

1. How to extend schemas without breaking existing code?
2. What other metadata would be useful?
3. How would you use this data in production?

---

## Experiment 9: Conditional UI - Human Escalation

**Difficulty**: ⭐⭐ Medium
**Time**: 20 minutes
**Concept**: Conditional rendering based on structured data

### Objective

Add an "Escalate to Human" button when `requires_human` is true.

### Files to Modify

1. `components/chat/MessageBubble.tsx`

### Instructions

```typescript
{/* Human escalation button */}
{message.structured_data && message.structured_data.requires_human && (
  <div className="mt-3">
    <button
      onClick={() => {
        // In production, this would open a support ticket
        alert('Connecting you with a human agent...');
      }}
      className="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 transition-colors"
    >
      Speak with Human Agent →
    </button>
  </div>
)}
```

### Expected Outcome

When AI sets `requires_human: true`, button appears.

### Solution

Test with: "I want to sue you" or "Legal advice needed"

### What You Learned

1. How structured data enables dynamic UX?
2. What other conditional UI could you add?
3. How would you track escalation rates?

---

## Experiment 10: Followup Question Limit

**Difficulty**: ⭐ Easy
**Time**: 10 minutes
**Concept**: Schema constraints and UI adaptation

### Objective

Change followup limit from 3 to 5 and update UI.

### Files to Modify

1. `lib/schemas/support-answer.ts`
2. Observe UI automatically adapts

### Instructions

```typescript
followups: z.array(z.string())
  .max(5) // Changed from 3
  .describe('Up to 5 suggested follow-up questions'),
```

### Expected Outcome

LLM may return up to 5 followups. UI displays all of them.

### Solution

Simple change. Observe how system adapts.

### What You Learned

1. How do constraints affect LLM behavior?
2. What's the UX trade-off of more followups?
3. What's the optimal number?

---

## Experiment 11: Citation Display Enhancement

**Difficulty**: ⭐⭐ Medium
**Time**: 25 minutes
**Concept**: Data formatting and links

### Objective

Make citations clickable when they're URLs.

### Files to Modify

1. `components/chat/MessageBubble.tsx`

### Instructions

Replace the simple citation display with:

```typescript
{/* Enhanced citations */}
{message.structured_data && message.structured_data.citations.length > 0 && (
  <div className="mt-2 bg-gray-50 rounded-lg p-3">
    <p className="text-xs font-medium text-gray-700 mb-2">Sources:</p>
    <ul className="space-y-1">
      {message.structured_data.citations.map((citation, i) => {
        // Check if citation is a URL
        const isURL = citation.startsWith('http://') || citation.startsWith('https://');

        return (
          <li key={i} className="text-sm text-gray-600">
            {isURL ? (
              <a
                href={citation}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800 underline"
              >
                {citation}
              </a>
            ) : (
              <span>📄 {citation}</span>
            )}
          </li>
        );
      })}
    </ul>
  </div>
)}
```

### Solution

See above.

### What You Learned

1. How to handle mixed data types (URLs vs filenames)?
2. What security considerations exist for links?
3. How would you validate URLs?

---

## Experiment 12: Debug Mode Toggle

**Difficulty**: ⭐⭐⭐ Advanced
**Time**: 30 minutes
**Concept**: Query parameters and conditional features

### Objective

Add `?debug=true` query parameter to show raw schema in UI.

### Files to Modify

1. `components/chat/ChatInterface.tsx`
2. `components/chat/MessageBubble.tsx`

### Instructions

**Step 1**: Detect debug mode

```typescript
// In ChatInterface.tsx

import { useSearchParams } from 'next/navigation';

export function ChatInterface() {
  const searchParams = useSearchParams();
  const debugMode = searchParams.get('debug') === 'true';

  // Pass to MessageBubble
  <MessageBubble message={message} debugMode={debugMode} />
}
```

**Step 2**: Display raw data in debug mode

```typescript
// In MessageBubble.tsx

interface MessageBubbleProps {
  message: Message;
  debugMode?: boolean; // NEW
}

export function MessageBubble({ message, debugMode = false }: MessageBubbleProps) {
  // ...existing code...

  {/* Debug panel */}
  {debugMode && !isUser && message.structured_data && (
    <details className="mt-2 bg-gray-900 rounded-lg">
      <summary className="text-xs text-white px-3 py-2 cursor-pointer">
        🔍 Debug: Raw Schema Data
      </summary>
      <pre className="text-xs text-green-400 p-3 overflow-x-auto">
        {JSON.stringify(message.structured_data, null, 2)}
      </pre>
    </details>
  )}
}
```

### Expected Outcome

Visit `http://localhost:3000?debug=true` and see raw JSON for each response.

### Solution

Complete implementation above.

### What You Learned

1. How to use URL parameters for features?
2. What debugging info is most useful?
3. How would you protect debug mode in production?
4. What other debug features would help?

---

## Bonus Experiments

### Experiment 13: Multi-Language Support

Add a `language` field and prompt the AI to respond in different languages.

### Experiment 14: Response Length Control

Add UI slider to control `max_tokens` dynamically.

### Experiment 15: Category-Specific Prompts

Load different system prompts based on detected category.

---

## Experiment Completion Checklist

After completing all experiments, you should be able to:

- ✅ Modify Zod schemas confidently
- ✅ Understand schema validation errors
- ✅ Change prompts and predict effects
- ✅ Build conditional UI from structured data
- ✅ Debug type errors
- ✅ Extend metadata
- ✅ Handle errors gracefully
- ✅ Use query parameters for features

**You've mastered Layer 0!** 🎉

---

## Next Steps

1. Review your completed experiments
2. Take the final assessment quiz in `docs/LEARNING_PATH.md`
3. Build a custom feature combining multiple concepts
4. Prepare for Layer 1: Observability with Logfire

**Happy experimenting!** 🚀
