# Support Agent - Layer 0: Foundation

> **Learning Project**: AI-powered support agent with structured outputs

## 🎯 Purpose

This project serves dual purposes:

1. **Working Application**: A functional AI support agent that provides helpful, structured responses
2. **Learning Resource**: A comprehensive example of LLM application development with production-grade patterns

## 🧠 Learning Approach

This project uses a **bottom-up learning methodology**:

- **Study first, understand second**: Read generated code to learn concepts
- **Experiment-driven**: 12 hands-on experiments reinforce each concept
- **Layered architecture**: Each layer builds on previous foundations
- **Production patterns**: Real-world code, not toy examples

## 📚 What You'll Learn

### Core Concepts (Layer 0)

1. **Structured Outputs**
   - Why LLMs need schema constraints
   - Using Zod for runtime validation
   - Type inference from schemas

2. **Prompt Engineering**
   - System prompt design
   - Role-based instruction
   - Self-assessment patterns

3. **API Design**
   - Request/response validation
   - Error handling strategies
   - Observability basics

4. **Type Safety**
   - TypeScript strict mode
   - No `any` types
   - Schema-driven development

5. **React Patterns**
   - Client/server component separation
   - Optimistic UI updates
   - Accessible forms

## 🗺️ Concept Map

```
                    ┌─────────────────┐
                    │  User Question  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Zod Validation │◄──── Input Schemas
                    │  (validation.ts)│
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   API Route     │
                    │ (app/api/chat)  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  AI SDK Client  │◄──── System Prompts
                    │   (client.ts)   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   LLM (Claude/  │
                    │      GPT)       │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ SupportAnswer   │◄──── Output Schema
                    │    Schema       │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  React UI       │
                    │  Components     │
                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn
- Anthropic API key OR OpenAI API key

### Setup (3 commands)

```bash
# 1. Install dependencies
npm install

# 2. Configure environment
cp .env.example .env
# Edit .env and add your API key

# 3. Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## 📖 Reading Order

Start here for maximum learning efficiency:

1. **lib/schemas/support-answer.ts** - Understand the core data structure
2. **lib/ai/prompts.ts** - See how we instruct the LLM
3. **lib/ai/client.ts** - Learn structured generation
4. **app/api/chat/route.ts** - Follow the request/response flow
5. **components/chat/ChatInterface.tsx** - See React integration

## 🧪 Experiments

See [experiments/README.md](../experiments/README.md) for 12 progressive experiments.

### Sample Experiment

**Experiment 1: Add a Sentiment Field**

```typescript
// In lib/schemas/support-answer.ts, add:
sentiment: z.enum(['positive', 'neutral', 'negative'])
  .describe('Detected user sentiment'),
```

**Expected**: The LLM automatically populates this field!
**Learn**: Schema changes propagate through the entire system.

## 🏗️ Architecture Overview

```
Layer 0: Foundation (YOU ARE HERE)
├── Structured outputs with Zod
├── Basic prompt engineering
├── Single-turn conversations
└── No memory, no RAG

Layer 1: Observability (Next)
├── Logfire integration
├── Trace visualization
├── Performance monitoring
└── Production debugging

Layer 2: Knowledge Base (RAG)
├── Document ingestion
├── Semantic search
├── Citation accuracy
└── Context injection

Layer 3: Conversation Memory
├── Message history
├── Context windows
├── Session management
└── Multi-turn reasoning
```

## 📁 Project Structure

```
support-agent/
├── app/                    # Next.js App Router
│   ├── api/chat/          # Chat API endpoint
│   ├── debug/             # Debug/introspection view
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Main chat page
├── lib/
│   ├── ai/                # AI SDK integration
│   │   ├── client.ts      # generateObject wrapper
│   │   ├── config.ts      # Model configuration
│   │   └── prompts.ts     # System prompts
│   ├── schemas/           # Zod schemas
│   │   ├── support-answer.ts  # Core output schema
│   │   ├── validation.ts      # Input validation
│   │   └── index.ts          # Exports
│   ├── types/             # TypeScript types
│   └── utils/             # Utilities
│       ├── error-handling.ts
│       └── logging.ts
├── components/
│   ├── chat/              # Chat UI components
│   └── debug/             # Debug components
├── docs/                  # Documentation
│   ├── README.md          # This file
│   ├── ARCHITECTURE.md    # Deep dive
│   ├── DATA_FLOW.md       # Request flow
│   ├── LEARNING_PATH.md   # Study guide
│   └── visuals/           # Diagrams
└── experiments/           # Learning experiments
```

## 🎓 Learning Path by Role

### For Beginners

1. Start with schema files to understand data structures
2. Read prompts to see how we "program" LLMs
3. Explore API routes to understand web APIs
4. Experiment with UI components

### For Experienced Developers

1. Review architectural decisions in `docs/ARCHITECTURE.md`
2. Study error handling patterns
3. Examine type safety implementation
4. Consider experiment variations

### For AI/ML Engineers

1. Focus on prompt engineering techniques
2. Study structured output mechanisms
3. Analyze confidence scoring patterns
4. Explore schema design trade-offs

## 🛠️ Available Commands

```bash
# Development
npm run dev              # Start dev server
npm run build           # Production build
npm run start           # Start production server

# Quality
npm run lint            # Run ESLint
npm run type-check      # TypeScript check

# Visualization
npm run ascii-flow      # Print ASCII flowchart
```

## 🔑 Key Design Decisions

1. **Zod over manual validation**: Automatic type inference
2. **Strict TypeScript**: Catch errors at compile time
3. **Stateless Layer 0**: Simplicity for learning
4. **Extensive comments**: Code as documentation
5. **Bottom-up learning**: Study by example

## 🐛 Debugging Tips

### Common Issues

**"No AI provider configured"**
- Check `.env` file exists (copy from `.env.example`)
- Verify API key is set

**Type errors**
- Run `npm run type-check`
- Ensure `strict: true` in `tsconfig.json`

**LLM returns invalid data**
- Check schema constraints in `support-answer.ts`
- Review prompt in `prompts.ts`
- Enable debug mode: `{ debug: true }` in API request

### Debug Mode

Visit `/debug` to inspect:
- Current schema structure
- Active configuration
- Example valid objects
- Validation results

## 📊 Success Metrics

You've mastered Layer 0 when you can:

- ✅ Explain why structured outputs matter
- ✅ Create a new Zod schema from scratch
- ✅ Modify system prompts effectively
- ✅ Trace a request through the full stack
- ✅ Add new fields to SupportAnswer
- ✅ Implement basic error handling

## 🔗 External Resources

- [Vercel AI SDK Docs](https://sdk.vercel.ai/docs)
- [Zod Documentation](https://zod.dev)
- [Anthropic Prompt Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Next.js App Router](https://nextjs.org/docs/app)

## 🤝 Contributing to Your Learning

### Suggested Exercises

1. Add a new category to `SUPPORT_CATEGORIES`
2. Create a second schema for "feedback" responses
3. Implement a "similarity score" for followup questions
4. Add markdown rendering to responses
5. Create a "history" panel (client-side only)

### Questions to Explore

- What happens if the LLM violates the schema?
- How does temperature affect confidence scores?
- Can you make the system bilingual?
- How would you add rate limiting?

## 📝 Next Steps

After mastering Layer 0:

1. **Layer 1**: Add Logfire observability
2. **Layer 2**: Implement RAG knowledge base
3. **Layer 3**: Add conversation memory
4. **Production**: Deploy to Vercel

Each layer builds on this foundation!

---

**Happy Learning!** 🚀

For questions or issues, review:
- `docs/ARCHITECTURE.md` for design rationale
- `docs/DATA_FLOW.md` for request tracing
- `docs/LEARNING_PATH.md` for structured curriculum
