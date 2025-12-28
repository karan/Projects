# Architecture Deep Dive - Layer 0

> **Purpose**: Understand the architectural decisions and design patterns in Layer 0

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [Schema-Driven Development](#schema-driven-development)
3. [Structured Outputs Explained](#structured-outputs-explained)
4. [Error Handling Strategy](#error-handling-strategy)
5. [Type Safety Approach](#type-safety-approach)
6. [Prompt Engineering Patterns](#prompt-engineering-patterns)
7. [Component Architecture](#component-architecture)
8. [Security Considerations](#security-considerations)
9. [Performance Considerations](#performance-considerations)
10. [Testing Strategy](#testing-strategy)

---

## Design Philosophy

### Core Principles

1. **Simplicity First**: Layer 0 is intentionally minimal
2. **Learning by Doing**: Code is the primary teacher
3. **Production Patterns**: Real-world code, not tutorials
4. **Type Safety**: Catch errors at compile time
5. **Explicit Over Implicit**: Clear over clever

### Why These Choices?

**Stateless Design**
- Easier to reason about
- No database complexity
- Focus on core LLM concepts
- Scales horizontally by default

**Extensive Documentation**
- Code comments explain "why"
- JSDoc provides context
- Examples show usage
- Learning checkpoints guide progress

**No External Dependencies** (beyond core stack)
- Reduced cognitive load
- Easier debugging
- Clear upgrade path
- Focus on fundamentals

---

## Schema-Driven Development

### The Central Concept

In traditional web development:
```
Data → Process → Display
```

In schema-driven LLM development:
```
Schema → Constrain → Validate → Display
```

### Why Schemas Matter

**Without Schemas** (Traditional LLM approach):
```typescript
// Unstructured output
const response = await llm.generate("Answer this question...");
// response = "Here's my answer: ..." (unpredictable format)

// Manual parsing required
const match = response.match(/confidence: (\d+\.?\d*)/);
const confidence = match ? parseFloat(match[1]) : 0.5;
// Fragile, error-prone, no type safety
```

**With Schemas** (Our approach):
```typescript
// Structured output
const response = await generateObject({
  schema: SupportAnswerSchema,
  prompt: "Answer this question..."
});
// response.object.confidence is guaranteed to be a number 0-1
// TypeScript knows this at compile time!
```

### Schema Design Principles

**1. Progressive Disclosure**
- Start with required fields only
- Add optional fields as needed
- Default values prevent breaking changes

**2. Validation at Boundaries**
```typescript
// Validate inputs
const input = ChatRequestSchema.parse(userInput);

// Process (business logic)
const result = await generateSupportResponse(input.message);

// Validate outputs
const output = SupportAnswerSchema.parse(result);
```

**3. Self-Documenting Schemas**
```typescript
confidence: z.number()
  .min(0)
  .max(1)
  .describe('Confidence score from 0.0 to 1.0')
```

The `.describe()` serves multiple purposes:
- Documentation for developers
- Hints for LLMs during generation
- Schema introspection for debug views

---

## Structured Outputs Explained

### How It Works (Deep Dive)

**Step 1: Schema Definition**
```typescript
export const SupportAnswerSchema = z.object({
  final_answer: z.string().min(10).max(2000),
  confidence: z.number().min(0).max(1),
  // ... more fields
});
```

**Step 2: AI SDK Conversion**
The AI SDK converts Zod schemas to JSON Schema:
```json
{
  "type": "object",
  "properties": {
    "final_answer": {
      "type": "string",
      "minLength": 10,
      "maxLength": 2000
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    }
  },
  "required": ["final_answer", "confidence"]
}
```

**Step 3: LLM Constraint**
The LLM is instructed to ONLY output JSON matching this schema:
```
System: You must respond with JSON matching this exact schema: {...}
User: How do I get a refund?
Assistant: { "final_answer": "...", "confidence": 0.9, ... }
```

**Step 4: Validation**
The AI SDK parses and validates the response:
```typescript
const rawOutput = await llm.generate(...);
const validated = SupportAnswerSchema.parse(JSON.parse(rawOutput));
// Throws if invalid!
```

**Step 5: Type Inference**
TypeScript knows the shape automatically:
```typescript
type SupportAnswer = z.infer<typeof SupportAnswerSchema>;
// No manual type definition needed!
```

### Benefits

| Aspect | Unstructured | Structured |
|--------|--------------|------------|
| Parsing | Manual regex/parsing | Automatic |
| Validation | Custom logic | Schema-driven |
| Type Safety | None | Full TypeScript |
| Consistency | Varies by prompt | Guaranteed |
| Debugging | Difficult | Schema violations are clear |
| Refactoring | Breaking changes | Compile-time errors |

---

## Error Handling Strategy

### Layered Error Handling

**Layer 1: Input Validation**
```typescript
const result = ChatRequestSchema.safeParse(body);
if (!result.success) {
  return errorResponse('VALIDATION_ERROR', ...);
}
```

**Layer 2: Business Logic Errors**
```typescript
try {
  const answer = await generateSupportResponse(message);
} catch (error) {
  return handleAPIError(error);
}
```

**Layer 3: Output Validation**
```typescript
// AI SDK handles this internally
// Throws if LLM output doesn't match schema
```

### Error Response Format

**Standardized Structure**:
```typescript
{
  error: {
    code: 'VALIDATION_ERROR',        // Machine-readable
    message: 'User-friendly message', // Human-readable
    details: {...},                   // Dev-only technical info
    timestamp: '2025-01-15T...',
    request_id: 'abc123'              // For tracing
  }
}
```

**Why This Format?**
- Clients can handle by `code`
- Users see friendly `message`
- Developers use `details` and `request_id` for debugging
- `timestamp` aids in log correlation

### Error Type Discrimination

```typescript
export function mapErrorToCode(error: unknown): ErrorCode {
  if (error instanceof z.ZodError) {
    return 'VALIDATION_ERROR';
  }
  if (error instanceof Error) {
    if (error.message.includes('rate limit')) {
      return 'RATE_LIMIT';
    }
    // ... more cases
  }
  return 'UNKNOWN_ERROR';
}
```

---

## Type Safety Approach

### TypeScript Configuration

**tsconfig.json highlights**:
```json
{
  "strict": true,
  "noUncheckedIndexedAccess": true,
  "noUnusedLocals": true,
  "noUnusedParameters": true
}
```

These settings catch:
- `undefined` access
- Unused variables (dead code)
- Missing null checks
- Implicit `any` types

### No `any` Policy

**Bad**:
```typescript
function process(data: any) {
  return data.something; // No type safety!
}
```

**Good**:
```typescript
function process(data: unknown) {
  if (typeof data === 'object' && data !== null && 'something' in data) {
    return data.something; // Type-safe!
  }
  throw new Error('Invalid data');
}
```

### Type Inference Over Explicit Types

**Manual (Don't do this)**:
```typescript
export type SupportAnswer = {
  final_answer: string;
  confidence: number;
  // ... 50 lines later, schema and type don't match
};
```

**Inferred (Do this)**:
```typescript
export const SupportAnswerSchema = z.object({...});
export type SupportAnswer = z.infer<typeof SupportAnswerSchema>;
// Single source of truth!
```

---

## Prompt Engineering Patterns

### Anatomy of Our System Prompt

**1. Role Definition**
```
You are a helpful and knowledgeable customer support agent.
```
Sets the context and tone.

**2. Capability Boundaries**
```
You can help with:
- Billing questions
- Technical issues
...
```
Prevents scope creep.

**3. Quality Guidelines**
```
1. Accuracy over Speed
2. Be Concise
...
```
Shapes response characteristics.

**4. Self-Assessment**
```
Always include a confidence score (0.0 to 1.0)
```
Meta-cognitive pattern.

**5. Examples**
```
Good Response (Billing Query): {...}
```
Few-shot learning.

### Why This Structure Works

- **LLMs are role-players**: Giving them a clear role improves performance
- **Constraints reduce variance**: Explicit rules = consistent outputs
- **Examples anchor behavior**: Few-shot > zero-shot
- **Self-assessment improves accuracy**: Meta-cognition pattern

### Prompt Versioning

```typescript
export const PROMPT_VERSION = '1.0';
```

Why version prompts?
- Track changes over time
- Correlate prompt versions with output quality
- A/B test different approaches
- Debug regressions

---

## Component Architecture

### React Component Hierarchy

```
page.tsx (Server Component)
  └── ChatInterface.tsx (Client Component)
      ├── MessageBubble.tsx (Client)
      │   ├── ConfidenceIndicator
      │   └── CategoryBadge
      └── InputArea.tsx (Client)
```

### Server vs Client Components

**Server Components** (`page.tsx`, `layout.tsx`):
- No JavaScript sent to client
- Can access secrets safely
- Better SEO
- Smaller bundle size

**Client Components** (`ChatInterface.tsx`, etc.):
- Interactive (useState, onClick)
- Browser APIs
- Real-time updates

### State Management

**Layer 0 uses local state**:
```typescript
const [messages, setMessages] = useState<Message[]>([]);
```

Why not global state?
- Simpler to understand
- No external dependencies
- Sufficient for single-page app
- Clear upgrade path (Layer 3 will add Zustand/etc)

---

## Security Considerations

### Input Sanitization

**Always validate**:
```typescript
const validated = ChatRequestSchema.parse(userInput);
```

Prevents:
- Malformed data
- Injection attacks (though LLMs are naturally resistant)
- Resource abuse (e.g., 10MB messages)

### API Key Safety

**Good** ✅:
```typescript
// Server-side (API routes)
const apiKey = process.env.ANTHROPIC_API_KEY;
```

**Bad** ❌:
```typescript
// Client-side component
const apiKey = process.env.NEXT_PUBLIC_ANTHROPIC_API_KEY; // LEAKED!
```

### Error Message Sanitization

```typescript
details: process.env.NODE_ENV === 'development' ? details : undefined
```

Never expose:
- Stack traces in production
- File paths
- API keys
- Internal service names

---

## Performance Considerations

### Response Time Targets

| Component | Target | Actual (Layer 0) |
|-----------|--------|------------------|
| Input validation | <1ms | ~0.5ms |
| API route overhead | <10ms | ~5ms |
| LLM generation | 1-3s | 1-2s |
| Total (cold start) | <5s | 2-3s |

### Optimization Strategies

**1. Parallel Processing**
```typescript
// Don't do this (serial)
await validateInput();
await getConfig();
await callLLM();

// Do this (parallel where possible)
const [validInput, config] = await Promise.all([
  validateInput(),
  getConfig(),
]);
await callLLM(validInput, config);
```

**2. Minimal Bundle Size**
- Server components for static content
- Code splitting for debug views
- Tree-shaking unused code

**3. Streaming (Layer 1+)**
Layer 0 is non-streaming for simplicity.
Future layers will use `streamObject()`.

---

## Testing Strategy

### Layer 0 Testing Philosophy

**Manual Testing Focus**:
- Use debug view
- Experiment with edge cases
- Validate schema violations
- Test error handling

**Why No Unit Tests Yet?**
1. Learning project (tests add complexity)
2. Rapid iteration expected
3. Schema validation provides safety net
4. Experiments serve as "tests"

### Future Testing (Layer 2+)

```typescript
describe('SupportAnswerSchema', () => {
  it('validates correct objects', () => {
    const valid = {
      final_answer: 'Test answer',
      confidence: 0.8,
      // ...
    };
    expect(() => SupportAnswerSchema.parse(valid)).not.toThrow();
  });

  it('rejects invalid confidence', () => {
    const invalid = { confidence: 1.5 };
    expect(() => SupportAnswerSchema.parse(invalid)).toThrow();
  });
});
```

---

## Architectural Trade-offs

### Decisions and Rationale

| Decision | Pro | Con | Rationale |
|----------|-----|-----|-----------|
| Stateless | Simple, scalable | No conversation memory | Learning focus |
| No database | Zero setup | No persistence | Layer 0 simplicity |
| Client state | Easy to understand | Resets on refresh | Acceptable for demo |
| Extensive comments | Self-documenting | Verbose | Educational priority |
| Single schema | Focused learning | Less flexible | Teachable moment |

### Evolution Path

```
Layer 0: Stateless, in-memory
         ↓
Layer 1: Add observability (Logfire)
         ↓
Layer 2: Add database (Supabase) + RAG
         ↓
Layer 3: Add conversation memory
         ↓
Production: Rate limiting, auth, caching
```

Each layer builds on the foundation without breaking it.

---

## Summary

**Key Architectural Insights**:

1. **Schemas are contracts** between app and LLM
2. **Type inference** eliminates manual type definitions
3. **Validation at boundaries** ensures data integrity
4. **Prompts are code** and should be versioned
5. **Errors are data** and should be structured
6. **Components are pure** where possible
7. **Security by default** (server-side secrets)

**Learning Outcomes**:

After understanding this architecture, you can:
- Design schemas for any LLM application
- Implement type-safe API routes
- Structure prompts effectively
- Handle errors gracefully
- Build accessible React UIs

**Next Steps**:

Read `DATA_FLOW.md` to trace a request through this architecture.
