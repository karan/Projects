# Pull Request: Module 1 - Observability Primitives & Instrumentation

## Title
```
Add Module 1: Observability Primitives & Instrumentation with FastAPI + Logfire
```

## Description

### Summary

This PR implements **Module 1: Observability Primitives & Instrumentation**, a comprehensive hands-on lab demonstrating production-ready observability practices using FastAPI and Logfire.

### 🎯 What's New

A complete observability lab project with:
- **FastAPI service** with auto-instrumentation
- **Logfire integration** for distributed tracing
- **Structured logging** with queryable attributes
- **Manual span creation** for granular tracing
- **Performance monitoring** with threshold-based alerting
- **Error tracking** with full exception correlation

### 📦 Implementation Breakdown

#### Phase 1: Service Skeleton
- ✅ FastAPI application with proper initialization
- ✅ Logfire configured with service name `observability-lab-01`
- ✅ Auto-instrumentation via `logfire.instrument_fastapi(app)`
- ✅ Graceful fallback to console-only mode for local development

#### Phase 2: Structural Depth (Professional Implementation)
- ✅ `GET /process-order/{order_id}` endpoint
- ✅ **Structured logging** using key-value pairs (not string formatting)
  - Ensures data is queryable in the dashboard
  - Example: `logfire.info("Processing order", order_id=order_id)`
- ✅ Manual `verify_inventory` span with metadata
  - Measures exact duration of specific operations
  - Attaches attributes: `order_id`, `sleep_duration_seconds`
- ✅ Simulated async database lookup (0.1s - 0.5s randomized)
- ✅ **Performance monitoring**: Logs warning when query > 0.4s
- ✅ **Span attributes** for filtering and analysis

#### Phase 3: Verification Challenge
- ✅ Conditional error injection: `order_id="error-test"` raises HTTP 500
- ✅ Structured error logging with context attributes
- ✅ Full exception trace correlation in spans
- ✅ Proper error flag on root span

### 🧪 Test Results

All verification tasks completed successfully:

**Test 1: Regular Order Processing**
```bash
curl http://localhost:8000/process-order/regular-123
```
```json
{
  "status": "success",
  "order_id": "regular-123",
  "inventory_check_duration": 0.483
}
```
- ✅ Slow query detected (0.483s > 0.4s threshold)
- ✅ Warning logged with structured attributes
- ✅ Span waterfall shows 99% time in `verify_inventory`

**Test 2: Error Case**
```bash
curl http://localhost:8000/process-order/error-test
```
```json
{
  "detail": "Simulated Crash"
}
```
- ✅ HTTP 500 status code returned
- ✅ Exception trace captured in span details
- ✅ Structured error log with `order_id` and `error_type` attributes

### 📁 Files Added

```
observability-lab/
├── main.py              # FastAPI app with Logfire (200 lines)
├── requirements.txt     # Dependencies (logfire[fastapi], etc.)
├── README.md           # Complete setup guide (226 lines)
├── TEST_RESULTS.md     # Actual test results & verification (283 lines)
└── .gitignore          # Python/IDE/Logfire ignores
```

Total: **762 lines** of code and documentation

### 🎓 Learning Objectives Demonstrated

1. **Structured Logging vs String Formatting**
   - ✅ Key-value pairs make data queryable
   - ✅ Better than f-strings for observability

2. **Manual Spans for Granular Tracing**
   - ✅ Created `verify_inventory` span
   - ✅ Measured specific operation duration
   - ✅ Attached metadata for filtering

3. **Performance Monitoring**
   - ✅ Threshold-based detection (> 0.4s)
   - ✅ Automatic warning logging
   - ✅ Proactive issue identification

4. **Error Correlation**
   - ✅ Exceptions linked to trace spans
   - ✅ Full stack traces in dashboard
   - ✅ Structured error context

5. **Auto-Instrumentation**
   - ✅ HTTP requests automatically traced
   - ✅ No manual span creation for endpoints
   - ✅ Fallback handling for unauthenticated mode

### 🚀 Usage

```bash
cd observability-lab

# Install dependencies
pip install -r requirements.txt

# Authenticate with Logfire (optional)
logfire auth

# Run the application
python main.py

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/process-order/regular-123
curl http://localhost:8000/process-order/error-test
```

### 📊 Dashboard Features (When Authenticated)

View traces at: https://logfire.pydantic.dev

- **Trace waterfall** showing request breakdown
- **Span attributes** filterable and searchable
- **Exception details** with full stack traces
- **Performance metrics** across all requests
- **Slow query identification** via warnings

### 🔍 Code Quality

- ✅ Comprehensive inline documentation
- ✅ Professional error handling
- ✅ Production-ready patterns
- ✅ Graceful degradation (console-only mode)
- ✅ Type hints and clear naming
- ✅ Follows FastAPI best practices

### 📖 Documentation

- **README.md**: Complete setup, usage, and troubleshooting guide
- **TEST_RESULTS.md**: Actual test outputs with detailed verification
- **Inline comments**: Every observability concept explained
- **Examples**: Curl commands for all endpoints

### ✅ Verification Checklist

- [x] Phase 1: Service skeleton with auto-instrumentation
- [x] Phase 2: Structured logging and manual spans
- [x] Phase 3: Error injection and verification
- [x] Regular order processing tested
- [x] Slow query detection tested
- [x] Error case with exception trace tested
- [x] All test results documented
- [x] README with setup instructions
- [x] Console-only fallback mode working

## Test Plan

To verify this PR:

1. **Install and run:**
   ```bash
   cd observability-lab
   pip install -r requirements.txt
   python main.py
   ```

2. **Test regular order:**
   ```bash
   curl http://localhost:8000/process-order/test-order-1
   # Should return success with duration
   ```

3. **Test error case:**
   ```bash
   curl http://localhost:8000/process-order/error-test
   # Should return 500 error
   ```

4. **Check logs:**
   - Verify structured logging output
   - Confirm slow query warnings when duration > 0.4s
   - Verify error logs for error-test case

5. **(Optional) View in Logfire Dashboard:**
   ```bash
   logfire auth
   python main.py
   # Visit https://logfire.pydantic.dev
   ```

---

This implementation provides a solid foundation for understanding observability primitives and demonstrates production-ready practices for real-world applications.
