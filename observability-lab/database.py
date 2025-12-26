"""
Module 2: Database Telemetry & Latency Attribution
==================================================

This module demonstrates database instrumentation and performance analysis
using SQLAlchemy with Logfire. It includes intentional N+1 query patterns
to visualize performance bottlenecks in traces.

Key Concepts:
- Database auto-instrumentation
- Query execution timing
- N+1 query problem visualization
- Latency attribution (app vs database)
- Query parameter sanitization
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from typing import List
import logfire

# ============================================================================
# PHASE 1: Persistence Layer Integration
# ============================================================================

# Create SQLite database
DATABASE_URL = "sqlite:///./observability_lab.db"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=False,  # Set to True to see SQL in console (noisy)
)

# Create declarative base for models
Base = declarative_base()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def instrument_database():
    """
    Instrument SQLAlchemy for automatic tracing.

    CRITICAL: This must be called AFTER logfire.configure() but BEFORE making any queries.
    This enables automatic tracing of all database operations.
    """
    try:
        logfire.instrument_sqlalchemy(engine=engine)
        logfire.info("SQLAlchemy instrumentation enabled")
    except Exception as e:
        logfire.warn("SQLAlchemy instrumentation skipped", reason=str(e))


# ============================================================================
# Database Models
# ============================================================================

class User(Base):
    """
    User model for demonstrating database queries and N+1 problems.

    Fields:
        id: Primary key
        username: Unique username
        email: User email address
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    # Relationship to orders
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Order(Base):
    """
    Order model for demonstrating JOIN queries and N+1 problems.

    Fields:
        id: Primary key
        user_id: Foreign key to User
        product_name: Name of the product ordered
        quantity: Quantity ordered
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)

    # Relationship to user
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, product='{self.product_name}')>"


# ============================================================================
# Database Initialization
# ============================================================================

def init_db():
    """
    Initialize the database by creating all tables.
    This should be called once at application startup.
    """
    Base.metadata.create_all(bind=engine)
    logfire.info("Database initialized", tables=["users", "orders"])


def get_db():
    """
    Dependency function to get database session.
    Use with FastAPI's Depends() for automatic session management.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# Database Seeding
# ============================================================================

def seed_database():
    """
    Seed the database with mock data for testing.

    Creates:
        - 20 mock users
        - 2-5 orders per user (40-100 total orders)

    This data is used to demonstrate the N+1 query problem.
    """
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            logfire.info("Database already seeded", user_count=existing_users)
            return

        # Create 20 mock users
        users = []
        for i in range(1, 21):
            user = User(
                username=f"user_{i:02d}",
                email=f"user{i:02d}@example.com"
            )
            users.append(user)

        db.add_all(users)
        db.commit()

        # Refresh to get IDs
        for user in users:
            db.refresh(user)

        # Create 2-5 orders for each user
        import random
        orders = []
        products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones",
                   "Webcam", "Microphone", "Desk", "Chair", "USB Cable"]

        for user in users:
            num_orders = random.randint(2, 5)
            for _ in range(num_orders):
                order = Order(
                    user_id=user.id,
                    product_name=random.choice(products),
                    quantity=random.randint(1, 3)
                )
                orders.append(order)

        db.add_all(orders)
        db.commit()

        logfire.info(
            "Database seeded successfully",
            users_created=len(users),
            orders_created=len(orders)
        )

    except Exception as e:
        logfire.error("Failed to seed database", error=str(e))
        db.rollback()
        raise
    finally:
        db.close()


# ============================================================================
# Query Functions - Demonstrating N+1 Problem
# ============================================================================

def get_users_with_order_counts_naive(db: Session) -> List[dict]:
    """
    NAIVE IMPLEMENTATION - N+1 Query Problem

    This function intentionally implements the N+1 query anti-pattern
    to demonstrate how it appears in traces.

    Pattern:
        1. Fetch all users (1 query)
        2. For each user, fetch order count (N queries)

    Total Queries: 1 + N (where N = number of users)

    Returns:
        List of dicts with user info and order count
    """
    with logfire.span("get_users_with_order_counts_naive") as span:
        # Query 1: Fetch all users
        users = db.query(User).all()
        span.set_attribute("users_fetched", len(users))

        result = []

        # N+1 Problem: Loop through users and make individual queries
        for user in users:
            # Query 2, 3, 4, ... N+1: Separate query for EACH user's order count
            # This is the performance killer!
            order_count = db.query(Order).filter(Order.user_id == user.id).count()

            result.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "order_count": order_count
            })

        span.set_attribute("total_queries", 1 + len(users))
        logfire.warn(
            "N+1 query pattern detected",
            total_queries=1 + len(users),
            users=len(users),
            pattern="naive"
        )

        return result


def get_users_with_order_counts_optimized(db: Session) -> List[dict]:
    """
    OPTIMIZED IMPLEMENTATION - Single Query with JOIN

    This function uses a single efficient query with a JOIN to fetch
    all necessary data at once.

    Pattern:
        1. Fetch all users with order counts in ONE query using JOIN + GROUP BY

    Total Queries: 1

    Returns:
        List of dicts with user info and order count
    """
    with logfire.span("get_users_with_order_counts_optimized") as span:
        # Single efficient query using JOIN and aggregation
        # This is the RIGHT way to do it!
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

        results = query.all()
        span.set_attribute("users_fetched", len(results))
        span.set_attribute("total_queries", 1)

        logfire.info(
            "Optimized query executed",
            total_queries=1,
            users=len(results),
            pattern="optimized"
        )

        return [
            {
                "id": row.id,
                "username": row.username,
                "email": row.email,
                "order_count": row.order_count
            }
            for row in results
        ]
