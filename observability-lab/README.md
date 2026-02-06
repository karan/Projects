# Module 1: Observability Primitives & Instrumentation

## Objective

Establish a baseline telemetry pipeline using FastAPI and Logfire. This implementation includes a service endpoint that mimics real-world processing behavior (latency and logic) to generate meaningful trace data.

## Prerequisites

- Python 3.10+
- `fastapi`
- `logfire` (pydantic-logfire)
- `uvicorn`

## Project Structure

```
observability-lab/
├── main.py              # FastAPI application with Logfire instrumentation
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd observability-lab
pip install -r requirements.txt
```

### 2. Configure Logfire

Before running the application, you need to authenticate with Logfire:

```bash
logfire auth
```

This will open a browser window for authentication. Follow the prompts to authenticate your Logfire account.

### 3. Run the Application

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Logfire Dashboard: https://logfire.pydantic.dev

## Implementation Details

### Phase 1: Service Skeleton

✅ **Initialized FastAPI Application**: Standard app entry point with auto-instrumentation

✅ **Configured Logfire**:
- Service name explicitly set to `observability-lab-01`
- Applied `logfire.instrument_fastapi(app)` hook for automatic HTTP tracing

### Phase 2: Structural Depth

✅ **Created Endpoint**: `GET /process-order/{order_id}`

This endpoint performs the following instrumented steps:

1. **Input Validation**: Logs incoming `order_id` using structured arguments
   ```python
   logfire.info('Processing order', order_id=order_id)
   ```
   - Uses structured logging (NOT string formatting)
   - Ensures data is queryable in the dashboard

2. **Simulated Work**:
   - Creates a manual span named `verify_inventory`
   - Uses `asyncio.sleep()` to simulate database lookup (0.1s - 0.5s randomized)
   - Logs a warning if sleep time exceeds 0.4s (simulating slow query detection)
   - Attaches metadata to the span for observability

### Phase 3: Verification Challenge

✅ **The Bug**: Conditional failure for testing

- When `order_id="error-test"`, raises `HTTPException(status_code=500, detail="Simulated Crash")`
- Allows testing error trace propagation

## Testing & Verification Tasks

### Task 1: Regular Order Processing

**Request:**
```bash
curl http://localhost:8000/process-order/regular-123
```

**Expected Response:**
```json
{
  "status": "success",
  "order_id": "regular-123",
  "message": "Order processed successfully",
  "inventory_check_duration": 0.234
}
```

**Verification Steps:**
1. Open Logfire Dashboard: https://logfire.pydantic.dev
2. Navigate to your project: `observability-lab-01`
3. Find the trace for `GET /process-order/regular-123`
4. Examine the trace waterfall:
   - Identify the **total request duration** (root span)
   - Identify the **verify_inventory span duration**
   - Compare the two durations
   - Verify structured attributes are present (order_id, sleep_duration_seconds)

**What to Look For:**
- The `verify_inventory` span should be nested within the HTTP request span
- Span attributes should include `order_id` and `sleep_duration_seconds`
- If the sleep time was > 0.4s, you should see a warning log entry

### Task 2: Simulated Error Case

**Request:**
```bash
curl http://localhost:8000/process-order/error-test
```

**Expected Response:**
```json
{
  "detail": "Simulated Crash"
}
```
(HTTP Status: 500)

**Verification Steps:**
1. Open Logfire Dashboard
2. Navigate to your project: `observability-lab-01`
3. Find the trace for `GET /process-order/error-test`
4. Examine the trace details:
   - Locate the **exception stack trace** within the span details
   - Confirm the 500 error is correctly associated with the root span
   - Verify the error log entry is present with structured attributes

**What to Look For:**
- The root span should be marked as an error (usually highlighted in red)
- The exception details should include the stack trace
- The error log should contain `order_id="error-test"` and `error_type="simulated_crash"`
- The span should show the `HTTPException` was raised

## Key Observability Concepts Demonstrated

1. **Auto-Instrumentation**: FastAPI requests are automatically traced
2. **Structured Logging**: All logs use key-value pairs for queryability
3. **Manual Spans**: Fine-grained tracing of specific operations
4. **Span Attributes**: Attaching metadata to spans for filtering and analysis
5. **Performance Monitoring**: Detecting and logging slow operations
6. **Error Tracking**: Exception propagation and error correlation

## Additional Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Root Endpoint
```bash
curl http://localhost:8000/
```

## Troubleshooting

### Logfire Authentication Issues

If you encounter authentication issues:

```bash
# Re-authenticate
logfire auth

# Check configuration
logfire whoami
```

### Port Already in Use

If port 8000 is already in use:

```bash
# Run on a different port
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Dependencies Not Found

Ensure you're in the correct directory and have installed all dependencies:

```bash
cd observability-lab
pip install -r requirements.txt
```

## Next Steps

After completing this module, you should be able to:

✅ Navigate the Logfire dashboard to find specific traces
✅ Understand the difference between auto-instrumented and manual spans
✅ Identify performance bottlenecks using span durations
✅ Correlate errors with their root causes using trace context
✅ Use structured logging for better observability

## Resources

- [Logfire Documentation](https://docs.pydantic.dev/logfire/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenTelemetry Concepts](https://opentelemetry.io/docs/concepts/)
