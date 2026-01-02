"""
Module 1: Observability Primitives & Instrumentation
====================================================

This implementation demonstrates a baseline telemetry pipeline using FastAPI
and Logfire. The service endpoint mimics real-world processing behavior to
generate meaningful trace data.

Features:
- Auto-instrumentation with Logfire
- Structured logging with queryable context
- Manual spans for granular tracing
- Simulated latency and error conditions
"""

import asyncio
import random
import os
from fastapi import FastAPI, HTTPException
import logfire

# ============================================================================
# PHASE 1: Service Skeleton - Initialize with Auto-Instrumentation
# ============================================================================

# Configure Logfire with explicit service name
# NOTE: For local development without authentication, Logfire will fall back
# to console output. In production, ensure LOGFIRE_TOKEN is set or run `logfire auth`
LOGFIRE_ENABLED = False
try:
    logfire.configure(
        service_name="observability-lab-01",
    )
    LOGFIRE_ENABLED = True
    print("✅ Logfire configured successfully - data will be sent to dashboard")
except Exception as e:
    print(f"⚠️  Logfire configuration note: {e}")
    print("📝 Running in console-only mode. To use Logfire dashboard, run: logfire auth")
    print()
    # Configure minimal setup for demo - console output only
    from logfire import ConsoleOptions
    logfire.configure(
        service_name="observability-lab-01",
        send_to_logfire=False,
        console=ConsoleOptions(colors='auto'),
    )

# Initialize FastAPI application
app = FastAPI(
    title="Observability Lab - Module 1",
    description="FastAPI + Logfire Observability Primitives",
    version="1.0.0",
)

# Apply Logfire auto-instrumentation to FastAPI
# This automatically traces all HTTP requests, responses, and exceptions
# Only instrument if Logfire is fully enabled to avoid version conflicts
if LOGFIRE_ENABLED:
    try:
        logfire.instrument_fastapi(app)
        print("✅ FastAPI auto-instrumentation enabled")
    except Exception as e:
        print(f"⚠️  FastAPI instrumentation warning: {e}")
        print("📝 Continuing with manual spans only")
else:
    print("📝 FastAPI auto-instrumentation disabled in console-only mode")
    print("   Manual spans and logging will still work")

# ============================================================================
# PHASE 2: Structural Depth - Professional Implementation
# ============================================================================


@app.get("/process-order/{order_id}")
async def process_order(order_id: str):
    """
    Process an order with instrumented tracing and structured logging.

    This endpoint demonstrates:
    1. Structured logging with queryable attributes
    2. Manual span creation for granular tracing
    3. Simulated database latency with performance monitoring
    4. Conditional error injection for testing

    Args:
        order_id: Unique identifier for the order

    Returns:
        dict: Order processing result with timing information

    Raises:
        HTTPException: 500 error for order_id="error-test"
    """
    # Phase 3: The Verification Challenge - Conditional Failure
    if order_id == "error-test":
        logfire.error(
            "Order processing failed - simulated crash",
            order_id=order_id,
            error_type="simulated_crash"
        )
        raise HTTPException(
            status_code=500,
            detail="Simulated Crash"
        )

    # Input Validation with Structured Logging
    # NOTE: Using structured arguments (order_id=order_id) instead of
    # string formatting ensures the data is queryable in the dashboard
    logfire.info(
        "Processing order",
        order_id=order_id
    )

    # Create a manual span for the verify_inventory operation
    # This allows us to measure the exact duration of this specific step
    with logfire.span("verify_inventory") as span:
        # Simulate database lookup with random latency (0.1s - 0.5s)
        sleep_time = random.uniform(0.1, 0.5)

        # Attach the sleep time to the span for observability
        span.set_attribute("sleep_duration_seconds", sleep_time)
        span.set_attribute("order_id", order_id)

        # Perform the simulated async work
        await asyncio.sleep(sleep_time)

        # Log a warning if the query is slow (> 0.4s)
        # This simulates detecting performance issues in real queries
        if sleep_time > 0.4:
            logfire.warn(
                "Slow inventory lookup detected",
                order_id=order_id,
                duration_seconds=sleep_time,
                threshold_seconds=0.4
            )

        # Log successful inventory verification
        logfire.info(
            "Inventory verified",
            order_id=order_id,
            duration_seconds=sleep_time
        )

    # Return success response with timing information
    return {
        "status": "success",
        "order_id": order_id,
        "message": "Order processed successfully",
        "inventory_check_duration": round(sleep_time, 3),
    }


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "observability-lab-01",
        "status": "healthy",
        "module": "Module 1: Observability Primitives & Instrumentation"
    }


@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": "observability-lab-01",
        "version": "1.0.0",
    }


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  Observability Lab - Module 1                                ║
    ║  FastAPI + Logfire Observability Primitives                  ║
    ║                                                              ║
    ║  Service: observability-lab-01                               ║
    ║  API Documentation: http://localhost:8000/docs               ║
    ║  Logfire Dashboard: https://logfire.pydantic.dev             ║
    ║                                                              ║
    ║  Test Endpoints:                                             ║
    ║  GET /process-order/regular-123   (normal execution)         ║
    ║  GET /process-order/error-test    (simulated crash)          ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
