# Layer 0 Checkpoint Quiz

> **Purpose**: Assess your understanding of Layer 0 concepts

## Instructions

1. Answer all questions in order
2. Don't look at the codebase (test your memory)
3. Write answers in a text file or notebook
4. Check answers at the end
5. Score yourself honestly

**Passing score**: 12/15 (80%)

---

## Part 1: Conceptual Understanding (5 questions)

### Question 1: Schema Rationale

**Q**: Why do we use Zod schemas instead of just TypeScript interfaces for structured outputs?

**Points**: 1

<details>
<summary>Answer</summary>

**Answer**: Zod schemas provide **runtime validation** in addition to compile-time types. TypeScript interfaces only exist at compile time and disappear after transpilation. Zod schemas:
1. Validate data at runtime (catch actual LLM errors)
2. Provide automatic type inference (`z.infer`)
3. Give detailed validation error messages
4. Can be converted to JSON Schema for the AI SDK
5. Serve as a single source of truth

**Key insight**: TypeScript = compile-time safety, Zod = runtime safety. You need both!
</details>

---

### Question 2: Structured vs Unstructured

**Q**: Explain the difference between `generateObject()` and `generateText()`. When would you use each?

**Points**: 1

<details>
<summary>Answer</summary>

**Answer**:

**generateObject()**:
- Returns JSON matching a Zod schema
- Guaranteed structure
- Type-safe output
- Use when you need predictable, parseable data

**generateText()**:
- Returns plain text string
- No structure guarantees
- More flexible
- Use for creative writing, summaries, or when structure isn't needed

**Example use cases**:
- `generateObject()`: API responses, form data, structured analysis
- `generateText()`: Blog posts, creative content, summaries

**Layer 0 uses `generateObject()` because we need consistent, type-safe responses.**
</details>

---

### Question 3: Confidence Scoring

**Q**: How does requiring a `confidence` field in the schema help reduce hallucination?

**Points**: 1

<details>
<summary>Answer</summary>

**Answer**: The confidence field creates a **meta-cognitive feedback loop**:

1. **Self-assessment**: Forces the LLM to evaluate its own certainty
2. **Uncertainty detection**: Models are actually good at knowing when they don't know
3. **Human escalation**: Low confidence can trigger human review
4. **Quality filtering**: You can discard or retry low-confidence responses

**Research insight**: LLMs that self-assess confidence tend to be more accurate because the act of assessing makes them "think" more carefully.

**Not a perfect solution**: Confidence scores aren't calibrated, but they're useful signals.
</details>

---

### Question 4: Stateless Design

**Q**: Why is Layer 0 stateless (no database)? What are the implications for conversation support?

**Points**: 1

<details>
<summary>Answer</summary>

**Answer**:

**Why stateless**:
1. **Simplicity**: Easier to learn and understand
2. **Focus**: Concentrate on core LLM concepts, not infrastructure
3. **Scalability**: Naturally scales horizontally
4. **Zero setup**: No database configuration required

**Implications**:
- ❌ No conversation history
- ❌ No user context across requests
- ❌ Can't reference previous messages
- ✅ But: Each request is independent and debuggable
- ✅ Perfect for learning fundamentals

**Layer 3 will add conversation memory**, building on this foundation.
</details>

---

### Question 5: Prompt Engineering Pattern

**Q**: Our system prompt includes "examples" of good responses. What prompt engineering technique is this, and why does it work?

**Points**: 1

<details>
<summary>Answer</summary>

**Answer**: This is **few-shot learning** (or few-shot prompting).

**How it works**:
1. LLM learns from examples in the prompt
2. Recognizes patterns and structure
3. Imitates style and format

**Why it's effective**:
- More reliable than pure instructions
- Shows rather than tells
- Anchors model behavior
- Reduces ambiguity

**Alternative**: Zero-shot (no examples) works but is less consistent.

**Our implementation**: Includes 2 examples (good billing response, low confidence response) to demonstrate range of acceptable outputs.
</details>

---

## Part 2: Practical Skills (5 questions)

### Question 6: Schema Modification

**Q**: You want to add a `priority` field (enum: low, medium, high, urgent). Write the Zod schema for this field including validation and description.

**Points**: 1

<details>
<summary>Answer</summary>

**Answer**:
```typescript
priority: z.enum(['low', 'medium', 'high', 'urgent'])
  .describe('Priority level of the support query'),
```

**Acceptable variations**:
```typescript
// With default value
priority: z.enum(['low', 'medium', 'high', 'urgent'])
  .default('medium')
  .describe('Priority level of the support query'),

// Optional
priority: z.enum(['low', 'medium', 'high', 'urgent'])
  .optional()
  .describe('Optional priority level of the support query'),
```

**Key points**:
- Must use `z.enum()` with array
- Must include `.describe()`
- Enum values should be strings (lowercase by convention)
</details>

---

### Question 7: Error Debugging

**Q**: You see this error in the terminal:
```
ZodError: [
  {
    "code": "too_small",
    "minimum": 10,
    "type": "string",
    "path": ["final_answer"]
  }
]
```

What's wrong, and how do you fix it?

**Points**: 1

<details>
<summary>Answer</summary>

**Answer**:

**What's wrong**: The `final_answer` field is too short (less than 10 characters).

**Why it happened**: The LLM generated a response shorter than the schema's `.min(10)` constraint.

**How to fix**:

**Option 1**: Adjust schema (if 10 chars is too strict)
```typescript
final_answer: z.string()
  .min(5) // Reduced from 10
```

**Option 2**: Improve prompt (encourage longer responses)
```typescript
"Provide a complete, helpful answer (minimum 10 characters)"
```

**Option 3**: Retry with different temperature/model

**Root cause**: Likely a prompt issue or edge case query. Check what the user asked.
</details>

---

### Question 8: Prompt Modification

**Q**: Modify the system prompt to make responses more concise (maximum 50 words). Show the specific change you'd make.

**Points**: 1

<details>
<summary>Answer</summary>

**Answer**:

**In `lib/ai/prompts.ts`**, add to the guidelines section:

```typescript
export const SUPPORT_AGENT_SYSTEM_PROMPT = `You are a helpful and knowledgeable customer support agent.

## Response Guidelines

1. **Accuracy over Speed**: ...

2. **Be Concise**: Provide complete answers in 50 words or less. Get straight to the point without unnecessary elaboration.

// ... rest of prompt
`;
```

**Or more forcefully**:
```typescript
2. **Maximum 50 Words**: All responses must be under 50 words. Be extremely concise and direct.
```

**Also adjust schema** (optional but recommended):
```typescript
final_answer: z.string()
  .min(10)
  .max(300) // ~50 words * 6 chars average
```

**Key point**: Combine prompt instruction with schema constraint for best results.
</details>

---

### Question 9: New Schema Creation

**Q**: Create a complete Zod schema for "FeedbackRequest" with these fields:
- rating (1-5 stars, required)
- comment (string, optional, max 500 chars)
- would_recommend (boolean, required)

**Points**: 1

<details>
<summary>Answer</summary>

**Answer**:
```typescript
// lib/schemas/feedback.ts

import { z } from 'zod';

export const FeedbackRequestSchema = z.object({
  rating: z.number()
    .int()
    .min(1, 'Rating must be at least 1')
    .max(5, 'Rating must be at most 5')
    .describe('Star rating from 1 to 5'),

  comment: z.string()
    .max(500, 'Comment too long (max 500 characters)')
    .optional()
    .describe('Optional feedback comment'),

  would_recommend: z.boolean()
    .describe('Whether user would recommend to others'),
});

export type FeedbackRequest = z.infer<typeof FeedbackRequestSchema>;
```

**Scoring**:
- Full credit: Includes all fields with proper constraints
- Partial credit: Missing `.describe()` or minor issues
- No credit: Incorrect types or missing required validations
</details>

---

### Question 10: Request Tracing

**Q**: A request fails in production. You have the `request_id: "abc123"`. List 3 places you'd check for logs/debugging info in order of priority.

**Points**: 1

<details>
<summary>Answer</summary>

**Answer**:

**Priority order**:

1. **Server logs** (terminal or log aggregator)
   - Search for `request_id: abc123`
   - Look for error level logs
   - Check timestamp correlation

2. **API route error handling** (`app/api/chat/route.ts`)
   - Check `handleAPIError()` output
   - Review error metadata
   - Examine error code and details

3. **Client browser logs** (if user can reproduce)
   - Network tab: See request/response
   - Console: JavaScript errors
   - Response body: Error details

**Additional checks**:
4. Validation errors in schema parsing
5. AI SDK logs (if available)
6. Provider status page (Anthropic/OpenAI outage?)

**Key insight**: `request_id` enables correlation across logs. This is why we generate it!
</details>

---

## Part 3: Critical Thinking (5 questions)

### Question 11: Architecture Trade-off

**Q**: We use client-side state (`useState`) in Layer 0. What breaks when the user refreshes the page? Propose a solution that doesn't require a database.

**Points**: 1

<details>
<summary>Answer</summary>

**Answer**:

**What breaks**:
- All conversation history lost
- User has to start over
- No persistence across sessions

**Solutions without database**:

**Option 1: localStorage** (best for Layer 0)
```typescript
// Save to localStorage after each message
useEffect(() => {
  localStorage.setItem('chat_history', JSON.stringify(messages));
}, [messages]);

// Load on mount
useEffect(() => {
  const saved = localStorage.getItem('chat_history');
  if (saved) setMessages(JSON.parse(saved));
}, []);
```

**Option 2: URL query parameters** (limited)
```typescript
// Encode last N messages in URL
?history=base64encodeddata
```

**Option 3: SessionStorage** (browser session only)
```typescript
sessionStorage.setItem('messages', JSON.stringify(messages));
```

**Trade-offs**:
- localStorage: Persists, but max ~5-10MB
- URL params: Shareable, but very limited size
- SessionStorage: Clean, but lost when browser closes

**Layer 2+ will use proper database.**
</details>

---

### Question 12: Schema Evolution

**Q**: You remove the `category` enum and make it free text (`z.string()`). Predict 2 problems this would cause.

**Points**: 1

<details>
<summary>Answer</summary>

**Answer**:

**Problem 1: Category drift**
- LLM invents inconsistent categories
- "billing" vs "Billing" vs "payment" vs "financial"
- Can't filter or group by category reliably
- Analytics become meaningless

**Problem 2: Broken UI**
```typescript
// This code breaks:
const colors: Record<string, string> = {
  billing: 'bg-blue-100',
  technical: 'bg-purple-100',
  // ...
};
const colorClass = colors[category]; // undefined for new categories!
```

**Problem 3: Loss of routing logic**
```typescript
// Can't do:
if (category === 'escalation') {
  // Route to urgent queue
}
// Because category values are unpredictable
```

**Additional issues**:
- Hard to write tests
- Migration nightmare
- No TypeScript type narrowing

**Key insight**: Enums provide structure. Free text provides chaos.
</details>

---

### Question 13: Rate Limiting

**Q**: How would you add rate limiting to `/api/chat` to prevent abuse? Describe your approach (no code required, but be specific).

**Points**: 1

<details>
<summary>Answer</summary>

**Answer**:

**Approach**:

**Option 1: IP-based limiting** (simple)
```
1. Extract IP from request headers
2. Check in-memory map: requests[ip] = count
3. If count > 10 requests/minute: Return 429
4. Increment count
5. Reset counts every minute (setInterval)
```

**Option 2: Token bucket** (better)
```
1. Each IP gets N tokens (bucket)
2. Each request consumes 1 token
3. Tokens refill at rate R per second
4. If bucket empty: Return 429
5. Allows bursts while limiting average
```

**Option 3: External service** (production)
```
- Use Vercel Rate Limiting
- Or Redis-based limiter
- Or Upstash Rate Limit
```

**Implementation details**:
```typescript
// In app/api/chat/route.ts
const ip = request.headers.get('x-forwarded-for') || 'unknown';
const rateLimiter = new RateLimiter({ maxRequests: 10, windowMs: 60000 });

if (!rateLimiter.check(ip)) {
  return Response.json(
    { error: { code: 'RATE_LIMIT', message: 'Too many requests' } },
    { status: 429 }
  );
}
```

**Considerations**:
- Per-IP vs per-user (if authenticated)
- Different limits for different plans
- Graceful degradation
- Clear error messages
</details>

---

### Question 14: Type Safety Benefits

**Q**: Give a concrete example of a bug that TypeScript would catch at compile-time that would be a runtime error in JavaScript.

**Points**: 1

<details>
<summary>Answer</summary>

**Answer**:

**Example**:
```typescript
// Bug: Typo in property name
const supportAnswer = await generateSupportResponse(message);

// JavaScript: Runtime error (property undefined)
console.log(supportAnswer.confience); // Oops! Typo: "confience"
// Output: undefined

// TypeScript: Compile-time error
console.log(supportAnswer.confience);
//                         ^^^^^^^^^
// Property 'confience' does not exist on type 'SupportAnswer'.
// Did you mean 'confidence'?
```

**More examples**:

**Example 2: Wrong type**
```typescript
supportAnswer.confidence = "high"; // String not assignable to number
```

**Example 3: Missing required field**
```typescript
const answer: SupportAnswer = {
  final_answer: "test"
  // TypeScript: Error! Missing required fields: confidence, category, ...
};
```

**Example 4: Non-existent method**
```typescript
supportAnswer.toUpperCase(); // Method doesn't exist on this type
```

**Key benefit**: Catch bugs during development, not in production!
</details>

---

### Question 15: Future Enhancement

**Q**: You're designing Layer 2 (RAG knowledge base). What new fields would you add to `SupportAnswer` and why?

**Points**: 1

<details>
<summary>Answer</summary>

**Answer**:

**Suggested fields**:

```typescript
// Layer 2 enhancements

// 1. Document references
source_documents: z.array(z.object({
  document_id: z.string(),
  title: z.string(),
  relevance_score: z.number().min(0).max(1),
  excerpt: z.string(),
}))
  .describe('Source documents from knowledge base'),

// 2. RAG-specific metadata
metadata: z.object({
  // ... existing fields
  retrieval_time_ms: z.number().optional(),
  documents_searched: z.number().optional(),
  embedding_model: z.string().optional(),
}),

// 3. Answer quality
answer_type: z.enum(['knowledge_base', 'general', 'hybrid'])
  .describe('Whether answer used KB or general knowledge'),

// 4. Verification
fact_checked: z.boolean()
  .default(false)
  .describe('Whether answer was verified against KB'),
```

**Rationale**:
- `source_documents`: Traceability and citation
- `retrieval_time_ms`: Performance monitoring
- `answer_type`: Distinguish RAG from general responses
- `fact_checked`: Quality assurance flag

**Key insight**: Each layer adds metadata that supports its new capabilities.
</details>

---

## Scoring

### Calculate Your Score

Count correct answers:
- **13-15**: 🌟 Excellent! You've mastered Layer 0
- **10-12**: ✅ Good! Ready to proceed, review missed concepts
- **7-9**: 📚 Fair. Spend more time on experiments and docs
- **0-6**: 🔄 Needs work. Re-read key documentation

### What to Review Based on Missed Questions

**Q1-5 (Conceptual)**: Read `docs/ARCHITECTURE.md` and `docs/README.md`

**Q6-10 (Practical)**: Complete `experiments/README.md` hands-on exercises

**Q11-15 (Critical Thinking)**: Study `docs/DATA_FLOW.md` and build a custom feature

---

## Next Steps

### If You Passed (80%+)

✅ You're ready for Layer 1!

**Prepare for**:
- Logfire observability integration
- Trace visualization
- Production monitoring
- Performance profiling

### If You Need More Practice

📚 **Focus on**:
1. Complete all 12 experiments
2. Build a custom schema for your domain
3. Modify prompts and observe effects
4. Trace requests end-to-end with debugging

### Challenge Yourself

Build a mini-project:
- Customer feedback system
- Bug report analyzer
- Product recommendation engine
- FAQ answering bot

**Apply all Layer 0 concepts**!

---

## Answer Key Summary

1. Runtime vs compile-time validation
2. Structured vs unstructured generation
3. Meta-cognitive confidence scoring
4. Stateless design trade-offs
5. Few-shot learning
6. Zod enum syntax
7. Schema validation debugging
8. Prompt constraint modification
9. Complete schema creation
10. Request tracing with request_id
11. Client-side persistence options
12. Enum vs free text problems
13. Rate limiting strategies
14. Type safety examples
15. RAG schema enhancements

---

**Congratulations on completing the quiz!** 🎉

Whether you aced it or have areas to improve, you've engaged deeply with Layer 0 concepts. Keep learning!
