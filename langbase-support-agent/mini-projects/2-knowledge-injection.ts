/**
 * MINI-PROJECT 2: THE "KNOWLEDGE INJECTION"
 *
 * GOAL: Learn how to update the agent's knowledge without changing code
 *
 * LEARNING OBJECTIVES:
 * - Understand that Memory is separate from application logic
 * - See how RAG allows dynamic knowledge updates
 * - Practice adding new documents to an existing Memory
 *
 * INSTRUCTIONS:
 * 1. This script creates a new document (Recipe.txt) with fictional content
 * 2. Uploads it to your existing Memory
 * 3. Tests if the agent can answer questions about it
 *
 * WHY THIS MATTERS:
 * - In traditional chatbots, adding knowledge means retraining the model (expensive!)
 * - With RAG, you just upload a new document (instant, free!)
 * - The same Pipe can now answer questions about both FAQs and recipes
 *
 * TO RUN:
 *   tsx mini-projects/2-knowledge-injection.ts
 */

import { Langbase } from 'langbase';
import * as dotenv from 'dotenv';
import * as fs from 'fs';
import * as path from 'path';

dotenv.config();

// The fictional recipe content
const QUANTUM_SPAGHETTI_RECIPE = `
QUANTUM SPAGHETTI RECIPE

A revolutionary dish that exists in multiple states until observed by a hungry diner.

INGREDIENTS:
- 500g Quantum Entangled Pasta (available at specialty physics stores)
- 3 cups Schrödinger's Tomato Sauce (simultaneously ripe and unripe)
- 2 tablespoons Heisenberg Uncertainty Herbs (exact measurement is impossible)
- 1 cup Superposition Cheese (both grated and un-grated)
- 4 cloves Quantum Tunneling Garlic (it phases through the garlic press)
- 3 tablespoons Planck-Constant Olive Oil (smallest possible drizzle)
- Entangled Particle Seasoning (to taste, affects all dishes simultaneously)

SPECIAL EQUIPMENT:
- Quantum Oven (maintains all temperatures at once)
- Probability Wave Whisk
- Observation-Proof Cooking Pot (to preserve superposition)

COOKING INSTRUCTIONS:

1. PREPARATION PHASE:
   Place the Quantum Entangled Pasta in Observation-Proof Pot.
   Note: Do NOT look at the pasta or it will collapse into a single state.
   The pasta should remain in superposition (simultaneously cooked and uncooked).

2. SAUCE CREATION:
   - Heat Planck-Constant Olive Oil in the Quantum Oven at all temperatures simultaneously
   - Add Quantum Tunneling Garlic (it will appear inside the pan without you adding it)
   - Pour Schrödinger's Tomato Sauce (do not check if the tomatoes are ripe or it will collapse the wavefunction)
   - Stir with Probability Wave Whisk in both clockwise and counterclockwise directions
   - Simmer for exactly π minutes (3.14159... minutes)

3. ENTANGLEMENT PROCESS:
   - Combine pasta and sauce WITHOUT observing either
   - The act of combining will quantum-entangle them
   - They will now share the same quantum state forever
   - Any seasoning added to one will instantly affect the other

4. THE UNCERTAINTY PRINCIPLE:
   - Add Heisenberg Uncertainty Herbs
   - You can know how much you added OR where you added it, but not both
   - This creates interesting flavor variations across the dish

5. SUPERPOSITION CHEESE:
   - Sprinkle the Superposition Cheese on top
   - It will simultaneously melt and not melt until observed
   - Warning: Looking at it will force it to choose a state

6. FINAL SEASONING:
   - Add Entangled Particle Seasoning
   - This will simultaneously season all Quantum Spaghetti dishes being made anywhere in the universe
   - Call your friends - their pasta is now also seasoned!

SERVING INSTRUCTIONS:
- Serve in a covered dish
- The pasta exists in all possible states of doneness until the lid is lifted
- Warning: Opening the lid will collapse the wavefunction
- The pasta will suddenly decide whether it's al dente, overcooked, or undercooked
- Probability of perfect doneness: ~31.4% (π/10)

TASTING NOTES:
- Flavor profile exists in quantum superposition
- Diners will experience all possible flavors simultaneously until they take a bite
- Side effects may include:
  * Tasting tomorrow's dinner today
  * Feeling both full and hungry at the same time
  * Experiencing entanglement with other diners (you'll taste what they taste)

STORAGE:
- Store in Observation-Proof container
- Leftovers exist in all states of freshness simultaneously
- Will remain fresh until observed
- Do NOT open the container or the pasta will decide whether it's still good or spoiled

NUTRITIONAL INFORMATION:
Due to the Uncertainty Principle, we can know either the calories OR the nutritional content, but not both.
- Calories: Both 500 and 1500 kcal (depends on observation)
- Quantum Nutrition: Yes

PAIRING SUGGESTIONS:
- Pairs well with Entangled Wine (drink one glass, feel the effects of the entire bottle)
- Also complements Non-Euclidean Breadsticks (they have more than 2 ends)

DIFFICULTY LEVEL: Advanced Quantum Physics Degree Required

Enjoy your meal across all possible timelines!
`;

async function injectNewKnowledge() {
  const apiKey = process.env.LANGBASE_API_KEY;
  if (!apiKey) {
    throw new Error('LANGBASE_API_KEY not found');
  }

  const langbase = new Langbase({ apiKey });
  const memoryName = process.env.MEMORY_NAME || 'support-faq-memory';
  const pipeName = process.env.PIPE_NAME || 'support-agent-pipe';

  console.log('\n🧪 KNOWLEDGE INJECTION EXPERIMENT\n');
  console.log('═'.repeat(70));

  // STEP 1: Create the new recipe file
  console.log('\n📝 Step 1: Creating Quantum Spaghetti Recipe...\n');

  const recipePath = path.join(__dirname, '../data/Recipe.txt');
  fs.writeFileSync(recipePath, QUANTUM_SPAGHETTI_RECIPE);

  console.log('✅ Recipe file created at:', recipePath);

  // STEP 2: Upload to existing Memory
  console.log('\n📤 Step 2: Injecting new knowledge into Memory...\n');
  console.log(`   Memory: ${memoryName}`);
  console.log('   File: Recipe.txt');
  console.log('\n⚙️  Processing:');
  console.log('   • Parsing text from file');
  console.log('   • Chunking into semantic segments');
  console.log('   • Generating embeddings');
  console.log('   • Adding to existing vector database\n');

  try {
    const document = await langbase.memory.documents.create({
      memoryName: memoryName,
      file: fs.createReadStream(recipePath),
    });

    console.log('✅ Recipe uploaded successfully!');
    console.log(`   Document ID: ${document.name}`);
    console.log(`   Status: ${document.status}\n`);

  } catch (error: any) {
    console.error('❌ Error uploading recipe:', error.message);
    throw error;
  }

  // STEP 3: Verify Memory now has both documents
  console.log('─'.repeat(70));
  console.log('\n📊 Step 3: Verifying Memory contents...\n');

  const documents = await langbase.memory.documents.list({
    memoryName: memoryName,
  });

  console.log(`   Total Documents in Memory: ${documents.data.length}`);
  console.log('   Documents:');
  documents.data.forEach((doc: any, idx: number) => {
    console.log(`   ${idx + 1}. ${doc.name}`);
  });

  // STEP 4: Test the agent with questions about BOTH domains
  console.log('\n\n═'.repeat(70));
  console.log('🧪 Step 4: Testing Cross-Domain Knowledge\n');
  console.log('The SAME agent can now answer questions about BOTH:');
  console.log('  • ACME Software (original FAQ)');
  console.log('  • Quantum Spaghetti (newly added recipe)\n');
  console.log('═'.repeat(70));

  const testQuestions = [
    {
      question: 'What are the ingredients for Quantum Spaghetti?',
      domain: 'Recipe (NEW)',
    },
    {
      question: 'How long do I cook Quantum Spaghetti?',
      domain: 'Recipe (NEW)',
    },
    {
      question: 'How do I upgrade my ACME Software plan?',
      domain: 'Software FAQ (ORIGINAL)',
    },
    {
      question: 'What is Schrödinger\'s Tomato Sauce?',
      domain: 'Recipe (NEW)',
    },
  ];

  for (const { question, domain } of testQuestions) {
    console.log(`\n📝 Question [${domain}]:`);
    console.log(`   "${question}"\n`);
    console.log('─'.repeat(70));

    try {
      const response = await langbase.pipe.run({
        name: pipeName,
        messages: [
          {
            role: 'user',
            content: question,
          },
        ],
      });

      console.log('🤖 Answer:');
      console.log(response.completion);
      console.log('\n' + '─'.repeat(70));

    } catch (error: any) {
      console.error(`❌ Error: ${error.message}`);
    }

    // Brief pause between requests
    await new Promise(resolve => setTimeout(resolve, 1000));
  }

  // STEP 5: Show what happened
  console.log('\n\n💡 WHAT JUST HAPPENED:\n');
  console.log('1. We added a NEW document to the Memory');
  console.log('   • No code changes required');
  console.log('   • No model retraining required');
  console.log('   • Instant availability\n');

  console.log('2. The retrieval system now searches BOTH documents');
  console.log('   • Semantic search works across all content');
  console.log('   • Relevant chunks from ANY document can be retrieved\n');

  console.log('3. The SAME Pipe now has broader knowledge');
  console.log('   • No changes to the Pipe configuration');
  console.log('   • No changes to the system prompt');
  console.log('   • Memory attachment makes it automatic\n');

  console.log('4. This is the POWER of RAG:');
  console.log('   • Separate knowledge from logic');
  console.log('   • Update knowledge dynamically');
  console.log('   • Scale to thousands of documents');
  console.log('   • No retraining required!\n');

  console.log('\n🧪 EXPERIMENTS TO TRY:\n');
  console.log('1. Add a PDF or CSV file (test multi-format support)');
  console.log('2. Add a very large document (test chunking strategy)');
  console.log('3. Add conflicting information (test how retrieval prioritizes)');
  console.log('4. Create a second Memory for recipes (test multi-memory architecture)\n');
}

// Run the experiment
injectNewKnowledge().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
