# 🚀 Quick Start Guide

**Goal:** Get your first AI agent running in 5 minutes!

## Prerequisites Check

```bash
node --version  # Should be v18 or higher
npm --version   # Any recent version
```

## Step-by-Step Setup

### 1️⃣ Install Dependencies (1 minute)

```bash
npm install
```

This installs:
- `langbase` - The Langbase SDK
- `typescript` - TypeScript compiler
- `tsx` - TypeScript executor
- `dotenv` - Environment variable loader

### 2️⃣ Get Your API Key (2 minutes)

1. Go to [https://langbase.com](https://langbase.com)
2. Sign up (free account)
3. Navigate to Settings → API Keys
4. Create a new API key
5. Copy it

### 3️⃣ Configure Environment (30 seconds)

```bash
cp .env.example .env
```

Edit `.env` and paste your API key:

```env
LANGBASE_API_KEY=your_actual_api_key_here
```

### 4️⃣ Build Your Agent (3 steps, ~2 minutes total)

**Step 1: Create Memory (Knowledge Base)**
```bash
npm run memory:create
```

You'll see:
- ✅ Memory created
- ✅ FAQ.txt uploaded
- ✅ Document processed (parsed, chunked, embedded)

**Step 2: Test Retrieval**
```bash
npm run retrieval:test
```

You'll see:
- 🔍 Sample questions
- 📄 Retrieved chunks
- 🔬 Similarity scores

**Step 3: Create Pipe (AI Agent)**
```bash
npm run pipe:create
```

You'll see:
- 🤖 Pipe created
- 🧪 Test query answered
- ✅ Agent ready!

### 5️⃣ Use Your Agent! 🎉

**Interactive Mode (Chat):**
```bash
npm run dev
```

Try asking:
- "How do I upgrade my plan?"
- "What are the system requirements?"
- "Is my data secure?"
- "What's your refund policy?"

**Single Query Mode:**
```bash
npm run dev "What payment methods do you accept?"
```

**Debug Mode:**
In interactive mode, type `debug` to see retrieval details.

## What You Just Built

```
┌─────────────────────────────────────────┐
│  FAQ.txt (Your Knowledge)               │
│  ↓ Parsed, Chunked, Embedded           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Memory (Vector Database)               │
│  • Stores semantic embeddings           │
│  • Enables similarity search            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Pipe (AI Agent)                        │
│  • Retrieves relevant chunks            │
│  • Generates answers with GPT-3.5       │
│  • Follows system prompt (persona)      │
└─────────────────────────────────────────┘
```

## Next Steps

### Learn the Fundamentals
Read the source code in order:
1. `src/1-memory-creation.ts` - Understand embeddings
2. `src/2-retrieval-test.ts` - Understand semantic search
3. `src/3-pipe-creation.ts` - Understand prompts and models
4. `src/main.ts` - Understand the full pipeline

### Tinker with Mini-Projects
1. **Personality Swap** - `tsx mini-projects/1-personality-swap.ts`
2. **Knowledge Injection** - `tsx mini-projects/2-knowledge-injection.ts`
3. **Accuracy Tuner** - `tsx mini-projects/3-accuracy-tuner.ts`
4. **Multi-Format** - `tsx mini-projects/4-multi-format-challenge.ts`

### Customize for Your Use Case
1. Replace `data/FAQ.txt` with your own documentation
2. Edit the system prompt in `3-pipe-creation.ts`
3. Adjust `top_k` in retrieval (experiment with values 1-10)
4. Try different models (gpt-4, claude-2)

## Troubleshooting

**"LANGBASE_API_KEY not found"**
→ Make sure `.env` file exists in project root (not in `src/`)

**"Memory already exists"**
→ Either delete it from Langbase dashboard or skip to next step

**"No chunks retrieved"**
→ Your question might not match the FAQ content. Try a different question.

**Agent gives generic answers**
→ Check retrieval: type `debug` to see what chunks are being used

## Need Help?

- 📚 Read the full [README.md](./README.md)
- 💬 Check Langbase docs: [https://langbase.com/docs](https://langbase.com/docs)
- 🐛 Found a bug? Open an issue

---

**Congratulations!** 🎉 You just built a RAG-powered AI agent from first principles!
