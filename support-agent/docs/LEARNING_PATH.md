# Learning Path - Layer 0

> **Purpose**: A structured curriculum for mastering Layer 0 concepts

## How to Use This Guide

1. **Follow the order**: Concepts build on each other
2. **Code-first**: Read code before theory
3. **Experiment**: Try each checkpoint activity
4. **Reflect**: Answer the checkpoint questions
5. **Iterate**: Return to earlier concepts as needed

---

## Week 1: Foundations

### Day 1-2: Schema Understanding

**Learning Objective**: Understand why and how schemas constrain LLM outputs

**Read** (in order):
1. `lib/schemas/support-answer.ts` - The core schema
2. `lib/schemas/validation.ts` - Input validation
3. `lib/types/index.ts` - Type definitions

**Concepts**:
- Runtime validation with Zod
- Type inference (`z.infer`)
- Schema constraints (min, max, enum)
- Optional vs required fields
- Default values

**Checkpoint Activity**:
```typescript
// Create a new schema for user feedback
// File: lib/schemas/feedback.ts

export const FeedbackSchema = z.object({
  rating: z.number().min(1).max(5),
  comment: z.string().max(500),
  would_recommend: z.boolean(),
  category: z.enum(['helpful', 'confusing', 'incorrect']),
});

export type Feedback = z.infer<typeof FeedbackSchema>;
```

**Checkpoint Questions**:
1. What happens if the LLM returns `confidence: 1.5`?
2. Why use `z.infer` instead of manual type definition?
3. How do `.min()` and `.max()` differ from TypeScript types?
4. What's the difference between `.optional()` and `.default()`?

**Expected Outcomes**:
- ✅ Can create Zod schemas from scratch
- ✅ Understand schema validation errors
- ✅ Explain runtime vs compile-time validation

---

### Day 3-4: Prompt Engineering

**Learning Objective**: Understand how prompts shape LLM behavior

**Read** (in order):
1. `lib/ai/prompts.ts` - System prompt design
2. `lib/ai/config.ts` - Model configuration
3. `docs/ARCHITECTURE.md` (Prompt Engineering section)

**Concepts**:
- Role-based instruction
- Capability boundaries
- Self-assessment patterns
- Few-shot examples
- Prompt versioning

**Checkpoint Activity**:
```typescript
// Modify lib/ai/prompts.ts
// Change temperature and tone

export const SUPPORT_AGENT_SYSTEM_PROMPT = `You are a friendly and casual customer support agent. Use a conversational tone and emojis occasionally. ...`;

// Then test: Does the response style change?
```

**Experiments to Try**:
1. **Formal tone**: "You are a professional, formal support representative..."
2. **Concise mode**: Add "Respond in 2 sentences maximum"
3. **Expert mode**: "You are a technical expert. Use industry jargon..."

**Checkpoint Questions**:
1. How does temperature affect output variety?
2. Why do we version prompts?
3. What's the difference between system and user messages?
4. How do examples (few-shot) improve responses?

**Expected Outcomes**:
- ✅ Can write effective system prompts
- ✅ Understand temperature trade-offs
- ✅ Explain role-based instruction benefits

---

### Day 5-7: Structured Generation

**Learning Objective**: Understand how AI SDK generates structured outputs

**Read** (in order):
1. `lib/ai/client.ts` - generateObject wrapper
2. `docs/ARCHITECTURE.md` (Structured Outputs section)
3. `docs/DATA_FLOW.md` (Step 5-6)

**Concepts**:
- `generateObject()` vs `generateText()`
- Schema-constrained generation
- JSON Schema conversion
- Automatic validation
- Retry logic

**Checkpoint Activity**:
```typescript
// Add logging to see the process
// In lib/ai/client.ts

console.log('Schema:', SupportAnswerSchema);
console.log('Prompt:', userMessage);

const result = await generateObject({...});

console.log('Raw result:', result);
console.log('Validation:', SupportAnswerSchema.safeParse(result.object));
```

**Checkpoint Questions**:
1. What's the difference between structured and unstructured generation?
2. How does the AI SDK enforce schema compliance?
3. What happens if the LLM violates the schema?
4. Why is automatic validation important?

**Expected Outcomes**:
- ✅ Can use `generateObject()` effectively
- ✅ Understand schema validation flow
- ✅ Explain benefits over manual parsing

---

## Week 2: Application Architecture

### Day 8-9: API Design

**Learning Objective**: Understand API route structure and patterns

**Read** (in order):
1. `app/api/chat/route.ts` - API endpoint
2. `lib/utils/error-handling.ts` - Error patterns
3. `docs/DATA_FLOW.md` (Steps 3-7)

**Concepts**:
- Next.js App Router API routes
- Request/response envelopes
- Error handling layers
- Validation at boundaries
- Request ID tracing

**Checkpoint Activity**:
```typescript
// Add a new API route: app/api/validate/route.ts
// Purpose: Validate a SupportAnswer object without LLM

export async function POST(request: NextRequest) {
  const body = await request.json();
  const result = SupportAnswerSchema.safeParse(body);

  return Response.json({
    valid: result.success,
    errors: result.success ? null : result.error.issues,
  });
}
```

**Checkpoint Questions**:
1. Why validate both request and response?
2. What's the purpose of request IDs?
3. How do error codes differ from HTTP status codes?
4. Why separate error handling into its own module?

**Expected Outcomes**:
- ✅ Can create API routes
- ✅ Implement proper error handling
- ✅ Understand request/response lifecycle

---

### Day 10-11: Type Safety

**Learning Objective**: Master TypeScript strict mode and type safety

**Read** (in order):
1. `tsconfig.json` - TypeScript configuration
2. `lib/types/index.ts` - Type definitions
3. `docs/ARCHITECTURE.md` (Type Safety section)

**Concepts**:
- Strict mode benefits
- Type inference vs explicit types
- Utility types
- Type guards
- `unknown` vs `any`

**Checkpoint Activity**:
```typescript
// Practice type safety
// Try to compile this:

function process(data: any) { // ❌ any is banned
  return data.something;
}

// Fix it:
function process(data: unknown) { // ✅ unknown is safe
  if (typeof data === 'object' && data !== null && 'something' in data) {
    return (data as { something: unknown }).something;
  }
  throw new Error('Invalid data');
}
```

**Checkpoint Questions**:
1. What's the difference between `unknown` and `any`?
2. Why enable `noUncheckedIndexedAccess`?
3. How does type inference reduce boilerplate?
4. What are the benefits of strict TypeScript?

**Expected Outcomes**:
- ✅ Write type-safe code
- ✅ Avoid `any` types
- ✅ Use utility types effectively

---

### Day 12-14: React Architecture

**Learning Objective**: Understand component patterns and state management

**Read** (in order):
1. `components/chat/ChatInterface.tsx` - Main component
2. `components/chat/MessageBubble.tsx` - Child component
3. `components/chat/InputArea.tsx` - Form handling
4. `app/page.tsx` - Page composition

**Concepts**:
- Server vs Client Components
- Local state management
- Optimistic updates
- Event handling
- Accessibility

**Checkpoint Activity**:
```typescript
// Add a "copy to clipboard" feature
// In MessageBubble.tsx

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <button onClick={handleCopy}>
      {copied ? 'Copied!' : 'Copy'}
    </button>
  );
}
```

**Checkpoint Questions**:
1. Why use optimistic updates?
2. What's the difference between Server and Client Components?
3. How does local state compare to global state?
4. Why are accessible forms important?

**Expected Outcomes**:
- ✅ Build accessible React components
- ✅ Manage state effectively
- ✅ Implement UX best practices

---

## Week 3: Integration & Mastery

### Day 15-16: End-to-End Flow

**Learning Objective**: Trace data through the entire system

**Read** (in order):
1. `docs/DATA_FLOW.md` - Complete walkthrough
2. All previously read files (review)

**Checkpoint Activity**:
1. Set breakpoints in:
   - `InputArea.tsx` (user input)
   - `app/api/chat/route.ts` (validation)
   - `lib/ai/client.ts` (generation)
   - `MessageBubble.tsx` (rendering)

2. Submit a question and step through each breakpoint

3. Draw your own diagram of the flow

**Checkpoint Questions**:
1. Where does validation happen? (List all places)
2. What data transformations occur?
3. How many TypeScript types are involved?
4. Where could performance be optimized?

**Expected Outcomes**:
- ✅ Trace requests end-to-end
- ✅ Understand all data transformations
- ✅ Identify optimization opportunities

---

### Day 17-18: Experiments

**Learning Objective**: Hands-on modifications to solidify learning

**Do**: Complete experiments from `experiments/README.md`

**Suggested Order**:
1. Experiment 1: Add sentiment field
2. Experiment 3: Confidence threshold
3. Experiment 4: New category
4. Experiment 5: Prompt engineering
5. Experiment 8: Metadata extension
6. Experiment 12: Debug mode

**Expected Outcomes**:
- ✅ Confident making changes
- ✅ Understand ripple effects
- ✅ Debug issues independently

---

### Day 19-20: Debug & Introspect

**Learning Objective**: Master debugging and introspection tools

**Read** (in order):
1. `components/debug/SchemaViewer.tsx` - Schema introspection
2. `app/debug/page.tsx` - Debug view
3. `lib/utils/logging.ts` - Logging patterns

**Checkpoint Activity**:
```typescript
// Add a new debug panel
// File: components/debug/PromptViewer.tsx

export function PromptViewer() {
  const systemPrompt = getSystemPrompt();
  const metadata = getPromptMetadata();

  return (
    <div>
      <h2>System Prompt</h2>
      <pre>{systemPrompt}</pre>
      <div>Version: {metadata.version}</div>
    </div>
  );
}
```

**Checkpoint Questions**:
1. How does schema introspection work?
2. What debugging info is most useful?
3. How do logs aid troubleshooting?
4. What would you add to the debug view?

**Expected Outcomes**:
- ✅ Use debug tools effectively
- ✅ Read logs for insights
- ✅ Build debugging aids

---

### Day 21: Assessment

**Final Checkpoint Quiz** (see end of this document)

**Build a Feature**:
Create a "suggestions" feature that:
1. Adds a `suggestions` field to SupportAnswer
2. Modifies the prompt to generate suggestions
3. Displays suggestions in the UI
4. Includes validation and error handling

**Success Criteria**:
- ✅ Schema validates correctly
- ✅ LLM populates field
- ✅ UI renders suggestions
- ✅ No TypeScript errors
- ✅ Proper error handling

---

## Learning Styles

### For Visual Learners

**Activities**:
- Draw diagrams of data flow
- Use `/debug` view extensively
- Create Mermaid diagrams
- Color-code components by role

**Resources**:
- `docs/visuals/diagrams.md`
- `npm run ascii-flow`

### For Hands-On Learners

**Activities**:
- Start with experiments immediately
- Break things intentionally
- Use `console.log` liberally
- Rebuild from scratch

**Resources**:
- `experiments/README.md`

### For Reading-First Learners

**Activities**:
- Read all documentation before coding
- Take notes on each concept
- Create summary documents
- Ask "why" for every decision

**Resources**:
- All `docs/*.md` files
- Inline code comments

---

## Troubleshooting Learning Blocks

### "I don't understand schemas"

**Try**:
1. Read `lib/schemas/support-answer.ts` line-by-line
2. Run validation examples in Node REPL
3. Intentionally violate schema constraints
4. Build a simple schema from scratch

### "Prompts seem like magic"

**Try**:
1. Change one word in the prompt and observe
2. Remove sections and see degradation
3. Compare with/without examples
4. Test different temperatures

### "The flow is too complex"

**Try**:
1. Focus on one layer at a time
2. Use `console.log` at each step
3. Set breakpoints in debugger
4. Draw simplified diagrams

### "TypeScript errors are confusing"

**Try**:
1. Read error messages carefully (bottom-up)
2. Check type definitions
3. Use `// @ts-expect-error` temporarily
4. Ask TypeScript to infer type: `type X = typeof y`

---

## Final Assessment Quiz

### Part 1: Conceptual Understanding

1. **Explain**: Why do we use Zod schemas instead of TypeScript interfaces?

2. **Compare**: What's the difference between `generateObject()` and `generateText()`?

3. **Analyze**: How does the confidence field help reduce hallucination?

4. **Design**: If you were adding a RAG layer, what new schema fields would you add?

5. **Evaluate**: What are the trade-offs of optimistic UI updates?

### Part 2: Practical Skills

6. **Implement**: Add a `priority` field (enum: low, medium, high, urgent) to SupportAnswer

7. **Debug**: Given this error, explain what's wrong:
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

8. **Modify**: Change the system prompt to make responses more concise (max 50 words)

9. **Extend**: Create a second schema for "escalation tickets" with different fields

10. **Trace**: Given a request ID, what logs would you check to debug a failure?

### Part 3: Critical Thinking

11. **Justify**: Why is Layer 0 stateless? What are the implications?

12. **Predict**: What would break if we removed the `category` enum and made it free text?

13. **Propose**: How would you add rate limiting to the API route?

14. **Reflect**: What was the most surprising thing you learned?

15. **Plan**: What feature would you build for Layer 1?

---

## Answer Key (Self-Assessment)

**Strong understanding**: Can answer 12+ questions confidently

**Good foundation**: Can answer 8-11 questions with reference to docs

**Need more practice**: Can answer < 8 questions → Review weak areas

---

## Next Steps After Layer 0

### Ready for Layer 1 when you can:

- ✅ Create Zod schemas independently
- ✅ Write effective system prompts
- ✅ Debug TypeScript type errors
- ✅ Trace requests end-to-end
- ✅ Build accessible React components
- ✅ Implement error handling
- ✅ Explain architectural decisions

### Layer 1 Preview

**New Concepts**:
- Logfire observability
- Trace visualization
- Production monitoring
- Performance profiling

**Skills Required**:
- Solid Layer 0 foundation
- Async JavaScript
- Reading flame graphs
- Log analysis

---

## Continued Learning Resources

### Books
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "Refactoring UI" by Adam Wathan & Steve Schoger

### Courses
- [Vercel AI SDK Course](https://sdk.vercel.ai/docs)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)

### Communities
- AI SDK Discord
- Next.js Discord
- r/typescript

---

**Remember**: Learning is non-linear. Revisit concepts, ask questions, and experiment freely!
