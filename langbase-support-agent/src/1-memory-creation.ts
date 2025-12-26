/**
 * STEP 1: MEMORY CREATION - THE DATA LAYER
 *
 * This script demonstrates the "Memory" primitive in Langbase.
 * Memory is where we store and index our knowledge base for semantic search.
 *
 * KEY CONCEPTS:
 * - PARSING: Langbase automatically extracts text from various file formats (.txt, .pdf, .docx, etc.)
 * - CHUNKING: Long documents are split into smaller pieces (chunks) to fit within LLM context limits
 *   Default chunk size is ~500 tokens with 50 token overlap to preserve context across boundaries
 * - EMBEDDING: Each chunk is converted to a vector (array of numbers) that represents its semantic meaning
 *   This allows us to find relevant chunks using similarity search rather than keyword matching
 * - INDEXING: Vectors are stored in a vector database for fast retrieval
 *
 * WHY WE DO THIS:
 * - LLMs have context limits (e.g., 8K, 32K, 100K tokens)
 * - We can't feed entire documentation into every request
 * - Semantic search retrieves only the RELEVANT chunks for each user question
 * - This is the foundation of RAG (Retrieval Augmented Generation)
 */

import { Langbase } from 'langbase';
import * as dotenv from 'dotenv';
import * as path from 'path';
import * as fs from 'fs';

// Load environment variables from .env file
dotenv.config();

/**
 * Main function to create and populate a Memory
 */
async function createMemory() {
  // STEP 1.1: Initialize the Langbase SDK
  // The API key authenticates our requests to Langbase
  const apiKey = process.env.LANGBASE_API_KEY;

  if (!apiKey) {
    throw new Error(
      'LANGBASE_API_KEY not found in environment variables. ' +
      'Please copy .env.example to .env and add your API key.'
    );
  }

  const langbase = new Langbase({ apiKey });

  // STEP 1.2: Define Memory configuration
  // The memory name should be unique and descriptive
  const memoryName = process.env.MEMORY_NAME || 'support-faq-memory';

  console.log('🧠 Creating Memory (Knowledge Base)...\n');
  console.log(`Memory Name: ${memoryName}`);
  console.log('─'.repeat(50));

  try {
    // STEP 1.3: Create the Memory
    // This creates an empty container for our documents
    // Under the hood, Langbase sets up:
    // - A vector database to store embeddings
    // - Text preprocessing pipelines
    // - Chunking configuration

    const memory = await langbase.memory.create({
      name: memoryName,
      description: 'Customer support FAQ knowledge base for ACME Software',
    });

    console.log('✅ Memory created successfully!');
    console.log(`   ID: ${memory.name}`);
    console.log(`   Description: ${memory.description}\n`);

    // STEP 1.4: Upload documents to the Memory
    // This is where the PARSING → CHUNKING → EMBEDDING pipeline runs

    const faqPath = path.join(__dirname, '../data/FAQ.txt');

    // Verify the file exists
    if (!fs.existsSync(faqPath)) {
      throw new Error(`FAQ file not found at: ${faqPath}`);
    }

    console.log('📄 Uploading document to Memory...');
    console.log(`   File: FAQ.txt`);
    console.log('─'.repeat(50));
    console.log('⚙️  Processing pipeline:');
    console.log('   1. PARSING: Extracting text from file');
    console.log('   2. CHUNKING: Splitting into ~500 token chunks');
    console.log('   3. EMBEDDING: Converting chunks to vectors');
    console.log('   4. INDEXING: Storing in vector database\n');

    // Upload the file
    // Langbase will automatically:
    // 1. Parse the .txt file
    // 2. Split it into semantic chunks
    // 3. Generate embeddings for each chunk using an embedding model
    // 4. Store the embeddings in the vector database
    const document = await langbase.memory.documents.create({
      memoryName: memoryName,
      file: fs.createReadStream(faqPath),
    });

    console.log('✅ Document uploaded and processed!');
    console.log(`   Document ID: ${document.name}`);
    console.log(`   Status: ${document.status}`);

    // STEP 1.5: Verify the Memory is ready
    console.log('\n' + '─'.repeat(50));
    console.log('📊 Memory Statistics:');

    // List all documents in the memory
    const documents = await langbase.memory.documents.list({
      memoryName: memoryName,
    });

    console.log(`   Total Documents: ${documents.data.length}`);
    console.log(`   Memory is ready for retrieval!\n`);

    console.log('🎉 Success! Your Memory is now populated and ready to use.');
    console.log('\n💡 WHAT JUST HAPPENED:');
    console.log('   • Your FAQ.txt was parsed and split into chunks');
    console.log('   • Each chunk was converted to a vector embedding');
    console.log('   • These embeddings are now searchable by semantic meaning');
    console.log('   • When a user asks a question, we\'ll find the most relevant chunks\n');

    console.log('🔜 NEXT STEP: Run the retrieval test script');
    console.log('   npm run retrieval:test\n');

  } catch (error: any) {
    console.error('❌ Error creating memory:', error.message);

    // Helpful error messages for common issues
    if (error.message.includes('already exists')) {
      console.log('\n💡 TIP: Memory already exists. You can either:');
      console.log('   1. Use a different MEMORY_NAME in your .env file');
      console.log('   2. Delete the existing memory from Langbase dashboard');
      console.log('   3. Skip to the next step: npm run retrieval:test\n');
    } else if (error.message.includes('unauthorized') || error.message.includes('API key')) {
      console.log('\n💡 TIP: Check your LANGBASE_API_KEY in .env file');
      console.log('   Get your API key from: https://langbase.com/settings\n');
    }

    throw error;
  }
}

// Run the script
createMemory().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
