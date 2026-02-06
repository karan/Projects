# backend/main.py
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session, relationship, Mapped, mapped_column
from pydantic import BaseModel
from typing import List, Optional

# --- 1. DATABASE CONFIGURATION ---
# Using SQLite for local dev. In prod, switch to PostgreSQL.
DATABASE_URL = "sqlite:///./saas.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# --- 2. DATA MODELS (SQLAlchemy) ---
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)

class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Relationships help us navigate data easily
    tasks = relationship("Task", back_populates="organization")

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    status: Mapped[str] = mapped_column(default="pending")

    # THE KEY TO SAAS: Every piece of data belongs to an Org, not just a user.
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    organization = relationship("Organization", back_populates="tasks")

Base.metadata.create_all(bind=engine)

# --- 3. SCHEMAS (Pydantic V2) ---
# Defines what API requests/responses look like
class OrgCreate(BaseModel):
    name: str

class OrgResponse(BaseModel):
    id: int
    name: str

class TaskCreate(BaseModel):
    title: str

class TaskResponse(BaseModel):
    id: int
    title: str
    status: str

# --- 4. DEPENDENCIES (The "Wiring") ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MOCK AUTH: In real life, decode a JWT here.
# Here, we trust the 'x-user-id' header for demo purposes.
def get_current_user(x_user_id: int = Header(...), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.id == x_user_id))
    if not user:
        # Auto-create user for demo simplicity
        user = User(id=x_user_id, email=f"user{x_user_id}@example.com")
        db.add(user)
        db.commit()
    return user

# CONTEXT AWARENESS: This is the most important part of SaaS architecture.
# We ensure the user actually belongs to the Org they are trying to access.
def get_current_org(
    x_org_id: Optional[int] = Header(None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not x_org_id:
        return None
    org = db.scalar(select(Organization).where(Organization.id == x_org_id, Organization.owner_id == user.id))
    if not org:
        raise HTTPException(status_code=403, detail="Access to Organization denied")
    return org

# --- 5. API ROUTES ---
app = FastAPI()

# CORS config to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/orgs", response_model=OrgResponse)
def create_org(
    org: OrgCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_org = Organization(name=org.name, owner_id=user.id)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org

@app.get("/orgs", response_model=List[OrgResponse])
def list_orgs(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(select(Organization).where(Organization.owner_id == user.id)).all()

@app.post("/tasks", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    # Logic: We inject the 'current_org' dependency. If it fails, this route is blocked.
    org: Organization = Depends(get_current_org),
    db: Session = Depends(get_db)
):
    # Security: We force the organization_id from the context, never from the user input.
    new_task = Task(title=task.title, organization_id=org.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(org: Organization = Depends(get_current_org), db: Session = Depends(get_db)):
    # Security: Database query is scoped to the specific Org ID.
    return db.scalars(select(Task).where(Task.organization_id == org.id)).all()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
