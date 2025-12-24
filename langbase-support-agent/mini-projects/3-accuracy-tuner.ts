/**
 * MINI-PROJECT 3: THE "ACCURACY TUNER"
 *
 * GOAL: Understand the precision vs. noise trade-off in retrieval
 *
 * LEARNING OBJECTIVES:
 * - See how top_k affects answer quality
 * - Understand when more context helps vs. hurts
 * - Learn to tune retrieval for different use cases
 *
 * THE TOP_K DILEMMA:
 * - Too low (k=1): Might miss important context → incomplete answers
 * - Too high (k=20): Too much noise → confused or verbose answers
 * - Sweet spot: Usually 3-5, but depends on your data!
 *
 * WHY THIS MATTERS:
 * - top_k directly affects answer quality AND cost
 * - More chunks = more tokens = higher API costs
 * - Finding the right balance is crucial for production
 *
 * TO RUN:
 *   tsx mini-projects/3-accuracy-tuner.ts
 */

import { Langbase } from 'langbase';
import * as dotenv from 'dotenv';

dotenv.config();

/**
 * Test different top_k values and compare results
 */
async function testTopKValues() {
  const apiKey = process.env.LANGBASE_API_KEY;
  if (!apiKey) {
    throw new Error('LANGBASE_API_KEY not found');
  }

  const langbase = new Langbase({ apiKey });
  const memoryName = process.env.MEMORY_NAME || 'support-faq-memory';

  console.log('\n🎯 ACCURACY TUNER EXPERIMENT\n');
  console.log('═'.repeat(70));
  console.log('Testing how top_k (number of retrieved chunks) affects answers\n');

  // Test with different questions
  const testCases = [
    {
      question: 'How do I upgrade my plan?',
      type: 'Specific question',
      expectedBehavior: 'Should work well with low top_k (answer is in one chunk)',
    },
    {
      question: 'Tell me about security and privacy.',
      type: 'Broad question',
      expectedBehavior: 'Needs higher top_k (info spread across multiple chunks)',
    },
    {
      question: 'What are the pricing options and can I get a refund?',
      type: 'Multi-part question',
      expectedBehavior: 'Needs moderate top_k (covers 2 topics)',
    },
  ];

  // Different top_k values to test
  const topKValues = [1, 3, 5, 10, 20];

  for (const testCase of testCases) {
    console.log('\n' + '═'.repeat(70));
    console.log(`📝 TEST CASE: ${testCase.type}`);
    console.log('═'.repeat(70));
    console.log(`\nQuestion: "${testCase.question}"`);
    console.log(`Expected: ${testCase.expectedBehavior}\n`);

    for (const topK of topKValues) {
      console.log('─'.repeat(70));
      console.log(`🔍 Testing with top_k = ${topK}`);
      console.log('─'.repeat(70));

      try {
        // STEP 1: Retrieve chunks with this top_k
        const retrieval = await langbase.memory.retrieve({
          memoryName: memoryName,
          query: testCase.question,
          topK: topK,
        });

        console.log(`\n📊 Retrieved ${retrieval.data.length} chunks:\n`);

        // Show chunk quality distribution
        const scores = retrieval.data
          .map((chunk: any) => chunk.score)
          .filter((score: number) => score !== undefined);

        if (scores.length > 0) {
          const avgScore = scores.reduce((a: number, b: number) => a + b, 0) / scores.length;
          const highQuality = scores.filter((s: number) => s > 0.7).length;
          const mediumQuality = scores.filter((s: number) => s > 0.5 && s <= 0.7).length;
          const lowQuality = scores.filter((s: number) => s <= 0.5).length;

          console.log(`   Quality Distribution:`);
          console.log(`   • 🟢 High relevance (>70%): ${highQuality} chunks`);
          console.log(`   • 🟡 Medium relevance (50-70%): ${mediumQuality} chunks`);
          console.log(`   • 🔴 Low relevance (<50%): ${lowQuality} chunks`);
          console.log(`   • 📈 Average similarity: ${(avgScore * 100).toFixed(1)}%\n`);

          // Calculate total tokens (rough estimate)
          const totalChars = retrieval.data.reduce(
            (sum: number, chunk: any) => sum + chunk.content.length,
            0
          );
          const estimatedTokens = Math.ceil(totalChars / 4); // Rough estimate: 1 token ≈ 4 chars

          console.log(`   📏 Context Size:`);
          console.log(`   • Total characters: ${totalChars}`);
          console.log(`   • Estimated tokens: ~${estimatedTokens}`);
          console.log(`   • Cost impact: ${topK}x chunks = ${topK}x retrieval cost\n`);

          // Analysis
          console.log(`   🔬 Analysis:`);
          if (topK === 1) {
            console.log(`   • Minimal context - might miss related info`);
            console.log(`   • Lowest cost`);
            console.log(`   • Best for: Very specific, single-fact questions`);
          } else if (topK <= 5) {
            console.log(`   • Balanced context - good for most questions`);
            console.log(`   • Moderate cost`);
            console.log(`   • Best for: Standard Q&A`);
          } else if (topK <= 10) {
            console.log(`   • Rich context - good for complex questions`);
            console.log(`   • Higher cost`);
            console.log(`   • Best for: Multi-part or broad questions`);
          } else {
            console.log(`   • Very rich context - potential noise`);
            console.log(`   • Highest cost`);
            console.log(`   • Best for: Research/exploration queries`);
            if (lowQuality > highQuality) {
              console.log(`   ⚠️  WARNING: More low-quality than high-quality chunks!`);
              console.log(`   ⚠️  This might confuse the LLM or add unnecessary cost`);
            }
          }
        }

        console.log('');

      } catch (error: any) {
        console.error(`   ❌ Error: ${error.message}\n`);
      }

      // Brief pause between requests
      await new Promise(resolve => setTimeout(resolve, 500));
    }

    console.log('\n');
  }

  // Summary and recommendations
  console.log('\n' + '═'.repeat(70));
  console.log('📊 SUMMARY & RECOMMENDATIONS\n');
  console.log('═'.repeat(70));

  console.log(`
┌─────────┬──────────────────────┬─────────────────────────────────┐
│  top_k  │     Use Case         │         Characteristics         │
├─────────┼──────────────────────┼─────────────────────────────────┤
│   1-2   │ Specific facts       │ • Fastest, cheapest             │
│         │ Simple Q&A           │ • Risk: Missing context         │
│         │                      │ • Good for: "What is X?"        │
├─────────┼──────────────────────┼─────────────────────────────────┤
│   3-5   │ Standard questions   │ • RECOMMENDED for most cases    │
│         │ Balanced coverage    │ • Good precision/recall balance │
│         │                      │ • Good for: "How do I...?"      │
├─────────┼──────────────────────┼─────────────────────────────────┤
│   5-10  │ Complex queries      │ • More comprehensive            │
│         │ Multi-part questions │ • Higher cost                   │
│         │                      │ • Good for: "Explain..." + "..."│
├─────────┼──────────────────────┼─────────────────────────────────┤
│  10-20  │ Research mode        │ • Maximum context               │
│         │ Exploratory queries  │ • Highest cost, slowest         │
│         │                      │ • Risk: Information overload    │
└─────────┴──────────────────────┴─────────────────────────────────┘
`);

  console.log('\n💡 KEY INSIGHTS:\n');
  console.log('1. PRECISION vs. RECALL Trade-off:');
  console.log('   • Low top_k: High precision (only most relevant) but might miss info');
  console.log('   • High top_k: High recall (catch everything) but includes noise\n');

  console.log('2. COST Implications:');
  console.log('   • Every chunk costs tokens (both retrieval and LLM processing)');
  console.log('   • top_k=20 can be 4-5x more expensive than top_k=4');
  console.log('   • For production, optimize for minimum effective top_k\n');

  console.log('3. ANSWER QUALITY:');
  console.log('   • More chunks ≠ better answers');
  console.log('   • Too much context can confuse the LLM');
  console.log('   • Watch for diminishing returns (scores drop significantly)\n');

  console.log('4. ADAPTIVE STRATEGIES:');
  console.log('   • Use similarity score thresholds (e.g., only use chunks >0.7)');
  console.log('   • Adjust top_k based on query complexity');
  console.log('   • Implement query classification (simple vs. complex)\n');

  console.log('\n🧪 EXPERIMENTS TO TRY:\n');
  console.log('1. Compare actual LLM answers (not just retrieval) for different top_k');
  console.log('2. Measure latency: How does top_k affect response time?');
  console.log('3. Cost analysis: Calculate actual token usage for different scenarios');
  console.log('4. Implement dynamic top_k based on query complexity');
  console.log('5. Add a similarity threshold filter (e.g., only chunks with score > 0.6)\n');

  console.log('🎯 NEXT STEPS:\n');
  console.log('1. Test YOUR specific use case with different top_k values');
  console.log('2. Monitor answer quality in production');
  console.log('3. A/B test different values with real users');
  console.log('4. Consider implementing adaptive retrieval strategies\n');
}

// Run the experiment
testTopKValues().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
