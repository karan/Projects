/**
 * CONFIGURATION FILE
 *
 * Centralized configuration for easy customization.
 * Modify these values to tune your agent's behavior.
 */

import * as dotenv from 'dotenv';

dotenv.config();

export const config = {
  // API Configuration
  api: {
    key: process.env.LANGBASE_API_KEY || '',
  },

  // Memory Configuration
  memory: {
    name: process.env.MEMORY_NAME || 'support-faq-memory',
    description: 'Customer support FAQ knowledge base',

    // Retrieval settings
    retrieval: {
      // Number of chunks to retrieve for each query
      // TUNING GUIDE:
      // - 1-2: Simple factual questions (fastest, cheapest)
      // - 3-5: Recommended for most use cases (balanced)
      // - 5-10: Complex multi-part questions
      // - 10-20: Research/exploratory (slowest, most expensive)
      topK: 4,

      // Minimum similarity score threshold (0-1)
      // Chunks below this score will be filtered out
      // - 0.0: Accept all chunks (not recommended)
      // - 0.5: Accept moderately relevant chunks
      // - 0.7: Only accept highly relevant chunks (recommended)
      minScore: 0.0, // Set to 0.0 to disable filtering
    },
  },

  // Pipe Configuration
  pipe: {
    name: process.env.PIPE_NAME || 'support-agent-pipe',
    description: 'Customer support agent with FAQ knowledge',

    // Model selection
    // OPTIONS:
    // - 'gpt-3.5-turbo': Fast, cheap, good for most tasks
    // - 'gpt-4': Best reasoning, more expensive
    // - 'gpt-4-turbo': Balance of speed and capability
    // - 'claude-2': Excellent at following instructions
    model: 'gpt-3.5-turbo',

    // Temperature (0.0 - 1.0)
    // Controls randomness in responses
    // - 0.0: Deterministic, always same answer (boring but consistent)
    // - 0.3: Slight variation, mostly consistent (RECOMMENDED for support)
    // - 0.7: Creative and varied
    // - 1.0: Maximum creativity (unpredictable)
    temperature: 0.3,

    // Maximum tokens in response
    // Controls response length and cost
    // - 100: Very brief answers
    // - 300: Concise answers (good for chat)
    // - 500: Standard answers (RECOMMENDED)
    // - 1000+: Detailed explanations
    maxTokens: 500,

    // System prompt (defines agent persona and behavior)
    // This is where you customize the agent's personality!
    systemPrompt: `You are a helpful and professional customer support agent for ACME Software.

YOUR ROLE:
- Assist customers with questions about our product, billing, and technical issues
- Provide accurate information based on the knowledge base
- Be friendly, patient, and clear in your explanations

RESPONSE GUIDELINES:
1. **Use the Knowledge Base**: Always base your answers on the provided context
2. **Be Concise**: Provide clear, direct answers without unnecessary elaboration
3. **Be Helpful**: If the user's question isn't directly addressed, provide the closest relevant information
4. **Cite Sources**: When referencing specific policies, mention they're from our documentation
5. **Admit Limitations**: If information isn't in the knowledge base, say so and suggest contacting support

TONE:
- Professional but warm
- Patient and understanding
- Avoid jargon unless necessary
- Use clear, simple language

CONSTRAINTS:
- Do NOT make up information not in the knowledge base
- Do NOT promise features or policies that aren't documented
- If a question is outside your knowledge, direct them to support@acme-software.com

FORMAT:
- Use bullet points for lists
- Use short paragraphs for readability
- Include specific details (prices, limits, URLs) when available`,
  },

  // Application settings
  app: {
    // Enable debug mode by default
    debugMode: false,

    // Show retrieval details in responses
    showRetrievalDetails: false,

    // Enable conversation history (for multi-turn chat)
    enableHistory: false,
    maxHistoryLength: 10, // Number of previous messages to keep
  },
};

// Validation
export function validateConfig(): void {
  if (!config.api.key) {
    throw new Error(
      'LANGBASE_API_KEY not found. Please set it in your .env file.\n' +
      'Get your API key from: https://langbase.com/settings'
    );
  }

  if (config.memory.retrieval.topK < 1 || config.memory.retrieval.topK > 50) {
    console.warn('⚠️  Warning: top_k should be between 1 and 50. Current value:', config.memory.retrieval.topK);
  }

  if (config.pipe.temperature < 0 || config.pipe.temperature > 1) {
    throw new Error('Temperature must be between 0.0 and 1.0');
  }

  if (config.pipe.maxTokens < 1 || config.pipe.maxTokens > 4000) {
    console.warn('⚠️  Warning: maxTokens should be between 1 and 4000. Current value:', config.pipe.maxTokens);
  }
}

// Helper to print current configuration
export function printConfig(): void {
  console.log('\n📋 Current Configuration:\n');
  console.log('Memory:');
  console.log(`  Name: ${config.memory.name}`);
  console.log(`  Top K: ${config.memory.retrieval.topK}`);
  console.log(`  Min Score: ${config.memory.retrieval.minScore}`);
  console.log('\nPipe:');
  console.log(`  Name: ${config.pipe.name}`);
  console.log(`  Model: ${config.pipe.model}`);
  console.log(`  Temperature: ${config.pipe.temperature}`);
  console.log(`  Max Tokens: ${config.pipe.maxTokens}`);
  console.log('\nApp:');
  console.log(`  Debug Mode: ${config.app.debugMode}`);
  console.log(`  Show Retrieval: ${config.app.showRetrievalDetails}`);
  console.log(`  History Enabled: ${config.app.enableHistory}\n`);
}
