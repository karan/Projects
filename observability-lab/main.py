"""
Observability Lab: FastAPI + Logfire
====================================

A comprehensive hands-on lab demonstrating production-ready observability
practices using FastAPI and Logfire.

Modules:
- Module 1: Observability Primitives & Instrumentation
- Module 2: Database Telemetry & Latency Attribution

Features:
- Auto-instrumentation with Logfire
- Structured logging with queryable context
- Manual spans for granular tracing
- Database query instrumentation
- N+1 query problem visualization
- Performance bottleneck identification
"""

import asyncio
import random
import os
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import logfire

# Import database functionality for Module 2
from database import (
    init_db,
    seed_database,
    get_db,
    instrument_database,
    get_users_with_order_counts_naive,
    get_users_with_order_counts_optimized
)

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

# Instrument database AFTER logfire is configured
instrument_database()

# Initialize FastAPI application
app = FastAPI(
    title="Observability Lab",
    description="FastAPI + Logfire: Modules 1 & 2",
    version="2.0.0",
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


# ============================================================================
# Module 2: Database Telemetry & Latency Attribution
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.

    Initializes the database and seeds it with mock data for testing.
    This runs once when the application starts.
    """
    with logfire.span("startup_initialization"):
        # Initialize database tables
        init_db()

        # Seed database with mock data
        seed_database()

        logfire.info("Application startup complete", modules=["Module 1", "Module 2"])


@app.get("/users/analytics")
async def get_users_analytics_naive(db: Session = Depends(get_db)):
    """
    NAIVE IMPLEMENTATION - Demonstrates N+1 Query Problem

    This endpoint intentionally implements the N+1 query anti-pattern
    to visualize performance issues in traces.

    The Problem:
        1. Fetches all users in one query
        2. For EACH user, makes a separate query for order count
        3. Total queries: 1 + N (where N = number of users)

    What to Look For in Traces:
        - "Staircase" pattern of database spans
        - High "Time in Database" vs "Time in App"
        - 21 separate database query spans (1 + 20 users)

    Returns:
        List of users with their order counts
    """
    with logfire.span("analytics_naive_endpoint") as span:
        logfire.info("Fetching user analytics", implementation="naive", pattern="N+1")

        # This function makes 21 separate database queries!
        result = get_users_with_order_counts_naive(db)

        span.set_attribute("users_returned", len(result))
        span.set_attribute("implementation", "naive")

        return {
            "implementation": "naive",
            "warning": "This endpoint uses N+1 queries - check traces!",
            "total_users": len(result),
            "users": result
        }


@app.get("/users/analytics/optimized")
async def get_users_analytics_optimized(db: Session = Depends(get_db)):
    """
    OPTIMIZED IMPLEMENTATION - Single Efficient Query

    This endpoint demonstrates the correct way to fetch related data
    using a single query with JOIN and GROUP BY.

    The Solution:
        1. Fetches all users WITH order counts in ONE query
        2. Uses SQL JOIN and aggregation
        3. Total queries: 1

    What to Look For in Traces:
        - Single database query span
        - Much lower total duration
        - Minimal "Time in Database"

    Returns:
        List of users with their order counts (same data, better performance)
    """
    with logfire.span("analytics_optimized_endpoint") as span:
        logfire.info("Fetching user analytics", implementation="optimized", pattern="single_query")

        # This function makes only 1 database query!
        result = get_users_with_order_counts_optimized(db)

        span.set_attribute("users_returned", len(result))
        span.set_attribute("implementation", "optimized")

        return {
            "implementation": "optimized",
            "info": "This endpoint uses a single efficient query",
            "total_users": len(result),
            "users": result
        }


# ============================================================================
# Module 1: Health & Status Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "observability-lab-01",
        "status": "healthy",
        "modules": [
            "Module 1: Observability Primitives & Instrumentation",
            "Module 2: Database Telemetry & Latency Attribution"
        ],
        "endpoints": {
            "module_1": ["/process-order/{order_id}"],
            "module_2": ["/users/analytics", "/users/analytics/optimized"]
        }
    }


@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": "observability-lab-01",
        "version": "2.0.0",
        "modules": {
            "module_1": "Observability Primitives & Instrumentation",
            "module_2": "Database Telemetry & Latency Attribution"
        }
    }


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  Observability Lab - Modules 1 & 2                           ║
    ║  FastAPI + Logfire + SQLAlchemy                              ║
    ║                                                              ║
    ║  Service: observability-lab-01                               ║
    ║  API Documentation: http://localhost:8000/docs               ║
    ║  Logfire Dashboard: https://logfire.pydantic.dev             ║
    ║                                                              ║
    ║  Module 1: Observability Primitives                          ║
    ║  GET /process-order/{order_id}    (tracing & logging)        ║
    ║                                                              ║
    ║  Module 2: Database Telemetry & N+1 Problem                  ║
    ║  GET /users/analytics             (N+1 queries - SLOW)       ║
    ║  GET /users/analytics/optimized   (1 query - FAST)           ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
