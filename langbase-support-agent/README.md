# Context-Aware Customer Support Agent 🤖

A **bottom-up learning project** for building AI agents with Langbase primitives. This project teaches you RAG (Retrieval Augmented Generation) from first principles, without "magic" frameworks.

## 🎯 Learning Philosophy

This project follows a **component-by-component** approach:

1. **Memory** (Data Layer) - Learn embeddings, chunking, and vector search
2. **Retrieval** (Logic Layer) - Understand semantic search and top_k tuning
3. **Pipe** (Cognition Layer) - Master prompts, model selection, and orchestration
4. **Mini-Projects** - Tinker with real scenarios to solidify understanding

**No black boxes.** Every step is explained with comments and rationale.

## 📋 Prerequisites

- Node.js 18+ and npm
- Langbase account ([sign up free](https://langbase.com))
- Basic TypeScript/JavaScript knowledge
- Curiosity about how AI agents actually work!

## 🚀 Quick Start

### 1. Clone and Install

```bash
cd langbase-support-agent
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Langbase API key:
```env
LANGBASE_API_KEY=your_api_key_here
```

Get your API key from: [https://langbase.com/settings](https://langbase.com/settings)

### 3. Build the Agent (Step-by-Step)

**Step 1: Create the Memory (Data Layer)**
```bash
npm run memory:create
```
This uploads FAQ.txt and creates vector embeddings. You'll see:
- How parsing works (text extraction)
- How chunking works (~500 tokens per chunk)
- How embeddings are generated (text → vectors)

**Step 2: Test Retrieval (Logic Layer)**
```bash
npm run retrieval:test
```
This queries the Memory WITHOUT the LLM. You'll see:
- Raw chunks retrieved for each question
- Similarity scores (0-1 scale)
- What context the LLM will actually receive

**Step 3: Create the Pipe (Cognition Layer)**
```bash
npm run pipe:create
```
This creates an AI agent with a system prompt. You'll see:
- How system prompts control behavior
- How Memory attaches to Pipes
- The full RAG pipeline in action

**Step 4: Run the Full Agent**
```bash
npm run dev
```
Interactive mode! Ask questions like:
- "How do I upgrade my plan?"
- "What are the system requirements?"
- "Is my data secure?"

Type `debug` to see retrieval details. Type `exit` to quit.

## 📚 Project Structure

```
langbase-support-agent/
├── src/
│   ├── 1-memory-creation.ts      # STEP 1: Memory primitive
│   ├── 2-retrieval-test.ts       # STEP 2: Retrieval testing
│   ├── 3-pipe-creation.ts        # STEP 3: Pipe primitive
│   └── main.ts                   # STEP 4: Full orchestration
├── data/
│   └── FAQ.txt                   # Sample knowledge base
├── mini-projects/                # Experiments for tinkering
│   ├── 1-personality-swap.ts     # Test different prompts
│   ├── 2-knowledge-injection.ts  # Add new documents
│   ├── 3-accuracy-tuner.ts       # Optimize top_k
│   └── 4-multi-format-challenge.ts # Test PDFs, CSVs, etc.
├── .env.example                  # Environment template
├── package.json                  # Dependencies & scripts
├── tsconfig.json                 # TypeScript config
└── README.md                     # This file
```

## 🧠 Understanding the Primitives

### Memory (Data Layer)

**What it does:**
- Stores documents in a vector database
- Converts text to embeddings (vectors that represent meaning)
- Enables semantic search (find by meaning, not keywords)

**Key concepts:**
- **Parsing**: Extracts text from files (.txt, .pdf, .docx, etc.)
- **Chunking**: Splits text into ~500 token pieces (LLMs have context limits)
- **Embedding**: Converts chunks to vectors using an embedding model
- **Indexing**: Stores vectors for fast similarity search

**When to use:**
- You have documentation, FAQs, or knowledge to query
- You want to search by meaning ("how to upgrade" matches "plan enhancement")
- You need to avoid retraining models when knowledge changes

### Pipe (Cognition Layer)

**What it does:**
- Defines the AI's personality and behavior (system prompt)
- Connects to a Memory for context (RAG)
- Calls the LLM with the right configuration

**Key concepts:**
- **System Prompt**: Instructions that define the agent's role and tone
- **Model**: Which LLM to use (GPT-4, GPT-3.5, Claude, etc.)
- **Temperature**: Creativity level (0=deterministic, 1=creative)
- **Memory Attachment**: Links Pipe to Memory for automatic RAG

**When to use:**
- You need consistent AI behavior (same prompt every time)
- You want to combine multiple data sources (attach multiple Memories)
- You need to A/B test different prompts or models

## 🎓 Learning Path

### Phase 1: Build Understanding (30 minutes)

1. Run each numbered script in order (`1-memory-creation.ts` → `2-retrieval-test.ts` → `3-pipe-creation.ts`)
2. Read the comments in each file carefully
3. Watch the console output to see what's happening under the hood

**Key questions to answer:**
- Where do chunks come from? (Answer: The chunking step in Memory creation)
- How does the LLM know what to say? (Answer: Retrieved chunks + system prompt)
- Why 500 token chunks? (Answer: Balance between context and precision)

### Phase 2: Tinker (1-2 hours)

Complete the mini-projects in order:

#### Mini-Project 1: Personality Swap
```bash
tsx mini-projects/1-personality-swap.ts
```
**Learn:** How prompts control style (facts stay the same)

#### Mini-Project 2: Knowledge Injection
```bash
tsx mini-projects/2-knowledge-injection.ts
```
**Learn:** How to update knowledge without code changes

#### Mini-Project 3: Accuracy Tuner
```bash
tsx mini-projects/3-accuracy-tuner.ts
```
**Learn:** The precision vs. noise trade-off in retrieval

#### Mini-Project 4: Multi-Format Challenge
```bash
tsx mini-projects/4-multi-format-challenge.ts
```
**Learn:** How different file formats are parsed and queried

### Phase 3: Experiment (Ongoing)

Try these challenges:

1. **Custom Knowledge Base**
   - Replace FAQ.txt with your own documentation
   - Could be: product docs, company policies, research papers, etc.

2. **Multi-Memory Agent**
   - Create a second Memory (e.g., "technical-docs")
   - Attach both to the same Pipe
   - See how retrieval searches across both

3. **Conversation History**
   - Modify `main.ts` to track previous messages
   - Add them to the `messages` array in pipe.run()
   - Test multi-turn conversations

4. **Advanced Prompting**
   - Add few-shot examples to the system prompt
   - Implement chain-of-thought reasoning
   - Add output formatting instructions (JSON, markdown, etc.)

5. **Production Optimization**
   - Add caching for common queries
   - Implement fallback responses for low-confidence retrievals
   - Add user feedback collection

## 🔬 How It Works: The RAG Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│                         USER QUESTION                             │
│                    "How do I upgrade?"                            │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                    STEP 1: EMBEDDING                              │
│  Convert question to vector: [0.23, -0.45, 0.78, ...]            │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                    STEP 2: RETRIEVAL                              │
│  Search Memory for chunks with similar vectors                   │
│  • Compute cosine similarity                                     │
│  • Rank by score                                                 │
│  • Return top-k (e.g., 4 chunks)                                 │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                    STEP 3: CONTEXT INJECTION                      │
│  Build prompt:                                                   │
│  • System prompt (persona)                                       │
│  • Retrieved chunks (context)                                    │
│  • User question                                                 │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                    STEP 4: LLM GENERATION                         │
│  Send full prompt to GPT-3.5                                     │
│  • Model reads context                                           │
│  • Follows system prompt instructions                            │
│  • Generates answer                                              │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                         FINAL ANSWER                              │
│  "To upgrade, go to Settings > Billing and click Upgrade..."    │
└──────────────────────────────────────────────────────────────────┘
```

## 🎛️ Configuration Reference

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LANGBASE_API_KEY` | Your Langbase API key | Required |
| `MEMORY_NAME` | Name for the Memory | `support-faq-memory` |
| `PIPE_NAME` | Name for the Pipe | `support-agent-pipe` |

### Memory Configuration

```typescript
await langbase.memory.create({
  name: 'my-memory',           // Unique identifier
  description: 'Knowledge base' // Human-readable description
});
```

### Retrieval Parameters

```typescript
await langbase.memory.retrieve({
  memoryName: 'my-memory',
  query: 'user question',
  topK: 4  // Number of chunks to retrieve
});
```

**top_k guidelines:**
- `1-2`: Simple factual questions
- `3-5`: **Recommended** for most use cases
- `5-10`: Complex or multi-part questions
- `10-20`: Research/exploratory queries (watch costs!)

### Pipe Configuration

```typescript
await langbase.pipe.create({
  name: 'my-pipe',
  systemPrompt: 'You are a...',  // Define persona
  model: 'gpt-3.5-turbo',        // LLM to use
  temperature: 0.3,              // 0=deterministic, 1=creative
  maxTokens: 500,                // Response length limit
  memory: { name: 'my-memory' }  // Attach Memory
});
```

**Model options:**
- `gpt-3.5-turbo`: Fast, cheap, good for simple tasks
- `gpt-4`: Best reasoning, more expensive
- `claude-2`: Great at following instructions

**Temperature guidelines:**
- `0.0-0.3`: Factual, consistent (support, Q&A)
- `0.4-0.7`: Balanced
- `0.7-1.0`: Creative, varied (content generation)

## 🐛 Troubleshooting

### "Memory already exists" error

The Memory name is already taken. Either:
1. Use a different `MEMORY_NAME` in `.env`
2. Delete the Memory from Langbase dashboard
3. Skip to the next step (if you just want to use it)

### "API key invalid" error

1. Check your `.env` file has the correct key
2. Verify the key at [langbase.com/settings](https://langbase.com/settings)
3. Make sure `.env` is in the project root (not `/src`)

### "No chunks retrieved" / Low similarity scores

The question might not match your knowledge base:
1. Try rephrasing the question
2. Check if the information exists in your documents
3. Try increasing `top_k` to cast a wider net
4. Add more relevant documents to the Memory

### Agent gives wrong answers

Debug the retrieval step:
1. Run in debug mode: type `debug` in interactive mode
2. Check which chunks are being retrieved
3. Verify the chunks contain the right information
4. If chunks are wrong → improve your documents or chunking
5. If chunks are right → improve your system prompt

## 📖 Further Learning

### Key Concepts to Understand

1. **Embeddings**: How text becomes vectors
   - Read: [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)

2. **Vector Databases**: How similarity search works
   - Read: [Vector DB Explained](https://www.pinecone.io/learn/vector-database/)

3. **Chunking Strategies**: How to split documents optimally
   - Experiment with different chunk sizes in your Memory

4. **Prompt Engineering**: How to write effective system prompts
   - Resource: [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)

### Advanced Topics

- **Hybrid Search**: Combine semantic + keyword search
- **Re-ranking**: Use a second model to re-rank retrieved chunks
- **Query Decomposition**: Break complex questions into sub-questions
- **Agentic RAG**: Let the agent decide when to retrieve vs. generate

## 🤝 Contributing

This is a learning project! Improvements are welcome:

1. Better system prompts
2. Additional mini-projects
3. More comprehensive FAQ examples
4. Performance optimizations
5. Better error handling

## 📄 License

ISC - Use freely for learning and commercial projects

## 🙏 Acknowledgments

Built with:
- [Langbase](https://langbase.com) - RAG infrastructure
- [TypeScript](https://www.typescriptlang.org/) - Type-safe JavaScript
- Educational approach inspired by bottom-up learning principles

---

## 🎯 Key Takeaways

After completing this project, you should understand:

✅ **Embeddings** - Text is converted to vectors that represent meaning
✅ **Chunking** - Documents are split to fit LLM context limits
✅ **Semantic Search** - Finding by meaning, not keywords
✅ **RAG Architecture** - How retrieval enhances generation
✅ **Prompt Engineering** - System prompts control behavior
✅ **Model Selection** - Different models for different tasks
✅ **top_k Tuning** - Precision vs. recall trade-offs
✅ **Cost Optimization** - More chunks ≠ better answers

**Most importantly:** You understand that there's no magic. Just well-orchestrated primitives!

---

Built with ❤️ for learners who want to understand, not just use, AI agents.
