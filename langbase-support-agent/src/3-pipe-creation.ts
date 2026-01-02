/**
 * STEP 3: PIPE CREATION - THE COGNITION LAYER
 *
 * This script creates a "Pipe" - Langbase's term for an AI Agent configuration.
 * A Pipe combines an LLM with a system prompt (persona) and optionally a Memory.
 *
 * KEY CONCEPTS:
 * - SYSTEM PROMPT: Instructions that define the AI's personality, role, and behavior
 *   This is where you control HOW the AI responds (tone, format, constraints)
 *
 * - MODEL SELECTION: Different LLMs have different strengths
 *   • GPT-4: Best reasoning, more expensive
 *   • GPT-3.5: Faster, cheaper, good for simple tasks
 *   • Claude: Great at following instructions and safety
 *
 * - TEMPERATURE: Controls randomness (0.0 = deterministic, 1.0 = creative)
 *   • 0.0-0.3: Factual, consistent (good for support)
 *   • 0.7-1.0: Creative, varied (good for content generation)
 *
 * - MEMORY ATTACHMENT: Links the Pipe to our FAQ Memory
 *   When a user asks a question, the Pipe will:
 *   1. Retrieve relevant chunks from Memory
 *   2. Inject them as context in the prompt
 *   3. Generate an answer based on that context
 *
 * WHY SEPARATE PIPE FROM MEMORY:
 * - You can have multiple Pipes using the same Memory (different personas)
 * - You can swap out the LLM model without re-uploading documents
 * - You can A/B test different system prompts
 */

import { Langbase } from 'langbase';
import * as dotenv from 'dotenv';

dotenv.config();

/**
 * Create an AI Agent Pipe with a specific persona
 */
async function createPipe() {
  const apiKey = process.env.LANGBASE_API_KEY;

  if (!apiKey) {
    throw new Error('LANGBASE_API_KEY not found in .env file');
  }

  const langbase = new Langbase({ apiKey });
  const pipeName = process.env.PIPE_NAME || 'support-agent-pipe';
  const memoryName = process.env.MEMORY_NAME || 'support-faq-memory';

  console.log('🤖 Creating AI Agent Pipe\n');
  console.log('═'.repeat(70));

  try {
    // STEP 3.1: Define the System Prompt
    // This is THE MOST IMPORTANT part of your agent's behavior
    // The prompt defines:
    // - Who the AI is (role/persona)
    // - What it should do
    // - How it should respond (tone, format, constraints)
    // - What it should NOT do (safety guardrails)

    const systemPrompt = `You are a helpful and professional customer support agent for ACME Software.

YOUR ROLE:
- Assist customers with questions about our product, billing, and technical issues
- Provide accurate information based on the knowledge base
- Be friendly, patient, and clear in your explanations

RESPONSE GUIDELINES:
1. **Use the Knowledge Base**: Always base your answers on the provided context from our FAQ
2. **Be Concise**: Provide clear, direct answers without unnecessary elaboration
3. **Be Helpful**: If the user's question isn't directly addressed, provide the closest relevant information
4. **Cite Sources**: When referencing specific policies or procedures, mention they're from our FAQ
5. **Admit Limitations**: If information isn't in the knowledge base, say so and suggest contacting support

TONE:
- Professional but warm
- Patient and understanding
- Avoid jargon unless necessary
- Use clear, simple language

CONSTRAINTS:
- Do NOT make up information not in the knowledge base
- Do NOT promise features or policies that aren't documented
- Do NOT provide medical, legal, or financial advice beyond our product's scope
- If a question is outside your knowledge, direct them to support@acme-software.com

FORMAT:
- Use bullet points for lists
- Use short paragraphs for readability
- Include specific details (prices, limits, URLs) when available
`;

    // STEP 3.2: Define Pipe Configuration
    const pipeConfig = {
      name: pipeName,
      description: 'Customer support agent with FAQ knowledge base',

      // System prompt defines the agent's persona
      systemPrompt: systemPrompt,

      // Model selection
      // Options: 'gpt-4', 'gpt-3.5-turbo', 'claude-2', etc.
      model: 'gpt-3.5-turbo',

      // Temperature controls creativity vs. consistency
      // 0.0 = Always gives same answer (deterministic)
      // 0.3 = Slight variation, mostly consistent (RECOMMENDED for support)
      // 0.7 = More creative and varied
      // 1.0 = Maximum creativity (use for content generation)
      temperature: 0.3,

      // Max tokens in the response
      // Prevents overly long answers and controls costs
      maxTokens: 500,

      // Attach the Memory we created earlier
      // This enables RAG (Retrieval Augmented Generation)
      memory: {
        name: memoryName,
      },
    };

    console.log('📋 Pipe Configuration:');
    console.log(`   Name: ${pipeConfig.name}`);
    console.log(`   Model: ${pipeConfig.model}`);
    console.log(`   Temperature: ${pipeConfig.temperature} (low = consistent)`);
    console.log(`   Max Tokens: ${pipeConfig.maxTokens}`);
    console.log(`   Memory Attached: ${memoryName}`);
    console.log('\n' + '─'.repeat(70));

    // STEP 3.3: Create the Pipe
    console.log('\n⚙️  Creating Pipe...\n');

    const pipe = await langbase.pipe.create(pipeConfig);

    console.log('✅ Pipe created successfully!');
    console.log(`   Pipe ID: ${pipe.name}`);
    console.log(`   Status: Ready to use\n`);

    // STEP 3.4: Test the Pipe with a sample query
    console.log('🧪 Testing the Pipe with a sample question...\n');
    console.log('─'.repeat(70));

    const testQuestion = 'How do I upgrade my plan?';
    console.log(`📝 Question: "${testQuestion}"\n`);

    // Run the pipe
    // This will:
    // 1. Retrieve relevant chunks from the Memory
    // 2. Inject them into the prompt as context
    // 3. Send the full prompt (system + context + question) to the LLM
    // 4. Return the generated answer

    const response = await langbase.pipe.run({
      name: pipeName,
      messages: [
        {
          role: 'user',
          content: testQuestion,
        },
      ],
    });

    console.log('🤖 Agent Response:');
    console.log('─'.repeat(70));
    console.log(response.completion);
    console.log('─'.repeat(70));

    // STEP 3.5: Show what happened under the hood
    console.log('\n🔍 What Just Happened:\n');
    console.log('1. ⚡ Your question was converted to a vector embedding');
    console.log('2. 🔍 Langbase searched the Memory for similar chunks');
    console.log(`3. 📦 Retrieved top-k most relevant chunks (typically 3-5)`);
    console.log('4. 📝 Chunks were injected into the prompt as context');
    console.log('5. 🤖 The LLM (GPT-3.5) generated an answer using that context');
    console.log('6. ✅ Response was returned to you\n');

    console.log('🎉 Success! Your AI Support Agent is fully operational.\n');

    console.log('💡 KEY INSIGHTS:\n');
    console.log('• The SYSTEM PROMPT controls personality and behavior');
    console.log('• The MEMORY provides factual knowledge');
    console.log('• The TEMPERATURE controls consistency vs. creativity');
    console.log('• The RETRIEVAL step happens automatically when Memory is attached\n');

    console.log('🔜 NEXT STEP: Run the full orchestration');
    console.log('   npm run dev\n');

  } catch (error: any) {
    console.error('❌ Error creating pipe:', error.message);

    if (error.message.includes('already exists')) {
      console.log('\n💡 TIP: Pipe already exists. You can either:');
      console.log('   1. Use a different PIPE_NAME in your .env file');
      console.log('   2. Delete the existing pipe from Langbase dashboard');
      console.log('   3. Skip to the next step: npm run dev\n');
    }

    throw error;
  }
}

// Run the script
createPipe().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
