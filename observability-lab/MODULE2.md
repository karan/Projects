# Module 2: Database Telemetry & Latency Attribution

## Objective

Integrate a relational database (SQLite via SQLAlchemy) into the observability lab and instrument it to visualize query execution, timing, and parameter sanitization within traces. This module demonstrates how to identify and fix the N+1 query problem—one of the most common performance bottlenecks in modern applications.

## Prerequisites

- Completed Module 1
- SQLAlchemy 2.0+
- Basic understanding of relational databases
- Understanding of SQL JOINs

## What You'll Learn

1. **Database Instrumentation**: Automatic tracing of all SQL queries
2. **N+1 Query Problem**: How to identify it in traces
3. **Latency Attribution**: Distinguishing between app logic time and database time
4. **Query Optimization**: Using JOINs to eliminate redundant queries
5. **Performance Analysis**: Reading trace waterfalls to find bottlenecks

## Implementation Overview

### Phase 1: Persistence Layer Integration

**Goal**: Establish a database connection and apply automatic instrumentation.

#### Database Schema

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    user = relationship("User", back_populates="orders")
```

#### Instrumentation Setup

```python
# Create engine
engine = create_engine("sqlite:///./observability_lab.db")

# CRITICAL: Instrument AFTER creating engine, BEFORE making queries
logfire.instrument_sqlalchemy(engine=engine)
```

**Why this order matters**:
- Instrumentation hooks into the engine's connection pool
- Must happen before any queries are executed
- Captures ALL database operations automatically

#### Seed Data

- **20 users**: `user_01` through `user_20`
- **40-100 orders**: 2-5 random orders per user
- **Purpose**: Realistic dataset to demonstrate N+1 problem

### Phase 2: The "Naive" Implementation (The Trap)

**Endpoint**: `GET /users/analytics`

This endpoint **intentionally** implements the N+1 query anti-pattern.

#### The Problem

```python
def get_users_with_order_counts_naive(db: Session) -> List[dict]:
    # Query 1: Fetch all users
    users = db.query(User).all()  # 1 query

    result = []
    for user in users:  # Loop through 20 users
        # Query 2, 3, 4, ... 21: Separate query for EACH user
        order_count = db.query(Order).filter(Order.user_id == user.id).count()
        # ⚠️ This is the performance killer!

        result.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "order_count": order_count
        })

    return result  # Total: 1 + 20 = 21 queries!
```

#### Why This Is Bad

1. **Query Count**: 1 + N queries (where N = number of users)
   - With 20 users: 21 database round trips
   - With 1000 users: 1001 database round trips
   - **Scales linearly with data**

2. **Network Latency**: Each query has overhead
   - Database connection time
   - Query parsing time
   - Result serialization time

3. **Resource Waste**:
   - Database server processes 21 separate queries
   - Application waits for 21 sequential responses
   - Connection pool exhaustion risk

### Phase 3: The Analysis & Refactor

**Endpoint**: `GET /users/analytics/optimized`

This endpoint demonstrates the **correct** approach.

#### The Solution

```python
def get_users_with_order_counts_optimized(db: Session) -> List[dict]:
    # Single efficient query using JOIN + GROUP BY
    query = (
        db.query(
            User.id,
            User.username,
            User.email,
            func.count(Order.id).label("order_count")
        )
        .outerjoin(Order)  # LEFT JOIN to include users with no orders
        .group_by(User.id, User.username, User.email)
    )

    results = query.all()  # Only 1 query!

    return [
        {
            "id": row.id,
            "username": row.username,
            "email": row.email,
            "order_count": row.order_count
        }
        for row in results
    ]
```

#### Why This Is Better

1. **Query Count**: Always 1 query
   - Works with 20 users: 1 query
   - Works with 1000 users: 1 query
   - **Constant performance**

2. **Database Efficiency**:
   - Single query plan
   - Database can optimize the JOIN
   - Indexes can be fully utilized

3. **Network Efficiency**:
   - One round trip to the database
   - Bulk data transfer
   - Minimal latency impact

---

## How to Use

### 1. Start the Application

```bash
cd observability-lab
python main.py
```

The application will:
- Initialize the database
- Create tables (users, orders)
- Seed with 20 users and their orders
- Start the server on port 8000

### 2. Test the Naive Endpoint (N+1 Problem)

```bash
curl http://localhost:8000/users/analytics | python -m json.tool
```

**Expected Response:**
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
    },
    ...
  ]
}
```

### 3. Test the Optimized Endpoint

```bash
curl http://localhost:8000/users/analytics/optimized | python -m json.tool
```

**Expected Response:**
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
    },
    ...
  ]
}
```

**Note**: The data is identical—only the performance differs!

---

## Analyzing the Traces

### In Console Output

When running without Logfire authentication, you'll see:

**Naive Endpoint:**
```
02:43:46.664 analytics_naive_endpoint
02:43:46.665   Fetching user analytics
02:43:46.667   get_users_with_order_counts_naive
02:43:46.716     N+1 query pattern detected  ⚠️
```

**Optimized Endpoint:**
```
02:43:59.216 analytics_optimized_endpoint
02:43:59.216   Fetching user analytics
02:43:59.217   get_users_with_order_counts_optimized
02:43:59.221     Optimized query executed  ✅
```

### In Logfire Dashboard (When Authenticated)

**Naive Endpoint Trace Waterfall:**
```
GET /users/analytics (50ms total)
└─ analytics_naive_endpoint (48ms)
   └─ get_users_with_order_counts_naive (46ms)
      ├─ SELECT users (2ms)          Query 1
      ├─ SELECT count(*) ... user_id=1 (2ms)  Query 2
      ├─ SELECT count(*) ... user_id=2 (2ms)  Query 3
      ├─ SELECT count(*) ... user_id=3 (2ms)  Query 4
      ...
      └─ SELECT count(*) ... user_id=20 (2ms) Query 21
```

**What to Look For:**
1. **"Staircase" Pattern**: 21 sequential database spans
2. **Time in Database**: 21 × 2ms = ~42ms (88% of total time)
3. **Time in App**: ~6ms (12% of total time)
4. **Latency Attribution**: Database is the bottleneck!

**Optimized Endpoint Trace Waterfall:**
```
GET /users/analytics/optimized (8ms total)
└─ analytics_optimized_endpoint (6ms)
   └─ get_users_with_order_counts_optimized (4ms)
      └─ SELECT users LEFT JOIN orders GROUP BY... (3ms)  Single query!
```

**What to Look For:**
1. **Single Database Span**: Only 1 query
2. **Time in Database**: 3ms (37% of total time)
3. **Time in App**: 5ms (63% of total time)
4. **Total Duration**: **6× faster** than naive implementation!

---

## Performance Comparison

| Metric | Naive (N+1) | Optimized | Improvement |
|--------|-------------|-----------|-------------|
| **Total Queries** | 21 | 1 | **21× fewer** |
| **Database Time** | ~42ms | ~3ms | **14× faster** |
| **Total Time** | ~50ms | ~8ms | **6× faster** |
| **Scales With** | Linear (O(n)) | Constant (O(1)) | ∞ better at scale |

**With 1000 users:**
| Metric | Naive (N+1) | Optimized |
|--------|-------------|-----------|
| Queries | 1001 | 1 |
| Est. Time | ~2000ms | ~10ms |

---

## Key Concepts Demonstrated

### 1. **N+1 Query Problem**

**Definition**: Making N+1 database queries when 1 query would suffice.

**Pattern**:
```python
# ❌ BAD: N+1 queries
items = db.query(Item).all()  # Query 1
for item in items:
    related = db.query(Related).filter(Related.item_id == item.id).first()  # N queries
```

```python
# ✅ GOOD: 1 query with JOIN
items = db.query(Item).join(Related).all()  # 1 query
```

**How to Spot in Traces**:
- "Staircase" pattern of database spans
- High count of similar queries
- Database time >> application time

### 2. **Latency Attribution**

**Question**: Is the app slow, or is the database slow?

**Answer from Traces**:
- **Naive**: 88% database time → Database is the bottleneck
- **Optimized**: 37% database time → More balanced

**Why This Matters**:
- Guides optimization efforts
- Prevents premature optimization
- Identifies architectural issues

### 3. **Query Parameter Sanitization**

**Security Feature**: Logfire/OpenTelemetry sanitizes query parameters by default.

**Example Query in Trace**:
```sql
SELECT count(*) FROM orders WHERE user_id = ?
```

**Why**:
- Prevents sensitive data (emails, passwords) from appearing in logs
- Compliance with data privacy regulations
- Trace logs can be shared safely

**To See Parameters** (if needed):
- Configure `include_statement_parameters=True` in instrumentation
- Only do this in development, never in production with sensitive data

### 4. **Database Instrumentation Benefits**

Automatic capture of:
- Query text (sanitized)
- Query duration
- Connection pool usage
- Transaction boundaries
- Error stack traces

**No code changes needed** for basic instrumentation!

---

## Common Mistakes & How to Avoid Them

### ❌ Mistake 1: Not Using JOINs

```python
# BAD: Fetching in loops
users = db.query(User).all()
for user in users:
    user.order_count = db.query(Order).filter(Order.user_id == user.id).count()
```

**Fix**: Use JOIN with aggregation
```python
# GOOD: Single query
db.query(User, func.count(Order.id)).join(Order).group_by(User.id).all()
```

### ❌ Mistake 2: Ignoring Trace Waterfall

**Symptom**: "The endpoint is slow, but I don't know why"

**Fix**:
1. Open Logfire dashboard
2. Find the slow request trace
3. Look at the waterfall
4. Identify the slowest spans
5. Optimize those specific operations

### ❌ Mistake 3: Optimizing the Wrong Thing

**Symptom**: Spent hours optimizing Python code, but endpoint is still slow

**Fix**: Check traces first!
- If 90% of time is in database → optimize queries
- If 90% of time is in app logic → optimize code
- **Don't guess—measure!**

---

## Exercises

### Exercise 1: Find the N+1

Run both endpoints and compare their traces in Logfire:

1. Count the database spans in each trace
2. Measure total database time vs total request time
3. Calculate the percentage of time spent in the database

**Expected Results**:
- Naive: 21 spans, ~85-90% database time
- Optimized: 1 span, ~30-40% database time

### Exercise 2: Scale Test

Modify the seed function to create 100 users instead of 20:

1. Change `range(1, 21)` to `range(1, 101)`
2. Restart the application
3. Test both endpoints
4. Compare the performance degradation

**Expected Results**:
- Naive: ~5× slower (101 queries vs 21)
- Optimized: Minimal change (~10% slower)

### Exercise 3: Add a Third Endpoint

Create a "middle ground" endpoint that uses eager loading:

```python
users = db.query(User).options(joinedload(User.orders)).all()
for user in users:
    user.order_count = len(user.orders)
```

**Questions**:
- How many queries does this make?
- Is it better than naive? Worse than optimized?
- When would this pattern be appropriate?

---

## Troubleshooting

### Issue: "No database spans in traces"

**Cause**: Instrumentation not applied or applied too late

**Fix**: Ensure `instrument_database()` is called after `logfire.configure()` but before any queries

### Issue: "Database already exists" error

**Cause**: Database file already exists from previous run

**Fix**: Delete `observability_lab.db` and restart

```bash
rm observability_lab.db
python main.py
```

### Issue: "Can't see query parameters in traces"

**Cause**: Parameters are sanitized by default

**Fix**: This is intentional! Only show parameters in development:

```python
logfire.instrument_sqlalchemy(engine=engine, enable_commenter=True)
```

---

## Next Steps

After completing this module, you should be able to:

✅ Identify N+1 query problems in production traces
✅ Use trace waterfalls to attribute latency
✅ Optimize database queries using JOINs
✅ Understand when to use eager loading vs JOINs
✅ Read and analyze database query patterns

**Continue to Module 3** (if available) or apply these concepts to your own applications!

---

## Summary

| Concept | Key Takeaway |
|---------|--------------|
| **N+1 Problem** | 1 + N queries when 1 would work—easy to spot in traces as a "staircase" |
| **Latency Attribution** | Traces show WHERE time is spent (app vs database) |
| **Query Optimization** | Use JOINs to fetch related data in one query |
| **Instrumentation** | Automatic—no code changes needed for basic tracing |
| **Traces Don't Lie** | Always check traces before optimizing—measure, don't guess! |

The N+1 query problem is the most common performance bottleneck in modern applications. Seeing it visually in a trace waterfall makes it unforgettable. Once you know what to look for, you'll spot it everywhere!
