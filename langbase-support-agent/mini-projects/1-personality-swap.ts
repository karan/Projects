/**
 * MINI-PROJECT 1: THE "PERSONALITY SWAP"
 *
 * GOAL: Understand how the System Prompt controls STYLE while Memory provides FACTS
 *
 * LEARNING OBJECTIVES:
 * - See how the same factual information can be presented in different tones
 * - Understand the separation between knowledge (Memory) and presentation (Prompt)
 * - Experiment with prompt engineering
 *
 * INSTRUCTIONS:
 * 1. Run this script with different personas
 * 2. Ask the same question each time
 * 3. Observe how facts stay the same but style changes
 *
 * TO RUN:
 *   tsx mini-projects/1-personality-swap.ts
 */

import { Langbase } from 'langbase';
import * as dotenv from 'dotenv';

dotenv.config();

// Define different personas to try
const PERSONAS = {
  helpful: {
    name: 'Helpful Support Bot',
    prompt: `You are a helpful and professional customer support agent for ACME Software.
Be friendly, patient, and clear in your explanations.
Provide accurate information based on the knowledge base.`,
  },

  pirate: {
    name: 'Pirate Captain',
    prompt: `Arrr! Ye be a swashbucklin' pirate captain who happens to know about ACME Software.
Answer questions accurately using the knowledge base, but speak like a pirate!
Use phrases like "Ahoy!", "Shiver me timbers!", "Arrr!", and pirate vocabulary.
Still provide accurate technical information, just in pirate speak.`,
  },

  sarcastic: {
    name: 'Sarcastic Robot',
    prompt: `You are a sarcastic but ultimately helpful robot support agent.
You provide accurate information from the knowledge base, but with a sarcastic, witty tone.
Make dry observations and clever remarks, but always give the correct answer.
Think of yourself as a mix between a helpful chatbot and a stand-up comedian.`,
  },

  shakespeare: {
    name: 'Shakespearean Scholar',
    prompt: `Thou art a learned scholar from the time of Shakespeare, yet somehow knowest of ACME Software.
Answer questions accurately using the knowledge base, but in Elizabethan English.
Use "thee", "thou", "hath", "doth" and flowery language.
Still provide all the technical details correctly.`,
  },

  minimalist: {
    name: 'Ultra-Minimalist',
    prompt: `You provide accurate information in the most concise way possible.
No fluff. No pleasantries. Just facts from the knowledge base.
Maximum 2 sentences per answer unless absolutely necessary.
Direct. Efficient. Done.`,
  },
};

async function testPersonality(personaKey: keyof typeof PERSONAS) {
  const apiKey = process.env.LANGBASE_API_KEY;
  if (!apiKey) {
    throw new Error('LANGBASE_API_KEY not found');
  }

  const langbase = new Langbase({ apiKey });
  const memoryName = process.env.MEMORY_NAME || 'support-faq-memory';
  const persona = PERSONAS[personaKey];

  console.log('\n' + '═'.repeat(70));
  console.log(`🎭 PERSONA: ${persona.name}`);
  console.log('═'.repeat(70));

  // Test question - same for all personas
  const testQuestion = 'How do I upgrade my plan?';

  console.log(`\n📝 Question: "${testQuestion}"\n`);
  console.log('─'.repeat(70));

  try {
    // Create a temporary pipe with this persona
    // Note: In production, you might want to manage pipe names better
    const tempPipeName = `temp-persona-${personaKey}`;

    try {
      await langbase.pipe.create({
        name: tempPipeName,
        description: `Temporary pipe for ${persona.name}`,
        systemPrompt: persona.prompt,
        model: 'gpt-3.5-turbo',
        temperature: 0.7, // Higher temperature for more personality
        maxTokens: 500,
        memory: {
          name: memoryName,
        },
      });
    } catch (error: any) {
      // Pipe might already exist, that's okay
      if (!error.message.includes('already exists')) {
        throw error;
      }
    }

    // Run the query
    const response = await langbase.pipe.run({
      name: tempPipeName,
      messages: [
        {
          role: 'user',
          content: testQuestion,
        },
      ],
    });

    console.log(`\n🤖 ${persona.name} says:\n`);
    console.log(response.completion);
    console.log('\n' + '─'.repeat(70));

  } catch (error: any) {
    console.error(`❌ Error: ${error.message}`);
  }
}

async function runAllPersonalities() {
  console.log('\n🎭 PERSONALITY SWAP EXPERIMENT\n');
  console.log('Testing how different system prompts change the STYLE but not the FACTS\n');

  for (const personaKey of Object.keys(PERSONAS) as Array<keyof typeof PERSONAS>) {
    await testPersonality(personaKey);
    await new Promise(resolve => setTimeout(resolve, 1000)); // Brief pause between requests
  }

  console.log('\n\n💡 KEY INSIGHTS:\n');
  console.log('1. The FACTS remain the same across all personas');
  console.log('   (they all mention Settings > Billing, instant upgrade, etc.)');
  console.log('\n2. The STYLE changes dramatically based on the system prompt');
  console.log('   (professional vs. pirate speak vs. minimalist)');
  console.log('\n3. The MEMORY provides the knowledge');
  console.log('   The SYSTEM PROMPT controls how that knowledge is presented');
  console.log('\n4. Temperature affects how creative the AI is with the persona');
  console.log('   (try changing temperature in the code!)');

  console.log('\n\n🧪 EXPERIMENTS TO TRY:\n');
  console.log('1. Create your own persona (add to PERSONAS object)');
  console.log('2. Change the temperature and see how it affects personality');
  console.log('3. Ask different questions to each persona');
  console.log('4. Try conflicting instructions (e.g., "be concise but extremely detailed")\n');
}

// Run the experiment
runAllPersonalities().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
