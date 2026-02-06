/**
 * STEP 2: RETRIEVAL TESTING - THE LOGIC LAYER
 *
 * This script demonstrates semantic search on the Memory we created.
 * We query the memory directly WITHOUT sending anything to an LLM yet.
 *
 * KEY CONCEPTS:
 * - SEMANTIC SEARCH: Unlike keyword search, this finds chunks by MEANING not exact words
 *   Example: "How do I upgrade?" will match "To upgrade your plan, navigate to..."
 *   even though the words are different
 *
 * - TOP_K: Number of most relevant chunks to retrieve
 *   • Too low (k=1): Might miss important context
 *   • Too high (k=20): Adds noise and costs more tokens
 *   • Sweet spot: Usually 3-5 chunks
 *
 * - SIMILARITY SCORE: Each chunk gets a score (0-1) showing how relevant it is
 *   • 0.8-1.0: Highly relevant
 *   • 0.6-0.8: Moderately relevant
 *   • Below 0.6: Probably not useful
 *
 * WHY WE TEST RETRIEVAL SEPARATELY:
 * - Verify our chunking strategy is working
 * - See what context the LLM will actually receive
 * - Debug if answers are wrong (maybe retrieval failed, not the LLM)
 * - Understand the trade-offs of different top_k values
 */

import { Langbase } from 'langbase';
import * as dotenv from 'dotenv';

dotenv.config();

/**
 * Test retrieval from Memory with a sample question
 */
async function testRetrieval() {
  const apiKey = process.env.LANGBASE_API_KEY;

  if (!apiKey) {
    throw new Error('LANGBASE_API_KEY not found in .env file');
  }

  const langbase = new Langbase({ apiKey });
  const memoryName = process.env.MEMORY_NAME || 'support-faq-memory';

  // STEP 2.1: Define test queries
  // These are sample customer questions to test our retrieval
  const testQueries = [
    {
      question: 'How do I upgrade my plan?',
      explanation: 'Testing if we can find billing/upgrade information',
    },
    {
      question: 'What are the system requirements?',
      explanation: 'Testing technical documentation retrieval',
    },
    {
      question: 'Is my data secure?',
      explanation: 'Testing security/privacy information retrieval',
    },
  ];

  console.log('🔍 Testing Semantic Retrieval\n');
  console.log('═'.repeat(70));

  // STEP 2.2: Test each query
  for (const { question, explanation } of testQueries) {
    console.log(`\n📝 Query: "${question}"`);
    console.log(`   Purpose: ${explanation}`);
    console.log('─'.repeat(70));

    try {
      // STEP 2.3: Perform semantic search
      // This converts the question to a vector embedding and finds
      // the most similar chunk embeddings in our Memory

      // TOP_K determines how many chunks to retrieve
      // Start with 3-5 for most use cases
      const topK = 4;

      console.log(`\n⚙️  Retrieval Config:`);
      console.log(`   • Memory: ${memoryName}`);
      console.log(`   • Top K: ${topK} chunks`);
      console.log(`   • Method: Semantic similarity (cosine distance)\n`);

      // Retrieve relevant documents
      const results = await langbase.memory.retrieve({
        memoryName: memoryName,
        query: question,
        topK: topK,
      });

      console.log(`✅ Retrieved ${results.data.length} chunks:\n`);

      // STEP 2.4: Display the retrieved chunks
      // This is the EXACT context that will be fed to the LLM
      results.data.forEach((chunk: any, index: number) => {
        console.log(`   📄 Chunk ${index + 1}:`);

        // Similarity score shows how relevant this chunk is
        if (chunk.score) {
          const scorePercent = (chunk.score * 100).toFixed(1);
          const relevance =
            chunk.score > 0.8
              ? '🟢 Highly Relevant'
              : chunk.score > 0.6
              ? '🟡 Moderately Relevant'
              : '🔴 Low Relevance';
          console.log(`   └─ Similarity: ${scorePercent}% ${relevance}`);
        }

        // Show a preview of the chunk content
        const preview = chunk.content.substring(0, 200);
        console.log(`   └─ Preview: "${preview}..."\n`);
      });

      // STEP 2.5: Analyze the results
      console.log('🔬 Analysis:');

      const highQualityChunks = results.data.filter(
        (chunk: any) => chunk.score && chunk.score > 0.7
      );

      if (highQualityChunks.length > 0) {
        console.log(`   ✅ Found ${highQualityChunks.length} high-quality matches`);
        console.log(`   ✅ Retrieval is working well for this query`);
      } else {
        console.log(`   ⚠️  No high-confidence matches found`);
        console.log(`   💡 This query might need:
          • More specific wording
          • Additional documents in the Memory
          • Lower similarity threshold`);
      }

      console.log('\n' + '═'.repeat(70));
    } catch (error: any) {
      console.error(`❌ Error retrieving for "${question}":`, error.message);
    }
  }

  // STEP 2.6: Experiment suggestions
  console.log('\n\n🧪 EXPERIMENTS TO TRY:\n');
  console.log('1. CHANGE TOP_K:');
  console.log('   • Set topK = 1 and see if answers are too narrow');
  console.log('   • Set topK = 10 and see if too much noise is retrieved\n');

  console.log('2. TEST EDGE CASES:');
  console.log('   • Ask a question NOT in the FAQ (e.g., "What is the meaning of life?")');
  console.log('   • See what chunks are returned when there\'s no good match\n');

  console.log('3. ANALYZE CHUNKING:');
  console.log('   • Look at chunk boundaries in the output');
  console.log('   • Verify that related information stays together\n');

  console.log('💡 KEY TAKEAWAY:');
  console.log('   This retrieval step is CRITICAL. If the right chunks aren\'t retrieved,');
  console.log('   the LLM can\'t generate accurate answers, no matter how good the prompt is.\n');

  console.log('🔜 NEXT STEP: Create the Pipe (AI Agent)');
  console.log('   npm run pipe:create\n');
}

// Run the script
testRetrieval().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
