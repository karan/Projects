/**
 * MAIN ORCHESTRATION - PUTTING IT ALL TOGETHER
 *
 * This is the production-ready entry point that combines all the primitives:
 * 1. Memory (Data Layer) - Stores and retrieves knowledge
 * 2. Pipe (Cognition Layer) - Generates intelligent responses
 *
 * THE RAG PIPELINE:
 * Query → Embedding → Retrieval → Context Injection → LLM → Response
 *
 * This file demonstrates:
 * - Clean separation of concerns
 * - Error handling
 * - Modular design (easy to swap components)
 * - Production-ready patterns
 */

import { Langbase } from 'langbase';
import * as dotenv from 'dotenv';
import * as readline from 'readline';

dotenv.config();

/**
 * Main support agent class
 * Encapsulates all the logic for running queries through the RAG pipeline
 */
class SupportAgent {
  private langbase: Langbase;
  private pipeName: string;
  private memoryName: string;

  constructor(apiKey: string, pipeName: string, memoryName: string) {
    this.langbase = new Langbase({ apiKey });
    this.pipeName = pipeName;
    this.memoryName = memoryName;
  }

  /**
   * Process a user query through the full RAG pipeline
   *
   * @param query - The user's question
   * @param showDebugInfo - Whether to show the retrieval details
   * @returns The AI-generated response
   */
  async answerQuery(query: string, showDebugInfo: boolean = false): Promise<string> {
    try {
      // OPTIONAL: Show retrieval details for debugging
      // This helps you understand what context the LLM is seeing
      if (showDebugInfo) {
        console.log('\n🔍 Debug: Retrieving context from Memory...');

        const retrievedChunks = await this.langbase.memory.retrieve({
          memoryName: this.memoryName,
          query: query,
          topK: 4,
        });

        console.log(`   Retrieved ${retrievedChunks.data.length} chunks:\n`);
        retrievedChunks.data.forEach((chunk: any, idx: number) => {
          const score = chunk.score ? (chunk.score * 100).toFixed(1) : 'N/A';
          console.log(`   ${idx + 1}. Similarity: ${score}%`);
          console.log(`      Preview: "${chunk.content.substring(0, 100)}..."\n`);
        });
      }

      // STEP 1: Run the query through the Pipe
      // Under the hood, this:
      // 1. Converts query to embedding
      // 2. Retrieves relevant chunks from Memory
      // 3. Injects chunks into the system prompt as context
      // 4. Sends full prompt to LLM
      // 5. Returns the generated response

      const response = await this.langbase.pipe.run({
        name: this.pipeName,
        messages: [
          {
            role: 'user',
            content: query,
          },
        ],
      });

      return response.completion;

    } catch (error: any) {
      throw new Error(`Failed to answer query: ${error.message}`);
    }
  }

  /**
   * Interactive CLI mode
   * Allows users to ask questions in a loop
   */
  async startInteractiveMode(): Promise<void> {
    console.log('\n🤖 ACME Support Agent - Interactive Mode\n');
    console.log('═'.repeat(70));
    console.log('Ask me anything about ACME Software!');
    console.log('Type "exit" to quit, "debug" to toggle debug mode\n');

    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    let debugMode = false;

    const askQuestion = () => {
      rl.question('You: ', async (input) => {
        const query = input.trim();

        // Handle special commands
        if (query.toLowerCase() === 'exit') {
          console.log('\n👋 Goodbye! Thanks for using ACME Support.\n');
          rl.close();
          return;
        }

        if (query.toLowerCase() === 'debug') {
          debugMode = !debugMode;
          console.log(`\n🔧 Debug mode: ${debugMode ? 'ON' : 'OFF'}\n`);
          askQuestion();
          return;
        }

        if (!query) {
          askQuestion();
          return;
        }

        try {
          // Process the query
          console.log('\n🤖 Agent: ');
          const answer = await this.answerQuery(query, debugMode);
          console.log(answer);
          console.log('\n' + '─'.repeat(70) + '\n');
        } catch (error: any) {
          console.error(`\n❌ Error: ${error.message}\n`);
        }

        askQuestion();
      });
    };

    askQuestion();
  }

  /**
   * Single query mode (for programmatic use)
   */
  async askSingle(query: string): Promise<void> {
    console.log('\n🤖 ACME Support Agent\n');
    console.log('═'.repeat(70));
    console.log(`\n📝 Question: ${query}\n`);
    console.log('─'.repeat(70));

    try {
      const answer = await this.answerQuery(query, true);
      console.log('\n🤖 Answer:');
      console.log(answer);
      console.log('\n' + '═'.repeat(70) + '\n');
    } catch (error: any) {
      console.error(`\n❌ Error: ${error.message}\n`);
      throw error;
    }
  }
}

/**
 * Main entry point
 */
async function main() {
  // Validate environment variables
  const apiKey = process.env.LANGBASE_API_KEY;
  if (!apiKey) {
    console.error('❌ Error: LANGBASE_API_KEY not found in environment variables');
    console.log('\n💡 Setup instructions:');
    console.log('   1. Copy .env.example to .env');
    console.log('   2. Add your Langbase API key');
    console.log('   3. Get your key from: https://langbase.com/settings\n');
    process.exit(1);
  }

  const pipeName = process.env.PIPE_NAME || 'support-agent-pipe';
  const memoryName = process.env.MEMORY_NAME || 'support-faq-memory';

  // Initialize the agent
  const agent = new SupportAgent(apiKey, pipeName, memoryName);

  // Check if a query was provided as command line argument
  const args = process.argv.slice(2);

  if (args.length > 0) {
    // Single query mode
    const query = args.join(' ');
    await agent.askSingle(query);
  } else {
    // Interactive mode
    await agent.startInteractiveMode();
  }
}

// Run the application
main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});

/**
 * USAGE EXAMPLES:
 *
 * 1. Interactive mode (chat with the agent):
 *    npm run dev
 *
 * 2. Single query mode:
 *    npm run dev "How do I upgrade my plan?"
 *
 * 3. Production build:
 *    npm run build
 *    node dist/main.js "What are the system requirements?"
 *
 * ARCHITECTURE OVERVIEW:
 *
 * ┌─────────────────────────────────────────────────────────────┐
 * │                        USER QUERY                            │
 * └─────────────────────┬───────────────────────────────────────┘
 *                       │
 *                       ▼
 * ┌─────────────────────────────────────────────────────────────┐
 * │                   MEMORY (Data Layer)                        │
 * │  • Convert query to embedding                                │
 * │  • Search vector database                                    │
 * │  • Retrieve top-k relevant chunks                            │
 * └─────────────────────┬───────────────────────────────────────┘
 *                       │
 *                       ▼
 * ┌─────────────────────────────────────────────────────────────┐
 * │                  PIPE (Cognition Layer)                      │
 * │  • Inject retrieved chunks as context                        │
 * │  • Apply system prompt (persona)                             │
 * │  • Send to LLM (GPT-3.5)                                     │
 * │  • Generate response                                         │
 * └─────────────────────┬───────────────────────────────────────┘
 *                       │
 *                       ▼
 * ┌─────────────────────────────────────────────────────────────┐
 * │                    FINAL ANSWER                              │
 * └─────────────────────────────────────────────────────────────┘
 *
 * KEY ADVANTAGES OF THIS ARCHITECTURE:
 *
 * 1. MODULARITY: Each component can be modified independently
 *    - Swap the LLM model without changing retrieval logic
 *    - Update the system prompt without re-uploading documents
 *    - Add new documents to Memory without touching the Pipe
 *
 * 2. TRANSPARENCY: You see exactly what's happening at each step
 *    - Debug mode shows retrieved chunks
 *    - Clear separation between data and logic
 *
 * 3. SCALABILITY: Easy to extend with new features
 *    - Add conversation history (multi-turn chat)
 *    - Implement caching for common queries
 *    - Add feedback loops for improvement
 *
 * 4. COST CONTROL: Only retrieve what you need
 *    - top_k limits context size
 *    - maxTokens caps response length
 *    - You pay only for what you use
 */
