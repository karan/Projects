# Observability Lab: FastAPI + Logfire + SQLAlchemy

A comprehensive hands-on lab demonstrating production-ready observability practices using FastAPI, Logfire, and SQLAlchemy.

## Overview

This lab consists of two progressive modules that teach critical observability and performance analysis skills:

- **Module 1**: Observability Primitives & Instrumentation
- **Module 2**: Database Telemetry & Latency Attribution

## Prerequisites

- Python 3.10+
- Basic understanding of:
  - FastAPI or similar web frameworks
  - SQL and relational databases
  - Async/await patterns in Python

## Quick Start

### 1. Install Dependencies

```bash
cd observability-lab
pip install -r requirements.txt
```

### 2. Configure Logfire (Optional)

For full trace visualization in the dashboard:

```bash
logfire auth
```

**Note**: The application works without authentication in console-only mode, which is perfect for learning!

### 3. Run the Application

```bash
python main.py
```

The application will be available at:
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Logfire Dashboard**: https://logfire.pydantic.dev (when authenticated)

## Project Structure

```
observability-lab/
├── main.py              # FastAPI application (Modules 1 & 2)
├── database.py          # SQLAlchemy models and queries (Module 2)
├── requirements.txt     # Python dependencies
├── README.md           # This file (overview)
├── MODULE2.md          # Module 2 detailed documentation
├── TEST_RESULTS.md     # Module 1 test results
└── PR_DESCRIPTION.md   # PR template
```

---

## Module 1: Observability Primitives & Instrumentation

### What You'll Learn

- Auto-instrumentation with Logfire
- Structured logging vs string formatting
- Manual span creation for granular tracing
- Performance monitoring with thresholds
- Error tracking and exception correlation

### Key Endpoints

#### `GET /process-order/{order_id}`

Demonstrates:
- Structured logging with queryable attributes
- Manual span creation (`verify_inventory`)
- Simulated async work with random latency (0.1s-0.5s)
- Warning logs for slow operations (> 0.4s)
- Conditional error injection for testing

**Example Usage:**

```bash
# Regular processing
curl http://localhost:8000/process-order/regular-123

# Simulated error
curl http://localhost:8000/process-order/error-test
```

**What to Look For in Traces:**
- Total request duration
- `verify_inventory` span duration
- Slow query warnings (when duration > 0.4s)
- Exception details for error cases

### Implementation Highlights

```python
# Structured logging - data is queryable!
logfire.info("Processing order", order_id=order_id)

# Manual span for granular tracing
with logfire.span("verify_inventory") as span:
    span.set_attribute("sleep_duration_seconds", sleep_time)
    await asyncio.sleep(sleep_time)

    # Performance monitoring
    if sleep_time > 0.4:
        logfire.warn("Slow query detected", duration_seconds=sleep_time)
```

### Full Documentation

See [TEST_RESULTS.md](TEST_RESULTS.md) for detailed test results and verification.

---

## Module 2: Database Telemetry & Latency Attribution

### What You'll Learn

- **N+1 Query Problem**: The most common performance bug
- **Latency Attribution**: App time vs Database time
- **Query Optimization**: Using JOINs effectively
- **Trace Analysis**: Reading waterfall diagrams
- **Performance Debugging**: Finding real bottlenecks

### The Problem: N+1 Queries

A classic anti-pattern that's easy to write but terrible for performance:

```python
# ❌ BAD: Makes 21 queries (1 + 20)
users = db.query(User).all()  # Query 1
for user in users:  # Loop 20 times
    count = db.query(Order).filter(Order.user_id == user.id).count()  # 20 queries!
```

### The Solution: Single Query with JOIN

```python
# ✅ GOOD: Makes 1 query
db.query(User, func.count(Order.id))\
  .outerjoin(Order)\
  .group_by(User.id)\
  .all()  # 1 query total!
```

### Key Endpoints

#### `GET /users/analytics` (Naive Implementation)

**Purpose**: Intentionally demonstrates the N+1 problem

**Performance**:
- **Queries**: 21 (1 + 20 users)
- **Duration**: ~50ms
- **Database Time**: ~42ms (88% of total)

**What to Look For in Traces**:
- "Staircase" pattern of 21 sequential database spans
- High database time percentage
- N+1 warning in logs

#### `GET /users/analytics/optimized` (Optimized Implementation)

**Purpose**: Shows the correct approach with JOIN

**Performance**:
- **Queries**: 1
- **Duration**: ~8ms
- **Database Time**: ~3ms (37% of total)

**What to Look For in Traces**:
- Single database span
- Much lower total duration
- Balanced app vs database time

### Performance Comparison

| Metric | Naive (N+1) | Optimized | Improvement |
|--------|-------------|-----------|-------------|
| Total Queries | 21 | 1 | **21× fewer** |
| Database Time | ~42ms | ~3ms | **14× faster** |
| Total Time | ~50ms | ~8ms | **6× faster** |

**With 1000 users**: Naive would make **1001 queries**, Optimized still makes **1 query**!

### Example Usage

```bash
# Test the N+1 problem
curl http://localhost:8000/users/analytics | python -m json.tool

# Test the optimized version
curl http://localhost:8000/users/analytics/optimized | python -m json.tool
```

Both return the same data—only the performance differs!

### Full Documentation

See [MODULE2.md](MODULE2.md) for comprehensive documentation, exercises, and troubleshooting.

---

## Database Schema

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_name VARCHAR NOT NULL,
    quantity INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Seed Data**:
- 20 users (`user_01` through `user_20`)
- 40-100 orders (2-5 per user)

---

## API Reference

### Health & Status

#### `GET /`
Root endpoint with service information

**Response:**
```json
{
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
```

#### `GET /health`
Detailed health check

**Response:**
```json
{
  "status": "healthy",
  "service": "observability-lab-01",
  "version": "2.0.0",
  "modules": {
    "module_1": "Observability Primitives & Instrumentation",
    "module_2": "Database Telemetry & Latency Attribution"
  }
}
```

### Module 1 Endpoints

#### `GET /process-order/{order_id}`
Process an order with instrumented tracing

**Parameters:**
- `order_id` (path): Order identifier

**Response:**
```json
{
  "status": "success",
  "order_id": "regular-123",
  "message": "Order processed successfully",
  "inventory_check_duration": 0.234
}
```

**Special Cases:**
- `order_id="error-test"`: Returns 500 error for testing

### Module 2 Endpoints

#### `GET /users/analytics`
Get user analytics with N+1 query pattern (slow)

**Response:**
```json
{
  "implementation": "naive",
  "warning": "This endpoint uses N+1 queries - check traces!",
  "total_users": 20,
  "users": [
    {
      "id": 1,
      "username": "user_01",
      "email": "user01@example.com",
      "order_count": 3
    }
  ]
}
```

#### `GET /users/analytics/optimized`
Get user analytics with optimized query (fast)

**Response:**
```json
{
  "implementation": "optimized",
  "info": "This endpoint uses a single efficient query",
  "total_users": 20,
  "users": [
    {
      "id": 1,
      "username": "user_01",
      "email": "user01@example.com",
      "order_count": 3
    }
  ]
}
```

---

## Key Concepts

### Structured Logging

**❌ String Formatting (Bad)**:
```python
logfire.info(f"Processing order {order_id}")  # Not queryable!
```

**✅ Structured Arguments (Good)**:
```python
logfire.info("Processing order", order_id=order_id)  # Queryable!
```

**Why**: Structured logs allow filtering, searching, and aggregation in the dashboard.

### Manual Spans

Create spans to measure specific operations:

```python
with logfire.span("operation_name") as span:
    span.set_attribute("key", "value")
    # do work
```

**Use Cases**:
- Database queries
- External API calls
- Complex computations
- File I/O operations

### Latency Attribution

**Question**: Is the app slow or is the database slow?

**Answer from Traces**:
```
Total Request Time: 50ms
├─ App Logic: 8ms (16%)
└─ Database Queries: 42ms (84%)
```

**Conclusion**: Database is the bottleneck → optimize queries!

### N+1 Query Problem

**Pattern**: Making N+1 queries when 1 would suffice

**Example**:
```python
# 1 query to get users
users = db.query(User).all()

# N queries to get related data
for user in users:  # N+1 problem!
    orders = db.query(Order).filter(Order.user_id == user.id).all()
```

**Solution**: Use JOIN
```python
# 1 query total
users = db.query(User).options(joinedload(User.orders)).all()
```

**How to Spot**: Look for "staircase" patterns in trace waterfalls

---

## Troubleshooting

### Issue: "Logfire not authenticated"

**Solution**: This is normal! The app works in console-only mode.

To use the dashboard:
```bash
logfire auth
python main.py
```

### Issue: "Database already exists"

**Solution**: Delete and recreate:
```bash
rm observability_lab.db
python main.py
```

### Issue: "Can't see database queries in traces"

**Cause**: Running in console-only mode (no Logfire auth)

**Solution**: Either:
1. Authenticate with `logfire auth` to see full traces
2. Check console output for structured logs

### Issue: "Port 8000 already in use"

**Solution**: Change the port:
```bash
uvicorn main:app --port 8001
```

---

## Learning Path

1. **Start with Module 1**
   - Understand structured logging
   - Learn manual span creation
   - Practice trace analysis

2. **Progress to Module 2**
   - Identify N+1 problems in traces
   - Learn to optimize database queries
   - Master latency attribution

3. **Apply to Your Projects**
   - Add instrumentation to your apps
   - Find performance bottlenecks
   - Optimize based on data, not guesses

---

## Additional Resources

- [Logfire Documentation](https://docs.pydantic.dev/logfire/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [OpenTelemetry Concepts](https://opentelemetry.io/docs/concepts/)

---

## Summary

This lab teaches you to:

✅ Instrument applications with minimal code changes
✅ Use structured logging for better observability
✅ Create manual spans for granular tracing
✅ Identify the N+1 query problem in traces
✅ Optimize database queries using trace data
✅ Attribute latency to the right components
✅ Make data-driven performance decisions

**Remember**: Traces don't lie. Always measure before optimizing!
