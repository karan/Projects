# Support Agent - Layer 0: Foundation

> **AI-powered support agent with structured outputs** | A comprehensive learning project for LLM application development

[![TypeScript](https://img.shields.io/badge/TypeScript-5.4-blue.svg)](https://www.typescriptlang.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2-black.svg)](https://nextjs.org/)
[![Vercel AI SDK](https://img.shields.io/badge/Vercel%20AI%20SDK-4.0-orange.svg)](https://sdk.vercel.ai/)
[![Zod](https://img.shields.io/badge/Zod-3.23-blue.svg)](https://zod.dev/)

---

## 🎯 Quick Start (3 Commands)

```bash
# 1. Install dependencies
npm install

# 2. Configure environment
cp .env.example .env
# Add your ANTHROPIC_API_KEY or OPENAI_API_KEY to .env

# 3. Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) 🚀

**Detailed setup**: See [SETUP.md](./SETUP.md)

---

## 📖 What Is This?

A **dual-purpose project**:

1. **Working Application**: Production-grade AI support agent with structured, type-safe responses
2. **Learning Resource**: Comprehensive educational material for understanding LLM application development

### What Makes It Different?

- ✅ **Bottom-up learning**: Study code to understand concepts
- ✅ **Production patterns**: Real-world architecture, not tutorials
- ✅ **Extensive documentation**: Every file teaches
- ✅ **Hands-on experiments**: 12 progressive coding exercises
- ✅ **Type-safe**: Full TypeScript with strict mode
- ✅ **Schema-driven**: Zod schemas ensure consistency

---

## 🧠 What You'll Learn

### Core Concepts

```
┌─────────────────────────────────────────────┐
│ 1. Structured Outputs with Zod             │
│    → Runtime validation                     │
│    → Type inference                         │
│    → Schema-driven development              │
├─────────────────────────────────────────────┤
│ 2. Prompt Engineering                       │
│    → System prompt design                   │
│    → Few-shot learning                      │
│    → Self-assessment patterns               │
├─────────────────────────────────────────────┤
│ 3. Type Safety with TypeScript             │
│    → Strict mode benefits                   │
│    → Type inference from schemas            │
│    → Compile-time error prevention          │
├─────────────────────────────────────────────┤
│ 4. API Design                               │
│    → Request/response validation            │
│    → Error handling strategies              │
│    → Observability basics                   │
├─────────────────────────────────────────────┤
│ 5. React Patterns                           │
│    → Server vs Client Components            │
│    → Optimistic UI updates                  │
│    → Accessible forms                       │
└─────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
support-agent/
├── app/                          # Next.js App Router
│   ├── api/chat/route.ts        # ⭐ API endpoint
│   ├── debug/page.tsx           # Debug/introspection view
│   ├── layout.tsx               # Root layout
│   └── page.tsx                 # Main chat interface
├── lib/
│   ├── ai/                      # AI SDK integration
│   │   ├── client.ts            # ⭐ generateObject wrapper
│   │   ├── config.ts            # Model configuration
│   │   └── prompts.ts           # ⭐ System prompts
│   ├── schemas/
│   │   ├── support-answer.ts    # ⭐ Core output schema
│   │   ├── validation.ts        # Input validation
│   │   └── index.ts             # Schema exports
│   ├── types/                   # TypeScript types
│   └── utils/                   # Error handling, logging
├── components/
│   ├── chat/                    # Chat UI components
│   └── debug/                   # Debug components
├── docs/                        # 📚 Comprehensive docs
│   ├── README.md                # Overview & concept map
│   ├── ARCHITECTURE.md          # Deep dive
│   ├── DATA_FLOW.md             # Request tracing
│   ├── LEARNING_PATH.md         # Structured curriculum
│   └── visuals/                 # Diagrams & flowcharts
├── experiments/                 # 🧪 12 hands-on experiments
├── SETUP.md                     # Installation guide
├── QUIZ.md                      # Assessment quiz
└── README.md                    # You are here

⭐ = Start reading here
```

---

## 🗺️ Learning Path

### For Beginners

```
Day 1-2:  Read docs/README.md + SETUP.md
Day 3-5:  Study core schema (lib/schemas/support-answer.ts)
Day 6-8:  Understand prompts (lib/ai/prompts.ts)
Day 9-12: Follow experiments/README.md (Exp 1-6)
Day 13-14: Complete remaining experiments
Day 15:   Take QUIZ.md assessment
```

### For Experienced Developers

```
Hour 1: Skim ARCHITECTURE.md for design decisions
Hour 2: Read lib/ai/client.ts and API route
Hour 3: Complete 3-4 experiments
Hour 4: Build a custom feature
```

### For AI/ML Engineers

```
Focus on:
→ lib/ai/prompts.ts (prompt engineering)
→ lib/schemas/ (structured outputs)
→ docs/ARCHITECTURE.md (schema design)
→ Experiments 5, 8, 12 (advanced topics)
```

---

## 🚀 Key Features

### 1. Structured Outputs

**Problem**: LLMs return unpredictable text
**Solution**: Schema-constrained generation

```typescript
const answer = await generateObject({
  schema: SupportAnswerSchema,
  prompt: userQuery
});

// Guaranteed shape:
answer.final_answer  // string (10-2000 chars)
answer.confidence    // number (0.0-1.0)
answer.category      // enum (billing|technical|...)
answer.followups     // string[] (max 3)
```

### 2. Self-Assessment

AI evaluates its own confidence:

```json
{
  "confidence": 0.92,
  "requires_human": false
}
```

Low confidence → Human escalation

### 3. Type Safety

```typescript
// ❌ This won't compile:
answer.confidence = "high";
//                  ^^^^^^ Type 'string' not assignable to type 'number'

// ✅ This is type-safe:
if (answer.confidence < 0.5) {
  escalateToHuman();
}
```

### 4. Observability

Every request has:
- Unique `request_id` for tracing
- Processing time metrics
- Detailed error messages
- Debug mode for development

---

## 📚 Documentation Guide

| Document | Purpose | Read When |
|----------|---------|-----------|
| **README.md** | Overview & quick start | First thing |
| **SETUP.md** | Installation & config | Before running |
| **docs/README.md** | Project philosophy | After setup |
| **docs/ARCHITECTURE.md** | Design deep-dive | When building features |
| **docs/DATA_FLOW.md** | Request tracing | When debugging |
| **docs/LEARNING_PATH.md** | Structured curriculum | For systematic study |
| **experiments/README.md** | Hands-on practice | After reading code |
| **QUIZ.md** | Self-assessment | After experiments |

---

## 🧪 Try It Now

### Interactive Demo

```bash
npm run dev
```

Then ask:
- ❓ "How do I get a refund?"
- ❓ "My account is locked, help!"
- ❓ "Can you add dark mode?"

Observe:
- ✅ Structured response with confidence
- ✅ Category classification
- ✅ Follow-up suggestions
- ✅ Citation handling

### Debug View

Visit [http://localhost:3000/debug](http://localhost:3000/debug)

Inspect:
- Schema structure
- Validation rules
- Current configuration
- Example valid objects

### ASCII Flow

```bash
npm run ascii-flow
```

Beautiful terminal visualization of data flow!

---

## 🎯 Use Cases

This foundation supports building:

- **Customer Support**: Automated ticket responses
- **FAQ Bots**: Knowledge base querying
- **Bug Triaging**: Automatic categorization
- **Feedback Analysis**: Sentiment + category extraction
- **Product Recommendations**: Structured suggestions

**Layer 0**: Basic structured outputs (you are here)
**Layer 1**: + Observability (Logfire)
**Layer 2**: + RAG knowledge base
**Layer 3**: + Conversation memory

---

## 🛠️ Tech Stack

| Technology | Purpose | Why This Choice |
|------------|---------|-----------------|
| **Next.js 14** | Framework | App Router, API routes, SSR |
| **TypeScript** | Language | Type safety, better DX |
| **Vercel AI SDK** | LLM integration | Structured outputs, streaming |
| **Zod** | Validation | Runtime schemas, type inference |
| **TailwindCSS** | Styling | Utility-first, minimal overhead |
| **Anthropic Claude** | LLM (primary) | Best for structured outputs |
| **OpenAI GPT** | LLM (alternative) | Wide availability |

---

## 📊 Architecture Diagram

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ User types question
       ▼
┌─────────────┐
│ ChatInterface│  (React Client Component)
└──────┬──────┘
       │ POST /api/chat
       ▼
┌─────────────┐
│  API Route  │  (Next.js API Handler)
└──────┬──────┘
       │ Validate with Zod
       ▼
┌─────────────┐
│  AI Client  │  (lib/ai/client.ts)
└──────┬──────┘
       │ generateObject()
       ▼
┌─────────────┐
│ Claude/GPT  │  (LLM Provider)
└──────┬──────┘
       │ JSON matching schema
       ▼
┌─────────────┐
│ SupportAnswer│  (Validated, Type-Safe)
└──────┬──────┘
       │ Render in UI
       ▼
┌─────────────┐
│  User sees  │
│  response   │
└─────────────┘
```

**Full diagrams**: See `docs/visuals/diagrams.md`

---

## ✨ What Makes This Special?

### 1. Educational First

**Not just code**:
- Every file has extensive comments
- Concepts explained inline
- "Why" documented, not just "what"
- Learning checkpoints throughout

### 2. Production Patterns

**Real-world architecture**:
- Proper error handling
- Type safety throughout
- Observability built-in
- Security best practices

### 3. Progressive Complexity

**Layered design**:
```
Layer 0: Structured outputs only
    ↓
Layer 1: + Observability
    ↓
Layer 2: + RAG knowledge base
    ↓
Layer 3: + Conversation memory
```

Each layer builds on the previous without breaking it.

### 4. Hands-On Learning

**12 experiments** ranging from:
- ⭐ Easy: Add a new schema field
- ⭐⭐ Medium: Modify UI conditionally
- ⭐⭐⭐ Advanced: Debug mode with query params

---

## 🎓 Learning Outcomes

After completing Layer 0, you can:

✅ Design Zod schemas for structured LLM outputs
✅ Write effective system prompts
✅ Use Vercel AI SDK `generateObject()`
✅ Implement type-safe API routes
✅ Build accessible React UIs
✅ Handle errors gracefully
✅ Debug TypeScript type errors
✅ Trace requests end-to-end
✅ Explain architectural trade-offs
✅ Extend the system with new features

**Validation**: Take the quiz in QUIZ.md

---

## 🔗 External Resources

- [Vercel AI SDK Documentation](https://sdk.vercel.ai/docs)
- [Zod Documentation](https://zod.dev)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Next.js App Router Guide](https://nextjs.org/docs/app)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

---

## 🤝 Contributing to Your Learning

### Suggested Exercises

1. Add a new category (e.g., "security", "sales")
2. Create a second schema for different use case
3. Implement response streaming (Vercel AI SDK)
4. Add markdown rendering for responses
5. Build a history panel (client-side storage)
6. Create A/B test for prompt variations

### Questions to Explore

- What happens if the LLM violates the schema?
- How does temperature affect response variety?
- Can you make the system bilingual?
- How would you add authentication?
- What's the optimal confidence threshold?

---

## 📝 Commands Reference

```bash
# Development
npm run dev              # Start dev server (localhost:3000)
npm run build            # Production build
npm run start            # Run production server

# Quality Checks
npm run lint             # Run ESLint
npm run type-check       # TypeScript validation

# Visualization
npm run ascii-flow       # Print ASCII flowchart

# Testing (manual)
# 1. Visit http://localhost:3000
# 2. Ask questions
# 3. Check http://localhost:3000/debug
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No AI provider configured" | Check `.env` file has API key |
| Type errors | Run `npm run type-check` |
| Port 3000 in use | Use `PORT=3001 npm run dev` |
| Validation errors | Check schema constraints |
| Slow responses | Try faster model (Sonnet, GPT-3.5) |

**Full troubleshooting**: See [SETUP.md](./SETUP.md#troubleshooting)

---

## 🗓️ Roadmap

### Layer 0 (Current) ✅
- Structured outputs
- Basic prompt engineering
- Type-safe API
- React UI

### Layer 1 (Next)
- Logfire observability
- Trace visualization
- Performance monitoring
- Production debugging

### Layer 2
- RAG knowledge base
- Document ingestion
- Semantic search
- Citation accuracy

### Layer 3
- Conversation memory
- Multi-turn reasoning
- Context management
- Session persistence

---

## 📄 License

This is a learning project. Feel free to:
- Study the code
- Modify for your use case
- Share with others
- Build upon it

---

## 🎉 Get Started

```bash
# Clone or download this project
# Then:

npm install
cp .env.example .env
# Edit .env with your API key
npm run dev

# Open http://localhost:3000
# Start learning! 🚀
```

---

## 💡 Pro Tips

1. **Read code first**: Don't skim, study it
2. **Break things**: Best way to learn
3. **Complete experiments**: Hands-on beats theory
4. **Use debug mode**: Visit `/debug` frequently
5. **Take the quiz**: Validates your understanding

---

## 📬 Next Steps

After completing Layer 0:

1. ✅ Finish all 12 experiments
2. ✅ Take QUIZ.md (aim for 80%+)
3. ✅ Build a custom feature
4. 🚀 Proceed to Layer 1 (Observability)

---

**Happy Learning!** 🎓

Built with ❤️ for developers learning LLM application development

---

*Questions? Check `docs/` folder. Still stuck? Review `experiments/` hands-on exercises.*
