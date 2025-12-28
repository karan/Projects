# Setup Instructions - Support Agent Layer 0

> **Quick start**: Get the application running in 3 commands

## Prerequisites

Before you begin, ensure you have:

- **Node.js** 18.0.0 or higher ([Download](https://nodejs.org/))
- **npm** 9.0.0 or higher (comes with Node.js)
- **AI Provider API Key** (one of):
  - [Anthropic API key](https://console.anthropic.com/) (recommended)
  - [OpenAI API key](https://platform.openai.com/)

### Check Your Node.js Version

```bash
node --version
# Should output v18.0.0 or higher
```

---

## Installation

### Step 1: Install Dependencies

```bash
npm install
```

**What this does**:
- Installs Next.js 14+ framework
- Installs Vercel AI SDK for structured generation
- Installs Zod for schema validation
- Installs TypeScript and development tools
- Installs TailwindCSS for styling

**Expected output**:
```
added 523 packages in 45s
```

**Troubleshooting**:
- If you see peer dependency warnings, they're safe to ignore
- If installation fails, try `npm cache clean --force` and retry

---

### Step 2: Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env with your favorite editor
nano .env
# or
code .env
# or
vim .env
```

**Add your API key**:

#### Option A: Using Anthropic (Claude) - Recommended

```bash
# .env file
ANTHROPIC_API_KEY=your_actual_api_key_here

# Optional: specify model
AI_MODEL=claude-3-5-sonnet-20241022
```

**Get your key**: Visit [https://console.anthropic.com/](https://console.anthropic.com/)

#### Option B: Using OpenAI (GPT-4)

```bash
# .env file
OPENAI_API_KEY=your_actual_api_key_here

# Optional: specify model
AI_MODEL=gpt-4-turbo-preview
```

**Get your key**: Visit [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

**Security reminder**: Never commit `.env` files to git! They're automatically ignored.

---

### Step 3: Start Development Server

```bash
npm run dev
```

**Expected output**:
```
> support-agent-layer-0@0.1.0 dev
> next dev

  ▲ Next.js 14.2.0
  - Local:        http://localhost:3000
  - ready in 2.1s
```

**Success!** Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Verification

### Test the Application

1. **Main Chat Interface**: Visit [http://localhost:3000](http://localhost:3000)

2. **Ask a question**: Try "How do I get a refund?"

3. **Expected response**:
   - Answer appears in chat bubble
   - Confidence score shown (0-100%)
   - Category badge displayed
   - Follow-up questions suggested

4. **Debug View**: Visit [http://localhost:3000/debug](http://localhost:3000/debug)
   - Shows schema structure
   - Displays current configuration
   - Example valid objects

### Run Type Check

```bash
npm run type-check
```

**Expected**: No errors

```bash
> tsc --noEmit

# No output = success!
```

### Run ASCII Flow Diagram

```bash
npm run ascii-flow
```

**Expected**: Beautiful ASCII flowchart in your terminal

---

## Configuration Options

### Model Selection

**Anthropic Models** (in `.env`):
```bash
AI_MODEL=claude-3-5-sonnet-20241022    # Recommended: Best balance
AI_MODEL=claude-3-opus-20240229        # Most capable (slower, expensive)
AI_MODEL=claude-3-haiku-20240307       # Fastest (less capable)
```

**OpenAI Models**:
```bash
AI_MODEL=gpt-4-turbo-preview           # Recommended
AI_MODEL=gpt-4                         # Stable
AI_MODEL=gpt-3.5-turbo                 # Faster, cheaper
```

### Generation Settings

Edit `lib/ai/config.ts` to adjust:

```typescript
export const GENERATION_SETTINGS = {
  temperature: 0.7,  // 0.0-1.0 (higher = more creative)
  maxTokens: 2048,   // Max response length
  topP: 1.0,         // Nucleus sampling (0.0-1.0)
};
```

**Temperature guide**:
- `0.0-0.3`: Very consistent, factual
- `0.4-0.7`: Balanced (default)
- `0.8-1.0`: Creative, varied

---

## Troubleshooting

### "No AI provider configured" Error

**Problem**: Environment variables not loaded

**Solution**:
1. Verify `.env` file exists in project root
2. Check file contains `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`
3. Restart dev server (`Ctrl+C`, then `npm run dev`)

### API Key Authentication Errors

**Problem**: "Invalid API key" or 401 errors

**Solution**:
1. Verify key is correct (no extra spaces)
2. Check key hasn't expired
3. Ensure billing is set up on provider account

### TypeScript Errors

**Problem**: Red squiggly lines in editor

**Solution**:
1. Restart TypeScript server in editor
2. Run `npm run type-check` to see actual errors
3. Check `tsconfig.json` paths are correct

### Port 3000 Already in Use

**Problem**: "Port 3000 is already in use"

**Solution**:
```bash
# Option 1: Kill process on port 3000
# macOS/Linux:
lsof -ti:3000 | xargs kill

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Option 2: Use different port
PORT=3001 npm run dev
```

### Slow LLM Responses

**Problem**: Responses taking >5 seconds

**Possible causes**:
1. Using GPT-4 (slower than Claude Sonnet)
2. Network latency
3. High `maxTokens` setting

**Solutions**:
- Switch to faster model (Claude Sonnet, GPT-3.5 Turbo)
- Reduce `maxTokens` in config
- Check internet connection

### Validation Errors

**Problem**: "Schema validation failed"

**What this means**: LLM output doesn't match schema

**Debug steps**:
1. Check server logs in terminal
2. Look for ZodError details
3. Verify schema constraints aren't too strict
4. Test with simpler queries

---

## Development Workflow

### Recommended Setup

1. **Terminal 1**: Run dev server
   ```bash
   npm run dev
   ```

2. **Terminal 2**: Watch for type errors
   ```bash
   npm run type-check -- --watch
   ```

3. **Browser**: DevTools open (F12)
   - Network tab: See API requests
   - Console: Check for errors

### File Watcher

Next.js automatically reloads when you save files:
- ✅ React components
- ✅ API routes
- ✅ Schemas
- ❌ Environment variables (requires restart)

### Code Editor Extensions

**VS Code** (recommended):
- ESLint
- Prettier
- TypeScript and JavaScript Language Features
- Tailwind CSS IntelliSense

---

## Available Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run start` | Run production build |
| `npm run lint` | Run ESLint |
| `npm run type-check` | Check TypeScript types |
| `npm run ascii-flow` | Print ASCII flowchart |

---

## What to Read First

After setup completes successfully, read in this order:

1. **docs/README.md** - Project overview and concept map
2. **lib/schemas/support-answer.ts** - Core schema (15 min)
3. **lib/ai/prompts.ts** - System prompts (10 min)
4. **lib/ai/client.ts** - AI client (15 min)
5. **app/api/chat/route.ts** - API endpoint (10 min)

**Total reading time**: ~1 hour

Then start experiments: **experiments/README.md**

---

## Production Build

When ready to deploy:

```bash
# Build production bundle
npm run build

# Test production build locally
npm run start
```

**Expected build output**:
```
Route (app)                              Size     First Load JS
┌ ○ /                                    137 B          87.2 kB
└ ○ /debug                               145 B          87.3 kB
```

**Deployment options**:
- Vercel (recommended, zero-config)
- Netlify
- Self-hosted with Docker

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | If using Claude | - | Anthropic API key |
| `OPENAI_API_KEY` | If using GPT | - | OpenAI API key |
| `AI_MODEL` | No | Auto-detect | Specific model ID |
| `NODE_ENV` | No | development | Environment mode |

---

## Getting Help

### Check These First

1. **Browser console**: F12 → Console tab
2. **Server logs**: Terminal running `npm run dev`
3. **Network tab**: F12 → Network → /api/chat
4. **Debug view**: [http://localhost:3000/debug](http://localhost:3000/debug)

### Common Issues

- **"Cannot find module"**: Run `npm install`
- **Type errors**: Run `npm run type-check`
- **Stale cache**: Delete `.next` folder and restart
- **Port conflict**: Use `PORT=3001 npm run dev`

### Still Stuck?

1. Read `docs/ARCHITECTURE.md` for design details
2. Check `experiments/README.md` for hands-on practice
3. Review code comments (they're extensive!)

---

## Success Criteria

You've completed setup when you can:

✅ Start dev server without errors
✅ Access [http://localhost:3000](http://localhost:3000)
✅ Ask a question and get a response
✅ See structured data (confidence, category)
✅ Visit debug view at `/debug`
✅ Run `npm run type-check` without errors

**Congratulations!** You're ready to learn. 🎉

---

## Next Steps

1. ✅ Complete setup (you're here!)
2. 📖 Read `docs/README.md`
3. 💻 Study `lib/schemas/support-answer.ts`
4. 🧪 Try `experiments/README.md` Experiment 1
5. 📚 Follow `docs/LEARNING_PATH.md` curriculum

**Happy coding!** 🚀
