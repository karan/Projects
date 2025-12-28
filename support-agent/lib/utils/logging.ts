/**
 * FILE: logging.ts
 * LAYER: 0 (Foundation)
 * PURPOSE: Development logging utilities for debugging and observability
 *
 * CONCEPTS DEMONSTRATED:
 * - Structured logging
 * - Environment-aware logging
 * - Performance measurement
 * - Debugging helpers
 *
 * CHECKPOINT: L0-logging
 *
 * DATA FLOW:
 * [Application Events] → [Logger] → [Console (dev) / External Service (prod)]
 *
 * LEARN MORE:
 * - docs/ARCHITECTURE.md (Observability Strategy)
 * - Layer 1+ will integrate Logfire for production logging
 */

/**
 * Log levels for filtering
 */
export type LogLevel = 'debug' | 'info' | 'warn' | 'error';

/**
 * Structured log entry
 */
interface LogEntry {
  level: LogLevel;
  message: string;
  timestamp: string;
  context?: Record<string, unknown>;
}

/**
 * Logger configuration
 */
interface LoggerConfig {
  /** Minimum level to log (default: 'debug' in dev, 'info' in prod) */
  minLevel: LogLevel;
  /** Enable pretty printing (default: true in dev) */
  pretty: boolean;
  /** Include timestamps (default: true) */
  timestamps: boolean;
}

const LOG_LEVELS: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
};

/**
 * Default configuration based on environment
 */
const defaultConfig: LoggerConfig = {
  minLevel: process.env.NODE_ENV === 'development' ? 'debug' : 'info',
  pretty: process.env.NODE_ENV === 'development',
  timestamps: true,
};

/**
 * Simple logger for Layer 0
 *
 * DESIGN NOTE: This is intentionally basic. Layer 1+
 * will integrate with proper observability tools.
 */
class Logger {
  private config: LoggerConfig;

  constructor(config: Partial<LoggerConfig> = {}) {
    this.config = { ...defaultConfig, ...config };
  }

  /**
   * Core logging method
   */
  private log(level: LogLevel, message: string, context?: Record<string, unknown>): void {
    // Filter by minimum level
    if (LOG_LEVELS[level] < LOG_LEVELS[this.config.minLevel]) {
      return;
    }

    const entry: LogEntry = {
      level,
      message,
      timestamp: new Date().toISOString(),
      context,
    };

    if (this.config.pretty) {
      this.prettyPrint(entry);
    } else {
      console.log(JSON.stringify(entry));
    }
  }

  /**
   * Pretty print for development
   */
  private prettyPrint(entry: LogEntry): void {
    const emoji = {
      debug: '🔍',
      info: 'ℹ️',
      warn: '⚠️',
      error: '❌',
    }[entry.level];

    const timestamp = this.config.timestamps
      ? `[${new Date(entry.timestamp).toLocaleTimeString()}]`
      : '';

    console.log(`${emoji} ${timestamp} ${entry.message}`);

    if (entry.context) {
      console.log('  Context:', entry.context);
    }
  }

  debug(message: string, context?: Record<string, unknown>): void {
    this.log('debug', message, context);
  }

  info(message: string, context?: Record<string, unknown>): void {
    this.log('info', message, context);
  }

  warn(message: string, context?: Record<string, unknown>): void {
    this.log('warn', message, context);
  }

  error(message: string, context?: Record<string, unknown>): void {
    this.log('error', message, context);
  }

  /**
   * Performance measurement helper
   *
   * @example
   * const timer = logger.startTimer('AI Generation');
   * // ... do work
   * timer.end(); // Logs: "AI Generation completed in 1234ms"
   */
  startTimer(label: string): { end: () => void } {
    const start = performance.now();

    return {
      end: () => {
        const duration = Math.round(performance.now() - start);
        this.info(`${label} completed in ${duration}ms`, { duration_ms: duration });
      },
    };
  }
}

/**
 * Global logger instance
 */
export const logger = new Logger();

/**
 * Create a scoped logger with automatic context
 *
 * @example
 * const apiLogger = createScopedLogger('API');
 * apiLogger.info('Request received'); // Logs: "[API] Request received"
 */
export function createScopedLogger(scope: string): Logger {
  return new Logger({
    ...defaultConfig,
  });
}

/**
 * Helper to log schema validation failures
 */
export function logValidationError(
  schema: string,
  error: unknown,
  data: unknown
): void {
  logger.error(`Schema validation failed: ${schema}`, {
    schema,
    error: error instanceof Error ? error.message : String(error),
    data_sample: JSON.stringify(data).slice(0, 200), // First 200 chars
  });
}

/**
 * Helper to log AI generation events
 */
export function logAIGeneration(
  model: string,
  prompt_length: number,
  response_length: number,
  duration_ms: number
): void {
  logger.info('AI generation completed', {
    model,
    prompt_length,
    response_length,
    duration_ms,
    chars_per_second: Math.round(response_length / (duration_ms / 1000)),
  });
}
