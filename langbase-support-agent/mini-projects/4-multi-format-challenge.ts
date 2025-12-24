/**
 * MINI-PROJECT 4: THE "MULTI-FORMAT CHALLENGE"
 *
 * GOAL: Test Langbase's parsing capabilities with different file formats
 *
 * LEARNING OBJECTIVES:
 * - Understand that Langbase can parse PDFs, CSVs, DOCX, etc.
 * - Learn how structured data (CSV) differs from unstructured (TXT)
 * - See how the parsing layer handles different formats automatically
 *
 * WHY THIS MATTERS:
 * - Real-world knowledge comes in many formats
 * - Structured data (tables, spreadsheets) requires different handling
 * - Being able to query across formats is powerful
 *
 * TO RUN:
 *   tsx mini-projects/4-multi-format-challenge.ts
 */

import { Langbase } from 'langbase';
import * as dotenv from 'dotenv';
import * as fs from 'fs';
import * as path from 'path';

dotenv.config();

/**
 * Create sample files in different formats
 */
function createSampleFiles() {
  const dataDir = path.join(__dirname, '../data');

  // 1. Create a CSV with pricing data
  const pricingCSV = `Plan,Monthly Price,Annual Price,Storage,Projects,Users,Support,API Rate Limit
Free,0,0,10GB,5,1,Community,100/hour
Pro,29,290,500GB,50,10,Email (12h),1000/hour
Enterprise,Custom,Custom,Unlimited,Unlimited,Unlimited,24/7 Phone,10000/hour
Student,15,150,250GB,25,1,Email (24h),500/hour
Nonprofit,20,200,300GB,30,5,Email (24h),750/hour`;

  fs.writeFileSync(path.join(dataDir, 'pricing-table.csv'), pricingCSV);

  // 2. Create a structured text file with feature comparisons
  const featureComparison = `
ACME SOFTWARE - FEATURE COMPARISON

=== COLLABORATION FEATURES ===

Free Tier:
- Real-time collaboration: NO
- Comments: YES (up to 50/month)
- @mentions: NO
- Team workspaces: NO
- Guest access: NO
- Version history: 7 days

Pro Tier:
- Real-time collaboration: YES
- Comments: UNLIMITED
- @mentions: YES
- Team workspaces: YES (up to 5 workspaces)
- Guest access: YES (up to 10 guests)
- Version history: 90 days

Enterprise Tier:
- Real-time collaboration: YES
- Comments: UNLIMITED
- @mentions: YES
- Team workspaces: UNLIMITED
- Guest access: UNLIMITED
- Version history: UNLIMITED
- Advanced permissions: YES
- SSO/SAML: YES
- Audit logs: YES

=== INTEGRATION FEATURES ===

Free Tier:
- Basic integrations: 5 (Slack, Google Drive, Dropbox, GitHub, Zapier)
- Webhooks: NO
- API access: Read-only
- Custom integrations: NO

Pro Tier:
- Basic integrations: ALL (50+)
- Webhooks: YES (up to 10)
- API access: Full read/write
- Custom integrations: YES
- Zapier premium actions: YES

Enterprise Tier:
- Basic integrations: ALL (50+)
- Webhooks: UNLIMITED
- API access: Full read/write with higher limits
- Custom integrations: YES
- Dedicated API support: YES
- White-label API: YES

=== SECURITY FEATURES ===

All Tiers:
- SSL/TLS encryption: YES
- Data encryption at rest: YES (AES-256)
- 2FA: YES

Pro Tier adds:
- IP allowlisting: YES
- Session management: YES
- Activity logs: 90 days

Enterprise Tier adds:
- SSO/SAML: YES
- SCIM provisioning: YES
- Advanced encryption: YES
- Compliance certifications: SOC 2, GDPR, HIPAA
- Data residency options: YES
- Custom data retention: YES
- Activity logs: UNLIMITED
`;

  fs.writeFileSync(path.join(dataDir, 'feature-comparison.txt'), featureComparison);

  return {
    csv: path.join(dataDir, 'pricing-table.csv'),
    txt: path.join(dataDir, 'feature-comparison.txt'),
  };
}

async function testMultiFormatParsing() {
  const apiKey = process.env.LANGBASE_API_KEY;
  if (!apiKey) {
    throw new Error('LANGBASE_API_KEY not found');
  }

  const langbase = new Langbase({ apiKey });
  const memoryName = process.env.MEMORY_NAME || 'support-faq-memory';
  const pipeName = process.env.PIPE_NAME || 'support-agent-pipe';

  console.log('\n📄 MULTI-FORMAT CHALLENGE\n');
  console.log('═'.repeat(70));
  console.log('Testing how Langbase handles different file formats\n');

  // Create sample files
  console.log('📝 Step 1: Creating sample files...\n');
  const files = createSampleFiles();
  console.log('✅ Created:');
  console.log('   • pricing-table.csv (structured data)');
  console.log('   • feature-comparison.txt (semi-structured text)\n');

  // Upload each file
  console.log('─'.repeat(70));
  console.log('\n📤 Step 2: Uploading files to Memory...\n');

  const uploadedDocs = [];

  // Upload CSV
  try {
    console.log('⚙️  Uploading pricing-table.csv...');
    console.log('   • Format: CSV (Comma-Separated Values)');
    console.log('   • Structure: Tabular data with headers');
    console.log('   • Parsing: Langbase will preserve row/column relationships\n');

    const csvDoc = await langbase.memory.documents.create({
      memoryName: memoryName,
      file: fs.createReadStream(files.csv),
    });

    console.log('✅ CSV uploaded successfully');
    console.log(`   Document ID: ${csvDoc.name}\n`);
    uploadedDocs.push({ name: 'pricing-table.csv', id: csvDoc.name });

  } catch (error: any) {
    if (error.message.includes('already exists')) {
      console.log('⚠️  CSV already uploaded (skipping)\n');
    } else {
      console.error(`❌ Error uploading CSV: ${error.message}\n`);
    }
  }

  // Upload feature comparison
  try {
    console.log('⚙️  Uploading feature-comparison.txt...');
    console.log('   • Format: Plain text with markdown-like structure');
    console.log('   • Structure: Hierarchical sections and lists');
    console.log('   • Parsing: Langbase will maintain semantic structure\n');

    const txtDoc = await langbase.memory.documents.create({
      memoryName: memoryName,
      file: fs.createReadStream(files.txt),
    });

    console.log('✅ Text file uploaded successfully');
    console.log(`   Document ID: ${txtDoc.name}\n`);
    uploadedDocs.push({ name: 'feature-comparison.txt', id: txtDoc.name });

  } catch (error: any) {
    if (error.message.includes('already exists')) {
      console.log('⚠️  Text file already uploaded (skipping)\n');
    } else {
      console.error(`❌ Error uploading text: ${error.message}\n`);
    }
  }

  // Test queries against different formats
  console.log('─'.repeat(70));
  console.log('\n🧪 Step 3: Testing queries across formats...\n');
  console.log('═'.repeat(70));

  const testQueries = [
    {
      question: 'What is the price for the Enterprise tier?',
      expectedSource: 'pricing-table.csv',
      testingFor: 'Numeric data extraction from CSV',
    },
    {
      question: 'How many projects can I have on the Pro plan?',
      expectedSource: 'pricing-table.csv',
      testingFor: 'Specific column lookup in CSV',
    },
    {
      question: 'Does the Free tier have real-time collaboration?',
      expectedSource: 'feature-comparison.txt',
      testingFor: 'Boolean feature lookup in structured text',
    },
    {
      question: 'What security features are available in Enterprise?',
      expectedSource: 'feature-comparison.txt',
      testingFor: 'List extraction from hierarchical text',
    },
    {
      question: 'Compare the API rate limits across all plans',
      expectedSource: 'pricing-table.csv',
      testingFor: 'Cross-row comparison in CSV',
    },
    {
      question: 'What compliance certifications does Enterprise have?',
      expectedSource: 'feature-comparison.txt',
      testingFor: 'Specific detail extraction from nested structure',
    },
  ];

  for (const { question, expectedSource, testingFor } of testQueries) {
    console.log(`\n📝 Question: "${question}"`);
    console.log(`   Testing: ${testingFor}`);
    console.log(`   Expected source: ${expectedSource}\n`);
    console.log('─'.repeat(70));

    try {
      // First, show what chunks are retrieved
      const retrieval = await langbase.memory.retrieve({
        memoryName: memoryName,
        query: question,
        topK: 3,
      });

      console.log(`\n🔍 Retrieved ${retrieval.data.length} chunks:\n`);
      retrieval.data.forEach((chunk: any, idx: number) => {
        const score = chunk.score ? (chunk.score * 100).toFixed(1) : 'N/A';
        console.log(`   ${idx + 1}. Similarity: ${score}%`);
        console.log(`      Content preview: "${chunk.content.substring(0, 150)}..."\n`);
      });

      // Then get the LLM answer
      const response = await langbase.pipe.run({
        name: pipeName,
        messages: [
          {
            role: 'user',
            content: question,
          },
        ],
      });

      console.log('🤖 Agent Answer:');
      console.log('─'.repeat(70));
      console.log(response.completion);
      console.log('─'.repeat(70));

    } catch (error: any) {
      console.error(`❌ Error: ${error.message}`);
    }

    console.log('\n' + '═'.repeat(70));

    // Brief pause
    await new Promise(resolve => setTimeout(resolve, 1500));
  }

  // Summary
  console.log('\n\n💡 KEY INSIGHTS:\n');
  console.log('═'.repeat(70));

  console.log('\n1. AUTOMATIC PARSING:');
  console.log('   • Langbase automatically detects file format');
  console.log('   • No manual parsing code required');
  console.log('   • Handles: .txt, .pdf, .docx, .csv, .md, and more\n');

  console.log('2. STRUCTURED vs. UNSTRUCTURED:');
  console.log('   • CSV: Preserves tabular structure in chunks');
  console.log('   • Text: Chunks by semantic meaning');
  console.log('   • Both: Searchable by similarity\n');

  console.log('3. CROSS-FORMAT QUERIES:');
  console.log('   • Same retrieval mechanism works for all formats');
  console.log('   • LLM can synthesize info from different sources');
  console.log('   • No need to know which file contains what\n');

  console.log('4. CHUNKING STRATEGY:');
  console.log('   • CSV: Often chunks by rows (preserving column context)');
  console.log('   • Text: Chunks by paragraphs/sections');
  console.log('   • Goal: Keep related info together\n');

  console.log('\n🧪 EXPERIMENTS TO TRY:\n');
  console.log('1. Upload a PDF document (test binary format parsing)');
  console.log('2. Upload a large CSV (>1000 rows) and test specific lookups');
  console.log('3. Upload a DOCX with tables and images (test complex parsing)');
  console.log('4. Upload code files (.py, .js) and ask about functions');
  console.log('5. Mix formats and ask questions that require info from multiple files\n');

  console.log('💪 ADVANCED CHALLENGES:\n');
  console.log('1. Upload financial data (CSV) and ask for calculations');
  console.log('2. Upload a multi-page PDF contract and query specific clauses');
  console.log('3. Upload meeting notes (DOCX) and extract action items');
  console.log('4. Compare information across different file formats\n');

  console.log('📚 SUPPORTED FORMATS (check Langbase docs for full list):');
  console.log('   • Text: .txt, .md, .json');
  console.log('   • Documents: .pdf, .docx, .pptx');
  console.log('   • Data: .csv, .xlsx, .tsv');
  console.log('   • Code: .py, .js, .java, .cpp (and more)\n');
}

// Run the experiment
testMultiFormatParsing().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
