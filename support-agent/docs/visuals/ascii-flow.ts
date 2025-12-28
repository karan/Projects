/**
 * FILE: ascii-flow.ts
 * LAYER: 0 (Foundation)
 * PURPOSE: Print ASCII flowchart for visual learners
 *
 * USAGE: npm run ascii-flow
 */

const COLORS = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  blue: '\x1b[34m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m',
  magenta: '\x1b[35m',
};

function printBox(title: string, width: number = 60): void {
  const padding = Math.max(0, Math.floor((width - title.length - 2) / 2));
  const line = '═'.repeat(width);
  const paddedTitle = ' '.repeat(padding) + title + ' '.repeat(padding);

  console.log(`╔${line}╗`);
  console.log(`║${paddedTitle}║`);
  console.log(`╚${line}╝`);
}

function printSection(title: string, content: string[]): void {
  console.log(`\n${COLORS.bright}${COLORS.cyan}${title}${COLORS.reset}`);
  console.log('─'.repeat(60));
  content.forEach(line => console.log(line));
}

function printFlow(): void {
  console.clear();

  printBox('SUPPORT AGENT - LAYER 0 DATA FLOW');

  printSection('1. USER INPUT', [
    '',
    '  [User types in browser]',
    '       │',
    '       ├─ Input validation (client-side)',
    '       ├─ Optimistic UI update',
    '       │',
    '       ▼',
    '  POST /api/chat',
    '  {',
    '    "message": "How do I get a refund?"',
    '  }',
    '',
  ]);

  printSection('2. API ROUTE VALIDATION', [
    '',
    '  app/api/chat/route.ts',
    '       │',
    '       ▼',
    '  ┌─────────────────────┐',
    '  │  Parse JSON Body    │',
    '  └──────────┬──────────┘',
    '             │',
    '             ▼',
    '  ┌─────────────────────┐      ╔═══════════════════╗',
    '  │ ChatRequestSchema   │ ◄────║ Zod Validation    ║',
    '  │ .safeParse()        │      ║ lib/schemas/      ║',
    '  └──────────┬──────────┘      ║ validation.ts     ║',
    '             │                 ╚═══════════════════╝',
    '             │',
    '        ┌────┴────┐',
    '        │         │',
    '    [Valid]   [Invalid]',
    '        │         │',
    '        │         └──► Return 400 Bad Request',
    '        │',
    '        ▼',
    '',
  ]);

  printSection('3. AI GENERATION', [
    '',
    '  lib/ai/client.ts',
    '       │',
    '       ├─ getModel() ──────────► lib/ai/config.ts',
    '       ├─ getSystemPrompt() ───► lib/ai/prompts.ts',
    '       │',
    '       ▼',
    '  ┌─────────────────────┐',
    '  │  generateObject()   │',
    '  │  ───────────────    │',
    '  │  • model: claude    │',
    '  │  • schema: Zod      │',
    '  │  • system: prompt   │',
    '  │  • prompt: message  │',
    '  └──────────┬──────────┘',
    '             │',
    '             ▼',
    '  ╔═══════════════════════════╗',
    '  ║  LLM (Claude/GPT)         ║',
    '  ║  ─────────────────         ║',
    '  ║  Generates JSON matching  ║',
    '  ║  SupportAnswerSchema      ║',
    '  ╚════════════┬══════════════╝',
    '               │',
    '               ▼',
    '',
  ]);

  printSection('4. SCHEMA VALIDATION', [
    '',
    '  AI SDK automatic validation',
    '       │',
    '       ▼',
    '  ┌─────────────────────┐      ╔═══════════════════╗',
    '  │ Parse JSON response │      ║ SupportAnswer     ║',
    '  └──────────┬──────────┘      ║ Schema            ║',
    '             │                 ║ lib/schemas/      ║',
    '             ▼                 ║ support-answer.ts ║',
    '  ┌─────────────────────┐      ╚═══════════════════╝',
    '  │ SupportAnswerSchema │ ◄────┘',
    '  │ .parse()            │',
    '  └──────────┬──────────┘',
    '             │',
    '        ┌────┴────┐',
    '        │         │',
    '    [Valid]   [Invalid]',
    '        │         │',
    '        │         └──► Throw ZodError ──► Return 500',
    '        │',
    '        ▼',
    '  ┌─────────────────────┐',
    '  │ Type-safe object!   │',
    '  │ SupportAnswer       │',
    '  └──────────┬──────────┘',
    '             │',
    '             ▼',
    '',
  ]);

  printSection('5. RESPONSE ENRICHMENT', [
    '',
    '  lib/ai/client.ts',
    '       │',
    '       ├─ Add metadata',
    '       │  • processing_time_ms',
    '       │  • model_used',
    '       │  • layer: "L0-basic"',
    '       │  • prompt_version',
    '       │',
    '       ▼',
    '  Return SupportAnswer object',
    '',
  ]);

  printSection('6. API RESPONSE', [
    '',
    '  app/api/chat/route.ts',
    '       │',
    '       ▼',
    '  ┌─────────────────────┐',
    '  │ Build response      │',
    '  │ envelope            │',
    '  └──────────┬──────────┘',
    '             │',
    '             ▼',
    '  Return 200 OK',
    '  {',
    '    "success": true,',
    '    "data": {',
    '      "final_answer": "...",',
    '      "confidence": 0.92,',
    '      "category": "billing",',
    '      "followups": [...],',
    '      "citations": [...],',
    '      "requires_human": false,',
    '      "metadata": {...}',
    '    },',
    '    "metadata": {',
    '      "request_id": "...",',
    '      "timestamp": "...",',
    '      "processing_time_ms": 1250',
    '    }',
    '  }',
    '',
  ]);

  printSection('7. UI RENDERING', [
    '',
    '  components/chat/ChatInterface.tsx',
    '       │',
    '       ├─ Parse response',
    '       ├─ Create Message object',
    '       ├─ Update state',
    '       │',
    '       ▼',
    '  React re-renders',
    '       │',
    '       ▼',
    '  components/chat/MessageBubble.tsx',
    '       │',
    '       ├─ Display final_answer',
    '       ├─ Show confidence bar',
    '       ├─ Render category badge',
    '       ├─ List followup questions',
    '       └─ Show citations',
    '       │',
    '       ▼',
    '  [User sees response]',
    '',
  ]);

  console.log(`\n${COLORS.bright}${COLORS.green}═══════════════════════════════════════════════════════════${COLORS.reset}\n`);
}

function printTypeSafety(): void {
  console.log(`\n${COLORS.bright}${COLORS.yellow}TYPE SAFETY GUARANTEES${COLORS.reset}`);
  console.log('─'.repeat(60));
  console.log('');
  console.log('  ┌─────────────────────────────────────────────────┐');
  console.log('  │ 1. Runtime Validation (Zod)                     │');
  console.log('  │    ✓ Input validation                           │');
  console.log('  │    ✓ Output validation                          │');
  console.log('  │    ✓ Detailed error messages                    │');
  console.log('  └─────────────────────────────────────────────────┘');
  console.log('');
  console.log('  ┌─────────────────────────────────────────────────┐');
  console.log('  │ 2. Compile-Time Validation (TypeScript)         │');
  console.log('  │    ✓ Type inference from schemas                │');
  console.log('  │    ✓ No manual type definitions                 │');
  console.log('  │    ✓ Catches errors before runtime              │');
  console.log('  └─────────────────────────────────────────────────┘');
  console.log('');
  console.log('  ┌─────────────────────────────────────────────────┐');
  console.log('  │ 3. Schema-Driven Development                    │');
  console.log('  │    ✓ Single source of truth                     │');
  console.log('  │    ✓ Changes propagate automatically            │');
  console.log('  │    ✓ Self-documenting code                      │');
  console.log('  └─────────────────────────────────────────────────┘');
  console.log('');
}

function printPerformance(): void {
  console.log(`\n${COLORS.bright}${COLORS.magenta}PERFORMANCE BREAKDOWN${COLORS.reset}`);
  console.log('─'.repeat(60));
  console.log('');
  console.log('  Typical request timing (Layer 0):');
  console.log('');
  console.log('  ┌──────────────────────────────┬─────────┬──────────┐');
  console.log('  │ Stage                        │ Time    │ % Total  │');
  console.log('  ├──────────────────────────────┼─────────┼──────────┤');
  console.log('  │ Client validation            │ <1ms    │ 0.1%     │');
  console.log('  │ HTTP request setup           │ ~5ms    │ 0.4%     │');
  console.log('  │ API route receives           │ ~10ms   │ 0.8%     │');
  console.log('  │ Request validation           │ ~1ms    │ 0.1%     │');
  console.log(`  │ ${COLORS.bright}LLM generation${COLORS.reset}               │ ~1200ms │ ${COLORS.bright}97.4%${COLORS.reset}    │`);
  console.log('  │ Schema validation            │ ~2ms    │ 0.2%     │');
  console.log('  │ Response building            │ ~1ms    │ 0.1%     │');
  console.log('  │ HTTP response                │ ~5ms    │ 0.4%     │');
  console.log('  │ UI rendering                 │ ~7ms    │ 0.6%     │');
  console.log('  ├──────────────────────────────┼─────────┼──────────┤');
  console.log('  │ TOTAL                        │ ~1231ms │ 100%     │');
  console.log('  └──────────────────────────────┴─────────┴──────────┘');
  console.log('');
  console.log('  Key Insight: LLM generation dominates response time.');
  console.log('  Layer 1+ will add streaming for perceived performance.');
  console.log('');
}

function printKeyFiles(): void {
  console.log(`\n${COLORS.bright}${COLORS.blue}KEY FILES TO UNDERSTAND${COLORS.reset}`);
  console.log('─'.repeat(60));
  console.log('');
  console.log('  Read in this order:');
  console.log('');
  console.log('  1️⃣  lib/schemas/support-answer.ts');
  console.log('     └─ The core schema defining all responses');
  console.log('');
  console.log('  2️⃣  lib/ai/prompts.ts');
  console.log('     └─ System prompt that guides the LLM');
  console.log('');
  console.log('  3️⃣  lib/ai/client.ts');
  console.log('     └─ Where generateObject() magic happens');
  console.log('');
  console.log('  4️⃣  app/api/chat/route.ts');
  console.log('     └─ API endpoint tying it all together');
  console.log('');
  console.log('  5️⃣  components/chat/ChatInterface.tsx');
  console.log('     └─ React UI bringing it to life');
  console.log('');
}

// Main execution
console.log('');
printFlow();
printTypeSafety();
printPerformance();
printKeyFiles();

console.log(`${COLORS.bright}${COLORS.green}╔══════════════════════════════════════════════════════════╗${COLORS.reset}`);
console.log(`${COLORS.bright}${COLORS.green}║  Next Steps: Visit http://localhost:3000/debug          ║${COLORS.reset}`);
console.log(`${COLORS.bright}${COLORS.green}║  Read docs/DATA_FLOW.md for detailed explanation        ║${COLORS.reset}`);
console.log(`${COLORS.bright}${COLORS.green}╚══════════════════════════════════════════════════════════╝${COLORS.reset}`);
console.log('');
